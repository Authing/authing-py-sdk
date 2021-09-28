import os
import unittest
from dotenv import load_dotenv

from authing.v2.management import ManagementClient, ManagementClientOptions
from authing.v2.test.utils import get_random_string

load_dotenv()

management = ManagementClient(ManagementClientOptions(
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

default_namespace = 'default'


def create():
    app_name = "python sdk unittest " + get_random_string(4)
    identifier = "python-sdk-unittest-" + get_random_string(4)
    redirect_uris = "https://www.authing.com"

    app = management.applications.create(
        name=app_name,
        identifier=identifier,
        redirect_uris=[redirect_uris]
    )

    return app


class TestApp(unittest.TestCase):

    def test_list(self):
        app_list = management.applications.list()

        self.assertTrue(app_list.get("list") is not None)
        self.assertTrue(app_list.get("totalCount") is not None)

    def test_create(self):
        app_name = "python sdk unittest " + get_random_string(4)
        identifier = "python-sdk-unittest-" + get_random_string(4)
        redirect_uris = "https://www.authing.com"

        app = management.applications.create(
            name=app_name,
            identifier=identifier,
            redirect_uris=[redirect_uris]
        )

        self.assertTrue(app.get("name") == app_name)
        self.assertTrue(app.get("identifier") == identifier)
        self.assertTrue(app.get("redirectUris")[0] == redirect_uris)

    def test_delete(self):
        app = create()
        deleted = management.applications.delete(app.get("id"))

        self.assertTrue(deleted)

    def test_find_by_id(self):
        app = create()
        find_app = management.applications.find_by_id(app.get("id"))

        self.assertTrue(find_app["id"] == app["id"])

        management.applications.delete(app["id"])

    def test_list_resources(self):

       rs = management.applications.list_resources(app_id="61384d3ee1b81dd1342e5635", resource_type="MENU")
       print (rs)
       self.assertTrue(rs)

    def test_create_resources(self):
        res = management.applications.create_resource(app_id="61384d3ee1b81dd1342e5635", resource_type="MENU",
                                                      code='xx', actions=[{'name':'x','description':'xxx'}])
        print res

    def test_get_access_policies(self):
        res = management.applications.get_access_policies("6139c4d24e78a4d706b7545b")
        print (res)

    def test_create_agreement(self):
        title = "cccc"
        res = management.applications.create_agreement("6139c4d24e78a4d706b7545b",title)
        self.assertEquals(res['data']['title'], title)

    def test_list_agreement(self):
        res = management.applications.list_agreement("6139c4d24e78a4d706b7545b")
        self.assertTrue(isinstance(res['data']['list'], list))

    def test_modify_agreement(self):
        title = "cc"
        res = management.applications.modify_agreement("6139c4d24e78a4d706b7545b","210",title)
        self.assertEquals(res['data']['title'], title)

    def test_delete_agreement(self):
        res = management.applications.delete_agreement("6139c4d24e78a4d706b7545b", "218")
        self.assertEquals(res['code'], 200)

    def test_order_agreement(self):
        res = management.applications.sort_agreement("6139c4d24e78a4d706b7545b",["210",'110'])
        self.assertEquals(res['code'], 200)

    def test_refresh_application_secret(self):
        res = management.applications.refresh_application_secret("6139c4d24e78a4d706b7545b")
        self.assertEquals(res['code'], 200)

    def test_active_users(self):
        res = management.applications.active_users("6139c4d24e78a4d706b7545b")
        self.assertTrue(isinstance(res['data']['list'],list))