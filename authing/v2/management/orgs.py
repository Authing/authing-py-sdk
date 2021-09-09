# coding: utf-8
from .types import ManagementClientOptions
from ..common.graphql import GraphqlClient
from .token_provider import ManagementTokenProvider
from ..common.codegen import QUERY
from ..common.utils import format_authorized_resources
from ..exceptions import AuthingWrongArgumentException, AuthingException

class OrgManagementClient(object):
    """Authing Org Management Client"""

    def __init__(self, options, graphqlClient, tokenProvider):
        # type:(ManagementClientOptions,GraphqlClient,ManagementTokenProvider) -> OrgManagementClient
        self.options = options
        self.graphqlClient = graphqlClient
        self.tokenProvider = tokenProvider

    def create_org(self, name, code=None, description=None):
        data = self.graphqlClient.request(
            query=QUERY["createOrg"],
            params={
                "name": name,
                "code": code,
                "description": description
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["createOrg"]

    def create_node(self, name, org_id, parent_node_id, code=None):
        data = self.graphqlClient.request(
            query=QUERY["addNodeV2"],
            params={
                "orgId": org_id,
                "name": name,
                "parentNodeId": parent_node_id,
                "code": code
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["addNodeV2"]

    def add_roles(self, node_id, role_list, namespace=None):
        """
        给部门批量授权角色

        Args:
            node_id: 组织机构部门的 ID；
            role_list: 角色 code 列表；
            namespace (str): 角色所在的权限分组
        """

        if not isinstance(role_list, list):
            raise AuthingWrongArgumentException('role_list must be a list')

        data = self.graphqlClient.request(
            query=QUERY["assignRole"],
            params={
                "nodeCodes": [node_id],
                "roleCodes": role_list,
                "namespace": namespace
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["assignRole"]

    def remove_roles(self, node_id, role_list, namespace=None):

        if not isinstance(role_list, list):
            raise AuthingWrongArgumentException('role_list must be a list')

        data = self.graphqlClient.request(
            query=QUERY["revokeRole"],
            params={
                "nodeCodes": [node_id],
                "roleCodes": role_list,
                "namespace": namespace
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["revokeRole"]

    def list_roles(self, node_id, namespace=None):
        """
        获取一个部门被授权的角色列表
        Args:
            node_id (str): 组织机构部门的 ID；
            namespace (str): 权限分组的 code；

        """

        data = self.graphqlClient.request(
            query=QUERY['getNodeRoles'],
            params={
                'id': node_id,
                'namespace': namespace,
            },
            token=self.tokenProvider.getAccessToken()
        )
        data = data.get('nodeById')
        if not data:
            raise AuthingException(500, 'department not exists')

        roles = data.get('roles')
        _list, total_count = roles.get('list'), roles.get('totalCount')
        return {
            'totalCount': total_count,
            'list': _list
        }

    def list_authorized_resources(self, node_id, namespace=None, resource_type=None):
        """
        获取一个部门被授权的所有资源。

        Args:
            node_id (str): 组织机构部门的 ID；
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
            if resource_type and resource_type not in valid_resource_types:
                raise AuthingWrongArgumentException('invalid argument: resource_type')

        data = self.graphqlClient.request(
            query=QUERY['listNodeByIdAuthorizedResources'],
            params={
                'id': node_id,
                'namespace': namespace,
                'resourceType': resource_type
            },
            token=self.tokenProvider.getAccessToken()
        )
        data = data.get('nodeById')
        if not data:
            raise AuthingException(500, 'department not exists')

        authorized_resources = data.get('authorizedResources')
        _list, total_count = authorized_resources.get('list'), authorized_resources.get('totalCount')
        _list = format_authorized_resources(_list)
        return {
            'totalCount': total_count,
            'list': _list
        }
