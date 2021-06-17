# coding: utf-8
import json

from ...exceptions import AuthingException
from ..utils import get_random_string
from ...authentication import AuthenticationClientOptions
from ...authentication.authing import AuthenticationClient
from ...management.types import ManagementClientOptions
from ...management.authing import ManagementClient
import unittest
import os
from datetime import datetime
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs

load_dotenv()

management = ManagementClient(
    ManagementClientOptions(
        user_pool_id=os.getenv("AUTHING_USERPOOL_ID"),
        secret=os.getenv("AUTHING_USERPOOL_SECRET"),
        host=os.getenv("AUTHING_SERVER"),
    )
)


def init_authentication_client():
    authentication_client = AuthenticationClient(
        options=AuthenticationClientOptions(
            app_id=os.getenv("AUTHING_APP_ID"),
            app_host=os.getenv("AUTHING_APP_HOST"),
            use_unverified_ssl=True
        )
    )
    return authentication_client


def register_random_user():
    authentication_client = init_authentication_client()
    email = "%s@authing.cn" % get_random_string(10)
    password = get_random_string(10)
    user = authentication_client.register_by_email(email, password, force_login=True)
    return email, password, user, authentication_client


class TestAuthentication(unittest.TestCase):


    def test_init_with_no_userpoolid_and_appid(self):
        error = False
        try:
            AuthenticationClient(options=AuthenticationClientOptions())
        except:
            error = True
        self.assertTrue(error)

    def test_catch_error(self):
        authentication = init_authentication_client()
        username = get_random_string(10)
        password = get_random_string(10)

        try:
            authentication.login_by_username(
                username=username,
                password=password,
            )
        except AuthingException as e:
            print(e.code)
            print(e.message)
            self.assertTrue(e.code)
            self.assertTrue(e.message)

    def test_register_by_email(self):
        authentication = init_authentication_client()
        email = "%s@authing.cn" % get_random_string(10)
        user = authentication.register_by_email(
            email=email,
            password=get_random_string(10),
        )
        self.assertTrue(user)
        self.assertTrue(user["id"])
        self.assertTrue(user["email"] == email)

    def test_register_by_email_with_profile(self):
        authentication = init_authentication_client()
        email = "%s@authing.cn" % get_random_string(10)
        user = authentication.register_by_email(
            email=email,
            password=get_random_string(10),
            profile={"nickname": "Nick"},
            generate_token=True,
        )
        self.assertTrue(user)
        self.assertTrue(user["id"])
        self.assertTrue(user["email"] == email)
        self.assertTrue(user["token"] is not None)

    def test_register_by_email_with_custom_data(self):
        authentication = init_authentication_client()
        email = "%s@authing.cn" % get_random_string(10)
        user = authentication.register_by_email(
            email=email,
            password=get_random_string(10),
            custom_data={
                'school': '华中科技大学',
                'age': 22
            },
            force_login=True
        )
        self.assertTrue(user['id'])
        udvs = authentication.get_udf_value()
        self.assertTrue(udvs['school'], '华中科技大学')
        self.assertTrue(udvs['age'], 22)

    def test_register_by_email_with_context(self):
        authentication = init_authentication_client()
        email = "%s@authing.cn" % get_random_string(10)
        user = authentication.register_by_email(
            email=email,
            password=get_random_string(10),
            context={
                'source': 'google'
            }
        )
        self.assertTrue(user['id'])

    def test_register_by_username(self):
        authentication = init_authentication_client()
        username = get_random_string(10)
        user = authentication.register_by_username(
            username=username,
            password=get_random_string(10),
        )
        self.assertTrue(user)
        self.assertTrue(user["id"])
        self.assertTrue(user["username"] == username)

    def test_send_sms_code(self):
        authentication = init_authentication_client()
        phone = '17670416754'
        authentication.send_sms_code(phone=phone)

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
        authentication = init_authentication_client()
        email = "%s@authing.cn" % get_random_string(10)
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
        self.assertTrue(user.get("token"))
        self.assertTrue(user.get("email") == email)

    def test_login_by_email_with_custom_data(self):
        authentication = init_authentication_client()
        email = "%s@authing.cn" % get_random_string(10)
        password = get_random_string(10)
        user = authentication.register_by_email(
            email=email,
            password=password,
        )
        user = authentication.login_by_email(
            email=email,
            password=password,
            custom_data={
                'school': '华中科技大学',
                'age': 22
            }
        )
        self.assertTrue(user['id'])
        udvs = authentication.get_udf_value()
        self.assertTrue(udvs['school'], '华中科技大学')
        self.assertTrue(udvs['age'], 22)

    def test_login_by_email_with_context(self):
        authentication = init_authentication_client()
        email = "%s@authing.cn" % get_random_string(10)
        password = get_random_string(10)
        user = authentication.register_by_email(
            email=email,
            password=password,
        )
        user = authentication.login_by_email(
            email=email,
            password=password,
            context={
                'source': 'google'
            }
        )
        self.assertTrue(user['id'])

    def test_login_by_username(self):
        authentication = init_authentication_client()
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
        self.assertTrue(user.get("token"))
        self.assertTrue(user.get("username") == username)

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

    def test_init_by_token(self):
        authentication = init_authentication_client()
        email = "%s@authing.cn" % get_random_string(10)
        password = get_random_string(10)
        user = authentication.register_by_email(
            email=email,
            password=password,
        )
        user = authentication.login_by_email(
            email=email,
            password=password,
        )
        token = user.get("token")
        self.assertTrue(token)
        authentication = AuthenticationClient(
            options=AuthenticationClientOptions(
                app_id=os.getenv("AUTHING_APP_ID"),
                app_host=os.getenv('AUTHING_APP_HOST'),
                token=token,
            )
        )
        user = authentication.get_current_user()
        self.assertTrue(user)

        data = authentication.check_login_status()
        print(json.dumps(data, indent=4, ensure_ascii=False))
        self.assertTrue(data)
        self.assertTrue(data.get("status"))

    def test_check_password_strength(self):
        authentication = init_authentication_client()
        res = authentication.check_password_strength('')
        valid, message = res['valid'], res['message']
        self.assertTrue(valid is False)
        self.assertTrue(message)

    def test_send_email(self):
        authentication = init_authentication_client()
        email = 'cj@authing.cn'
        res = authentication.send_email(email, 'RESET_PASSWORD')
        code, message = res['code'], res['message']
        self.assertTrue(code == 200)

    @unittest.skip('need to send sms code')
    def test_rest_password_by_phone_code(self):
        authentication = init_authentication_client()
        phone = '17670416754'
        user = management.users.create({
            'phone': phone
        })
        # authentication.send_sms_code(phone)

        new_password = 'passw0rd'
        authentication.reset_password_by_phone_code(phone, '1811', new_password)
        user = authentication.login_by_phone_password(phone, new_password)
        self.assertTrue(user['id'])

    def test_reset_password_by_email_code(self):
        authentication = init_authentication_client()
        email = 'cj@authing.cn'
        # user = management.users.create({
        #     'email': email
        # })

        new_password = 'passw0rd'
        # authentication.send_email(email, 'RESET_PASSWORD')
        authentication.reset_password_by_email_code(email, '1670', new_password)
        user = authentication.login_by_email(email, new_password)
        self.assertTrue(user['id'])

    def test_update_profile(self):
        authentication = init_authentication_client()
        email = "%s@authing.cn" % get_random_string(10)
        password = get_random_string(10)
        user = authentication.register_by_email(
            email=email,
            password=password,
        )
        user = authentication.login_by_email(
            email=email,
            password=password,
        )
        user = authentication.update_profile({"nickname": "Nick"})
        self.assertTrue(user)
        self.assertTrue(user.get("nickname") == "Nick")

    def test_update_password(self):
        authentication = init_authentication_client()
        email = "%s@authing.cn" % get_random_string(10)
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
        authentication.update_password(new_password=new_password, old_password=password)
        user = authentication.login_by_email(
            email=email,
            password=new_password,
        )
        self.assertTrue(user)

    def test_add_udv_wrong_type(self):
        authentication = init_authentication_client()
        email = "%s@authing.cn" % get_random_string(10)
        password = get_random_string(10)
        authentication.register_by_email(
            email=email, password=password, generate_token=True
        )

        # 字符串
        failed = False
        try:
            management.udf.set(
                targetType="USER", key="school", dataType="STRING", label="学校"
            )
            authentication.set_udv(key="school", value=11)
        except Exception as e:
            failed = True
        self.assertTrue(failed)

        # 数字
        failed = False
        try:
            management.udf.set(
                targetType="USER", key="age", dataType="NUMBER", label="学校"
            )
            authentication.set_udv(key="age", value="18")
        except:
            failed = True
        self.assertTrue(failed)

        # boolean
        failed = False
        try:
            management.udf.set(
                targetType="USER", key="is_boss", dataType="BOOLEAN", label="是否为 boss"
            )
            authentication.set_udv(key="is_boss", value="ok")
        except:
            failed = True
        self.assertTrue(failed)

    def test_add_udv_string(self):
        authentication = init_authentication_client()
        email = "%s@authing.cn" % get_random_string(10)
        password = get_random_string(10)
        authentication.register_by_email(
            email=email, password=password, generate_token=True
        )

        management.udf.set(
            targetType="USER", key="school", dataType="STRING", label="学校"
        )
        authentication.set_udv(key="school", value="ucla")
        udvs = authentication.list_udv()
        self.assertTrue(len(udvs) == 1)
        self.assertTrue(isinstance(udvs[0]["value"], str))

    def test_add_udv_int(self):
        authentication = init_authentication_client()
        email = "%s@authing.cn" % get_random_string(10)
        password = get_random_string(10)
        authentication.register_by_email(
            email=email, password=password, generate_token=True
        )
        management.udf.set(targetType="USER", key="age", dataType="NUMBER", label="学校")
        authentication.set_udv(key="age", value=18)
        udvs = authentication.list_udv()
        self.assertTrue(len(udvs) == 1)
        self.assertTrue(isinstance(udvs[0]["value"], int))

    def test_add_udv_boolean(self):
        authentication = init_authentication_client()
        email = "%s@authing.cn" % get_random_string(10)
        password = get_random_string(10)
        authentication.register_by_email(
            email=email, password=password, generate_token=True
        )
        management.udf.set(
            targetType="USER", key="is_boss", dataType="BOOLEAN", label="是否为 boss"
        )
        authentication.set_udv(key="is_boss", value=False)
        udvs = authentication.list_udv()
        self.assertTrue(len(udvs) == 1)
        self.assertTrue(isinstance(udvs[0]["value"], bool))

    def test_add_udv_datetime(self):
        authentication = init_authentication_client()
        email = "%s@authing.cn" % get_random_string(10)
        password = get_random_string(10)
        authentication.register_by_email(
            email=email, password=password, generate_token=True
        )
        management.udf.set(
            targetType="USER", key="birthday", dataType="DATETIME", label="生日"
        )
        authentication.set_udv(key="birthday", value=datetime.now())
        udvs = authentication.list_udv()
        self.assertTrue(len(udvs) == 1)
        self.assertTrue(isinstance(udvs[0]["value"], datetime))

    def test_add_udv_object(self):
        authentication = init_authentication_client()
        email = "%s@authing.cn" % get_random_string(10)
        password = get_random_string(10)
        authentication.register_by_email(
            email=email, password=password, generate_token=True
        )
        management.udf.set(
            targetType="USER", key="settings", dataType="OBJECT", label="设置"
        )
        authentication.set_udv(key="settings", value={"favorColor": "red"})
        udvs = authentication.list_udv()
        self.assertTrue(len(udvs) == 1)
        self.assertTrue(isinstance(udvs[0]["value"], dict))

    def test_remove_duv(self):
        authentication = init_authentication_client()
        email = "%s@authing.cn" % get_random_string(10)
        password = get_random_string(10)
        authentication.register_by_email(
            email=email, password=password, generate_token=True
        )
        management.udf.set(targetType="USER", key="age", dataType="NUMBER", label="学校")
        authentication.set_udv(key="age", value=18)
        authentication.remove_udv(
            key="age",
        )
        udvs = authentication.list_udv()
        self.assertTrue(len(udvs) == 0)

    @unittest.skip('logout')
    def test_logout(self):
        authentication_client = init_authentication_client()
        authentication_client.login_by_email('abc@authing.cn', 'abc@authing.cn')
        success = authentication_client.logout()
        self.assertTrue(success)

    def test_logout_with_wrong_token(self):
        try:
            authentication_client = AuthenticationClient(
                options=AuthenticationClientOptions(
                    app_id=os.getenv("AUTHING_APP_ID"),
                    app_host=os.getenv("AUTHING_APP_HOST"),
                    token='wrong token'
                )
            )
            authentication_client.logout()
        except AuthingException as e:
            self.assertTrue(e.code == 2020)

    @unittest.skip('ldap')
    def test_login_by_ldap(self):
        authentication_client = init_authentication_client()
        user = authentication_client.login_by_ldap('admin', 'admin')
        self.assertTrue(user)

    @unittest.skip('ad')
    def test_login_by_ad(self):
        authentication_client = init_authentication_client()
        user = authentication_client.login_by_ad('admin', 'admin')
        self.assertTrue(user)

    @unittest.skip('list_orgs')
    def test_list_orgs(self):
        authentication_client = init_authentication_client()
        user = authentication_client.login_by_email('cj@authing.cn', 'cj@authing.cn')
        data = authentication_client.list_orgs()
        self.assertTrue(data)

    def test_set_udf_value(self):
        authentication_client = init_authentication_client()
        email = "%s@authing.cn" % get_random_string(10)
        password = get_random_string(10)
        user = authentication_client.register_by_email(email, password, force_login=True)

        authentication_client.set_udf_value({
            'school': '华中科技大学',
            'age': 22
        })

        values = authentication_client.get_udf_value()
        self.assertTrue(values['school'] == '华中科技大学')
        self.assertTrue(values['age'] == 22)

    def test_remove_udf_value(self):
        authentication_client = init_authentication_client()
        email = "%s@authing.cn" % get_random_string(10)
        password = get_random_string(10)
        user = authentication_client.register_by_email(email, password, force_login=True)
        authentication_client.set_udf_value({
            'school': '华中科技大学',
            'age': 22
        })
        authentication_client.remove_udf_value('school')

        values = authentication_client.get_udf_value()
        self.assertTrue(values.get('school') is None)
        self.assertTrue(values['age'] == 22)

    def test_get_security_level(self):
        authentication_client = init_authentication_client()
        email = "%s@authing.cn" % get_random_string(10)
        password = get_random_string(10)
        user = authentication_client.register_by_email(email, password, force_login=True)

        data = authentication_client.get_security_level()
        self.assertTrue(data.get('email'))
        self.assertTrue(data.get('password'))
        self.assertFalse(data.get('mfa'))
        self.assertTrue(isinstance(data.get('passwordSecurityLevel'), int))

    def test_list_roles(self):
        _, _, user, authentication_client = register_random_user()
        code = get_random_string(10)
        role = management.roles.create(
            code=code
        )
        management.users.add_roles(user.get('id'), [code])

        data = authentication_client.list_roles()
        total_count, roles = data['totalCount'], data['list']
        self.assertTrue(total_count == 1)

    def test_has_role(self):
        _, _, user, authentication_client = register_random_user()
        code = get_random_string(10)
        role = management.roles.create(
            code=code
        )
        management.users.add_roles(user.get('id'), [code])
        has_role = authentication_client.has_role(code)
        self.assertTrue(has_role)

    def test_list_applications(self):
        _, _, user, authentication_client = register_random_user()
        data = authentication_client.list_applications()
        list, total_count = data.get('list'), data.get('totalCount')
        self.assertTrue(len(list))
        self.assertTrue(total_count > 0)

    def test_list_authorized_resources(self):
        pass

    @unittest.skip('test_get_access_token_by_code_with_client_secret_post')
    def test_oidc_get_access_token_by_code_with_client_secret_post(self):
        authentication_client = AuthenticationClient(options=AuthenticationClientOptions(
            app_id=os.getenv('AUTHING_APP_ID'),
            app_host=os.getenv('AUTHING_APP_HOST'),
            secret=os.getenv('AUTHING_APP_SECRET'),
            protocol=os.getenv('AUTHING_APP_PROTOCOL'),
            redirect_uri=os.getenv('AUTHING_APP_REDIRECT_URI'),
            token_endpoint_auth_method='client_secret_post'
        ))
        data = authentication_client.get_access_token_by_code('Qzi_nSKjqgzFyDwjPpiGS5q01OGqcePVMR1MqJ8dnp7')
        self.assertTrue(data.get('access_token'))

    @unittest.skip('test_oidc_get_access_token_by_code_with_client_secret_basic')
    def test_oidc_get_access_token_by_code_with_client_secret_basic(self):
        authentication_client = AuthenticationClient(options=AuthenticationClientOptions(
            app_id=os.getenv('AUTHING_APP_ID'),
            app_host=os.getenv('AUTHING_APP_HOST'),
            secret=os.getenv('AUTHING_APP_SECRET'),
            protocol=os.getenv('AUTHING_APP_PROTOCOL'),
            redirect_uri=os.getenv('AUTHING_APP_REDIRECT_URI'),
            token_endpoint_auth_method='client_secret_basic'
        ))
        data = authentication_client.get_access_token_by_code('ZfHkrJNaByvLophVTVLKdCmvCNIzuQwtcCTXK1E08cS')
        self.assertTrue(data.get('access_token'))

    @unittest.skip('test_oidc_get_access_token_by_code_with_none')
    def test_oidc_get_access_token_by_code_with_none(self):
        authentication_client = AuthenticationClient(options=AuthenticationClientOptions(
            app_id=os.getenv('AUTHING_APP_ID'),
            app_host=os.getenv('AUTHING_APP_HOST'),
            secret=os.getenv('AUTHING_APP_SECRET'),
            protocol=os.getenv('AUTHING_APP_PROTOCOL'),
            redirect_uri=os.getenv('AUTHING_APP_REDIRECT_URI'),
            token_endpoint_auth_method='none'
        ))
        data = authentication_client.get_access_token_by_code('O36lNUcRrpB2wcbyUbGh1lQuP9ERrc79LKrKKB8hDkb')
        self.assertTrue(data.get('access_token'))

    @unittest.skip('test_oauth_get_access_token_by_code_with_client_secret_post')
    def test_oauth_get_access_token_by_code_with_client_secret_post(self):
        authentication_client = AuthenticationClient(options=AuthenticationClientOptions(
            app_id=os.getenv('AUTHING_APP_ID'),
            app_host=os.getenv('AUTHING_APP_HOST'),
            secret=os.getenv('AUTHING_APP_SECRET'),
            protocol=os.getenv('AUTHING_APP_PROTOCOL'),
            redirect_uri=os.getenv('AUTHING_APP_REDIRECT_URI'),
            token_endpoint_auth_method='client_secret_post'
        ))
        data = authentication_client.get_access_token_by_code('a910d08497c69fd04867851b9ad82755aa1dd127')
        self.assertTrue(data.get('access_token'))
        self.assertTrue(data.get('refresh_token'))

    @unittest.skip('test_oauth_get_access_token_by_code_with_client_secret_basic')
    def test_oauth_get_access_token_by_code_with_client_secret_basic(self):
        authentication_client = AuthenticationClient(options=AuthenticationClientOptions(
            app_id=os.getenv('AUTHING_APP_ID'),
            app_host=os.getenv('AUTHING_APP_HOST'),
            secret=os.getenv('AUTHING_APP_SECRET'),
            protocol=os.getenv('AUTHING_APP_PROTOCOL'),
            redirect_uri=os.getenv('AUTHING_APP_REDIRECT_URI'),
            token_endpoint_auth_method='client_secret_basic'
        ))
        data = authentication_client.get_access_token_by_code('b77ca8b05009a6bf695d212f1ae02d5b812fb4cb')
        self.assertTrue(data.get('access_token'))
        self.assertTrue(data.get('refresh_token'))

    @unittest.skip('test_oauth_get_access_token_by_code_with_none')
    def test_oauth_get_access_token_by_code_with_none(self):
        authentication_client = AuthenticationClient(options=AuthenticationClientOptions(
            app_id=os.getenv('AUTHING_APP_ID'),
            app_host=os.getenv('AUTHING_APP_HOST'),
            secret=os.getenv('AUTHING_APP_SECRET'),
            protocol=os.getenv('AUTHING_APP_PROTOCOL'),
            redirect_uri=os.getenv('AUTHING_APP_REDIRECT_URI'),
            token_endpoint_auth_method='none'
        ))
        data = authentication_client.get_access_token_by_code('5ff759fa7fd649cc2b8b29a11b7c800f6829cc9d')
        self.assertTrue(data.get('access_token'))
        self.assertTrue(data.get('refresh_token'))

    @unittest.skip('test_get_access_token_by_client_credentials')
    def test_get_access_token_by_client_credentials(self):
        authentication_client = AuthenticationClient(options=AuthenticationClientOptions(
            app_id=os.getenv('AUTHING_APP_ID'),
            app_host=os.getenv('AUTHING_APP_HOST'),
            secret=os.getenv('AUTHING_APP_SECRET'),
            protocol=os.getenv('AUTHING_APP_PROTOCOL'),
        ))
        scope = 'customer'
        access_key = '608521d72488c6bf44ceb6c8'
        access_secret = '6bfdea5545f52d1644ac0ba696592f94'
        data = authentication_client.get_access_token_by_client_credentials(scope, access_key, access_secret)
        self.assertTrue(data.get('access_token'))

    @unittest.skip('test_get_user_info_by_access_token')
    def test_get_user_info_by_access_token(self):
        authentication_client = AuthenticationClient(options=AuthenticationClientOptions(
            app_id=os.getenv('AUTHING_APP_ID'),
            app_host=os.getenv('AUTHING_APP_HOST'),
            secret=os.getenv('AUTHING_APP_SECRET'),
            protocol=os.getenv('AUTHING_APP_PROTOCOL'),
            redirect_uri=os.getenv('AUTHING_APP_REDIRECT_URI'),
            token_endpoint_auth_method='client_secret_post'
        ))
        data = authentication_client.get_access_token_by_code('VgVaLlOsY3GcB8TTzwPn12kcm1OqJ0zbBpLYCW_Gfib')
        access_token = data.get('access_token')
        if not access_token:
            self.fail()
        user_info = authentication_client.get_user_info_by_access_token(access_token)
        self.assertTrue(user_info.get('sub'))

    # 拼接 OIDC 授权码模式授权链接
    def test_oidc_build_authorize_url_authorization_code_mode(self):
        authentication_client = AuthenticationClient(options=AuthenticationClientOptions(
            app_id=os.getenv('AUTHING_APP_ID'),
            app_host=os.getenv('AUTHING_APP_HOST'),
            secret=os.getenv('AUTHING_APP_SECRET'),
            protocol=os.getenv('AUTHING_APP_PROTOCOL'),
            redirect_uri=os.getenv('AUTHING_APP_REDIRECT_URI'),
            token_endpoint_auth_method='client_secret_basic'
        ))
        url = authentication_client.build_authorize_url(response_mode='form_post')
        parsed_url = urlparse(url)
        queries = parse_qs(parsed_url.query)

        self.assertTrue(queries.get('nonce') is not None)
        self.assertTrue(queries.get('state') is not None)
        self.assertTrue(queries.get('scope') is not None)
        self.assertTrue(queries.get('client_id')[0] == os.getenv('AUTHING_APP_ID'))
        self.assertTrue(queries.get('redirect_uri')[0] == os.getenv('AUTHING_APP_REDIRECT_URI'))
        self.assertTrue(queries.get('response_type')[0] == 'code')
        self.assertTrue(queries.get('response_mode')[0] == 'form_post')

    # 拼接 OIDC 隐式模式授权链接
    def test_oidc_build_authorize_url_implicit_mode(self):
        authentication_client = AuthenticationClient(options=AuthenticationClientOptions(
            app_id=os.getenv('AUTHING_APP_ID'),
            app_host=os.getenv('AUTHING_APP_HOST'),
            secret=os.getenv('AUTHING_APP_SECRET'),
            protocol=os.getenv('AUTHING_APP_PROTOCOL'),
            redirect_uri=os.getenv('AUTHING_APP_REDIRECT_URI'),
            token_endpoint_auth_method='client_secret_basic'
        ))
        url = authentication_client.build_authorize_url(response_type='id_token token')
        parsed_url = urlparse(url)
        queries = parse_qs(parsed_url.query)
        self.assertTrue(queries.get('response_type')[0] == 'id_token token')

    # 拼接 OIDC 带 refresh_token 能力的授权链接
    def test_oidc_build_authorize_url_offline_access(self):
        authentication_client = AuthenticationClient(options=AuthenticationClientOptions(
            app_id=os.getenv('AUTHING_APP_ID'),
            app_host=os.getenv('AUTHING_APP_HOST'),
            secret=os.getenv('AUTHING_APP_SECRET'),
            protocol=os.getenv('AUTHING_APP_PROTOCOL'),
            redirect_uri=os.getenv('AUTHING_APP_REDIRECT_URI'),
            token_endpoint_auth_method='client_secret_basic'
        ))
        url = authentication_client.build_authorize_url(scope='openid profile offline_access')
        parsed_url = urlparse(url)
        queries = parse_qs(parsed_url.query)
        self.assertTrue(queries.get('prompt')[0] == 'consent')

    # 拼接 OIDC 授权码 + PKCE 带 refresh_token 能力的授权链接
    def test_oidc_build_authorize_url_pkce_s256(self):
        authentication_client = AuthenticationClient(options=AuthenticationClientOptions(
            app_id=os.getenv('AUTHING_APP_ID'),
            app_host=os.getenv('AUTHING_APP_HOST'),
            secret=os.getenv('AUTHING_APP_SECRET'),
            protocol=os.getenv('AUTHING_APP_PROTOCOL'),
            redirect_uri=os.getenv('AUTHING_APP_REDIRECT_URI'),
            token_endpoint_auth_method='client_secret_basic'
        ))
        code_verifier = authentication_client.generate_code_challenge()
        code_challenge = authentication_client.generate_code_challenge_digest(code_verifier)
        url = authentication_client.build_authorize_url(
            code_challenge=code_challenge,
            code_challenge_method='S256'
        )
        parsed_url = urlparse(url)
        queries = parse_qs(parsed_url.query)

        self.assertTrue(queries.get('code_challenge')[0] == code_challenge)
        self.assertTrue(queries.get('code_challenge_method')[0] == 'S256')

        print(code_challenge)
        print(url)

    # 拼接 OIDC 授权码 + PKCE 带 refresh_token 能力的授权链接
    def test_oidc_build_authorize_url_pkce_plain(self):
        authentication_client = AuthenticationClient(options=AuthenticationClientOptions(
            app_id=os.getenv('AUTHING_APP_ID'),
            app_host=os.getenv('AUTHING_APP_HOST'),
            secret=os.getenv('AUTHING_APP_SECRET'),
            protocol=os.getenv('AUTHING_APP_PROTOCOL'),
            redirect_uri=os.getenv('AUTHING_APP_REDIRECT_URI'),
            token_endpoint_auth_method='client_secret_basic'
        ))
        code_verifier = authentication_client.generate_code_challenge()
        code_challenge = authentication_client.generate_code_challenge_digest(code_verifier, method='plain')
        url = authentication_client.build_authorize_url(
            code_challenge=code_challenge,
            code_challenge_method='plain',
            scope='openid profile offline_access'
        )
        parsed_url = urlparse(url)
        queries = parse_qs(parsed_url.query)

        self.assertTrue(queries.get('code_challenge')[0] == code_challenge)
        self.assertTrue(queries.get('code_challenge_method')[0] == 'plain')
        self.assertTrue(queries.get('prompt')[0] == 'consent')

    # OIDC 授权码 + PKCE code 换 token
    def test_oidc_get_access_token_by_code_with_pkce(self):
        authentication_client = AuthenticationClient(options=AuthenticationClientOptions(
            app_id=os.getenv('AUTHING_APP_ID'),
            app_host=os.getenv('AUTHING_APP_HOST'),
            secret=os.getenv('AUTHING_APP_SECRET'),
            protocol=os.getenv('AUTHING_APP_PROTOCOL'),
            redirect_uri=os.getenv('AUTHING_APP_REDIRECT_URI'),
            token_endpoint_auth_method='client_secret_post'
        ))
        data = authentication_client.get_access_token_by_code(
            't2wMl5im8glCz-ILg1KY9i8b-8OazHtvRnKXO8ojo59',
            code_verifier='qPpNQbYT_fFa4bnKwf8udH5JjMz1f3b93WrmYmL7nZg'
        )

    def test_oauth_build_authorize_url(self):
        authentication_client = AuthenticationClient(options=AuthenticationClientOptions(
            app_id=os.getenv('AUTHING_APP_ID'),
            app_host=os.getenv('AUTHING_APP_HOST'),
            secret=os.getenv('AUTHING_APP_SECRET'),
            protocol=os.getenv('AUTHING_APP_PROTOCOL'),
            redirect_uri=os.getenv('AUTHING_APP_REDIRECT_URI'),
            token_endpoint_auth_method='client_secret_post'
        ))
        url = authentication_client.build_authorize_url()
        parsed_url = urlparse(url)
        queries = parse_qs(parsed_url.query)
        self.assertTrue(queries.get('response_type')[0] == 'code')
        self.assertTrue(queries.get('scope')[0] == 'user')
