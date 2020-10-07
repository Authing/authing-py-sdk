from ..common.codegen import QUERY
from .types import ManagementClientOptions
from ..common.graphql import GraphqlClient
from .token_provider import ManagementTokenProvider


class PolicyManagementClient(object):
    """Authing Policy Management Client
    """

    def __init__(self, options: ManagementClientOptions, graphqlClient: GraphqlClient, tokenProvider: ManagementTokenProvider):
        self.options = options
        self.graphqlClient = graphqlClient
        self.tokenProvider = tokenProvider

    def list(self, page=1, limit=10):
        """获取策略列表

        Args:
            page (int, optional): 页码数，从 1 开始，默认为 1 。
            limit (int, optional): 每页个数，默认为 10 。
        """
        data = self.graphqlClient.request(
            query=QUERY["policies"],
            params={
                'page': page,
                'limit': limit
            },
            token=self.tokenProvider.getAccessToken()
        )
        return data['policies']

    def create(self, code, statements, description=None):
        """创建策略
        """
        data = self.graphqlClient.request(
            query=QUERY["createPolicy"],
            params={
                'code': code,
                'description': description,
                'statements': statements
            },
            token=self.tokenProvider.getAccessToken()
        )
        return data['createPolicy']

    def detail(self, code: str):
        """获取策略详情
        """
        data = self.graphqlClient.request(
            query=QUERY["policy"],
            params={
                'code': code,
            },
            token=self.tokenProvider.getAccessToken()
        )
        return data['policy']

    def update(self, code: str, statements, description: str = None, ):
        """修改策略
        """
        data = self.graphqlClient.request(
            query=QUERY["updatePolicy"],
            params={
                'code': code,
                'description': description,
                'statements': statements
            },
            token=self.tokenProvider.getAccessToken()
        )
        return data['updatePolicy']

    def delete(self, code: str):
        """删除策略
        """
        data = self.graphqlClient.request(
            query=QUERY["deletePolicy"],
            params={
                'code': code,
            },
            token=self.tokenProvider.getAccessToken()
        )
        return data['deletePolicy']

    def delete_many(self, code_list):
        """批量删除策略
        """
        data = self.graphqlClient.request(
            query=QUERY["deletePolicies"],
            params={
                'codes': code_list,
            },
            token=self.tokenProvider.getAccessToken()
        )
        return data['deletePolicies']

    def list_assignments(self, code, page=1, limit=10):
        """获取授权记录
        """
        data = self.graphqlClient.request(
            query=QUERY["policyAssignments"],
            params={
                'code': code,
                'page': page,
                'limit': limit
            },
            token=self.tokenProvider.getAccessToken()
        )
        return data['policyAssignments']

    def add_assignments(self, policies, targetType, targetIdentifiers):
        """添加授权
        """
        data = self.graphqlClient.request(
            query=QUERY["addPolicyAssignments"],
            params={
                'policies': policies,
                'targetType': targetType,
                'targetIdentifiers': targetIdentifiers
            },
            token=self.tokenProvider.getAccessToken()
        )
        return data['addPolicyAssignments']

    def remove_assignments(self, policies, targetType, targetIdentifiers):
        """删除授权
        """
        data = self.graphqlClient.request(
            query=QUERY["removePolicyAssignments"],
            params={
                'policies': policies,
                'targetType': targetType,
                'targetIdentifiers': targetIdentifiers
            },
            token=self.tokenProvider.getAccessToken()
        )
        return data['removePolicyAssignments']
