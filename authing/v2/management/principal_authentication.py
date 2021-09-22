# coding: utf-8

from ..common.codegen import QUERY
from .types import ManagementClientOptions
from ..common.graphql import GraphqlClient
from .token_provider import ManagementTokenProvider
from ..exceptions import AuthingWrongArgumentException

class PrincipalAuthenticationClient(object):
    """Authing PrincipalAuthentication Client"""

    def __init__(self, options, restClient, graphqlClient, tokenProvider, managementClient):

        self.options = options
        self.restClient = restClient
        self.graphqlClient = graphqlClient
        self.tokenProvider = tokenProvider
        self.__super__ = managementClient

    def detail(self, user_id):
        """获取主体认证详情 """
        url = "%s/api/v2/users/%s/management/principal_authentication" % (self.options.host, user_id)
        return self.restClient.request(method='GET', url=url, token=self.tokenProvider.getAccessToken())

    def authenticate(self, user_id, type, name, id_card, ext):
        """进行主体认证

        Args:
            user_id(str):用户ID
            type(str):类型 取值仅 P 或 E
            name(str): 名称
            id_card(str): type为 P时 个人身份证
                          type为 E时 企业统一信用编码
            ext(str)： type为 P时 银行卡号
                       type为 E时 企业法人名称
        """
        if type not in ["P", "E"]:
            raise AuthingWrongArgumentException("type value only P or E")
        url = "%s/api/v2/users/%s/management/principal_authentication" % (self.options.host, user_id)
        params = {
            'type': type,
            'name': name,
            'idCard': id_card,
            'ext': ext
        }
        return self.restClient.request(method='POST', url=url, token=self.tokenProvider.getAccessToken(),params=params)


