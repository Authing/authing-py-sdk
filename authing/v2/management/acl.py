# coding: utf-8

from .types import ManagementClientOptions
from ..common.graphql import GraphqlClient
from .token_provider import ManagementTokenProvider
from ..common.codegen import QUERY
from ..exceptions import AuthingWrongArgumentException
from ..common.rest import RestClient
from ..common.utils import format_authorized_resources


class AclManagementClient(object):
    """Authing Access Control Management Client"""

    def __init__(self, options, graphqlClient, restClient, tokenProvider):
        # type:(ManagementClientOptions,GraphqlClient,RestClient,ManagementTokenProvider) -> AclManagementClient
        self.options = options
        self.graphqlClient = graphqlClient
        self.restClient = restClient
        self.tokenProvider = tokenProvider

    def allow(self, resource, action, namespace, role=None, user_id=None):
        """允许某个用户操作某个资源

        Args:
            resource (str): 资源的 code
            action (str): 资源操作类型
            user_id (str): 用户 ID
            role (str): 角色的 code
            namespace (str): 权限分组的 code
        """

        if not user_id and not role:
            raise AuthingWrongArgumentException('must provide user_id or role')

        data = self.graphqlClient.request(
            query=QUERY["allow"],
            params={
                "userId": user_id,
                "resource": resource,
                "action": action,
                "namespace": namespace,
                "roleCode": role
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["allow"]

    def is_allowed(self, user_id, action, resource, namespace):
        """
        判断某个用户是否能够具备某个资源资源某个操作的权限。

        Args:
            resource (str) 资源的 code
            action (str) 资源操作类型
            user_id (str) 用户 ID
            namespace (str) 权限分组的 code
        """
        data = self.graphqlClient.request(
            query=QUERY["isActionAllowed"],
            params={
                "userId": user_id,
                "resource": resource,
                "action": action,
                "namespace": namespace
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["isActionAllowed"]

    def create_namespace(self, code, name, description=None):
        """
        创建权限分组。权限分组可以理解为权限的命名空间，不同权限分组中的角色和资源相互独立，即使同名也不会冲突。

        Args:
            code (str): 权限分组唯一标识符；
            name (str): 权限分组名称；
            description (str): 可选，权限分组描述。
        """

        url = "%s/api/v2/resource-namespace/%s" % (self.options.host, self.options.user_pool_id)
        data = self.restClient.request(
            method='POST',
            url=url,
            json={
                'name': name,
                'code': code,
                'description': description
            },
            token=self.tokenProvider.getAccessToken()
        )
        code, message, data = data.get("code"), data.get(
            "message"), data.get("data")
        if code == 200:
            return data
        else:
            self.options.on_error(code, message)

    def update_namespace(self, id, name=None, code=None, description=None):
        """
        更新权限分组。

        Args:
            id (number): 权限分组的 ID；
            name (str): 新的权限分组名称；
            code (str): 新的 code；
            description (str): 描述信息
        """
        url = "%s/api/v2/resource-namespace/%s/%s" % (self.options.host, self.options.user_pool_id, id)
        data = self.restClient.request(
            method='PUT',
            url=url,
            json={
                'name': name,
                'code': code,
                'description': description
            },
            token=self.tokenProvider.getAccessToken()
        )
        code, message, data = data.get("code"), data.get(
            "message"), data.get("data")
        if code == 200:
            return data
        else:
            self.options.on_error(code, message)

    def list_namespaces(self, page=1, limit=10):
        """
        获取权限分组列表。
        """

        url = "%s/api/v2/resource-namespace/%s?page=%s&limit=%s" % (
            self.options.host, self.options.user_pool_id, page, limit)
        data = self.restClient.request(
            method='GET',
            url=url,
            token=self.tokenProvider.getAccessToken()
        )
        code, message, data = data.get("code"), data.get(
            "message"), data.get("data")
        if code == 200:
            return data
        else:
            self.options.on_error(code, message)

    def delete_namespace(self, id):
        """
        删除权限分组。

        Args:
            id (str): 权限分组 ID;
        """
        url = "%s/api/v2/resource-namespace/%s/%s" % (self.options.host, self.options.user_pool_id, id)
        data = self.restClient.request(
            method='DELETE',
            url=url,
            token=self.tokenProvider.getAccessToken()
        )
        code, message, data = data.get("code"), data.get(
            "message"), data.get("data")
        if code == 200:
            return True
        else:
            self.options.on_error(code, message)

    def __check_resource_actions(self, actions):
        if not isinstance(actions, list):
            raise AuthingWrongArgumentException('actions must be a list of dict like { "name": "xxx", '
                                                '"description": "xxx" }')
        for item in actions:
            if not isinstance(item, dict):
                raise AuthingWrongArgumentException('actions must be a list of dict like { "name": "xxx", '
                                                    '"description": "xxx" }')
            keys = item.keys()
            if 'name' not in keys or 'description' not in keys:
                raise AuthingWrongArgumentException('actions must be a list of dict like { "name": "xxx", '
                                                    '"description": "xxx" }')

    def __check_resource_type(self, resource_type):
        if resource_type not in ['DATA', 'API', 'MENU', 'UI', 'BUTTON']:
            raise AuthingWrongArgumentException('unsupported resource_type: %s' % resource_type)

    def create_resource(self, namespace, code, resource_type, actions, description=None):
        """
        创建资源。

        Args:
            namespace: (str): 权限分组信息
            code (str): 资源标识符;
            resource_type (str): 资源类型，可选值为 DATA、API、MENU、UI、BUTTON；
            actions (list): 资源操作对象数组。其中 name 为操作名称，填写一个动词，description 为操作描述，填写描述信息。
            description (str): 描述信息
        """

        self.__check_resource_actions(actions)
        self.__check_resource_type(resource_type)

        url = "%s/api/v2/resources" % self.options.host
        data = self.restClient.request(
            method='POST',
            url=url,
            json={
                'code': code,
                'type': resource_type,
                'actions': actions,
                'namespace': namespace,
                'description': description
            },
            token=self.tokenProvider.getAccessToken()
        )
        code, message, data = data.get("code"), data.get(
            "message"), data.get("data")
        if code == 200:
            return data
        else:
            self.options.on_error(code, message)

    def update_resource(self, namespace, code, resource_type=None, actions=None, description=None):
        """
        更新资源。

        Args:
            namespace (str): 权限分组 code；
            code (str): 资源唯一标志符 code；
            resource_type (str): 新的资源类型；
            actions (list): 资源操作对象数组。其中 name 为操作名称，填写一个动词，description 为操作描述，填写描述信息。
            description (str): 描述信息
        """

        body = {
            'namespace': namespace
        }

        if description:
            body['description'] = description

        if actions:
            self.__check_resource_actions(actions)
            body['actions'] = actions

        if resource_type:
            self.__check_resource_type(resource_type)
            body['type'] = resource_type

        url = "%s/api/v2/resources/%s" % (self.options.host, code)
        data = self.restClient.request(
            method='POST',
            url=url,
            json=body,
            token=self.tokenProvider.getAccessToken()
        )
        code, message, data = data.get("code"), data.get(
            "message"), data.get("data")
        if code == 200:
            return data
        else:
            self.options.on_error(code, message)

    def list_resources(self, namespace, resource_type=None, page=1, limit=10):
        """
        根据筛选条件，查询用户池下的资源列表。

        Args:
            namespace (str): 权限分组 code；
            resource_type (str): 资源类型，可选值为 DATA、API、MENU、UI、BUTTON；
            page (int): 页码数据，从 1 开始，默认为 1；
            limit (int): 每页个数，默认为 10；
        """

        if not isinstance(namespace, str):
            raise AuthingWrongArgumentException('namespace must be a str')

        if resource_type:
            self.__check_resource_type(resource_type)

        if page:
            if not isinstance(page, int):
                raise AuthingWrongArgumentException('page must be a int bigger than 0')
            if page < 1:
                raise AuthingWrongArgumentException('page must be a int bigger than 0')

        if limit:
            if not isinstance(limit, int):
                raise AuthingWrongArgumentException('limit must be a int bigger than 0')
            if limit < 1:
                raise AuthingWrongArgumentException('limit must be a int bigger than 0')

        url = "%s/api/v2/resources" % self.options.host
        data = self.restClient.request(
            method='GET',
            url=url,
            params={
                'namespace': namespace,
                'type': resource_type,
                'page': page,
                'limit': limit
            },
            token=self.tokenProvider.getAccessToken()
        )
        code, message, data = data.get("code"), data.get(
            "message"), data.get("data")
        if code == 200:
            return data
        else:
            self.options.on_error(code, message)

    def delete_resource(self, namespace, code):
        """
        删除资源。

        Args:
            namespace (str): 权限分组 code；
            code (str): 资源唯一标志符 code；
        """
        if not isinstance(namespace, str):
            raise AuthingWrongArgumentException('namespace must be a str')

        url = "%s/api/v2/resources/%s" % (self.options.host, code)
        data = self.restClient.request(
            method='DELETE',
            url=url,
            params={
                'namespace': namespace
            },
            token=self.tokenProvider.getAccessToken()
        )
        code, message, data = data.get("code"), data.get(
            "message"), data.get("data")
        if code == 200:
            return True
        else:
            self.options.on_error(code, message)

    def __check_target_type(self, target_type):
        if target_type not in ['USER', 'ROLE', 'GROUP', 'ORG']:
            raise AuthingWrongArgumentException('unsupported target_type: %s' % target_type)

    def list_authorized_resources(self, namespace, target_type, target_identifier, resource_type=None):
        """
        获取某个主体（用户、角色、分组、组织机构节点）被授权的所有资源。

        Args:
            target_type (str): 主体类型，可选值包含 USER, ROLE, GROUP, ORG
            target_identifier (str): 主体的唯一标志符，用户为用户 ID，角色为角色 code，分组为分组 code，组织机构节点为该节点 ID
            namespace (str): 权限分组的 code
            resource_type (str): 资源类型，可选值为 DATA、API、MENU、UI、BUTTON；
        """

        self.__check_target_type(target_type)

        if resource_type:
            self.__check_resource_type(resource_type)

        data = self.graphqlClient.request(
            query=QUERY['authorizedResources'],
            params={
                'targetType': target_type,
                'targetIdentifier': target_identifier,
                'namespace': namespace,
                'resourceType': resource_type
            },
            token=self.tokenProvider.getAccessToken()
        )
        data = data['authorizedResources']
        _list, total_count = data.get('list'), data.get('totalCount')
        _list = format_authorized_resources(_list)

        return {
            'list': _list,
            'totalCount': total_count
        }

    def authorize_resource(self, namespace, resource, opts):
        """
        批量授权资源权限。

        Args:
            namespace (str): 权限分组的 code
            resource (str): 资源的 code
            opts (list): 示例数据：
                        [
                            {
                                'targetType': 'USER',
                                'targetIdentifier': '123',
                                'actions': ['books:edit']
                            }
                        ]
        """

        if not isinstance(opts, list):
            raise AuthingWrongArgumentException('opts must be a list')

        for item in opts:
            if not isinstance(item, dict):
                raise AuthingWrongArgumentException('item of opts must be a dict')
            keys = item.keys()
            if 'targetType' not in keys or 'targetIdentifier' not in keys:
                raise AuthingWrongArgumentException('item of opts must be a dict with targetType and targetIdentifier key')

        self.graphqlClient.request(
            query=QUERY['authorizeResource'],
            params={
                'namespace': namespace,
                'resource': resource,
                'opts': opts
            },
            token=self.tokenProvider.getAccessToken()
        )

        return True

    def get_authorized_targets(self, namespace, resource_type, resource, actions=None, target_type=None):
        """
        获取具备某个（类）资源操作权限的用户、分组、角色、组织机构。

        Args:
            namespace (str): 权限分组的 code
            resource_type (str): 资源类型
            resource (str): 资源的 code
            actions (dict): 示例数据：具备 action1 或者 action2 权限
                            {
                                'op': 'OR',
                                'list': ['action1', 'action2']
                            }
            target_type (str): 目标对象类型。
        """

        if actions:
            if not isinstance(actions, dict):
                raise AuthingWrongArgumentException('actions must be a dict')
            keys = actions.keys()
            if 'op' not in keys or 'list' not in keys:
                raise AuthingWrongArgumentException('invalid argument actions')
            op = actions.get('op')
            if op not in ['AND', 'OR']:
                raise AuthingWrongArgumentException('op must be AND or OR')

        if target_type:
            self.__check_target_type(target_type)

        data = self.graphqlClient.request(
            query=QUERY['authorizedTargets'],
            params={
                'namespace': namespace,
                'resourceType': resource_type,
                'resource': resource,
                'targetType': target_type,
                'actions': actions
            },
            token=self.tokenProvider.getAccessToken()
        )

        return data['authorizedTargets']
