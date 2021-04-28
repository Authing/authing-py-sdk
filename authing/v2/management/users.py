# coding: utf-8
from functools import singledispatch

from .types import ManagementClientOptions
from ..common.rest import RestClient
from ..common.utils import encrypt, url_join_args, convert_udv_list_to_dict
from ..common.graphql import GraphqlClient
from .token_provider import ManagementTokenProvider
from ..common.codegen import QUERY
import json
import datetime
from dateutil import parser

from ..exceptions import AuthingWrongArgumentException


class UsersManagementClient(object):
    """Authing Users Management Client"""

    def __init__(self, options, graphqlClient, restClient, tokenProvider):
        # type:(ManagementClientOptions,GraphqlClient,RestClient,ManagementTokenProvider) -> UsersManagementClient
        self.options = options
        self.graphqlClient = graphqlClient
        self.tokenProvider = tokenProvider
        self.restClient = restClient

    def list(self, page=1, limit=10):
        """获取用户池用户列表

        Args:
            page (int): 页码数，从 1 开始，默认为 1 。
            limit (int): 每页个数，默认为 10 。

        Returns:
            [totalCount, _list]: 返回一个 tuple，第一个值为用户总数，第二个为元素为用户信息的列表。
        """
        data = self.graphqlClient.request(
            query=QUERY["users"],
            params={"page": page, "limit": limit},
            token=self.tokenProvider.getAccessToken(),
        )
        return data["users"]

    def create(self, userInfo, keep_password=False):
        """创建用户

        Args:
            userInfo (dict): 用户信息
            keep_password (bool): 该参数一般在迁移旧有用户数据到 Authing 的时候会设置。开启这个开关，password 字段会直接写入 Authing 数据库，
                                    Authing 不会再次加密此字段。如果你的密码不是明文存储，你应该保持开启，并编写密码函数计算。

        Returns:
            [User]: 用户详情
        """

        if not isinstance(userInfo, dict):
            raise AuthingWrongArgumentException('userInfo must be a dict')

        if userInfo.get("password"):
            userInfo["password"] = encrypt(
                userInfo["password"], self.options.enc_public_key
            )
        data = self.graphqlClient.request(
            query=QUERY["createUser"],
            params={
                "userInfo": userInfo,
                "keepPassword": keep_password
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["createUser"]

    def update(self, userId, updates):
        """修改用户信息

        Args:
            userId (str): 用户 ID
            updates (dict): 需要修改的用户字段
        """
        if updates.get("password"):
            updates["password"] = encrypt(
                updates["password"], self.options.enc_public_key
            )

        data = self.graphqlClient.request(
            query=QUERY["updateUser"],
            params={"id": userId, "input": updates},
            token=self.tokenProvider.getAccessToken(),
        )
        return data["updateUser"]

    def detail(self, userId):
        """获取用户资料详情

        Args:
            userId (str): 用户 ID
        """
        data = self.graphqlClient.request(
            query=QUERY["user"],
            params={"id": userId},
            token=self.tokenProvider.getAccessToken(),
        )
        return data["user"]

    def find(self, email=None, username=None, phone=None, external_id=None):
        """查找用户

        Args:
            email (str): 邮箱
            username (str): 用户名
            phone (str): 手机号
            external_id (str): 外部员工 ID
        """
        data = self.graphqlClient.request(
            query=QUERY["findUser"],
            params={
                "email": email,
                "username": username,
                "phone": phone,
                "externalId": external_id
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["findUser"]

    def search(self, query, page=1, limit=10, department_opts=None, group_opts=None, role_opts=None):
        """搜索用户

        Args:
            query (str): 查询语句
            page (int): 页码数，从 1 开始，默认为 1 。
            limit (int): 每页个数，默认为 10 。
            department_opts (list): 限制条件，用户所在的部门
            group_opts (list): 限制条件，用户所在的分组
            role_opts (list): 限制条件，用户所在的角色
        """

        if department_opts:
            if not isinstance(department_opts, list):
                raise AuthingWrongArgumentException('department_opts must be a list')

        if group_opts:
            if not isinstance(group_opts, list):
                raise AuthingWrongArgumentException('group_opts must be a list')

        if role_opts:
            if not isinstance(role_opts, list):
                raise AuthingWrongArgumentException('group_opts must be a list')

        data = self.graphqlClient.request(
            query=QUERY["searchUser"],
            params={
                "query": query,
                "page": page,
                "limit": limit,
                'departmentOpts': department_opts,
                'groupOpts': group_opts,
                'roleOpts': role_opts
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["searchUser"]

    def batch_get(self, identifiers, query_field='id'):
        """
        通过 id、username、email、phone、email、externalId 批量获取用户详情。一次最多支持查询 80 个用户。
        """
        url = "%s/api/v2/users/batch" % self.options.host
        return self.restClient.request(
            method='POST',
            url=url,
            json={
                'ids': identifiers,
                'type': query_field
            },
            token=self.tokenProvider.getAccessToken(),
            auto_parse_result=True
        )

    def batch(self, userIds):
        """已废弃，请使用 batch_get 接口
        """
        data = self.graphqlClient.request(
            query=QUERY["userBatch"],
            params={"ids": userIds},
            token=self.tokenProvider.getAccessToken(),
        )
        return data["userBatch"]

    def delete(self, userId):
        """删除用户

        Args:
            userId (str): 用户 ID

        Returns:
            [int, str]: 一个 tuple ，第一个为状态码，200 表示成功，第二个为 message
        """
        data = self.graphqlClient.request(
            query=QUERY["deleteUser"],
            params={"id": userId},
            token=self.tokenProvider.getAccessToken(),
        )
        return data["deleteUser"]

    def delete_many(self, userIds):
        """批量删除用户

        Args:
            userIds (list): 用户 ID 列表
        """
        data = self.graphqlClient.request(
            query=QUERY["deleteUsers"],
            params={"ids": userIds},
            token=self.tokenProvider.getAccessToken(),
        )
        return data["deleteUsers"]

    def list_roles(self, userId, namespace=None):
        """获取用户的角色列表

        Args:
            userId (str): 用户 ID
            namespace (str): 权限分组的 Code
        """
        data = self.graphqlClient.request(
            query=QUERY["getUserRoles"],
            params={
                "id": userId,
                "namespace": namespace
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["user"]["roles"]

    def add_roles(self, userId, roles, namespace=None):
        """批量授权用户角色

        Args:
            userId (str): 用户 ID
            roles: 角色 code 列表
            namespace (str): 权限分组的 Code
        """
        data = self.graphqlClient.request(
            query=QUERY["assignRole"],
            params={
                "userIds": [userId],
                "roleCodes": roles,
                "namespace": namespace
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["assignRole"]

    def remove_roles(self, userId, roles, namespace=None):
        """批量撤销用户角色

        Args:
            userId (str): 用户 ID
            roles: 用户角色 code 列表
            namespace (str): 权限分组的 Code
        """
        data = self.graphqlClient.request(
            query=QUERY["revokeRole"],
            params={
                "userIds": [userId],
                "roleCodes": roles,
                'namespace': namespace
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["revokeRole"]

    def refresh_token(self, userId):
        """刷新某个用户的 token

        Args:
            userId (str): 用户 ID

        Returns:
            [str, number, number]: jwt token, iat, exp
        """
        data = self.graphqlClient.request(
            query=QUERY["refreshToken"],
            params={
                "id": userId,
            },
            token=self.tokenProvider.getAccessToken(),
        )
        data = data["refreshToken"]
        return data

    def list_groups(self, userId):
        """获取用户的分组列表

        Args:
            userId (str): 用户 ID
        """
        data = self.graphqlClient.request(
            query=QUERY["getUserGroups"],
            params={
                "id": userId,
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["user"]["groups"]

    def add_group(self, userId, group):
        """获取用户的分组列表

        Args:
            userId (str): 用户 ID
            group (str): 分组的 code
        """
        data = self.graphqlClient.request(
            query=QUERY["addUserToGroup"],
            params={"userIds": [userId], "code": group},
            token=self.tokenProvider.getAccessToken(),
        )
        return data["addUserToGroup"]

    def remove_group(self, userId, group):
        """获取用户的分组列表

        Args:
            userId (str): 用户 ID
            group (str): 分组的 code
        """
        data = self.graphqlClient.request(
            query=QUERY["removeUserFromGroup"],
            params={"userIds": [userId], "code": group},
            token=self.tokenProvider.getAccessToken(),
        )
        return data["removeUserFromGroup"]

    def list_policies(self, userId, page=1, limit=10):
        """获取策略列表"""
        data = self.graphqlClient.request(
            query=QUERY["policyAssignments"],
            params={
                "targetType": "USER",
                "targetIdentifier": userId,
                "page": page,
                "limit": limit,
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["policyAssignments"]

    def add_policies(self, userId, policies):
        """添加策略"""
        data = self.graphqlClient.request(
            query=QUERY["addPolicyAssignments"],
            params={
                "policies": policies,
                "targetType": "USER",
                "targetIdentifiers": [userId],
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["addPolicyAssignments"]

    def remove_policies(self, userId, policies):
        """移除策略"""
        data = self.graphqlClient.request(
            query=QUERY["removePolicyAssignments"],
            params={
                "policies": policies,
                "targetType": "USER",
                "targetIdentifiers": [userId],
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["removePolicyAssignments"]

    def list_udv(self, userId):
        """获取该用户的自定义数据列表"""
        data = self.graphqlClient.request(
            query=QUERY["udv"],
            params={"targetType": "USER", "targetId": userId},
            token=self.tokenProvider.getAccessToken(),
        )
        data = data["udv"]
        for i, item in enumerate(data):
            dataType, value = item["dataType"], item["value"]
            if dataType == "NUMBER":
                data[i]["value"] = json.loads(value)
            elif dataType == "BOOLEAN":
                data[i]["value"] = json.loads(value)
            elif dataType == "DATETIME":
                data[i]["value"] = parser.parse(value)
            elif dataType == "OBJECT":
                data[i]["value"] = json.loads(value)
        return data

    def get_udf_value(self, user_id):
        data = self.graphqlClient.request(
            query=QUERY["udv"],
            params={"targetType": "USER", "targetId": user_id},
            token=self.tokenProvider.getAccessToken()
        )
        data = data['udv']
        return convert_udv_list_to_dict(data)

    def get_udf_value_batch(self, user_ids):
        if type(user_ids).__name__ != "list":
            raise AuthingWrongArgumentException('empty user id list')

        return self.graphqlClient.request(
            query=QUERY["udfValueBatch"],
            params={"targetType": "USER", "targetId": user_ids},
            token=self.tokenProvider.getAccessToken()
        )["udfValueBatch"]

    def set_udv(self, userId, key, value):
        """设置自定义用户数据

        Args:
            userId (str): 用户 ID
            key (str): key
            value (str): value
        """

        if isinstance(value, datetime.datetime):

            def default(o):
                if isinstance(o, (datetime.date, datetime.datetime)):
                    return o.isoformat()

            value = json.dumps(value, sort_keys=True, indent=1, default=default)
        else:
            value = json.dumps(value)
        data = self.graphqlClient.request(
            query=QUERY["setUdv"],
            params={
                "targetType": "USER",
                "targetId": userId,
                "key": key,
                "value": value,
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["setUdv"]

    def set_udf_value(self, user_id, data):
        """
        设置用户的自定义数据。

        Args:
            user_id (str): 用户 ID；
            data (dict): 自定义数据，类型为一个字典
        """


        if not isinstance(data, dict):
            raise AuthingWrongArgumentException('data must be a dict')

        if len(data.keys()) == 0:
            raise AuthingWrongArgumentException('data must not be a empty dict')

        list = []
        for k, v in data.items():
            if isinstance(v, datetime.datetime):
                def default(o):
                    if isinstance(o, (datetime.date, datetime.datetime)):
                        return o.isoformat()

                v = json.dumps(v, sort_keys=True,
                               indent=1, default=default)
            else:
                v = json.dumps(v)
            list.append({
                'key': k,
                'value': v
            })
        self.graphqlClient.request(
            query=QUERY['setUdvBatch'],
            params={
                'targetType': 'USER',
                'targetId': user_id,
                'udvList': list
            },
            token=self.tokenProvider.getAccessToken()
        )
        return True

    def set_udf_value_batch(self, data):
        """
        批量设置多个用户的自定义数据。

        Args:
            data (dict): 输入数据，格式为一个字典，key 为角色 ID，value 为自定义数据；value 格式要求为一个字典，key 为自定义字段的 key，value 为需要设置的值。
                        示例：{ 'USER_ID1': { 'school': '清华大学' } }
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
                'targetType': 'USER',
                'input': params
            },
            token=self.tokenProvider.getAccessToken()
        )
        return True

    def remove_udv(self, userId, key):
        """删除用户自定义字段数据

        Args:
            userId (str): 用户 ID
            key (str): str
        """
        data = self.graphqlClient.request(
            query=QUERY["removeUdv"],
            params={
                "targetType": "USER",
                "targetId": userId,
                "key": key,
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["removeUdv"]

    def remove_udf_value(self, user_id, key):
        self.remove_udv(user_id, key)

    def list_archived_users(self, page=1, limit=10):
        """获取已归档用户列表

        Args:
            page (int): 页码数，从 1 开始，默认为 1 。
            limit (int): 每页个数，默认为 10 。
        """

        data = self.graphqlClient.request(
            query=QUERY["archivedUsers"],
            params={
                "page": page,
                "limit": limit
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["archivedUsers"]

    def exists(self, username=None, email=None, phone=None, external_id=None):
        """
        检查用户是否存在

        Args:
            username (str) 用户名，区分大小写
            email (str) 邮箱，邮箱不区分大小写
            phone (str) 手机号
            external_id (str) External ID
        """

        data = self.graphqlClient.request(
            query=QUERY["isUserExists"],
            params={
                "username": username,
                "email": email,
                "phone": phone,
                'externalId': external_id
            },
            token=self.tokenProvider.getAccessToken()
        )
        return data["isUserExists"]

    def list_org(self, user_id):
        """
        获取用户所在组织机构

        Args:
            user_id (str) 用户 ID
        """

        url = "%s/api/v2/users/%s/orgs" % (self.options.host, user_id)
        res = self.restClient.request(
            method="GET",
            url=url,
            token=self.tokenProvider.getAccessToken()
        )

        if res.get("code") == 200:
            return res.get("data")
        else:
            self.options.on_error(res.get("code"), res.get("message"))

    def list_department(self, user_id):
        """
        获取用户所在部门

        Args:
            user_id (str) 用户 ID
        """

        return self.graphqlClient.request(
            query=QUERY["getUserDepartments"],
            params={
                "id": user_id
            },
            token=self.tokenProvider.getAccessToken()
        )["user"]

    def list_authorized_resources(self, user_id, namespace, resource_type=None):
        """
        获取用户被授权的所有资源

        Args:
            user_id (str) 用户 ID
            namespace (str)  权限分组的 Code
            resource_type (str) 资源类型，可选值包含 DATA、API、MENU、UI、BUTTON
        """

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
            query=QUERY["listUserAuthorizedResources"],
            params={
                "id": user_id,
                "namespace": namespace,
                "resourceType": resource_type
            },
            token=self.tokenProvider.getAccessToken()
        )

        return data["user"]["authorizedResources"]

    def has_role(self, user_id, role_code, namespace=None):
        role_list = self.list_roles(user_id, namespace)

        if role_list["totalCount"] < 1:
            return False

        has_role = False

        for item in role_list["list"]:
            if item["code"] == role_code:
                has_role = True

        return has_role

    def kick(self, user_ids):

        if type(user_ids).__name__ != "list":
            raise AuthingWrongArgumentException('empty user id list')

        url = "%s/api/v2/users/kick" % self.options.host
        return self.restClient.request(
            method="POST",
            url=url,
            token=self.tokenProvider.getAccessToken(),
            json={
                "userIds": user_ids
            }
        )["data"]

    def list_user_actions(self, page=1, limit=10, client_ip=None, operation_name=None, operato_arn=None):

        url = "%s/api/v2/analysis/user-action" % self.options.host

        query = url_join_args(url, {
            "page": page,
            "limit": limit,
            "clientip": client_ip,
            "operation_name": operation_name,
            "operator_arn": operato_arn
        })

        return self.restClient.request(
            method="GET",
            url=query,
            token=self.tokenProvider.getAccessToken()
        )["data"]
