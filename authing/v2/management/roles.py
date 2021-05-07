# coding: utf-8
import json

from .types import ManagementClientOptions
from ..common.graphql import GraphqlClient
from .token_provider import ManagementTokenProvider
from ..common.codegen import QUERY
from ..common.utils import format_authorized_resources, convert_udv_list_to_dict, convert_nested_pagination_custom_data_list_to_dict
from ..exceptions import AuthingWrongArgumentException, AuthingException
import datetime


class RolesManagementClient(object):
    """Authing Roles Management Client"""

    def __init__(self, options, graphqlClient, tokenProvider):
        # type:(ManagementClientOptions,GraphqlClient,ManagementTokenProvider) -> RolesManagementClient
        self.options = options
        self.graphqlClient = graphqlClient
        self.tokenProvider = tokenProvider

    def list(self, page=1, limit=10, namespace=None):
        """获取用户池角色列表

        Args:
            page (int): 页码数，从 1 开始，默认为 1 。
            limit (int): 每页个数，默认为 10 。
            namespace (str): 权限分组 code。

        Returns:
            [totalCount, _list]: 返回一个 tuple，第一个值为角色总数，第二个为元素为角色详情的列表。
        """
        data = self.graphqlClient.request(
            query=QUERY["roles"],
            params={"page": page, "limit": limit, "namespace": namespace},
            token=self.tokenProvider.getAccessToken(),
        )
        return data["roles"]

    def create(self, code, description=None, parentCode=None, namespace=None):
        """创建角色

        Args:
            code (str): 角色唯一标志
            description (str): 角色描述
            parentCode (str): 父角色唯一标志
            namespace (str): 权限分组 code。
        """
        data = self.graphqlClient.request(
            query=QUERY["createRole"],
            params={"code": code, "description": description, "parentCode": parentCode, "namespace": namespace},
            token=self.tokenProvider.getAccessToken(),
        )
        return data["createRole"]

    def detail(self, code, namespace=None):
        """获取角色详情

        Args:
            code (str): 角色唯一标志
            namespace (str): 权限分组 code。
        """
        data = self.graphqlClient.request(
            query=QUERY["role"],
            params={
                "code": code,
                "namespace": namespace
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["role"]

    def update(self, code, description=None, newCode=None, namespace=None):
        # type:(str,str,str,str) -> object
        """修改角色资料

        Args:
            code (str): 角色唯一标志
            description (str): 角色描述
            newCode (str): 新的 code
            namespace (str): 权限分组 code。
        """
        data = self.graphqlClient.request(
            query=QUERY["updateRole"],
            params={"code": code, "description": description, "newCode": newCode, "namespace": namespace},
            token=self.tokenProvider.getAccessToken(),
        )
        return data["updateRole"]

    def delete(self, code, namespace=None):
        """删除角色

        Args:
            code (str): 角色唯一标志
            namespace (str): 权限分组 code。
        """
        data = self.graphqlClient.request(
            query=QUERY["deleteRole"],
            params={
                "code": code,
                "namespace": namespace
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["deleteRole"]

    def delete_many(self, code_list, namespace=None):
        """批量删除角色

        Args:
            code_list : 角色 code 列表
            namespace (str): 权限分组 code。
        """
        data = self.graphqlClient.request(
            query=QUERY["deleteRoles"],
            params={
                "codeList": code_list,
                "namespace": namespace
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["deleteRoles"]

    def list_users(self, code, page=0, limit=10, namespace=None, with_custom_data=False):
        """获取用户列表

        Args:
            code : 角色 code 列表
            page (int): 页码数，从 1 开始，默认为 1 。
            limit (int): 每页个数，默认为 10 。
            namespace (str): 权限分组 code。
            with_custom_data (bool, optional): 是否获取自定义数据，默认为 false；如果设置为 true，将会在 customData 字段返回用户的所有自定义数据。
        """
        query = QUERY['roleWithUsers'] if not with_custom_data else QUERY['roleWithUsersWithCustomData']
        data = self.graphqlClient.request(
            query=query,
            params={
                "code": code,
                "namespace": namespace,
                "page": page,
                "limit": limit
            },
            token=self.tokenProvider.getAccessToken(),
        )
        data = data["role"]["users"]
        if with_custom_data:
            convert_nested_pagination_custom_data_list_to_dict(data)
        return data

    def add_users(self, code, userIds, namespace=None):
        # type:(str,object,str) -> object
        """添加用户"""
        data = self.graphqlClient.request(
            query=QUERY["assignRole"],
            params={
                "userIds": userIds,
                "roleCodes": [code],
                "namespace": namespace
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["assignRole"]

    def remove_users(self, code, userIds, namespace=None):
        # type:(str,object,str) -> object
        """移除用户"""
        data = self.graphqlClient.request(
            query=QUERY["revokeRole"],
            params={
                "userIds": userIds,
                "roleCodes": [code],
                "namespace": namespace
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["revokeRole"]

    def list_policies(self, code, page=1, limit=10):
        # type:(str,int,int) -> object
        """获取策略列表"""
        data = self.graphqlClient.request(
            query=QUERY["policyAssignments"],
            params={
                "targetType": "ROLE",
                "targetIdentifier": code,
                "page": page,
                "limit": limit,
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["policyAssignments"]

    def add_policies(self, code, policies):
        # type:(str,object) -> object
        """添加策略"""
        data = self.graphqlClient.request(
            query=QUERY["addPolicyAssignments"],
            params={
                "policies": policies,
                "targetType": "ROLE",
                "targetIdentifiers": [code],
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["addPolicyAssignments"]

    def remove_policies(self, code, policies):
        # type:(str,object) -> object
        """移除策略"""
        data = self.graphqlClient.request(
            query=QUERY["removePolicyAssignments"],
            params={
                "policies": policies,
                "targetType": "ROLE",
                "targetIdentifiers": [code],
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["removePolicyAssignments"]

    def list_authorized_resources(self, code, namespace, resource_type=None):
        """
        获取一个角色被授权的所有资源。

        Args:
            code (str): 角色 code；
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
            query=QUERY['listRoleAuthorizedResources'],
            params={
                'code': code,
                'namespace': namespace,
                'resourceType': resource_type
            },
            token=self.tokenProvider.getAccessToken()
        )
        data = data.get('role')
        if not data:
            raise AuthingException(500, 'role not exists')

        authorized_resources = data.get('authorizedResources')
        _list, total_count = authorized_resources.get('list'), authorized_resources.get('totalCount')
        _list = format_authorized_resources(_list)
        return {
            'totalCount': total_count,
            'list': _list
        }

    def get_udf_value(self, id):
        """
        获取角色的所有自定义字段数据。

        Args:
            id (str): 角色 ID
        """
        data = self.graphqlClient.request(
            query=QUERY["udv"],
            params={"targetType": "ROLE", "targetId": id},
            token=self.tokenProvider.getAccessToken()
        )
        values = data['udv']
        return convert_udv_list_to_dict(values)

    def get_udf_value_batch(self, ids):
        """
        获取多个角色的扩展字段列表。

        Args:
            ids (list): 角色 ID 列表
        """

        data = self.graphqlClient.request(
            query=QUERY['udfValueBatch'],
            params={
                'targetType': 'ROLE',
                'targetIds': ids
            },
            token=self.tokenProvider.getAccessToken()
        )
        raw_result = data['udfValueBatch']
        ret = {}
        for item in raw_result:
            target_id, value = item.get('targetId'), item.get('data')
            ret[target_id] = convert_udv_list_to_dict(value)
        return ret

    def get_specific_udf_value(self, id, key):
        """
        获取角色的某个自定义字段值。

        Args:
            id (str): 角色 ID
            key (str): 自定义字段的 key
        """
        values = self.get_udf_value(id)
        return values.get(key)

    def set_udf_value(self, id, data):
        """
        设置角色的自定义数据。

        Args:
            id (str): 角色 ID
            data (dict): 自定义数据，类型是一个字段，如 { 'school': '清华大学' }
        """
        if not isinstance(data, dict):
            raise AuthingWrongArgumentException('data must be a dict, received a %s' % type(data))

        _list = []
        for k, v in data.items():
            if isinstance(v, datetime.datetime):
                def default(o):
                    if isinstance(o, (datetime.date, datetime.datetime)):
                        return o.isoformat()

                v = json.dumps(v, sort_keys=True, indent=1, default=default)
            else:
                v = json.dumps(v)
            _list.append({
                'key': k,
                'value': v
            })
        self.graphqlClient.request(
            query=QUERY['setUdvBatch'],
            params={
                'targetType': 'ROLE',
                'targetId': id,
                'udvList': _list
            },
            token=self.tokenProvider.getAccessToken()
        )
        return True

    def set_udf_value_batch(self, data):
        """
        批量设置多个角色的自定义数据。

        Args:
            data (dict): 输入数据，格式为一个字典，key 为角色 ID，value 为自定义数据；value 格式要求为一个字典，key 为自定义字段的 key，value 为需要设置的值。
                        示例：{ roleId1: { 'school': '清华大学' } }
        """
        if not isinstance(data, dict):
            raise AuthingWrongArgumentException('data must be a list')

        for k, v in data.items():
            if not isinstance(v, dict):
                raise AuthingWrongArgumentException('invalid data input')

        params = []
        for role_id in data.keys():
            for k, v in data[role_id].items():
                if isinstance(v, datetime.datetime):
                    def default(o):
                        if isinstance(o, (datetime.date, datetime.datetime)):
                            return o.isoformat()

                    v = json.dumps(v, sort_keys=True, indent=1, default=default)
                else:
                    v = json.dumps(v)
                params.append({
                    'targetId': role_id,
                    'key': k,
                    'value': v
                })

        self.graphqlClient.request(
            query=QUERY['setUdfValueBatch'],
            params={
                'targetType': 'ROLE',
                'input': params
            },
            token=self.tokenProvider.getAccessToken()
        )
        return True

    def remove_udf_value(self, id, key):
        """
        删除角色的自定义字段。

        Args:
            id (str): 角色 ID；
            key (str): 自定义字段 key
        """
        self.graphqlClient.request(
            query=QUERY['removeUdv'],
            params={
                'targetType': 'ROLE',
                'targetId': id,
                'key': key
            },
            token=self.tokenProvider.getAccessToken()
        )
        return True
