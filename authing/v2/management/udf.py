from .types import ManagementClientOptions
from ..common.graphql import GraphqlClient
from .token_provider import ManagementTokenProvider
from ..common.codegen import QUERY


class UdfManagementClient(object):
    """Authing User Defined Field Management Client
    """

    def __init__(self, options: ManagementClientOptions, graphqlClient: GraphqlClient, tokenProvider: ManagementTokenProvider):
        self.options = options
        self.graphqlClient = graphqlClient
        self.tokenProvider = tokenProvider

    def list(self, targetType):
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

    def add(self, targetType, key, dataType, label):
        """添加自定义字段定义
        """
        data = self.graphqlClient.request(
            query=QUERY["addUdf"],
            params={
                'targetType': targetType,
                'key': key,
                'dataType': dataType,
                'label': label
            },
            token=self.tokenProvider.getAccessToken()
        )
        return data['addUdf']

    def remove(self, targetType, key):
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
