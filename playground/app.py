from authing.authing import Authing
import rsa

clientId = '5d43a3f2437ff00c51dda3be'
secret = '3d45c27c6af6dfd28d4cd0eb490e8ed2'


# log_tester_name('AccessToken')
authing = Authing(clientId, secret, {
            "oauth": 'https://users.kingdomai.com/graphql',
            "users": 'https://oauth.kingdomai.com/graphql'
})
# log_test_result(authing.accessToken)

#------- oauth test -------#
# log_tester_name('readOAuthList')
oauthList = authing.readOauthList()
# log_test_result(oauthList)

# class MyAuthing(Authing):
    
#     """docstring for Authing"""

#     def __init__(self, clientId, secret, userToken=None):
#         self.clientId = clientId
#         self.secret = secret
#         self.userToken = userToken

#         self.servies = {
#             "oauth": 'https://users.kingdomai.com/graphql',
#             "users": 'https://oauth.kingdomai.com/graphql'
#         }

#         with open('./pub.pem', mode='rb') as pubFile:
#             keyData = pubFile.read()
#             self.pubKey = rsa.PublicKey.load_pkcs1_openssl_pem(keyData)

#         self.auth()

# client = MyAuthing(clientId, secret)
