import os
import unittest
from dotenv import load_dotenv

from authing.v2.management import ManagementClient, ManagementClientOptions
from authing.v2.test.utils import get_random_string


default_namespace = 'default'


class TestAuditLog(unittest.TestCase):

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

    def test_list_env(self):
        res = self.management.auditLog.list_audit_logs(app_ids=["6139c4d24e78a4d706b7545b"])
        self.assertTrue(isinstance(res['data']['list'], list))
