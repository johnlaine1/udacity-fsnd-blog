import os
import jinja2
import webapp2
import hmac
import validate
import time
from post import Post
from user import User
from comment import Comment
import user
from google.appengine.ext import db

SECRET ='ilovemyfamily'

# Declares the directory where the templates are stored for jinja
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


class BaseHandler(webapp2.RequestHandler):
    '''The class creates some generic functions for use in other handlers
    Add all template data to the 'data' dictionary to make it available to 
    templates.
    '''
    
    def __init__(self, request, response):
        '''This is how we call the base class constructor, see this link:
        http://stackoverflow.com/questions/15398179/in-python-webapp2-how-put-a-init-in-a-handler-for-get-and-post
        '''
        self.initialize(request, response)
        self.tpl_data = {}
        self.current_user = None
        # If the user is logged in get thier username, otherwise store None
        username = self.get_cookie('username')
        if (username):
            self.current_user = self.get_user(username)
            self.tpl_data['user'] = self.current_user
            
        self.redirect_for_restricted_paths(request)
        
    def redirect_for_restricted_paths(self, request):
        '''If the user is not logged in and tries to access forbidden pages,
        redirect to login page.
        If the user is logged in and tries to access forbidden pages,
        redirect to front page.
        '''
        restricted_non_user_paths = [
            '/post/create', 
            '/post/update', 
            '/post/delete', 
            '/welcome',
            '/logout',
            '/comment/create',
            '/comment/update',
            '/comment/delete'
        ]
            
        restricted_user_paths = ['/login', '/signup']
        
        if not(self.current_user):
            for path in restricted_non_user_paths:
                if path in request.url:
                    self.redirect('/login')
        elif (self.current_user):
            for path in restricted_user_paths:
                if path in request.url:
                    self.redirect('/')
    
    def get_user(self, username):
        q = db.Query(User)
        q.filter("username =", username)
        return q.get()
        
    def get_cookie(self, name):
        username = self.request.cookies.get(name)
        if (username):
            return self.check_secure_val(username)
        else:
            return None
        
    def set_cookie(self, name, value):
        cookie = self.make_secure_val(value)
        self.response.headers.add_header(
            'Set-Cookie', 
            '%s=%s; Path=/' % (name, str(cookie)))
    
    def hash_str(self, s):
        return hmac.new(SECRET, s).hexdigest()
        
    def make_secure_val(self, s):
        return '%s|%s' % (s, self.hash_str(s))
    
    def check_secure_val(self, h):
        val = h.split('|')[0]
        
        if h == self.make_secure_val(val):
            return val
        else:
            return None

    def render(self, template, **kwargs):
        t = jinja_env.get_template(template)
        self.response.out.write(t.render(data = self.tpl_data))
        
class FrontHandler(BaseHandler):
    def get(self):
        posts = db.Query(Post).order('-created')
        self.tpl_data['posts'] = posts
        self.render('front.html')

class RegistrationHandler(BaseHandler):
    def get(self):
        self.render("registration.html")
        
    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        cookie = self.request.cookies.get('username')
        
        errors = validate.user_validate(username, password, verify, email)
        
        user_exists = self.get_user(username)
        if not errors:
            if not user_exists:
                # Hash the password
                password = self.hash_str(password)
                # Create the user
                user = User(username = username, password = password)
                user.put()
                # Add the user to the global data property
                self.tpl_data['user'] = user
                # Hash the cookie
                cookie = self.make_secure_val(username)
                # Set the cookie
                self.response.headers.add_header('Set-Cookie', 'username=%s; Path=/' % str(cookie))
                # Send the user to the welcome screen
                self.redirect('/welcome')
            else:
                errors['user_exists_error'] = 'That username already exists'
    
        # Send user back to registration page and show them the errors.
        self.tpl_data.update({'username': username, 'email': email, 'errors': errors})
        self.render("registration.html")            

class WelcomeHandler(BaseHandler):
    def get(self):
            posts = db.Query(Post).order('-created')
            self.tpl_data['posts'] = posts
            self.render('welcome.html')

class LoginHandler(BaseHandler):
    def get(self):
        if not(self.current_user):
            self.render('login.html')
        else:
            self.redirect('/')
            
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        user = self.get_user(username)
        
        if user and username and password:
            if self.hash_str(password) == user.password:
                self.set_cookie('username', username)
                self.redirect('/welcome')
        
        self.tpl_data['error'] = "Invalid Login"
        self.render('login.html')

class LogoutHandler(BaseHandler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'username=; Path=/')
        self.redirect('/login')
    
class ViewPostHandler(BaseHandler):
    def get(self, post_id=''):
        post = Post.get_by_id(int(post_id))
        comments = db.get(post.comments)
        comments.reverse()
        self.tpl_data['post'] = post
        self.tpl_data['comments'] = comments
        self.render("post-view.html")
            
class CreatePostHandler(BaseHandler):
    def get(self, post_id=''):
        # If this is the 'update' form a post_id will be passed in. We
        # can then get the post data and populate the form.
        if post_id:
            post = Post.get_by_id(int(post_id))
            
            # If the user is not the author, do not let them edit the post.
            if not(post.user.username == self.current_user.username):
                self.redirect('/post/%s' % post_id)
            else:
                self.tpl_data.update({
                    'update_post': True,
                    'post': post
                })
        self.render('create-post.html')
        
    def post(self, post_id=''):
        subject = self.request.get("subject")
        content = self.request.get("content")
        
        if subject and content:
            # If this is an update, the post_id will be present
            if post_id:
                post = Post.get_by_id(int(post_id))
                post.subject = subject
                post.content = content
                post.put()
            # If this is a new post
            else:
                post = Post(subject = subject, 
                            content = content,
                            user = self.current_user
                            )
                post.put()
            self.redirect('/post/%s' % str(post.key().id()))
        else:
            error = "Please enter a subject and some content."
            self.tpl_data.update({
                'subject': subject, 
                'content': content,
                'error': error
            })
            self.render('create-post.html')            
    
class DeletePostHandler(BaseHandler):
    def get(self, post_id=''):
        post = Post.get_by_id(int(post_id))
        if not(post.user.username == self.current_user.username):
            self.redirect('/post/%s' % post_id)
        else:
            db.delete(post)
            # This is a hack, but the only way I could figure out how to solve
            # the problem. After post is deleted, user is redirected to '/' and
            # the deleted post still shows up. If you refresh the page the post
            # is gone. It's like the page is rendered before the database has
            # a chance to purge the post.
            time.sleep(0.1)
            self.redirect('/')

class CreateCommentHandler(BaseHandler):
    '''This handler both creates and updates comments, if comment_id contains
    a value then we are updating, if not we are creating.
    '''
    def get(self, post_id = '', comment_id = ''):
        if comment_id:
            comment = Comment.get_by_id(int(comment_id))
            
            # If the user is not the author do not let them edit comment.
            if not(comment.user.username == self.current_user.username):
                self.redirect('/comment/%s' % comment_id)
            # Otherwise pass the data along to the template
            else:
                self.tpl_data.update({
                    'update_comment': True,
                    'comment': comment
                })
                
        self.render('create-comment.html')
        
    def post(self, post_id = '', comment_id = ''):
        post = Post.get_by_id(int(post_id))
        subject = self.request.get("subject")
        content = self.request.get("content")
        
        # Check if we have all the data we need from the user
        if subject and content:
            # If this is an update, the comment_id will be present
            if comment_id:
                comment = Comment.get_by_id(int(comment_id))
                comment.subject = subject
                comment.content = content
                comment.put()
            # If this is a new comment, we create the comment then append it
            # to the comment list on the related post.
            else:
                comment = Comment(subject = subject, 
                                  content = content,
                                  user = self.current_user,
                                  post_id = post_id
                                  )
                comment.put()
                # post.comments is a list, append our new comment key to it.
                post.comments.append(comment.key())
                post.put()
            self.redirect('/post/%s' % str(post.key().id()))
        else:
            error = "Please enter a subject and some content."
            self.tpl_data.update({
                'subject': subject,
                'content': content,
                'error': error
            })
            self.render('create-comment.html')
class DeleteCommentHandler(BaseHandler):
    #TODO Delete the comment
    #TODO Remove the reference from the related post
    #TODO Redirect user back to the related post
    pass

class ViewCommentHandler(BaseHandler):
    def get(self, comment_id = ''):
        comment = Comment.get_by_id(int(comment_id))
        self.tpl_data['comment'] = comment
        self.render('comment-view.html')

app = webapp2.WSGIApplication([
    ('/', FrontHandler),
    ('/signup', RegistrationHandler),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/welcome', WelcomeHandler),
    ('/post/create', CreatePostHandler),
    ('/post/update/(\d+)', CreatePostHandler),
    ('/post/delete/(\d+)', DeletePostHandler),
    ('/post/(\d+)', ViewPostHandler),
    ('/post/(\d+)/comment/create', CreateCommentHandler),
    ('/post/(\d+)/comment/update/(\d+)', CreateCommentHandler),
    ('/comment/delete/(\d+)', DeleteCommentHandler),
    ('/comment/(\d+)', ViewCommentHandler)
], debug=True)