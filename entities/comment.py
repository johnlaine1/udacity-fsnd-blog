from google.appengine.ext import db
from user import User

class Comment(db.Model):
    '''A class used to manipulate a Comment entity in the appengine datastore.
    
    The comment entity is attached to the post comment by adding it's entity
    key to the related post attribute 'comments'
    
    Attribues
        subject: (string) The subject or title of the comment.
        content: (string) The body or content of the comment.
        user: (reference) A reference to the User entity that created the 
                          comment.
        created: (timestamp) A unix timestamp of the date the comment was 
                             created.
    '''    
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    user = db.ReferenceProperty(User)
    post_id = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add = True)