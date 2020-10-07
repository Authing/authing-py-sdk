from ...common.utils import get_random_string
import unittest
import os
from ...management import ManagementClientOptions
from ...management.authing import ManagementClient
from dotenv import load_dotenv
load_dotenv()


management = ManagementClient(ManagementClientOptions(
    user_pool_id=os.getenv('AUTHING_USERPOOL_ID'),
    secret=os.getenv('AUTHING_USERPOOL_SECRET'),
    host=os.getenv('AUTHING_SERVER')
))


def createRole():
    code = get_random_string(5)
    role = management.roles.create(code=code)
    return role


class TestRoles(unittest.TestCase):
    def test_list(self):
        totalCount, _list = management.roles.list()
        self.assertTrue(totalCount)
        self.assertTrue(_list)

    def test_create(self):
        role = createRole()
        self.assertTrue(role)
        self.assertTrue(role['code'])

    def test_detail(self):
        code = get_random_string(5)
        management.roles.create(code=code)
        role = management.roles.detail(code=code)
        self.assertTrue(role)
        self.assertTrue(role['code'] == code)

    def test_update(self):
        code = get_random_string(5)
        management.roles.create(code=code)
        desc = get_random_string(10)
        role = management.roles.update(code=code, description=desc)
        self.assertTrue(role['description'] == desc)

    def test_update_with_new_code(self):
        code = get_random_string(5)
        management.roles.create(code=code)

        newCode = get_random_string(5)
        role = management.roles.update(code=code, newCode=newCode)
        self.assertTrue(role['code'] == newCode)

    def test_delete(self):
        role = management.roles.create(
            code=get_random_string(5)
        )
        status_code, message = management.roles.delete(code=role['code'])
        self.assertTrue(status_code == 200)

        newRole = management.roles.detail(code=role['code'])
        self.assertTrue(newRole == None)

    def test_list_users(self):
        role = management.roles.create(
            code=get_random_string(5)
        )
        totalCount, users = management.roles.list_users(role['code'])
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
        totalCount, users = management.roles.list_users(role['code'])
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
        totalCount, users = management.roles.list_users(role['code'])
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
        role = createRole()
        management.roles.add_policies(role['code'], [policy['code']])
        totalCount, _list = management.roles.list_policies(role['code'])
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
        role = createRole()
        management.roles.add_policies(role['code'], [policy['code']])
        management.roles.remove_policies(role['code'], [policy['code']])
        totalCount, _list = management.roles.list_policies(role['code'])
        self.assertTrue(totalCount == 0)
