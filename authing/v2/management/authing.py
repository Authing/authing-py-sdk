# coding: utf-8

from .policies import PolicyManagementClient
from .types import ManagementClientOptions
from ..common.graphql import GraphqlClient
from ..common.codegen import QUERY
from .token_provider import ManagementTokenProvider
from .users import UsersManagementClient
from .roles import RolesManagementClient
from .acl import AclManagementClient
from .udf import UdfManagementClient


class ManagementClient(object):
    """Authing Management Client"""

    def __init__(self, options):
        # type:(ManagementClientOptions) -> ManagementClient
        self.options = options
        self.graphqlClient = GraphqlClient(
            options=self.options, endpoint=self.options.graphql_endpoint
        )
        self.tokenProvider = ManagementTokenProvider(
            options=self.options, graphqlClient=self.graphqlClient
        )

        self.users = UsersManagementClient(
            options=self.options,
            graphqlClient=self.graphqlClient,
            tokenProvider=self.tokenProvider,
        )

        self.roles = RolesManagementClient(
            options=self.options,
            graphqlClient=self.graphqlClient,
            tokenProvider=self.tokenProvider,
        )

        self.policies = PolicyManagementClient(
            options=self.options,
            graphqlClient=self.graphqlClient,
            tokenProvider=self.tokenProvider,
        )

        self.acl = AclManagementClient(
            options=self.options,
            graphqlClient=self.graphqlClient,
            tokenProvider=self.tokenProvider,
        )

        self.udf = UdfManagementClient(
            options=self.options,
            graphqlClient=self.graphqlClient,
            tokenProvider=self.tokenProvider,
        )

        # 用户池详情
        self._userpool_detail = None

    def _get_userpool_detail(self):
        if self._userpool_detail:
            return self._userpool_detail

        data = self.graphqlClient.request(
            query=QUERY["userpool"],
            params={},
            token=self.tokenProvider.getAccessToken(),
        )
        self._userpool_detail = data["userpool"]
        return self._userpool_detail

    def check_login_status(self, token):
        # type:(str,bool) -> any
        data = self.graphqlClient.request(
            query=QUERY["checkLoginStatus"], params={"token": token}
        )
        return data["checkLoginStatus"]
