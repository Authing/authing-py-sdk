import os
import unittest
from dotenv import load_dotenv

from authing.v2.management import ManagementClient, ManagementClientOptions
from authing.v2.test.utils import get_random_string


default_namespace = 'default'


class TestUserPool(unittest.TestCase):

    management = None

    def setUp(self) :
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

    def test_list_env(self):
        self.management.userPool.add_env("tt","xx")
        res = self.management.userPool.list_env()
        self.assertEquals(dict.get(res[u'data'][0],"key"),"tt")

    def test_add_env(self):
        result = self.management.userPool.add_env("tct", "xx")
        self.assertEquals(result['code'], 200)

    def test_remove_env(self):
        result = self.management.userPool.remove_env("tt")
        self.assertEquals(result['code'], 200)

    def test_details(self):
        result = self.management.userPool.detail()
        self.assertIsNotNone(result['data'])

    def test_update(self):
        result = self.management.userPool.update(updates={
            "name": "newSDK",
            "whitelist": {
                "phoneEnabled":True
            }
        })
        self.assertEquals(True,result['whitelist']["phoneEnabled"])
