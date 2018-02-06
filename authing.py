from sgqlc.endpoint.http import HTTPEndpoint
import json

class Authing():

    """docstring for Authing"""

    def __init__(self, clientId, secret):
        self.clientId = clientId
        self.secret = secret

        self.servies = {
            "oauth": 'https://oauth.authing.cn/graphql',
            "users": 'https://users.authing.cn/graphql'
        }

    def auth(self):
        if 'authService' not in self.__dict__:
            self.authService = self.initService(self.servies['users'])

        

        pass

    def _initService(self, url, headers={}):
        # headers = {'Authorization': 'bearer TOKEN'}
        variables = {'clientId': '59f86b4832eb28071bdd9214'}
        endpoint = HTTPEndpoint(url, headers)
        return endpoint

    def _initOAuth(self, headers={}):
        self.oauth = self.initService(self.servies['oauth'], headers=headers)
        return self.oauth

    def _initUsers(self, headers={}):
        self.users = self.initService(self.servies['users'], headers=headers)
        return self.users

    def login(self, email, password):
        pass

    def register(self, email, password):
        pass

    def user(self, options):
        '''
            options: {
                "id": 'xxxxxxxxxx'
            }
        '''
        pass

    def list(self, page, count):
        pass

    def checkLoginStatus(self):
        pass

    def logout(self, uid):
        pass

    def remove(self, uid):
        pass

    def update(self, options):

        '''
        options = {
            _id String MUST
            email String
            emailVerified: Boolean
            username: String
            nickname: String
            company: String
            photo: {String || file object}
            browser: String
            password: String
            oldPassword: String(当有password时, 此参数必需)
            token: String
            tokenExpiredAt: String
            loginsCount: Number
            lastLogin: String
            lastIP: String
            signedUp: String
            blocked: Boolean
            isDeleted: Boolean        
        }
        '''
        pass

    def sendResetPasswordEmail(self, options):
        '''
            options = {
                "email": 'xxxxx'
            }
        '''
        pass

    def verifyResetPasswordVerifyCode(self, options):
        '''
            options = {
                email: email,
                verifyCode: verifyCode
            }
        '''
        pass

    def changePassword(self, options):
        '''
            options = {
                email: email,
                password: password,
                verifyCode: verifyCode
            }
        '''
        pass

    def sendVerifyEmail(self, options):
        '''
            options = {
                client: clientId,
                email: email
            }
        '''
        pass

    def readOauthList(self):

        query = '''
            query getOAuthList($clientId: String!) {
                ReadOauthList(clientId: $clientId) {
                    _id
                    name
                    image
                    description
                    enabled
                    client
                    user
                    oAuthUrl
                }
            }
        '''
        variables = {'clientId': self.clientId}

        return self.oauth(query, variables)

