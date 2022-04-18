# coding: utf-8

class ManagementTokenProvider:
    def __init__(self, options):
        self.options = options
        self._accessToken = None
        self._accessTokenExpriredAt = None

    def getAccessToken(self):
        """获取访问Token"""
        return "REPACE ME"
