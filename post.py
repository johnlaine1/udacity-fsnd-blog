from google.appengine.ext import db
from user import User
from comment import Comment

class Post(db.Model):
    '''A class used to create a Post database table
    
    comments: A list of comment keys
    likes: A list of user keys
    '''
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    user = db.ReferenceProperty(User)
    comments = db.ListProperty(db.Key)
    likes = db.ListProperty(db.Key)
    created = db.DateTimeProperty(auto_now_add = True)