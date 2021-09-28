# coding: utf-8
import json

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
    def test_list_authorized_resources(self):
        node_id = '6139a937437e50e4d31770a2'
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
        node_id = '612333f55fca511687cafde5'
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

    def test_list_authorized_resources_by_code(self):

        data = management.org.list_authorized_resources_by_code(
            code='codes',
            org_id='6142c2c41c6e6c6cc3edfd88',
            namespace='default'
        )
        _list, total_count = data.get('list'), data.get('totalCount')
        self.assertTrue(len(_list) == 1)
        self.assertTrue(total_count == 1)


    def test_create(self):
        result = management.org.create("xx21")
        self.assertEquals(result['rootNode']['name'],"xx21")

    def test_list(self):
        result = management.org.list(treeify=True)
        self.assertIsNotNone(result['list'])

    def test_add_node(self):
        result = management.org.add_node(org_id='6142c2c41c6e6c6cc3edfd88', parent_node_id='6142c2c4f8abf18c6c978b2c',
                                       name='add')
        self.assertEquals(result['id'], '6142c2c41c6e6c6cc3edfd88')

    def test_delete_by_id(self):
        result = management.org.delete_by_id('614c3822355bb8538eb5b663')
        self.assertEquals(result['code'], 200)

    def test_get_node_by_id(self):
        result = management.org.get_node_by_id("6142c32360021c1a05081579")
        self.assertEquals(result['id'],'6142c32360021c1a05081579')

    def test_update_node(self):
        result = management.org.update_node('6142c32360021c1a05081579', name='qqqx')
        self.assertEquals(result['name'], 'qqqx')

    def test_find_by_id(self):
        result = management.org.find_by_id('6142c2c41c6e6c6cc3edfd88',treeify=True)
        self.assertEquals(result['id'], '6142c2c41c6e6c6cc3edfd88')

    def test_delete_node(self):
        result = management.org.delete_node(org_id="6142c2c41c6e6c6cc3edfd88", node_id='614c3c5372b6b3f340ab6937')
        self.assertEquals(result['code'], 200)

    def test_is_root_node(self):
        result = management.org.is_root_node(org_id="6142c2c41c6e6c6cc3edfd88",node_id='6142e08f64d5a8873598e9fb')
        self.assertFalse(result)

    def test_move_node(self):
        result = management.org.move_node(org_id="6142c2c41c6e6c6cc3edfd88", node_id='6142e08f64d5a8873598e9fb',
                                          target_parent_id='6142e03436f09aa7e66c1935')
        result['nodes']

    def test_list_children(self):
        result = management.org.list_children("6142c32360021c1a05081579")
        self.assertTrue(isinstance(result,list))

    def test_root_node(self):
        result = management.org.root_node("6142c2c41c6e6c6cc3edfd88")
        self.assertIsNotNone(result)

    def test_import_by_json(self):
        json ="""
                {
                    "name": "北京非凡科技有限公司",
                    "code": "feifan",
                    "children": []
            } """
        result = management.org.import_by_json(json)
        print (result)

    def test_add_members(self):
        result = management.org.add_members("6142e833716601219e93d813",["6141876341abedef979c3740"]);
        self.assertIsNotNone(result['users'])

    def test_list_members(self):
        result = management.org.list_members(node_id='6142e833716601219e93d813',page=2)
        self.assertIsNotNone(result['users'])

    def test_move_members(self):
        result = management.org.move_members(["6141876341abedef979c3740"], target_node_id="6142e08f64d5a8873598e9fb",
                                             source_node_id="6142e83c8db6a68ea5e62aca")
        self.assertEquals(result['code'], 200)

    def test_remove_members(self):
        res = management.org.delete_members("6142e08f64d5a8873598e9fb",["6141876341abedef979c3740"])
        self.assertTrue(res['users']['list'] == [])

    def test_export_all(self):
        res = management.org.export_all()
        self.assertEquals(res['message'],'导出数据成功')

    def test_set_main_dept(self):
        res = management.org.set_main_department("6141876341abedef979c3740","6142e0483f54818690c99600")
        self.assertEquals(res['code'], 200)

    def test_export_by_org_id(self):
        res = management.org.export_by_org_id('6142c2c41c6e6c6cc3edfd88')
        self.assertEquals(res['code'], 200)

    def test_search_nodes(self):
        res = management.org.search_nodes("xx2")
        self.assertEquals(res['name'], 'xx2')

    def test_start_sync(self):
        res = management.org.start_sync(provider_type="dingtalk")
        self.assertEquals(res['message'],u'你还没有配置钉钉通讯录')