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



class TestMfaAuthentication(unittest.TestCase):
    """授权邮箱相关方法"""
    authentication = None;

    @classmethod
    def setUpClass(cls):
        load_dotenv()

    def setUp(self):
        self.authentication = TestHelper().init_authentication_client();

    def test_get_mfa_authenticators(self):
        tt=self.authentication.login_by_email("fptvmzqyxn@authing.cn","12345678")
        res = self.authentication.get_mfa_authenticators(mfa_token=tt['token'])
        self.assertEquals(res['code'], 200)

    def test_assosicate_mfa_authenticator(self):
        tt = self.authentication.login_by_email("fptvmzqyxn@authing.cn", "12345678")
        res = self.authentication.assosicate_mfa_authenticator(tt['token'])
        self.assertEquals(res['code'], 200)

    def test_delete_mfa_authenticator(self):
        tt = self.authentication.login_by_email("fptvmzqyxn@authing.cn", "12345678")
        res = self.authentication.delete_mfa_authenticator()
        self.assertEquals(res['code'], 200)

    def test_confirm_assosicate_mfa_authenticator(self):
        tt = self.authentication.login_by_email("fptvmzqyxn@authing.cn", "12345678")
        res = self.authentication.confirm_assosicate_mfa_authenticator(tt['token'])
        self.assertEquals(res['code'], 200)

    def test_verify_totp_mfa(self):
        user = self.authentication.login_by_phone_password("18515006338", "123456")
        res = self.authentication.verify_totp_mfa("",user['token'])
        print res

    def test_verify_app_sms_mfa(self):
        user = self.authentication.login_by_phone_password("18515006338", "123456")
        res = self.authentication.verify_app_sms_mfa("18515006338","11",user['token'])

    def test_verify_app_email_mfa(self):
        user = self.authentication.login_by_email("fptvmzqyxn@authing.cn", "12345678")
        res = self.authentication.verify_app_email_mfa("fptvmzqyxn@authing.cn", "11", user['token'])

    def test_phone_or_email_bindable(self):
        user = self.authentication.login_by_email("fptvmzqyxn@authing.cn", "12345678")
        res=self.authentication.phone_or_email_bindable(mfa_token=user['token'],email="fptvmzqyxn@authing.cn")
        self.assertNotEqual(res['code'],200)

    def test_verify_totp_recovery_code(self):
        user = self.authentication.login_by_email("fptvmzqyxn@authing.cn", "12345678")
        res = self.authentication.verify_totp_recovery_code(mfa_token=user['token'], recovery_code="fptvmzqyxn@authing.cn")
        self.assertNotEqual(res['code'], 200)

    def test_associate_face_by_url(self):
        user = self.authentication.login_by_email("fptvmzqyxn@authing.cn", "12345678")
        res = self.authentication.associate_face_by_url(mfa_token=user['token'],
                                                            base_face="fptvmzqyxn@authing.cn",compare_face="url")
        self.assertNotEqual(res['code'], 200)

    def test_verify_face_mfa(self):
        user = self.authentication.login_by_email("fptvmzqyxn@authing.cn", "12345678")
        res = self.authentication.verify_face_mfa(mfa_token=user['token'],
                                                        photo="fptvmzqyxn@authing.cn")
        self.assertNotEqual(res['code'], 200)
