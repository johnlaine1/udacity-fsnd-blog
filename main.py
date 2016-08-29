import os
import jinja2
import webapp2
import hmac
import validate

from google.appengine.ext import db

SECRET ='ilovemyfamily'

# Declares the directory where the templates are stored for jinja
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class User(db.Model):
    '''A class to create a User database'''
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    email = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add = True)
    
class Post(db.Model):
    '''A class used to create a Post database table'''
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    
def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()
    
def make_secure_val(s):
    return '%s|%s' % (s, hash_str(s))
    
def check_secure_val(h):
    val = h.split('|')[0]
    
    if h == make_secure_val(val):
        return val
    else:
        return None

class Handler(webapp2.RequestHandler):
    '''The class creates some generic functions for use in other handlers'''
    def get_user(self, username):
        q = db.Query(User)
        q.filter("username =", username)
        return q.get()
        
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
        
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
        
class FrontHandler(Handler):
    def get(self):
        self.render('front.html')

class RegistrationHandler(Handler):
    def get(self):
        self.render("registration.html", errors={})
        
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
                password = hash_str(password)
                # Create the user
                user = User(username = username, password = password)
                # Add user to the database
                user.put()
                # Hash the cookie
                cookie = make_secure_val(username)
                # Send the cookie
                self.response.headers.add_header('Set-Cookie', 'username=%s; Path=/' % str(cookie))
                # Redirect
                self.redirect('/welcome')
            else:
                errors['user_exists_error'] = 'That username already exists'
    
        # Send user back to registration page and show them the errors.
        self.render("registration.html", username=username, 
                                         email=email, errors=errors)            

class WelcomeHandler(Handler):
    def get(self):
        username = self.request.cookies.get('username')
        username = check_secure_val(username)
        self.render('welcome.html', username = username)

class LoginHandler(Handler):
    def get(self):
        self.render('login.html')
        
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        user = self.get_user(username)
        
        if user and username and password:
            if hash_str(password) == user.password:
                # Hash the cookie
                cookie = make_secure_val(username)
                # Send the cookie
                self.response.headers.add_header('Set-Cookie', 'username=%s; Path=/' % str(cookie))
                # Redirect
                self.redirect('/welcome')
        
        self.render('login.html', error="Invalid Login")

class LogoutHandler(Handler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'username=; Path=/')
        self.redirect('/signup')
        
app = webapp2.WSGIApplication([
    ('/', FrontHandler),
    ('/signup', RegistrationHandler),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/welcome', WelcomeHandler),
    ('/create-post', CreatePostHandler),
    ('/post/(\d+)', ViewPostHandler)
], debug=True)