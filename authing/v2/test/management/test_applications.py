import os
import unittest
from dotenv import load_dotenv

from authing.v2.management import ManagementClient, ManagementClientOptions
from authing.v2.test.utils import get_random_string

load_dotenv()

management = ManagementClient(ManagementClientOptions(
    user_pool_id=os.getenv('AUTHING_USERPOOL_ID'),
    secret=os.getenv('AUTHING_USERPOOL_SECRET'),
    host=os.getenv('AUTHING_SERVER')
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

        management.applications.list_resources(app_id="123", resource_type="123");