from os import scandir
from ...common.utils import get_random_string
import unittest
import os
from ...management.types import ManagementClientOptions
from ...management.authing import ManagementClient
from dotenv import load_dotenv
load_dotenv()


management = ManagementClient(ManagementClientOptions(
    user_pool_id=os.getenv('AUTHING_USERPOOL_ID'),
    secret=os.getenv('AUTHING_USERPOOL_SECRET'),
    host=os.getenv('AUTHING_SERVER')
))


class TestUdf(unittest.TestCase):
    def test_add(self):
        udf = management.udf.set(
            targetType='USER',
            key='school',
            dataType='STRING',
            label='学校'
        )
        self.assertTrue(udf)

        udfs = management.udf.list('USER')
        self.assertTrue(len(udfs))

    def test_remove(self):
        udf = management.udf.set(
            targetType='USER',
            key='school',
            dataType='STRING',
            label='学校'
        )
        self.assertTrue(udf)
        management.udf.remove(
            targetType='USER',
            key='school'
        )
