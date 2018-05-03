from authing import Authing

if __name__ == '__main__':

    clientId = '5aeab91410ecb800018db165' 
    secret = '4822165c545486ffd32c2b9d62b11936'

    authing = Authing(clientId, secret)

    #------- oauth test -------#
    # oauthList = authing.readOauthList()
    # print(oauthList)
    #------- oauth test -------#

    #------- register test -------#
    # _reg = authing.register('xieyang@dodora.cn', '123456')
    # print(_reg)
    #------- register test -------#

    #------- login test -------#

    #------- login test -------#

    #------- update test -------#

    authing.update({
        "_id": 'xxx',
        "nickname": 'xxxxx'
    })

    #------- update test -------#
