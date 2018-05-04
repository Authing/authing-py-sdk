from authing import Authing

if __name__ == '__main__':

    clientId = '5aeab91410ecb800018db165' 
    secret = '4822165c545486ffd32c2b9d62b11936'

    test_name = ''

    def log_tester_name(name):
        global test_name
        test_name = name
        print('>>> 测试 {}'.format(test_name))

    def log_test_result(result):
        print('>>> {} 测试结果'.format(test_name))
        print('>>> {}'.format(result))        
        print('')

    print('')

    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImVtYWlsIjoieGlleWFuZ0Bkb2RvcmEuY24iLCJpZCI6IjVhZWMxZWE2MTBlY2I4MDAwMThkYjE3NiIsImNsaWVudElkIjoiNWFlYWI5MTQxMGVjYjgwMDAxOGRiMTY1In0sImlhdCI6MTUyNTQyNDU3MSwiZXhwIjoxNTI2NzIwNTcxfQ.8Bi2mwZzJg2wIqhWxBxQlr5NcJoXVjzwC3nIjtAst9Y'

    log_tester_name('AccessToken')
    authing = Authing(clientId, secret, userToken=token)
    log_test_result(authing.accessToken)

    #------- oauth test -------#
    log_tester_name('readOAuthList')
    oauthList = authing.readOauthList()
    log_test_result(oauthList)
    #------- oauth test -------#

    #------- register test -------#
    log_tester_name('跳过 register')    
    # _reg = authing.register('xieyang@dodora.cn', '123456')
    # log_test_result(_reg)
    #------- register test -------#

    #------- login test -------#
    log_tester_name('跳过login')
    # _login = authing.login('xieyang@dodora.cn', '123456')
    # log_test_result(_login)
    print('现有token：{}'.format(token))
    print('')
    #------- login test -------#

    #------- user test -------#
    log_tester_name('user')    
    info = authing.user({
        "id": '5aec1ea610ecb800018db176'
    })
    log_test_result(info)
    log_tester_name('user error')
    info = authing.user({
        "id": '5aec1ea610ecb800018db176xx'
    })
    log_test_result(info)    
    #------- user test -------#

    #------- list test -------#
    log_tester_name('list')    
    _list = authing.list()
    log_test_result(_list)
    #------- list test -------#

    #------- list test -------#
    log_tester_name('list')    
    _list = authing.list()
    log_test_result(_list)
    #------- list test -------#

    #------- checkLoginStatus test -------#
    log_tester_name('checkLoginStatus')    
    _list = authing.checkLoginStatus()
    log_test_result(_list)
    #------- checkLoginStatus test -------#

    #------- update test -------#
    log_tester_name('update')
    update = authing.update({
        "_id": '5aec1ea610ecb800018db176',
        "username": 'alter-by-py'
    });
    log_test_result(update)
    #------- update test -------#

    #------- remove test -------#
    log_tester_name('跳过 remove （已测试过）')
    # result = authing.remove('5aec2e9610ecb800018db182')
    # log_test_result(result)
    #------- remove test -------#

