# coding: utf-8

from .exceptions import AuthingWrongArgumentException
from .http.AuthenticationHttpClient import AuthenticationHttpClient
from .http.ProtocolHttpClient import ProtocolHttpClient
from .utils import get_random_string, url_join_args
import base64
import hashlib


class AuthenticationClient(object):
    """Authing Authentication Client"""

    def __init__(
        self,
        app_id,
        app_host,
        app_secret=None,
        access_token=None,
        timeout=10.0,
        protocol=None,
        token_endpoint_auth_method=None,
        introspection_endpoint_auth_method=None,
        revocation_endpoint_auth_method=None,
        redirect_uri=None,
        use_unverified_ssl=False,
        lang=None
    ):

        """
        初始化 AuthenticationClient 参数

        Args:
            app_id (str): 应用 ID
            app_host (str): 应用地址，如 https://your-app.authing.cn
            app_secret (str): 应用密钥
            enc_public_key (str): 密码非对称加密公钥（可选），如果你使用的是 Authing 公有云服务，可以忽略；如果你使用的是私有化部署的 Authing，请联系 Authing IDaaS 服务管理员
            timeout (int): 请求超时时间，位为毫秒，默认为 10000（10 秒）
            lang (str): 接口 Message 返回语言格式（可选），可选值为 zh-CN 和 en-US，默认为 zh-CN。
            protocol (str): 协议类型，可选值为 oidc、oauth、saml、cas
            token_endpoint_auth_method (str): 获取 token 端点验证方式，可选值为 client_secret_post、client_secret_basic、none，默认为 client_secret_post。
            introspection_endpoint_auth_method (str): 检验 token 端点验证方式，可选值为 `client_secret_post`、`client_secret_basic`、`none`，默认为 `client_secret_post`。
            revocation_endpoint_auth_method (str): 撤回 token 端点验证方式，可选值为 `client_secret_post`、`client_secret_basic`、`none`，默认为 `client_secret_post`。
            redirect_uri (str): 业务回调 URL
        """
        if not app_id:
            raise Exception('Please provide app_id')

        self.app_id = app_id
        self.app_host = app_host
        self.timeout = timeout
        self.access_token = access_token
        self.lang = lang
        self.protocol = protocol or 'oidc'
        self.app_secret = app_secret
        self.token_endpoint_auth_method = token_endpoint_auth_method or 'client_secret_post'
        self.introspection_endpoint_auth_method = introspection_endpoint_auth_method or 'client_secret_post'
        self.revocation_endpoint_auth_method = revocation_endpoint_auth_method or 'client_secret_post'
        self.redirect_uri = redirect_uri
        self.use_unverified_ssl = use_unverified_ssl

        # V3 API 接口
        self.http_client = AuthenticationHttpClient(
            app_id=self.app_id,
            host=self.app_host,
            lang=self.lang,
            use_unverified_ssl=self.use_unverified_ssl,
        )
        if self.access_token:
            self.http_client.set_access_token(self.access_token)

        # 标准协议相关接口
        self.protocol_http_client = ProtocolHttpClient(
            host=self.app_host,
            use_unverified_ssl=self.use_unverified_ssl,
        )

    def set_access_token(self, access_token):
        self.access_token = access_token
        self.http_client.set_access_token(self.access_token)

    def ___get_access_token_by_code_with_client_secret_post(self, code, code_verifier=None):
        url = "/%s/token" % ('oidc' if self.protocol == 'oidc' else 'oauth')
        data = self.protocol_http_client.request(
            method='POST',
            url=url,
            data={
                'client_id': self.app_id,
                'client_secret': self.app_secret,
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': self.redirect_uri,
                'code_verifier': code_verifier
            }
        )
        return data

    def ___get_access_token_by_code_with_client_secret_basic(self, code, code_verifier=None):
        url = "/%s/token" % ('oidc' if self.protocol == 'oidc' else 'oauth')
        data = self.protocol_http_client.request(
            method='POST',
            url=url,
            data={
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': self.redirect_uri,
                'code_verifier': code_verifier
            },
            basic_token=base64.b64encode(('%s:%s' % (self.app_id, self.app_secret)).encode()).decode()
        )
        return data

    def __get_access_token_by_code_with_none(self, code, code_verifier=None):
        url = "/%s/token" % ('oidc' if self.protocol == 'oidc' else 'oauth')
        data = self.protocol_http_client.request(
            method='POST',
            url=url,
            data={
                'client_id': self.app_id,
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': self.redirect_uri,
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

        if self.protocol not in ['oidc', 'oauth']:
            raise AuthingWrongArgumentException('argument protocol must be oidc or oauth')

        if not self.redirect_uri:
            raise AuthingWrongArgumentException('argument redirect_uri must be oidc or oauth')

        if not self.app_secret and self.token_endpoint_auth_method != 'none':
            raise AuthingWrongArgumentException('argument secret must be provided')

        if self.token_endpoint_auth_method == 'client_secret_post':
            return self.___get_access_token_by_code_with_client_secret_post(code, code_verifier)

        elif self.token_endpoint_auth_method == 'client_secret_basic':
            return self.___get_access_token_by_code_with_client_secret_basic(code, code_verifier)

        elif self.token_endpoint_auth_method == 'none':
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

        url = "/%s/token" % ('oidc' if self.protocol == 'oidc' else 'oauth')
        data = self.protocol_http_client.request(
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
        url = "/%s/me" % ('oidc' if self.protocol == 'oidc' else 'oauth')

        data = self.protocol_http_client.request(
            method='POST',
            url=url,
            token=access_token
        )
        return data

    def __build_saml_authorize_url(self):
        return "%s/api/v2/saml-idp/%s" % (self.app_host, self.app_id)

    def __build_cas_authorize_url(self, service=None):
        if service:
            return "%s/cas-idp/%s?service=%s" % (self.app_host, self.app_id, service)
        else:
            return "%s/cas-idp/%s?service" % (self.app_host, self.app_id)

    def __build_oauth_authorize_url(self, scope=None, redirect_uri=None, state=None, response_type=None):
        res = {
            'state': get_random_string(10),
            'scope': 'user',
            'client_id': self.app_id,
            'redirect_uri': self.redirect_uri,
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

        return url_join_args('%s/oauth/auth' % self.app_host, res)

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
            'client_id': self.app_id,
            'redirect_uri': self.redirect_uri,
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

        return url_join_args('%s/oidc/auth' % self.app_host, res)

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
        if not self.app_host:
            raise AuthingWrongArgumentException('must provider app_host when you init AuthenticationClient')

        if self.protocol == 'oidc':
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
        elif self.protocol == 'oauth':
            return self.__build_oauth_authorize_url(
                scope=scope,
                redirect_uri=redirect_uri,
                state=state,
                response_type=response_type
            )
        elif self.protocol == 'saml':
            return self.__build_saml_authorize_url()

        elif self.protocol == 'cas':
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
                self.app_host,
                id_token,
                redirect_uri
            )
        else:
            return "%s/oidc/session/end" % self.app_host

    def __build_easy_logout_url(self, redirect_uri=None):
        if redirect_uri:
            return "%s/login/profile/logout?redirect_uri=%s" % (
                self.app_host,
                redirect_uri
            )
        else:
            return "%s/login/profile/logout" % (
                self.app_host
            )

    def __build_cas_logout_url(self, redirect_uri=None):
        if redirect_uri:
            return "%s/cas-idp/logout?url=%s" % (
                self.app_host,
                redirect_uri
            )
        else:
            return "%s/cas-idp/logout" % (
                self.app_host
            )

    def build_logout_url(self, expert=None, redirect_uri=None, id_token=None):
        """拼接登出 URL。"""
        if not self.app_host:
            raise AuthingWrongArgumentException('must provider app_host when you init AuthenticationClient')

        if self.protocol == 'oidc':
            if not expert:
                return self.__build_easy_logout_url(redirect_uri)
            else:
                return self.__build_oidc_logout_url(
                    id_token=id_token,
                    redirect_uri=redirect_uri
                )
        elif self.protocol == 'cas':
            return self.__build_cas_logout_url(redirect_uri=redirect_uri)

    def __get_new_access_token_by_refresh_token_with_client_secret_post(self, refresh_token):
        url = "/%s/token" % ('oidc' if self.protocol == 'oidc' else 'oauth')
        data = self.protocol_http_client.request(
            method='POST',
            url=url,
            data={
                'client_id': self.app_id,
                'client_secret': self.app_secret,
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token
            }
        )
        return data

    def __get_new_access_token_by_refresh_token_with_client_secret_basic(self, refresh_token):
        url = "/%s/token" % ('oidc' if self.protocol == 'oidc' else 'oauth')
        data = self.protocol_http_client.request(
            method='POST',
            url=url,
            data={
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token
            },
            basic_token=base64.b64encode(('%s:%s' % (self.app_id, self.app_secret)).encode()).decode()
        )
        return data

    def __get_new_access_token_by_refresh_token_with_none(self, refresh_token):
        url = "/%s/token" % ('oidc' if self.protocol == 'oidc' else 'oauth')
        data = self.protocol_http_client.request(
            method='POST',
            url=url,
            data={
                'client_id': self.app_id,
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
        if self.protocol not in ['oauth', 'oidc']:
            raise AuthingWrongArgumentException('protocol must be oauth or oidc')

        if not self.app_secret and self.token_endpoint_auth_method != 'none':
            raise AuthingWrongArgumentException('secret must be provided')

        if self.token_endpoint_auth_method == 'client_secret_post':
            return self.__get_new_access_token_by_refresh_token_with_client_secret_post(refresh_token)
        elif self.token_endpoint_auth_method == 'client_secret_basic':
            return self.__get_new_access_token_by_refresh_token_with_client_secret_basic(refresh_token)
        elif self.token_endpoint_auth_method == 'none':
            return self.__get_new_access_token_by_refresh_token_with_none(refresh_token)
        else:
            raise AuthingWrongArgumentException('unsupported argument token_endpoint_auth_method')

    def __revoke_token_with_client_secret_post(self, token):
        url = "/%s/token/revocation" % ('oidc' if self.protocol == 'oidc' else 'oauth')
        return self.protocol_http_client.request(
            method='POST',
            url=url,
            data={
                'client_id': self.app_id,
                'client_secret': self.app_secret,
                'token': token
            }
        )

    def __revoke_token_with_client_secret_basic(self, token):
        url = "/%s/token/revocation" % ('oidc' if self.protocol == 'oidc' else 'oauth')
        return self.protocol_http_client.request(
            method='POST',
            url=url,
            data={
                'token': token
            },
            basic_token=base64.b64encode(('%s:%s' % (self.app_id, self.app_secret)).encode()).decode()
        )

    def __revoke_token_with_none(self, token):
        url = "/%s/token/revocation" % ('oidc' if self.protocol == 'oidc' else 'oauth')
        return self.protocol_http_client.request(
            method='POST',
            url=url,
            data={
                'client_id': self.app_id,
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
        if self.protocol not in ['oauth', 'oidc']:
            raise AuthingWrongArgumentException('protocol must be oauth or oidc')

        if not self.app_secret and self.revocation_endpoint_auth_method != 'none':
            raise AuthingWrongArgumentException('secret must be provided')

        if self.revocation_endpoint_auth_method == 'client_secret_post':
            return self.__revoke_token_with_client_secret_post(token)

        elif self.revocation_endpoint_auth_method == 'client_secret_basic':
            return self.__revoke_token_with_client_secret_basic(token)

        elif self.revocation_endpoint_auth_method == 'none':
            return self.__revoke_token_with_none(token)

        else:
            raise AuthingWrongArgumentException('unsupported argument token_endpoint_auth_method')

    def __introspect_token_with_client_secret_post(self, token):
        url = "/%s/token/introspection" % ('oidc' if self.protocol == 'oidc' else 'oauth')
        return self.protocol_http_client.request(
            method='POST',
            url=url,
            data={
                'client_id': self.app_id,
                'client_secret': self.app_secret,
                'token': token
            }
        )

    def __introspect_token_with_client_secret_basic(self, token):
        url = "/%s/token/introspection" % ('oidc' if self.protocol == 'oidc' else 'oauth')
        return self.protocol_http_client.request(
            method='POST',
            url=url,
            data={
                'token': token
            },
            basic_token=base64.b64encode(('%s:%s' % (self.app_id, self.app_secret)).encode()).decode()
        )

    def __introspect_token_with_none(self, token):
        url = "/%s/token/introspection" % ('oidc' if self.protocol == 'oidc' else 'oauth')
        return self.protocol_http_client.request(
            method='POST',
            url=url,
            data={
                'client_id': self.app_id,
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
        if self.protocol not in ['oauth', 'oidc']:
            raise AuthingWrongArgumentException('protocol must be oauth or oidc')

        if not self.app_secret and self.introspection_endpoint_auth_method != 'none':
            raise AuthingWrongArgumentException('secret must be provided')

        if self.introspection_endpoint_auth_method == 'client_secret_post':
            return self.__introspect_token_with_client_secret_post(token)

        elif self.introspection_endpoint_auth_method == 'client_secret_basic':
            return self.__introspect_token_with_client_secret_basic(token)

        elif self.introspection_endpoint_auth_method == 'none':
            return self.__introspect_token_with_none(token)

        else:
            raise AuthingWrongArgumentException('unsupported argument token_endpoint_auth_method')

    def __validate_id_token(self, id_token):
        url = "/api/v2/oidc/validate_token?id_token=%s" % (id_token)
        return self.protocol_http_client.request(
            method='GET',
            url=url,
        )

    def __validate_access_token(self, access_token):
        url = "/api/v2/oidc/validate_token?access_token=%s" % (access_token)
        return self.protocol_http_client.request(
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
        url = '/cas-idp/%s/validate?service=%s&ticket=%s' % (self.app_id, service, ticket)
        data = self.protocol_http_client.request(
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

    # ==== AUTO GENERATED AUTHENTICATION METHODS BEGIN ====
    def send_enroll_factor_request(self, profile, factor_type ):
        """发起绑定 MFA 认证要素请求

        当用户未绑定某个 MFA 认证要素时，可以发起绑定 MFA 认证要素请求。不同类型的 MFA 认证要素绑定请求需要发送不同的参数，详细见 profile 参数。发起验证请求之后，Authing 服务器会根据相应的认证要素类型和传递的参数，使用不同的手段要求验证。此接口会返回 enrollmentToken，你需要在请求「绑定 MFA 认证要素」接口时带上此 enrollmentToken，并提供相应的凭证。

        Attributes:
            profile (dict): MFA 认证要素详细信息
            factor_type (str): MFA 认证要素类型，目前共支持短信、邮箱验证码、OTP、人脸四种类型的认证要素。
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/send-enroll-factor-request',
            json={
                'profile': profile,
                'factorType': factor_type,
            },
        )

    def enroll_factor(self, enrollment_data, enrollment_token, factor_type ):
        """绑定 MFA 认证要素

        绑定 MFA 要素

        Attributes:
            enrollment_data (dict): 绑定 MFA 认证要素时，对应认证要素要求的验证信息。
            enrollment_token (str): 「发起绑定 MFA 认证要素请求」接口返回的 enrollmentToken，此 token 有效时间为一分钟。
            factor_type (str): MFA 认证要素类型，目前共支持短信、邮箱验证码、OTP、人脸四种类型的认证要素。
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/enroll-factor',
            json={
                'enrollmentData': enrollment_data,
                'enrollmentToken': enrollment_token,
                'factorType': factor_type,
            },
        )

    def reset_factor(self, factor_id ):
        """解绑 MFA 认证要素

        当前不支持通过此接口解绑短信、邮箱验证码类型的认证要素。如果需要，请调用「解绑邮箱」和「解绑手机号」接口。

        Attributes:
            factor_id (str): MFA 认证要素 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/reset-factor',
            json={
                'factorId': factor_id,
            },
        )

    def list_enrolled_factors(self, ):
        """获取绑定的所有 MFA 认证要素

        Authing 目前支持四种类型的 MFA 认证要素：手机短信、邮件验证码、OTP、人脸。如果用户绑定了手机号 / 邮箱之后，默认就具备了手机短信、邮箱验证码的 MFA 认证要素。

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-enrolled-factors',
        )

    def get_factor(self, factor_id ):
        """获取绑定的某个 MFA 认证要素

        根据 Factor ID 获取用户绑定的某个 MFA Factor 详情。

        Attributes:
            factorId (str): MFA Factor ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-factor',
            params={
                'factorId': factor_id,
            },
        )

    def list_factors_to_enroll(self, ):
        """获取可绑定的 MFA 认证要素

        获取所有应用已经开启、用户暂未绑定的 MFA 认证要素，用户可以从返回的列表中绑定新的 MFA 认证要素。

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-factors-to-enroll',
        )

    def link_ext_idp(self, ext_idp_conn_identifier, app_id, id_token ):
        """绑定外部身份源

        

    由于绝大多数的外部身份源登录不允许在第三方系统直接输入账号密码进行登录，所以外部身份源的绑定总是需要先跳转到对方的登录页面进行认证。此端点会通过浏览器 `302` 跳转的方式先跳转到第三方的登录页面，
    终端用户在第三方系统认证完成之后，浏览器再会跳转到 Authing 服务器，Authing 服务器会将此外部身份源绑定到该用户身上。最终的结果会通过浏览器 Window Post Message 的方式传递给开发者。
    你可以在你的应用系统中放置一个按钮，引导用户点击之后，弹出一个 Window Popup，地址为此端点，当用户在第三方身份源认证完成之后，此 Popup 会通过 Window Post Message 的方式传递给父窗口。

    为此我们在 `@authing/browser` SDK 中封装了相关方法，为开发者省去了其中大量的细节：

    ```typescript
    import { Authing } from "@authing/browser"
    const sdk = new Authing({
    // 应用的认证地址，例如：https://domain.authing.cn
    domain: "",

    // Authing 应用 ID
    appId: "you_authing_app_id",

    // 登录回调地址，需要在控制台『应用配置 - 登录回调 URL』中指定
    redirectUri: "your_redirect_uri"
    });


    // success 表示此次绑定操作是否成功；
    // errMsg 为如果绑定失败，具体的失败原因，如此身份源已被其他账号绑定等。
    // identities 为此次绑定操作具体绑定的第三方身份信息
    const { success, errMsg, identities } = await sdk.bindExtIdpWithPopup({
    "extIdpConnIdentifier": "my-wechat"
    })

    ```

    绑定外部身份源成功之后，你可以得到用户在此第三方身份源的信息，以绑定飞书账号为例：

    ```json
    [
    {
        "identityId": "62f20932xxxxbcc10d966ee5",
        "extIdpId": "62f209327xxxxcc10d966ee5",
        "provider": "lark",
        "type": "open_id",
        "userIdInIdp": "ou_8bae746eac07cd2564654140d2a9ac61",
        "originConnIds": ["62f2093244fa5cb19ff21ed3"]
    },
    {
        "identityId": "62f726239xxxxe3285d21c93",
        "extIdpId": "62f209327xxxxcc10d966ee5",
        "provider": "lark",
        "type": "union_id",
        "userIdInIdp": "on_093ce5023288856aa0abe4099123b18b",
        "originConnIds": ["62f2093244fa5cb19ff21ed3"]
    },
    {
        "identityId": "62f72623e011cf10c8851e4c",
        "extIdpId": "62f209327xxxxcc10d966ee5",
        "provider": "lark",
        "type": "user_id",
        "userIdInIdp": "23ded785",
        "originConnIds": ["62f2093244fa5cb19ff21ed3"]
    }
    ]
    ```

    可以看到，我们获取到了用户在飞书中的身份信息：

    - `open_id`: ou_8bae746eac07cd2564654140d2a9ac61
    - `union_id`: on_093ce5023288856aa0abe4099123b18b
    - `user_id`: 23ded785

    绑定此外部身份源之后，后续用户就可以使用此身份源进行登录了，见**登录**接口。

    

        Attributes:
            ext_idp_conn_identifier (str): 外部身份源连接唯一标志
            app_id (str): Authing 应用 ID
            id_token (str): 用户的 id_token
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/link-extidp',
            params={
                'ext_idp_conn_identifier': ext_idp_conn_identifier,
                'app_id': app_id,
                'id_token': id_token,
            },
        )

    def generate_link_ext_idp_url(self, ext_idp_conn_identifier, app_id, id_token ):
        """生成绑定外部身份源的链接

        

    由于绝大多数的外部身份源登录不允许在第三方系统直接输入账号密码进行登录，所以外部身份源的绑定总是需要先跳转到对方的登录页面进行认证。此端点会通过浏览器 `302` 跳转的方式先跳转到第三方的登录页面，
    终端用户在第三方系统认证完成之后，浏览器再会跳转到 Authing 服务器，Authing 服务器会将此外部身份源绑定到该用户身上。最终的结果会通过浏览器 Window Post Message 的方式传递给开发者。
    你可以在你的应用系统中放置一个按钮，引导用户点击之后，弹出一个 Window Popup，地址为此端点，当用户在第三方身份源认证完成之后，此 Popup 会通过 Window Post Message 的方式传递给父窗口。

    为此我们在 `@authing/browser` SDK 中封装了相关方法，为开发者省去了其中大量的细节：

    ```typescript
    import { Authing } from "@authing/browser"
    const sdk = new Authing({
    // 应用的认证地址，例如：https://domain.authing.cn
    domain: "",

    // Authing 应用 ID
    appId: "you_authing_app_id",

    // 登录回调地址，需要在控制台『应用配置 - 登录回调 URL』中指定
    redirectUri: "your_redirect_uri"
    });


    // success 表示此次绑定操作是否成功；
    // errMsg 为如果绑定失败，具体的失败原因，如此身份源已被其他账号绑定等。
    // identities 为此次绑定操作具体绑定的第三方身份信息
    const { success, errMsg, identities } = await sdk.bindExtIdpWithPopup({
    "extIdpConnIdentifier": "my-wechat"
    })

    ```

    绑定外部身份源成功之后，你可以得到用户在此第三方身份源的信息，以绑定飞书账号为例：

    ```json
    [
    {
        "identityId": "62f20932xxxxbcc10d966ee5",
        "extIdpId": "62f209327xxxxcc10d966ee5",
        "provider": "lark",
        "type": "open_id",
        "userIdInIdp": "ou_8bae746eac07cd2564654140d2a9ac61",
        "originConnIds": ["62f2093244fa5cb19ff21ed3"]
    },
    {
        "identityId": "62f726239xxxxe3285d21c93",
        "extIdpId": "62f209327xxxxcc10d966ee5",
        "provider": "lark",
        "type": "union_id",
        "userIdInIdp": "on_093ce5023288856aa0abe4099123b18b",
        "originConnIds": ["62f2093244fa5cb19ff21ed3"]
    },
    {
        "identityId": "62f72623e011cf10c8851e4c",
        "extIdpId": "62f209327xxxxcc10d966ee5",
        "provider": "lark",
        "type": "user_id",
        "userIdInIdp": "23ded785",
        "originConnIds": ["62f2093244fa5cb19ff21ed3"]
    }
    ]
    ```

    可以看到，我们获取到了用户在飞书中的身份信息：

    - `open_id`: ou_8bae746eac07cd2564654140d2a9ac61
    - `union_id`: on_093ce5023288856aa0abe4099123b18b
    - `user_id`: 23ded785

    绑定此外部身份源之后，后续用户就可以使用此身份源进行登录了，见**登录**接口。

    

        Attributes:
            ext_idp_conn_identifier (str): 外部身份源连接唯一标志
            app_id (str): Authing 应用 ID
            id_token (str): 用户的 id_token
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/generate-link-extidp-url',
            params={
                'ext_idp_conn_identifier': ext_idp_conn_identifier,
                'app_id': app_id,
                'id_token': id_token,
            },
        )

    def unbind_ext_idp(self, ext_idp_id ):
        """解绑外部身份源

        解绑外部身份源，此接口需要传递用户绑定的外部身份源 ID，**注意不是身份源连接 ID**。

        Attributes:
            ext_idp_id (str): 外部身份源 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/unlink-extidp',
            json={
                'extIdpId': ext_idp_id,
            },
        )

    def get_identities(self, ):
        """获取绑定的外部身份源

        
    如在**介绍**部分中所描述的，一个外部身份源对应多个外部身份源连接，用户通过某个外部身份源连接绑定了某个外部身份源账号之后，
    用户会建立一条与此外部身份源之间的关联关系。此接口用于获取此用户绑定的所有外部身份源。

    取决于外部身份源的具体实现，一个用户在外部身份源中，可能会有多个身份 ID，比如在微信体系中会有 `openid` 和 `unionid`，在非书中有
    `open_id`、`union_id` 和 `user_id`。在 Authing 中，我们把这样的一条 `open_id` 或者 `unionid_` 叫做一条 `Identity`， 所以用户在一个身份源会有多条 `Identity` 记录。

    以微信为例，如果用户使用微信登录或者绑定了微信账号，他的 `Identity` 信息如下所示：

    ```json
    [
    {
        "identityId": "62f20932xxxxbcc10d966ee5",
        "extIdpId": "62f209327xxxxcc10d966ee5",
        "provider": "wechat",
        "type": "openid",
        "userIdInIdp": "oH_5k5SflrwjGvk7wqpoBKq_cc6M",
        "originConnIds": ["62f2093244fa5cb19ff21ed3"]
    },
    {
        "identityId": "62f726239xxxxe3285d21c93",
        "extIdpId": "62f209327xxxxcc10d966ee5",
        "provider": "wechat",
        "type": "unionid",
        "userIdInIdp": "o9Nka5ibU-lUGQaeAHqu0nOZyJg0",
        "originConnIds": ["62f2093244fa5cb19ff21ed3"]
    }
    ]
    ```


    可以看到他们的 `extIdpId` 是一样的，这个是你在 Authing 中创建的**身份源 ID**；`provider` 都是 `wechat`；
    通过 `type` 可以区分出哪个是 `openid`，哪个是 `unionid`，以及具体的值（`userIdInIdp`）；他们都来自于同一个身份源连接（`originConnIds`）。


    

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-identities',
        )

    def get_ext_idps(self, ):
        """获取应用开启的外部身份源列表

        获取应用开启的外部身份源列表，前端可以基于此渲染外部身份源按钮。

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-extidps',
        )

    def sign_up(self, connection, password_payload=None, pass_code_payload=None, profile=None, options=None ):
        """注册

        
    此端点目前支持以下几种基于的注册方式：

    1. 基于密码（PASSWORD）：用户名 + 密码，邮箱 + 密码。
    2. 基于一次性临时验证码（PASSCODE）：手机号 + 验证码，邮箱 + 验证码。你需要先调用发送短信或者发送邮件接口获取验证码。

    社会化登录等使用外部身份源“注册”请直接使用**登录**接口，我们会在其第一次登录的时候为其创建一个新账号。


        Attributes:
            connection (str): 注册方式：
    - `PASSWORD`: 邮箱密码方式
    - `PASSCODE`: 邮箱/手机号验证码方式
        
            password_payload (dict): 当主持方式为 `PASSWORD` 时此参数必填。
            pass_code_payload (dict): 当认证方式为 `PASSCODE` 时此参数必填
            profile (dict): 用户资料
            options (dict): 可选参数
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/signup',
            json={
                'connection': connection,
                'passwordPayload': password_payload,
                'passCodePayload': pass_code_payload,
                'profile': profile,
                'options': options,
            },
        )

    def decrypt_wechat_mini_program_data(self, code, iv, encrypted_data, ext_idp_connidentifier ):
        """解密微信小程序数据

        

        Attributes:
            code (str): `wx.login` 接口返回的用户 `code`
            iv (str): 对称解密算法初始向量，由微信返回
            encrypted_data (str): 获取微信开放数据返回的加密数据（encryptedData）
            ext_idp_connidentifier (str): 微信小程序的外部身份源连接标志符
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/decrypt-wechat-miniprogram-data',
            json={
                'code': code,
                'iv': iv,
                'encryptedData': encrypted_data,
                'extIdpConnidentifier': ext_idp_connidentifier,
            },
        )

    def get_wechat_miniprogram_phone(self, code, ext_idp_connidentifier ):
        """获取小程序的手机号

        

        Attributes:
            code (str): `open-type=getphonecode` 接口返回的 `code`
            ext_idp_connidentifier (str): 微信小程序的外部身份源连接标志符
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-wechat-miniprogram-phone',
            json={
                'code': code,
                'extIdpConnidentifier': ext_idp_connidentifier,
            },
        )

    def get_wechat_mp_access_token(self, app_secret, app_id ):
        """获取 Authing 服务器缓存的微信小程序、公众号 Access Token

        

        Attributes:
            app_secret (str): 微信小程序或微信公众号的 AppSecret
            app_id (str): 微信小程序或微信公众号的 AppId
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-wechat-access-token',
            json={
                'appSecret': app_secret,
                'appId': app_id,
            },
        )

    def decrypt_wechat_mini_program_data1(self, app_id=None, client_ip=None, success=None, start=None, end=None, page=None, limit=None ):
        """获取登录日志

        获取登录日志

        Attributes:
            appId (str): 应用 ID，可根据应用 ID 筛选。默认不传获取所有应用的登录历史。
            clientIp (str): 客户端 IP，可根据登录时的客户端 IP 进行筛选。默认不传获取所有登录 IP 的登录历史。
            success (bool): 是否登录成功，可根据是否登录成功进行筛选。默认不传获取的记录中既包含成功也包含失败的的登录历史。
            start (int): 开始时间，为单位为毫秒的时间戳
            end (int): 结束时间，为单位为毫秒的时间戳
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-login-history',
            params={
                'appId': app_id,
                'clientIp': client_ip,
                'success': success,
                'start': start,
                'end': end,
                'page': page,
                'limit': limit,
            },
        )

    def get_logged_in_apps(self, ):
        """获取登录应用

        获取登录应用

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-logged-in-apps',
        )

    def get_accessible_apps(self, ):
        """获取具备访问权限的应用

        获取具备访问权限的应用

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-accessible-apps',
        )

    def get_department_list(self, page=None, limit=None, with_custom_data=None, sort_by=None, order_by=None ):
        """获取部门列表

        此接口用于获取用户的部门列表，可根据一定排序规则进行排序。

        Attributes:
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            withCustomData (bool): 是否获取部门的自定义数据
            sortBy (str): 排序依据，如 部门创建时间、加入部门时间、部门名称、部门标志符
            orderBy (str): 增序或降序
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-department-list',
            params={
                'page': page,
                'limit': limit,
                'withCustomData': with_custom_data,
                'sortBy': sort_by,
                'orderBy': order_by,
            },
        )

    def get_authorized_resources(self, namespace=None, resource_type=None ):
        """获取被授权的资源列表

        此接口用于获取用户被授权的资源列表。

        Attributes:
            namespace (str): 所属权限分组的 code
            resourceType (str): 资源类型，如 数据、API、菜单、按钮
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-authorized-resources',
            params={
                'namespace': namespace,
                'resourceType': resource_type,
            },
        )

    def upload(self, folder=None, is_private=None ):
        """文件上传

        

        Attributes:
            folder (str): 上传的目录
            is_private (bool): 是否为私有资源
        """
        return self.http_client.request(
            method='POST',
            url='/api/v2/upload',
            json={
                'folder': folder,
                'isPrivate': is_private,
            },
        )

    def sign_in_by_credentials(self, connection, password_payload=None, pass_code_payload=None, ad_payload=None, ldap_payload=None, options=None ):
        """使用用户凭证登录

        
    此端点为基于直接 API 调用形式的登录端点，适用于你需要自建登录页面的场景。**此端点暂时不支持 MFA、信息补全、首次密码重置等流程，如有需要，请使用 OIDC 标准协议认证端点。**

    ### 错误码

    此接口可能出现的异常类型：

    | 请求状态码 `statusCode` | 业务状态码 `apiCode` | 含义 | 错误提示示例 |
    | --- | --- | --- | --- |
    | 400  | - | 请求参数错误 | Parameter passwordPayload must include account, email, username or phone when authenticationType is PASSWORD. |
    | 403  | 2333 | 账号或密码错误 | Account not exists or password is incorrect. |
    | 403  | 2006 | 密码错误 | Password is incorrect. |
    | 403  | 2000 | 当用户池开启**登录失败次数限制**并且**登录安全策略**设置为**验证码**时，如果当前请求触发登录失败次数上限，要求用户输入图形验证码。见**生成图形验证码**接口了解如何生成图形验证码。图形验证码参数通过 `options.captchaCode` 进行传递。 | Please enter captcha code for this login request. |
    | 404  | 2004 | 用户不存在 | User not exists. |
    | 499  | 2016 | 当 `passwordEncryptType` 不为 `none` 时，服务器尝试解密密码失败 | Decrypt password failed, please check your encryption configuration. |

    错误示例：

    ```json
    {
    "statusCode": 400,
    "message": "Parameter passwordPayload must include account, email, username or phone when authenticationType is PASSWORD."
    }
    ```

    

        Attributes:
            connection (str): 认证方式：
    - `PASSWORD`: 使用密码方式进行认证。
    - `PASSCODE`: 使用一次性临时验证码进行认证。
    - `LDAP`: 基于 LDAP 用户目录进行认证。
    - `AD`: 基于 Windows AD 用户目录进行认证。
        
            password_payload (dict): 当认证方式为 `PASSWORD` 时此参数必填。
            pass_code_payload (dict): 当认证方式为 `PASSCODE` 时此参数必填
            ad_payload (dict): 当认证方式为 `AD` 时此参数必填
            ldap_payload (dict): 当认证方式为 `LDAP` 时此参数必填
            options (dict): 可选参数
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/signin',
            json={
                'connection': connection,
                'passwordPayload': password_payload,
                'passCodePayload': pass_code_payload,
                'adPayload': ad_payload,
                'ldapPayload': ldap_payload,
                'options': options,
            },
        )

    def sign_in_by_mobile(self, ext_idp_connidentifier, connection, wechat_payload=None, alipay_payload=None, wechatwork_payload=None, wechatwork_agency_payload=None, lark_public_payload=None, lark_internal_payload=None, yidun_payload=None, wechat_mini_program_code_payload=None, wechat_mini_program_phone_payload=None, options=None ):
        """使用移动端社会化登录

        
    此端点为移动端社会化登录接口，使用第三方移动社会化登录返回的临时凭证登录，并换取用户的 `id_token` 和 `access_token`。请先阅读相应社会化登录的接入流程。
    

        Attributes:
            ext_idp_connidentifier (str): 外部身份源连接标志符
            connection (str): 移动端社会化登录类型：
    - `wechat`: 微信移动应用
    - `alipay`: 支付宝移动应用
    - `wechatwork`: 企业微信移动应用
    - `wechatwork_agency`: 企业微信移动应用（代开发模式）
    - `lark_internal`: 飞书移动端企业自建应用
    - `lark_public`: 飞书移动端应用商店应用
    - `yidun`: 网易易盾一键登录
    - `wechat_mini_program_code`: 微信小程序使用 code 登录
    - `wechat_mini_program_phone `: 微信小程序使用手机号登录

            wechat_payload (dict): 微信移动端社会化登录数据，当 `connection` 为 `wechat` 的时候必填
            alipay_payload (dict): 支付宝移动端社会化登录数据，当 `connection` 为 `alipay` 的时候必填
            wechatwork_payload (dict): 企业微信移动端社会化登录数据，当 `connection` 为 `wechatwork` 的时候必填
            wechatwork_agency_payload (dict): 企业微信（代开发模式）移动端社会化登录数据，当 `connection` 为 `wechatwork_agency` 的时候必填
            lark_public_payload (dict): 飞书应用商店应用移动端社会化登录数据，当 `connection` 为 `lark_public` 的时候必填
            lark_internal_payload (dict): 飞书应用商店应用移动端社会化登录数据，当 `connection` 为 `lark_internal` 的时候必填
            yidun_payload (dict): 网易易盾移动端社会化登录数据，当 `connection` 为 `yidun` 的时候必填
            wechat_mini_program_code_payload (dict): 网易易盾移动端社会化登录数据，当 `connection` 为 `wechat_mini_program_code` 的时候必填
            wechat_mini_program_phone_payload (dict): 网易易盾移动端社会化登录数据，当 `connection` 为 `wechat_mini_program_phone` 的时候必填
            options (dict): 可选参数
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/signin-by-mobile',
            json={
                'extIdpConnidentifier': ext_idp_connidentifier,
                'connection': connection,
                'wechatPayload': wechat_payload,
                'alipayPayload': alipay_payload,
                'wechatworkPayload': wechatwork_payload,
                'wechatworkAgencyPayload': wechatwork_agency_payload,
                'larkPublicPayload': lark_public_payload,
                'larkInternalPayload': lark_internal_payload,
                'yidunPayload': yidun_payload,
                'wechatMiniProgramCodePayload': wechat_mini_program_code_payload,
                'wechatMiniProgramPhonePayload': wechat_mini_program_phone_payload,
                'options': options,
            },
        )

    def get_alipay_auth_info(self, ext_idp_connidentifier ):
        """获取支付宝 AuthInfo

        此接口用于获取发起支付宝认证需要的[初始化参数 AuthInfo](https://opendocs.alipay.com/open/218/105325)。

        Attributes:
            extIdpConnidentifier (str): 外部身份源连接标志符
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-alipay-authinfo',
            params={
                'extIdpConnidentifier': ext_idp_connidentifier,
            },
        )

    def gene_qr_code(self, type, ext_idp_conn_id=None, custom_data=None, context=None, auto_merge_qr_code=None ):
        """生成用于登录的二维码

        生成用于登录的二维码，目前支持生成微信公众号扫码登录、小程序扫码登录、自建移动 APP 扫码登录的二维码。

        Attributes:
            type (str): 二维码类型。当前支持三种类型：
    - `MOBILE_APP`: 自建移动端 APP 扫码
    - `WECHAT_MINIPROGRAM`: 微信小程序扫码
    - `WECHAT_OFFICIAL_ACCOUN` 关注微信公众号扫码
            ext_idp_conn_id (str): 当 `type` 为 `WECHAT_MINIPROGRAM` 或 `WECHAT_OFFICIAL_ACCOUNT` 时，可以指定身份源连接，否则默认使用应用开启的第一个对应身份源连接生成二维码。
            custom_data (dict): 当 `type` 为 `MOBILE_APP` 时，可以传递用户的自定义数据，当用户成功扫码授权时，会将此数据存入用户的自定义数据。
            context (dict): 当 type 为 `WECHAT_OFFICIAL_ACCOUNT` 或 `WECHAT_MINIPROGRAM` 时，指定自定义的 pipeline 上下文，将会传递的 pipeline 的 context 中
            auto_merge_qr_code (bool): 当 type 为 `WECHAT_MINIPROGRAM` 时，是否将自定义的 logo 自动合并到生成的图片上，默认为 false。服务器合并二维码的过程会加大接口响应速度，推荐使用默认值，在客户端对图片进行拼接。如果你使用 Authing 的 SDK，可以省去手动拼接的过程。
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/gene-qrcode',
            json={
                'type': type,
                'extIdpConnId': ext_idp_conn_id,
                'customData': custom_data,
                'context': context,
                'autoMergeQrCode': auto_merge_qr_code,
            },
        )

    def check_qr_code_status(self, qrcode_id ):
        """查询二维码状态

        按照用户扫码顺序，共分为未扫码、已扫码等待用户确认、用户同意/取消授权、二维码过期以及未知错误六种状态，前端应该通过不同的状态给到用户不同的反馈。你可以通过下面这篇文章了解扫码登录详细的流程：https://docs.authing.cn/v2/concepts/how-qrcode-works.html.

        Attributes:
            qrcodeId (str): 二维码唯一 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/check-qrcode-status',
            params={
                'qrcodeId': qrcode_id,
            },
        )

    def exchange_token_set_with_qr_code_ticket(self, ticket ):
        """使用二维码 ticket 换取 TokenSet

        

        Attributes:
            ticket (str): 当二维码状态为已授权时返回。如果在控制台应用安全 - 通用安全 - 登录安全 - APP 扫码登录 Web 安全中未开启「Web 轮询接口返回完整用户信息」（默认处于关闭状态），会返回此 ticket，用于换取完整的用户信息。
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/exchange-tokenset-with-qrcode-ticket',
            json={
                'ticket': ticket,
            },
        )

    def gene_captcha_code(self, r=None ):
        """生成图形验证码

        当用户池开启**登录失败次数限制**并且**登录安全策略**设置为**验证码**时，如果当前请求触发登录失败次数上限，要求用户输入图形验证码。此接口用于在前端生成图形验证码，会返回一个 `content-type` 为 `image/svg+xml` 的响应。

        Attributes:
            r (str): 随机字符串或者时间戳，防止浏览器缓存
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/captcha-code',
            params={
                'r': r,
            },
        )

    def change_qr_code_status(self, action, qrcode_id ):
        """自建 APP 扫码登录：APP 端修改二维码状态

        此端点用于在自建 APP 扫码登录中修改二维码状态，对应着在浏览器渲染出二维码之后，终端用户扫码、确认授权、取消授权的过程。**此接口要求具备用户的登录态**。

        Attributes:
            action (str): 修改二维码状态的动作:
    - `SCAN`: 修改二维码状态为已扫码状态，当移动 APP 扫了码之后，应当立即执行此操作；
    - `CONFIRM`: 修改二维码状态为已授权，执行此操作前必须先执行 `SCAN 操作；
    - `CANCEL`: 修改二维码状态为已取消，执行此操作前必须先执行 `SCAN 操作；
        
            qrcode_id (str): 二维码唯一 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/change-qrcode-status',
            json={
                'action': action,
                'qrcodeId': qrcode_id,
            },
        )

    def send_sms(self, channel, phone_number, phone_country_code=None ):
        """发送短信

        发送短信时必须指定短信 Channel，每个手机号同一 Channel 在一分钟内只能发送一次。

        Attributes:
            channel (str): 短信通道，指定发送此短信的目的，如 CHANNEL_LOGIN 用于登录、CHANNEL_REGISTER 用于注册。
            phone_number (str): 手机号，不带区号。如果是国外手机号，请在 phoneCountryCode 参数中指定区号。
            phone_country_code (str): 手机区号，中国大陆手机号可不填。Authing 短信服务暂不内置支持国际手机号，你需要在 Authing 控制台配置对应的国际短信服务。完整的手机区号列表可参阅 https://en.wikipedia.org/wiki/List_of_country_calling_codes。
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/send-sms',
            json={
                'channel': channel,
                'phoneNumber': phone_number,
                'phoneCountryCode': phone_country_code,
            },
        )

    def send_email(self, channel, email ):
        """发送邮件

        发送邮件时必须指定邮件 Channel，每个邮箱同一 Channel 在一分钟内只能发送一次。

        Attributes:
            channel (str): 短信通道，指定发送此短信的目的，如 CHANNEL_LOGIN 用于登录、CHANNEL_REGISTER 用于注册。
            email (str): 邮箱，不区分大小写
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/send-email',
            json={
                'channel': channel,
                'email': email,
            },
        )

    def get_profile(self, with_custom_data=None, with_identities=None, with_department_ids=None ):
        """获取用户资料

        此端点用户获取用户资料，需要在请求头中带上用户的 `access_token`，Authing 服务器会根据用户 `access_token` 中的 `scope` 返回对应的字段。

        Attributes:
            withCustomData (bool): 是否获取自定义数据
            withIdentities (bool): 是否获取 identities
            withDepartmentIds (bool): 是否获取部门 ID 列表
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-profile',
            params={
                'withCustomData': with_custom_data,
                'withIdentities': with_identities,
                'withDepartmentIds': with_department_ids,
            },
        )

    def update_profile(self, name=None, nickname=None, photo=None, external_id=None, birthdate=None, country=None, province=None, city=None, address=None, street_address=None, postal_code=None, gender=None, username=None, custom_data=None ):
        """修改用户资料

        此接口用于修改用户的用户资料，包含用户的自定义数据。如果需要**修改邮箱**、**修改手机号**、**修改密码**，请使用对应的单独接口。

        Attributes:
            name (str): 用户真实名称，不具备唯一性
            nickname (str): 昵称
            photo (str): 头像链接
            external_id (str): 第三方外部 ID
            birthdate (str): 出生日期
            country (str): 所在国家
            province (str): 所在省份
            city (str): 所在城市
            address (str): 所处地址
            street_address (str): 所处街道地址
            postal_code (str): 邮政编码号
            gender (str): 性别
            username (str): 用户名，用户池内唯一
            custom_data (dict): 自定义数据，传入的对象中的 key 必须先在用户池定义相关自定义字段
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-profile',
            json={
                'name': name,
                'nickname': nickname,
                'photo': photo,
                'externalId': external_id,
                'birthdate': birthdate,
                'country': country,
                'province': province,
                'city': city,
                'address': address,
                'streetAddress': street_address,
                'postalCode': postal_code,
                'gender': gender,
                'username': username,
                'customData': custom_data,
            },
        )

    def bind_email(self, pass_code, email ):
        """绑定邮箱

        如果用户还**没有绑定邮箱**，此接口可用于用户**自主**绑定邮箱。如果用户已经绑定邮箱想要修改邮箱，请使用**修改邮箱**接口。你需要先调用**发送邮件**接口发送邮箱验证码。

        Attributes:
            pass_code (str): 邮箱验证码，一个邮箱验证码只能使用一次，且有一定有效时间。
            email (str): 邮箱，不区分大小写。
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/bind-email',
            json={
                'passCode': pass_code,
                'email': email,
            },
        )

    def bind_phone(self, pass_code, phone_number, phone_country_code=None ):
        """绑定手机号

        如果用户还**没有绑定手机号**，此接口可用于用户**自主**绑定手机号。如果用户已经绑定手机号想要修改手机号，请使用**修改手机号**接口。你需要先调用**发送短信**接口发送短信验证码。

        Attributes:
            pass_code (str): 短信验证码，注意一个短信验证码指南使用一次，且有过期时间。
            phone_number (str): 手机号，不带区号。如果是国外手机号，请在 phoneCountryCode 参数中指定区号。
            phone_country_code (str): 手机区号，中国大陆手机号可不填。Authing 短信服务暂不内置支持国际手机号，你需要在 Authing 控制台配置对应的国际短信服务。完整的手机区号列表可参阅 https://en.wikipedia.org/wiki/List_of_country_calling_codes。
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/bind-phone',
            json={
                'passCode': pass_code,
                'phoneNumber': phone_number,
                'phoneCountryCode': phone_country_code,
            },
        )

    def get_security_level(self, ):
        """获取密码强度和账号安全等级评分

        获取用户的密码强度和账号安全等级评分，需要在请求头中带上用户的 `access_token`。

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-security-info',
        )

    def update_password(self, new_password, old_password=None, password_encrypt_type=None ):
        """修改密码

        此端点用于用户自主修改密码，如果用户之前已经设置密码，需要提供用户的原始密码作为凭证。如果用户忘记了当前密码，请使用**忘记密码**接口。

        Attributes:
            new_password (str): 新密码
            old_password (str): 原始密码，如果用户当前设置了密码，此参数必填。
            password_encrypt_type (str): 密码加密类型，支持 sm2 和 rsa。默认可以不加密。
    - `none`: 不对密码进行加密，使用明文进行传输。
    - `rsa`: 使用 RSA256 算法对密码进行加密，需要使用 Authing 服务的 RSA 公钥进行加密，请阅读**介绍**部分了解如何获取 Authing 服务的 RSA256 公钥。
    - `sm2`: 使用 [国密 SM2 算法](https://baike.baidu.com/item/SM2/15081831) 对密码进行加密，需要使用 Authing 服务的 SM2 公钥进行加密，请阅读**介绍**部分了解如何获取 Authing 服务的 SM2 公钥。
        
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-password',
            json={
                'newPassword': new_password,
                'oldPassword': old_password,
                'passwordEncryptType': password_encrypt_type,
            },
        )

    def verify_update_email_request(self, email_passcode_payload, verify_method ):
        """发起修改邮箱的验证请求

        终端用户自主修改邮箱时，需要提供相应的验证手段。此接口用于验证用户的修改邮箱请求是否合法。当前支持通过**邮箱验证码**的方式进行验证，你需要先调用发送邮件接口发送对应的邮件验证码。

        Attributes:
            email_passcode_payload (dict): 使用邮箱验证码方式验证的数据
            verify_method (str): 修改当前邮箱使用的验证手段：
    - `EMAIL_PASSCODE`: 通过邮箱验证码进行验证，当前只支持这种验证方式。
        
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/veirfy-update-email-request',
            json={
                'emailPasscodePayload': email_passcode_payload,
                'verifyMethod': verify_method,
            },
        )

    def update_email(self, update_email_token ):
        """修改邮箱

        终端用户自主修改邮箱，需要提供相应的验证手段，见[发起修改邮箱的验证请求](#tag/用户资料/修改邮箱/operation/ProfileV3Controller_updateEmailVerification)。
    此参数需要提供一次性临时凭证 `updateEmailToken`，此数据需要从**发起修改邮箱的验证请求**接口获取。

        Attributes:
            update_email_token (str): 用于临时修改邮箱的 token，可从**发起修改邮箱的验证请求**接口获取。
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-email',
            json={
                'updateEmailToken': update_email_token,
            },
        )

    def verify_update_phone_request(self, phone_pass_code_payload, verify_method ):
        """发起修改手机号的验证请求

        终端用户自主修改手机号时，需要提供相应的验证手段。此接口用于验证用户的修改手机号请求是否合法。当前支持通过**短信验证码**的方式进行验证，你需要先调用发送短信接口发送对应的短信验证码。

        Attributes:
            phone_pass_code_payload (dict): 使用手机号验证码方式验证的数据
            verify_method (str): 修改手机号的验证方式：
    - `PHONE_PASSCODE`: 使用短信验证码的方式进行验证，当前仅支持这一种方式。
        
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/veirfy-update-phone-request',
            json={
                'phonePassCodePayload': phone_pass_code_payload,
                'verifyMethod': verify_method,
            },
        )

    def update_phone(self, update_phone_token ):
        """修改手机号

        终端用户自主修改手机号，需要提供相应的验证手段，见[发起修改手机号的验证请求](#tag/用户资料/修改邮箱/operation/ProfileV3Controller_updatePhoneVerification)。
    此参数需要提供一次性临时凭证 `updatePhoneToken`，此数据需要从**发起修改手机号的验证请求**接口获取。

        Attributes:
            update_phone_token (str): 用于临时修改手机号的 token，可从**发起修改手机号的验证请求**接口获取。
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-phone',
            json={
                'updatePhoneToken': update_phone_token,
            },
        )

    def verify_reset_password_request(self, verify_method, phone_pass_code_payload=None, email_pass_code_payload=None ):
        """发起忘记密码请求

        当用户忘记密码时，可以通过此端点找回密码。用户需要使用相关验证手段进行验证，目前支持**邮箱验证码**和**手机号验证码**两种验证手段。

        Attributes:
            verify_method (str): 忘记密码请求使用的验证手段：
    - `EMAIL_PASSCODE`: 通过邮箱验证码进行验证，当前只支持这种验证方式。
        
            phone_pass_code_payload (dict): 使用手机号验证码验证的数据
            email_pass_code_payload (dict): 使用邮箱验证码验证的数据
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/verify-reset-password-request',
            json={
                'verifyMethod': verify_method,
                'phonePassCodePayload': phone_pass_code_payload,
                'emailPassCodePayload': email_pass_code_payload,
            },
        )

    def reset_password(self, password, password_reset_token ):
        """忘记密码

        此端点用于用户忘记密码之后，通过**手机号验证码**或者**邮箱验证码**的方式重置密码。此接口需要提供用于重置密码的临时凭证 `passwordResetToken`，此参数需要通过**发起忘记密码请求**接口获取。

        Attributes:
            password (str): 密码
            password_reset_token (str): 重置密码的 token
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/reset-password',
            json={
                'password': password,
                'passwordResetToken': password_reset_token,
            },
        )

    def veirfy_delete_account_request(self, verify_method, phone_pass_code_payload=None, email_pass_code_payload=None, password_payload=None ):
        """发起注销账号请求

        当用户希望注销账号时，需提供相应凭证，当前支持**使用邮箱验证码**、使用**手机验证码**、**使用密码**三种验证方式。

        Attributes:
            verify_method (str): 注销账号的验证手段：
    - `PHONE_PASSCODE`: 使用手机号验证码方式进行验证。
    - `EMAIL_PASSCODE`: 使用邮箱验证码方式进行验证。
    - `PASSWORD`: 如果用户既没有绑定手机号又没有绑定邮箱，可以使用密码作为验证手段。
        
            phone_pass_code_payload (dict): 使用手机号验证码验证的数据
            email_pass_code_payload (dict): 使用邮箱验证码验证的数据
            password_payload (dict): 使用密码验证的数据
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/verify-delete-account-request',
            json={
                'verifyMethod': verify_method,
                'phonePassCodePayload': phone_pass_code_payload,
                'emailPassCodePayload': email_pass_code_payload,
                'passwordPayload': password_payload,
            },
        )

    def delete_account(self, delete_account_token ):
        """注销账户

        此端点用于用户自主注销账号，需要提供用于注销账号的临时凭证 passwordResetToken，此参数需要通过**发起注销账号请求**接口获取。

        Attributes:
            delete_account_token (str): 注销账户的 token
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-account',
            json={
                'deleteAccountToken': delete_account_token,
            },
        )

    def get_application_public_config(self, app_id=None ):
        """获取应用公开配置

        

        Attributes:
            appId (str): 应用 ID，可选，默认会从请求的域名获取对应的应用
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-application-public-config',
            params={
                'appId': app_id,
            },
        )

    def get_system_info(self, ):
        """获取服务器公开信息

        可端点可获取服务器的公开信息，如 RSA256 公钥、SM2 公钥、Authing 服务版本号等。

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/system',
        )

    def get_country_list(self, ):
        """获取国家列表

        动态获取国家列表，可以用于前端登录页面国家选择和国际短信输入框选择，以减少前端静态资源体积。

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-country-list',
        )

    def pre_check_code(self, code_type, sms_code_payload=None, email_code_payload=None ):
        """预检验验证码是否正确

        预检测验证码是否有效，此检验不会使得验证码失效。

        Attributes:
            code_type (str): 验证码类型
            sms_code_payload (dict): 短信验证码检验参数
            email_code_payload (dict): 邮箱验证码检验参数
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/pre-check-code',
            json={
                'codeType': code_type,
                'smsCodePayload': sms_code_payload,
                'emailCodePayload': email_code_payload,
            },
        )


# ==== AUTO GENERATED AUTHENTICATION METHODS END ====