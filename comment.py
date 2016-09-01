from google.appengine.ext import db
from user import User

class Comment(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    user = db.ReferenceProperty(User)
    post_id = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add = True)