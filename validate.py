'''Helper function related to user input validation.'''

import re

def check_username(username):
    '''Check if a username passes a regex.
    
    Args:
        username: (string) The username to check.
        
    Returns:
        True if the username matches the regex and false otherwise.
    '''
    
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    
    return USER_RE.match(username)
    
def check_password(password):
    '''Check if a password passes a regex.
    
    Args:
        password: (string) The password to check.
        
    Returns:
        True if the password matches the regex and false otherwise.
    '''
    PASS_RE = re.compile(r"^.{3,20}$")
    
    return PASS_RE.match(password)
    
def check_verify(password, verify):
    '''Check if a password and the 'verify password' inputs match
    
    Arguments:
        password: (string) A password.
        verify: (string) The value that should match the password.
        
    Returns:
        True if the 2 strings match, False otherwise.
    '''
    
    if password == verify:
        return True
    else:
        return False
        
def check_email(email):
    '''Check if an email passes a regex.
    
    Args:
        email: (string) The email to check.
        
    Returns:
        True if the email matches the regex and false otherwise.
    '''
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    
    return EMAIL_RE.match(email)
    
def user_validate(username, password, verify, email):
    '''Validate user input collected during registraion.
    
    Args:
        username: (string) A username.
        password: (string) A password.
        verify: (string) A string that should match the password.
        email: (string) An email address.
    
    Returns:
        A dictionary mapping 'error type' to 'error message'. An empty dict is
        returned if there are no errors.
    '''
    
    
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
    
    
    
    