# coding: utf-8

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from gql.client import Client
from .. import __version__
from ..exceptions import AuthingException


def execute(self, document, *args, **kwargs):
    if self.schema:
        self.validate(document)

    result = self._get_result(document, *args, **kwargs)
    return result


Client.execute = execute


class GraphqlClient(object):
    def __init__(self, options, endpoint):
        self.options = options
        self.endpoint = endpoint

    def request(self, query, params, token=None):
        # type:(str,dict,str) -> any
        headers = {
            "x-authing-sdk-version": "python:%s" % __version__,
            "x-authing-userpool-id": self.options.user_pool_id
            if hasattr(self.options, "user_pool_id")
            else None,
            "x-authing-request-from": "sdk",
            "x-authing-app-id": self.options.app_id
            if hasattr(self.options, "app_id")
            else None,
            'x-authing-lang': self.options.lang if hasattr(self.options, 'lang') else None
        }
        if token:
            headers["authorization"] = "Bearer %s" % token
        transport = RequestsHTTPTransport(self.endpoint, headers=headers, verify=not self.options.use_unverified_ssl)
        client = Client(transport=transport, fetch_schema_from_transport=True)

        result = client.execute(gql(query), variable_values=params)
        if result.errors:
            errmsg = None
            errcode = None
            for _, err in enumerate(result.errors):
                msg = err["message"]
                errcode, errmsg = msg["code"], msg["message"]
                self.options.on_error(errcode, errmsg)
            raise AuthingException(code=errcode, errmsg=errmsg)
        return result.data
