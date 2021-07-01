# coding: utf-8
import re

from ..common.rest import RestClient
from .types import AuthenticationClientOptions
from ..common.graphql import GraphqlClient
from ..common.utils import encrypt, convert_udv_data_type, convert_udv_list_to_dict, get_hostname_from_url, \
    format_authorized_resources, get_random_string, url_join_args
from ..common.codegen import QUERY
from ..exceptions import AuthingWrongArgumentException, AuthingException
import json
import datetime
import base64
import hashlib


class AuthenticationClient(object):
    """Authing Management Client"""

    def __init__(self, options):
        # type:(AuthenticationClientOptions) -> AuthenticationClient

        self.options = options
        self.graphqlClient = GraphqlClient(
            options=self.options, endpoint=self.options.graphql_endpoint
        )
        self.restClient = RestClient(options=self.options)

        # 当前用户
        self._user = None
        # 当前用户的 token
        self._token = self.options.token or None

    def _set_current_user(self, user):
        self._user = user
        self._token = user.get("token")

    def _clear_current_user(self):
        self._user = None
        self._token = None

    def _check_logged_in(self):
        user = self.get_current_user()
        if not user:
            raise Exception("Please Login First")
        return user

    def _get_token(self):
        return self._token

    def _set_token(self, token):
        self._token = token

    def get_current_user(self, token=None):
        """获取当前用户的资料

        Args:
            token (str): 用户登录凭证
        """
        url = "%s/api/v2/users/me" % self.options.host
        data = self.restClient.request(
            method="GET", url=url, token=token or self._get_token()
        )
        code, message, user = data.get("code"), data.get(
            "message"), data.get("data")
        if code == 200:
            self._set_current_user(user)
            return user
        else:
            self.options.on_error(code, message)

    def register_by_email(
            self,
            email,
            password,
            profile=None,
            force_login=False,
            generate_token=False,
            client_ip=None,
            custom_data=None,
            context=None
    ):
        """通过邮箱注册

        Args:
            email (str): 邮箱
            password (str): 密码
            profile (dict): 用户资料
            force_login (bool): 强制登录
            generate_token (bool): 自动生成 token
            client_ip (str): 客户端真实 IP
            custom_data (dict): 用户自定义数据
            context (dict): 请求上下文，将会传递到 Pipeline 中
        """
        password = encrypt(password, self.options.enc_public_key)

        params = []
        if custom_data:
            if not isinstance(custom_data, dict):
                raise Exception('custom_data must be a dict')
            for k, v in custom_data.items():
                params.append({
                    'key': k,
                    'value': v
                })
        context = context and json.dumps(context)
        data = self.graphqlClient.request(
            query=QUERY["registerByEmail"],
            params={
                "input": {
                    "email": email,
                    "password": password,
                    "profile": profile,
                    "forceLogin": force_login,
                    "generateToken": generate_token,
                    "clientIp": client_ip,
                    "params": json.dumps(params) if len(params) > 0 else None,
                    "context": context
                }
            },
        )
        user = data["registerByEmail"]
        self._set_current_user(user)
        return user

    def register_by_username(
            self,
            username,
            password,
            profile=None,
            force_login=False,
            generate_token=False,
            client_ip=None,
            custom_data=None,
            context=None
    ):
        """通过用户名注册

        Args:
            username (str): 用户名
            password (str): 密码
            profile (dict): 用户资料
            force_login (bool): 强制登录
            generate_token (bool): 自动生成 token
            client_ip (str): 客户端真实 IP
            custom_data (dict): 用户自定义数据
            context (dict): 请求上下文，将会传递到 Pipeline 中
        """
        password = encrypt(password, self.options.enc_public_key)
        params = []
        if custom_data:
            if not isinstance(custom_data, dict):
                raise Exception('custom_data must be a dict')
            for k, v in custom_data.items():
                params.append({
                    'key': k,
                    'value': v
                })
        context = context and json.dumps(context)
        data = self.graphqlClient.request(
            query=QUERY["registerByUsername"],
            params={
                "input": {
                    "username": username,
                    "password": password,
                    "profile": profile,
                    "forceLogin": force_login,
                    "generateToken": generate_token,
                    "clientIp": client_ip,
                    "params": json.dumps(params) if len(params) > 0 else None,
                    "context": context
                }
            },
        )
        user = data["registerByUsername"]
        self._set_current_user(user)
        return user

    def register_by_phone_code(
            self,
            phone,
            code,
            password=None,
            profile=None,
            force_login=False,
            generate_token=False,
            client_ip=None,
            custom_data=None,
            context=None
    ):
        """通过手机号验证码注册

        Args:
            phone (str): 手机号
            code (str): 手机号验证码
            password (str): 密码
            profile (dict): 用户资料
            force_login (bool): 强制登录
            generate_token (bool): 自动生成 token
            client_ip (str): 客户端真实 IP
            custom_data (dict): 用户自定义数据
            context (dict): 请求上下文，将会传递到 Pipeline 中
        """
        if password:
            password = encrypt(password, self.options.enc_public_key)
        params = []
        if custom_data:
            if not isinstance(custom_data, dict):
                raise Exception('custom_data must be a dict')
            for k, v in custom_data.items():
                params.append({
                    'key': k,
                    'value': v
                })
        context = context and json.dumps(context)
        data = self.graphqlClient.request(
            query=QUERY["registerByPhoneCode"],
            params={
                "input": {
                    "phone": phone,
                    "code": code,
                    "password": password,
                    "profile": profile,
                    "forceLogin": force_login,
                    "generateToken": generate_token,
                    "clientIp": client_ip,
                    "params": json.dumps(params) if len(params) > 0 else None,
                    "context": context
                }
            },
        )
        user = data["registerByPhoneCode"]
        self._set_current_user(user)
        return user

    def send_sms_code(self, phone):
        """发送手机号验证码

        Args:
            phone (str): 手机号
        """
        url = "%s/api/v2/sms/send" % self.options.host
        data = self.restClient.request(
            method="POST", url=url, token=None, json={"phone": phone}
        )
        return data

    def login_by_email(
            self,
            email,
            password,
            auto_register=False,
            captcha_code=None,
            client_ip=None,
            custom_data=None,
            context=None
    ):
        """使用邮箱登录

        Args:
            email (str): 邮箱
            password (str): 密码
            auto_register (bool): 如果用户不存在，是否自动注册。
            captcha_code (str): 图形验证码
            client_ip (str): 客户端真实 IP
            custom_data (dict): 用户自定义数据
            context (dict): 请求上下文，将会传递到 Pipeline 中
        """
        password = encrypt(password, self.options.enc_public_key)
        params = []
        if custom_data:
            if not isinstance(custom_data, dict):
                raise Exception('custom_data must be a dict')
            for k, v in custom_data.items():
                params.append({
                    'key': k,
                    'value': v
                })
        context = context and json.dumps(context)
        data = self.graphqlClient.request(
            query=QUERY["loginByEmail"],
            params={
                "input": {
                    "email": email,
                    "password": password,
                    "autoRegister": auto_register,
                    "captchaCode": captcha_code,
                    "clientIp": client_ip,
                    "params": json.dumps(params) if len(params) > 0 else None,
                    "context": context
                }
            },
        )
        user = data["loginByEmail"]
        self._set_current_user(user)
        return user

    def login_by_username(
            self,
            username,
            password,
            auto_register=False,
            captcha_code=None,
            client_ip=None,
            custom_data=None,
            context=None
    ):
        """使用邮箱登录

        Args:
            username (str): 用户名
            password (str): 密码
            auto_register (bool): 如果用户不存在，是否自动注册。
            captcha_code (str): 图形验证码
            client_ip (str): 客户端真实 IP
            custom_data (dict): 用户自定义数据
            context (dict): 请求上下文，将会传递到 Pipeline 中
        """
        password = encrypt(password, self.options.enc_public_key)
        params = []
        if custom_data:
            if not isinstance(custom_data, dict):
                raise Exception('custom_data must be a dict')
            for k, v in custom_data.items():
                params.append({
                    'key': k,
                    'value': v
                })
        context = context and json.dumps(context)
        data = self.graphqlClient.request(
            query=QUERY["loginByUsername"],
            params={
                "input": {
                    "username": username,
                    "password": password,
                    "autoRegister": auto_register,
                    "captchaCode": captcha_code,
                    "clientIp": client_ip,
                    "params": json.dumps(params) if len(params) > 0 else None,
                    "context": context
                }
            },
        )
        user = data["loginByUsername"]
        self._set_current_user(user)
        return user

    def login_by_phone_code(
            self,
            phone,
            code,
            client_ip=None,
            custom_data=None,
            context=None
        ):
        """使用邮箱登录

        Args:
            phone (str): 手机号
            code (str): 手机号验证码
            client_ip (str): 客户端真实 IP
            custom_data (dict): 用户自定义数据
            context (dict): 请求上下文，将会传递到 Pipeline 中
        """
        params = []
        if custom_data:
            if not isinstance(custom_data, dict):
                raise Exception('custom_data must be a dict')
            for k, v in custom_data.items():
                params.append({
                    'key': k,
                    'value': v
                })
        context = context and json.dumps(context)
        data = self.graphqlClient.request(
            query=QUERY["loginByPhoneCode"],
            params={
                "input": {
                    "phone": phone,
                    "code": code,
                    "clientIp": client_ip,
                    "params": json.dumps(params) if len(params) > 0 else None,
                    "context": context
                }
            },
        )
        user = data["loginByPhoneCode"]
        self._set_current_user(user)
        return user

    def login_by_phone_password(
            self,
            phone,
            password,
            auto_register=False,
            captcha_code=None,
            client_ip=None,
            custom_data=None,
            context=None
    ):
        """使用邮箱登录

        Args:
            phone (str): 手机号
            password (str): 密码
            auto_register (bool): 如果用户不存在，是否自动注册。
            captcha_code (str): 图形验证码
            client_ip (str): 客户端真实 IP
            custom_data (dict): 用户自定义数据
            context (dict): 请求上下文，将会传递到 Pipeline 中
        """
        password = encrypt(password, self.options.enc_public_key)
        params = []
        if custom_data:
            if not isinstance(custom_data, dict):
                raise Exception('custom_data must be a dict')
            for k, v in custom_data.items():
                params.append({
                    'key': k,
                    'value': v
                })
        context = context and json.dumps(context)
        data = self.graphqlClient.request(
            query=QUERY["loginByPhonePassword"],
            params={
                "input": {
                    "phone": phone,
                    "password": password,
                    "autoRegister": auto_register,
                    "captchaCode": captcha_code,
                    "clientIp": client_ip,
                    "params": json.dumps(params) if len(params) > 0 else None,
                    "context": context
                }
            },
        )
        user = data["loginByPhonePassword"]
        self._set_current_user(user)
        return user

    def login_by_ldap(self, username, password):
        """使用 LDAP 身份源账号登录

        Args:
            username: (str): LDAP 用户名
            password: (str): LDAP 账号密码
        """

        url = "%s/api/v2/ldap/verify-user" % self.options.host
        data = self.restClient.request(
            method="POST", url=url, json={
                'username': username,
                'password': password
            }
        )
        code, message, user = data.get("code"), data.get(
            "message"), data.get("data")
        if code == 200:
            self._set_current_user(user)
            return user
        else:
            self.options.on_error(code, message)

    def login_by_ad(self, username, password):
        """
        使用 AD 身份源账号登录

        Args:
            username: (str): AD 用户名
            password: (str): AD 账号密码
        """
        hostname = get_hostname_from_url(self.options.host)
        first_level_domain = '.'.join(hostname.split('.')[1:]) if len(hostname.split('.')) > 2 else hostname
        websocket_host = self.options.websocket_host or "https://ws.%s" % first_level_domain
        url = "%s/api/v2/ad/verify-user" % websocket_host
        data = self.restClient.request(
            method="POST", url=url, json={
                'username': username,
                'password': password
            }
        )
        code, message, user = data.get("code"), data.get(
            "message"), data.get("data")
        if code == 200:
            self._set_current_user(user)
            return user
        else:
            self.options.on_error(code, message)

    def check_password_strength(self, password):
        """检查密码强度，详情请见 https://docs.authing.co/v2/guides/security/config-password.html"""
        data = self.graphqlClient.request(
            query=QUERY['checkPasswordStrength'],
            params={
                'password': password
            }
        )
        return data['checkPasswordStrength']

    def check_login_status(self, token=None):
        """检查 token 的登录状态

        Args:
            token (str): token
        """
        data = self.graphqlClient.request(
            query=QUERY["checkLoginStatus"], params={
                "token": token or self._token}
        )
        return data["checkLoginStatus"]

    def send_email(self, email, scene):
        """发送邮件"""
        data = self.graphqlClient.request(
            query=QUERY["sendEmail"], params={"email": email, "scene": scene}
        )
        return data["sendEmail"]

    def reset_password_by_phone_code(self, phone, code, new_password):
        """通过手机号验证码重置密码

        Args:
            phone (str): 手机号
            code (str): 手机号验证码
            new_password (str): 新的密码
        """
        new_password = encrypt(new_password, self.options.enc_public_key)
        data = self.graphqlClient.request(
            query=QUERY["resetPassword"],
            params={"phone": phone, "code": code, "newPassword": new_password},
        )
        return data["resetPassword"]

    def reset_password_by_email_code(self, email, code, new_password):
        """通过邮件验证码修改密码

        Args:
            email (str): 邮箱
            code (str): 邮箱验证码
            new_password (str): 新的密码
        """
        new_password = encrypt(new_password, self.options.enc_public_key)
        data = self.graphqlClient.request(
            query=QUERY["resetPassword"],
            params={"email": email, "code": code, "newPassword": new_password},
        )
        return data["resetPassword"]

    def update_profile(self, updates):
        """修改用户资料"""
        user = self._check_logged_in()
        data = self.graphqlClient.request(
            query=QUERY["updateUser"],
            params={"id": user["id"], "input": updates},
            token=self._get_token(),
        )
        user = data["updateUser"]
        self._set_current_user(user)
        return user

    def update_password(self, new_password, old_password):
        """修改密码

        Args:
            new_password (str): 新密码
            old_password (str): 老密码
        """
        new_password = encrypt(new_password, self.options.enc_public_key)
        old_password = encrypt(old_password, self.options.enc_public_key)
        data = self.graphqlClient.request(
            query=QUERY["updatePassword"],
            params={"newPassword": new_password, "oldPassword": old_password},
            token=self._get_token(),
        )
        user = data["updatePassword"]
        return user

    def update_phone(self, phone, phone_code, old_phone=None, old_phone_code=None):
        """
        更新用户手机号。和修改邮箱一样，默认情况下，如果用户当前已经绑定了手机号，需要同时验证原有手机号（目前账号绑定的手机号）和当前邮箱（将要绑定的手机号）。'
        也就是说，用户 A 当前绑定的手机号为 15888888888，想修改为 15899999999，那么就需要同时验证这两个手机号。
        开发者也可以选择不开启 “验证原有手机号“ ，可以在 Authing 控制台的设置目录下的安全信息模块进行关闭。
        用户首次绑定手机号请使用 bind_phone 接口。

        Args:
            phone (str): 新手机号
            phone_code (str): 新手机号的验证码
            old_phone (str): 原手机号
            old_phone_code (str): 原手机号验证码
        """
        data = self.graphqlClient.request(
            query=QUERY["updatePhone"],
            params={
                "phone": phone,
                "phoneCode": phone_code,
                "oldPhone": old_phone,
                "oldPhoneCode": old_phone_code,
            },
            token=self._get_token(),
        )
        user = data["updatePhone"]
        self._set_current_user(user)
        return user

    def update_email(self, email, email_code, old_email=None, old_email_code=None):
        """
        如果用户已经绑定了邮箱，默认情况下，需要同时验证原有邮箱（目前账号绑定的邮箱）和当前邮箱（将要绑定的邮箱）。
        也就是说，用户 A 当前绑定的邮箱为 123456@qq.com，想修改为 1234567@qq.com，那么就需要同时验证这两个邮箱。
        开发者也可以选择不开启 “验证原有邮箱“ ，可以在 Authing 控制台的设置目录下的安全信息模块进行关闭。

        用户首次绑定邮箱请使用 bind_email 接口。

        Args:
            email (str): 新邮箱
            email_code (str): 新邮箱的验证码
            old_email (str): 原邮箱
            old_email_code (str): 原邮箱验证码
        """
        data = self.graphqlClient.request(
            query=QUERY["updateEmail"],
            params={
                "email": email,
                "emailCode": email_code,
                "oldEmail": old_email,
                "oldEmailCode": old_email_code,
            },
            token=self._get_token(),
        )
        user = data["updatePhone"]
        self._set_current_user(user)
        return user

    def link_account(self, primary_user_token, secondary_user_token):
        """绑定账号。将一个社交账号（如微信账号、GitHub 账号）绑定到一个主账号（手机号、邮箱账号）。

        Args:
            primary_user_token (str): 主账号的 Token
            secondary_user_token (str): 社交账号 Token
        """
        url = "%s/api/v2/users/link" % self.options.host
        self.restClient.request(
            method="POST", url=url, token=self._get_token(), json={
                'primaryUserToken': primary_user_token,
                'secondaryUserToken': secondary_user_token
            }
        )
        return True

    def unlink_account(self, primary_user_token, provider):
        """"主账号解绑社会化登录账号。

        Args:
            primary_user_token (str): 主账号的 Token
            provider (str): 社会化登录类型
        """
        url = "%s/api/v2/users/unlink" % self.options.host
        self.restClient.request(
            method="POST", url=url, token=self._get_token(), json={
                'primaryUserToken': primary_user_token,
                'provider': provider
            }
        )
        return True

    def refresh_token(self, token=None):
        """刷新 token

        Returns:
            [type]: [description]
        """
        data = self.graphqlClient.request(
            query=QUERY["refreshToken"], params={}, token=token or self._get_token()
        )
        token = data["refreshToken"].get("token")
        self._set_token(token)
        return data["refreshToken"]

    def bind_phone(self, phone, phone_code):
        """
        用户初次绑定手机号，如果需要修改手机号请使用 updatePhone 方法。
        如果该手机号已被绑定，将会绑定失败。
        发送验证码请使用 send_sms_code 方法。

        Args:
            phone (str): 手机号
            phone_code (str): 手机号验证码
        """
        data = self.graphqlClient.request(
            query=QUERY["bindPhone"],
            params={"phone": phone, "phoneCode": phone_code},
            token=self._get_token(),
        )
        user = data["bindPhone"]
        self._set_current_user(user)
        return user

    def unbind_phone(self):
        """用户解绑手机号，如果用户没有绑定其他登录方式（邮箱、社会化登录账号），将无法解绑手机号，会提示错误。"""
        data = self.graphqlClient.request(
            query=QUERY["unbindPhone"], params={}, token=self._get_token()
        )
        user = data["unbindPhone"]
        self._set_current_user(user)
        return user

    def bind_email(self, email, email_code):
        """
        用于用户初次绑定邮箱，需检验邮箱验证码。
        如果需要修改邮箱请使用 update_email 方法。
        如果该邮箱已被绑定，将会绑定失败。发送邮件验证码请使用 send_email 方法。

        Args:
            email (str): 邮箱
            email_code (str): 邮箱验证码
        """
        data = self.graphqlClient.request(
            query=QUERY["bindEmail"], params={
                "email": email,
                "emailCode": email_code
            }, token=self._get_token()
        )
        user = data["bindEmail"]
        self._set_current_user(user)
        return user

    def unbind_email(self):
        """用户解绑邮箱，如果用户没有绑定其他登录方式（手机号、社会化登录账号），将无法解绑邮箱，会提示错误。"""
        data = self.graphqlClient.request(
            query=QUERY["unbindEmail"], params={
            }, token=self._get_token()
        )
        user = data["unbindEmail"]
        self._set_current_user(user)
        return user

    def get_udf_value(self):
        """获取当前用户的自定义用户数据"""
        user = self._check_logged_in()
        data = self.graphqlClient.request(
            query=QUERY["udv"],
            params={"targetType": "USER", "targetId": user["id"]},
            token=self._get_token(),
        )
        data = data['udv']
        return convert_udv_list_to_dict(data)

    def set_udf_value(self, data):
        """
        设置用户的自定义字段。
        你需要先在用户池定义用户自定义数据元信息，且传入值的类型必须和定义的类型匹配。
        如果设置失败，会抛出异常，你需要对异常进行捕捉。

        Args:
            data (dict): 自定义数据
        """
        user = self._check_logged_in()
        if len(data.keys()) == 0:
            raise AuthingWrongArgumentException('data must not be a empty dict')
        list = []
        for k, v in data.items():
            if isinstance(v, datetime.datetime):
                def default(o):
                    if isinstance(o, (datetime.date, datetime.datetime)):
                        return o.isoformat()

                v = json.dumps(v, sort_keys=True,
                               indent=1, default=default)
            else:
                v = json.dumps(v)
            list.append({
                'key': k,
                'value': v
            })
        self.graphqlClient.request(
            query=QUERY['setUdvBatch'],
            params={
                'targetType': 'USER',
                'targetId': user['id'],
                'udvList': list
            },
            token=self._get_token()
        )
        return True

    def remove_udf_value(self, key):
        """
        删除自定义数据。

        Args:
            key (str): 自定义字段 key
        """
        user = self._check_logged_in()
        self.graphqlClient.request(
            query=QUERY['removeUdv'],
            params={
                'targetType': 'USER',
                'targetId': user['id'],
                'key': key
            },
            token=self._get_token()
        )
        return True

    def list_udv(self):
        """【已废弃，请使用 get_udf_vale】获取当前用户的自定义用户数据"""
        user = self._check_logged_in()
        data = self.graphqlClient.request(
            query=QUERY["udv"],
            params={"targetType": "USER", "targetId": user["id"]},
            token=self._get_token(),
        )
        data = data["udv"]
        return convert_udv_data_type(data)

    def set_udv(self, key, value):
        """设置自定义用户数据

        Args:
            key (type): key
            value (type): value
        """
        user = self._check_logged_in()
        if isinstance(value, datetime.datetime):

            def default(o):
                if isinstance(o, (datetime.date, datetime.datetime)):
                    return o.isoformat()

            value = json.dumps(value, sort_keys=True,
                               indent=1, default=default)
        else:
            value = json.dumps(value)
        data = self.graphqlClient.request(
            query=QUERY["setUdv"],
            params={
                "targetType": "USER",
                "targetId": user["id"],
                "key": key,
                "value": value,
            },
            token=self._get_token(),
        )
        data = data["setUdv"]
        return convert_udv_data_type(data)

    def remove_udv(self, key):
        """删除用户自定义字段数据

        Args:
            key (str): 自定义字段 key
        """
        user = self._check_logged_in()
        data = self.graphqlClient.request(
            query=QUERY["removeUdv"],
            params={
                "targetType": "USER",
                "targetId": user["id"],
                "key": key,
            },
            token=self._get_token(),
        )
        data = data["removeUdv"]
        return convert_udv_data_type(data)

    def logout(self):
        """ 用户退出登录。
        1. 清空该用户在当前应用下的 session 会话信息；
        2. 将用户当前的 id_token 标记为已失效，使用此 id_token将调用 Authing 接口无法获取到相关数据。
        """
        self._check_logged_in()
        url = "%s/api/v2/logout?app_id=%s" % (self.options.host, self.options.app_id)
        self.restClient.request(
            method="GET", url=url, token=self._get_token()
        )
        self._clear_current_user()
        return True

    def list_orgs(self):
        """
        获取用户所在组织机构列表
        """
        url = "%s/api/v2/users/me/orgs" % self.options.host
        data = self.restClient.request(
            method="GET",
            url=url,
            token=self._get_token()
        )
        code, message, data = data.get("code"), data.get(
            "message"), data.get("data")
        if code == 200:
            return data
        else:
            self.options.on_error(code, message)

    def get_security_level(self):
        """
        获取用户账号安全等级。
        """
        url = "%s/api/v2/users/me/security-level" % self.options.host
        data = self.restClient.request(
            method='GET',
            url=url,
            token=self._get_token()
        )
        code, message, data = data.get("code"), data.get(
            "message"), data.get("data")
        if code == 200:
            return data
        else:
            self.options.on_error(code, message)

    def list_roles(self, namespace=None):
        """
        获取用户拥有的角色列表

        Args:
            namespace (str): 权限分组的 code，默认为
             - 默认权限分组
        """
        user = self._check_logged_in()
        data = self.graphqlClient.request(
            query=QUERY["getUserRoles"],
            params={
                "id": user['id'],
                "namespace": namespace
            },
            token=self._get_token()
        )
        res = data["user"]["roles"]
        return res

    def has_role(self, code, namespace=None):
        """判断用户是否具有某在角色

        Args:
            code (str): 角色的唯一标志符 code
            namespace (str): 权限分组的 code，默认为 default - 默认权限分组
        """
        data = self.list_roles(namespace)
        _list, total_count = data['list'], data['totalCount']

        if total_count == 0:
            return False

        has_role = False
        for item in _list:
            if item.get('code') == code:
                has_role = True
        return has_role

    def list_applications(self, page=1, limit=10):
        """
        获取用户能够访问的应用列表

        Args:
            page (int) 页数，从 1 开始，默认为 1
            limit (int) 每页个数，默认为 10
        """
        url = "%s/api/v2/users/me/applications/allowed?page=%s&limit=%s" % (self.options.host, page, limit)
        data = self.restClient.request(
            method="GET",
            url=url,
            token=self._get_token()
        )
        code, message, data = data.get("code"), data.get(
            "message"), data.get("data")
        if code == 200:
            return data
        else:
            self.options.on_error(code, message)

    def list_authorized_resources(self, namespace, resource_type=None):
        """
        获取一个用户被授权的所有资源，用户被授权的所有资源里面包括从角色、分组、组织机构继承的资源。

        Args:
            namespace (str) 权限分组的 code
            resource_type (str) 资源类型，可选值包含 DATA、API、MENU、UI、BUTTON
        """

        user = self._check_logged_in()
        valid_resource_types = [
            'DATA',
            'API',
            'MENU',
            'UI',
            'BUTTON'
        ]
        if not valid_resource_types.index(resource_type):
            raise AuthingWrongArgumentException('invalid argument: resource_type')
        data = self.graphqlClient.request(
            query=QUERY['listUserAuthorizedResources'],
            params={
                'id': user.get('id'),
                'namespace': namespace,
                'resourceType': resource_type
            }
        )
        data = data.get('user')
        if not data:
            raise AuthingException(500, 'user not exists')

        authorized_resources = data.get('authorizedResources')
        _list, total_count = authorized_resources.get('list'), authorized_resources.get('totalCount')
        _list = format_authorized_resources(_list)
        return {
            'totalCount': total_count,
            'list': _list
        }

    def compute_password_security_level(self, password):
        """
        计算密码安全等级。

        Args:
            password (str) 明文密码
        """
        high_level_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^]{12,}$"
        middle_level_regex = r"^(?=.*[a-zA-Z])(?=.*\d)[^]{8,}$"
        if re.match(high_level_regex, password):
            return 1

    def ___get_access_token_by_code_with_client_secret_post(self, code, code_verifier=None):
        url = "%s/%s/token" % (self.options.host, 'oidc' if self.options.protocol == 'oidc' else 'oauth')
        data = self.restClient.request(
            method='POST',
            url=url,
            data={
                'client_id': self.options.app_id,
                'client_secret': self.options.secret,
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': self.options.redirect_uri,
                'code_verifier': code_verifier
            }
        )
        return data

    def ___get_access_token_by_code_with_client_secret_basic(self, code, code_verifier=None):
        url = "%s/%s/token" % (self.options.host, 'oidc' if self.options.protocol == 'oidc' else 'oauth')
        data = self.restClient.request(
            method='POST',
            url=url,
            data={
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': self.options.redirect_uri,
                'code_verifier': code_verifier
            },
            basic_token=base64.b64encode(('%s:%s' % (self.options.app_id, self.options.secret)).encode()).decode()
        )
        return data

    def __get_access_token_by_code_with_none(self, code, code_verifier=None):
        url = "%s/%s/token" % (self.options.host, 'oidc' if self.options.protocol == 'oidc' else 'oauth')
        data = self.restClient.request(
            method='POST',
            url=url,
            data={
                'client_id': self.options.app_id,
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': self.options.redirect_uri,
                'code_verifier': code_verifier
            }
        )
        return data

    def get_access_token_by_code(self, code, code_verifier=None):
        """
        使用授权码 Code 获取用户的 Token 信息。

        Args:
            code (str): 授权码 Code，用户在认证成功后，Authing 会将授权码 Code 发送到回调地址。
            code_verifier (str): 发起 PKCE 授权登录时需要填写此参数。
        """

        if self.options.protocol not in ['oidc', 'oauth']:
            raise AuthingWrongArgumentException('argument protocol must be oidc or oauth')

        if not self.options.redirect_uri:
            raise AuthingWrongArgumentException('argument redirect_uri must be oidc or oauth')

        if not self.options.secret and self.options.token_endpoint_auth_method != 'none':
            raise AuthingWrongArgumentException('argument secret must be provided')

        if self.options.token_endpoint_auth_method == 'client_secret_post':
            return self.___get_access_token_by_code_with_client_secret_post(code, code_verifier)

        elif self.options.token_endpoint_auth_method == 'client_secret_basic':
            return self.___get_access_token_by_code_with_client_secret_basic(code, code_verifier)

        elif self.options.token_endpoint_auth_method == 'none':
            return self.__get_access_token_by_code_with_none(code, code_verifier)

        raise AuthingWrongArgumentException(
            'unsupported argument token_endpoint_auth_method, must be client_secret_post, client_secret_basic or none')

    def get_access_token_by_client_credentials(self, scope, access_key, access_secret):
        """
        使用编程访问账号获取具备权限的 Access Token。

        Args:
            scope (str): 权限项目，空格分隔的字符串，每一项代表一个权限。
            access_key (str): 编程访问账号 AccessKey
            access_secret (str): 编程访问账号 SecretKey
        """

        if not scope:
            raise AuthingWrongArgumentException(
                'must provide scope argument, see doc here: '
                'https://docs.authing.cn/v2/guides/authorization/m2m-authz.html')

        url = "%s/%s/token" % (self.options.host, 'oidc' if self.options.protocol == 'oidc' else 'oauth')
        data = self.restClient.request(
            method='POST',
            url=url,
            data={
                'client_id': access_key,
                'client_secret': access_secret,
                'grant_type': 'client_credentials',
                'scope': scope
            }
        )
        return data

    def get_user_info_by_access_token(self, access_token):
        """
        使用 Access token 获取用户信息。

        Args:
            access_token (str) Access token，使用授权码 Code 换取的 Access token 的内容。
        """
        url = "%s/%s/me" % (self.options.host, 'oidc' if self.options.protocol == 'oidc' else 'oauth')

        data = self.restClient.request(
            method='POST',
            url=url,
            token=access_token
        )
        return data

    def __build_saml_authorize_url(self):
        return "%s/api/v2/saml-idp/%s" % (self.options.app_host, self.options.app_id)

    def __build_cas_authorize_url(self, service=None):
        if service:
            return "%s/cas-idp/%s?service=%s" % (self.options.app_host, self.options.app_id, service)
        else:
            return "%s/cas-idp/%s?service" % (self.options.app_host, self.options.app_id)

    def __build_oauth_authorize_url(self, scope=None, redirect_uri=None, state=None, response_type=None):
        res = {
            'state': get_random_string(10),
            'scope': 'user',
            'client_id': self.options.app_id,
            'redirect_uri': self.options.redirect_uri,
            'response_type': 'code'
        }
        if scope:
            res['scope'] = scope

        if redirect_uri:
            res['redirect_uri'] = redirect_uri

        if state:
            res['state'] = state

        if response_type:
            if response_type not in ['code', 'token']:
                raise AuthingWrongArgumentException('response_type must be code or token')
            res['response_type'] = response_type

        return url_join_args('%s/oauth/auth' % self.options.app_host, res)

    def __build_oidc_authorize_url(self, redirect_uri=None, response_type=None, response_mode=None,
                                   state=None, nonce=None, scope=None,
                                   code_challenge_method=None, code_challenge=None):
        """
        生成 OIDC 协议的用户登录地址。

        Args:
            redirect_uri (str): 回调地址，选填，默认为 SDK 初始化时的 redirectUri 参数。
            response_type (str): 响应类型，选填，可选值为 code、code id_token token、code id_token、code id_token、code token、id_token token、id_token、none；默认为 code，授权码模式。
            response_mode (str):  响应类型，选填，可选值为 query、fragment、form_post；默认为 query，即通过浏览器重定向发送 code 到回调地址。
            state (str): 随机字符串，选填，默认自动生成。
            nonce (str): 随机字符串，选填，默认自动生成。
            scope (str): 请求的权限项目，选填，OIDC 协议默认为 openid profile email phone address，OAuth 2.0 协议默认为 user。
            code_challenge_method (str): 可以为 plain、S256，表示计算 code_challenge 时使用的摘要算法，plain 表示不用任何算法，S256 表示 code_challenge 是使用 SHA256 计算的。
            code_challenge (str): 一个长度大于等于 43 的字符串，作为 code_challenge 发送到 Authing。
        """
        res = {
            'nonce': get_random_string(10),
            'state': get_random_string(10),
            'scope': 'openid profile email phone address',
            'client_id': self.options.app_id,
            'redirect_uri': self.options.redirect_uri,
            'response_type': 'code'
        }

        if redirect_uri:
            res['redirect_uri'] = redirect_uri

        if response_type:
            res['response_type'] = response_type

        if response_mode:
            res['response_mode'] = response_mode

        if state:
            res['state'] = state

        if scope:
            res['scope'] = scope
            if 'offline_access' in scope:
                res['prompt'] = 'consent'

        if nonce:
            res['nonce'] = nonce

        if code_challenge:
            res['code_challenge'] = code_challenge

        if code_challenge_method:
            res['code_challenge_method'] = code_challenge_method

        return url_join_args('%s/oidc/auth' % self.options.app_host, res)

    def build_authorize_url(
            self,
            redirect_uri=None,
            response_type=None,
            response_mode=None,
            state=None,
            nonce=None,
            scope=None,
            code_challenge_method=None,
            code_challenge=None,
            service=None
    ):
        """
        生成用于用户登录的地址链接。
        """
        if not self.options.app_host:
            raise AuthingWrongArgumentException('must provider app_host when you init AuthenticationClient')

        if self.options.protocol == 'oidc':
            return self.__build_oidc_authorize_url(
                response_mode=response_mode,
                response_type=response_type,
                redirect_uri=redirect_uri,
                state=state,
                nonce=nonce,
                scope=scope,
                code_challenge=code_challenge,
                code_challenge_method=code_challenge_method
            )
        elif self.options.protocol == 'oauth':
            return self.__build_oauth_authorize_url(
                scope=scope,
                redirect_uri=redirect_uri,
                state=state,
                response_type=response_type
            )
        elif self.options.protocol == 'saml':
            return self.__build_saml_authorize_url()

        elif self.options.protocol == 'cas':
            return self.__build_cas_authorize_url(service=service)

        else:
            raise AuthingWrongArgumentException('protocol must be oidc oauth saml or cas')

    def generate_code_challenge(self, length=43):
        """
        生成一个 PKCE 校验码，长度必须大于等于 43。

        Args:
            length (int): 校验码长度，默认为 43。
        """
        if not isinstance(length, int):
            raise AuthingWrongArgumentException('length must be a int')

        if length < 43:
            raise AuthingWrongArgumentException('length must be grater than 43')

        return get_random_string(length)

    def generate_code_challenge_digest(self, code_challenge, method=None):
        """
        生成一个 PKCE 校验码摘要值。

        Args:
            code_challenge (str): 待生成摘要值的 code_challenge 原始值，一个长度大于等于 43 的随机字符串。
            method (str): 可以为 plain、S256，表示计算 code_challenge 时使用的摘要算法，plain 表示不用任何算法原样返回，S256 表示使用 SHA256 计算 code_challenge 摘要。
        """
        if len(code_challenge) < 43:
            raise AuthingWrongArgumentException('code_challenge must be a string length grater than 43')

        if not method:
            method = 'S256'

        if method not in ['S256', 'plain']:
            raise AuthingWrongArgumentException('method must be S256 or plain')

        if method == 'S256':
            code_challenge = hashlib.sha256(code_challenge.encode('utf-8')).digest()
            code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8')
            code_challenge = code_challenge.replace('=', '')
            return code_challenge

        elif method == 'plain':
            return code_challenge

        else:
            raise AuthingWrongArgumentException('unsupported method, must be S256 or plain')

    def __build_oidc_logout_url(self, redirect_uri=None, id_token=None):
        if redirect_uri:
            return "%s/oidc/session/end?id_token_hint=%s&post_logout_redirect_uri=%s" % (
                self.options.app_host,
                id_token,
                redirect_uri
            )
        else:
            return "%s/oidc/session/end" % self.options.app_host

    def __build_easy_logout_url(self, redirect_uri=None):
        if redirect_uri:
            return "%s/login/profile/logout?redirect_uri=%s" % (
                self.options.app_host,
                redirect_uri
            )
        else:
            return "%s/login/profile/logout" % (
                self.options.app_host
            )

    def __build_cas_logout_url(self, redirect_uri=None):
        if redirect_uri:
            return "%s/cas-idp/logout?url=%s" % (
                self.options.app_host,
                redirect_uri
            )
        else:
            return "%s/cas-idp/logout" % (
                self.options.app_host
            )

    def build_logout_url(self, expert=None, redirect_uri=None, id_token=None):
        """拼接登出 URL。"""
        if not self.options.app_host:
            raise AuthingWrongArgumentException('must provider app_host when you init AuthenticationClient')

        if self.options.protocol == 'oidc':
            if not expert:
                return self.__build_easy_logout_url(redirect_uri)
            else:
                return self.__build_oidc_logout_url(
                    id_token=id_token,
                    redirect_uri=redirect_uri
                )
        elif self.options.protocol == 'cas':
            return self.__build_cas_logout_url(redirect_uri=redirect_uri)

    def __get_new_access_token_by_refresh_token_with_client_secret_post(self, refresh_token):
        url = "%s/%s/token" % (self.options.host, 'oidc' if self.options.protocol == 'oidc' else 'oauth')
        data = self.restClient.request(
            method='POST',
            url=url,
            data={
                'client_id': self.options.app_id,
                'client_secret': self.options.secret,
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token
            }
        )
        return data

    def __get_new_access_token_by_refresh_token_with_client_secret_basic(self, refresh_token):
        url = "%s/%s/token" % (self.options.host, 'oidc' if self.options.protocol == 'oidc' else 'oauth')
        data = self.restClient.request(
            method='POST',
            url=url,
            data={
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token
            },
            basic_token=base64.b64encode(('%s:%s' % (self.options.app_id, self.options.secret)).encode()).decode()
        )
        return data

    def __get_new_access_token_by_refresh_token_with_none(self, refresh_token):
        url = "%s/%s/token" % (self.options.host, 'oidc' if self.options.protocol == 'oidc' else 'oauth')
        data = self.restClient.request(
            method='POST',
            url=url,
            data={
                'client_id': self.options.app_id,
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token
            }
        )
        return data

    def get_new_access_token_by_refresh_token(self, refresh_token):
        """
        使用 Refresh token 获取新的 Access token。

        Args:
            refresh_token (str): Refresh token，可以从 AuthenticationClient.get_access_token_by_code 方法的返回值中的 refresh_token 获得。
                                注意: refresh_token 只有在 scope 中包含 offline_access 才会返回。

        """
        if self.options.protocol not in ['oauth', 'oidc']:
            raise AuthingWrongArgumentException('protocol must be oauth or oidc')

        if not self.options.secret and self.options.token_endpoint_auth_method != 'none':
            raise AuthingWrongArgumentException('secret must be provided')

        if self.options.token_endpoint_auth_method == 'client_secret_post':
            return self.__get_new_access_token_by_refresh_token_with_client_secret_post(refresh_token)
        elif self.options.token_endpoint_auth_method == 'client_secret_basic':
            return self.__get_new_access_token_by_refresh_token_with_client_secret_basic(refresh_token)
        elif self.options.token_endpoint_auth_method == 'none':
            return self.__get_new_access_token_by_refresh_token_with_none(refresh_token)
        else:
            raise AuthingWrongArgumentException('unsupported argument token_endpoint_auth_method')

    def __revoke_token_with_client_secret_post(self, token):
        url = "%s/%s/token/revocation" % (self.options.host, 'oidc' if self.options.protocol == 'oidc' else 'oauth')
        return self.restClient.request(
            method='POST',
            url=url,
            data={
                'client_id': self.options.app_id,
                'client_secret': self.options.secret,
                'token': token
            }
        )

    def __revoke_token_with_client_secret_basic(self, token):
        url = "%s/%s/token/revocation" % (self.options.host, 'oidc' if self.options.protocol == 'oidc' else 'oauth')
        return self.restClient.request(
            method='POST',
            url=url,
            data={
                'token': token
            },
            basic_token=base64.b64encode(('%s:%s' % (self.options.app_id, self.options.secret)).encode()).decode()
        )

    def __revoke_token_with_none(self, token):
        url = "%s/%s/token/revocation" % (self.options.host, 'oidc' if self.options.protocol == 'oidc' else 'oauth')
        return self.restClient.request(
            method='POST',
            url=url,
            data={
                'client_id': self.options.app_id,
                'token': token
            }
        )

    def revoke_token(self, token):
        """
        撤回 Access token 或 Refresh token。Access token 或 Refresh token 的持有者可以通知 Authing 已经不再需要令牌，希望 Authing 将其吊销。

        Args:
            token (str): Access token 或 Refresh token，可以从 AuthenticationClient.get_access_token_by_code 方法的返回值中的 access_token、refresh_token 获得。
                        注意: refresh_token 只有在 scope 中包含 offline_access 才会返回。
        """
        if self.options.protocol not in ['oauth', 'oidc']:
            raise AuthingWrongArgumentException('protocol must be oauth or oidc')

        if not self.options.secret and self.options.revocation_endpoint_auth_method != 'none':
            raise AuthingWrongArgumentException('secret must be provided')

        if self.options.revocation_endpoint_auth_method == 'client_secret_post':
            return self.__revoke_token_with_client_secret_post(token)

        elif self.options.revocation_endpoint_auth_method == 'client_secret_basic':
            return self.__revoke_token_with_client_secret_basic(token)

        elif self.options.revocation_endpoint_auth_method == 'none':
            return self.__revoke_token_with_none(token)

        else:
            raise AuthingWrongArgumentException('unsupported argument token_endpoint_auth_method')

    def __introspect_token_with_client_secret_post(self, token):
        url = "%s/%s/token/introspection" % (self.options.host, 'oidc' if self.options.protocol == 'oidc' else 'oauth')
        return self.restClient.request(
            method='POST',
            url=url,
            data={
                'client_id': self.options.app_id,
                'client_secret': self.options.secret,
                'token': token
            }
        )

    def __introspect_token_with_client_secret_basic(self, token):
        url = "%s/%s/token/introspection" % (self.options.host, 'oidc' if self.options.protocol == 'oidc' else 'oauth')
        return self.restClient.request(
            method='POST',
            url=url,
            data={
                'token': token
            },
            basic_token=base64.b64encode(('%s:%s' % (self.options.app_id, self.options.secret)).encode()).decode()
        )

    def __introspect_token_with_none(self, token):
        url = "%s/%s/token/introspection" % (self.options.host, 'oidc' if self.options.protocol == 'oidc' else 'oauth')
        return self.restClient.request(
            method='POST',
            url=url,
            data={
                'client_id': self.options.app_id,
                'token': token
            }
        )

    def introspect_token(self, token):
        """
        检查 Access token 或 Refresh token 的状态。

        Args:
            token (str): Access token 或 Refresh token，可以从 AuthenticationClient.get_access_token_by_code 方法的返回值中的 access_token、refresh_token 获得。
                        注意: refresh_token 只有在 scope 中包含 offline_access 才会返回。
        """
        if self.options.protocol not in ['oauth', 'oidc']:
            raise AuthingWrongArgumentException('protocol must be oauth or oidc')

        if not self.options.secret and self.options.introspection_endpoint_auth_method != 'none':
            raise AuthingWrongArgumentException('secret must be provided')

        if self.options.introspection_endpoint_auth_method == 'client_secret_post':
            return self.__introspect_token_with_client_secret_post(token)

        elif self.options.introspection_endpoint_auth_method == 'client_secret_basic':
            return self.__introspect_token_with_client_secret_basic(token)

        elif self.options.introspection_endpoint_auth_method == 'none':
            return self.__introspect_token_with_none(token)

        else:
            raise AuthingWrongArgumentException('unsupported argument token_endpoint_auth_method')

    def __validate_id_token(self, id_token):
        url = "%s/api/v2/oidc/validate_token?id_token=%s" % (self.options.app_host, id_token)
        return self.restClient.request(
            method='GET',
            url=url,
        )

    def __validate_access_token(self, access_token):
        url = "%s/api/v2/oidc/validate_token?access_token=%s" % (self.options.app_host, access_token)
        return self.restClient.request(
            method='GET',
            url=url,
        )

    def validate_token(self, id_token=None, access_token=None):
        """
        通过 Authing 提供的在线接口验证 Id token 或 Access token。会产生网络请求。

        Args:
            id_token (str):
            access_token (str): Access token，可以从 AuthenticationClient.get_access_token_by_code 方法的返回值中的 access_token 获得。
        """

        if not access_token and not id_token:
            raise AuthingWrongArgumentException('must provide id_token or access_token')

        if id_token:
            return self.__validate_id_token(id_token)
        elif access_token:
            return self.__validate_access_token(access_token)

    def validate_ticket_v1(self, ticket, service):
        """
        检验 CAS 1.0 Ticket 合法性。

        Args:
            ticket (str): CAS 认证成功后，Authing 颁发的 ticket。
            service (str): CAS 回调地址。
        """
        url = '%s/cas-idp/%s/validate?service=%s&ticket=%s' % (self.options.app_host, self.options.app_id, service, ticket)
        data = self.restClient.request(
            method='GET',
            url=url
        )
        raw_valid, username = data.split('\n')
        valid = raw_valid == 'yes'
        res = {
            'valid': valid
        }
        if username:
            res['username'] = username
        if not valid:
            res['message'] = 'ticket is not valid'
