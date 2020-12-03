from .. import __version__
import requests


class RestClient(object):
    def __init__(self, options):
        self.options = options

    def request(self, method, url, token=None, **kwargs):
        headers = {
            'x-authing-sdk-version': 'python:%s' % __version__,
            'x-authing-userpool-id': self.options.user_pool_id,
            'x-authing-request-from': 'sdk',
        }
        if token:
            headers['authorization'] = 'Bearer %s' % token
        r = requests.request(
            method=method,
            url=url,
            headers=headers,
            **kwargs
        )
        return r.json()
