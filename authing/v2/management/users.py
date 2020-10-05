from ..management import ManagementClientOptions
from ..common.utils import encrypt
from ..common.graphql import GraphqlClient
from .token_provider import ManagementTokenProvider
from ..common.codegen import QUERY


class UsersManagementClient(object):
    """Authing Users Management Client
    """

    def __init__(self, options: ManagementClientOptions, graphqlClient: GraphqlClient, tokenProvider: ManagementTokenProvider):
        self.options = options
        self.graphqlClient = graphqlClient
        self.tokenProvider = tokenProvider

    def list(self, page=1, limit=10):
        """获取用户池用户列表

        Args:
            page (int, optional): 页码数，从 1 开始，默认为 1 。
            limit (int, optional): 每页个数，默认为 10 。

        Returns:
            [totalCount, _list]: 返回一个 tuple，第一个值为用户总数，第二个为元素为用户信息的列表。
        """
        data = self.graphqlClient.request(
            query=QUERY["users"], params={
                'page': page,
                'limit': limit
            }, token=self.tokenProvider.getAccessToken())
        totalCount, _list = data['users']['totalCount'], data['users']['list']
        return totalCount, _list

    def create(self, userInfo: object):
        """创建用户

        Args:
            userInfo (object): 用户信息

        Returns:
            [User]: 用户详情
        """
        if userInfo.get('password'):
            userInfo['password'] = encrypt(
                userInfo['password'], self.options.encPublicKey)
        data = self.graphqlClient.request(query=QUERY['createUser'], params={
            'userInfo': userInfo,
        }, token=self.tokenProvider.getAccessToken())
        return data["createUser"]

    def update(self, userId: str, updates: object):
        """修改用户信息

        Args:
            userId (str): 用户 ID
            updates: 需要修改的用户字段
        """
        if updates.get('password'):
            updates['password'] = encrypt(
                updates['password'], self.options.encPublicKey)

        data = self.graphqlClient.request(
            query=QUERY['updateUser'],
            params={
                'id': userId,
                'input': updates
            },
            token=self.tokenProvider.getAccessToken()
        )
        return data['updateUser']

    def detail(self, userId: str):
        """获取用户资料详情

        Args:
            userId (str): 用户 ID
        """
        data = self.graphqlClient.request(
            query=QUERY['user'],
            params={
                'id': userId
            },
            token=self.tokenProvider.getAccessToken()
        )
        return data['user']

    def search(self, query: str, page=1, limit=10):
        """搜索用户

        Args:
            query (str): 查询语句
            page (int, optional): 页码数，从 1 开始，默认为 1 。
            limit (int, optional): 每页个数，默认为 10 。
        """
        data = self.graphqlClient.request(
            query=QUERY['searchUser'],
            params={
                'query': query,
                'page': page,
                'limit': limit
            },
            token=self.tokenProvider.getAccessToken()
        )
        totalCount, _list = data['searchUser']['totalCount'], data['searchUser']['list']
        return totalCount, _list

    def batch(self, userIds):
        """批量获取用户详情

        Args:
            userIds: 用户 ID 列表
        """
        data = self.graphqlClient.request(
            query=QUERY['userBatch'],
            params={
                'ids': userIds
            },
            token=self.tokenProvider.getAccessToken()
        )
        return data['userBatch']

    def delete(self, userId: str):
        """删除用户

        Args:
            userId (str): 用户 ID

        Returns:
            [int, str]: 一个 tuple ，第一个为状态码，200 表示成功，第二个为 message
        """
        data = self.graphqlClient.request(
            query=QUERY['deleteUser'],
            params={
                'id': userId
            },
            token=self.tokenProvider.getAccessToken()
        )
        code, message = data['deleteUser']['code'], data['deleteUser']['message']
        return code, message

    def delete_many(self, userIds):
        """批量删除用户

        Args:
            userIds: 用户 ID 列表
        """
        data = self.graphqlClient.request(
            query=QUERY['deleteUsers'],
            params={
                'ids': userIds
            },
            token=self.tokenProvider.getAccessToken()
        )
        code, message = data['deleteUsers']['code'], data['deleteUsers']['message']
        return code, message

    def list_roles(self, userId: str):
        """获取用户的角色列表

        Args:
            userId (str): 用户 ID
        """
        data = self.graphqlClient.request(
            query=QUERY['getUserRoles'],
            params={
                'id': userId,
            },
            token=self.tokenProvider.getAccessToken()
        )
        totalCount, _list = data['user']['roles']['totalCount'], data['user']['roles']['list']
        return totalCount, _list

    def add_roles(self, userId: str, roles):
        """批量授权用户角色

        Args:
            userId (str): 用户 ID
            roles: 角色 code 列表
        """
        data = self.graphqlClient.request(
            query=QUERY['assignRole'],
            params={
                'userIds': [userId],
                'roleCodes': roles,
            },
            token=self.tokenProvider.getAccessToken()
        )
        code, message = data['assignRole']['code'], data['assignRole']['message']
        return code, message

    def remove_roles(self, userId: str, roles):
        """批量撤销用户角色

        Args:
            userId (str): 用户 ID
            roles: 用户角色 code 列表
        """
        data = self.graphqlClient.request(
            query=QUERY['revokeRole'],
            params={
                'userIds': [userId],
                'roleCodes': roles,
            },
            token=self.tokenProvider.getAccessToken()
        )
        code, message = data['revokeRole']['code'], data['revokeRole']['message']
        return code, message

    def refresh_token(self, userId: str):
        """刷新某个用户的 token

        Args:
            userId (str): 用户 ID

        Returns:
            [str, number, number]: jwt token, iat, exp
        """
        data = self.graphqlClient.request(
            query=QUERY['refreshToken'],
            params={
                'id': userId,
            },
            token=self.tokenProvider.getAccessToken()
        )
        data = data['refreshToken']
        token, iat, exp = data['token'], data['iat'], data['exp']
        return token, iat, exp
