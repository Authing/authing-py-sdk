# coding: utf-8

import rsa
import base64
import json
import re
from dateutil import parser


def encrypt(plainText, publicKey):
    # type:(str,str) -> str
    data = rsa.encrypt(
        plainText.encode("utf8"), rsa.PublicKey.load_pkcs1_openssl_pem(publicKey)
    )
    return base64.b64encode(data).decode()


def convert_udv_data_type(data):
    for i, item in enumerate(data):
        dataType, value = item["dataType"], item["value"]
        if dataType == "NUMBER":
            data[i]["value"] = json.loads(value)
        elif dataType == "BOOLEAN":
            data[i]["value"] = json.loads(value)
        elif dataType == "DATETIME":
            data[i]["value"] = parser.parse(value)
        elif dataType == "OBJECT":
            data[i]["value"] = json.loads(value)
    return data


def convert_udv_list_to_dict(data):
    data = convert_udv_data_type(data)
    ret = {}
    for item in data:
        ret[item['key']] = item['value']
    return ret


def get_hostname_from_url(url):
    p = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'
    m = re.search(p, url)
    return m.group('host')