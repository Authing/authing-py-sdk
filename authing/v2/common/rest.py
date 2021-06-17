from .. import __version__
import requests

from ..exceptions import AuthingWrongArgumentException


class RestClient(object):
    def __init__(self, options):
        self.options = options

    def request(self, method, url, token=None, basic_token=None, json=None, auto_parse_result=False, **kwargs):
        headers = {
            "x-authing-sdk-version": "python:%s" % __version__,
            "x-authing-userpool-id": self.options.user_pool_id if hasattr(self.options, 'user_pool_id') else None,
            "x-authing-app-id": self.options.app_id if hasattr(self.options, 'app_id') else None,
            "x-authing-request-from": "sdk",
            'x-authing-lang': self.options.lang or ''
        }
        if token:
            headers["authorization"] = "Bearer %s" % token

        elif basic_token:
            headers['authorization'] = "Basic %s" % basic_token

        if json is not None:
            if not isinstance(json, dict):
                raise AuthingWrongArgumentException('json must be a dict')
            for key in list(json.keys()):
                if json[key] is None:
                    del json[key]

        verify = not self.options.use_unverified_ssl
        r = requests.request(method=method, url=url, headers=headers, json=json, verify=verify, **kwargs)
        data = r.json()
        if auto_parse_result:
            code, data, message = data.get("code"), data.get("data"), data.get("message")
            if code == 200:
                return data
            else:
                self.options.on_error(code, message)
        else:
            return data
