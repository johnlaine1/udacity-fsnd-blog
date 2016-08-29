from google.appengine.ext import db

class User(db.Model):
    '''A class to create a User database'''
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    email = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add = True)