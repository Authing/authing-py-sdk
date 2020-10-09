# coding: utf-8

from .types import ManagementClientOptions
from ..common.graphql import GraphqlClient
from .token_provider import ManagementTokenProvider
from ..common.codegen import QUERY


class AclManagementClient(object):
    """Authing Access Control Management Client
    """

    def __init__(self, options, graphqlClient, tokenProvider):
        # type:(ManagementClientOptions,GraphqlClient,ManagementTokenProvider) -> AclManagementClient
        self.options = options
        self.graphqlClient = graphqlClient
        self.tokenProvider = tokenProvider

    def allow(self, resource, action, userId=None, role=None):
        # type:(str,str,str,str) -> object
        """允许某个用户操作某个资源
        """
        if not userId and not role:
            raise "userId 和 role 必填其一"
        data = self.graphqlClient.request(
            query=QUERY["allow"], params={
                'userId': userId,
                'roleCode': role,
                'resource': resource,
                'action': action
            }, token=self.tokenProvider.getAccessToken())
        return data['allow']

    def is_allowed(self, userId, action, resource):
        # type:(str,str,str) -> object
        """是否允许某个用户操作某个资源
        """
        data = self.graphqlClient.request(
            query=QUERY["isActionAllowed"], params={
                'userId': userId,
                'resource': resource,
                'action': action
            }, token=self.tokenProvider.getAccessToken())
        return data['isActionAllowed']
