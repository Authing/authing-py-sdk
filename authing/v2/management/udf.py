# coding: utf-8

from .types import ManagementClientOptions
from ..common.graphql import GraphqlClient
from .token_provider import ManagementTokenProvider
from ..common.codegen import QUERY


class UdfManagementClient(object):
    """Authing User Defined Field Management Client
    """

    def __init__(self, options, graphqlClient, tokenProvider):
        # type:(ManagementClientOptions,GraphqlClient,ManagementTokenProvider) -> UdfManagementClient
        self.options = options
        self.graphqlClient = graphqlClient
        self.tokenProvider = tokenProvider

    def list(self, targetType):
        # type:(str) -> object
        """获取自定义字段定义
        """
        data = self.graphqlClient.request(
            query=QUERY["udf"],
            params={
                'targetType': targetType,
            },
            token=self.tokenProvider.getAccessToken()
        )
        return data['udf']

    def set(self, targetType, key, dataType, label):
        # type:(str,str,str,str,str) -> object
        """添加自定义字段定义
        """
        data = self.graphqlClient.request(
            query=QUERY["setUdf"],
            params={
                'targetType': targetType,
                'key': key,
                'dataType': dataType,
                'label': label
            },
            token=self.tokenProvider.getAccessToken()
        )
        return data['setUdf']

    def remove(self, targetType, key):
        # type:(str,str) -> object
        """删除自定义字段定义
        """
        data = self.graphqlClient.request(
            query=QUERY["removeUdf"],
            params={
                'targetType': targetType,
                'key': key,
            },
            token=self.tokenProvider.getAccessToken()
        )
        return data['removeUdf']
