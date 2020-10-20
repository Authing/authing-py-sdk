class AuthingException(Exception):
    def __init__(self, code, errmsg):
        self.code = code
        self.message = errmsg

    def __str__(self):
        return 'Authing Error: {} {}'.format(self.code, self.message)
