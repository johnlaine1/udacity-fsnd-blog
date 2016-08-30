import os
import jinja2
import webapp2
import hmac
import validate
from post import Post
from user import User
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
    templates
    '''
    
    def __init__(self, request, response):
        '''This is how we call the base class constructor, see this link:
        http://stackoverflow.com/questions/15398179/in-python-webapp2-how-put-a-init-in-a-handler-for-get-and-post
        '''
        self.initialize(request, response)
        self.data = {}
        # If the a user is logged in get thier username, otherwise store None
        self.data['username'] = self.get_cookie('username')
        
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
        self.response.out.write(t.render(data = self.data))
        
class FrontHandler(BaseHandler):
    def get(self):
        posts = db.Query(Post).order('-created')
        self.data['posts'] = posts
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
                self.data['user'] = user
                # Hash the cookie
                cookie = self.make_secure_val(username)
                # Set the cookie
                self.response.headers.add_header('Set-Cookie', 'username=%s; Path=/' % str(cookie))
                # Send the user to the welcome screen
                self.redirect('/welcome')
            else:
                errors['user_exists_error'] = 'That username already exists'
    
        # Send user back to registration page and show them the errors.
        self.data.update({'username': username, 'email': email, 'errors': errors})
        self.render("registration.html")            

class WelcomeHandler(BaseHandler):
    def get(self):
        self.data['username'] = self.get_cookie('username')
        if self.data['username']:
            self.render('welcome.html')
        else:
            self.redirect('/signup')

class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')
        
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        user = self.get_user(username)
        
        if user and username and password:
            if self.hash_str(password) == user.password:
                self.set_cookie('username', username)
                self.data['username'] = username
                self.redirect('/welcome')
        
        self.data['error'] = "Invalid Login"
        self.render('login.html')

class LogoutHandler(BaseHandler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'username=; Path=/')
        self.redirect('/signup')
    
class CreatePostHandler(BaseHandler):
    '''Creates the content on the Add Post page'''
    def get(self):
        self.render('create-post.html')
        
    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")
        
        if subject and content:
            post = Post(subject = subject, content = content)
            post.put()
            self.redirect('/post/%s' % str(post.key().id()))
        else:
            error = "Please enter a subject and some content."
            self.data.update({
                'subject': subject, 
                'content': content,
                'error': error
            })
            self.render('create-post.html')
    
class ViewPostHandler(BaseHandler):
    def get(self, post_id=''):
        self.data['post'] = Post.get_by_id(int(post_id))
        self.render("view-post.html")

app = webapp2.WSGIApplication([
    ('/', FrontHandler),
    ('/signup', RegistrationHandler),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/welcome', WelcomeHandler),
    ('/create-post', CreatePostHandler),
    ('/post/(\d+)', ViewPostHandler)
], debug=True)