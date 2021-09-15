# coding: utf-8

from authing.v2.exceptions import AuthingException
from authing.v2.test.utils import get_random_string
from authing.v2.authentication import AuthenticationClientOptions
from authing.v2.authentication.authing import AuthenticationClient
from authing.v2.management.types import ManagementClientOptions
from authing.v2.management.authing import ManagementClient
from authing.v2.test.test_common import TestHelper
import json
import unittest
import os
from datetime import datetime
from dotenv import load_dotenv

from urlparse import urlparse,parse_qs

# from urllib.parse import urlparse, parse_qs



class TestAuthenticationByEmail(unittest.TestCase):
    """授权邮箱相关方法"""
    authentication = None;

    @classmethod
    def setUpClass(cls):
        load_dotenv()

    def setUp(self):
        self.authentication = TestHelper().init_authentication_client();

    def test_register_by_email(self):
        email = "%s@authing.cn" % get_random_string(10)
        password = get_random_string(10)
        user = self.authentication.register_by_email(
            email=email,
            password=password,
        )
        self.assertTrue(user)
        self.assertTrue(user["id"])
        self.assertTrue(user["email"] == email)

    def test_register_by_email_with_profile(self):

        email = "%s@authing.cn" % get_random_string(10)
        password = get_random_string(10)
        user = self.authentication.register_by_email(
            email=email,
            password=password,
            profile={"nickname": "Nick"},
            generate_token=True,
        )
        self.assertTrue(user)
        self.assertTrue(user["id"])
        self.assertTrue(user["email"] == email)
        self.assertTrue(user["token"] is not None)

    def test_register_by_email_with_custom_data(self):

        email = "%s@authing.cn" % get_random_string(10)
        password = get_random_string(10)
        user = self.authentication.register_by_email(
            email=email,
            password=password,
            custom_data={
                'school': '华中科技大学',
                'age': 22
            },
            force_login=True
        )
        self.assertTrue(user['id'])
        udvs = self.authentication.get_udf_value()
        self.assertTrue(udvs['school'], '华中科技大学')
        self.assertTrue(udvs['age'], 22)

    def test_register_by_email_with_context(self):

        email = "%s@authing.cn" % get_random_string(10)
        password = get_random_string(10)
        user = self.authentication.register_by_email(
            email=email,
            password=password,
            context={
                'source': 'google'
            }
        )
        self.assertTrue(user['id'])

    def test_login_by_email(self):

        email = "%s@authing.cn" % get_random_string(10)
        password = get_random_string(10)
        user = self.authentication.register_by_email(
            email=email,
            password=password,
        )
        user = self.authentication.login_by_email(
            email=email,
            password=password,
        )
        self.assertTrue(user)
        self.assertTrue(user.get("token"))
        self.assertTrue(user.get("email") == email)

    def test_login_by_email_with_custom_data(self):

        email = "%s@authing.cn" % get_random_string(10)
        password = get_random_string(10)
        user = self.authentication.register_by_email(
            email=email,
            password=password,
        )
        user = self.authentication.login_by_email(
            email=email,
            password=password,
            custom_data={
                'school': '华中科技大学',
                'age': 22
            }
        )
        self.assertTrue(user['id'])
        udvs = self.authentication.get_udf_value()
        self.assertTrue(udvs['school'], '华中科技大学')
        self.assertTrue(udvs['age'], 22)

    def test_login_by_email_with_context(self):

        email = "%s@authing.cn" % get_random_string(10)
        password = get_random_string(10)
        user = self.authentication.register_by_email(
            email=email,
            password=password,
        )
        user = self.authentication.login_by_email(
            email=email,
            password=password,
            context={
                'source': 'google'
            }
        )
        self.assertTrue(user['id'])

    def test_send_email(self):
        email = "email"
        authentication = TestHelper().init_authentication_client()
        res = authentication.send_email(email, 'RESET_PASSWORD')
        code, message = res['code'], res['message']
        self.assertTrue(code == 200)

    def test_reset_password_by_email_code(self):

        # email = "%s@authing.cn" % get_random_string(10)
        email = "email"
        new_password = 'passw0rd'
        self.authentication.reset_password_by_email_code(email, '8668', new_password)
        user = self.authentication.login_by_email(email, new_password)
        self.assertTrue(user['id'])

    @unittest.skip("dynamic email code")
    def test_send_email_bind(self):
        email = "old email"
        authentication = TestHelper().init_authentication_client()
        authentication.send_email(email, 'CHANGE_EMAIL')
        email = "new email"
        res = authentication.send_email(email, 'CHANGE_EMAIL')
        code, message = res['code'], res['message']
        self.assertTrue(code == 200)

    @unittest.skip("dynamic email code")
    def test_bind_email(self):
        newEmail = "new email"
        password = 'password'
        self.authentication.login_by_username(username="username",password=password)
        res = self.authentication.bind_email(email=newEmail,email_code="5904")
        self.assertTrue(res['email'] == newEmail)

    def test_unbing_email(self):
        self.authentication.login_by_username(username="username",password="password")
        self.authentication.unbind_email()
        user = self.authentication.get_current_user()
        self.assertIsNone(user['email'])

    @unittest.skip("dynamic email code")
    def test_update_email(self):
        email = "xsjzviiiwf@authing.cn"
        password = 'password'
        self.authentication.login_by_username(username="username", password=password)
        self.authentication.update_email(email_code="4894",email="new email",old_email="old email", old_email_code="6264")
