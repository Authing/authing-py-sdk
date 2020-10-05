from ..common.codegen import QUERY
from . import ManagementClientOptions
from ..common.graphql import GraphqlClient


class ManagementTokenProvider():
    def __init__(self, options: ManagementClientOptions, graphqlClient: GraphqlClient):
        self.options = options
        self.graphqlClient = graphqlClient

        self._accessToken = None
        self._accessTokenExpriredAt = None

    def _getClientWhenSdkInit(self):
        res = self.graphqlClient.request(query=QUERY["accessToken"], params={
            "userPoolId": self.options.userPoolId,
            "secret": self.options.secret
        })
        return res['accessToken']['accessToken']

    def getAccessToken(self):
        if self._accessToken:
            return self._accessToken
        self._accessToken = self._getClientWhenSdkInit()
        return self._accessToken
