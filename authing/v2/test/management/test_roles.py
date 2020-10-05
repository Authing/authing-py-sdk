import unittest
import os
from ...management import ManagementClientOptions
from ...management.authing import ManagementClient
from dotenv import load_dotenv
load_dotenv()


management = ManagementClient(ManagementClientOptions(
    userPoolId=os.getenv('AUTHING_USERPOOL_ID'),
    secret=os.getenv('AUTHING_USERPOOL_SECRET'),
    host=os.getenv('AUTHING_SERVER')
))


class TestRoles(unittest.TestCase):
    def test_list(self):
        totalCount, _list = management.roles.list()
        self.assertTrue(totalCount)
        self.assertTrue(_list)
