from google.appengine.ext import db
from user import User

class Post(db.Model):
    '''A class used to create a Post database table'''
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    author = db.TextProperty()
    user = db.ReferenceProperty(User)
    created = db.DateTimeProperty(auto_now_add = True)