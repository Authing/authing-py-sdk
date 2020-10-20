# coding: utf-8

from .types import ManagementClientOptions
from ..common.graphql import GraphqlClient
from .token_provider import ManagementTokenProvider
from ..common.codegen import QUERY


class RolesManagementClient(object):
    """Authing Roles Management Client
    """

    def __init__(self, options, graphqlClient, tokenProvider):
        # type:(ManagementClientOptions,GraphqlClient,ManagementTokenProvider) -> RolesManagementClient
        self.options = options
        self.graphqlClient = graphqlClient
        self.tokenProvider = tokenProvider

    def list(self, page=1, limit=10):
        # type:(int,int) -> object
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
        return data['roles']

    def create(self,
               code,
               description=None,
               parentCode=None
               ):
        # type:(str,str,str) -> object
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

    def detail(self, code):
        # type:(str) -> object
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

    def update(self, code, description=None, newCode=None):
        # type:(str,str,str) -> object
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

    def delete(self, code):
        # type:(str) -> object
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
        return data['deleteRole']

    def delete_many(self, code_list):
        # type:(object) -> object
        """批量删除角色

        Args:
            code_list : 角色 code 列表
        """
        data = self.graphqlClient.request(
            query=QUERY["deleteRoles"],
            params={
                'codeList': code_list,
            },
            token=self.tokenProvider.getAccessToken()
        )
        return data['deleteRoles']

    def list_users(self, code):
        # type:(str) -> object
        """获取用户列表
        """
        data = self.graphqlClient.request(
            query=QUERY["roleWithUsers"],
            params={
                'code': code,
            },
            token=self.tokenProvider.getAccessToken()
        )
        return data['role']['users']

    def add_users(self, code, userIds):
        # type:(str,object) -> object
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
        return data['assignRole']

    def remove_users(self, code, userIds):
        # type:(str,object) -> object
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
        return data['revokeRole']

    def list_policies(self, code, page=1, limit=10):
        # type:(str,int,int) -> object
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
        return data['policyAssignments']

    def add_policies(self, code, policies):
        # type:(str,object) -> object
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
        return data['addPolicyAssignments']

    def remove_policies(self, code, policies):
        # type:(str,object) -> object
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
        return data['removePolicyAssignments']
