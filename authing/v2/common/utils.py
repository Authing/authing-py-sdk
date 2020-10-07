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


def get_random_phone_number():
    # 第二位数
    second = [3, 4, 5, 7, 8][random.randint(0, 4)]
    # 第三位数
    third = {
        3: random.randint(0, 9),
        4: [5, 7][random.randint(0, 1)],
        5: [i for i in range(0, 10) if i != 4][random.randint(0, 8)],
        7: [6, 7, 8][random.randint(0, 2)],
        8: random.randint(0, 9)
    }[second]
    # 后八位数
    suffix = ''
    for j in range(0, 8):
        suffix = suffix + str(random.randint(0, 9))

    return "1{}{}{}".format(second, third, suffix)


def jwt_verify(token: str, secret: str):
    result = jwt.decode(
        token,
        secret_key=secret,
        verify=False,
        algorithms='HS256'
    )
    return result