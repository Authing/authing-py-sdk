DEFAULT_RSA_PUBLICKEY = """
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
        timeout=10.0,
        lang=None,
        use_unverified_ssl=False
    ):
        self.user_pool_id = user_pool_id
        self.secret = secret
        self.host = host or "https://core.authing.cn"
        self.timeout = timeout
        self.enc_public_key = enc_public_key or DEFAULT_RSA_PUBLICKEY
        self.lang = lang
        self.use_unverified_ssl = use_unverified_ssl

