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
    log_tester_name('AccessToken')
    authing = Authing(clientId, secret)
    log_test_result(authing.accessToken)

    #------- oauth test -------#
    log_tester_name('readOAuthList')
    oauthList = authing.readOauthList()
    log_test_result(oauthList)
    #------- oauth test -------#

    #------- register test -------#
    log_tester_name('测试register')    
    _reg = authing.register('xieyang@dodora.cn', '123456')
    log_test_result(_reg)
    #------- register test -------#

    #------- login test -------#

    #------- login test -------#

    #------- update test -------#

    authing.update({
        "_id": 'xxx',
        "nickname": 'xxxxx'
    });

    #------- update test -------#
