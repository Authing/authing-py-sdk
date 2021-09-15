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



phone = "18515006338"
password = "password"
class TestAuthenticationByPhone(unittest.TestCase):
    """授权邮箱相关方法"""
    authentication = None;

    @classmethod
    def setUpClass(cls):
        load_dotenv()

    def setUp(self):
        self.authentication = TestHelper().init_authentication_client();

    def test_send_sms_code(self):
        self.authentication.send_sms_code(phone)

    def test_register_by_phone(self):
        user = self.authentication.register_by_phone_code(
            phone=phone,
            password=password,
            code="code",
        )
        self.assertTrue(user)
        self.assertTrue(user["id"])
        self.assertTrue(user["phone"] == phone)

    def test_register_by_phone_with_profile(self):

        user = self.authentication.register_by_phone_code(
            phone=phone,
            code="code",
            password=password,
            profile={"nickname": "Nick"},
            generate_token=True,
        )
        self.assertTrue(user)
        self.assertTrue(user["id"])
        self.assertTrue(user["phone"] == phone)
        self.assertTrue(user["token"] is not None)

    def test_register_by_phone_with_custom_data(self):

        password = get_random_string(10)
        user = self.authentication.register_by_phone_code(
            phone=phone,
            password=password,
            custom_data={
                'school': '华中科技大学',
                'age': 22
            },
            code="code",
            force_login=True
        )
        self.assertTrue(user['id'])
        udvs = self.authentication.get_udf_value()
        self.assertTrue(udvs['school'], '华中科技大学')
        self.assertTrue(udvs['age'], 22)

    @unittest.skip("dynamic phone code")
    def test_login_by_phone(self):

        user = self.authentication.register_by_phone_code(
            phone=phone,
            password=password,
            code="code"
        )
        user = self.authentication.login_by_phone_password(
            phone=phone,
            password=password,
        )
        self.assertTrue(user)
        self.assertTrue(user.get("token"))
        self.assertTrue(user.get("phone") == phone)

    @unittest.skip("dynamic phone code")
    def test_login_by_phone_code(self):

        user = self.authentication.login_by_phone_code(phone=phone,code="code")
        self.assertTrue(user)
        self.assertTrue(user.get("token"))
        self.assertTrue(user.get("phone") == phone)

    @unittest.skip("dynamic phone code")
    def test_reset_password_by_phone_code(self):
        new_password = 'password'
        self.authentication.reset_password_by_phone_code(phone, '5975', new_password)
        user = self.authentication.login_by_phone_password(phone, new_password)
        self.assertTrue(user['id'])

    def test_set_custom_data(self):
        self.authentication.login_by_phone_password(phone,"password")
        res = self.authentication.set_udf_value({
            'school': '华中科技大学',
            'age': 22
        })
        self.assertTrue(res)

    def test_update_phone_before(self):
        self.authentication.send_sms_code(phone)

    @unittest.skip("dynamic phone code")
    def test_update_phone(self):
        newPhone = "phone"
        user = self.authentication.login_by_phone_password(phone=phone, password=password)
        id = user['id']
        self.authentication.update_phone(phone=newPhone, phone_code="2778", old_phone=phone, old_phone_code="9138")
        self.authentication.logout()
        user = self.authentication.login_by_phone_password(phone=newPhone, password=password)
        self.assertEqual(id, user['id'])

    def test_unbind_phone(self):
        user = self.authentication.login_by_phone_password(phone=phone, password=password)
        self.authentication.unbind_phone()
        user = self.authentication.get_current_user()
        self.assertIsNone(user['phone'])

    @unittest.skip("dynamic phone code")
    def test_bind_phone(self):
        self.authentication.login_by_email("testMail", password=password)
        self.authentication.bind_phone(phone=phone, phone_code="7884")
        user = self.authentication.get_current_user()
        self.assertEqual(user['phone'], phone)

    def test_bind_link(self):
        user = self.authentication.login_by_phone_password(phone=phone, password=password)
        res = self.authentication.link_account(user['token'],'vxzzz')
        print (res)
        self.assertTrue(res)