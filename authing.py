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
                    return {'data': None, 'errors': [{
                        'message': exc,
                        'exception': exc,
                        'body': body,
                    }]}
        except urllib.error.HTTPError as exc:
            return self._log_http_error(query, req, exc)        

    def _log_http_error(self, query, req, exc):
        '''Log :exc:`urllib.error.HTTPError`, converting to
        GraphQL's ``{"data": null, "errors": [{"message": str(exc)...}]}``

        :param query: the GraphQL query that triggered the result.
        :type query: str

        :param req: :class:`urllib.request.Request` instance that was opened.
        :type req: :class:`urllib.request.Request`

        :param exc: :exc:`urllib.error.HTTPError` instance
        :type exc: :exc:`urllib.error.HTTPError`

        :return: GraphQL-compliant dict with keys ``data`` and ``errors``.
        :rtype: dict
        '''
        body = exc.read().decode('utf-8')
        content_type = exc.headers.get('Content-Type', '')
        if not content_type.startswith('application/json'):
            return {'data': None, 'errors': [{
                'message': exc,
                'exception': exc,
                'status': exc.code,
                'headers': exc.headers,
                'body': body,
            }]}
        else:
            # GraphQL servers return 400 and {'errors': [...]}
            # if only errors was returned, no {'data': ...}
            data = json.loads(body)
            if data and data.get('errors'):
                return data.get('errors')
            return {'data': None, 'errors': [{
                'message': exc,
                'exception': exc,
                'status': exc.code,
                'headers': exc.headers,
                'body': body,
            }]}

class Authing():

    """docstring for Authing"""

    def __init__(self, clientId, secret):
        self.clientId = clientId
        self.secret = secret

        self.servies = {
            "oauth": 'https://oauth.authing.cn/graphql',
            "users": 'https://users.authing.cn/graphql'
        }

        self.pubKey = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC4xKeUgQ+Aoz7TLfAfs9+paePb
5KIofVthEopwrXFkp8OCeocaTHt9ICjTT2QeJh6cZaDaArfZ873GPUn00eOIZ7Ae
+TiA2BKHbCvloW3w5Lnqm70iSsUi5Fmu9/2+68GZRH9L7Mlh8cFksCicW2Y2W2uM
GKl64GDcIq3au+aqJQIDAQAB
-----END PUBLIC KEY-----"""

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
        return AuthingEndPoint(url, headers)

    def _initOAuth(self, headers={}):
        self.oauth = self._initService(self.servies['oauth'], headers=headers)
        return self.oauth

    def _initUsers(self, headers={}):
        self.users = self._initService(self.servies['users'], headers=headers)
        return self.users

    def login(self, email=None, password=None, verifyCode=None):

        if not email: 
            raise Exception('请提供邮箱：email')

        if not password: 
            raise Exception('请提供密码：password')

        loginQuery = """
            mutation login($unionid: String, $email: String, $password: String, $lastIP: String, $registerInClient: String!, $verifyCode: String) {
                login(unionid: $unionid, email: $email, password: $password, lastIP: $lastIP, registerInClient: $registerInClient, verifyCode: $verifyCode) {
                    _id
                    email
                    emailVerified
                    username
                    nickname
                    company
                    photo
                    browser
                    token
                    tokenExpiredAt
                    loginsCount
                    lastLogin
                    lastIP
                    signedUp
                    blocked
                    isDeleted
                }
            }
        """

        variables = {
            "email": email,
            "password": password,
            "registerInClient": self.clientId,
            "verifyCode": verifyCode
        }

        loginResult = this.users(loginQuery, variables)

        if not loginResult.get('errors'):
            self.users = self._initUsers({
                "Authorization": 'Bearer {}'.format(loginResult['token'])    
            })

        return loginResult

    def register(self, email=None, password=None):

        if not email: 
            raise Exception('请提供邮箱：email')

        if not password: 
            raise Exception('请提供密码：password')

        registerQuery = """
            mutation register(
                $unionid: String,
                $email: String, 
                $password: String, 
                $lastIP: String, 
                $forceLogin: Boolean,
                $registerInClient: String!,
                $oauth: String,
                $username: String,
                $nickname: String,
                $registerMethod: String,
                $photo: String
            ) {
                register(userInfo: {
                    unionid: $unionid,
                    email: $email,
                    password: $password,
                    lastIP: $lastIP,
                    forceLogin: $forceLogin,
                    registerInClient: $registerInClient,
                    oauth: $oauth,
                    registerMethod: $registerMethod,
                    photo: $photo,
                    username: $username,
                    nickname: $nickname
                }) {
                    _id,
                    email,
                    emailVerified,
                    username,
                    nickname,
                    company,
                    photo,
                    browser,
                    password,
                    token,
                    group {
                        name
                    },
                    blocked
                }
            }
        """

        variables = {
            'email': email,
            'password': password,
            'registerInClient': self.clientId
        }

        return self.users(registerQuery, variables)

    def user(self, options):

        if not options.get('id'):
            raise Exception('请提供用户id: { "id": "xxxxxxxx" }')            

        query = '''
            query user($id: String!, $registerInClient: String!){
                user(id: $id, registerInClient: $registerInClient) {
                    _id
                    email
                    emailVerified
                    username
                    nickname
                    company
                    photo
                    browser
                    registerInClient
                    registerMethod
                    oauth
                    token
                    tokenExpiredAt
                    loginsCount
                    lastLogin
                    lastIP
                    signedUp
                    blocked
                    isDeleted
                }
            }
        '''
        variables = {
            "id": options['id'],
            "registerInClient": self.clientId
        }

        return this.authService(query, variables)

    def list(self, page=1, count=10):

        query = '''
            query user($id: String!, $registerInClient: String!){
                user(id: $id, registerInClient: $registerInClient) {
                    _id
                    email
                    emailVerified
                    username
                    nickname
                    company
                    photo
                    browser
                    registerInClient
                    registerMethod
                    oauth
                    token
                    tokenExpiredAt
                    loginsCount
                    lastLogin
                    lastIP
                    signedUp
                    blocked
                    isDeleted
                }
            }
        '''
        variables = {
            "id": options['id'],
            "registerInClient": self.clientId
        }
        
        return this.authService(query, variables)        

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

