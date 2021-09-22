# coding: utf-8

from authing.v2.test.utils import get_random_string
from authing.v2.authentication import AuthenticationClientOptions
from authing.v2.authentication.authing import AuthenticationClient
from authing.v2.management.types import ManagementClientOptions
from authing.v2.management.authing import ManagementClient
import os

class TestHelper():

    def __init__(self):
        pass

    @staticmethod
    def init_authentication_client():
        authentication_client = AuthenticationClient(
            options=AuthenticationClientOptions(
                app_id=os.getenv("AUTHING_APP_ID"),
                app_host=os.getenv("AUTHING_APP_HOST"),
                use_unverified_ssl=True
            )
        )
        return authentication_client

    @staticmethod
    def init_mfa_authentication_client():
        return MfaAuthenticationClient(options=AuthenticationClientOptions(
                app_id=os.getenv("AUTHING_APP_ID"),
                app_host=os.getenv("AUTHING_APP_HOST"),
                use_unverified_ssl=True
            ))

    def register_random_user(self):
        authentication_client = self.init_authentication_client()
        email = "%s@authing.cn" % get_random_string(10)
        password = get_random_string(10)
        user = authentication_client.register_by_email(email, password, force_login=True)
        return email, password, user, authentication_client

    def getManagementByEnv(self):
        return ManagementClient(ManagementClientOptions(
                        user_pool_id=os.getenv("AUTHING_USERPOOL_ID"),
                        secret=os.getenv("AUTHING_USERPOOL_SECRET"),
                        host=os.getenv("AUTHING_SERVER"))
                )
