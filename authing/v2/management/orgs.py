# coding: utf-8
from .types import ManagementClientOptions
from ..common.graphql import GraphqlClient
from .token_provider import ManagementTokenProvider
from ..common.codegen import QUERY
from ..common.utils import format_authorized_resources
from ..exceptions import AuthingWrongArgumentException, AuthingException


class OrgManagementClient(object):
    """Authing Org Management Client"""

    def __init__(self, options, graphqlClient, tokenProvider,restClient):
        # type:(ManagementClientOptions,GraphqlClient,ManagementTokenProvider) -> OrgManagementClient
        self.options = options
        self.graphqlClient = graphqlClient
        self.tokenProvider = tokenProvider
        self.restClient = restClient

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
        """获取组织机构节点被授权的所有资源

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

    def create(self, name, code=None, description=None):
        """创建组织机构

        Args:
            name(str):名称
            code(str):编码
            description(str):描述
        """
        params = {
            'name': name
        }
        if code:
            params['code'] = code

        if description:
            params['description'] = description
        data = self.graphqlClient.request(
            query=QUERY['createOrg'],
            params=params,
            token=self.tokenProvider.getAccessToken()
        )
        return data['createOrg']

    def delete_by_id(self, id):
        """删除组织机构

        Args:
            id(str):机构ID
        """
        res = self.graphqlClient.request(
            query=QUERY['deleteOrg'],
            params={
                'id':id
            },
            token=self.tokenProvider.getAccessToken()
        )
        return res['deleteOrg']

    def __pop_node_by_id(self, list, id):
        for node in list:
            if id == node['id']:
                list.remove(node)
                return node

    def __convert_children_to_tree(self, nodes, node):
        ids = node['children']
        result = []
        for node_id in ids:

            children_node = self.__pop_node_by_id(nodes, node_id)
            result.append(children_node)
            self.__convert_children_to_tree(nodes, children_node)
        node['children'] = result

    def __convert_tree(self,result):
        for orgs in result:
            for node in orgs['nodes']:
                self.__convert_children_to_tree(orgs['nodes'], node)


    def list(self, page=1, limit=10, treeify=False):
        """获取用户池组织机构列表

        Args:
            page(int):页号
            limit(int):每页记录数
            treeify(bool):是否树化
        """
        data = self.graphqlClient.request(
            query=QUERY['orgs'],
            params={
                'page': page,
                'limit':limit
            },
            token=self.tokenProvider.getAccessToken()
        )
        totalCount, list = data['orgs']['totalCount'],data['orgs']['list']

        if treeify:
            self.__convert_tree(list)
        return {'totalCount': totalCount, 'list': list}

    def add_node(self, org_id, name, parent_node_id, code=None, description=None, order=None,
                 name_i18n=None, description_i18n=None):
        """在组织机构中添加一个节点

        Args:
            org_id(str): 机构ID
            name(str): 名称
            parent_node_id(str):父节点
            code(str):编码
            description(str):描述
            description_i18n(str):国际化描述
            name_i18n(str):国际化名称
            order(int):排序号
        """
        params = {
            'orgId': org_id,
            'parentNodeId': parent_node_id,
            'name': name,
            'code': code,
            'description': description,
            'order': order,
            'name_i18n': name_i18n,
            'description_i18n': description_i18n
        }

        data = self.graphqlClient.request(
            query=QUERY['addNode'],
            params=params,
            token=self.tokenProvider.getAccessToken()
        )
        return data['addNode']

    def get_node_by_id(self, node_id):
        """获取某个节点详情"""
        data = self.graphqlClient.request(
            query=QUERY['nodeById'],
            params={
                'id': node_id
            },
            token=self.tokenProvider.getAccessToken()
        )
        return data['nodeById']

    def update_node(self, node_id, name=None, code=None, description=None):
        """修改节点

        Args:
            node_id(str): Node主键
            name(str): 名称
            code(str): 编码
            description(str): 描述
        """
        params = {
            'id': node_id,
            'name': name,
            'code': code,
            'description': description
        }

        data = self.graphqlClient.request(
            query=QUERY['updateNode'],
            params=params,
            token=self.tokenProvider.getAccessToken()
        )
        return data['updateNode']

    def find_by_id(self, org_id, treeify=False):
        """获取组织机构详情"""
        data = self.graphqlClient.request(
            query=QUERY['org'],
            params={
                'id': org_id
            },
            token=self.tokenProvider.getAccessToken()
        )
        org = data['org']
        if treeify:
            for node in org['nodes']:
                self.__convert_children_to_tree(org['nodes'], node)
        return data['org']

    def delete_node(self, org_id, node_id):
        """删除节点

        Args:
            org_id(str):机构ID
            node_id(str):节点ID
        """
        data = self.graphqlClient.request(
            query=QUERY['deleteNode'],
            params={
                'orgId': org_id,
                'nodeId': node_id
            },
            token=self.tokenProvider.getAccessToken()
        )
        return data['deleteNode']

    def is_root_node(self, org_id, node_id):
        """判断是否为根节点

        Args:
            org_id(str):机构ID
            node_id(str):节点ID
        """
        data = self.graphqlClient.request(
            query=QUERY['isRootNode'],
            params={
                'orgId': org_id,
                'nodeId': node_id
            },
            token=self.tokenProvider.getAccessToken()
        )
        return data['isRootNode']

    def move_node(self, org_id, node_id, target_parent_id, treeify=False):
        """移动节点

        Args:
            org_id(str):机构ID
            node_id(str):节点ID
            target_parent_id(str):目标节点ID
        """
        data = self.graphqlClient.request(
            query=QUERY['moveNode'],
            params={
                'orgId': org_id,
                'nodeId': node_id,
                'targetParentId': target_parent_id
            },
            token=self.tokenProvider.getAccessToken()
        )
        result = data['moveNode']
        if treeify:
            for node in result['nodes']:
                self.__convert_children_to_tree(result['nodes'], node)
        return data['moveNode']

    def list_children(self, node_id):
        """获取子节点列表

        Args:
            node_id(str):节点ID
        """
        data = self.graphqlClient.request(
            query=QUERY['getChildrenNodes'],
            params={
                'nodeId': node_id
            },
            token=self.tokenProvider.getAccessToken()
        )
        return data['childrenNodes']

    def root_node(self, org_id):
        """获取根节点"""
        data = self.graphqlClient.request(
            query=QUERY['rootNode'],
            params={
                'orgId': org_id
            },
            token=self.tokenProvider.getAccessToken()
        )
        return data['rootNode']

    def import_by_json(self, json_str):
        """通过 JSON 导入

        Args:
            json_str(str):json字符串
        """
        url = "%s/api/v2/orgs/import" % self.options.host
        body ={
            'filetype': 'json',
            'file': json_str
        }
        return self.restClient.request(method='POST', token=self.tokenProvider.getAccessToken(), url=url, json=body)

    def add_members(self, node_id, user_ids):
        """节点添加成员

        Args:
            node_id(str):节点ID
            user_ids(list):用户ID集合
        """
        data = self.graphqlClient.request(
            query=QUERY['addMember'],
            params={
                'nodeId': node_id,
                'userIds': user_ids
            },
            token=self.tokenProvider.getAccessToken()
        )
        return data['addMember']

    def list_members(self,node_id, page=None,limit=None, include_children_nodes=None):
        """获取节点成员

        Args:
            node_id(str):节点ID
            page(int):分页号
            limit(int):每页记录数
            include_children_nodes(bool):是否级联子级用户
        """
        data = self.graphqlClient.request(
            query=QUERY['getMembersById'],
            params={
                'id': node_id,
                'page': page,
                'limit': limit,
                'includeChildrenNodes': include_children_nodes
            },
            token=self.tokenProvider.getAccessToken()
        )
        return data['nodeById']

    def move_members(self, user_ids, target_node_id, source_node_id):
        """移动节点成员

        Args:
            user_ids(list):用户集合
            target_node_id(str):目标节点ID
            source_node_id(str):源目标节点
        """
        data = self.graphqlClient.request(
            query=QUERY['moveMembers'],
            params={
                'userIds': user_ids,
                'targetNodeId': target_node_id,
                'sourceNodeId': source_node_id
            },
            token=self.tokenProvider.getAccessToken()
        )
        return data['moveMembers']

    def delete_members(self, node_id, user_ids):
        """删除节点成员

        Args:
            node_id(str):节点ID
            user_ids(list):用户ID集合
        """
        data = self.graphqlClient.request(
            query=QUERY['removeMembers'],
            params={
                'userIds': user_ids,
                'nodeId': node_id
            },
            token=self.tokenProvider.getAccessToken()
        )
        return data['removeMember']

    def export_all(self):
        """导出所有组织机构"""
        url = "%s/api/v2/orgs/export" % self.options.host
        return self.restClient.request(method='GET', token=self.tokenProvider.getAccessToken(), url=url)

    def set_main_department(self, user_id, department_id):
        """设置用户主部门

        Args:
            user_id(str):用户ID
            department_id(str):部门ID
        """
        data = self.graphqlClient.request(
            query=QUERY['setMainDepartment'],
            params={
                'userId': user_id,
                'departmentId': department_id
            },
            token=self.tokenProvider.getAccessToken()
        )
        return data['setMainDepartment']

    def export_by_org_id(self,org_id):
        """导出某个组织机构"""
        url = "%s/api/v2/orgs/export?org_id=%s" % (self.options.host, org_id)
        return self.restClient.request(method='GET', token=self.tokenProvider.getAccessToken(), url=url)

    def list_authorized_resources_by_code(self, org_id, code, namespace=None, resource_type=None):
        """获取组织机构节点被授权的所有资源

        Args:
            org_id (str): 组织机构部门的 ID；
            code(str): 组织机构Code
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
            query=QUERY['listNodeByCodeAuthorizedResources'],
            params={
                'orgId': org_id,
                'code': code,
                'namespace': namespace,
                'resourceType': resource_type
            },
            token=self.tokenProvider.getAccessToken()
        )
        data = data.get('nodeByCode')
        if not data:
            raise AuthingException(500, 'department not exists')

        authorized_resources = data.get('authorizedResources')
        _list, total_count = authorized_resources.get('list'), authorized_resources.get('totalCount')
        _list = format_authorized_resources(_list)
        return {
            'totalCount': total_count,
            'list': _list
        }

    def search_nodes(self, keyword):
        """搜索组织机构节点"""
        data = self.graphqlClient.request(
            query=QUERY['searchNodes'],
            params={
                'keyword': keyword
            },
            token=self.tokenProvider.getAccessToken()
        )
        return data['searchNodes']

    def start_sync(self, provider_type, ad_connector_id=None):
        """组织机构同步"""
        if provider_type not in ["dingtalk", "wechatwork", "ad"]:
            raise AuthingWrongArgumentException("provider_type value only ['dingtalk','wechatwork','ad']")
        url = "%s/connections/enterprise/%s/start-sync" % (self.options.host, provider_type)
        if provider_type == 'ad':
            url = "%s/api/v2/ad/sync" % self.options.host
            if ad_connector_id:
                raise AuthingWrongArgumentException("type is ad must provider adConnector_id")
            return self.restClient.request(method='POST', token=self.tokenProvider.getAccessToken(), url=url,
                                           json={
                                               "connectionId":ad_connector_id
                                           })
        return self.restClient.request(method='POST', token=self.tokenProvider.getAccessToken(), url=url,json={})
