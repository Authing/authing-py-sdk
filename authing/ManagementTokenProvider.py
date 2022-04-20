# coding: utf-8
from this import d
from webbrowser import get
import requests
import base64
import json
import time

from authing.AuthingException import AuthingException

class ManagementTokenProvider:
    def __init__(self, options):
        self.options = options
        self._userpool_id = None
        self._access_token = None
        self._expires_at = None

    def decode_jwt(self, access_token):
        payload = access_token.split(".")[1]
        # Apply padding. Add = until length is multiple of 4
        while len(payload) % 4 != 0:
            payload += "="
        decoded_payload = base64.b64decode(payload)
        decoded_token = json.loads(decoded_payload.decode("utf-8"))
        return decoded_token

    def __get_access_token(self):
        """获取访问Token"""
        resp = requests.request(
            method="POST",
            url="%s/api/v3/get-management-token" % self.options.host,
            json={
                "accessKeyId": self.options.access_key_id,
                "accessKeySecret": self.options.access_key_secret,
            },
        )
        # TODO: 实现 token 缓存逻辑
        data = resp.json()
        code, message, errorCode, data = (
            data.get("code"),
            data.get("message"),
            data.get("errorCode"),
            data.get("data"),
        )
        if code != 200:
            raise AuthingException(code, message, errorCode)
        access_token, expires_in = data.get("access_token"), data.get("expires_in")
        if not access_token:
            raise AuthingException(500, "get access token failed")
        decoded = self.decode_jwt(access_token)
        userpool_id = decoded['scoped_userpool_id']
        self._expires_at = int(time.time()) + expires_in
        self._access_token = access_token
        self._userpool_id = userpool_id
        return access_token, userpool_id

    def get_access_token(self):
        if self._access_token and self._expires_at > int(time.time()):
            return self._access_token, self._userpool_id
        return self.__get_access_token()
