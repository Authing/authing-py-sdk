from authing.v2.management.policy import PolicyManagementClient
from . import ManagementClientOptions
from ..common.graphql import GraphqlClient
from ..common.codegen import QUERY
from ..common.utils import jwt_verify
from .token_provider import ManagementTokenProvider
from .users import UsersManagementClient
from .roles import RolesManagementClient


class ManagementClient(object):
    """Authing Management Client

    Args:
        userPoolId (str): Your Authing UserPool Id
        secret (str): Your Authing UserPool Secret
    """

    def __init__(self, options: ManagementClientOptions):
        self.options = options
        self.graphqlClient = GraphqlClient(
            options=self.options,
            endpoint=self.options.graphqlEndpoint
        )
        self.tokenProvider = ManagementTokenProvider(
            options=self.options,
            graphqlClient=self.graphqlClient
        )

        self.users = UsersManagementClient(
            options=self.options,
            graphqlClient=self.graphqlClient,
            tokenProvider=self.tokenProvider
        )

        self.roles = RolesManagementClient(
            options=self.options,
            graphqlClient=self.graphqlClient,
            tokenProvider=self.tokenProvider
        )

        self.policies = PolicyManagementClient(
            options=self.options,
            graphqlClient=self.graphqlClient,
            tokenProvider=self.tokenProvider
        )

        # 用户池详情
        self._userpool_detail = None

    def _get_userpool_detail(self):
        if self._userpool_detail:
            return self._userpool_detail

        data = self.graphqlClient.request(
            query=QUERY['userpool'],
            params={},
            token=self.tokenProvider.getAccessToken()
        )
        self._userpool_detail = data['userpool']
        return self._userpool_detail

    def check_login_status(self, token: str, fetchUserDetail: bool = False):
        jwt_secret = self._get_userpool_detail()['jwtSecret']
        result = jwt_verify(token, jwt_secret)
        data, iat, exp = result['data'], result['iat'], result['exp']
        if not fetchUserDetail:
            return data
        userId = data['userId']
        user = self.users.detail(userId=userId)
        return user
