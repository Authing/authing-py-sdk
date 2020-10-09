# coding: utf-8

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from ..management.types import ManagementClientOptions
from .. import __version__


class GraphqlClient(object):
    def __init__(self, options, endpoint):
        # type:(ManagementClientOptions,str) -> GraphqlClient
        self.options = options
        self.endpoint = endpoint

    def request(self, query, params, token=None):
        # type:(str,dict,str) -> any
        headers = {
            'x-authing-sdk-version': 'py2:%s' % __version__,
            'x-authing-userpool-id': self.options.user_pool_id,
            'x-authing-request-from': 'sdk',
        }
        if token:
            headers['authorization'] = 'Bearer %s' % token
        transport = RequestsHTTPTransport(self.endpoint, headers=headers)
        client = Client(transport=transport,
                        fetch_schema_from_transport=True)
        result = client.execute(
            gql(query), variable_values=params)
        return result
