# coding: utf-8

import sys


class AuthingException(Exception):
    def __init__(self, code, errmsg, errorCode=None):
        self.code = code
        self.message = errmsg
        self.errorCode = errorCode

    def __str__(self):
        message = (
            self.message.encode("utf-8") if sys.version_info[0] == 2 else self.message
        )
        return "Authing Request Error: code={}, message={}, errorCode={}".format(
            self.code, message, self.errorCode
        )
