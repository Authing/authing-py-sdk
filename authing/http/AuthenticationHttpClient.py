# coding: utf-8

from pickle import FALSE
from ..version import __version__
import requests

class AuthenticationHttpClient(object):
    def __init__(self, app_id, host, lang, use_unverified_ssl):
        self.app_id = app_id
        self.host = host
        self.lang = lang
        self.use_unverified_ssl = use_unverified_ssl or FALSE
        self.access_token = None

    def set_access_token(self, access_token):
        self.access_token = access_token

    def request(self, method, url, json=None, **kwargs):
        url = "%s%s" % (self.host, url)

        # 把 json 中为 null 的去掉
        if json:
            json = {k: v for k, v in json.items() if v is not None}
        headers = {
            "x-authing-sdk-version": "python:%s" % __version__,
            "x-authing-request-from": "sdk",
            'x-authing-app-id': self.app_id,
            "x-authing-lang": self.lang
        }
        if self.access_token:
            headers['authorization'] = self.access_token
        verify = not self.use_unverified_ssl
        r = requests.request(method=method, url=url, headers=headers, json=json, verify=verify, **kwargs)
        data = r.json()
        return data
