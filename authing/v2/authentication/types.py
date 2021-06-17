from ..exceptions import AuthingException
import ssl

def DEFAULT_ONERROR(code, message):
    raise AuthingException(code=code, errmsg=message)


DEFAULT_ENCRYPT_PUBLICKEY = """
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC4xKeUgQ+Aoz7TLfAfs9+paePb
5KIofVthEopwrXFkp8OCeocaTHt9ICjTT2QeJh6cZaDaArfZ873GPUn00eOIZ7Ae
+TiA2BKHbCvloW3w5Lnqm70iSsUi5Fmu9/2+68GZRH9L7Mlh8cFksCicW2Y2W2uM
GKl64GDcIq3au+aqJQIDAQAB
-----END PUBLIC KEY-----
"""


class AuthenticationClientOptions:
    def __init__(
        self,
        app_id=None,
        app_host=None,
        user_pool_id=None,
        token=None,
        host=None,
        enc_public_key=None,
        on_error=None,
        timeout=10.0,
        lang=None,
        websocket_host=None,
        protocol=None,
        secret=None,
        token_endpoint_auth_method=None,
        introspection_endpoint_auth_method=None,
        revocation_endpoint_auth_method=None,
        redirect_uri=None,
        use_unverified_ssl=False
    ):

        """
        初始化 AuthenticationClient 参数

        Args:
            app_id (str): 应用 ID
            app_host (str): 应用地址，如 https://your-app.authing.cn
            token (str): 用户的 id_token，你可以使用 id_token 初始化 SDK，从而实现记住登录的目的
            enc_public_key (str): 密码非对称加密公钥（可选），如果你使用的是 Authing 公有云服务，可以忽略；如果你使用的是私有化部署的 Authing，请联系 Authing IDaaS 服务管理员
            timeout (int): 请求超时时间，位为毫秒，默认为 10000（10 秒）
            lang (str): 接口 Message 返回语言格式（可选），可选值为 zh-CN 和 en-US，默认为 zh-CN。
            websocket_host (str): Authing Websocket 服务器域名，如果不填写，将默认为 http(s)://ws.YOUR_AUTHING_SERVER
            protocol (str): 协议类型，可选值为 oidc、oauth、saml、cas
            secret (str): 应用密钥
            token_endpoint_auth_method (str): 获取 token 端点验证方式，可选值为 client_secret_post、client_secret_basic、none，默认为 client_secret_post。
            introspection_endpoint_auth_method (str): 检验 token 端点验证方式，可选值为 `client_secret_post`、`client_secret_basic`、`none`，默认为 `client_secret_post`。
            revocation_endpoint_auth_method (str): 撤回 token 端点验证方式，可选值为 `client_secret_post`、`client_secret_basic`、`none`，默认为 `client_secret_post`。
            redirect_uri (str): 业务回调 URL
        """
        if not app_id and not user_pool_id:
            raise Exception('Please provide app_id or user_pool_id')

        self.app_id = app_id
        self.user_pool_id = user_pool_id
        self.host = app_host or host or "https://core.authing.cn"
        self.app_host = app_host
        self.on_error = on_error or DEFAULT_ONERROR
        self.timeout = timeout
        self.graphql_endpoint = "%s/graphql/v2" % self.host
        self.enc_public_key = enc_public_key or DEFAULT_ENCRYPT_PUBLICKEY
        self.token = token
        self.lang = lang
        self.websocket_host = websocket_host
        self.protocol = protocol or 'oidc'
        self.secret = secret
        self.token_endpoint_auth_method = token_endpoint_auth_method
        self.introspection_endpoint_auth_method = introspection_endpoint_auth_method
        self.revocation_endpoint_auth_method = revocation_endpoint_auth_method
        self.redirect_uri = redirect_uri
        self.use_unverified_ssl = use_unverified_ssl
