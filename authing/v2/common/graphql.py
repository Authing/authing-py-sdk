from gql import Client, AIOHTTPTransport, gql
from ..management import ManagementClientOptions
from .. import __version__


class GraphqlClient(object):
    def __init__(self, options: ManagementClientOptions, endpoint: ManagementClientOptions):
        self.options = options
        self.endpoint = endpoint

    def request(self, query, params, token: str = None):

        headers = {
            'x-authing-sdk-version': 'py3:%s' % __version__,
            'x-authing-userpool-id': self.options.userPoolId,
            'x-authing-request-from': 'sdk',
        }
        if token:
            headers['authorization'] = 'Bearer %s' % token
        transport = AIOHTTPTransport(self.endpoint, headers=headers)
        client = Client(transport=transport,
                        fetch_schema_from_transport=True)
        result = client.execute(
            gql(query), variable_values=params)
        return result
