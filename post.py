from google.appengine.ext import db

class Post(db.Model):
    '''A class used to create a Post database table'''
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    author = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add = True)