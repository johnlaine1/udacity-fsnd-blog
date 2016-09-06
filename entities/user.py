from google.appengine.ext import db

class User(db.Model):
    '''A class used to manipulate a User entity in the appengine datastore.
    
    Attributes
        username: (string) A unique username.
        password: (string) A hashed password.
        email: (string) A unique password.
        created: (timestamp) The date the user was created.
    '''
    
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    email = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add = True)