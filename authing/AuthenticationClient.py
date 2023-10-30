# coding: utf-8

from .exceptions import AuthingWrongArgumentException
from .http.AuthenticationHttpClient import AuthenticationHttpClient
from .http.ProtocolHttpClient import ProtocolHttpClient
from .utils import get_random_string, url_join_args
import base64
import hashlib
import json
import jwt

from .utils.wss import handleMessage


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
            post_logout_redirect_uri=None,
            use_unverified_ssl=False,
            lang=None,
            websocket_host=None,
            websocket_endpoint=None,
            real_ip=None
    ):

        """
        初始化 AuthenticationClient 参数

        Args:
            app_id (str): Authing 应用 ID
            app_host (str): Authing 应用地址，如 https://your-app.authing.cn
            app_secret (str): Authing 应用密钥
            enc_public_key (str): 密码非对称加密公钥（可选），如果你使用的是 Authing 公有云服务，可以忽略；如果你使用的是私有化部署的 Authing，请联系 Authing IDaaS 服务管理员
            timeout (int): 请求超时时间，位为毫秒，默认为 10000（10 秒）
            lang (str): 接口 Message 返回语言格式（可选），可选值为 zh-CN 和 en-US，默认为 zh-CN。
            protocol (str): 协议类型，可选值为 oidc、oauth、saml、cas
            token_endpoint_auth_method (str): 获取 token 端点验证方式，可选值为 client_secret_post、client_secret_basic、none，默认为 client_secret_post。
            introspection_endpoint_auth_method (str): 检验 token 端点验证方式，可选值为 `client_secret_post`、`client_secret_basic`、`none`，默认为 `client_secret_post`。
            revocation_endpoint_auth_method (str): 撤回 token 端点验证方式，可选值为 `client_secret_post`、`client_secret_basic`、`none`，默认为 `client_secret_post`。
            redirect_uri (str): 认证完成后的重定向目标 URL。可选，默认使用控制台中配置的第一个回调地址。
            post_logout_redirect_uri(str): 登出完成后的重定向目标 URL
            real_ip (str): 客户端真实 ip，如果不传的话将一直使用服务器的 ip 作为请求 ip，这可能会影响发送验证码等接口的限流策略。
        """
        if not app_id:
            raise Exception('Please provide app_id')

        self.app_id = app_id
        self.app_host = app_host or "https://api.authing.cn"
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
        self.post_logout_redirect_uri = post_logout_redirect_uri
        self.websocket_host = websocket_host or "wss://events.authing.cn"
        self.websocket_endpoint = websocket_endpoint or "/events/v1/authentication/sub"
        self.real_ip = real_ip

        # V3 API 接口使用的 HTTP Client
        self.http_client = AuthenticationHttpClient(
            app_id=self.app_id,
            app_secret=self.app_secret,
            host=self.app_host,
            lang=self.lang,
            use_unverified_ssl=self.use_unverified_ssl,
            token_endpoint_auth_method=token_endpoint_auth_method,
            real_ip=real_ip
        )
        if self.access_token:
            self.http_client.set_access_token(self.access_token)

        # 标准协议相关接口使用的 HTTP Client
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
            bearer_token=access_token
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
        if redirect_uri and id_token:
            return "%s/oidc/session/end?id_token_hint=%s&post_logout_redirect_uri=%s" % (
                self.app_host,
                id_token,
                redirect_uri
            )
        elif (redirect_uri and not id_token) or (id_token and not redirect_uri):
            raise AuthingWrongArgumentException('must pass redirect_uri and id_token together')
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

    def build_logout_url(self, redirect_uri=None, id_token=None, state=None):
        """拼接登出 URL

        Attributes:
            redirect_uri(str): 登出完成后的重定向目标 URL
            id_token(str): 用户登录时获取的 ID Token，用于无效化用户 Token，建议传入
            state(str): 传递到目标 URL 的中间状态标识符
        """
        if not self.app_host:
            raise AuthingWrongArgumentException('must provider app_host when you init AuthenticationClient')

        if self.protocol == 'oidc':
            return self.__build_oidc_logout_url(
                id_token=id_token,
                redirect_uri=redirect_uri or self.post_logout_redirect_uri
            )
        elif self.protocol == 'cas':
            return self.__build_cas_logout_url(redirect_uri=redirect_uri)
        else:
            return self.__build_easy_logout_url(redirect_uri)

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
        self.protocol_http_client.request(
            method='POST',
            url=url,
            data={
                'client_id': self.app_id,
                'client_secret': self.app_secret,
                'token': token
            },
            raw_content=True
        )
        return True

    def __revoke_token_with_client_secret_basic(self, token):
        url = "/%s/token/revocation" % ('oidc' if self.protocol == 'oidc' else 'oauth')
        self.protocol_http_client.request(
            method='POST',
            url=url,
            data={
                'token': token
            },
            basic_token=base64.b64encode(('%s:%s' % (self.app_id, self.app_secret)).encode()).decode(),
            raw_content=True
        )
        return True

    def __revoke_token_with_none(self, token):
        url = "/%s/token/revocation" % ('oidc' if self.protocol == 'oidc' else 'oauth')
        self.protocol_http_client.request(
            method='POST',
            url=url,
            data={
                'client_id': self.app_id,
                'token': token
            },
            raw_content=True
        )
        return True

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
        在线验证 Access token 或 Refresh token 的状态。

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

    def __fetch_jwks(self, server_jwks=None):
        if server_jwks:
            return server_jwks
        else:
            keys = self.protocol_http_client.request(
                method="GET",
                url="/oidc/.well-known/jwks.json"
            )
            return keys

    def introspect_token_offline(self, token, server_jwks=None):
        """
        本地验证 Access token 或 Refresh token 的状态。

        Args:
            token (str): Access token 或 Refresh token，可以从 AuthenticationClient.get_access_token_by_code 方法的返回值中的 access_token、refresh_token 获得。
                        注意: refresh_token 只有在 scope 中包含 offline_access 才会返回。
            serverJWKS: 服务端的 JWKS 公钥，用于验证 Token 签名，默认会通过网络请求从服务端的 JWKS 端点自动获取
        """
        jwks = self.__fetch_jwks(server_jwks)
        public_keys = {}
        for jwk in jwks['keys']:
            kid = jwk['kid']
            public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
        kid = jwt.get_unverified_header(token)['kid']
        key = public_keys[kid]
        payload = jwt.decode(token, key=key, algorithms=['RS256'], audience=self.app_id)
        return payload

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

    # ==== 基于 signInByCredentials 封装的登录方式 BEGIN
    def sign_in_by_email_password(self, email, password, options=None):
        """
        使用邮箱 + 密码登录
        """
        return self.sign_in_by_credentials(
            connection="PASSWORD",
            password_payload={
                "email": email,
                "password": password,
            },
            options=options,
            client_id=self.app_id if self.token_endpoint_auth_method == 'client_secret_post' else None,
            client_secret=self.app_secret if self.token_endpoint_auth_method == 'client_secret_post' else None,
        )

    def sign_in_by_phone_password(self, phone, password, options=None):
        """
        使用手机号 + 密码登录
        """
        return self.sign_in_by_credentials(
            connection="PASSWORD",
            password_payload={
                "phone": phone,
                "password": password,
            },
            options=options,
            client_id=self.app_id if self.token_endpoint_auth_method == 'client_secret_post' else None,
            client_secret=self.app_secret if self.token_endpoint_auth_method == 'client_secret_post' else None,
        )

    def sign_in_by_username_password(self, username, password, options=None):
        """
        使用用户名 + 密码登录
        """
        return self.sign_in_by_credentials(
            connection="PASSWORD",
            password_payload={
                "username": username,
                "password": password,
            },
            options=options,
            client_id=self.app_id if self.token_endpoint_auth_method == 'client_secret_post' else None,
            client_secret=self.app_secret if self.token_endpoint_auth_method == 'client_secret_post' else None,
        )

    def sign_in_by_account_password(self, account, password, options=None):
        """
        使用账号（用户名/手机号/邮箱） + 密码登录
        """
        return self.sign_in_by_credentials(
            connection="PASSWORD",
            password_payload={
                "account": account,
                "password": password,
            },
            options=options,
            client_id=self.app_id if self.token_endpoint_auth_method == 'client_secret_post' else None,
            client_secret=self.app_secret if self.token_endpoint_auth_method == 'client_secret_post' else None,
        )

    def sign_in_by_email_passcode(self, email, pass_code, options=None):
        """
        使用邮箱 + 验证码登录
        """
        return self.sign_in_by_credentials(
            connection="PASSCODE",
            pass_code_payload={
                "email": email,
                "passCode": pass_code,
            },
            options=options,
            client_id=self.app_id if self.token_endpoint_auth_method == 'client_secret_post' else None,
            client_secret=self.app_secret if self.token_endpoint_auth_method == 'client_secret_post' else None,
        )

    def sign_in_by_phone_passcode(self, phone, pass_code, phone_country_code=None, options=None):
        """
        使用手机号 + 验证码登录
        """
        return self.sign_in_by_credentials(
            connection="PASSCODE",
            pass_code_payload={
                "phone": phone,
                "passCode": pass_code,
                "phoneCountryCode": phone_country_code
            },
            options=options,
            client_id=self.app_id if self.token_endpoint_auth_method == 'client_secret_post' else None,
            client_secret=self.app_secret if self.token_endpoint_auth_method == 'client_secret_post' else None,
        )

    def sign_in_by_ldap(self, sAMAccountName, password, options=None):
        """
        使用 LDAP 账号密码登录
        """
        return self.sign_in_by_credentials(
            connection="LDAP",
            ldap_payload={
                "sAMAccountName": sAMAccountName,
                "password": password,
            },
            options=options,
            client_id=self.app_id if self.token_endpoint_auth_method == 'client_secret_post' else None,
            client_secret=self.app_secret if self.token_endpoint_auth_method == 'client_secret_post' else None,
        )

    def sign_in_by_ad(self, sAMAccountName, password, options=None):
        """
        使用 AD 账号密码登录
        """
        return self.sign_in_by_credentials(
            connection="AD",
            ad_payload={
                "sAMAccountName": sAMAccountName,
                "password": password,
            },
            options=options,
            client_id=self.app_id if self.token_endpoint_auth_method == 'client_secret_post' else None,
            client_secret=self.app_secret if self.token_endpoint_auth_method == 'client_secret_post' else None,
        )

    # ==== 基于 signInByCredentials 封装的登录方式 BEGIN

    # ==== 基于 signup 封装的注册方式 BEGIN
    def sign_up_by_email_password(self, email, password, profile=None, options=None):
        """
        使用邮箱 + 密码注册
        """
        return self.sign_up(
            connection="PASSWORD",
            password_payload={
                "email": email,
                "password": password,
            },
            profile=profile,
            options=options
        )

    def sign_up_by_username_password(self, username, password, profile=None, options=None):
        """
        使用用户名 + 密码注册
        """
        return self.sign_up(
            connection="PASSWORD",
            password_payload={
                "username": username,
                "password": password,
            },
            profile=profile,
            options=options
        )

    def sign_up_by_email_passcode(self, email, pass_code, profile=None, options=None):
        """
        使用邮箱 + 验证码注册
        """
        return self.sign_up(
            connection="PASSCODE",
            pass_code_payload={
                "email": email,
                "passCode": pass_code,
            },
            profile=profile,
            options=options
        )

    def sign_up_by_phone_passcode(self, phone, pass_code, phone_country_code=None, profile=None, options=None):
        """
        使用手机号 + 验证码注册
        """
        return self.sign_up(
            connection="PASSCODE",
            pass_code_payload={
                "phone": phone,
                "passCode": pass_code,
                "phoneCountryCode": phone_country_code
            },
            profile=profile,
            options=options
        )

    # ==== 基于 signUp 封装的注册方式 END

    # ==== AUTO GENERATED AUTHENTICATION METHODS BEGIN ====
    def sign_up(self, connection, password_payload=None, pass_code_payload=None, profile=None, options=None):
        """注册


    此端点目前支持以下几种基于的注册方式：

    1. 基于密码（PASSWORD）：用户名 + 密码，邮箱 + 密码。
    2. 基于一次性临时验证码（PASSCODE）：手机号 + 验证码，邮箱 + 验证码。你需要先调用发送短信或者发送邮件接口获取验证码。

    社会化登录等使用外部身份源“注册”请直接使用**登录**接口，我们会在其第一次登录的时候为其创建一个新账号。


        Attributes:
            connection (str): 注册方式：
    - `PASSWORD`: 邮箱密码方式
    - `PASSCODE`: 邮箱/手机号验证码方式

            password_payload (dict): 当注册方式为 `PASSWORD` 时此参数必填。
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

    def generate_link_ext_idp_url(self, ext_idp_conn_identifier, app_id, id_token):
        """生成绑定外部身份源的链接


    此接口用于生成绑定外部身份源的链接，生成之后可以引导用户进行跳转。


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

    def unlink_ext_idp(self, ext_idp_id):
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

    def get_application_enabled_ext_idps(self, ):
        """获取应用开启的外部身份源列表

        获取应用开启的外部身份源列表，前端可以基于此渲染外部身份源按钮。

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-application-enabled-extidps',
        )

    def sign_in_by_credentials(self, connection, password_payload=None, pass_code_payload=None, ad_payload=None,
                               ldap_payload=None, options=None, client_id=None, client_secret=None):
        """使用用户凭证登录


    此端点为基于直接 API 调用形式的登录端点，适用于你需要自建登录页面的场景。**此端点暂时不支持 MFA、信息补全、首次密码重置等流程，如有需要，请使用 OIDC 标准协议认证端点。**


    注意事项：取决于你在 Authing 创建应用时选择的**应用类型**和应用配置的**换取 token 身份验证方式**，在调用此接口时需要对客户端的身份进行不同形式的验证。

    <details>
    <summary>点击展开详情</summary>

    <br>

    你可以在 [Authing 控制台](https://console.authing.cn) 的**应用** - **自建应用** - **应用详情** - **应用配置** - **其他设置** - **授权配置**
    中找到**换取 token 身份验证方式** 配置项：

    > 单页 Web 应用和客户端应用隐藏，默认为 `none`，不允许修改；后端应用和标准 Web 应用可以修改此配置项。

    ![](https://files.authing.co/api-explorer/tokenAuthMethod.jpg)

    #### 换取 token 身份验证方式为 none 时

    调用此接口不需要进行额外操作。

    #### 换取 token 身份验证方式为 client_secret_post 时

    调用此接口时必须在 body 中传递 `client_id` 和 `client_secret` 参数，作为验证客户端身份的条件。其中 `client_id` 为应用 ID、`client_secret` 为应用密钥。

    #### 换取 token 身份验证方式为 client_secret_basic 时

    调用此接口时必须在 HTTP 请求头中携带 `authorization` 请求头，作为验证客户端身份的条件。`authorization` 请求头的格式如下（其中 `client_id` 为应用 ID、`client_secret` 为应用密钥。）：

    ```
    Basic base64(<client_id>:<client_secret>)
    ```

    结果示例：

    ```
    Basic NjA2M2ZiMmYzY3h4eHg2ZGY1NWYzOWViOjJmZTdjODdhODFmODY3eHh4eDAzMjRkZjEyZGFlZGM3
    ```

    JS 代码示例：

    ```js
    'Basic ' + Buffer.from(client_id + ':' + client_secret).toString('base64');
    ```

    </details>



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
            client_id (str): 应用 ID。当应用的「换取 token 身份验证方式」配置为 `client_secret_post` 需要传。
            client_secret (str): 应用密钥。当应用的「换取 token 身份验证方式」配置为 `client_secret_post` 需要传。
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
                'client_id': client_id,
                'client_secret': client_secret,
            },
        )

    def sign_in_by_mobile(self, ext_idp_connidentifier, connection, wechat_payload=None, apple_payload=None,
                          alipay_payload=None, wechatwork_payload=None, wechatwork_agency_payload=None,
                          lark_public_payload=None, lark_internal_payload=None, lark_block_payload=None,
                          yidun_payload=None, wechat_mini_program_code_payload=None,
                          wechat_mini_program_phone_payload=None, wechat_mini_program_code_and_phone_payload=None,
                          google_payload=None, facebook_payload=None, qq_payload=None, weibo_payload=None,
                          baidu_payload=None, linked_in_payload=None, ding_talk_payload=None, github_payload=None,
                          gitee_payload=None, gitlab_payload=None, douyin_payload=None, kuaishou_payload=None,
                          xiaomi_payload=None, line_payload=None, slack_payload=None, oppo_payload=None,
                          huawei_payload=None, amazon_payload=None, options=None, client_id=None, client_secret=None):
        """使用移动端社会化登录


    此端点为移动端社会化登录接口，使用第三方移动社会化登录返回的临时凭证登录，并换取用户的 `id_token` 和 `access_token`。请先阅读相应社会化登录的接入流程。


    注意事项：取决于你在 Authing 创建应用时选择的**应用类型**和应用配置的**换取 token 身份验证方式**，在调用此接口时需要对客户端的身份进行不同形式的验证。

    <details>
    <summary>点击展开详情</summary>

    <br>

    你可以在 [Authing 控制台](https://console.authing.cn) 的**应用** - **自建应用** - **应用详情** - **应用配置** - **其他设置** - **授权配置**
    中找到**换取 token 身份验证方式** 配置项：

    > 单页 Web 应用和客户端应用隐藏，默认为 `none`，不允许修改；后端应用和标准 Web 应用可以修改此配置项。

    ![](https://files.authing.co/api-explorer/tokenAuthMethod.jpg)

    #### 换取 token 身份验证方式为 none 时

    调用此接口不需要进行额外操作。

    #### 换取 token 身份验证方式为 client_secret_post 时

    调用此接口时必须在 body 中传递 `client_id` 和 `client_secret` 参数，作为验证客户端身份的条件。其中 `client_id` 为应用 ID、`client_secret` 为应用密钥。

    #### 换取 token 身份验证方式为 client_secret_basic 时

    调用此接口时必须在 HTTP 请求头中携带 `authorization` 请求头，作为验证客户端身份的条件。`authorization` 请求头的格式如下（其中 `client_id` 为应用 ID、`client_secret` 为应用密钥。）：

    ```
    Basic base64(<client_id>:<client_secret>)
    ```

    结果示例：

    ```
    Basic NjA2M2ZiMmYzY3h4eHg2ZGY1NWYzOWViOjJmZTdjODdhODFmODY3eHh4eDAzMjRkZjEyZGFlZGM3
    ```

    JS 代码示例：

    ```js
    'Basic ' + Buffer.from(client_id + ':' + client_secret).toString('base64');
    ```

    </details>



        Attributes:
            ext_idp_connidentifier (str): 外部身份源连接标志符
            connection (str): 移动端社会化登录类型：
    - `apple`: Apple 移动端应用
    - `wechat`: 微信移动应用
    - `alipay`: 支付宝移动应用
    - `wechatwork`: 企业微信移动应用
    - `wechatwork_agency`: 企业微信移动应用（代开发模式）
    - `lark_internal`: 飞书移动端企业自建应用
    - `lark_public`: 飞书移动端应用商店应用
    - `lark_block`: 飞书小组件
    - `yidun`: 网易易盾一键登录
    - `wechat_mini_program_code`: 微信小程序使用 code 登录
    - `wechat_mini_program_phone `: 微信小程序使用手机号登录
    - `wechat_mini_program_code_and_phone `: 微信小程序使用 code 和手机号登录
    - `google`: Google 移动端社会化登录
    - `facebook`: Facebook 移动端社会化登录
    - `qq`: QQ 移动端社会化登录
    - `weibo`: 新浪微博移动端社会化登录
    - `baidu`: 百度移动端社会化登录
    - `linkedin`: LinkedIn 移动端社会化登录
    - `dingtalk`: 钉钉移动端社会化登录
    - `github`: Github 动端社会化登录
    - `gitee`: Gitee 移动端社会化登录
    - `gitlab`: GitLab 移动端社会化登录
    - `douyin`: 抖音移动端社会化登录
    - `kuaishou`: 快手移动端社会化登录
    - `xiaomi`: 小米移动端社会化登录
    - `line`: LINE 移动端社会化登录
    - `slack`: Slack 移动端社会化登录
    - `oppo`: OPPO 移动端社会化登录
    - `huawei`: 华为移动端社会化登录
    - `amazon`: 亚马逊移动端社会化登录

            wechat_payload (dict): 苹果移动端社会化登录数据，当 `connection` 为 `wechat` 的时候必填。
            apple_payload (dict): 微信移动端社会化登录数据，当 `connection` 为 `apple` 的时候必填。
            alipay_payload (dict): 支付宝移动端社会化登录数据，当 `connection` 为 `alipay` 的时候必填。
            wechatwork_payload (dict): 企业微信移动端社会化登录数据，当 `connection` 为 `wechatwork` 的时候必填。
            wechatwork_agency_payload (dict): 企业微信（代开发模式）移动端社会化登录数据，当 `connection` 为 `wechatwork_agency` 的时候必填。
            lark_public_payload (dict): 飞书应用商店应用移动端社会化登录数据，当 `connection` 为 `lark_public` 的时候必填。
            lark_internal_payload (dict): 飞书自建应用移动端社会化登录数据，当 `connection` 为 `lark_internal` 的时候必填。
            lark_block_payload (dict): 飞书小组件移动端社会化登录数据，当 `connection` 为 `lark_block` 的时候必填。
            yidun_payload (dict): 网易易盾移动端社会化登录数据，当 `connection` 为 `yidun` 的时候必填。
            wechat_mini_program_code_payload (dict): 微信小程序使用 code 登录相关数据，当 `connection` 为 `wechat_mini_program_code` 的时候必填。
            wechat_mini_program_phone_payload (dict): 微信小程序使用手机号登录相关数据，当 `connection` 为 `wechat_mini_program_phone` 的时候必填。
            wechat_mini_program_code_and_phone_payload (dict): 微信小程序使用 code 和手机号登录相关数据，当 `connection` 为 `wechat_mini_program_code_and_phone` 的时候必填。
            google_payload (dict): Google 移动端社会化登录数据，当 `connection` 为 `google` 的时候必填。
            facebook_payload (dict): Facebook 移动端社会化登录数据，当 `connection` 为 `facebook` 的时候必填。
            qq_payload (dict): QQ 移动端社会化登录数据，当 `connection` 为 `qq` 的时候必填。
            weibo_payload (dict): 新浪微博移动端社会化登录数据，当 `connection` 为 `weibo` 的时候必填。
            baidu_payload (dict): 百度移动端社会化登录数据，当 `connection` 为 `baidu` 的时候必填，且 `baiduPayload` 的属性 `code` 和 `access_token` 必选其一，优先使用 `code` 值作为授权登录方式。
            linked_in_payload (dict): LinkedIn 移动端社会化登录数据，当 `connection` 为 `linkedin` 的时候必填。
            ding_talk_payload (dict): 钉钉移动端社会化登录数据，当 `connection` 为 `dingtalk` 的时候必填。
            github_payload (dict): Github 移动端社会化登录数据，当 `connection` 为 `github` 的时候必填。
            gitee_payload (dict): Gitee 移动端社会化登录数据，当 `connection` 为 `gitee` 的时候必填。
            gitlab_payload (dict): GitLab 移动端社会化登录数据，当 `connection` 为 `gitlab` 的时候必填。
            douyin_payload (dict): 抖音移动端社会化登录数据，当 `connection` 为 `douyin` 的时候必填。
            kuaishou_payload (dict): 快手移动端社会化登录数据，当 `connection` 为 `kuaishou` 的时候必填。
            xiaomi_payload (dict): 小米移动端社会化登录数据，当 `connection` 为 `xiaomi` 的时候必填。
            line_payload (dict): LINE 移动端社会化登录数据，当 `connection` 为 `line` 的时候必填。
            slack_payload (dict): Slack 移动端社会化登录数据，当 `connection` 为 `slack` 的时候必填。
            oppo_payload (dict): OPPO 移动端社会化登录数据，当 `connection` 为 `oppo` 的时候必填。
            huawei_payload (dict): 华为移动端社会化登录数据，当 `connection` 为 `huawei` 的时候必填。
            amazon_payload (dict): 亚马逊移动端社会化登录数据，当 `connection` 为 `amazon` 的时候必填。
            options (dict): 可选参数
            client_id (str): 应用 ID。当应用的「换取 token 身份验证方式」配置为 `client_secret_post` 需要传。
            client_secret (str): 应用密钥。当应用的「换取 token 身份验证方式」配置为 `client_secret_post` 需要传。
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/signin-by-mobile',
            json={
                'extIdpConnidentifier': ext_idp_connidentifier,
                'connection': connection,
                'wechatPayload': wechat_payload,
                'applePayload': apple_payload,
                'alipayPayload': alipay_payload,
                'wechatworkPayload': wechatwork_payload,
                'wechatworkAgencyPayload': wechatwork_agency_payload,
                'larkPublicPayload': lark_public_payload,
                'larkInternalPayload': lark_internal_payload,
                'larkBlockPayload': lark_block_payload,
                'yidunPayload': yidun_payload,
                'wechatMiniProgramCodePayload': wechat_mini_program_code_payload,
                'wechatMiniProgramPhonePayload': wechat_mini_program_phone_payload,
                'wechatMiniProgramCodeAndPhonePayload': wechat_mini_program_code_and_phone_payload,
                'googlePayload': google_payload,
                'facebookPayload': facebook_payload,
                'qqPayload': qq_payload,
                'weiboPayload': weibo_payload,
                'baiduPayload': baidu_payload,
                'linkedInPayload': linked_in_payload,
                'dingTalkPayload': ding_talk_payload,
                'githubPayload': github_payload,
                'giteePayload': gitee_payload,
                'gitlabPayload': gitlab_payload,
                'douyinPayload': douyin_payload,
                'kuaishouPayload': kuaishou_payload,
                'xiaomiPayload': xiaomi_payload,
                'linePayload': line_payload,
                'slackPayload': slack_payload,
                'oppoPayload': oppo_payload,
                'huaweiPayload': huawei_payload,
                'amazonPayload': amazon_payload,
                'options': options,
                'client_id': client_id,
                'client_secret': client_secret,
            },
        )

    def switch_login_by_user(self, target_user_id, options=None):
        """公共账号切换登录

        允许个人账号与关联的公共账号间做切换登录，此端点要求账号已登录

        Attributes:
            target_user_id (str): 切换登录目标用户 ID
            options (dict): 可选参数
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/switch-login-by-user',
            json={
                'targetUserId': target_user_id,
                'options': options,
            },
        )

    def get_alipay_auth_info(self, ext_idp_connidentifier):
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

    def gene_qr_code(self, type, ext_idp_conn_id=None, custom_data=None, context=None, auto_merge_qr_code=None):
        """生成用于登录的二维码

        生成用于登录的二维码，目前支持生成微信公众号扫码登录、小程序扫码登录、自建移动 APP 扫码登录的二维码。

        Attributes:
            type (str): 二维码类型。当前支持三种类型：
    - `MOBILE_APP`: 自建移动端 APP 扫码
    - `WECHAT_MINIPROGRAM`: 微信小程序扫码
    - `WECHAT_OFFICIAL_ACCOUNT` 关注微信公众号扫码
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

    def check_qr_code_status(self, qrcode_id):
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

    def exchange_token_set_with_qr_code_ticket(self, ticket, client_id=None, client_secret=None):
        """使用二维码 ticket 换取 TokenSet


    此端点为使用二维码的 ticket 换取用户的 `access_token` 和 `id_token`。


    注意事项：取决于你在 Authing 创建应用时选择的**应用类型**和应用配置的**换取 token 身份验证方式**，在调用此接口时需要对客户端的身份进行不同形式的验证。

    <details>
    <summary>点击展开详情</summary>

    <br>

    你可以在 [Authing 控制台](https://console.authing.cn) 的**应用** - **自建应用** - **应用详情** - **应用配置** - **其他设置** - **授权配置**
    中找到**换取 token 身份验证方式** 配置项：

    > 单页 Web 应用和客户端应用隐藏，默认为 `none`，不允许修改；后端应用和标准 Web 应用可以修改此配置项。

    ![](https://files.authing.co/api-explorer/tokenAuthMethod.jpg)

    #### 换取 token 身份验证方式为 none 时

    调用此接口不需要进行额外操作。

    #### 换取 token 身份验证方式为 client_secret_post 时

    调用此接口时必须在 body 中传递 `client_id` 和 `client_secret` 参数，作为验证客户端身份的条件。其中 `client_id` 为应用 ID、`client_secret` 为应用密钥。

    #### 换取 token 身份验证方式为 client_secret_basic 时

    调用此接口时必须在 HTTP 请求头中携带 `authorization` 请求头，作为验证客户端身份的条件。`authorization` 请求头的格式如下（其中 `client_id` 为应用 ID、`client_secret` 为应用密钥。）：

    ```
    Basic base64(<client_id>:<client_secret>)
    ```

    结果示例：

    ```
    Basic NjA2M2ZiMmYzY3h4eHg2ZGY1NWYzOWViOjJmZTdjODdhODFmODY3eHh4eDAzMjRkZjEyZGFlZGM3
    ```

    JS 代码示例：

    ```js
    'Basic ' + Buffer.from(client_id + ':' + client_secret).toString('base64');
    ```

    </details>



        Attributes:
            ticket (str): 当二维码状态为已授权时返回。如果在控制台应用安全 - 通用安全 - 登录安全 - APP 扫码登录 Web 安全中未开启「Web 轮询接口返回完整用户信息」（默认处于关闭状态），会返回此 ticket，用于换取完整的用户信息。
            client_id (str): 应用 ID。当应用的「换取 token 身份验证方式」配置为 `client_secret_post` 需要传。
            client_secret (str): 应用密钥。当应用的「换取 token 身份验证方式」配置为 `client_secret_post` 需要传。
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/exchange-tokenset-with-qrcode-ticket',
            json={
                'ticket': ticket,
                'client_id': client_id,
                'client_secret': client_secret,
            },
        )

    def change_qr_code_status(self, action, qrcode_id):
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

    def sign_in_by_push(self, account, options=None):
        """推送登录

        推送登录。

        Attributes:
            account (str): 用户账号（用户名/手机号/邮箱）
            options (dict): 可选参数
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/signin-by-push',
            json={
                'account': account,
                'options': options,
            },
        )

    def check_push_code_status(self, push_code_id):
        """查询推送码状态

        按照推送码使用顺序，共分为已推送、等待用户 同意/取消 授权、推送码过期以及未知错误五种状态，前端应该通过不同的状态给到用户不同的反馈。

        Attributes:
            pushCodeId (str): 推送码（推送登录唯一 ID）
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/check-pushcode-status',
            params={
                'pushCodeId': push_code_id,
            },
        )

    def change_push_code_status(self, action, push_code_id):
        """推送登录：APP 端修改推送码状态

        此端点用于在 Authing 令牌 APP 推送登录中修改推送码状态，对应着在浏览器使用推送登录，点击登录之后，终端用户收到推送登录信息，确认授权、取消授权的过程。**此接口要求具备用户的登录态**。

        Attributes:
            action (str): 修改推送码状态的动作:
    - `CONFIRM`: 修改推送码状态为已授权；
    - `CANCEL`: 修改推送码状态为已取消；

            push_code_id (str): 推送码（推送登录唯一 ID）
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/change-pushcode-status',
            json={
                'action': action,
                'pushCodeId': push_code_id,
            },
        )

    def send_sms(self, channel, phone_number, phone_country_code=None):
        """发送短信

        发送短信时必须指定短信 Channel，每个手机号同一 Channel 在一分钟内只能发送一次。

        Attributes:
            channel (str): 短信通道，指定发送此短信的目的：
    - `CHANNEL_LOGIN`: 用于用户登录
    - `CHANNEL_REGISTER`: 用于用户注册
    - `CHANNEL_RESET_PASSWORD`: 用于重置密码
    - `CHANNEL_BIND_PHONE`: 用于绑定手机号
    - `CHANNEL_UNBIND_PHONE`: 用于解绑手机号
    - `CHANNEL_BIND_MFA`: 用于绑定 MFA
    - `CHANNEL_VERIFY_MFA`: 用于验证 MFA
    - `CHANNEL_UNBIND_MFA`: 用于解绑 MFA
    - `CHANNEL_COMPLETE_PHONE`: 用于在注册/登录时补全手机号信息
    - `CHANNEL_IDENTITY_VERIFICATION`: 用于进行用户实名认证
    - `CHANNEL_DELETE_ACCOUNT`: 用于注销账号

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

    def send_email(self, channel, email):
        """发送邮件

        发送邮件时必须指定邮件 Channel，每个邮箱同一 Channel 在一分钟内只能发送一次。

        Attributes:
            channel (str): 短信通道，指定发送此短信的目的：
    - `CHANNEL_LOGIN`: 用于用户登录
    - `CHANNEL_REGISTER`: 用于用户注册
    - `CHANNEL_RESET_PASSWORD`: 用于重置密码
    - `CHANNEL_VERIFY_EMAIL_LINK`: 用于验证邮箱地址
    - `CHANNEL_UPDATE_EMAIL`: 用于修改邮箱
    - `CHANNEL_BIND_EMAIL`: 用于绑定邮箱
    - `CHANNEL_UNBIND_EMAIL`: 用于解绑邮箱
    - `CHANNEL_VERIFY_MFA`: 用于验证 MFA
    - `CHANNEL_UNLOCK_ACCOUNT`: 用于自助解锁
    - `CHANNEL_COMPLETE_EMAIL`: 用于注册/登录时补全邮箱信息
    - `CHANNEL_DELETE_ACCOUNT`: 用于注销账号

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

    def decrypt_wechat_mini_program_data(self, code, iv, encrypted_data, ext_idp_connidentifier):
        """解密微信小程序数据

        解密微信小程序数据

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

    def get_wechat_mp_access_token(self, app_id, app_secret):
        """获取微信小程序、公众号 Access Token

        获取 Authing 服务器缓存的微信小程序、公众号 Access Token（废弃，请使用 /api/v3/get-wechat-access-token-info）

        Attributes:
            app_id (str): 微信小程序或微信公众号的 AppId
            app_secret (str): 微信小程序或微信公众号的 AppSecret
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-wechat-access-token',
            json={
                'appId': app_id,
                'appSecret': app_secret,
            },
        )

    def get_wechat_mp_access_token_info(self, app_id, app_secret):
        """获取微信小程序、公众号 Access Token

        获取 Authing 服务器缓存的微信小程序、公众号 Access Token

        Attributes:
            app_id (str): 微信小程序或微信公众号的 AppId
            app_secret (str): 微信小程序或微信公众号的 AppSecret
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-wechat-access-token-info',
            json={
                'appId': app_id,
                'appSecret': app_secret,
            },
        )

    def get_login_history(self, app_id=None, client_ip=None, success=None, start=None, end=None, page=None, limit=None):
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
            url='/api/v3/get-my-login-history',
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
            url='/api/v3/get-my-logged-in-apps',
        )

    def get_accessible_apps(self, ):
        """获取具备访问权限的应用

        获取具备访问权限的应用

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-my-accessible-apps',
        )

    def get_tenant_list(self, ):
        """获取租户列表

        获取租户列表

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-my-tenant-list',
        )

    def get_role_list(self, namespace=None):
        """获取角色列表

        获取角色列表

        Attributes:
            namespace (str): 所属权限分组(权限空间)的 Code
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-my-role-list',
            params={
                'namespace': namespace,
            },
        )

    def get_group_list(self, ):
        """获取分组列表

        获取分组列表

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-my-group-list',
        )

    def get_department_list(self, page=None, limit=None, with_custom_data=None, sort_by=None, order_by=None):
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
            url='/api/v3/get-my-department-list',
            params={
                'page': page,
                'limit': limit,
                'withCustomData': with_custom_data,
                'sortBy': sort_by,
                'orderBy': order_by,
            },
        )

    def get_authorized_resources(self, namespace=None, resource_type=None):
        """获取被授权的资源列表

        此接口用于获取用户被授权的资源列表。

        Attributes:
            namespace (str): 所属权限分组(权限空间)的 Code
            resourceType (str): 资源类型，如 数据、API、菜单、按钮
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-my-authorized-resources',
            params={
                'namespace': namespace,
                'resourceType': resource_type,
            },
        )

    def get_profile(self, with_custom_data=None, with_identities=None, with_department_ids=None):
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

    def update_profile(self, name=None, nickname=None, photo=None, external_id=None, birthdate=None, country=None,
                       province=None, city=None, address=None, street_address=None, postal_code=None, gender=None,
                       username=None, company=None, custom_data=None, identity_number=None):
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
            company (str): 所在公司
            custom_data (dict): 自定义数据，传入的对象中的 key 必须先在用户池定义相关自定义字段
            identity_number (str): 用户身份证号码
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
                'company': company,
                'customData': custom_data,
                'identityNumber': identity_number,
            },
        )

    def bind_email(self, pass_code, email):
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

    def unbind_email(self, pass_code):
        """解绑邮箱

        用户解绑邮箱，如果用户没有绑定其他登录方式（手机号、社会化登录账号），将无法解绑邮箱，会提示错误。

        Attributes:
            pass_code (str): 邮箱验证码，需要先调用**发送邮件**接口接收验证码。
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/unbind-email',
            json={
                'passCode': pass_code,
            },
        )

    def bind_phone(self, pass_code, phone_number, phone_country_code=None):
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

    def unbind_phone(self, pass_code):
        """解绑手机号

        用户解绑手机号，如果用户没有绑定其他登录方式（邮箱、社会化登录账号），将无法解绑手机号，会提示错误。

        Attributes:
            pass_code (str): 短信验证码，需要先调用**发送短信**接口接收验证码。
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/unbind-phone',
            json={
                'passCode': pass_code,
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

    def update_password(self, new_password, old_password=None, password_encrypt_type=None):
        """修改密码

        此端点用于用户自主修改密码，如果用户之前已经设置密码，需要提供用户的原始密码作为凭证。如果用户忘记了当前密码，请使用**忘记密码**接口。

        Attributes:
            new_password (str): 新密码
            old_password (str): 原始密码，如果用户当前设置了密码，此参数必填。
            password_encrypt_type (str): 密码加密类型，支持使用 RSA256 和国密 SM2 算法进行加密。默认为 `none` 不加密。
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

    def verify_update_email_request(self, email_pass_code_payload, verify_method):
        """发起修改邮箱的验证请求

        终端用户自主修改邮箱时，需要提供相应的验证手段。此接口用于验证用户的修改邮箱请求是否合法。当前支持通过**邮箱验证码**的方式进行验证，你需要先调用发送邮件接口发送对应的邮件验证码。

        Attributes:
            email_pass_code_payload (dict): 使用邮箱验证码方式验证的数据
            verify_method (str): 修改当前邮箱使用的验证手段：
    - `EMAIL_PASSCODE`: 通过邮箱验证码进行验证，当前只支持这种验证方式。

        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/verify-update-email-request',
            json={
                'emailPassCodePayload': email_pass_code_payload,
                'verifyMethod': verify_method,
            },
        )

    def update_email(self, update_email_token):
        """修改邮箱

        终端用户自主修改邮箱，需要提供相应的验证手段，见[发起修改邮箱的验证请求](#tag/用户资料/API%20列表/operation/ProfileV3Controller_verifyUpdateEmailRequest)。
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

    def verify_update_phone_request(self, phone_pass_code_payload, verify_method):
        """发起修改手机号的验证请求

        终端用户自主修改手机号时，需要提供相应的验证手段。此接口用于验证用户的修改手机号请求是否合法。当前支持通过**短信验证码**的方式进行验证，你需要先调用发送短信接口发送对应的短信验证码。

        Attributes:
            phone_pass_code_payload (dict): 使用手机号验证码方式验证的数据
            verify_method (str): 修改手机号的验证方式：
    - `PHONE_PASSCODE`: 使用短信验证码的方式进行验证，当前仅支持这一种方式。

        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/verify-update-phone-request',
            json={
                'phonePassCodePayload': phone_pass_code_payload,
                'verifyMethod': verify_method,
            },
        )

    def update_phone(self, update_phone_token):
        """修改手机号

        终端用户自主修改手机号，需要提供相应的验证手段，见[发起修改手机号的验证请求](#tag/用户资料/API%20列表/operation/ProfileV3Controller_updatePhoneVerification)。
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

    def verify_reset_password_request(self, verify_method, phone_pass_code_payload=None, email_pass_code_payload=None):
        """发起忘记密码请求

        当用户忘记密码时，可以通过此端点找回密码。用户需要使用相关验证手段进行验证，目前支持**邮箱验证码**和**手机号验证码**两种验证手段。

        Attributes:
            verify_method (str): 忘记密码请求使用的验证手段：
    - `EMAIL_PASSCODE`: 通过邮箱验证码进行验证
    - `PHONE_PASSCODE`: 通过手机号验证码进行验证

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

    def reset_password(self, password, password_reset_token, password_encrypt_type=None):
        """忘记密码

        此端点用于用户忘记密码之后，通过**手机号验证码**或者**邮箱验证码**的方式重置密码。此接口需要提供用于重置密码的临时凭证 `passwordResetToken`，此参数需要通过**发起忘记密码请求**接口获取。

        Attributes:
            password (str): 密码
            password_reset_token (str): 重置密码的 token
            password_encrypt_type (str): 密码加密类型，支持使用 RSA256 和国密 SM2 算法进行加密。默认为 `none` 不加密。
    - `none`: 不对密码进行加密，使用明文进行传输。
    - `rsa`: 使用 RSA256 算法对密码进行加密，需要使用 Authing 服务的 RSA 公钥进行加密，请阅读**介绍**部分了解如何获取 Authing 服务的 RSA256 公钥。
    - `sm2`: 使用 [国密 SM2 算法](https://baike.baidu.com/item/SM2/15081831) 对密码进行加密，需要使用 Authing 服务的 SM2 公钥进行加密，请阅读**介绍**部分了解如何获取 Authing 服务的 SM2 公钥。

        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/reset-password',
            json={
                'password': password,
                'passwordResetToken': password_reset_token,
                'passwordEncryptType': password_encrypt_type,
            },
        )

    def verify_delete_account_request(self, verify_method, phone_pass_code_payload=None, email_pass_code_payload=None,
                                      password_payload=None):
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

    def delete_account(self, delete_account_token):
        """注销账户

        此端点用于用户自主注销账号，需要提供用于注销账号的临时凭证 deleteAccountToken，此参数需要通过**发起注销账号请求**接口获取。

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

    def list_public_accounts_for_switch_logged_in(self, with_origin_user=None):
        """查询当前登录用户可切换登录的公共账号列表

        此端点用于查询当前登录用户可切换登录的公共账号列表，如果没有可切换登录的公共账号，则返回空数组。

        Attributes:
            withOriginUser (bool): 是否包含当前个人用户基本信息
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-select-login-public-accounts',
            params={
                'withOriginUser': with_origin_user,
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

    def check_permission_by_string_resource(self, resources, action):
        """字符串类型资源鉴权

        字符串类型资源鉴权，支持用户对一个或者多个字符串资源进行权限判断

        Attributes:
            resources (list): 字符串数据资源路径列表,
            action (str): 数据资源权限操作, read、get、write 等动作
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/check-permission-string-resource',
            json={
                'resources': resources,
                'action': action,
            },
        )

    def check_permission_by_array_resource(self, resources, action):
        """数组类型资源鉴权

        数组类型资源鉴权，支持用户对一个或者多个数组资源进行权限判断

        Attributes:
            resources (list): 数组数据资源路径列表,
            action (str): 数据资源权限操作, read、get、write 等动作
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/check-permission-array-resource',
            json={
                'resources': resources,
                'action': action,
            },
        )

    def check_permission_by_tree_resource(self, resources, action):
        """树类型资源鉴权

        树类型资源鉴权，支持用户对一个或者多个树资源进行权限判断

        Attributes:
            resources (list): 树数据资源路径列表,
            action (str): 数据资源权限操作, read、get、write 等动作
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/check-permission-tree-resource',
            json={
                'resources': resources,
                'action': action,
            },
        )

    def get_user_authorized_resources_list(self, ):
        """获取用户在登录应用下被授权资源列表

        获取用户指定资源权限列表，用户获取在某个应用下所拥有的资源列表。

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-auth-resource-list',
        )

    def get_user_auth_resource_permission_list(self, resources):
        """获取用户指定资源权限列表

        获取用户指定资源的权限列表,用户获取某个应用下指定资源的权限列表。

        Attributes:
            resources (list): 数据资源路径列表,**树资源需到具体树节点**
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-user-auth-resource-permission-list',
            json={
                'resources': resources,
            },
        )

    def get_user_auth_resource_struct(self, resource):
        """获取用户授权资源的结构列表

        获取用户授权的资源列表，用户获取某个应用下的某个资源所授权的结构列表，通过不同的资源类型返回对应资源的授权列表。

        Attributes:
            resource (str): 数据资源 Code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-user-auth-resource-struct',
            json={
                'resource': resource,
            },
        )

    def init_authentication_options(self, ):
        """获取 WebAuthn 认证请求初始化参数

        获取 WebAuthn 认证请求初始化参数

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/webauthn/authentication',
        )

    def verify_authentication(self, ticket, authentication_credential, options=None):
        """验证 WebAuthn 认证请求凭证

        验证 WebAuthn 认证请求凭证

        Attributes:
            ticket (str): 从 获取 WebAuthn 认证请求初始化参数接口 获得的 ticket
            authentication_credential (dict): 认证器凭证信息
            options (dict): 可选参数
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/webauthn/authentication',
            json={
                'ticket': ticket,
                'authenticationCredential': authentication_credential,
                'options': options,
            },
        )

    def init_register_options(self, ):
        """获取 webauthn 凭证创建初始化参数

        获取 webauthn 凭证创建初始化参数。**此接口要求具备用户的登录态**

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/webauthn/registration',
        )

    def verify_register(self, ticket, registration_credential, authenticator_code=None):
        """验证 webauthn 绑定注册认证器凭证

        验证 webauthn 绑定注册认证器凭证

        Attributes:
            ticket (str): 获取凭证创建初始化参数时的 ticket
            registration_credential (dict): 绑定认证器凭证信息
            authenticator_code (str): 凭证信息类型：
    - `FINGERPRINT`: 指纹
    - `FACE`: 人脸
    - `OTHER` 其他
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/webauthn/registration',
            json={
                'ticket': ticket,
                'registrationCredential': registration_credential,
                'authenticatorCode': authenticator_code,
            },
        )

    def list(self, page=None, limit=None):
        """我的设备列表

        我登录过的设备列表。

        Attributes:
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/mydevices/list',
            params={
                'page': page,
                'limit': limit,
            },
        )

    def unbind(self, device_id):
        """移除设备

        移除某个设备。

        Attributes:
            device_id (str): 设备唯一标识
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/mydevices/unbind',
            json={
                'deviceId': device_id,
            },
        )

    def revoke(self, device_id):
        """从设备上退出登录

        移除某个已登录设备的登录态。

        Attributes:
            device_id (str): 设备唯一标识
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/mydevices/revoke-session',
            json={
                'deviceId': device_id,
            },
        )

    def auth_by_code_identity(self, code, app_id=None, conn_id=None, options=None):
        """微信移动端登录

        移动端应用：使用微信作为外部身份源登录。

        Attributes:
            code (str): 客户端微信授权成功，微信返回当前认证授权码
            app_id (str): 应用 ID
            conn_id (str): 身份源连接 ID
            options (dict): 登录参数
        """
        return self.http_client.request(
            method='POST',
            url='/api/v2/ecConn/wechatMobile/authByCodeIdentity',
            json={
                'code': code,
                'appId': app_id,
                'connId': conn_id,
                'options': options,
            },
        )

    def register_new_user(self, key, action):
        """微信移动端：使用身份源中用户信息

        询问绑定开启时：绑定到外部身份源，根据外部身份源中的用户信息创建用户后绑定到当前身份源并登录。

        Attributes:
            key (str): 中间态键
            action (str): 操作编码
        """
        return self.http_client.request(
            method='POST',
            url='/api/v2/ecConn/wechatMobile/register',
            json={
                'key': key,
                'action': action,
            },
        )

    def bind_by_email_code(self, key, action, code, email):
        """微信移动端：邮箱验证码模式

        询问绑定开启时：绑定到外部身份源，根据输入的邮箱验证用户信息，找到对应的用户后绑定到当前身份源并登录；找不到时报错“用户不存在”。

        Attributes:
            key (str): 中间态键
            action (str): 操作编码
            code (str): 邮箱验证码（四位：1234；六位：123456）
            email (str): 邮箱
        """
        return self.http_client.request(
            method='POST',
            url='/api/v2/ecConn/wechatMobile/byEmailCode',
            json={
                'key': key,
                'action': action,
                'code': code,
                'email': email,
            },
        )

    def bind_by_phone_code(self, key, action, code, phone, phone_country_code=None):
        """微信移动端：手机号验证码模式

        询问绑定开启时：绑定到外部身份源，根据输入的手机验证用户信息，找到对应的用户后绑定到当前身份源并登录；找不到时报错“用户不存在”。

        Attributes:
            key (str): 中间态键
            action (str): 操作编码
            code (str): 手机验证码（四位：1234；六位：123456）
            phone (str): 手机号
            phone_country_code (str): 国家码（标准格式：加号“+”加国家码数字；当前校验兼容历史用户输入习惯。例，中国国家码标准格式为「+86」，历史用户输入记录中存在「86、086、0086」等格式）
        """
        return self.http_client.request(
            method='POST',
            url='/api/v2/ecConn/wechatMobile/byPhoneCode',
            json={
                'key': key,
                'action': action,
                'code': code,
                'phone': phone,
                'phoneCountryCode': phone_country_code,
            },
        )

    def bind_by_account(self, key, action, password, account):
        """微信移动端：账号密码模式

        询问绑定开启时：绑定到外部身份源，根据输入的账号（用户名/手机号/邮箱）密码验证用户信息，找到对应的用户后绑定到当前身份源并登录；找不到时报错“用户不存在”。

        Attributes:
            key (str): 中间态键
            action (str): 操作编码
            password (str): 账号密码
            account (str): 账号（手机/邮箱/用户名）
        """
        return self.http_client.request(
            method='POST',
            url='/api/v2/ecConn/wechatMobile/byAccount',
            json={
                'key': key,
                'action': action,
                'password': password,
                'account': account,
            },
        )

    def select_account(self, key, action, account):
        """微信移动端：多账号场景

        询问绑定开启时：根据选择的账号绑定外部身份源，根据输入的账号 ID 验证用户信息，找到对应的用户后绑定到当前身份源并登录；找不到时报错“用户不存在”。

        Attributes:
            key (str): 中间态键
            action (str): 操作编码
            account (str): 账号 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v2/ecConn/wechatMobile/select',
            json={
                'key': key,
                'action': action,
                'account': account,
            },
        )

    def bind_by_account_id(self, key, action, account_id):
        """微信移动端：账号 ID 模式

        询问绑定开启时：绑定到外部身份源，根据输入的账号 ID 验证用户信息，找到对应的用户后绑定到当前身份源并登录；找不到时报错“用户不存在”。

        Attributes:
            key (str): 中间态键
            action (str): 操作编码
            account_id (str): 账号 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v2/ecConn/wechatMobile/byAccountId',
            json={
                'key': key,
                'action': action,
                'accountId': account_id,
            },
        )

    def get_push_login_relation_apps(self, app_id, push_code_id):
        """获取推送登录请求关联的客户端应用

        此端点用于在 Authing 令牌 APP 收到推送登录通知时，可检查当前用户登录的应用是否支持对推送登录请求进行授权。

        Attributes:
            app_id (str): 发起推送登录的应用 ID
            push_code_id (str): 推送码（推送登录唯一 ID）
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-pushlogin-relation-apps',
            json={
                'appId': app_id,
                'pushCodeId': push_code_id,
            },
        )

    def gene_fastpass_qrcode_info(self, options=None):
        """获取快速认证二维码数据

        此端点用于在用户个人中心，获取快速认证参数生成二维码，可使用 Authing 令牌 APP 扫码，完成快速认证。**此接口要求具备用户的登录态**。

        Attributes:
            options (dict): 可选参数
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/gene-fastpass-qrcode-info',
            json={
                'options': options,
            },
        )

    def get_fastpass_params(self, qrcode_id, app_id):
        """获取快速认证的应用列表

        此端点用于使用 Authing 令牌 APP 扫「用户个人中心」-「快速认证」二维码后，拉取可快速认证的客户端应用列表。

        Attributes:
            qrcodeId (str):
            appId (str):
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-fastpass-client-apps',
            params={
                'qrcodeId': qrcode_id,
                'appId': app_id,
            },
        )

    def get_qr_code_status(self, qrcode_id):
        """查询个人中心「快速认证二维码」的状态

        按照用户扫码顺序，共分为未扫码、已扫码、已登录、二维码过期以及未知错误五种状态，前端应该通过不同的状态给到用户不同的反馈。

        Attributes:
            qrcodeId (str): 二维码唯一 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-app-login-qrcode-status',
            params={
                'qrcodeId': qrcode_id,
            },
        )

    def qr_code_app_login(self, action, qrcode_id):
        """APP 端扫码登录

        此端点用于在授权使 APP 成功扫码登录中，对应着在「个人中心」-「快速认证」页面渲染出二维码，终端用户扫码并成功登录的过程。

        Attributes:
            action (str): APP 扫二维码登录:
    - `APP_LOGIN`: APP 扫码登录；

            qrcode_id (str): 二维码唯一 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/qrcode-app-login',
            json={
                'action': action,
                'qrcodeId': qrcode_id,
            },
        )

    def pre_check_code(self, code_type, sms_code_payload=None, email_code_payload=None):
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

    def list_credentials_by_page(self, ):
        """



        Attributes:
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/webauthn/page-authenticator-device',
            json={
            },
        )

    def check_valid_credentials_by_cred_ids(self, ):
        """



        Attributes:
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/webauthn/check-valid-credentials-by-credIds',
            json={
            },
        )

    def remove_all_credentials(self, ):
        """



        Attributes:
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/webauthn/remove-credentials-by-authenticator-code',
            json={
            },
        )

    def remove_credential(self, ):
        """



        Attributes:
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/webauthn/remove-credential/{credentialID}',
            json={
            },
        )

    def verify_mfa_token(self, token):
        """验证 MFA Token

        验证 MFA Token

        Attributes:
            token (str): `mfa_token` 的值
        """
        return self.http_client.request(
            method='POST',
            url='/mfa/token/introspection',
        )

    def send_enroll_factor_request(self, profile, factor_type):
        """发起绑定 MFA 认证要素请求

        当用户未绑定某个 MFA 认证要素时，可以发起绑定 MFA 认证要素请求。不同类型的 MFA 认证要素绑定请求需要发送不同的参数，详细见 profile 参数。发起验证请求之后，Authing 服务器会根据相应的认证要素类型和传递的参数，使用不同的手段要求验证。此接口会返回 enrollmentToken，你需要在请求「绑定 MFA 认证要素」接口时带上此 enrollmentToken，并提供相应的凭证。

        Attributes:
            profile (dict): MFA 认证要素详细信息
            factor_type (str): MFA 认证要素类型：
    - `OTP`: OTP
    - `SMS`: 短信
    - `EMAIL`: 邮件
    - `FACE`: 人脸

        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/send-enroll-factor-request',
            json={
                'profile': profile,
                'factorType': factor_type,
            },
        )

    def enroll_factor(self, enrollment_data, enrollment_token, factor_type):
        """绑定 MFA 认证要素

        绑定 MFA 要素。

        Attributes:
            enrollment_data (dict): 绑定 MFA 认证要素时，对应认证要素要求的验证信息。
            enrollment_token (str): 「发起绑定 MFA 认证要素请求」接口返回的 enrollmentToken，此 token 有效时间为一分钟。
            factor_type (str): MFA 认证要素类型：
    - `OTP`: OTP
    - `SMS`: 短信
    - `EMAIL`: 邮件
    - `FACE`: 人脸

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

    def reset_factor(self, factor_id):
        """解绑 MFA 认证要素

        根据 Factor ID 解绑用户绑定的某个 MFA 认证要素。

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

        Authing 目前支持四种类型的 MFA 认证要素：手机短信、邮件验证码、OTP、人脸。

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-enrolled-factors',
        )

    def get_factor(self, factor_id):
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

    def mfa_otp_verify(self, totp):
        """校验用户 MFA 绑定的 OTP

        校验用户 MFA 绑定的 OTP。

        Attributes:
            totp (str): OTP 口令
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/mfa-totp-verify',
            json={
                'totp': totp,
            },
        )

    # ==== AUTO GENERATED AUTHENTICATION METHODS END ====
    def sub_event(self, event_code, callback):
        """订阅事件

        订阅 authing 公共事件或自定义事件

        Attributes:
            eventCode (str): 事件编码
            callback (callable): 回调函数
        """
        assert event_code, "eventCode 不能为空"
        assert self.access_token, "access_token 不能为空"
        assert callable(callback), "callback 必须为可执行函数"
        eventUri = self.websocket_host + \
                   self.websocket_endpoint + \
                   "?code=" + event_code + \
                   "&token=" + self.access_token
        print("eventUri:" + eventUri)
        handleMessage(eventUri, callback)

    def put_event(self, event_code, data):
        """发布自定义事件

        发布事件

        Attributes:
            event_code (str): 事件编码
            data (json): 事件体
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/pub-userEvent",
            json={
                "eventType": event_code,
                "eventData": json.dumps(data)
            },
        )
