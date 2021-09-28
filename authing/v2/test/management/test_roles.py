# coding: utf-8
from ...common.utils import get_random_string
import unittest
import os
from ...management.types import ManagementClientOptions
from ...management.authing import ManagementClient
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

management = ManagementClient(ManagementClientOptions(
    user_pool_id=os.getenv('AUTHING_USERPOOL_ID'),
    secret=os.getenv('AUTHING_USERPOOL_SECRET'),
    host=os.getenv('AUTHING_SERVER'),
    # enc_public_key="""-----BEGIN PUBLIC KEY-----
    # MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDb+rq+GQ8L8hgi6sXph2Dqcih0
    # 4CfQt8Zm11GVhXh/0ad9uewFQIXMtytgdNfqFNiwSH5SQZSdA0AwDaYLG6Sc57L1
    # DFuHxzHbMf9b8B2WnyJl3S85Qt6wmjBNfyy+dYlugFt04ZKDxsklXW5TVlGNA5Cg
    # o/E0RlTdNza6FcAHeQIDAQAB
    # -----END PUBLIC KEY-----"""
))


def create_role():
    code = get_random_string(5)
    role = management.roles.create(code=code)
    return role


def create_user(custom_data=None):
    if custom_data:
        for key, value in custom_data.items():
            management.udf.set(
                targetType='USER',
                dataType='STRING',
                label=get_random_string(10),
                key=key
            )
    user = management.users.create(
        userInfo={
            'username': get_random_string(10),
            'password': get_random_string(10)
        },
        custom_data=custom_data
    )

    return user


namespace = 'default'


class TestRoles(unittest.TestCase):
    def test_list(self):
        data = management.roles.list()
        self.assertTrue(data['totalCount'])
        self.assertTrue(data['list'])

    def test_list_with_namespace(self):
        data = management.roles.list(namespace=namespace)
        self.assertTrue(data['totalCount'])
        self.assertTrue(data['list'])

    def test_create(self):
        role = create_role()
        self.assertIsNotNone(role['id'])

    def test_create_with_namespace(self):
        code = get_random_string(5)
        role = management.roles.create(code=code, namespace=namespace)
        self.assertIsNotNone(role['id'])

    def test_detail(self):
        code = get_random_string(5)
        management.roles.create(code=code)
        role = management.roles.detail(code=code)
        self.assertEquals(role['code'],code)

    def test_detail_with_namespace(self):
        code = get_random_string(5)
        management.roles.create(code=code, namespace=namespace)
        role = management.roles.detail(code=code, namespace=namespace)
        self.assertEquals(role['code'], code)

    def test_update(self):
        code = get_random_string(5)
        management.roles.create(code=code)
        desc = get_random_string(10)
        role = management.roles.update(code=code, description=desc)
        self.assertEquals(role['description'], desc)

    def test_update_with_namespace(self):
        code = get_random_string(5)
        management.roles.create(code=code, namespace=namespace)
        desc = get_random_string(10)
        role = management.roles.update(code=code, description=desc, namespace=namespace)
        self.assertEquals(role['description'],desc)

    def test_update_with_new_code(self):
        code = get_random_string(5)
        management.roles.create(code=code)

        newCode = get_random_string(5)
        role = management.roles.update(code=code, newCode=newCode)
        self.assertEquals(role['code'],newCode)

    def test_update_with_new_code_with_namespace(self):
        code = get_random_string(5)
        management.roles.create(code=code, namespace=namespace)

        newCode = get_random_string(5)
        role = management.roles.update(code=code, newCode=newCode, namespace=namespace)
        self.assertEquals(role['code'] , newCode)

    def test_delete(self):
        role = management.roles.create(
            code=get_random_string(5)
        )
        data = management.roles.delete(code=role['code'])
        status_code = data['code']
        self.assertTrue(status_code == 200)

        newRole = management.roles.detail(code=role['code'])
        self.assertIsNone(newRole)

    def test_delete_namespace(self):
        role = management.roles.create(
            code=get_random_string(5),
            namespace=namespace
        )
        data = management.roles.delete(code=role['code'], namespace=namespace)
        status_code = data['code']
        self.assertTrue(status_code == 200)

        newRole = management.roles.detail(code=role['code'], namespace=namespace)
        self.assertIsNone(newRole )

    def test_delete_many(self):
        role = management.roles.create(
            code=get_random_string(5)
        )
        data = management.roles.delete_many(code_list=[role['code']])
        status_code = data['code']
        self.assertEquals(status_code, 200)

        newRole = management.roles.detail(code=role['code'])
        self.assertIsNone(newRole )

    def test_delete_many_with_namespace(self):
        role = management.roles.create(
            code=get_random_string(5),
            namespace=namespace
        )
        data = management.roles.delete_many(code_list=[role['code']], namespace=namespace)
        status_code = data['code']
        self.assertEquals(status_code , 200)

        newRole = management.roles.detail(code=role['code'], namespace=namespace)
        self.assertIsNone(newRole)

    def test_list_users(self):
        # role = management.roles.create(
        #     code=get_random_string(5)
        # )
        data = management.roles.list_users(code='uqetc',namespace=namespace)
        totalCount = data['totalCount']
        users = data['list']
        self.assertTrue(totalCount == 0)
        self.assertTrue(len(users) == 0)

    def test_list_users_with_custom_data(self):
        key = get_random_string(10)
        value = get_random_string(10)
        user = create_user({
            key: value
        })
        code = get_random_string(5)
        role = management.roles.create(
            code=code
        )
        management.roles.add_users(
            code=code,
            userIds=[user.get('id')]
        )

        data = management.roles.list_users(role['code'], with_custom_data=True)
        totalCount = data['totalCount']
        users = data['list']
        self.assertTrue(totalCount == 1)
        self.assertTrue(users[0]['customData'][key] == value)

    def test_list_users_with_namespace(self):
        role = management.roles.create(
            code=get_random_string(5),
            namespace=namespace
        )
        data = management.roles.list_users(role['code'], namespace=namespace)
        totalCount = data['totalCount']
        users = data['list']
        self.assertTrue(totalCount == 0)
        self.assertTrue(len(users) == 0)

    def test_add_users(self):
        role = management.roles.create(
            code=get_random_string(5)
        )
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        management.roles.add_users(role['code'], [user['id']])
        data = management.roles.list_users(role['code'])
        totalCount = data['totalCount']
        users = data['list']
        self.assertTrue(totalCount == 1)
        self.assertTrue(len(users) == 1)

    def test_add_users_with_namespace(self):
        role = management.roles.create(
            code=get_random_string(5),
            namespace=namespace
        )
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        management.roles.add_users(role['code'], [user['id']], namespace=namespace)
        data = management.roles.list_users(role['code'], namespace=namespace)
        totalCount = data['totalCount']
        users = data['list']
        self.assertTrue(totalCount == 1)
        self.assertTrue(len(users) == 1)

    def test_remove_users(self):
        role = management.roles.create(
            code=get_random_string(5)
        )
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        management.roles.add_users(role['code'], [user['id']])
        management.roles.remove_users(role['code'], [user['id']])
        data = management.roles.list_users(role['code'])
        totalCount = data['totalCount']
        users = data['list']
        self.assertTrue(totalCount == 0)
        self.assertTrue(len(users) == 0)

    def test_remove_users_with_namespace(self):
        role = management.roles.create(
            code=get_random_string(5),
            namespace=namespace
        )
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        management.roles.add_users(role['code'], [user['id']], namespace=namespace)
        management.roles.remove_users(role['code'], [user['id']], namespace=namespace)
        data = management.roles.list_users(role['code'], namespace=namespace)
        totalCount = data['totalCount']
        users = data['list']
        self.assertTrue(totalCount == 0)
        self.assertTrue(len(users) == 0)

    def test_add_policies(self):
        policy = management.policies.create(
            code=get_random_string(10),
            statements=[
                {
                    'resource': 'book:123',
                    'actions': ['books:read'],
                    'effect': 'ALLOW'
                }
            ]
        )
        role = create_role()
        management.roles.add_policies(role['code'], [policy['code']])
        data = management.roles.list_policies(role['code'])
        totalCount = data['totalCount']
        self.assertTrue(totalCount == 1)

    def test_remove_policies(self):
        policy = management.policies.create(
            code=get_random_string(10),
            statements=[
                {
                    'resource': 'book:123',
                    'actions': ['books:read'],
                    'effect': 'ALLOW'
                }
            ]
        )
        role = create_role()
        management.roles.add_policies(role['code'], [policy['code']])
        management.roles.remove_policies(role['code'], [policy['code']])
        data = management.roles.list_policies(role['code'])
        totalCount = data['totalCount']
        self.assertTrue(totalCount == 0)

    def test_get_udf_value(self):
        role = create_role()
        id = role.get('id')
        values = management.roles.get_udf_value('613acf1c57331c1246a80c0d')
        self.assertTrue(values is not None)

    def test_get_specific_udf_value(self):
        role = create_role()
        id = role.get('id')
        key = get_random_string(10)
        value = get_random_string(10)
        management.udf.set(
            targetType='ROLE',
            key=key,
            dataType='STRING',
            label=get_random_string()
        )
        management.roles.set_udf_value(id, {key: value})
        ret_value = management.roles.get_specific_udf_value(id, key)
        self.assertTrue(ret_value == value)

    def test_set_udf_value_int_type(self):
        role = create_role()
        key = get_random_string()
        value = 10
        management.udf.set(
            targetType='ROLE',
            key=key,
            dataType='NUMBER',
            label=get_random_string()
        )
        management.roles.set_udf_value(role.get('id'), {
            key: value
        })
        ret_value = management.roles.get_specific_udf_value(role.get('id'), key)
        self.assertTrue(value == ret_value)

    def test_set_udf_value_boolean_type(self):
        role = create_role()
        key = get_random_string()
        value = False
        management.udf.set(
            targetType='ROLE',
            key=key,
            dataType='BOOLEAN',
            label=get_random_string()
        )
        management.roles.set_udf_value(role.get('id'), {
            key: value
        })
        ret_value = management.roles.get_specific_udf_value(role.get('id'), key)
        self.assertTrue(value == ret_value)

    def test_set_udf_value_datetime_type(self):
        role = create_role()
        key = get_random_string()
        value = datetime.now()
        management.udf.set(
            targetType='ROLE',
            key=key,
            dataType='DATETIME',
            label='生日'
        )
        management.roles.set_udf_value(role.get('id'), {
            key: value
        })
        ret_value = management.roles.get_specific_udf_value(role.get('id'), key)
        self.assertTrue(isinstance(ret_value, datetime))

    def test_set_udf_value_dict_type(self):
        role = create_role()
        key = get_random_string()
        value = {
            'favorColor': 'red'
        }
        management.udf.set(
            targetType='ROLE',
            key=key,
            dataType='OBJECT',
            label='设置'
        )
        management.roles.set_udf_value(role.get('id'), {
            key: value
        })
        ret_value = management.roles.get_specific_udf_value(role.get('id'), key)
        self.assertTrue(isinstance(ret_value, dict))

    def test_get_udf_value_batch(self):
        role1 = create_role()
        role2 = create_role()
        key = get_random_string(10)
        value = get_random_string(10)
        management.udf.set(
            targetType='ROLE',
            key=key,
            dataType='STRING',
            label=get_random_string()
        )
        management.roles.set_udf_value(role1.get('id'), {
            key: value
        })
        management.roles.set_udf_value(role2.get('id'), {
            key: value
        })

        data = management.roles.get_udf_value_batch([role1.get('id'), role2.get('id')])
        role1_udvs = data.get(role1.get('id'))
        role2_udvs = data.get(role2.get('id'))

        self.assertTrue(role1_udvs.get(key) == value)
        self.assertTrue(role2_udvs.get(key) == value)

    def test_set_udf_value_batch(self):
        role1 = create_role()
        role2 = create_role()
        role1_id = role1.get('id')
        role2_id = role2.get('id')
        key = get_random_string(10)
        value = get_random_string(10)
        management.udf.set(
            targetType='ROLE',
            key=key,
            dataType='STRING',
            label=get_random_string()
        )

        management.roles.set_udf_value_batch(
            {
                role1_id: {
                    key: value
                },
                role2_id: {
                    key: value
                }
            }
        )
        data = management.roles.get_udf_value_batch([role1_id, role2_id])
        role1_udvs = data.get(role1.get('id'))
        role2_udvs = data.get(role2.get('id'))

        self.assertTrue(role1_udvs.get(key) == value)
        self.assertTrue(role2_udvs.get(key) == value)

    def test_remove_udf_value(self):
        role = create_role()
        key = get_random_string()
        value = 10
        management.udf.set(
            targetType='ROLE',
            key=key,
            dataType='NUMBER',
            label=get_random_string()
        )
        management.roles.set_udf_value(role.get('id'), {
            key: value
        })
        management.roles.remove_udf_value(role.get('id'), key)
        ret_value = management.roles.get_specific_udf_value(role.get('id'), key)
        self.assertTrue(ret_value is None)
