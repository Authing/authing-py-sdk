class AuthingException(Exception):
    def __init__(self, errcode, errmsg):
        self.errcode = errcode
        self.errmsg = errmsg
        self.message = errmsg

    def __str__(self):
        return 'Authing Error: {} {}'.format(self.errcode, self.errmsg)
