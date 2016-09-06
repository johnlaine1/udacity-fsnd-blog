import re


class Validator(object):
    '''A class to validate user input for registration.
    
    Attributes:
        username:
            The username that was passed into the class.
        password:
            The password that was passed into the class.
        verify:
            The verify that was passed into the class.
        email:
            The email that was passed into the class.
        errors: 
            A dict containing error messages related to the user
            input. If there are no errors, an empty dict is returned.
    '''
    
    def __init__(self, username, password, verify, email):
        self.username = username
        self.password = password
        self.verify = verify
        self.email = email
        self.errors = self.get_errors()
        
    def check_username(self):
        '''Check if a username passes a regex.
            
        Returns:
            True if the username matches the regex and false otherwise.
        '''
        
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    
        return USER_RE.match(self.username)
    
    def check_password(self):
        '''Check if a password passes a regex.
        
        Returns:
            True if the password matches the regex and false otherwise.
        '''
        PASS_RE = re.compile(r"^.{3,20}$")
        
        return PASS_RE.match(self.password)
    
    def check_verify(self):
        '''Check if a password and the 'verify password' inputs match
        
        Arguments:
            password: (string) A password.
            verify: (string) The value that should match the password.
            
        Returns:
            True if the 2 strings match, False otherwise.
        '''
        
        if self.password == self.verify:
            return True
        else:
            return False
            
    def check_email(self):
        '''Check if an email passes a regex.
            
        Returns:
            True if the email matches the regex and false otherwise.
        '''
        
        EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
        
        return EMAIL_RE.match(self.email)
        
    def get_errors(self):
        '''Validate user input collected during registraion.
        

        Returns:
            A dictionary mapping 'error type' to 'error message'. An empty dict is
            returned if there are no errors.
        '''
        
        
        errors = {}
        
        if not self.check_username():
            errors['username_error'] = "The username is not valid"
            
        if not self.check_password():
            errors['password_error'] = "The password is not valid"
            
        if not self.check_verify():
            errors['verify_error'] = "The passwords do not match"
    
        if not self.check_email() and self.email:
            errors['email_error'] = "The email address is not valid"
    
        return errors    
    
    