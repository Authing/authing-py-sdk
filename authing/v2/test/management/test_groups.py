# coding: utf-8
import json

from authing.v2.common.utils import get_random_string
import unittest
import os
from authing.v2.management.types import ManagementClientOptions
from authing.v2.management.authing import ManagementClient
from dotenv import load_dotenv

load_dotenv()

management = ManagementClient(ManagementClientOptions(
    user_pool_id=os.getenv('AUTHING_USERPOOL_ID'),
    secret=os.getenv('AUTHING_USERPOOL_SECRET'),
    host=os.getenv('AUTHING_SERVER')
))


def create_group():
    code = get_random_string(5)
    name = get_random_string(5)
    group = management.groups.create(code=code, name=name)
    return group


def create_user():
    user = management.users.create(
        userInfo={
            'username': get_random_string(10),
            'password': get_random_string(10)
        }
    )
    return user


class TestRoles(unittest.TestCase):
    def test_list(self):
        totalCount, _list = management.roles.list()
        self.assertTrue(totalCount)
        self.assertTrue(_list)

    def test_create(self):
        group = create_group()
        print(json.dumps(group, indent=4))
        self.assertTrue(group)
        self.assertTrue(group['code'])

    def test_detail(self):
        group1 = create_group()
        code = group1.get('code')
        group2 = management.groups.detail(code)
        self.assertTrue(group1.get('code') == group2.get('code'))
        self.assertTrue(group1.get('name') == group2.get('name'))
        self.assertTrue(group1.get('description') == group2.get('description'))

    def test_update(self):
        group = create_group()
        code = group.get('code')
        name = get_random_string(10)
        desc = get_random_string(10)
        new_group = management.groups.update(code, name=name, description=desc)
        self.assertTrue(new_group.get('code') == code)
        self.assertTrue((new_group.get('name') == name))
        self.assertTrue(new_group.get('description') == desc)

    def test_update_code(self):
        group = create_group()
        code = group.get('code')
        new_code = get_random_string(10)
        new_group = management.groups.update(
            code=code,
            new_code=new_code
        )
        self.assertTrue(new_group.get('code') == new_code)
        self.assertTrue(new_group.get('code') != code)

    def test_list(self):
        group = create_group()
        data = management.groups.list()
        _list, total_count = data.get('list'), data.get('totalCount')
        self.assertTrue(total_count > 0)
        self.assertTrue(len(_list) > 0)

    def test_delete(self):
        group = create_group()
        code = group.get('code')

        management.groups.delete(code)

        group2 = management.groups.detail(code=code)
        self.assertTrue(group2 is None)

    def test_delete_many(self):
        group = create_group()
        code = group.get('code')

        management.groups.delete_many(code_list=[code])
        group2 = management.groups.detail(code=code)
        self.assertTrue(group2 is None)

    def test_add_users(self):
        user1 = create_user()
        user2 = create_user()
        group = create_group()
        code = group.get('code')

        data = management.groups.add_users(code=code, user_ids=[user1.get('id'), user2.get('id')])
        code, message = data.get('code'), data.get('message')
        self.assertTrue(code == 200)

    def test_list_users(self):
        user1 = create_user()
        user2 = create_user()
        group = create_group()
        code = group.get('code')
        # management.groups.add_users(code=code, user_ids=[user1.get('id'), user2.get('id')])

        data = management.groups.list_users('pngrn')
        _list, total_count = data.get('list'), data.get('totalCount')
        self.assertTrue(len(_list) == 2)
        self.assertTrue(total_count == 2)

        for user in _list:
            self.assertTrue(user.get('status') is not None)
            self.assertTrue(user.get('lastIP') is not None)

    def test_remove_users(self):
        user1 = create_user()
        user2 = create_user()
        group = create_group()
        code = group.get('code')
        management.groups.add_users(code=code, user_ids=[user1.get('id'), user2.get('id')])
        management.groups.remove_users(code=code, user_ids=[user1.get('id'), user2.get('id')])

        data = management.groups.list_users(code)
        _list, total_count = data.get('list'), data.get('totalCount')
        self.assertTrue(len(_list) == 0)
        self.assertTrue(total_count == 0)

    def test_list_authorized_resources(self):
        group = create_group()
        management.acl.authorize_resource(
            namespace='default',
            resource='books:*',
            opts=[
                {
                    'targetType': 'GROUP',
                    'targetIdentifier': group.get('code'),
                    'actions': [
                        'books:edit'
                    ]
                }
            ]
        )

        data = management.groups.list_authorized_resources(
            namespace='default',
            code=group.get('code')
        )
        _list, total_count = data.get('list'), data.get('totalCount')
        self.assertTrue(len(_list) == 1)
        self.assertTrue(total_count == 1)

    def test_list_authorized_resources_without_namespace(self):
        group = create_group()
        namespace_code = get_random_string(10)
        management.acl.create_namespace(namespace_code, namespace_code)
        management.acl.authorize_resource(
            namespace='default',
            resource='books:*',
            opts=[
                {
                    'targetType': 'GROUP',
                    'targetIdentifier': group.get('code'),
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
                    'targetType': 'GROUP',
                    'targetIdentifier': group.get('code'),
                    'actions': [
                        'books:edit'
                    ]
                }
            ]
        )
        data = management.groups.list_authorized_resources(
            code=group.get('code')
        )
        _list, total_count = data.get('list'), data.get('totalCount')
        self.assertTrue(len(_list) == 2)
        self.assertTrue(total_count == 2)
