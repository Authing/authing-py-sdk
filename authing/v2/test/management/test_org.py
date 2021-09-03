from ...common.utils import get_random_string
import unittest
import os
from ...management.types import ManagementClientOptions
from ...management.authing import ManagementClient
from dotenv import load_dotenv

load_dotenv()

management = ManagementClient(ManagementClientOptions(
    user_pool_id=os.getenv('AUTHING_USERPOOL_ID'),
    secret=os.getenv('AUTHING_USERPOOL_SECRET'),
    host=os.getenv('AUTHING_SERVER')
))


class TestRoles(unittest.TestCase):

    def test_create_org(self):
        name = '测试组织机构'
        org = management.org.create_org(name)
        self.assertTrue(org['rootNode'])
        self.assertTrue(org['rootNode']['name'] == name)

    def test_add_roles(self):
        role_code = get_random_string(10)
        management.roles.create(role_code)
        org = management.org.create_org('测试组织机构')
        node_id = org['rootNode']['id']
        management.org.add_roles(node_id, [role_code])

        assigned_roles = management.org.list_roles(node_id)
        total_count, _list = assigned_roles.get('totalCount'), assigned_roles.get('list')
        self.assertTrue(total_count == 1)
        self.assertTrue(len(_list) == 1)
        self.assertTrue(_list[0]['code'] == role_code)

    def test_remove_roles(self):
        role_code = get_random_string(10)
        management.roles.create(role_code)
        org = management.org.create_org('测试组织机构')
        node_id = org['rootNode']['id']
        management.org.add_roles(node_id, [role_code])
        management.org.remove_roles(node_id, [role_code])

        assigned_roles = management.org.list_roles(node_id)
        total_count, _list = assigned_roles.get('totalCount'), assigned_roles.get('list')
        self.assertTrue(total_count == 0)
        self.assertTrue(len(_list) == 0)

    def test_inherited_from_parent_node(self):
        role_code = get_random_string(10)
        management.roles.create(role_code)
        org = management.org.create_org('测试组织机构')
        node_id1 = org['rootNode']['id']
        node_2 = management.org.create_node(
            name=get_random_string(10),
            org_id=org['id'],
            parent_node_id=node_id1
        )
        node_2_id = node_2['id']

        management.org.add_roles(node_id1, [role_code])
        assigned_roles = management.org.list_roles(node_2_id)
        total_count, _list = assigned_roles.get('totalCount'), assigned_roles.get('list')
        self.assertTrue(total_count == 1)
        self.assertTrue(len(_list) == 1)

    def test_inherited_from_parent_node_duplicate(self):
        role_code = get_random_string(10)
        management.roles.create(role_code)
        org = management.org.create_org('测试组织机构')
        node_id1 = org['rootNode']['id']
        node_2 = management.org.create_node(
            name=get_random_string(10),
            org_id=org['id'],
            parent_node_id=node_id1
        )
        node_2_id = node_2['id']

        management.org.add_roles(node_id1, [role_code])
        management.org.add_roles(node_2_id, [role_code])
        assigned_roles = management.org.list_roles(node_2_id)
        total_count, _list = assigned_roles.get('totalCount'), assigned_roles.get('list')
        self.assertTrue(total_count == 1)
        self.assertTrue(len(_list) == 1)

    def test_list_authorized_resources(self):
        org = management.org.create_org('测试组织机构')
        node_id = org['rootNode']['id']
        management.acl.authorize_resource(
            namespace='default',
            resource='books:*',
            opts=[
                {
                    'targetType': 'ORG',
                    'targetIdentifier': node_id,
                    'actions': [
                        'books:edit'
                    ]
                }
            ]
        )

        data = management.org.list_authorized_resources(
            node_id=node_id,
            namespace='default'
        )
        _list, total_count = data.get('list'), data.get('totalCount')
        self.assertTrue(len(_list) == 1)
        self.assertTrue(total_count == 1)

    def test_list_authorized_resources_without_namespace(self):
        org = management.org.create_org('测试组织机构')
        node_id = org['rootNode']['id']
        namespace_code = get_random_string(10)
        management.acl.create_namespace(namespace_code, namespace_code)
        management.acl.authorize_resource(
            namespace='default',
            resource='books:*',
            opts=[
                {
                    'targetType': 'ORG',
                    'targetIdentifier': node_id,
                    'actions': [
                        'books:edit'
                    ]
                }
            ]
        )
        management.acl.authorize_resource(
            namespace=namespace_code,
            resource='orders:*',
            opts=[
                {
                    'targetType': 'ORG',
                    'targetIdentifier': node_id,
                    'actions': [
                        'books:edit'
                    ]
                }
            ]
        )
        data = management.org.list_authorized_resources(
            node_id
        )
        _list, total_count = data.get('list'), data.get('totalCount')
        self.assertTrue(len(_list) == 2)
        self.assertTrue(total_count == 2)
