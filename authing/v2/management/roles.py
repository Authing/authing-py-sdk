from ..management import ManagementClientOptions
from ..common.graphql import GraphqlClient
from .token_provider import ManagementTokenProvider
from ..common.codegen import QUERY


class RolesManagementClient(object):
    """Authing Roles Management Client
    """

    def __init__(self, options: ManagementClientOptions, graphqlClient: GraphqlClient, tokenProvider: ManagementTokenProvider):
        self.options = options
        self.graphqlClient = graphqlClient
        self.tokenProvider = tokenProvider

    def list(self, page=1, limit=10):
        """获取用户池角色列表

        Args:
            page (int, optional): 页码数，从 1 开始，默认为 1 。
            limit (int, optional): 每页个数，默认为 10 。

        Returns:
            [totalCount, _list]: 返回一个 tuple，第一个值为角色总数，第二个为元素为角色详情的列表。
        """
        data = self.graphqlClient.request(
            query=QUERY["roles"], params={
                'page': page,
                'limit': limit
            }, token=self.tokenProvider.getAccessToken())
        totalCount, _list = data['roles']['totalCount'], data['roles']['list']
        return totalCount, _list
