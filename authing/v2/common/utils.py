# coding: utf-8
import rsa
import base64
import json
import re
import string
import random
from dateutil import parser

try:
    # python 3
    from urllib.parse import urlencode
except:
    # python 2
    from urllib import urlencode


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


def convert_nested_pagination_custom_data_list_to_dict(data):
    lst = data['list']
    for user in lst:
        user['customData'] = convert_udv_list_to_dict(user['customData'])


def get_hostname_from_url(url):
    p = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'
    m = re.search(p, url)
    return m.group('host')


def url_join_args(api, query=None, **kwargs):
    result = api
    if not result.endswith('?') and (query or kwargs):
        result = api + '?'
    if query:
        result = result + urlencode(query)
    if kwargs:
        if query:
            result = result + '&' + urlencode(kwargs)
        else:
            result = result + urlencode(kwargs)
    return result


def camel_to_snake(string):
    string = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    string = re.sub('(.)([0-9]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', string).lower()


def format_authorized_resources(arr):
    def func(item):
        for key in list(item.keys()):
            if not item[key]:
                del item[key]
        return item

    arr = list(map(func, arr))
    return arr


def get_random_string(length=10):
    # type:(int) -> str
    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str
