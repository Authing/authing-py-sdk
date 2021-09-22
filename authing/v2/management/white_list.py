# coding: utf-8

from ..common.codegen import QUERY
from .types import ManagementClientOptions
from ..common.graphql import GraphqlClient
from .token_provider import ManagementTokenProvider
from ..exceptions import AuthingWrongArgumentException


class WhiteListManagementClient(object):
    """Authing Policy Management Client"""

    def __init__(self, options, restClient, graphqlClient, tokenProvider, managementClient):

        self.options = options
        self.restClient = restClient
        self.graphqlClient = graphqlClient
        self.tokenProvider = tokenProvider
        self.__super__ = managementClient

    def __check_type(self, type):
        if type not in ["USERNAME", "Email", "Phone"]:
            raise AuthingWrongArgumentException('type value only ["USERNAME","Email","Phone"]')

    def list(self, type):
        """获取白名单记录

        Args:
            type(str): 白名单类型，USERNAME 为用户名、Email 为邮箱、Phone 为手机号。
        """
        self.__check_type(type)
        data = self.graphqlClient.request(
            query=QUERY["whitelist"],
            params={'type': type},
            token=self.tokenProvider.getAccessToken(),
        )
        return data["whitelist"]

    def add(self, type, list):
        """添加白名单

        Args:
             type(str): 白名单类型，USERNAME 为用户名、Email 为邮箱、Phone 为手机号。
             list(list):白名单对象
        """
        self.__check_type(type)
        data = self.graphqlClient.request(
            query=QUERY["addWhitelist"],
            params={'type': type, "list": list},
            token=self.tokenProvider.getAccessToken(),
        )
        return data['addWhitelist']

    def remove(self, type, list):
        """移除白名单

        Args:
             type(str): 白名单类型，USERNAME 为用户名、Email 为邮箱、Phone 为手机号。
             list(list):白名单对象
        """
        self.__check_type(type)
        data = self.graphqlClient.request(
            query=QUERY["removeWhiteList"],
            params={'type': type, "list": list},
            token=self.tokenProvider.getAccessToken(),
        )
        return data['removeWhitelist']

    def enable_white_list(self, type):
        """开启白名单

        Args:
            type(str): 白名单类型，USERNAME 为用户名、Email 为邮箱、Phone 为手机号。
        """
        self.__check_type(type)
        if type == 'USERNAME':
            enable_type = {"whitelist": {"usernameEnabled": True}}
        if type == 'Email':
            enable_type = {"whitelist": {"emailEnabled": True}}
        if type == 'Phone':
            enable_type = {"whitelist": {"phoneEnabled": True}}

        return self.__super__.userPool.update(enable_type)

    def disable_white_list(self, type):
        """关闭白名单

        Args:
            type(str): 白名单类型，USERNAME 为用户名、Email 为邮箱、Phone 为手机号。
        """
        self.__check_type(type)
        if type == 'USERNAME':
            enable_type = {"whitelist": {"usernameEnabled": False}}
        if type == 'Email':
            enable_type = {"whitelist": {"emailEnabled": False}}
        if type == 'Phone':
            enable_type = {"whitelist": {"phoneEnabled": False}}

        return self.__super__.userPool.update(enable_type)