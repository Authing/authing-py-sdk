# coding: utf-8

import sys


class AuthingException(Exception):
    def __init__(self, statusCode, errmsg, apiCode=None):
        self.statusCode = statusCode
        self.message = errmsg
        self.apiCode = apiCode

    def __str__(self):
        message = (
            self.message.encode("utf-8") if sys.version_info[0] == 2 else self.message
        )
        return "Authing Request Error: statusCode={}, message={}, apiCode={}".format(
            self.statusCode, message, self.apiCode
        )
