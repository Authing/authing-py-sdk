from .. import __version__
from .ManagementTokenProvider import ManagementTokenProvider
import requests

class RestClient(object):
    def __init__(self, options):
        self.options = options
        self.token_provider = ManagementTokenProvider(self.options);

    def request(self, method, url, json=None, **kwargs):
        headers = {
            "x-authing-sdk-version": "python:%s" % __version__,
            "x-authing-userpool-id": self.options.user_pool_id if hasattr(self.options, 'user_pool_id') else None,
            "x-authing-app-id": self.options.app_id if hasattr(self.options, 'app_id') else None,
            "x-authing-request-from": "sdk",
            'x-authing-lang': self.options.lang or ''
        }
        token = self.token_provider.getAccessToken()
        if token:
            headers["authorization"] = "Bearer %s" % token
        verify = not self.options.use_unverified_ssl
        r = requests.request(method=method, url=url, headers=headers, json=json, verify=verify, **kwargs)
        data = r.json()
        return data
