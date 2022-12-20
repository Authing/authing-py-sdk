# coding: utf-8

from pickle import FALSE
from ..version import __version__
import requests


class ProtocolHttpClient(object):
    def __init__(self, host, use_unverified_ssl):
        self.host = host
        self.use_unverified_ssl = use_unverified_ssl or FALSE

    def request(self, method, url, basic_token=None, bearer_token=None, raw_content=False, json=None, **kwargs):
        url = "%s%s" % (self.host, url)
        headers = {}
        if basic_token:
            headers["authorization"] = "Basic %s" % basic_token
        if bearer_token:
            headers["authorization"] = "Bearer %s" % bearer_token
        # 把 json 中为 null 的去掉
        if json:
            json = {k: v for k, v in json.items() if v is not None}
        verify = not self.use_unverified_ssl
        r = requests.request(
            method=method, url=url, json=json, headers=headers, verify=verify, **kwargs
        )
        data = r.json() if not raw_content else r.text
        return data
