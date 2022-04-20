# coding: utf-8
from this import d
from webbrowser import get
import requests

from authing.AuthingException import AuthingException


class ManagementTokenProvider:
    def __init__(self, options):
        self.options = options
        self._accessToken = None
        self._accessTokenExpriredAt = None

    def getAccessToken(self):
        """获取访问Token"""
        resp = requests.request(
            method="POST",
            url="%s/api/v3/get-management-token" % self.options.host,
            json={
                "userPoolId": self.options.user_pool_id,
                "secret": self.options.secret,
            },
        )
        # TODO: 实现 token 缓存逻辑
        data = resp.json()
        code, message, errorCode, data = (
            data.get('code'),
            data.get('message'),
            data.get('errorCode'),
            data.get('data'),
        )
        if code != 200:
            raise AuthingException(code, message, errorCode)
        access_token, expires_in = data.get('access_token'), data.get('expires_in')
        if not access_token:
            raise AuthingException(500, 'get access token failed')
        return access_token
