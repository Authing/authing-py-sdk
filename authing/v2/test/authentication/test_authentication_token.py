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

class TestAuthenticationToken(unittest.TestCase):
    """授权邮箱相关方法"""
    authentication = None;

    @classmethod
    def setUpClass(cls):
        load_dotenv()

    def setUp(self):
        self.authentication = TestHelper().init_authentication_client();

    def test_refresh_token(self):
        email = "%s@authing.cn" % get_random_string(10)
        password = get_random_string(10)
        user = self.authentication.register_by_email(
            email=email,
            password=password,
        )
        user = self.authentication.login_by_email(email,password)
        res = self.authentication.refresh_token()
        self.assertTrue(res)