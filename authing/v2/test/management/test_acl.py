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


class TestAcl(unittest.TestCase):

    def test_allow_check_input(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        failed = False
        try:
            management.acl.allow(
                resource='books',  # resource 必须为 resourceType:resourceId 格式
                action='books:edit',
                userId=user['id'],
            )
        except:
            failed = True

        self.assertTrue(failed)

    def test_allow_by_user(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        management.acl.allow(
            resource='books:123',
            action='books:edit',
            userId=user['id'],
        )
        is_allowed = management.acl.is_allowed(
            userId=user['id'],
            action='books:edit',
            resource='books:123'
        )
        self.assertTrue(is_allowed)
        is_allowed = management.acl.is_allowed(
            userId=user['id'],
            action='books:delete',
            resource='books:123'
        )
        self.assertFalse(is_allowed)

    def test_allow_by_user_with_action_wildcard(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        management.acl.allow(
            resource='books:123',
            action='books:*',
            userId=user['id'],
        )
        is_allowed = management.acl.is_allowed(
            userId=user['id'],
            action='books:edit',
            resource='books:123'
        )
        self.assertTrue(is_allowed)
        is_allowed = management.acl.is_allowed(
            userId=user['id'],
            action='books:delete',
            resource='books:123'
        )
        self.assertTrue(is_allowed)

    def test_allow_by_user_with_resource_wildcard(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        management.acl.allow(
            resource='books:*',
            action='books:edit',
            userId=user['id'],
        )
        is_allowed = management.acl.is_allowed(
            userId=user['id'],
            action='books:edit',
            resource='books:123'
        )
        self.assertTrue(is_allowed)

    def test_allow_by_user_with_resource_wildcard_2(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        management.acl.allow(
            resource='books:*',
            action='edit',
            userId=user['id'],
        )
        is_allowed = management.acl.is_allowed(
            userId=user['id'],
            action='edit',
            resource='books:123'
        )
        self.assertTrue(is_allowed)

    def test_allow_by_role(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        role = management.roles.create(
            code=get_random_string(10)
        )
        management.roles.add_users(role['code'], [user['id']])
        management.acl.allow(
            resource='books:*',
            action='books:edit',
            role=role['code']
        )
        is_allowed = management.acl.is_allowed(
            userId=user['id'],
            resource='books:*',
            action='books:edit',
        )
        self.assertTrue(is_allowed)
