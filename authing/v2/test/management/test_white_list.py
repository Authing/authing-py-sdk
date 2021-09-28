import os
import unittest
from dotenv import load_dotenv

from authing.v2.management import ManagementClient, ManagementClientOptions
from authing.v2.test.utils import get_random_string


default_namespace = 'default'


class TestWhiteList(unittest.TestCase):

    management = None

    def setUp(self):
        self.management = ManagementClient(ManagementClientOptions(
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

    def test_list(self):
        res = self.management.whiteList.list("USERNAME")
        self.assertEquals(res, [])

    def test_add(self):
        result = self.management.whiteList.add("USERNAME", ["xx2x1"])
        self.assertTrue(isinstance(result, list))

    def test_remove(self):
        result = self.management.whiteList.remove("USERNAME",["xx"])
        self.assertTrue(isinstance(result, list))

    def test_enable_white_list(self):
        res = self.management.whiteList.enable_white_list("USERNAME")
        self.assertEquals(res['whitelist']['usernameEnabled'], True)

    def test_disable_white_list(self):
        res = self.management.whiteList.disable_white_list("USERNAME")
        self.assertEquals(res['whitelist']['usernameEnabled'], False)

