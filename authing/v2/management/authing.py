# coding: utf-8
from .applications import ApplicationsManagementClient
from .check_type import CheckType
from .policies import PolicyManagementClient
from .types import ManagementClientOptions
from ..common.graphql import GraphqlClient
from ..common.codegen import QUERY
from .token_provider import ManagementTokenProvider
from .users import UsersManagementClient
from .roles import RolesManagementClient
from .acl import AclManagementClient
from .udf import UdfManagementClient
from .groups import GroupsManagementClient
from .orgs import OrgManagementClient
from ..common.rest import RestClient
from .user_pool import UserPoolManagementClient
from .white_list import WhiteListManagementClient
from .audit_log import AuditLogManagementClient
from .principal_authentication import PrincipalAuthenticationClient


class ManagementClient(object):
    """Authing Management Client"""

    def __init__(self, options):
        # type:(ManagementClientOptions) -> ManagementClient
        self.options = options
        self.graphqlClient = GraphqlClient(
            options=self.options, endpoint=self.options.graphql_endpoint
        )
        self.restClient = RestClient(options=self.options)
        self.tokenProvider = ManagementTokenProvider(
            options=self.options, graphqlClient=self.graphqlClient
        )

        self.users = UsersManagementClient(
            options=self.options,
            graphqlClient=self.graphqlClient,
            restClient=self.restClient,
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
            managementClient=self
        )

        self.acl = AclManagementClient(
            options=self.options,
            graphqlClient=self.graphqlClient,
            restClient=self.restClient,
            tokenProvider=self.tokenProvider,
            managementClient=self
        )

        self.udf = UdfManagementClient(
            options=self.options,
            graphqlClient=self.graphqlClient,
            tokenProvider=self.tokenProvider,
        )

        self.applications = ApplicationsManagementClient(
            options=self.options,
            graphqlClient=self.graphqlClient,
            restClient=self.restClient,
            tokenProvider=self.tokenProvider,
            managementClient=self
        )

        self.groups = GroupsManagementClient(
            options=self.options,
            graphqlClient=self.graphqlClient,
            tokenProvider=self.tokenProvider
        )

        self.org = OrgManagementClient(
            options=self.options,
            graphqlClient=self.graphqlClient,
            tokenProvider=self.tokenProvider,
            restClient=self.restClient
        )

        self.userPool = UserPoolManagementClient(
            options=self.options,
            graphqlClient=self.graphqlClient,
            restClient=self.restClient,
            tokenProvider=self.tokenProvider,
            managementClient=self
        )

        self.whiteList = WhiteListManagementClient(
            options=self.options,
            graphqlClient=self.graphqlClient,
            restClient=self.restClient,
            tokenProvider=self.tokenProvider,
            managementClient=self
        )
        self.auditLog = AuditLogManagementClient(
            options=self.options,
            graphqlClient=self.graphqlClient,
            restClient=self.restClient,
            tokenProvider=self.tokenProvider,
            managementClient=self
        )
        self.principalAuth = PrincipalAuthenticationClient(
            options=self.options,
            graphqlClient=self.graphqlClient,
            restClient=self.restClient,
            tokenProvider=self.tokenProvider,
            managementClient=self
        )
        # 用户池详情
        self._userpool_detail = None

        # Check

        self.check = CheckType()

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
        """检测登录状态"""
        # type:(str,bool) -> any
        data = self.graphqlClient.request(
            query=QUERY["checkLoginStatus"], params={"token": token}
        )
        return data["checkLoginStatus"]

    def send_email(self, email, scene):
        """发送邮件"""
        data = self.graphqlClient.request(
            query=QUERY["sendEmail"], params={"email": email, "scene": scene}
        )
        return data["sendEmail"]

    def is_password_valid(self,password):
        """检测密码是否合法"""
        url = "%s/api/v2/password/check" % self.options.host
        return self.restClient.request(method='POST', token=self.tokenProvider.getAccessToken(), url=url,
                                       json={'password': password})
