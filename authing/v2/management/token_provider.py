# coding: utf-8

from ..common.codegen import QUERY
from .types import ManagementClientOptions
from ..common.graphql import GraphqlClient
import time


class ManagementTokenProvider:
    def __init__(self, options, graphqlClient):
        # type:(ManagementClientOptions,GraphqlClient) -> ManagementTokenProvider
        self.options = options
        self.graphqlClient = graphqlClient

        self._accessToken = None
        self._accessTokenExpriredAt = None

    def _getClientWhenSdkInit(self):
        res = self.graphqlClient.request(
            query=QUERY["accessToken"],
            params={
                "userPoolId": self.options.user_pool_id,
                "secret": self.options.secret,
            },
        )
        data = res["accessToken"]
        accessToken, iat, exp = data["accessToken"], data["iat"], data["exp"]
        return accessToken, iat, exp

    def getAccessToken(self):
        if self._accessToken and self._accessTokenExpriredAt >= time.time() + 3600:
            return self._accessToken
        accessToken, iat, exp = self._getClientWhenSdkInit()
        self._accessToken = accessToken
        self._accessTokenExpriredAt = exp
        return self._accessToken
