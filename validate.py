import re

def check_username(username):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    
    # Returns True if username passes, False otherwise
    return USER_RE.match(username)
    
def check_password(password):
    PASS_RE = re.compile(r"^.{3,20}$")
    
    return PASS_RE.match(password)
    
def check_verify(password, verify):
    if password == verify:
        return True
    else:
        return False
        
def check_email(email):
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    
    # Returns True if email passes, False otherwise
    return EMAIL_RE.match(email)
    
def user_validate(username, password, verify, email):
    errors = {}
    
    if not(check_username(username)):
        errors['username_error'] = "The username is not valid"
        
    if not(check_password(password)):
        errors['password_error'] = "The password is not valid"
        
    if not(check_verify(password, verify)):
        errors['verify_error'] = "The passwords do not match"

    if not(check_email(email)) and email:
        errors['email_error'] = "The email address is not valid"

    return errors
    
    
    
    