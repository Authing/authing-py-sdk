# coding: utf-8

from .types import ManagementClientOptions
from ..common.graphql import GraphqlClient
from .token_provider import ManagementTokenProvider
from ..common.codegen import QUERY
from ..exceptions import AuthingWrongArgumentException
from ..common.rest import RestClient
from ..common.utils import format_authorized_resources,get_random_string_secret

class AclManagementClient(object):
    """Authing Access Control Management Client"""

    def __init__(self, options, graphqlClient, restClient, tokenProvider, managementClient):
        # type:(ManagementClientOptions,GraphqlClient,RestClient,ManagementTokenProvider) -> AclManagementClient
        self.options = options
        self.graphqlClient = graphqlClient
        self.restClient = restClient
        self.tokenProvider = tokenProvider
        self.__super__ = managementClient

    def allow(self, resource, action, namespace, role=None, user_id=None):
        """允许某个用户对某个资源进行某个操作

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
        """判断某个用户是否对某个资源有某个操作权限

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
        """创建权限分组。权限分组可以理解为权限的命名空间，不同权限分组中的角色和资源相互独立，即使同名也不会冲突。

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
        """更新权限分组。

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
        """获取权限分组列表"""

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
        """删除权限分组。

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
        """创建资源

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
        """更新资源

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
        """获取资源列表

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
        """删除资源

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
        """获取某个主体（用户、角色、分组、组织机构节点）被授权的所有资源。

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


    def __check_opts(self, opts):
        if not isinstance(opts, list):
            raise AuthingWrongArgumentException('opts must be a list')

        for item in opts:
            if not isinstance(item, dict):
                raise AuthingWrongArgumentException('item of opts must be a dict')
            keys = item.keys()
            if 'targetType' not in keys or 'targetIdentifier' not in keys:
                raise AuthingWrongArgumentException('item of opts must be a dict with targetType and targetIdentifier key')


    def revoke_resource(self, namespace, resource, opts):
        """
        批量撤销资源的授权。

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
        self.__check_opts(opts)
        url = "%s/api/v2/acl/revoke-resource" % (
            self.options.host
        )
        self.restClient.request(
            method='POST',
            url=url,
            token=self.tokenProvider.getAccessToken(),
            auto_parse_result=True,
            json={
                "namespace": namespace,
                "resource": resource,
                "opts": opts
            }
        )
        return True


    def authorize_resource(self, namespace, resource, opts):
        """将一个（类）资源授权给用户、角色、分组、组织机构，且可以分别指定不同的操作权限。

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

        self.__check_opts(opts)

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
        """获取具备某些资源操作权限的主体

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

    def programmatic_access_account_list(self, app_id, page=1, limit=10):
        """编程访问账号列表

        Args:
            app_id (str): 应用ID
            page (int): 分页
            limit (int): 每页数量
        """
        if not app_id:
            raise AuthingWrongArgumentException("app_id not found")
        url = "%s/api/v2/applications/%s/programmatic-access-accounts?limit=%s&page=%s" % (self.options.host, app_id,
                                                                                           limit, page)
        return self.restClient.request(method='GET', token=self.tokenProvider.getAccessToken(), url=url)

    def create_programmatic_access_account(self, app_id, remark=None, token_lifetime=600):
        """添加编程访问账号

        Args:
            app_id (str): 应用ID
            remark (str): 备注
            token_lifetime (int): Token过期时间
        """
        url = "%s/api/v2/applications/%s/programmatic-access-accounts" % (self.options.host, app_id)
        body = {
            'tokenLifetime': token_lifetime
        }
        if remark:
            body['remark'] = remark
        return self.restClient.request(method='POST', token=self.tokenProvider.getAccessToken(), url=url, json=body)

    def disable_programmatic_access_account(self, programmatic_access_account_id):
        """禁用编程访问账号

         Args:
            programmatic_access_account_id (str): 编程账号ID
        """
        url = "%s/api/v2/applications/programmatic-access-accounts" % self.options.host
        body = {
            'id': programmatic_access_account_id,
            'enabled': False
        }
        return self.restClient.request(method='PATCH', token=self.tokenProvider.getAccessToken(), url=url, json=body)

    def delete_programmatic_access_account(self, programmatic_access_account_id):
        """删除编程访问账号

        Args:
            programmatic_access_account_id (str): 编程账号ID
        """
        url = "%s/api/v2/applications/programmatic-access-accounts?id=%s" % (self.options.host,programmatic_access_account_id )
        return self.restClient.request(method='DELETE', token=self.tokenProvider.getAccessToken(), url=url)

    def enable_programmatic_access_account(self, programmatic_access_account_id):
        """启用编程访问账号

         Args:
            programmatic_access_account_id (str): 编程账号ID
        """
        url = "%s/api/v2/applications/programmatic-access-accounts" % self.options.host
        body = {
            'id': programmatic_access_account_id,
            'enabled': True
        }
        return self.restClient.request(method='PATCH', token=self.tokenProvider.getAccessToken(), url=url, json=body)

    def refresh_programmatic_access_account_secret(self, programmatic_access_account_id, secret=get_random_string_secret(32)):
        """刷新编程访问账号密钥

         Args:
            programmatic_access_account_id (str): 编程账号ID
            secret (str) : 默认秘钥
        """
        url = "%s/api/v2/applications/programmatic-access-accounts" % self.options.host
        body = {
            'id': programmatic_access_account_id,
            'secret': secret
        }
        return self.restClient.request(method='PATCH', token=self.tokenProvider.getAccessToken(), url=url, json=body)

    def get_resource_by_id(self, id):
        """根据 ID 获取单个资源

          Args:
            id (str): 资源ID
        """
        url = "%s/api/v2/resources/detail" % self.options.host
        return self.restClient.request(method='GET', token=self.tokenProvider.getAccessToken(),
                                       url=url,params={'id': id})

    def get_resource_by_code(self, namespace, code):
        """根据 Code 获取单个资源

        Args:
            namespace (str): 空间编码
            code (str): 资源Code
        """
        url = "%s/api/v2/resources/detail" % self.options.host
        return self.restClient.request(method='GET', token=self.tokenProvider.getAccessToken(),
                                       url=url, params={'namespace': namespace, 'code': code})

    def __convert_access_application_params_to_json(self, app_id, target_type, target_identifiers, namespace, inherit_by_children):
        self.__super__.check.target_type(target_type)
        if not app_id:
            raise AuthingWrongArgumentException("app_id is required")
        body = {
            'targetType': target_type,
            'targetIdentifiers': target_identifiers,
            'namespace': namespace,
            'inheritByChildren': inherit_by_children
        }
        return body

    def enable_application_access_policies(self, app_id, target_type, target_identifiers, namespace, inherit_by_children):
        """启用应用访问控制策略

        Args:
            app_id (str): 应用编码
            target_type (str): 对象类型
            target_identifiers (str[]): 对象ID集合
            namespace (str):空间编码
            inherit_by_children(bool):是否内联子类
        """
        body = self.__convert_access_application_params_to_json(app_id, target_type, target_identifiers, namespace, inherit_by_children)
        url = "%s/api/v2/applications/%s/authorization/enable-effect" % (self.options.host, app_id)
        return self.restClient.request(method='POST', token=self.tokenProvider.getAccessToken(), url=url, json=body)

    def disable_application_access_policies(self, app_id, target_type, target_identifiers, namespace,
                                           inherit_by_children):
        """停用应用访问控制策略

        Args:
            app_id (str): 应用编码
            target_type (str): 对象类型
            target_identifiers (str[]): 对象ID集合
            namespace (str):空间编码
            inherit_by_children(bool):是否内联子类
        """
        body = self.__convert_access_application_params_to_json(app_id, target_type, target_identifiers, namespace, inherit_by_children)

        url = "%s/api/v2/applications/%s/authorization/disable-effect" % (self.options.host, app_id)
        return self.restClient.request(method='POST', token=self.tokenProvider.getAccessToken(), url=url, json=body)

    def delete_application_access_policies(self, app_id, target_type, target_identifiers, namespace,
                                            inherit_by_children):
        """删除应用访问控制策略

        Args:
            app_id (str): 应用编码
            target_type (str): 对象类型
            target_identifiers (str[]): 对象ID集合
            namespace (str):空间编码
            inherit_by_children(bool):是否内联子类
        """
        body = self.__convert_access_application_params_to_json(app_id, target_type, target_identifiers, namespace, inherit_by_children)

        url = "%s/api/v2/applications/%s/authorization/revoke" % (self.options.host, app_id)
        return self.restClient.request(method='POST', token=self.tokenProvider.getAccessToken(), url=url, json=body)

    def allow_access_application(self, app_id, target_type, target_identifiers, namespace,
                                            inherit_by_children):
        """配置「允许主体（用户、角色、分组、组织机构节点）访问应用」的控制策略

                   Args:
                       app_id (str): 应用编码
                       target_type (str): 对象类型
                       target_identifiers (str[]): 对象ID集合
                       namespace (str):空间编码
                       inherit_by_children(bool):是否内联子类
                   """
        body = self.__convert_access_application_params_to_json(app_id, target_type, target_identifiers, namespace, inherit_by_children)

        url = "%s/api/v2/applications/%s/authorization/allow" % (self.options.host, app_id)
        return self.restClient.request(method='POST', token=self.tokenProvider.getAccessToken(), url=url, json=body)

    def deny_access_application(self, app_id, target_type, target_identifiers, namespace,
                                            inherit_by_children):
        """配置「拒绝主体（用户、角色、分组、组织机构节点）访问应用」的控制策略

             Args:
                 app_id (str): 应用编码
                 target_type (str): 对象类型
                 target_identifiers (str[]): 对象ID集合
                 namespace (str):空间编码
                 inherit_by_children(bool):是否内联子类
             """
        body = self.__convert_access_application_params_to_json(app_id, target_type, target_identifiers, namespace, inherit_by_children)

        url = "%s/api/v2/applications/%s/authorization/deny" % (self.options.host, app_id)
        return self.restClient.request(method='POST', token=self.tokenProvider.getAccessToken(), url=url, json=body)

    def update_default_application_access_policy(self, app_id, default_strategy):
        """更改默认应用访问策略（默认拒绝所有用户访问应用、默认允许所有用户访问应用）"""
        if default_strategy not in ['ALLOW_ALL', 'DENY_ALL']:
            raise AuthingWrongArgumentException('default_strategy value only "ALLOW_ALL" or "DENY_ALL" ')
        if not app_id:
            raise AuthingWrongArgumentException(' app_id is required')
        url = "%s/api/v2/applications/%s" % (self.options.host, app_id)
        return self.restClient.request(method='POST', token=self.tokenProvider.getAccessToken(), url=url, json={
            'permissionStrategy': {
                'defaultStrategy': default_strategy
            }
        })
