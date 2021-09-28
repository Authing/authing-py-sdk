# coding: utf-8

from ..common.codegen import QUERY
from .types import ManagementClientOptions
from ..common.graphql import GraphqlClient
from .token_provider import ManagementTokenProvider
from ..exceptions import AuthingWrongArgumentException


class AuditLogManagementClient(object):
    """Authing Audit Log Management Client"""

    def __init__(self, options, restClient, graphqlClient, tokenProvider, managementClient):

        self.options = options
        self.restClient = restClient
        self.graphqlClient = graphqlClient
        self.tokenProvider = tokenProvider
        self.__super__ = managementClient

    def list_audit_logs(self, client_ip=None, operation_names=None, user_ids=None, app_ids=None, page=None, limit=None):
        """审计日志列表查询

        Args:
            client_ip(str): 登录IP
            operation_names(list)：操作人名称
            user_ids(list):用户Id
            app_ids(list):应用Id
            page(int):页号
            limit(int):每页记录数
        """
        url = "%s/api/v2/analysis/audit" % self.options.host
        params = {}
        if client_ip:
            params['clientip'] = client_ip
        if operation_names:
            params['operation_name'] = operation_names
        if operation_names:
            for index in range(len(user_ids)):
                user_ids[index] = 'arn:cn:authing:user:' + user_ids[index]
            params['operator_arn'] = user_ids
        if operation_names:
            params['app_id'] = app_ids
        if operation_names:
            params['operation_name'] = page
        if operation_names:
            params['operation_name'] = limit

        return self.restClient.request(method='GET', url=url, token=self.tokenProvider.getAccessToken(), params=params)



