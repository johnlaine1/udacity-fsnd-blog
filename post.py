from google.appengine.ext import db
from user import User
from comment import Comment

class Post(db.Model):
    '''A class used to create a Post database table'''
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    user = db.ReferenceProperty(User)
    comments = db.ListProperty(db.Key)
    created = db.DateTimeProperty(auto_now_add = True)