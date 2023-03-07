# coding: utf-8

def composeStringToSign(method, uri=None, headers=None, queries=None):
    '''
        StringBuilder sb = new StringBuilder();
        sb.append(method).append(HEADER_SEPARATOR);
        List<String> list = headers.keySet().stream().sorted().collect(Collectors.toList());
        for (String s : list) {
            sb.append(s).append(":").append(headers.get(s)).append(HEADER_SEPARATOR);
        }
        sb.append(buildQueryString(uri, queries));
        return sb.toString();
    '''
    if method:
        return method+"\n" # websocket 没有用到 uri, headers, queries 这几个参数，暂时不实现

import base64
import hmac
from hashlib import sha1

def getAuthorization(accessKeyId, accessKeySecret):
    signa = composeStringToSign("websocket")
    signature = signString(accessKeySecret, signa)
    return "authing " + accessKeyId + ":" + signature

def signString(key, code):
    hmac_code = hmac.new(key.encode(), code.encode(), sha1).digest()
    return base64.b64encode(hmac_code).decode()

if __name__ == '__main__':
    print(getAuthorization("63f60a8e31e6ebd92080dc7d","00711487506bc4a92cfada3520b76d7f"))
