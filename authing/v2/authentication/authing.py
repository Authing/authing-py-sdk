# coding: utf-8

from ..common.rest import RestClient
from .types import AuthenticationClientOptions
from ..common.graphql import GraphqlClient
from ..common.utils import encrypt
from ..common.codegen import QUERY
import json
import datetime
from dateutil import parser


class AuthenticationClient(object):
    """Authing Management Client
    """

    def __init__(self, options):
        # type:(AuthenticationClientOptions) -> AuthenticationClient

        self.options = options
        self.graphqlClient = GraphqlClient(
            options=self.options,
            endpoint=self.options.graphql_endpoint
        )
        self.restClient = RestClient(
            options=self.options
        )

        # 当前用户
        self._user = None
        # 当前用户的 token
        self._token = self.options.access_token or None

    def _set_current_user(self, user):
        self._user = user
        self._token = user.get('token')

    def _clear_current_user(self):
        self._user = None
        self._token = None

    def _check_logged_in(self):
        user = self.get_current_user()
        if not user:
            raise '清先登录'
        return user

    def _get_access_token(self):
        return self._token

    def _set_access_token(self, token):
        self._token = token

    def get_current_user(self, token=None):
        """获取当前用户的资料

        Args:
            token (str, optional): 用户登录凭证
        """
        data = self.graphqlClient.request(
            query=QUERY['user'],
            params={},
            token=token or self._get_access_token()
        )
        user = data['user']
        self._set_current_user(user)
        return user

    def register_by_email(self, email, password, profile=None, force_login=False, generate_token=False, clientIp=None):
        """通过邮箱注册

        Args:
            email (str): 邮箱
            password (str): 密码
            profile ([type], optional): 用户资料
            force_login (bool, optional): 强制登录
            generate_token ([type], optional): 自动生成 token
        """
        password = encrypt(password, self.options.enc_public_key)
        data = self.graphqlClient.request(
            query=QUERY['registerByEmail'],
            params={
                'input': {
                    'email': email,
                    'password': password,
                    'profile': profile,
                    'forceLogin': force_login,
                    'generateToken': generate_token,
                    'clientIp': clientIp
                }
            }
        )
        user = data['registerByEmail']
        self._set_current_user(user)
        return user

    def register_by_username(self, username, password, profile=None, force_login=False, generate_token=False, clientIp=None):
        """通过用户名注册

        Args:
            username (str): 用户名
            password (str): 密码
            profile ([type], optional): 用户资料
            force_login (bool, optional): 强制登录
            generate_token ([type], optional): 自动生成 token
        """
        password = encrypt(password, self.options.enc_public_key)
        data = self.graphqlClient.request(
            query=QUERY['registerByUsername'],
            params={
                'input': {
                    'username': username,
                    'password': password,
                    'profile': profile,
                    'forceLogin': force_login,
                    'generateToken': generate_token,
                    'clientIp': clientIp
                }
            }
        )
        user = data['registerByUsername']
        self._set_current_user(user)
        return user

    def register_by_phone_code(self, phone, code, password=None, profile=None, force_login=False, generate_token=False, clientIp=None):
        """通过手机号验证码注册

        Args:
            phone (str): 手机号
            code (str): 手机号验证码
            password (str): 密码
            profile ([type], optional): 用户资料
            force_login (bool, optional): 强制登录
            generate_token ([type], optional): 自动生成 token
        """
        if password:
            password = encrypt(password, self.options.enc_public_key)
        data = self.graphqlClient.request(
            query=QUERY['registerByPhoneCode'],
            params={
                'input': {
                    'phone': phone,
                    'code': code,
                    'password': password,
                    'profile': profile,
                    'forceLogin': force_login,
                    'generateToken': generate_token,
                    'clientIp': clientIp
                }
            }
        )
        user = data['registerByPhoneCode']
        self._set_current_user(user)
        return user

    def send_sms_code(self, phone):
        url = '%s/api/v2/sms/send' % self.options.host
        data = self.restClient.request(
            method='POST',
            url=url,
            token=None,
            json={
                'phone': phone
            }
        )
        return data

    def login_by_email(self, email, password, auto_register=False, captcha_code=None, clientIp=None):
        """使用邮箱登录

        Args:
            email (str): 邮箱
            password (str): 密码
            auto_register (bool, optional): 如果用户不存在，是否自动注册。
            captcha_code (str, optional): 图形验证码
        """
        password = encrypt(password, self.options.enc_public_key)
        data = self.graphqlClient.request(
            query=QUERY['loginByEmail'],
            params={
                'input': {
                    'email': email,
                    'password': password,
                    'autoRegister': auto_register,
                    'captchaCode': captcha_code,
                    'clientIp': clientIp
                }
            }
        )
        user = data['loginByEmail']
        self._set_current_user(user)
        return user

    def login_by_username(self, username, password, auto_register=False, captcha_code=None, clientIp=None):
        """使用邮箱登录

        Args:
            username (str): 用户名
            password (str): 密码
            auto_register (bool, optional): 如果用户不存在，是否自动注册。
            captcha_code (str, optional): 图形验证码
        """
        password = encrypt(password, self.options.enc_public_key)
        data = self.graphqlClient.request(
            query=QUERY['loginByUsername'],
            params={
                'input': {
                    'username': username,
                    'password': password,
                    'autoRegister': auto_register,
                    'captchaCode': captcha_code,
                    'clientIp': clientIp
                }
            }
        )
        user = data['loginByUsername']
        self._set_current_user(user)
        return user

    def login_by_phone_code(self, phone, code, clientIp=None):
        """使用邮箱登录

        Args:
            phone (str): 手机号
            code (str): 手机号验证码
        """
        data = self.graphqlClient.request(
            query=QUERY['loginByPhoneCode'],
            params={
                'input': {
                    'phone': phone,
                    'code': code,
                    'clientIp': clientIp
                }
            }
        )
        user = data['loginByPhoneCode']
        self._set_current_user(user)
        return user

    def login_by_phone_password(self, phone, password, auto_register=False, captcha_code=None, clientIp=None):
        """使用邮箱登录

        Args:
            phone (str): 手机号
            password (str): 密码
            auto_register (bool, optional): 如果用户不存在，是否自动注册。
            captcha_code (str, optional): 图形验证码
        """
        password = encrypt(password, self.options.enc_public_key)
        data = self.graphqlClient.request(
            query=QUERY['loginByPhonePassword'],
            params={
                'input': {
                    'phone': phone,
                    'password': password,
                    'autoRegister': auto_register,
                    'captchaCode': captcha_code,
                    'clientIp': clientIp
                }
            }
        )
        user = data['loginByPhonePassword']
        self._set_current_user(user)
        return user

    def check_login_status(self, token=None):
        """检查 token 的登录状态

        Args:
            token (str, optional): token
        """
        data = self.graphqlClient.request(
            query=QUERY['checkLoginStatus'],
            params={
                'token': token or self._token
            }
        )
        return data['checkLoginStatus']

    def send_email(self, email, scene):
        """发送邮件
        """
        data = self.graphqlClient.request(
            query=QUERY['sendEmail'],
            params={
                'email': email,
                'scene': scene
            }
        )
        return data['sendEmail']

    def reset_password_by_phone_code(
        self,
        phone,
        code,
        new_password
    ):
        """通过手机号验证码重置密码

        Args:
            phone ([str]): 手机号
            code ([str]): 手机号验证码
            new_password ([str]): 新的密码
        """
        new_password = encrypt(new_password, self.options.enc_public_key)
        data = self.graphqlClient.request(
            query=QUERY['resetPassword'],
            params={
                'phone': phone,
                'code': code,
                'newPassword': new_password
            }
        )
        return data['resetPassword']

    def reset_password_by_email_code(
        self,
        email,
        code,
        new_password
    ):
        """通过邮件验证码修改密码

        Args:
            email ([str]): 邮箱
            code ([str]): 邮箱验证码
            new_password ([str]): 新的密码
        """
        new_password = encrypt(new_password, self.options.enc_public_key)
        data = self.graphqlClient.request(
            query=QUERY['resetPassword'],
            params={
                'email': email,
                'code': code,
                'newPassword': new_password
            },
        )
        return data['resetPassword']

    def update_profile(self, updates):
        """修改用户资料
        """
        user = self._check_logged_in()
        data = self.graphqlClient.request(
            query=QUERY['updateUser'],
            params={
                'id': user['id'],
                'input': updates
            },
            token=self._get_access_token()
        )
        user = data['updateUser']
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
            query=QUERY['updatePassword'],
            params={
                'newPassword': new_password,
                'oldPassword': old_password
            },
            token=self._get_access_token()
        )
        user = data['updatePassword']
        return user

    def update_phone(self, phone, phoneCode, oldPhone=None, oldPhoneCode=None):
        """修改手机号
        """
        data = self.graphqlClient.request(
            query=QUERY['updatePhone'],
            params={
                'phone': phone,
                'phoneCode': phoneCode,
                'oldPhone': oldPhone,
                'oldPhoneCode': oldPhoneCode
            },
            token=self._get_access_token()
        )
        user = data['updatePhone']
        self._set_current_user(user)
        return user

    def update_email(self, email, emailCode, oldEmail=None, oldEmailCode=None):
        data = self.graphqlClient.request(
            query=QUERY['updatePhone'],
            params={
                'email': email,
                'emailCode': emailCode,
                'oldEmail': oldEmail,
                'oldEmailCode': oldEmailCode
            },
            token=self._get_access_token()
        )
        user = data['updatePhone']
        self._set_current_user(user)
        return user

    def refresh_token(self, token=None):
        """刷新 token

        Returns:
            [type]: [description]
        """
        data = self.graphqlClient.request(
            query=QUERY['refreshToken'],
            params={},
            token=token or self._get_access_token()
        )
        token = data['refreshToken'].get('token')
        self._set_access_token(token)
        return data['refreshToken']

    def bind_phone(self, phone, phoneCode):
        """绑定手机号
        """
        data = self.graphqlClient.request(
            query=QUERY['bindPhone'],
            params={
                'phone': phone,
                'phoneCode': phoneCode
            },
            token=self._get_access_token()
        )
        user = data['bindPhone']
        self._set_current_user(user)
        return user

    def unbind_phone(self):
        """解绑手机号
        """
        data = self.graphqlClient.request(
            query=QUERY['unbindPhone'],
            params={},
            token=self._get_access_token()
        )
        user = data['unbindPhone']
        self._set_current_user(user)
        return user

    def _convert_udv(self, data):
        for i, item in enumerate(data):
            dataType, value = item['dataType'], item['value']
            if dataType == "NUMBER":
                data[i]['value'] = json.loads(value)
            elif dataType == "BOOLEAN":
                data[i]['value'] = json.loads(value)
            elif dataType == 'DATETIME':
                data[i]['value'] = parser.parse(value)
            elif dataType == 'OBJECT':
                data[i]['value'] = json.loads(value)
        return data

    def list_udv(self):
        """获取当前用户的自定义用户数据
        """
        user = self._check_logged_in()
        data = self.graphqlClient.request(
            query=QUERY['udv'],
            params={
                'targetType': 'USER',
                'targetId': user['id']
            },
            token=self._get_access_token()
        )
        data = data['udv']
        return self._convert_udv(data)

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
            value = json.dumps(
                value,
                sort_keys=True,
                indent=1,
                default=default
            )
        else:
            value = json.dumps(value)
        data = self.graphqlClient.request(
            query=QUERY['setUdv'],
            params={
                'targetType': 'USER',
                'targetId': user['id'],
                'key': key,
                'value': value
            },
            token=self._get_access_token()
        )
        data = data['setUdv']
        return self._convert_udv(data)

    def remove_udv(self, key):
        """删除用户自定义字段数据

        Args:
            key ([str]): str
        """
        user = self._check_logged_in()
        data = self.graphqlClient.request(
            query=QUERY['removeUdv'],
            params={
                'targetType': 'USER',
                'targetId': user['id'],
                'key': key,
            },
            token=self._get_access_token()
        )
        data = data['removeUdv']
        return self._convert_udv(data)

    def logout(self):
        """退出登录 会使当前的 token 失效
        """
        user = self._check_logged_in()
        self.graphqlClient.request(
            query=QUERY['updateUser'],
            params={
                'id': user['id'],
                'input': {
                    'tokenExpiredAt': '0'
                }
            },
            token=self._get_access_token()
        )
        self._clear_current_user()
