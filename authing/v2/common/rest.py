from .. import __version__
import requests


class RestClient(object):
    def __init__(self, options):
        self.options = options

    def request(self, method, url, token=None, basic_token=None, **kwargs):
        headers = {
            "x-authing-sdk-version": "python:%s" % __version__,
            "x-authing-userpool-id": self.options.user_pool_id if hasattr(self.options, 'user_pool_id') else None,
            "x-authing-app-id": self.options.app_id,
            "x-authing-request-from": "sdk",
            'x-authing-lang': self.options.lang or ''
        }
        if token:
            headers["authorization"] = "Bearer %s" % token

        elif basic_token:
            headers['authorization'] = "Basic %s" % basic_token

        r = requests.request(method=method, url=url, headers=headers, **kwargs)
        return r.json()
