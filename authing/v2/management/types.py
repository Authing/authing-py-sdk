from ..exceptions import AuthingException

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


class ManagementClientOptions:
    def __init__(
        self,
        user_pool_id,
        secret,
        host=None,
        enc_public_key=None,
        on_error=None,
        timeout=10.0,
        lang=None,
        use_unverified_ssl=False
    ):
        # type:(str,str,str,str,any,float) -> ManagementClientOptions
        self.user_pool_id = user_pool_id
        self.secret = secret
        self.host = host or "https://core.authing.cn"
        self.on_error = on_error or DEFAULT_ONERROR
        self.timeout = timeout
        self.graphql_endpoint = "%s/graphql/v2" % self.host
        self.enc_public_key = enc_public_key or DEFAULT_ENCRYPT_PUBLICKEY
        self.lang = lang
        self.use_unverified_ssl = use_unverified_ssl

