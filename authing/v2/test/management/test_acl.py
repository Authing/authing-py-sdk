from ...common.utils import get_random_string
import unittest
import os
from ...management.types import ManagementClientOptions
from ...management.authing import ManagementClient
from ...exceptions import AuthingException
from dotenv import load_dotenv

load_dotenv()

management = ManagementClient(ManagementClientOptions(
    user_pool_id=os.getenv('AUTHING_USERPOOL_ID'),
    secret=os.getenv('AUTHING_USERPOOL_SECRET'),
    host=os.getenv('AUTHING_SERVER')
))

default_namespace = 'default'


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
                user_id=user['id'],
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
            user_id=user['id'],
            namespace=default_namespace
        )
        is_allowed = management.acl.is_allowed(
            user_id=user['id'],
            action='books:edit',
            resource='books:123',
            namespace=default_namespace
        )
        self.assertTrue(is_allowed)
        is_allowed = management.acl.is_allowed(
            user_id=user['id'],
            action='books:delete',
            resource='books:123',
            namespace=default_namespace
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
            user_id=user['id'],
            namespace=default_namespace
        )
        is_allowed = management.acl.is_allowed(
            user_id=user['id'],
            action='books:edit',
            resource='books:123',
            namespace=default_namespace
        )
        self.assertTrue(is_allowed)
        is_allowed = management.acl.is_allowed(
            user_id=user['id'],
            action='books:delete',
            resource='books:123',
            namespace=default_namespace
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
            user_id=user['id'],
            namespace=default_namespace
        )
        is_allowed = management.acl.is_allowed(
            user_id=user['id'],
            action='books:edit',
            resource='books:123',
            namespace=default_namespace
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
            user_id=user['id'],
            namespace=default_namespace
        )
        is_allowed = management.acl.is_allowed(
            user_id=user['id'],
            action='edit',
            resource='books:123',
            namespace=default_namespace
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
            role=role['code'],
            namespace=default_namespace
        )
        is_allowed = management.acl.is_allowed(
            user_id=user['id'],
            resource='books:*',
            action='books:edit',
            namespace=default_namespace
        )
        self.assertTrue(is_allowed)

    def test_create_namespace(self):
        code = get_random_string()
        name = get_random_string()
        namespace = management.acl.create_namespace(code, name)
        self.assertTrue(namespace)
        self.assertTrue(namespace.get('id'))
        self.assertTrue(namespace.get('code') == code)
        self.assertTrue(namespace.get('name') == name)

    def test_update_namespace_not_exists(self):
        try:
            management.acl.update_namespace(0, name=get_random_string())
            self.fail()
        except AuthingException as e:
            self.assertTrue(e.code == 3005)

    def test_update_namespace(self):
        code = get_random_string()
        name = get_random_string()
        namespace = management.acl.create_namespace(code, name)
        id = namespace.get('id')

        new_name = get_random_string()
        namespace = management.acl.update_namespace(id, name=new_name)
        self.assertTrue(namespace.get('name') == new_name)

    def test_list_namespaces(self):
        data = management.acl.list_namespaces()
        total, list = data.get('total'), data.get('list')
        self.assertTrue(total)
        self.assertTrue(len(list))

    def test_delete_namespace_not_exists(self):
        try:
            id = 0
            management.acl.delete_namespace(id)
            self.fail()
        except AuthingException as e:
            self.assertTrue(e.code == 3003)

    def test_delete_namespace(self):
        code = get_random_string()
        name = get_random_string()
        namespace = management.acl.create_namespace(code, name)
        id = namespace.get('id')

        success = management.acl.delete_namespace(id)
        self.assertTrue(success)

    def test_create_resource(self):
        code = get_random_string()
        name = get_random_string()
        namespace = management.acl.create_namespace(code, name)
        resource = management.acl.create_resource(
            code=code,
            resource_type='DATA',
            actions=[
                {
                    'name': get_random_string(),
                    'description': get_random_string()
                }
            ],
            namespace=namespace.get('code')
        )
        self.assertTrue(resource)

    def test_update_resource(self):
        code = get_random_string()
        name = get_random_string()
        namespace = management.acl.create_namespace(code, name)
        resource = management.acl.create_resource(
            code=code,
            resource_type='DATA',
            actions=[
                {
                    'name': get_random_string(),
                    'description': get_random_string()
                }
            ],
            namespace=namespace.get('code')
        )

        new_description = get_random_string()
        new_actions = [
            {
                'name': 'name',
                'description': 'description'
            }
        ]
        resource = management.acl.update_resource(
            namespace=namespace.get('code'),
            code=code,
            description=new_description,
            actions=new_actions
        )
        self.assertTrue(resource.get('description') == new_description)
        actions = resource.get('actions')
        self.assertTrue(isinstance(actions, list))
        self.assertTrue(actions[0]['name'] == 'name')
        self.assertTrue(actions[0]['description'] == 'description')

    def test_list_resources(self):
        code = get_random_string()
        name = get_random_string()
        namespace = management.acl.create_namespace(code, name)
        management.acl.create_resource(
            code=get_random_string(),
            resource_type='DATA',
            actions=[
                {
                    'name': get_random_string(),
                    'description': get_random_string()
                }
            ],
            namespace=namespace.get('code')
        )
        resources = management.acl.list_resources(namespace=namespace.get('code'))
        self.assertTrue(resources.get('totalCount') == 1)
        self.assertTrue(len(resources.get('list')) == 1)

        resources = management.acl.list_resources(
            namespace=namespace.get('code'),
            resource_type='MENU'
        )
        self.assertTrue(resources.get('totalCount') == 0)
        self.assertTrue(len(resources.get('list')) == 0)

    def test_delete_resource(self):
        code = get_random_string()
        name = get_random_string()
        namespace = management.acl.create_namespace(code, name)

        resource_code = get_random_string()
        management.acl.create_resource(
            code=resource_code,
            resource_type='DATA',
            actions=[
                {
                    'name': get_random_string(),
                    'description': get_random_string()
                }
            ],
            namespace=namespace.get('code')
        )
        success = management.acl.delete_resource(
            namespace=namespace.get('code'),
            code=resource_code
        )
        self.assertTrue(success)

    def test_authorize_resource(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )

        success = management.acl.authorize_resource(
            namespace=default_namespace,
            resource=get_random_string(),
            opts=[
                {
                    'targetType': 'USER',
                    'targetIdentifier': user.get('id'),
                    'actions': [
                        get_random_string(),
                        get_random_string()
                    ]
                }
            ]
        )

        self.assertTrue(success)
        data = management.acl.list_authorized_resources(
            namespace=default_namespace,
            target_type='USER',
            target_identifier=user.get('id')
        )
        self.assertTrue(data.get('totalCount') == 1)


    def test_list_authorized_resources(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        management.acl.allow(
            resource='books:123',
            action='books:edit',
            user_id=user['id'],
            namespace=default_namespace
        )

        data = management.acl.list_authorized_resources(
            namespace=default_namespace,
            target_type='USER',
            target_identifier=user.get('id')
        )

        self.assertTrue(data.get('totalCount') == 1)

