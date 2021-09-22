import os
import unittest
from dotenv import load_dotenv

from authing.v2.management import ManagementClient, ManagementClientOptions
from authing.v2.test.utils import get_random_string


default_namespace = 'default'


class TestManagementAuthing(unittest.TestCase):

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

    def test_send_mail(self):
        res = self.management.send_email(scene='CHANGE_EMAIL',email='530495062@qq.com')
        print (res)

    def test_is_password_valid(self):
        res = self.management.is_password_valid("123456")
        print (res)

