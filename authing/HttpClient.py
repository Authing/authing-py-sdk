# coding: utf-8

from .version import __version__
from .ManagementTokenProvider import ManagementTokenProvider
import requests

class HttpClient(object):
    def __init__(self, options):
        self.options = options
        self.token_provider = ManagementTokenProvider(self.options);

    def request(self, method, url, json=None, **kwargs):
        url = "%s%s" % (self.options.host, url)

        # 把 json 中为 null 的去掉
        if json:
            json = {k: v for k, v in json.items() if v is not None}
        token, userpool_id = self.token_provider.get_access_token()
        headers = {
            "x-authing-sdk-version": "python:%s" % __version__,
            "x-authing-userpool-id": userpool_id if userpool_id else None,
            "x-authing-request-from": "sdk",
            'x-authing-lang': self.options.lang or ''
        }
        if token:
            headers["authorization"] = "Bearer %s" % token
        verify = not self.options.use_unverified_ssl
        r = requests.request(method=method, url=url, headers=headers, json=json, verify=verify, **kwargs)
        data = r.json()
        return data
