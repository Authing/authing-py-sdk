from ..common.rest import RestClient
from . import AuthenticationClientOptions
from ..common.graphql import GraphqlClient
from ..common.utils import encrypt
from ..common.codegen import QUERY
import json


class AuthenticationClient(object):
    """Authing Management Client
    """

    def __init__(self, options: AuthenticationClientOptions):

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

    def _set_access_token(self, token: str):
        self._token = token

    def get_current_user(self, token: str = None):
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
        return data

    def register_by_email(self, email: str, password: str, profile=None, forceLogin=False, generateToken=None):
        """通过邮箱注册

        Args:
            email (str): 邮箱
            password (str): 密码
            profile ([type], optional): 用户资料
            forceLogin (bool, optional): 强制登录
            generateToken ([type], optional): 自动生成 token
        """
        password = encrypt(password, self.options.enc_public_key)
        data = self.graphqlClient.request(
            query=QUERY['registerByEmail'],
            params={
                'input': {
                    'email': email,
                    'password': password,
                    'profile': profile,
                    'forceLogin': forceLogin,
                    'generateToken': generateToken
                }
            }
        )
        user = data['registerByEmail']
        self._set_current_user(user)
        return user

    def register_by_username(self, username: str, password: str, profile=None, forceLogin=False, generateToken=None):
        """通过用户名注册

        Args:
            username (str): 用户名
            password (str): 密码
            profile ([type], optional): 用户资料
            forceLogin (bool, optional): 强制登录
            generateToken ([type], optional): 自动生成 token
        """
        password = encrypt(password, self.options.enc_public_key)
        data = self.graphqlClient.request(
            query=QUERY['registerByUsername'],
            params={
                'input': {
                    'username': username,
                    'password': password,
                    'profile': profile,
                    'forceLogin': forceLogin,
                    'generateToken': generateToken
                }
            }
        )
        user = data['registerByUsername']
        self._set_current_user(user)
        return user

    def register_by_phone_code(self, phone: str, code: str, password=None, profile=None, forceLogin=False, generateToken=None):
        """通过手机号验证码注册

        Args:
            phone (str): 手机号
            code (str): 手机号验证码
            password (str): 密码
            profile ([type], optional): 用户资料
            forceLogin (bool, optional): 强制登录
            generateToken ([type], optional): 自动生成 token
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
                    'forceLogin': forceLogin,
                    'generateToken': generateToken
                }
            }
        )
        user = data['registerByPhoneCode']
        self._set_current_user(user)
        return user

    def send_sms_code(self, phone: str):
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

    def login_by_email(self, email: str, password: str, autoRegister: bool = False, captchaCode: str = None):
        """使用邮箱登录

        Args:
            email (str): 邮箱
            password (str): 密码
            autoRegister (bool, optional): 如果用户不存在，是否自动注册。
            captchaCode (str, optional): 图形验证码
        """
        password = encrypt(password, self.options.enc_public_key)
        data = self.graphqlClient.request(
            query=QUERY['loginByEmail'],
            params={
                'input': {
                    'email': email,
                    'password': password,
                    'autoRegister': autoRegister,
                    'captchaCode': captchaCode
                }
            }
        )
        user = data['loginByEmail']
        self._set_current_user(user)
        return user

    def login_by_username(self, username: str, password: str, autoRegister: bool = False, captchaCode: str = None):
        """使用邮箱登录

        Args:
            username (str): 用户名
            password (str): 密码
            autoRegister (bool, optional): 如果用户不存在，是否自动注册。
            captchaCode (str, optional): 图形验证码
        """
        password = encrypt(password, self.options.enc_public_key)
        data = self.graphqlClient.request(
            query=QUERY['loginByUsername'],
            params={
                'input': {
                    'username': username,
                    'password': password,
                    'autoRegister': autoRegister,
                    'captchaCode': captchaCode
                }
            }
        )
        user = data['loginByUsername']
        self._set_current_user(user)
        return user

    def login_by_phone_code(self, phone: str, code: str):
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
                }
            }
        )
        user = data['loginByPhoneCode']
        self._set_current_user(user)
        return user

    def login_by_phone_password(self, phone: str, password: str, autoRegister: bool = False, captchaCode: str = None):
        """使用邮箱登录

        Args:
            phone (str): 手机号
            password (str): 密码
            autoRegister (bool, optional): 如果用户不存在，是否自动注册。
            captchaCode (str, optional): 图形验证码
        """
        password = encrypt(password, self.options.enc_public_key)
        data = self.graphqlClient.request(
            query=QUERY['loginByPhonePassword'],
            params={
                'input': {
                    'phone': phone,
                    'password': password,
                    'autoRegister': autoRegister,
                    'captchaCode': captchaCode
                }
            }
        )
        user = data['loginByPhonePassword']
        self._set_current_user(user)
        return user

    def check_login_status(self, token: str = None):
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

    def send_email(self, email: str, scene: str):
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
        newPassword
    ):
        """通过手机号验证码重置密码

        Args:
            phone ([str]): 手机号
            code ([str]): 手机号验证码
            newPassword ([str]): 新的密码
        """
        newPassword = encrypt(newPassword, self.options.enc_public_key)
        data = self.graphqlClient.request(
            query=QUERY['resetPassword'],
            params={
                'phone': phone,
                'code': code,
                'newPassword': newPassword
            }
        )
        return data['resetPassword']

    def reset_password_by_email_code(
        self,
        email,
        code,
        newPassword
    ):
        """通过邮件验证码修改密码

        Args:
            email ([str]): 邮箱
            code ([str]): 邮箱验证码
            newPassword ([str]): 新的密码
        """
        newPassword = encrypt(newPassword, self.options.enc_public_key)
        data = self.graphqlClient.request(
            query=QUERY['resetPassword'],
            params={
                'email': email,
                'code': code,
                'newPassword': newPassword
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

    def update_password(self, newPassword, oldPassword):
        """修改密码

        Args:
            newPassword ([str]): 新密码
            oldPassword ([str]): 老密码
        """
        newPassword = encrypt(newPassword, self.options.enc_public_key)
        oldPassword = encrypt(oldPassword, self.options.enc_public_key)
        data = self.graphqlClient.request(
            query=QUERY['updatePassword'],
            params={
                'newPassword': newPassword,
                'oldPassword': oldPassword
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

    def refresh_token(self, token: str = None):
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

    def unbind_phone(self, phone, phoneCode):
        """解绑手机号

        Args:
            phone ([str]): 手机号
            phoneCode ([str]): 手机号验证码
        """
        data = self.graphqlClient.request(
            query=QUERY['unbindPhone'],
            params={
                'phone': phone,
                'phoneCode': phoneCode
            },
            token=self._get_access_token()
        )
        user = data['unbindPhone']
        self._set_current_user(user)
        return user

    def udv(self):
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
        return data['udv']

    def set_udv(self, key, value):
        """设置自定义用户数据

        Args:
            key ([type]): key
            value ([type]): valud
        """
        user = self._check_logged_in()
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
        return data['setUdv']

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
        return data['removeUdv']

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
