from authing import Authing


def log_tester_name(name):
    global test_name
    test_name = name
    print('>>> 测试 {}'.format(test_name))


def log_test_result(result):
    print('>>> {} 测试结果'.format(test_name))
    print('>>> {}'.format(result))
    print('')


if __name__ == '__main__':
    clientId = '5de935b82a709748e17681f0'
    secret = 'cfb8a38a52f3a0bec44602b0c0e4518d'
    test_name = ''

    email = "921520348@qq.com"
    username = "holegots"
    password = "123456"
    phone = "17624555576"
    phoneCode = 1234

    print('')

    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImVtYWlsIjoieGlleWFuZ0Bkb2RvcmEuY24iLCJpZCI6IjVhZWMxZWE2MTBlY2I4MDAwMThkYjE3NiIsImNsaWVudElkIjoiNWFlYWI5MTQxMGVjYjgwMDAxOGRiMTY1In0sImlhdCI6MTUyNTQyNDU3MSwiZXhwIjoxNTI2NzIwNTcxfQ.8Bi2mwZzJg2wIqhWxBxQlr5NcJoXVjzwC3nIjtAst9Y'

    log_tester_name('AccessToken')
    authing = Authing(clientId, secret, {
        "oauth": 'https://oauth.authing.cn/graphql',
        "users": 'https://users.authing.cn/graphql'
    })
    log_test_result(authing.accessToken)

    # ------- login test ---------- #
    log_tester_name("使用邮箱密码登陆")
    loginResult = authing.login(
        email=email,
        password=password
    )
    log_test_result(loginResult)

    # ------- login test ---------- #
    log_tester_name("使用用户名密码登陆")
    loginResult = authing.login(
        username=username,
        password=password
    )
    log_test_result(loginResult)

    # ------- sms test ---------- #
    log_tester_name("发送验证码")
    verificationResult = authing.getVerificationCode(phone)
    log_test_result(verificationResult)

    # ------- login test ---------- #
    log_tester_name("使用手机号登陆")
    loginResult = authing.loginByPhoneCode(
        phone=phone,
        phoneCode=phoneCode
    )
    log_test_result(loginResult)

    # ------- oauth test -------#
    log_tester_name('readOAuthList')
    oauthList = authing.readOauthList()
    log_test_result(oauthList)
    # ------- oauth test -------#

    # ------- register test -------#
    log_tester_name('跳过 register')
    # _reg = authing.register('xieyang@dodora.cn', '123456')
    # log_test_result(_reg)
    # ------- register test -------#

    # ------- login test -------#
    log_tester_name('跳过login')
    # _login = authing.login('xieyang@dodora.cn', '123456')
    # log_test_result(_login)
    print('现有token：{}'.format(token))
    print('')
    # ------- login test -------#

    # ------- user test -------#
    log_tester_name('user')
    info = authing.user({
        "id": '5df089049d0df42ce076f53b'
    })
    log_test_result(info)
    log_tester_name('user error')
    info = authing.user({
        "id": '5df089049d0df42ce076f53b'
    })
    log_test_result(info)
    # ------- user test -------#

    # ------- list test -------#
    log_tester_name('list')
    _list = authing.list()
    log_test_result(_list)
    # ------- list test -------#

    # ------- checkLoginStatus test -------#
    log_tester_name('checkLoginStatus')
    _list = authing.checkLoginStatus()
    log_test_result(_list)
    # ------- checkLoginStatus test -------#

    #------- sendEmailCode test -------#
    log_tester_name('sendEmailCode')
    code = authing.sendChangeEmailVerifyCode("fuergaosi@gmail.com")
    log_test_result(code)
    #------- sendEmailCode test -------#

    code = input('输入验证码:')

    #------- updateEmail test -------#
    log_tester_name('updateEmail')
    result = authing.updateEmail(
        {'email': 'fuergaosi@gmail.com', 'emailCode': code}
    )
    log_test_result(result)

    #------- sendEmailCode test -------#

    # ------- update test -------#
    log_tester_name('update')
    update = authing.update({
        "_id": '5aec1ea610ecb800018db176',
        "username": 'alter-by-py'
    })
    log_test_result(update)
    # ------- update test -------#

    # ------- remove test -------#
    log_tester_name('跳过 remove （已测试过）')
    # result = authing.remove('5aec2e9610ecb800018db182')
    # log_test_result(result)
    # ------- remove test -------#
