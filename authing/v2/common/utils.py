import rsa
import base64
import string
import random
import jwt


def encrypt(plainText: str, publicKey: str):
    data = rsa.encrypt(plainText.encode('utf8'),
                       rsa.PublicKey.load_pkcs1_openssl_pem(publicKey))
    return base64.b64encode(data).decode()


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def jwt_verify(token: str, secret: str):
    result = jwt.decode(
        token,
        secret_key=secret,
        verify=False,
        algorithms='HS256'
    )
    return result
