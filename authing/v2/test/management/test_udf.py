# coding: utf-8

import unittest
import os
from authing.v2.management.types import ManagementClientOptions
from authing.v2.management.authing import ManagementClient
from dotenv import load_dotenv






class TestUdf(unittest.TestCase):

    management = None;
    @classmethod
    def setUpClass(cls):
        load_dotenv()

    def setUp(self):
        self.management = ManagementClient(ManagementClientOptions(
            user_pool_id=os.getenv('AUTHING_USERPOOL_ID'),
            secret=os.getenv('AUTHING_USERPOOL_SECRET'),
            host=os.getenv('AUTHING_SERVER')
        ))

    def test_add(self):
        udf = self.management.udf.set(
            targetType='USER',
            key='school',
            dataType='STRING',
            label='学校'
        )
        self.assertTrue(udf)

        udfs = self.management.udf.list('USER')
        self.assertTrue(len(udfs))

    def test_remove(self):
        udf = self.management.udf.set(
            targetType='USER',
            key='schoosl',
            dataType='STRING',
            label='学校'
        )
        self.assertTrue(udf)
        self.management.udf.remove(
            targetType='USER',
            key='school'
        )
        res = self.management.udf.list('USER')
        self.assertFalse(udf in res)

    def test_set_udf_value_batch(self):
        res = self.management.udf.set_udf_value_batch(target_type="ROLE", target_id="6139e242fd34431069abe95c",udf_value_list=[
            {'key':'rr','value':'{"ccc":"qq"}'}])
        print (res)
        pass

    def test_list_udf_value(self):
        res = self.management.udf.list_udf_value(target_type="ROLE",target_id="6139cd72eee4ef2653efd1db")
        print (res)