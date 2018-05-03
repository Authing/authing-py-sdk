from sgqlc.endpoint.http import HTTPEndpoint
import json
import urllib

class AuthingEndPoint(HTTPEndpoint):

    def __init__(self, url, base_headers=None, timeout=None, urlopen=None):
        HTTPEndpoint.__init__(self, url=url, base_headers=base_headers, timeout=timeout, urlopen=urlopen)

    def __call__(self, query, variables=None, operation_name=None,
                 extra_headers=None, timeout=None):
        '''Calls the GraphQL endpoint.
        :param query: the GraphQL query or mutation to execute. Note
          that this is converted using ``bytes()``, thus one may pass
          an object implementing ``__bytes__()`` method to return the
          query, eventually in more compact form (no indentation, etc).
        :type query: :class:`str` or :class:`bytes`.
        :param variables: variables (dict) to use with
          ``query``. This is only useful if the query or
          mutation contains ``$variableName``.
        :type variables: dict
        :param operation_name: if more than one operation is listed in
          ``query``, then it should specify the one to be executed.
        :type operation_name: str
        :param extra_headers: dict with extra HTTP headers to use.
        :type extra_headers: dict
        :param timeout: overrides the default timeout.
        :type timeout: float
        :return: dict with optional fields ``data`` containing the GraphQL
          returned data as nested dict and ``errors`` with an array of
          errors. Note that both ``data`` and ``errors`` may be returned!
        :rtype: dict
        '''
        if isinstance(query, bytes):
            query = query.decode('utf-8')
        elif not isinstance(query, str):
            # allows sgqlc.operation.Operation to be passed
            # and generate compact representation of the queries
            query = bytes(query).decode('utf-8')

        post_data = json.dumps({
            'query': query,
            'variables': variables,
            'operationName': operation_name,
        }).encode('utf-8')
        headers = self.base_headers.copy()
        if extra_headers:
            headers.update(extra_headers)
        headers.update({
            'Accept': 'application/json; charset=utf-8',
            'Content-Type': 'application/json; charset=utf-8',
            'Content-Length': len(post_data),
        })

        self.logger.debug('Query:\n%s', query)

        req = urllib.request.Request(
            url=self.url, data=post_data, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as f:
                body = f.read().decode('utf-8')
                try:
                    data = json.loads(body)
                    if data and data.get('errors'):
                        data['errors'][0]['message']['errors'] = True
                        return data['errors'][0]['message']
                    return data
                except json.JSONDecodeError as exc:
                    return self._log_json_error(body, exc)
        except urllib.error.HTTPError as exc:
            return self._log_http_error(query, req, exc)        

class Authing():

    """docstring for Authing"""

    def __init__(self, clientId, secret):
        self.clientId = clientId
        self.secret = secret

        self.servies = {
            "oauth": 'https://oauth.authing.cn/graphql',
            "users": 'https://users.authing.cn/graphql'
        }

        self.auth()

    def auth(self):
        if 'authService' not in self.__dict__:
            self.authService = self._initService(self.servies['users'])

            authQuery = '''
                query getAccessTokenByAppSecret($secret: String!, $clientId: String!){
                    getAccessTokenByAppSecret(secret: $secret, clientId: $clientId)
                }
            '''
            variables = { 'clientId': self.clientId, 'secret': self.secret }

            authResult = ''

            authResult = self.authService(authQuery, variables)                

            if authResult.get('errors'):
                raise Exception(authResult)
            else:
                self.accessToken = authResult['data']['getAccessTokenByAppSecret']

                self.oauth = self._initOAuth(headers={
                    'Authorization': 'Bearer {}'.format(self.accessToken)
                });

                self.users = self._initUsers();

    def _initService(self, url, headers={}):
        endpoint = AuthingEndPoint(url, headers)
        return endpoint            

    def _initOAuth(self, headers={}):
        self.oauth = self._initService(self.servies['oauth'], headers=headers)
        return self.oauth

    def _initUsers(self, headers={}):
        self.users = self._initService(self.servies['users'], headers=headers)
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

