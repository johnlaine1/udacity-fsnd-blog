from google.appengine.ext import db
from user import User
from comment import Comment

class Post(db.Model):
    '''A class used to create a Post entity type for the appengine datastore.
    
    Attribues
        subject: (string) The subject or title of the post.
        content: (string) The body or content of the post.
        user: (reference) A reference to the User entity that created this post.
        comments: (list) A list of comment keys.
        likes: (list) A list of user keys.
        created: (timestamp) A unix timestamp of the date the post was created.
    '''
    
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    user = db.ReferenceProperty(User)
    comments = db.ListProperty(db.Key)
    likes = db.ListProperty(db.Key)
    created = db.DateTimeProperty(auto_now_add = True)