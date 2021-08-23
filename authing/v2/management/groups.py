# coding: utf-8
from .types import ManagementClientOptions
from ..common.graphql import GraphqlClient
from .token_provider import ManagementTokenProvider
from ..common.codegen import QUERY
from ..common.utils import format_authorized_resources, convert_nested_pagination_custom_data_list_to_dict
from ..exceptions import AuthingWrongArgumentException, AuthingException


class GroupsManagementClient(dict):
    """Authing Groups Management Client"""

    def __init__(self, options, graphqlClient, tokenProvider):
        # type:(ManagementClientOptions,GraphqlClient,ManagementTokenProvider) -> GroupsManagementClient
        self.options = options
        self.graphqlClient = graphqlClient
        self.tokenProvider = tokenProvider

    def list(self, page=1, limit=10):
        """获取用户池分组列表

        Args:
            page (int): 页码数，从 1 开始，默认为 1 。
            limit (int): 每页个数，默认为 10 。
        """
        data = self.graphqlClient.request(
            query=QUERY["groups"],
            params={"page": page, "limit": limit},
            token=self.tokenProvider.getAccessToken(),
        )
        return data["groups"]

    def create(self, code, name, description=None):
        """创建分组

        Args:
            code (str): 分组唯一标志符，如 developers
            name (str): 分组名称，如开发者。
            description (str): 描述信息
        """
        data = self.graphqlClient.request(
            query=QUERY["createGroup"],
            params={"code": code, "description": description, "name": name},
            token=self.tokenProvider.getAccessToken(),
        )
        return data["createGroup"]

    def detail(self, code):
        """获取分组详情

        Args:
            code (str): 分组唯一标志符，如 developers
        """
        data = self.graphqlClient.request(
            query=QUERY["group"],
            params={
                "code": code,
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["group"]

    def update(self, code, new_code=None, name=None, description=None):
        # type:(str,str,str,str) -> dict
        """修改分组

        Args:
            code (str): 分组唯一标志符，如 developers
            new_code (str): 新的 code
            name (str): 新的名称
            description (str): 新的描述信息
        """
        data = self.graphqlClient.request(
            query=QUERY["updateGroup"],
            params={"code": code, "description": description, "newCode": new_code, "name": name},
            token=self.tokenProvider.getAccessToken(),
        )
        return data["updateGroup"]

    def delete(self, code):
        """删除分组

        Args:
            code (str): 分组唯一标志符，如 developers
        """
        data = self.graphqlClient.request(
            query=QUERY["deleteGroups"],
            params={
                "codeList": [code],
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["deleteGroups"]

    def delete_many(self, code_list):
        """删除分组

        Args:
            code_list : 分组 code 列表
        """
        data = self.graphqlClient.request(
            query=QUERY["deleteGroups"],
            params={
                "codeList": code_list,
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["deleteGroups"]

    def list_users(self, code, page=1, limit=10, with_custom_data=None):
        """获取用户列表

        Args:
            code : 角色 code 列表
            page (int): 页码数，从 1 开始，默认为 1 。
            limit (int): 每页个数，默认为 10 。
            with_custom_data (bool, optional): 是否获取自定义数据，默认为 false；如果设置为 true，将会在 customData 字段返回用户的所有自定义数据。
        """
        query = QUERY['groupWithUsers'] if not with_custom_data else QUERY['groupWithUsersWithCustomData']
        data = self.graphqlClient.request(
            query=query,
            params={
                "code": code,
                "page": page,
                "limit": limit
            },
            token=self.tokenProvider.getAccessToken(),
        )
        data = data["group"]["users"]
        if with_custom_data:
            convert_nested_pagination_custom_data_list_to_dict(data)
        return data

    def add_users(self, code, user_ids):
        # type:(str,list) -> dict
        """添加用户"""
        data = self.graphqlClient.request(
            query=QUERY["addUserToGroup"],
            params={
                "userIds": user_ids,
                "code": code,
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["addUserToGroup"]

    def remove_users(self, code, user_ids):
        # type:(str,list) -> dict
        """移除用户"""
        data = self.graphqlClient.request(
            query=QUERY["removeUserFromGroup"],
            params={
                "userIds": user_ids,
                "code": code,
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["removeUserFromGroup"]

    def list_authorized_resources(self, code, namespace=None, resource_type=None):
        """
        获取一个分组被授权的所有资源。

        Args:
            code (str): 分组的 code；
            namespace (str): 权限分组的 code；
            resource_type (str): 可选，资源类型，默认会返回所有有权限的资源，现有资源类型如下：
                                - DATA: 数据类型；
                                - API: API 类型数据；
                                - MENU: 菜单类型数据；
                                - BUTTON: 按钮类型数据。
        """
        if resource_type:
            valid_resource_types = [
                'DATA',
                'API',
                'MENU',
                'UI',
                'BUTTON'
            ]
            if not valid_resource_types.index(resource_type):
                raise AuthingWrongArgumentException('invalid argument: resource_type')

        data = self.graphqlClient.request(
            query=QUERY['listGroupAuthorizedResources'],
            params={
                'code': code,
                'namespace': namespace,
                'resourceType': resource_type
            },
            token=self.tokenProvider.getAccessToken()
        )
        data = data.get('group')
        if not data:
            raise AuthingException(500, 'group not exists')
        authorized_resources = data.get('authorizedResources')
        _list, total_count = authorized_resources.get('list'), authorized_resources.get('totalCount')
        _list = format_authorized_resources(_list)
        return {
            'totalCount': total_count,
            'list': _list
        }
