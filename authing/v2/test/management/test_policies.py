from ...common.utils import get_random_string
import unittest
import os
from ...management.types import ManagementClientOptions
from ...management.authing import ManagementClient
from dotenv import load_dotenv
from deepdiff import DeepDiff
load_dotenv()


management = ManagementClient(ManagementClientOptions(
    user_pool_id=os.getenv('AUTHING_USERPOOL_ID'),
    secret=os.getenv('AUTHING_USERPOOL_SECRET'),
    host=os.getenv('AUTHING_SERVER')
))


class TestPolicies(unittest.TestCase):
    def test_list(self):
        data = management.policies.list()
        totalCount, _list = data['totalCount'], data['list']
        self.assertTrue(totalCount != None)
        self.assertTrue(_list != None)

    def test_create(self):
        code = get_random_string(10)
        statements = [
            {
                'resource': 'book:123',
                'actions': ['books:read'],
                'effect': 'ALLOW'
            }
        ]
        policy = management.policies.create(
            code=code,
            statements=statements
        )
        self.assertTrue(DeepDiff(statements, policy['statements']))

    def test_detail(self):
        code = get_random_string(10)
        statements = [
            {
                'resource': 'book:123',
                'actions': ['books:read'],
                'effect': 'ALLOW'
            }
        ]
        management.policies.create(
            code=code,
            statements=statements
        )
        policy = management.policies.detail(code)
        self.assertTrue(DeepDiff(statements, policy['statements']))

    def test_update(self):
        code = get_random_string(10)
        statements = [
            {
                'resource': 'book:123',
                'actions': ['books:read'],
                'effect': 'ALLOW'
            }
        ]
        policy = management.policies.create(
            code=code,
            statements=statements
        )
        self.assertTrue(DeepDiff(statements, policy['statements']))
        newStatements = [
            {
                'resource': 'book:123',
                'actions': ['books:read', 'books:update'],
                'effect': 'ALLOW'
            }
        ]
        policy = management.policies.update(
            code=code,
            statements=newStatements
        )
        self.assertTrue(DeepDiff(newStatements, policy['statements']))

    def test_delete(self):
        code = get_random_string(10)
        statements = [
            {
                'resource': 'book:123',
                'actions': ['books:read'],
                'effect': 'ALLOW'
            }
        ]
        policy = management.policies.create(
            code=code,
            statements=statements
        )
        management.policies.delete(policy['code'])
        policy = management.policies.detail(code)
        self.assertTrue(policy == None)

    def test_delete_many(self):
        code = get_random_string(10)
        statements = [
            {
                'resource': 'book:123',
                'actions': ['books:read'],
                'effect': 'ALLOW'
            }
        ]
        policy = management.policies.create(
            code=code,
            statements=statements
        )
        management.policies.delete_many([policy['code']])
        policy = management.policies.detail(code)
        self.assertTrue(policy == None)

    def test_add_assignments_to_user(self):
        code = get_random_string(10)
        statements = [
            {
                'resource': 'book:123',
                'actions': ['books:read'],
                'effect': 'ALLOW'
            }
        ]
        policy = management.policies.create(
            code=code,
            statements=statements
        )
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )

        management.policies.add_assignments(
            policies=[policy['code']],
            targetType='USER',
            targetIdentifiers=[user['id']]
        )

        data = management.policies.list_assignments(
            code=policy['code']
        )
        totalCount = data['totalCount']
        self.assertTrue(totalCount == 1)

    def test_add_assignments_to_role(self):
        code = get_random_string(10)
        statements = [
            {
                'resource': 'book:123',
                'actions': ['books:read'],
                'effect': 'ALLOW'
            }
        ]
        policy = management.policies.create(
            code=code,
            statements=statements
        )
        role = management.roles.create(code=get_random_string(10))

        management.policies.add_assignments(
            policies=[policy['code']],
            targetType='ROLE',
            targetIdentifiers=[role['code']]
        )
        data = management.policies.list_assignments(
            code=policy['code']
        )
        totalCount = data['totalCount']
        self.assertTrue(totalCount == 1)

    def test_remove_assignments(self):
        code = get_random_string(10)
        statements = [
            {
                'resource': 'book:123',
                'actions': ['books:read'],
                'effect': 'ALLOW'
            }
        ]
        policy = management.policies.create(
            code=code,
            statements=statements
        )
        role = management.roles.create(code=get_random_string(10))

        management.policies.add_assignments(
            policies=[policy['code']],
            targetType='ROLE',
            targetIdentifiers=[role['code']]
        )
        management.policies.remove_assignments(
            policies=[policy['code']],
            targetType='ROLE',
            targetIdentifiers=[role['code']]
        )
        data = management.policies.list_assignments(
            code=policy['code']
        )
        totalCount = data['totalCount']
        self.assertTrue(totalCount == 0)

    def test_enable_assignments(self):
        code = get_random_string(10)
        statements = [
            {
                'resource': 'book:123',
                'actions': ['books:read'],
                'effect': 'ALLOW'
            }
        ]
        policy = management.policies.create(
            code=code,
            statements=statements
        )
        role = management.roles.create(code=get_random_string(10))

        management.policies.add_assignments(
            policies=[policy['code']],
            targetType='ROLE',
            targetIdentifiers=[role['code']]
        )
        res = management.policies.enable_assignment(code, target_type='ROLE', target_identifier=role['id'])
        print res

    def test_disable_assignments(self):
        code = get_random_string(10)
        statements = [
            {
                'resource': 'book:123',
                'actions': ['books:read'],
                'effect': 'ALLOW'
            }
        ]
        policy = management.policies.create(
            code=code,
            statements=statements
        )
        role = management.roles.create(code=get_random_string(10))

        management.policies.add_assignments(
            policies=[policy['code']],
            targetType='ROLE',
            targetIdentifiers=[role['code']]
        )
        res = management.policies.enable_assignment(code, target_type='ROLE', target_identifier=role['id'])
        res = management.policies.disable_assignment(code, target_type='ROLE',
                                                    target_identifier=role['id'])
        print res
        self.assertEquals(res['code'],200)
