
class HostNotFoundException(Exception):
    def __init__(self, message: str = "Host not Found"):
        super().__init__(message)
        self.statusCode = 701

class NoInternetConnection(Exception):
    def __init__(self, message="No Internet is Available to connect"):
        super().__init__(message)
        self.statusCode = 702
    
class CredentialException(Exception):
    def __init__(self, message: str = "Authentication Failure: Recheck credentials"):
        super().__init__(message)
        self.statusCode = 703

class UnknownException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.statusCode = 700
    
