from ...common.utils import get_random_string, get_random_phone_number
from ...authentication import AuthenticationClientOptions
from ...authentication.authing import AuthenticationClient
import unittest
import os
from dotenv import load_dotenv
load_dotenv()


class TestAuthentication(unittest.TestCase):
    def test_register_by_email(self):
        authentication = AuthenticationClient(
            options=AuthenticationClientOptions(
                user_pool_id=os.getenv('AUTHING_USERPOOL_ID'),
                host=os.getenv('AUTHING_SERVER')
            )
        )
        email = '%s@authing.cn' % get_random_string(10)
        user = authentication.register_by_email(
            email=email,
            password=get_random_string(10),
        )
        self.assertTrue(user)
        self.assertTrue(user['id'])
        self.assertTrue(user['email'] == email)

    def test_register_by_username(self):
        authentication = AuthenticationClient(
            options=AuthenticationClientOptions(
                user_pool_id=os.getenv('AUTHING_USERPOOL_ID'),
                host=os.getenv('AUTHING_SERVER')
            )
        )
        username = get_random_string(10)
        user = authentication.register_by_username(
            username=username,
            password=get_random_string(10),
        )
        self.assertTrue(user)
        self.assertTrue(user['id'])
        self.assertTrue(user['username'] == username)

    # def test_send_sms_code(self):
    #     phone = get_random_phone_number()
    #     authentication.send_sms_code(phone=phone)

    # def test_register_by_phone_code(self):
    #     phone = get_random_phone_number()
    #     code = "6201"
    #     user = authentication.register_by_phone_code(
    #         phone=phone,
    #         code=code,
    #         password=get_random_string(10),
    #     )
    #     self.assertTrue(user)
    #     self.assertTrue(user['id'])
    #     self.assertTrue(user.get('phone') == phone)

    def test_login_by_email(self):
        authentication = AuthenticationClient(
            options=AuthenticationClientOptions(
                user_pool_id=os.getenv('AUTHING_USERPOOL_ID'),
                host=os.getenv('AUTHING_SERVER')
            )
        )
        email = '%s@authing.cn' % get_random_string(10)
        password = get_random_string(10)
        user = authentication.register_by_email(
            email=email,
            password=password,
        )
        user = authentication.login_by_email(
            email=email,
            password=password,
        )
        self.assertTrue(user)
        self.assertTrue(user.get('token'))
        self.assertTrue(user.get('email') == email)

    def test_login_by_username(self):
        authentication = AuthenticationClient(
            options=AuthenticationClientOptions(
                user_pool_id=os.getenv('AUTHING_USERPOOL_ID'),
                host=os.getenv('AUTHING_SERVER')
            )
        )
        username = get_random_string(10)
        password = get_random_string(10)
        user = authentication.register_by_username(
            username=username,
            password=password,
        )
        user = authentication.login_by_username(
            username=username,
            password=password,
        )
        self.assertTrue(user)
        self.assertTrue(user.get('token'))
        self.assertTrue(user.get('username') == username)

    # def test_login_by_phone_code(self):
    #     phone = '18899666324'
    #     code = "6201"
    #     user = authentication.login_by_phone_code(
    #         phone=phone,
    #         code=code,
    #     )
    #     self.assertTrue(user)
    #     self.assertTrue(user.get('token'))
    #     self.assertTrue(user.get('phone') == phone)

    # def test_login_by_phone_password(self):
    #     phone = '18899666325'
    #     code = "6201"
    #     password = get_random_string(10)
    #     user = authentication.register_by_phone_code(
    #         phone=phone,
    #         code=code,
    #         password=password
    #     )
    #     self.assertTrue(user)
    #     self.assertTrue(user.get('phone') == phone)

    #     user = authentication.login_by_phone_password(
    #         phone=phone,
    #         password=password
    #     )
    #     self.assertTrue(user)
    #     self.assertTrue(user.get('phone') == phone)
    #     self.assertTrue(user.get('token'))

    def test_init_by_access_token(self):
        authentication = AuthenticationClient(
            options=AuthenticationClientOptions(
                user_pool_id=os.getenv('AUTHING_USERPOOL_ID'),
                host=os.getenv('AUTHING_SERVER')
            )
        )
        email = '%s@authing.cn' % get_random_string(10)
        password = get_random_string(10)
        user = authentication.register_by_email(
            email=email,
            password=password,
        )
        user = authentication.login_by_email(
            email=email,
            password=password,
        )
        access_token = user.get('token')
        self.assertTrue(access_token)
        authentication = AuthenticationClient(
            options=AuthenticationClientOptions(
                user_pool_id=os.getenv('AUTHING_USERPOOL_ID'),
                host=os.getenv('AUTHING_SERVER'),
                access_token=access_token
            )
        )
        user = authentication.get_current_user()
        self.assertTrue(user)

        data = authentication.check_login_status()
        self.assertTrue(data)
        self.assertTrue(data.get('status'))

    def test_update_profile(self):
        authentication = AuthenticationClient(
            options=AuthenticationClientOptions(
                user_pool_id=os.getenv('AUTHING_USERPOOL_ID'),
                host=os.getenv('AUTHING_SERVER')
            )
        )
        email = '%s@authing.cn' % get_random_string(10)
        password = get_random_string(10)
        user = authentication.register_by_email(
            email=email,
            password=password,
        )
        user = authentication.login_by_email(
            email=email,
            password=password,
        )
        user = authentication.update_profile({
            'nickname': 'Nick'
        })
        self.assertTrue(user)
        self.assertTrue(user.get('nickname') == 'Nick')

    def test_update_password(self):
        authentication = AuthenticationClient(
            options=AuthenticationClientOptions(
                user_pool_id=os.getenv('AUTHING_USERPOOL_ID'),
                host=os.getenv('AUTHING_SERVER')
            )
        )
        email = '%s@authing.cn' % get_random_string(10)
        password = get_random_string(10)
        user = authentication.register_by_email(
            email=email,
            password=password,
        )
        user = authentication.login_by_email(
            email=email,
            password=password,
        )
        new_password = get_random_string(10)
        authentication.update_password(
            new_password=new_password,
            old_password=password
        )
        user = authentication.login_by_email(
            email=email,
            password=new_password,
        )
        self.assertTrue(user)

    def test_refresh_token(self):
        authentication = AuthenticationClient(
            options=AuthenticationClientOptions(
                user_pool_id=os.getenv('AUTHING_USERPOOL_ID'),
                host=os.getenv('AUTHING_SERVER')
            )
        )
        email = '%s@authing.cn' % get_random_string(10)
        password = get_random_string(10)
        user = authentication.register_by_email(
            email=email,
            password=password,
            generate_token=True
        )
        authentication.refresh_token()
        user = authentication.get_current_user()
        self.assertTrue(user)
