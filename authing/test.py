import random
import pytest
from authing import Authing

test_name = ''
user_id = ''
email = "fuergaosi@qq.com"
username = "holegots"
password = "123456"
phone = "17624555576"
phoneCode = 1234
clientId = '5de935b82a709748e17681f0'
secret = 'cfb8a38a52f3a0bec44602b0c0e4518d'
code = ''
authing = None
authing = Authing(clientId, secret, {
    "oauth": 'https://oauth.authing.cn/graphql',
    "users": 'https://users.authing.cn/graphql',
})


def test_list():
    _list = authing.list()
    assert not _list.get('errors')


def test_loginResult_with_email():
    loginResult = authing.login(
        email=email,
        password=password
    )
    assert not loginResult.get('errors')
    global user_id
    user_id = loginResult['_id']


def test_LoginResult_with_username():
    loginResult = authing.login(
        username=username,
        password=password
    )
    assert user_id == loginResult['_id']


def test_getVerificationCode():
    verificationResult = authing.getVerificationCode(phone)
    if verificationResult[-1] == '请求过于频繁，请稍候再试':
        assert not verificationResult[0]
    else:
        assert verificationResult[0]


def test_readOauthList():
    oauthList = authing.readOauthList()
    assert isinstance(oauthList, list)


def test_User():
    info = authing.user({
        "id": user_id
    })
    assert not info.get('errors')
    assert info['_id'] == user_id


def test_Error_User():
    info = authing.user({
        "id": '5aec1ea610ecb800018db176'
    })
    assert info is None


def test_sendEmailCode():
    code = authing.sendChangeEmailVerifyCode("fuergaosi@gmail.com")
    assert not code.get('errors')


def test_updateEmail():
    result = authing.updateEmail(
        {'email': 'fuergaosi@gmail.com', 'emailCode': '12345'}
    )
    assert result.get('errors')


def test_update():
    update = authing.update({
        "_id": '5aec1ea610ecb800018db176',
        "username": 'alter-by-py'
    })
    assert update.get('errors')


def test_checkLoginStatus():
    res = authing.checkLoginStatus()
    assert not res.get('errors')


def test_remove():
    pass
