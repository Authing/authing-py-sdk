from datetime import datetime
from ...management.types import ManagementClientOptions
from ...management.authing import ManagementClient
from ...test.utils import get_random_string
import unittest
import os
from dotenv import load_dotenv

load_dotenv()

management = ManagementClient(ManagementClientOptions(
    user_pool_id=os.getenv('AUTHING_USERPOOL_ID'),
    secret=os.getenv('AUTHING_USERPOOL_SECRET'),
    host=os.getenv('AUTHING_SERVER')
))


def create_user():
    user = management.users.create(
        userInfo={
            'username': get_random_string(10),
            'password': get_random_string(10)
        }
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

    def test_create(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        self.assertTrue(user)
        self.assertTrue(user['id'])

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
        newUser = management.users.detail(userId=user['id'])
        self.assertTrue(user['id'] == newUser['id'])
        self.assertTrue(user['username'] == newUser['username'])

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

        newUser = management.users.detail(userId=user['id'])
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
        newUser = management.users.detail(userId=user['id'])
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
        self.assertTrue(status['id'] == user['id'])

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

        management.users.add_policies(
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
        management.users.remove_policies(
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
        management.users.set_udv(
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
        management.users.remove_udv(
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
        group = 'feifan'
        data = management.users.add_group(user['id'], group)
        self.assertTrue(data['code'] == 200)

    def test_remove_group(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        group = 'feifan'
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

    def test_list_authorized_resources(self):
        user = create_user()

        resources_list = management.users.list_authorized_resources(
            user_id=user["id"],
            namespace="default",
            resource_type="API"
        )

        print(resources_list)
