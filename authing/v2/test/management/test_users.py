# coding: utf-8
from datetime import datetime
from authing.v2.management.types import ManagementClientOptions
from authing.v2.management.authing import ManagementClient
from authing.v2.common.utils import get_random_string
import unittest
import os
from dotenv import load_dotenv

load_dotenv()

management = ManagementClient(ManagementClientOptions(
    user_pool_id=os.getenv('AUTHING_USERPOOL_ID'),
    secret=os.getenv('AUTHING_USERPOOL_SECRET'),
    host=os.getenv('AUTHING_SERVER'),
    use_unverified_ssl=True,
    # enc_public_key="""-----BEGIN PUBLIC KEY-----
    # MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDb+rq+GQ8L8hgi6sXph2Dqcih0
    # 4CfQt8Zm11GVhXh/0ad9uewFQIXMtytgdNfqFNiwSH5SQZSdA0AwDaYLG6Sc57L1
    # DFuHxzHbMf9b8B2WnyJl3S85Qt6wmjBNfyy+dYlugFt04ZKDxsklXW5TVlGNA5Cg
    # o/E0RlTdNza6FcAHeQIDAQAB
    # -----END PUBLIC KEY-----"""
))

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


class TestUsers(unittest.TestCase):
    pass

    def test_list(self):
        data = management.users.list()
        totalCount = data['totalCount']
        users = data['list']
        self.assertTrue(totalCount)
        self.assertTrue(users)

    def test_list_has_identities(self):
        data = management.users.list()
        total_count, _list = data.get('totalCount'), data.get('list')
        for user in _list:
            self.assertTrue(user.get('identities') is not None)
            self.assertTrue(isinstance(user.get('identities'), list))

    def test_list_with_custom_data(self):
        key = get_random_string(10)
        value = get_random_string(10)
        create_user(
            custom_data={
                key: value
            }
        )
        data = management.users.list(limit=200,with_custom_data=True)
        totalCount = data['totalCount']
        users = data['list']
        self.assertTrue(totalCount)
        self.assertTrue(users)
        self.assertTrue(users[0]['customData'][key] == value)

    def test_create(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        self.assertTrue(user)
        self.assertTrue(user['id'])

    def test_create_with_custom_data(self):
        udf_key = get_random_string(10)
        udf_value = get_random_string(10)
        management.udf.set(
            targetType='USER',
            dataType='STRING',
            key=udf_key,
            label=get_random_string(10)
        )
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            },
            custom_data={
                udf_key: udf_value
            }
        )
        self.assertTrue(user['customData'][udf_key] == udf_value)

    def test_update(self):
        username = get_random_string(10)
        password = get_random_string(10)
        user = management.users.create(
            userInfo={
                'username': username,
                'password': password
            }
        )
        nickname = get_random_string(10)
        user = management.users.update(
            userId=user['id'],
            updates={
                'nickname': nickname
            }
        )
        self.assertTrue(nickname == user.get('nickname'))

    def test_detail(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        newUser = management.users.detail(user_id=user['id'])
        self.assertTrue(user['id'] == newUser['id'])
        self.assertTrue(user['username'] == newUser['username'])

    def test_detail_with_custom_data_string(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        udf_key = get_random_string(10)
        udf_value = get_random_string(10)
        management.udf.set(
            targetType='USER',
            key=udf_key,
            dataType='STRING',
            label=get_random_string(10)
        )
        management.users.set_udf_value(user.get('id'), {
            udf_key: udf_value
        })

        user = management.users.detail(
            user_id=user.get('id'),
            with_custom_data=True
        )
        self.assertTrue(user['customData'][udf_key] == udf_value)

    def test_detail_with_custom_data_number(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        udf_key = get_random_string(10)
        udf_value = 10
        management.udf.set(
            targetType='USER',
            key=udf_key,
            dataType='NUMBER',
            label=get_random_string(10)
        )
        management.users.set_udf_value(user.get('id'), {
            udf_key: udf_value
        })

        user = management.users.detail(
            user_id=user.get('id'),
            with_custom_data=True
        )
        self.assertTrue(user['customData'][udf_key] == udf_value)

    def test_detail_with_custom_data_datetime(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        udf_key = get_random_string(10)
        udf_value = datetime.now()
        management.udf.set(
            targetType='USER',
            key=udf_key,
            dataType='DATETIME',
            label=get_random_string(10)
        )
        management.users.set_udf_value(user.get('id'), {
            udf_key: udf_value
        })
        user = management.users.detail(
            user_id=user.get('id'),
            with_custom_data=True
        )
        self.assertTrue(isinstance(user['customData'][udf_key], datetime))
        self.assertTrue(user['customData'][udf_key] == udf_value)

    def test_detail_with_custom_data_object(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        udf_key = get_random_string(10)
        udf_value = {
            'key': 'value'
        }
        management.udf.set(
            targetType='USER',
            key=udf_key,
            dataType='OBJECT',
            label=get_random_string(10)
        )
        management.users.set_udf_value(user.get('id'), {
            udf_key: udf_value
        })
        user = management.users.detail(
            user_id=user.get('id'),
            with_custom_data=True
        )
        self.assertTrue(isinstance(user['customData'][udf_key], dict))
        self.assertTrue(user['customData'][udf_key] == udf_value)

    def test_batch(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        users = management.users.batch(
            userIds=[user['id']]
        )
        self.assertTrue(len(users) == 1)

    def test_find(self):
        nickname = get_random_string(10)
        username = get_random_string(10)
        user = management.users.create(
            userInfo={
                'username': username,
                'password': get_random_string(10),
                'nickname': nickname
            }
        )
        user = management.users.find(username=username)
        self.assertTrue(user)

    def test_find_with_custom_data_string(self):
        username = get_random_string(10)
        user = management.users.create(
            userInfo={
                'username': username,
                'password': get_random_string(10)
            }
        )
        udf_key = get_random_string(10)
        udf_value = get_random_string(10)
        management.udf.set(
            targetType='USER',
            key=udf_key,
            dataType='STRING',
            label=get_random_string(10)
        )
        management.users.set_udf_value(user.get('id'), {
            udf_key: udf_value
        })

        user = management.users.find(
            username=username,
            with_custom_data=True
        )
        self.assertTrue(user['customData'][udf_key] == udf_value)

    def test_find_with_custom_data_number(self):
        username = get_random_string(10)
        user = management.users.create(
            userInfo={
                'username': username,
                'password': get_random_string(10)
            }
        )
        udf_key = get_random_string(10)
        udf_value = 10
        management.udf.set(
            targetType='USER',
            key=udf_key,
            dataType='NUMBER',
            label=get_random_string(10)
        )
        management.users.set_udf_value(user.get('id'), {
            udf_key: udf_value
        })

        user = management.users.find(
            username=username,
            with_custom_data=True
        )
        self.assertTrue(user['customData'][udf_key] == udf_value)

    def test_find_with_custom_data_datetime(self):
        username = get_random_string(10)
        user = management.users.create(
            userInfo={
                'username': username,
                'password': get_random_string(10)
            }
        )
        udf_key = get_random_string(10)
        udf_value = datetime.now()
        management.udf.set(
            targetType='USER',
            key=udf_key,
            dataType='DATETIME',
            label=get_random_string(10)
        )
        management.users.set_udf_value(user.get('id'), {
            udf_key: udf_value
        })
        user = management.users.find(
            username=username,
            with_custom_data=True
        )
        self.assertTrue(isinstance(user['customData'][udf_key], datetime))
        self.assertTrue(user['customData'][udf_key] == udf_value)

    def test_find_with_custom_data_object(self):
        username = get_random_string(10)
        user = management.users.create(
            userInfo={
                'username': username,
                'password': get_random_string(10)
            }
        )
        udf_key = get_random_string(10)
        udf_value = {
            'key': 'value'
        }
        management.udf.set(
            targetType='USER',
            key=udf_key,
            dataType='OBJECT',
            label=get_random_string(10)
        )
        management.users.set_udf_value(user.get('id'), {
            udf_key: udf_value
        })
        user = management.users.find(
            username=username,
            with_custom_data=True
        )
        self.assertTrue(isinstance(user['customData'][udf_key], dict))
        self.assertTrue(user['customData'][udf_key] == udf_value)


    def test_search(self):
        nickname = get_random_string(10)
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10),
                'nickname': nickname
            }
        )
        data = management.users.search(query=nickname)
        _list = data['list']
        userIds = list(map(lambda x: x['id'], _list))
        self.assertTrue(user['id'] in userIds)

    def test_search_with_custom_data(self):
        nickname = get_random_string(10)
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10),
                'nickname': nickname
            }
        )
        udf_key = get_random_string(10)
        udf_value = {
            'key': 'value'
        }
        management.udf.set(
            targetType='USER',
            key=udf_key,
            dataType='OBJECT',
            label=get_random_string(10)
        )
        management.users.set_udf_value(user.get('id'), {
            udf_key: udf_value
        })
        data = management.users.search(query=nickname, with_custom_data=True)
        user = data['list'][0]
        self.assertTrue(user['customData'][udf_key] == udf_value)

    def test_delete(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        data = management.users.delete(userId=user['id'])
        code = data['code']
        self.assertTrue(code == 200)

        newUser = management.users.detail(user_id=user['id'])
        self.assertTrue(newUser == None)

    def test_delete_many(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        data = management.users.delete_many(
            userIds=[user['id']]
        )
        code = data['code']
        self.assertTrue(code == 200)
        newUser = management.users.detail(user_id=user['id'])
        self.assertTrue(newUser == None)

    def test_list_roles(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        data = management.users.list_roles(
            userId=user['id']
        )
        totalCount = data['totalCount']
        self.assertTrue(totalCount == 0)

    def test_add_roles(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        data = management.roles.list()
        roles = data['list']
        management.users.add_roles(
            userId=user['id'],
            roles=list(map(lambda x: x['code'], roles))
        )
        data = management.users.list_roles(
            userId=user['id']
        )
        totalCount = data['totalCount']
        _list = data['list']
        self.assertTrue(len(_list) == totalCount)

    def test_remove_roles(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        data = management.roles.list()
        roles = data['list']
        management.users.add_roles(
            userId=user['id'],
            roles=list(map(lambda x: x['code'], roles))
        )
        management.users.remove_roles(
            userId=user['id'],
            roles=list(map(lambda x: x['code'], roles))
        )
        data = management.users.list_roles(
            userId=user['id']
        )
        totalCount = data['totalCount']
        _list = data['list']
        self.assertTrue(totalCount == 0)
        self.assertTrue(len(_list) == 0)

    def test_refresh_token(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        data = management.users.refresh_token(
            userId=user['id']
        )
        token, iat, exp = data['token'], data['iat'], data['exp']
        self.assertTrue(token)
        self.assertTrue(iat)
        self.assertTrue(exp)

        status = management.check_login_status(
            token=token)
        self.assertTrue(status)
        self.assertTrue(status['data']['id'] == user['id'])

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
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )

        d=management.users.add_policies(
            userId=user['id'],
            policies=[policy['code']]
        )

        data = management.users.list_policies(
            userId=user['id']
        )
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
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )

        management.users.add_policies(
            userId=user['id'],
            policies=[policy['code']]
        )
        d=management.users.remove_policies(
            userId=user['id'],
            policies=[policy['code']]
        )
        data = management.users.list_policies(
            userId=user['id']
        )
        totalCount = data['totalCount']
        _list = data['list']
        self.assertTrue(totalCount == 0)

    def test_add_udv_wrong_type(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )

        # 字符串
        failed = False
        try:
            management.udf.set(
                targetType='USER',
                key='school',
                dataType='STRING',
                label='学校'
            )
            management.users.set_udv(
                userId=user['id'],
                key='school',
                value=11
            )
        except:
            failed = True
        self.assertTrue(failed)

        # 数字
        failed = False
        try:
            management.udf.set(
                targetType='USER',
                key='age',
                dataType='NUMBER',
                label='学校'
            )
            management.users.set_udv(
                userId=user['id'],
                key='age',
                value='18'
            )
        except:
            failed = True
        self.assertTrue(failed)

        # boolean
        failed = False
        try:
            management.udf.set(
                targetType='USER',
                key='is_boss',
                dataType='BOOLEAN',
                label='是否为 boss'
            )
            management.users.set_udv(
                userId=user['id'],
                key='is_boss',
                value='ok'
            )
        except:
            failed = True
        self.assertTrue(failed)

    def test_add_udv_string(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        management.udf.set(
            targetType='USER',
            key='school',
            dataType='STRING',
            label='学校'
        )
        management.users.set_udv(
            userId=user['id'],
            key='school',
            value='ucla'
        )
        udvs = management.users.list_udv(user['id'])
        self.assertTrue(len(udvs) == 1)
        self.assertTrue(isinstance(udvs[0]['value'], str))

    def test_add_udv_int(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        management.udf.set(
            targetType='USER',
            key='age',
            dataType='NUMBER',
            label='学校'
        )
        management.users.set_udv(
            userId=user['id'],
            key='age',
            value=18
        )
        udvs = management.users.list_udv(user['id'])
        self.assertTrue(len(udvs) == 1)
        self.assertTrue(isinstance(udvs[0]['value'], int))

    def test_add_udv_boolean(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        management.udf.set(
            targetType='USER',
            key='is_boss',
            dataType='BOOLEAN',
            label='是否为 boss'
        )
        d=management.users.set_udv(
            userId=user['id'],
            key='is_boss',
            value=False
        )
        udvs = management.users.list_udv(user['id'])
        self.assertTrue(len(udvs) == 1)
        self.assertTrue(isinstance(udvs[0]['value'], bool))

    def test_add_udv_datetime(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        management.udf.set(
            targetType='USER',
            key='birthday',
            dataType='DATETIME',
            label='生日'
        )
        management.users.set_udv(
            userId=user['id'],
            key='birthday',
            value=datetime.now()
        )
        udvs = management.users.list_udv(user['id'])
        self.assertTrue(len(udvs) == 1)
        self.assertTrue(isinstance(udvs[0]['value'], datetime))

    def test_add_udv_object(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        management.udf.set(
            targetType='USER',
            key='settings',
            dataType='OBJECT',
            label='设置'
        )
        management.users.set_udv(
            userId=user['id'],
            key='settings',
            value={
                'favorColor': 'red'
            }
        )
        udvs = management.users.list_udv(user['id'])
        self.assertTrue(len(udvs) == 1)
        self.assertTrue(isinstance(udvs[0]['value'], dict))

    def test_remove_duv(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        management.udf.set(
            targetType='USER',
            key='age',
            dataType='NUMBER',
            label='学校'
        )
        management.users.set_udv(
            userId=user['id'],
            key='age',
            value=18
        )
        d = management.users.remove_udv(
            userId=user['id'],
            key='age',
        )
        udvs = management.users.list_udv(user['id'])
        self.assertTrue(len(udvs) == 0)

    def test_add_group(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        group = 'debug'
        data = management.users.add_group(user['id'], group)
        self.assertTrue(data['code'] == 200)

    def test_remove_group(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        group = 'debug'
        data = management.users.remove_group(user['id'], group)
        self.assertTrue(data['code'] == 200)

    def test_list_groups(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        data = management.users.list_groups(user['id'])
        self.assertTrue(data['totalCount'] != None)
        self.assertTrue(data['list'] != None)

    def test_list_archived_users(self):
        res = management.users.list_archived_users()

        self.assertTrue(res['list'] is not None)
        self.assertTrue(res['totalCount'] is not None)

    def test_exists(self):
        user = create_user()

        is_exists_user = management.users.exists(
            username=user["username"],
            email=user["email"],
            phone=user["phone"]
        )

        self.assertTrue(is_exists_user)

        random_user = management.users.exists(
            username=get_random_string(10)
        )

        self.assertFalse(random_user)

    def test_list_authorized_resources_case1(self):
        user = create_user()
        management.acl.authorize_resource(
            namespace='default',
            resource='books:*',
            opts=[
                {
                    'targetType': 'USER',
                    'targetIdentifier': user.get('id'),
                    'actions': [
                        'books:edit'
                    ]
                }
            ]
        )
        data = management.users.list_authorized_resources(
            user_id=user.get('id'),
            namespace="default",
        )
        _list, total_count = data.get('list'), data.get('totalCount')
        self.assertTrue(len(_list) == 1)
        self.assertTrue(total_count == 1)
        for item in _list:
            self.assertTrue(item.get('code'))
            self.assertTrue(item.get('code') == 'books:*')
            self.assertTrue(item.get('actions'))
            self.assertTrue(isinstance(item.get('actions'), list))
            self.assertTrue(len(item.get('actions')) == 1)

    def test_list_authorized_resources_case2(self):
        user = create_user()
        management.acl.authorize_resource(
            namespace='default',
            resource='books:1',
            opts=[
                {
                    'targetType': 'USER',
                    'targetIdentifier': user.get('id'),
                    'actions': [
                        'books:edit'
                    ]
                }
            ]
        )
        data = management.users.list_authorized_resources(
            user_id=user.get('id'),
            namespace="default",
        )
        _list, total_count = data.get('list'), data.get('totalCount')
        self.assertTrue(len(_list) == 1)
        self.assertTrue(total_count == 1)
        for item in _list:
            self.assertTrue(item.get('code'))
            self.assertTrue(item.get('code') == 'books:1')
            self.assertTrue(item.get('actions'))
            self.assertTrue(isinstance(item.get('actions'), list))
            self.assertTrue(len(item.get('actions')) == 1)


    def test_check_resource_permission_batch_case1(self):
        # 授权某一类资源，判断某个具体资源权限
        user = create_user()
        management.acl.authorize_resource(
            namespace='default',
            resource='books:*',
            opts=[
                {
                    'targetType': 'USER',
                    'targetIdentifier': user.get('id'),
                    'actions': [
                        'books:edit'
                    ]
                }
            ]
        )
        management.acl.authorize_resource(
            namespace='default',
            resource='orders:*',
            opts=[
                {
                    'targetType': 'USER',
                    'targetIdentifier': user.get('id'),
                    'actions': [
                        'orders:edit'
                    ]
                }
            ]
        )

        data = management.users.check_resource_permission_batch(
            user_id=user.get('id'),
            namespace='default',
            resources=['books:1', 'orders:2']
        )

        # 返回数据格式：[{'code': 'books:1', 'actions': ['books:edit']}, {'code': 'orders:2', 'actions': ['orders:edit']}]

        self.assertTrue(len(data) == 2)
        self.assertTrue(data[0]['code'] == 'books:1')
        self.assertTrue(data[0]['actions'])
        self.assertTrue(data[1]['code'] == 'orders:2')
        self.assertTrue(data[1]['actions'])

    def test_check_resource_permission_batch_case2(self):
        # 授权具体资源，判断具体资源权限
        user = create_user()
        management.acl.authorize_resource(
            namespace='default',
            resource='books:1',
            opts=[
                {
                    'targetType': 'USER',
                    'targetIdentifier': user.get('id'),
                    'actions': [
                        'books:edit'
                    ]
                }
            ]
        )
        management.acl.authorize_resource(
            namespace='default',
            resource='orders:2',
            opts=[
                {
                    'targetType': 'USER',
                    'targetIdentifier': user.get('id'),
                    'actions': [
                        'orders:edit'
                    ]
                }
            ]
        )

        data = management.users.check_resource_permission_batch(
            user_id=user.get('id'),
            namespace='default',
            resources=['books:1', 'orders:2']
        )

        # 返回数据格式：[{'code': 'books:1', 'actions': ['books:edit']}, {'code': 'orders:2', 'actions': ['orders:edit']}]

        self.assertTrue(len(data) == 2)
        self.assertTrue(data[0]['code'] == 'books:1')
        self.assertTrue(data[0]['actions'])
        self.assertTrue(data[1]['code'] == 'orders:2')
        self.assertTrue(data[1]['actions'])

    def test_check_resource_permission_batch_case3(self):
        # 授权具体资源，判断具体资源权限
        user = create_user()
        management.acl.authorize_resource(
            namespace='default',
            resource='books:1',
            opts=[
                {
                    'targetType': 'USER',
                    'targetIdentifier': user.get('id'),
                    'actions': [
                        'books:edit'
                    ]
                }
            ]
        )
        management.acl.authorize_resource(
            namespace='default',
            resource='orders:2',
            opts=[
                {
                    'targetType': 'USER',
                    'targetIdentifier': user.get('id'),
                    'actions': [
                        'orders:edit'
                    ]
                }
            ]
        )

        data = management.users.check_resource_permission_batch(
            user_id=user.get('id'),
            namespace='default',
            resources=['books:2', 'orders:1']
        )

        # 返回数据格式：[{'code': 'books:1', 'actions': ['books:edit']}, {'code': 'orders:2', 'actions': ['orders:edit']}]
        self.assertTrue(len(data) == 0)

    def test_check_resource_permission_batch_case4(self):
        # 授权具体资源，判断某类资源权限
        user = create_user()
        management.acl.authorize_resource(
            namespace='default',
            resource='books:1',
            opts=[
                {
                    'targetType': 'USER',
                    'targetIdentifier': user.get('id'),
                    'actions': [
                        'books:edit'
                    ]
                }
            ]
        )
        management.acl.authorize_resource(
            namespace='default',
            resource='orders:2',
            opts=[
                {
                    'targetType': 'USER',
                    'targetIdentifier': user.get('id'),
                    'actions': [
                        'orders:edit'
                    ]
                }
            ]
        )

        data = management.users.check_resource_permission_batch(
            user_id=user.get('id'),
            namespace='default',
            resources=['books:*', 'orders:*']
        )

        # 返回数据格式：[{'code': 'books:1', 'actions': ['books:edit']}, {'code': 'orders:2', 'actions': ['orders:edit']}]
        self.assertTrue(len(data) == 0)

    def test_check_resource_permission_batch_case5(self):
        # 授权某类资源，判断某类资源权限
        user = create_user()
        management.acl.authorize_resource(
            namespace='default',
            resource='books:*',
            opts=[
                {
                    'targetType': 'USER',
                    'targetIdentifier': user.get('id'),
                    'actions': [
                        'books:edit'
                    ]
                }
            ]
        )
        management.acl.authorize_resource(
            namespace='default',
            resource='orders:*',
            opts=[
                {
                    'targetType': 'USER',
                    'targetIdentifier': user.get('id'),
                    'actions': [
                        'orders:edit'
                    ]
                }
            ]
        )

        data = management.users.check_resource_permission_batch(
            user_id=user.get('id'),
            namespace='default',
            resources=['books:*', 'orders:*']
        )

        # 返回数据格式：[{'code': 'books:1', 'actions': ['books:edit']}, {'code': 'orders:2', 'actions': ['orders:edit']}]
        self.assertTrue(len(data) == 2)
        self.assertTrue(data[0]['code'] == 'books:*')
        self.assertTrue(data[0]['actions'])
        self.assertTrue(data[1]['code'] == 'orders:*')
        self.assertTrue(data[1]['actions'])

    def test_list_authorized_resources_of_resource_kind_case1(self):
        user = create_user()
        management.acl.authorize_resource(
            namespace='default',
            resource='books:1',
            opts=[
                {
                    'targetType': 'USER',
                    'targetIdentifier': user.get('id'),
                    'actions': [
                        'books:edit'
                    ]
                }
            ]
        )
        data = management.users.list_authorized_resources_of_resource_kind(user_id=user['id'], namespace='default', resource='books')
        self.assertTrue(len(data) == 1)
        self.assertTrue(data[0]['code'] == 'books:1')
        self.assertTrue(data[0]['actions'])

    def test_list_authorized_resources_of_resource_kind_case2(self):
        user = create_user()
        management.acl.authorize_resource(
            namespace='default',
            resource='books:1',
            opts=[
                {
                    'targetType': 'USER',
                    'targetIdentifier': user.get('id'),
                    'actions': [
                        'books:edit'
                    ]
                }
            ]
        )
        management.acl.authorize_resource(
            namespace='default',
            resource='books:2',
            opts=[
                {
                    'targetType': 'USER',
                    'targetIdentifier': user.get('id'),
                    'actions': [
                        'books:edit'
                    ]
                }
            ]
        )
        management.acl.authorize_resource(
            namespace='default',
            resource='orders:2',
            opts=[
                {
                    'targetType': 'USER',
                    'targetIdentifier': user.get('id'),
                    'actions': [
                        'books:edit'
                    ]
                }
            ]
        )
        data = management.users.list_authorized_resources_of_resource_kind(user_id=user['id'], namespace='default', resource='books')
        self.assertTrue(len(data) == 2)
        self.assertTrue(data[0]['code'] == 'books:1')
        self.assertTrue(data[0]['actions'])
        self.assertTrue(data[1]['code'] == 'books:2')
        self.assertTrue(data[1]['actions'])

    def test_list_authorized_resources_without_namespace(self):
        user = create_user()
        namespace_code = get_random_string(10)
        management.acl.create_namespace(namespace_code, namespace_code)
        management.acl.authorize_resource(
            namespace='default',
            resource='books:*',
            opts=[
                {
                    'targetType': 'USER',
                    'targetIdentifier': user.get('id'),
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
                    'targetType': 'USER',
                    'targetIdentifier': user.get('id'),
                    'actions': [
                        'orders:edit'
                    ]
                }
            ]
        )
        data = management.users.list_authorized_resources(
            user_id=user.get('id'),
        )
        _list, total_count = data.get('list'), data.get('totalCount')
        self.assertTrue(len(_list) == 2)
        self.assertTrue(total_count == 2)

    def test_set_udf_value(self):
        user = create_user()
        management.users.set_udf_value(
            user_id=user.get('id'),
            data={
                'school': '华中科技大学',
                'age': 22
            }
        )
        values = management.users.get_udf_value(user_id=user.get('id'))
        self.assertTrue(values['school'] == '华中科技大学')
        self.assertTrue(values['age'] == 22)

    def test_set_udf_value_batch(self):
        user1 = create_user()
        user2 = create_user()

        user1_id = user1.get('id')
        user2_id = user2.get('id')
        management.users.set_udf_value_batch(
            {
                user1_id: {
                    'school': '华中科技大学',
                    'age': 22
                },
                user2_id: {
                    'school': '华中科技大学',
                    'age': 22
                }
            }
        )

        values1 = management.users.get_udf_value(user_id=user1_id)
        self.assertTrue(values1['school'] == '华中科技大学')
        self.assertTrue(values1['age'] == 22)

        values2 = management.users.get_udf_value(user_id=user2_id)
        self.assertTrue(values2['school'] == '华中科技大学')
        self.assertTrue(values2['age'] == 22)

    def test_batch_get_with_custom_data(self):
        key = get_random_string(10)
        value1 = get_random_string(10)
        value2 = get_random_string(10)
        user1 = create_user({
            key: value1
        })
        user2 = create_user({
            key: value2
        })
        user1_id = user1.get('id')
        user2_id = user2.get('id')

        users = management.users.batch_get([user1_id, user2_id], with_custom_data=True)
        self.assertTrue(len(users) == 2)

        self.assertTrue(users[0]['customData'][key] == value1)
        self.assertTrue(users[1]['customData'][key] == value2)

    def test_kick_users(self):
        success = management.users.kick(['5a597f35085a2000144a10ed'])
        self.assertTrue(success)

    def test_list_user_actions(self):
        res = management.users.list_user_actions()
        print(res)

    def test_list_org(self):
        res = management.users.list_org('613872b19c90be7d4da44466')
        self.assertIsNotNone(res)

    def test_list_dept(self):
        res = management.users.list_department('613872b19c90be7d4da44466')
        self.assertIsNotNone(res)


    def test_has_role(self):
       has = management.users.has_role(user_id='613ad439397280659fc1a056',role_code='vureo')
       self.assertTrue(has)

    def test_send_first_login_email(self):
        res = management.users.send_first_login_verify_email(app_id="6139c4d24e78a4d706b7545b",user_id="613872b19c90be7d4da44466")
        self.assertEquals(res['message'],'发送成功')

    def test_logout(self):
        res = management.users.logout("613872b19c90be7d4da44466")
        self.assertEquals(res['code'], 200)

    def test_check_login_status(self):
        res = management.users.check_login_status("613872b19c90be7d4da44466")
        self.assertEquals(res['message'],'用户不存在')