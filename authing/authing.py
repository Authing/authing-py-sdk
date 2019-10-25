from sgqlc.endpoint.http import HTTPEndpoint
import urllib
import rsa
import base64
import json

LOGIN_METHOD_USING_EMAIL = "EMAIL"
LOGIN_METHOD_USING_PHONE = "PHONE"
LOGIN_METHOD_USING_USERNAME = "USERNAME"


class AuthingEndPoint(HTTPEndpoint):

    def __init__(self, url, base_headers=None, timeout=None, urlopen=None):
        HTTPEndpoint.__init__(self, url=url, base_headers=base_headers, timeout=timeout, urlopen=urlopen)

    def __call__(self, query, variables=None, operation_name=None,
                 extra_headers=None, timeout=None):
        '''Calls the GraphQL endpoint.
        :param query: the GraphQL query or mutation to execute. Note
          that self is converted using ``bytes()``, thus one may pass
          an object implementing ``__bytes__()`` method to return the
          query, eventually in more compact form (no indentation, etc).
        :type query: :class:`str` or :class:`bytes`.
        :param variables: variables (dict) to use with
          ``query``. self is only useful if the query or
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
                data.get('errors')[0]['message']['errors'] = True
                return data.get('errors')[0]['message']
            return {'data': None, 'errors': [{
                'message': exc,
                'exception': exc,
                'status': exc.code,
                'headers': exc.headers,
                'body': body,
            }]}


class Authing():
    """docstring for Authing"""

    def __init__(self, clientId, secret, options=None):
        self.clientId = clientId
        self.secret = secret

        if options is None:
            options = {}
            options = {
                "oauth": 'https://oauth.authing.cn/graphql',
                "users": 'https://users.authing.cn/graphql'
            }
            options["userToken"] = None

        if "userToken" not in options:
            options["userToken"] = None

        self.userToken = options["userToken"]

        self.services = {
            "oauth": options["oauth"],
            "users": options["users"]
        }

        with open('./pub.pem', mode='rb') as pubFile:
            keyData = pubFile.read()
            self.pubKey = rsa.PublicKey.load_pkcs1_openssl_pem(keyData)

        self.auth()

    def auth(self):
        if 'authService' not in self.__dict__:
            self.authService = self._initService(self.services['users'])

            authQuery = '''
                query getAccessTokenByAppSecret($secret: String!, $clientId: String!){
                    getAccessTokenByAppSecret(secret: $secret, clientId: $clientId)
                }
            '''
            variables = {'clientId': self.clientId, 'secret': self.secret}

            authResult = ''

            authResult = self.authService(authQuery, variables)

            print(authResult)

            if authResult.get('errors'):
                raise Exception(authResult)
            else:
                self.accessToken = authResult['data']['getAccessTokenByAppSecret']

                self.oauth = self._initOAuth(headers={
                    'Authorization': 'Bearer {}'.format(self.accessToken)
                })

                self.users = self._initUsers({
                    "Authorization": 'Bearer {}'.format(self.userToken or self.accessToken)
                })

                self.authService = self._initService(self.services['users'], headers={
                    "Authorization": 'Bearer {}'.format(self.userToken or self.accessToken)
                })

                if self.userToken:
                    self.users = self._initUsers({
                        "Authorization": 'Bearer {}'.format(self.userToken)
                    })

    def _initService(self, url, headers={}):
        return AuthingEndPoint(url, headers)

    def _initOAuth(self, headers={}):
        self.oauth = self._initService(self.services['oauth'], headers=headers)
        return self.oauth

    def _initUsers(self, headers={}):
        self.users = self._initService(self.services['users'], headers=headers)
        return self.users

    def login(self, email=None, username: str = None, password=None, verifyCode=None):

        if not email and not username:
            raise Exception('请提供邮箱 email 或用户名 username')

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

        _password = self.encrypt(password)

        variables = {
            "password": _password,
            "registerInClient": self.clientId,
            "verifyCode": verifyCode
        }
        if email:
            variables['email'] = email
        elif username:
            variables['username'] = username

        loginResult = self.users(loginQuery, variables)

        if not loginResult.get('errors'):
            self.users = self._initUsers({
                "Authorization": 'Bearer {}'.format(loginResult['data']['login']['token'])
            })
            return loginResult['data']['login']
        else:
            return loginResult

    def loginByPhoneCode(self, phone: str, phoneCode: int):

        if not isinstance(phoneCode, int):
            raise Exception("phoneCode 必须为 int 类型")

        loginQuery = """
mutation login($phone: String, $phoneCode: Int, $registerInClient: String!, $browser: String) {
  login(phone: $phone, phoneCode: $phoneCode, registerInClient: $registerInClient, browser: $browser) {
    _id
    email
    unionid
    openid
    emailVerified
    username
    nickname
    phone
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
            "registerInClient": self.clientId,
            'phone': phone,
            'phoneCode': phoneCode
        }

        loginResult = self.users(loginQuery, variables)
        if not loginResult.get('errors'):
            self.users = self._initUsers({
                "Authorization": 'Bearer {}'.format(loginResult['data']['login']['token'])
            })
            return loginResult['data']['login']
        else:
            return loginResult

    def getVerificationCode(self, phone: str) -> (bool, str):
        """

        :param phone: 手机号
        :return: 返回一个二元组，第一个表示是否成功，第二个为文字提示
        """
        send_sms_spi = "htt{}/send_smscode/{}/{}".format(
            self.services['users'].replace("/graphql", ''),
            phone,
            self.clientId
        )
        req = urllib.request.Request(send_sms_spi)
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read())
        code, msg = data['code'], data['message']
        success = code == 200
        return success, msg

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

        _password = self.encrypt(password)

        variables = {
            'email': email,
            'password': _password,
            'registerInClient': self.clientId
        }

        result = self.users(registerQuery, variables)

        if not result.get('errors'):
            return result['data']['register']
        else:
            return result

    def encrypt(self, data):
        _data = rsa.encrypt(data.encode('utf8'), self.pubKey)
        return base64.b64encode(_data).decode()

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

        result = self.users(query, variables)

        if not result.get('errors'):
            return result['data']['user']
        else:
            return result

    def list(self, page=1, count=10):

        query = '''
            query users($registerInClient: String, $page: Int, $count: Int){
              users(registerInClient: $registerInClient, page: $page, count: $count) {
                totalCount
                list {
                  _id
                  email
                  emailVerified
                  username
                  nickname
                  company
                  photo
                  browser
                  password
                  registerInClient
                  token
                  tokenExpiredAt
                  loginsCount
                  lastLogin
                  lastIP
                  signedUp
                  blocked
                  isDeleted
                  group {
                    _id
                    name
                    descriptions
                    createdAt
                  }
                  clientType {
                    _id
                    name
                    description
                    image
                    example
                  }
                  userLocation {
                    _id
                    when
                    where
                  }
                  userLoginHistory {
                    totalCount
                    list{
                      _id
                      when
                      success
                      ip
                      result
                    }
                  }
                  systemApplicationType {
                    _id
                    name
                    descriptions
                    price
                  }
                }
              }
            }
        '''
        variables = {
            "page": page,
            "count": count,
            "registerInClient": self.clientId
        }

        result = self.users(query, variables)

        if not result.get('errors'):
            return result['data']['users']
        else:
            return result

    def checkLoginStatus(self, token=None):
        query = """
            query checkLoginStatus($token: String) {
                checkLoginStatus(token: $token) {
                    status
                    code
                        message
                }
            }        
        """

        result = None

        if not token:
            result = self.users(query)
        else:
            result = self.users(query, {
                token: token
            })

        if not result.get('errors'):
            return result['data']['checkLoginStatus']
        else:
            return result

    def logout(self, uid):

        if not uid:
            raise Exception('请提供用户id：uid')

        return self.update({
            "_id": uid,
            "tokenExpiredAt": 0
        })

    def remove(self, uid):

        if not uid:
            raise Exception('请提供用户id：uid')

        query = """
            mutation removeUsers($ids: [String], $registerInClient: String, $operator: String){
              removeUsers(ids: $ids, registerInClient: $registerInClient, operator: $operator) {
                _id
              }
            }        
        """
        variables = {
            "ids": [uid],
            "registerInClient": self.clientId
        }

        result = self.authService(query, variables)

        if not result.get('errors'):
            return result['data']['removeUsers']
        else:
            return result

    def update(self, options):

        '''
        options = {
            _id: String MUST
            email: String
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

        if not options.get('_id'):
            raise Exception('请提供用户id: { "_id": "xxxxxxxx" }')

        typeList = {
            '_id': 'String!',
            'email': 'String',
            'emailVerified': 'Boolean',
            'username': 'String',
            'nickname': 'String',
            'company': 'String',
            'photo': 'String',
            'browser': 'String',
            'password': 'String',
            'oldPassword': 'String',
            'registerInClient': 'String!',
            'token': 'String',
            'tokenExpiredAt': 'String',
            'loginsCount': 'Int',
            'lastLogin': 'String',
            'lastIP': 'String',
            'signedUp': 'String',
            'blocked': 'Boolean',
            'isDeleted': 'Boolean'
        }

        query = """
            mutation UpdateUser(
                {0}
            ){
              updateUser(options: {
                {1}
              }) {
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
        """

        variables = options
        variables['registerInClient'] = self.clientId

        def genParams(variables):

            resultTpl = []
            tpl = "${}: {}"

            for key in variables:
                if typeList.get(key):
                    _type = typeList.get(key)
                    resultTpl.append(tpl.format(key, _type))

            return ',\r\n                '.join(resultTpl)

        def genSecondParams(variables):

            resultTpl = []
            tpl = "{}: ${}"

            for key in variables:
                if typeList.get(key):
                    resultTpl.append(tpl.format(key, key))

            return ',\r\n                '.join(resultTpl)

        _query = query.replace('{0}', genParams(variables))
        _query = _query.replace('{1}', genSecondParams(variables))

        print(_query)

        if 'password' in variables:
            variables['password'] = self.encrypt(variables['password'])

        if 'oldPassword' in variables:
            variables['oldPassword'] = self.encrypt(variables['oldPassword'])

        result = self.authService(_query, variables)

        print(_query)

        if not result.get('errors'):
            return result['data']['updateUser']
        else:
            return result

    def sendResetPasswordEmail(self, options={"email": ''}):
        '''
            options = {
                "email": 'xxxxx'
            }
        '''

        if options.get('email'):
            raise Exception('请提供用户邮箱：{"email": "xxxx@xxx.com"}')

        query = """
            mutation sendResetPasswordEmail(
                $email: String!,
                $client: String!
            ){
                sendResetPasswordEmail(
                    email: $email,
                    client: $client
                ) {
                      message
                      code
                }
            }
        """

        variables = {
            "email": options['email'],
            "client": self.clientId
        }

        result = self.authService(query, variables)

        if not result.get('errors'):
            return result['data']['sendResetPasswordEmail']
        else:
            return result

    def verifyResetPasswordVerifyCode(self, options={'email': '', 'verifyCode': ''}):
        '''
            options = {
                email: email,
                verifyCode: verifyCode
            }
        '''

        if options.get('email'):
            raise Exception('请提供用户邮箱：{"email": "xxxx@xxx.com", "verifyCode": "xxxx"}')

        if options.get('verifyCode'):
            raise Exception('请提供验证码：{"email": "xxxx@xxx.com", "verifyCode": "xxxx"}')

        query = """
            mutation verifyResetPasswordVerifyCode(
                $email: String!,
                $client: String!,
                $verifyCode: String!
            ) {
                verifyResetPasswordVerifyCode(
                    email: $email,
                    client: $client,
                    verifyCode: $verifyCode
                ) {
                      message
                      code
                }
            }
        """

        variables = {
            "email": options['email'],
            "verifyCode": options['verifyCode'],
            "client": self.clientId
        }

        result = self.authService(query, variables)

        if not result.get('errors'):
            return result['data']['verifyResetPasswordVerifyCode']
        else:
            return result

    def changePassword(self, options={'email': '', 'verifyCode': '', 'password': ''}):
        '''
            options = {
                email: email,
                password: password,
                verifyCode: verifyCode
            }
        '''

        if options.get('email'):
            raise Exception("""请提供用户邮箱：{"email": "xxxx@xxx.com", "verifyCode": "xxxx", "password": "xxxx"'}""")

        if options.get('verifyCode'):
            raise Exception('请提供验证码：{"email": "xxxx@xxx.com", "verifyCode": "xxxx", "password": "xxxx"}')

        query = """
            mutation changePassword(
                $email: String!,
                $client: String!,
                $password: String!,
                $verifyCode: String!
            ){
                changePassword(
                    email: $email,
                    client: $client,
                    password: $password,
                    verifyCode: $verifyCode
                ) {
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
        """

        variables = {
            "email": options['email'],
            "verifyCode": options['verifyCode'],
            "password": self.encrypt(options['password']),
            "client": self.clientId
        }

        result = self.authService(query, variables)

        if not result.get('errors'):
            return result['data']['changePassword']
        else:
            return result

    def sendVerifyEmail(self, options={"email": ''}):
        '''
            options = {
                client: clientId,
                email: email
            }
        '''

        if options.get('email'):
            raise Exception('请提供用户邮箱：{"email": "xxxx@xxx.com"}')

        query = """
            mutation sendVerifyEmail(
                $email: String!,
                $client: String!
            ){
                sendVerifyEmail(
                    email: $email,
                    client: $client
                ) {
                    message,
                    code,
                    status
                }
            }
        """

        variables = {
            "email": options['email'],
            "client": self.clientId
        }

        result = self.authService(query, variables)

        if not result.get('errors'):
            return result['data']['sendVerifyEmail']
        else:
            return result

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

        result = self.oauth(query, variables)

        if not result.get('errors'):
            return result['data']['ReadOauthList']
        else:
            return result

    def queryPermissions(self, userId):

        query = '''
            query QueryRoleByUserId($user: String!, $client: String!){
                queryRoleByUserId(user: $user, client: $client) {
                totalCount
                list {
                    group {
                    name
                    permissions
                    }
                }
                }
            }
        '''
        variables = {
            'clientId': self.clientId,
            'user': userId
        }

        result = self.authService(query, variables)

        if not result.get('errors'):
            return result['data']['queryRoleByUserId']
        else:
            return result

    def queryRoles(self, options):

        query = '''
            query ClientRoles(
            $clientId: String!
            $page: Int
            $count: Int
            ) {
            clientRoles(
                client: $clientId
                page: $page
                count: $count
            ) {
                totalCount
                list {
                _id
                name
                descriptions
                client
                createdAt
                permissions
                }
            }
            }
        '''
        variables = {
            'clientId': self.clientId,
            'page': options.page,
            'count': options.count
        }

        result = self.authService(query, variables)

        if not result.get('errors'):
            return result['data']['clientRoles']
        else:
            return result

    def createRole(self, options):

        query = '''
            mutation CreateRole(
            $name: String!
            $client: String!
            $descriptions: String
            ) {
                createRole(
                    name: $name
                    client: $client
                    descriptions: $descriptions
                ) {
                    _id,
                    name,
                    client,
                    descriptions
                }
            }
        '''
        variables = {
            'clientId': self.clientId,
            'name': options.name,
            'descriptions': options.descriptions
        }

        result = self.authService(query, variables)

        if not result.get('errors'):
            return result['data']['createRole']
        else:
            return result

    def updateRolePermissions(self, options):

        query = '''
            mutation UpdateRole(
            $_id: String!
            $name: String!
            $client: String!
            $descriptions: String
            $permissions: String
            ) {
            updateRole(
                _id: $_id
                name: $name
                client: $client
                descriptions: $descriptions
                permissions: $permissions
            ) {
                _id,
                name,
                client,
                descriptions,
                permissions
            }
            }
        '''
        variables = {
            'clientId': self.clientId,
            'name': options.name,
            'permissions': options.permissions,
            '_id': options.roleId
        }

        result = self.authService(query, variables)

        if not result.get('errors'):
            return result['data']['updateRole']
        else:
            return result

    def assignUserToRole(self, options):

        query = '''
            mutation AssignUserToRole(
            $group: String!
            $client: String!
            $user: String!
            ) {
            assignUserToRole(
                group: $group
                client: $client
                user: $user
            ) {
                totalCount,
                list {
                _id,
                client {
                    _id
                },
                user {
                    _id
                },
                createdAt
                }
            }
            }
        '''
        variables = {
            'clientId': self.clientId,
            'group': options.roleId,
            'user': options.user
        }

        result = self.authService(query, variables)

        if not result.get('errors'):
            return result['data']['assignUserToRole']
        else:
            return result

    def removeUserFromRole(self, options):

        query = '''
            mutation RemoveUserFromGroup(
                $group: String!
                $client: String!
                $user: String!
            ) {
            removeUserFromGroup(
                group: $group
                client: $client
                user: $user
            ) {
                _id,
                group {
                    _id
                },
                client {
                    _id
                },
                user {
                    _id
                }
            }
            }
        '''
        variables = {
            'clientId': self.clientId,
            'group': options.roleId,
            'user': options.user
        }

        result = self.authService(query, variables)

        if not result.get('errors'):
            return result['data']['removeUserFromGroup']
        else:
            return result
