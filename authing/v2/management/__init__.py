def DEFAULT_ONERROR(code, message):
    raise(code, message)


DEFAULT_ENCRYPT_PUBLICKEY = """
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC4xKeUgQ+Aoz7TLfAfs9+paePb
5KIofVthEopwrXFkp8OCeocaTHt9ICjTT2QeJh6cZaDaArfZ873GPUn00eOIZ7Ae
+TiA2BKHbCvloW3w5Lnqm70iSsUi5Fmu9/2+68GZRH9L7Mlh8cFksCicW2Y2W2uM
GKl64GDcIq3au+aqJQIDAQAB
-----END PUBLIC KEY-----
"""


class ManagementClientOptions():
    def __init__(self, userPoolId: str, secret: str, host=None, encPublicKey=None, onError=None, timeout=10.0):
        self.userPoolId = userPoolId
        self.secret = secret
        self.host = host or 'https://core.authing.cn'
        self.onError = onError or DEFAULT_ONERROR
        self.timeout = timeout
        self.graphqlEndpoint = '%s/v2/graphql' % self.host
        self.encPublicKey = encPublicKey or DEFAULT_ENCRYPT_PUBLICKEY
