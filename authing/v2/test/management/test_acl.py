# coding: utf-8
from authing.v2.common.utils import get_random_string
import unittest
import os
from authing.v2.management.types import ManagementClientOptions
from authing.v2.management.authing import ManagementClient
from authing.v2.exceptions import AuthingException
from dotenv import load_dotenv

load_dotenv()

management = ManagementClient(ManagementClientOptions(
    user_pool_id=os.getenv('AUTHING_USERPOOL_ID'),
    secret=os.getenv('AUTHING_USERPOOL_SECRET'),
    host=os.getenv('AUTHING_SERVER'),
    enc_public_key="""-----BEGIN PUBLIC KEY-----
    MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDb+rq+GQ8L8hgi6sXph2Dqcih0
    4CfQt8Zm11GVhXh/0ad9uewFQIXMtytgdNfqFNiwSH5SQZSdA0AwDaYLG6Sc57L1
    DFuHxzHbMf9b8B2WnyJl3S85Qt6wmjBNfyy+dYlugFt04ZKDxsklXW5TVlGNA5Cg
    o/E0RlTdNza6FcAHeQIDAQAB
    -----END PUBLIC KEY-----"""
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
        resources = management.acl.list_resources(namespace=namespace.get('code').encode("utf-8"))
        self.assertTrue(resources.get('totalCount') == 1)
        self.assertTrue(len(resources.get('list')) == 1)

        resources = management.acl.list_resources(
            namespace=namespace.get('code').encode("utf-8"),
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
            namespace=namespace.get('code').encode("utf-8"),
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

    def test_revoke_resource(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        user2 = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        resource = get_random_string()
        management.acl.authorize_resource(
            namespace=default_namespace,
            resource=resource,
            opts=[
                {
                    'targetType': 'USER',
                    'targetIdentifier': user.get('id'),
                    'actions': [
                        get_random_string(),
                        get_random_string()
                    ]
                },
                {
                    'targetType': 'USER',
                    'targetIdentifier': user2.get('id'),
                    'actions': [
                        get_random_string(),
                        get_random_string()
                    ]
                }
            ]
        )
        management.acl.revoke_resource(
            namespace=default_namespace,
            resource=resource,
            opts=[
                {
                    'targetType': 'USER',
                    'targetIdentifier': user.get('id'),
                }
            ]
        )
        data1 = management.acl.list_authorized_resources(
            namespace=default_namespace,
            target_type='USER',
            target_identifier=user.get('id')
        )
        self.assertTrue(data1.get('totalCount') == 0)

        data2 = management.acl.list_authorized_resources(
            namespace=default_namespace,
            target_type='USER',
            target_identifier=user2.get('id')
        )
        self.assertTrue(data2.get('totalCount') == 1)

    def test_revoke_resource_2(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        user2 = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        resource = "%s:%s" % (get_random_string(), '1')
        management.acl.authorize_resource(
            namespace=default_namespace,
            resource=resource,
            opts=[
                {
                    'targetType': 'USER',
                    'targetIdentifier': user.get('id'),
                    'actions': [
                        get_random_string(),
                        get_random_string()
                    ]
                },
                {
                    'targetType': 'USER',
                    'targetIdentifier': user2.get('id'),
                    'actions': [
                        get_random_string(),
                        get_random_string()
                    ]
                }
            ]
        )
        management.acl.revoke_resource(
            namespace=default_namespace,
            resource=resource,
            opts=[
                {
                    'targetType': 'USER',
                    'targetIdentifier': user.get('id'),
                }
            ]
        )
        data1 = management.acl.list_authorized_resources(
            namespace=default_namespace,
            target_type='USER',
            target_identifier=user.get('id')
        )
        self.assertTrue(data1.get('totalCount') == 0)

        data2 = management.acl.list_authorized_resources(
            namespace=default_namespace,
            target_type='USER',
            target_identifier=user2.get('id')
        )
        self.assertTrue(data2.get('totalCount') == 1)

    def test_revoke_resource_3(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        user2 = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        resource_type = get_random_string()
        # 授权一个具体资源
        resource = "%s:%s" % (resource_type, '1')
        management.acl.authorize_resource(
            namespace=default_namespace,
            resource=resource,
            opts=[
                {
                    'targetType': 'USER',
                    'targetIdentifier': user.get('id'),
                    'actions': [
                        get_random_string(),
                        get_random_string()
                    ]
                },
                {
                    'targetType': 'USER',
                    'targetIdentifier': user2.get('id'),
                    'actions': [
                        get_random_string(),
                        get_random_string()
                    ]
                }
            ]
        )

        # 取消授权
        management.acl.revoke_resource(
            namespace=default_namespace,
            resource=resource_type,
            opts=[
                {
                    'targetType': 'USER',
                    'targetIdentifier': user.get('id'),
                }
            ]
        )
        data1 = management.acl.list_authorized_resources(
            namespace=default_namespace,
            target_type='USER',
            target_identifier=user.get('id')
        )
        self.assertTrue(data1.get('totalCount') == 0)

        data2 = management.acl.list_authorized_resources(
            namespace=default_namespace,
            target_type='USER',
            target_identifier=user2.get('id')
        )
        self.assertTrue(data2.get('totalCount') == 1)

    def test_revoke_resource_4(self):
        user = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        user2 = management.users.create(
            userInfo={
                'username': get_random_string(10),
                'password': get_random_string(10)
            }
        )
        resource_type = get_random_string()
        # 授权一类资源
        management.acl.authorize_resource(
            namespace=default_namespace,
            resource=resource_type,
            opts=[
                {
                    'targetType': 'USER',
                    'targetIdentifier': user.get('id'),
                    'actions': [
                        get_random_string(),
                        get_random_string()
                    ]
                },
                {
                    'targetType': 'USER',
                    'targetIdentifier': user2.get('id'),
                    'actions': [
                        get_random_string(),
                        get_random_string()
                    ]
                }
            ]
        )

        # 取消授权某一个具体资源
        resource = "%s:%s" % (resource_type, '1')
        management.acl.revoke_resource(
            namespace=default_namespace,
            resource=resource,
            opts=[
                {
                    'targetType': 'USER',
                    'targetIdentifier': user.get('id'),
                }
            ]
        )
        data1 = management.acl.list_authorized_resources(
            namespace=default_namespace,
            target_type='USER',
            target_identifier=user.get('id')
        )
        self.assertTrue(data1.get('totalCount') == 1)

        data2 = management.acl.list_authorized_resources(
            namespace=default_namespace,
            target_type='USER',
            target_identifier=user2.get('id')
        )
        self.assertTrue(data2.get('totalCount') == 1)


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

    def test_get_authorized_targets(self):
        data = management.acl.get_authorized_targets(namespace="mvcbbdutsn", resource_type="DATA", resource="test",target_type="GROUP")
        print (data)

    def test_programmatic_access_account_list(self):
        result = management.acl.programmatic_access_account_list("6139c4d24e78a4d706b7545b")
        self.assertEquals(result['message'], '获取编程访问账号列表成功')

    def test_create_programmatic_access_account(self):
        result = management.acl.create_programmatic_access_account(app_id='6139c4d24e78a4d706b7545b', remark='xx')
        self.assertEquals(result['code'], 200)

    def test_disable_programmatic_access_account(self):
        result = management.acl.disable_programmatic_access_account("61418fad9d4357a5308e5ecd")
        self.assertFalse(result['data']['enabled'])

    def test_delete_programmatic_access_account(self):
        result = management.acl.delete_programmatic_access_account('61418fad9d4357a5308e5ecd')
        self.assertEquals(result['code'], 200)

    def test_enable_programmatic_access_account(self):
        account = management.acl.create_programmatic_access_account(app_id='6139c4d24e78a4d706b7545b', remark='xx')
        result = management.acl.enable_programmatic_access_account(account['data']['id'])
        self.assertTrue(result['data']['enabled'])

    def test_refresh_programmatic_access_account_secret(self):
        account = management.acl.create_programmatic_access_account(app_id='6139c4d24e78a4d706b7545b', remark='xx')
        result = management.acl.refresh_programmatic_access_account_secret(account['data']['id'])
        self.assertNotEqual(account['data']['secret'], result['data']['secret'])

    def test_get_resource_by_id(self):
        result = management.acl.get_resource_by_id('6141a1bc2129d0b83415227f')
        self.assertEquals(result['data']['id'], '6141a1bc2129d0b83415227f')

    def test_get_resource_by_code(self):
        result = management.acl.get_resource_by_code(namespace='gvymeeehxt', code='eyqcalgaeo')
        self.assertEquals(result['data']['id'], '6141a1bc2129d0b83415227f')

    def test_enable_application_access_policies(self):
        result = management.acl.enable_application_access_policies(namespace='61360547f4807f63584fa152',
                                                                   app_id='61360547f4807f63584fa152',
                                                                   inherit_by_children=False,
                                                                   target_type='USER',
                                                                   target_identifiers=[
                                                                       '613ad7081436dc0f42d8ee65'
                                                                   ])
        self.assertEquals(result['code'], 200)

    def test_disable_application_access_policies(self):
        result = management.acl.disable_application_access_policies(namespace='gvymeeehxt',
                                                                    app_id='6139c4d24e78a4d706b7545b',
                                                                    inherit_by_children=False,
                                                                    target_type='USER',
                                                                    target_identifiers=[
                                                                       '613eb8b33cd935afe7470c88'
                                                                    ])
        self.assertEquals(result['code'], 200)

    def test_delete_application_access_policies(self):
        result = management.acl.disable_application_access_policies(namespace='gvymeeehxt',
                                                                    app_id='6139c4d24e78a4d706b7545b',
                                                                    inherit_by_children=False,
                                                                    target_type='USER',
                                                                    target_identifiers=[
                                                                        '613eb8b33cd935afe7470c88'
                                                                    ])
        self.assertEquals(result['code'], 200)

    def test_allow_access_application(self):
        result = management.acl.allow_access_application(namespace='gvymeeehxt',
                                                         app_id='6139c4d24e78a4d706b7545b',
                                                         inherit_by_children=False,
                                                         target_type='USER',
                                                         target_identifiers=[
                                                                        '613eb8b33cd935afe7470c88'
                                                                    ])
        self.assertEquals(result['code'], 200)

    def test_deny_access_application(self):
        result = management.acl.deny_access_application(namespace='gvymeeehxt',
                                                        app_id='6139c4d24e78a4d706b7545b',
                                                        inherit_by_children=False,
                                                        target_type='USER',
                                                        target_identifiers=[
                                                                        '613eb8b33cd935afe7470c88'
                                                                    ])
        self.assertEquals(result['code'], 200)

    def test_update_default_application_access_policy(self):
        result = management.acl.update_default_application_access_policy( app_id='6139c4d24e78a4d706b7545b',
                                                                          default_strategy='ALLOW_ALL')
        self.assertEquals(result['code'], 200)

