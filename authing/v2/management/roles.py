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
            query=QUERY["roles"],
            params={
                'page': page,
                'limit': limit
            },
            token=self.tokenProvider.getAccessToken()
        )
        totalCount, _list = data['roles']['totalCount'], data['roles']['list']
        return totalCount, _list

    def create(self,
               code: str,
               description: str = None,
               parentCode: str = None
               ):
        """创建角色 

        Args:
            code (str): 角色唯一标志
            description (str, optional): 角色描述
            parentCode (str, optional): 父角色唯一标志
        """
        data = self.graphqlClient.request(
            query=QUERY["createRole"],
            params={
                'code': code,
                'description': description,
                'parentCode': parentCode
            },
            token=self.tokenProvider.getAccessToken()
        )
        return data['createRole']

    def detail(self, code: str):
        """获取角色详情

        Args:
            code (str): 角色唯一标志
        """
        data = self.graphqlClient.request(
            query=QUERY["role"],
            params={
                'code': code,
            },
            token=self.tokenProvider.getAccessToken()
        )
        return data['role']

    def update(self, code: str, description: str = None, newCode: str = None):
        """修改角色资料

        Args:
            code (str): 角色唯一标志
            description (str, optional): 角色描述
            newCode (str, optional): 新的 code
        """
        data = self.graphqlClient.request(
            query=QUERY["updateRole"],
            params={
                'code': code,
                'description': description,
                'newCode': newCode
            },
            token=self.tokenProvider.getAccessToken()
        )
        return data['updateRole']

    def delete(self, code: str):
        """删除角色

        Args:
            code (str): 角色唯一标志
        """
        data = self.graphqlClient.request(
            query=QUERY["deleteRole"],
            params={
                'code': code,
            },
            token=self.tokenProvider.getAccessToken()
        )
        code, message = data['deleteRole']['code'], data['deleteRole']['message']
        return code, message

    def delete_many(self, code_list):
        """批量删除角色

        Args:
            code_list : 角色 code 列表
        """
        data = self.graphqlClient.request(
            query=QUERY["deleteRoles"],
            params={
                'codes': code_list,
            },
            token=self.tokenProvider.getAccessToken()
        )
        code, message = data['deleteRoles']['code'], data['deleteRoles']['message']
        return code, message

    def list_users(self, code: str):
        """获取用户列表
        """
        data = self.graphqlClient.request(
            query=QUERY["roleWithUsers"],
            params={
                'code': code,
            },
            token=self.tokenProvider.getAccessToken()
        )
        data = data['role']['users']
        totalCount, _list = data['totalCount'], data['list']
        return totalCount, _list

    def add_users(self, code, userIds):
        """添加用户
        """
        data = self.graphqlClient.request(
            query=QUERY['assignRole'],
            params={
                'userIds': userIds,
                'roleCodes': [code],
            },
            token=self.tokenProvider.getAccessToken()
        )
        code, message = data['assignRole']['code'], data['assignRole']['message']
        return code, message

    def remove_users(self, code: str, userIds):
        """移除用户
        """
        data = self.graphqlClient.request(
            query=QUERY['revokeRole'],
            params={
                'userIds': userIds,
                'roleCodes': [code],
            },
            token=self.tokenProvider.getAccessToken()
        )
        code, message = data['revokeRole']['code'], data['revokeRole']['message']
        return code, message

    def list_policies(self, code: str, page=1, limit=10):
        """获取策略列表
        """
        data = self.graphqlClient.request(
            query=QUERY["policyAssignments"],
            params={
                'targetType': 'ROLE',
                'targetIdentifier': code,
                'page': page,
                'limit': limit
            },
            token=self.tokenProvider.getAccessToken()
        )
        totalCount, _list = data['policyAssignments']['totalCount'], data['policyAssignments']['list']
        return totalCount, _list

    def add_policies(self, code, policies):
        """添加策略
        """
        data = self.graphqlClient.request(
            query=QUERY["addPolicyAssignments"],
            params={
                'policies': policies,
                'targetType': 'ROLE',
                'targetIdentifiers': [code]
            },
            token=self.tokenProvider.getAccessToken()
        )
        code, message = data['addPolicyAssignments']['code'], data['addPolicyAssignments']['message']
        return code, message

    def remove_policies(self, code, policies):
        """移除策略
        """
        data = self.graphqlClient.request(
            query=QUERY["removePolicyAssignments"],
            params={
                'policies': policies,
                'targetType': 'ROLE',
                'targetIdentifiers': [code]
            },
            token=self.tokenProvider.getAccessToken()
        )
        code, message = data['removePolicyAssignments']['code'], data['removePolicyAssignments']['message']
        return code, message
