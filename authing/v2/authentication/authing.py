# coding: utf-8

from ..common.rest import RestClient
from .types import AuthenticationClientOptions
from ..common.graphql import GraphqlClient
from ..common.utils import encrypt, convert_udv_data_type, convert_udv_list_to_dict, get_hostname_from_url
from ..common.codegen import QUERY
import json
import datetime


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
            token (str, optional): 用户登录凭证
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
            profile ([type], optional): 用户资料
            force_login (bool, optional): 强制登录
            generate_token ([bool], optional): 自动生成 token
            client_ip ([str], optional): 客户端真实 IP
            custom_data ([dict], optional): 用户自定义数据
            context ([dict], optional): 请求上下文，将会传递到 Pipeline 中
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
            profile ([type], optional): 用户资料
            force_login (bool, optional): 强制登录
            generate_token ([type], optional): 自动生成 token
            client_ip ([str], optional): 客户端真实 IP
            custom_data ([dict], optional): 用户自定义数据
            context ([dict], optional): 请求上下文，将会传递到 Pipeline 中
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
            profile ([type], optional): 用户资料
            force_login (bool, optional): 强制登录
            generate_token ([type], optional): 自动生成 token
            client_ip ([str], optional): 客户端真实 IP
            custom_data ([dict], optional): 用户自定义数据
            context ([dict], optional): 请求上下文，将会传递到 Pipeline 中
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
            self, email, password, auto_register=False, captcha_code=None, client_ip=None,

            custom_data=None,
            context=None
    ):
        """使用邮箱登录

        Args:
            email (str): 邮箱
            password (str): 密码
            auto_register (bool, optional): 如果用户不存在，是否自动注册。
            captcha_code (str, optional): 图形验证码
            client_ip ([str], optional): 客户端真实 IP
            custom_data ([dict], optional): 用户自定义数据
            context ([dict], optional): 请求上下文，将会传递到 Pipeline 中
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
            self, username, password, auto_register=False, captcha_code=None, client_ip=None,
            custom_data=None,
            context=None
    ):
        """使用邮箱登录

        Args:
            username (str): 用户名
            password (str): 密码
            auto_register (bool, optional): 如果用户不存在，是否自动注册。
            captcha_code (str, optional): 图形验证码
            client_ip ([str], optional): 客户端真实 IP
            custom_data ([dict], optional): 用户自定义数据
            context ([dict], optional): 请求上下文，将会传递到 Pipeline 中
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

    def login_by_phone_code(self, phone, code, client_ip=None,
                            custom_data=None,
                            context=None
                            ):
        """使用邮箱登录

        Args:
            phone (str): 手机号
            code (str): 手机号验证码
            client_ip ([str], optional): 客户端真实 IP
            custom_data ([dict], optional): 用户自定义数据
            context ([dict], optional): 请求上下文，将会传递到 Pipeline 中
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
            self, phone, password, auto_register=False, captcha_code=None, client_ip=None,
            custom_data=None,
            context=None
    ):
        """使用邮箱登录

        Args:
            phone (str): 手机号
            password (str): 密码
            auto_register (bool, optional): 如果用户不存在，是否自动注册。
            captcha_code (str, optional): 图形验证码
            client_ip ([str], optional): 客户端真实 IP
            custom_data ([dict], optional): 用户自定义数据
            context ([dict], optional): 请求上下文，将会传递到 Pipeline 中
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
            token (str, optional): token
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
            phone ([str]): 手机号
            code ([str]): 手机号验证码
            new_password ([str]): 新的密码
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
            email ([str]): 邮箱
            code ([str]): 邮箱验证码
            new_password ([str]): 新的密码
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
            new_password ([str]): 新密码
            old_password ([str]): 老密码
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
            phone ([str]): 新手机号
            phone_code ([str]): 新手机号的验证码
            old_phone ([str], optional): 原手机号
            old_phone_code ([str], optional): 原手机号验证码
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
            email ([str]): 新邮箱
            email_code ([str]): 新邮箱的验证码
            old_email ([str], optional): 原邮箱
            old_email_code ([str], optional): 原邮箱验证码
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
            primary_user_token ([str]): 主账号的 Token
            secondary_user_token ([str]): 社交账号 Token
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
            primary_user_token ([str]): 主账号的 Token
            provider ([str]): 社会化登录类型
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
            phone ([str]): 手机号
            phone_code ([str]): 手机号验证码
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
            email ([str]): 邮箱
            email_code ([str]): 邮箱验证码
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
            key ([type]): key
            value ([type]): valud
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
            key ([str]): str
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