
class HostNotFoundException(Exception):
    def __init__(self, message: str = "Host not Found"):
        self.message = message
    
    def __str__(self):
        return self.message

class NoInternetConnection(Exception):
    def __init__(self):
        self.message = "No Internet is Available to connect"
    
    def __str__(self):
        return self.message

class CredentialException(Exception):
    def __init__(self, message: str = "Unable to authenticate, check credentials"):
        self.message = message
    
    def __str__(self):
        return self.message

class UnknownException(BaseException):
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return self.message