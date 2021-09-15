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
