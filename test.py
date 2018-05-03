from authing import Authing

if __name__ == '__main__':

    clientId = '5aeab91410ecb800018db165' 
    secret = '4822165c545486ffd32c2b9d62b11936'

    authing = Authing(clientId, secret)

    oauthList = authing.readOauthList()
    print(oauthList)

    # test_auth()