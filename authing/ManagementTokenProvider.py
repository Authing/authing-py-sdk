# coding: utf-8
from this import d
import requests

class ManagementTokenProvider:
    def __init__(self, options):
        self.options = options
        self._accessToken = None
        self._accessTokenExpriredAt = None

    def getAccessToken(self):
        """获取访问Token"""
        resp = requests.request(
            method='POST',
            url='%s/api/v3/get-management-token' % self.options.host,
            json={
                "userPoolId": self.options.user_pool_id,
                "secret": self.options.secret
            }
        )
        # TODO: handle exception
        # TODO: 实现 token 缓存逻辑
        data = resp.json()['data']
        access_token = data['access_token']
        return access_token
