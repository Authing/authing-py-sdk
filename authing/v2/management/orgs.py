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
            if not valid_resource_types.index(resource_type):
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
