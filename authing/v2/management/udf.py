# coding: utf-8

from .types import ManagementClientOptions
from ..common.graphql import GraphqlClient
from .token_provider import ManagementTokenProvider
from ..common.codegen import QUERY


class UdfManagementClient(object):
    """Authing User Defined Field Management Client"""

    def __init__(self, options, graphqlClient, tokenProvider):
        # type:(ManagementClientOptions,GraphqlClient,ManagementTokenProvider) -> UdfManagementClient
        self.options = options
        self.graphqlClient = graphqlClient
        self.tokenProvider = tokenProvider

    def list(self, targetType):
        """
        获取自定义字段定义

        Args:
            targetType (str) 自定义字段目标类型， USER 表示用户、ROLE 表示角色。
        """
        data = self.graphqlClient.request(
            query=QUERY["udf"],
            params={
                "targetType": targetType,
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["udf"]

    def set(self, targetType, key, dataType, label):
        """
        添加自定义字段定义

        Args:
            targetType (str) 自定义字段目标类型， USER 表示用户、ROLE 表示角色。
            key (str) 字段 key
            dataType (str) 数据类型，目前共支持四种数据类型。STRING 为字符串、NUMBER 为数字、DATETIME 为日期、BOOLEAN 为 boolean 值。
            label (str) 字段 Label，一般是一个 Human Readable 字符串。
        """
        data = self.graphqlClient.request(
            query=QUERY["setUdf"],
            params={
                "targetType": targetType,
                "key": key,
                "dataType": dataType,
                "label": label,
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["setUdf"]

    def remove(self, targetType, key):
        """
        删除自定义字段定义

        Args:
            targetType (str) 自定义字段目标类型， USER 表示用户、ROLE 表示角色。
            key (str) 字段 key
        """
        data = self.graphqlClient.request(
            query=QUERY["removeUdf"],
            params={
                "targetType": targetType,
                "key": key,
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["removeUdf"]

    def list_udf_value(self, target_type, target_id):
        """
        获取某一实体的自定义字段数据列表

        Args:
            target_type (str) 自定义字段目标类型， USER 表示用户、ROLE 表示角色。
            target_id (str) 自定义字段目标 id，如用户 ID
        """
        return self.graphqlClient.request(
            query=QUERY["udv"],
            params={
                "targetType": target_type,
                "targetId": target_id
            },
            token=self.tokenProvider.getAccessToken(),
        )["udv"]

    def set_udf_value_batch(self, target_type, target_id, udf_value_list):
        """
        批量添加自定义数据

        Args:
            target_type (str) 自定义字段目标类型， USER 表示用户、ROLE 表示角色。
            target_id (str) 自定义字段目标 id，如用户 ID
            udf_value_list (list) 存放 Key Value 的数组
        """

        return self.graphqlClient.request(
            query=QUERY["setUdvBatch"],
            params={
                "targetType": target_type,
                "targetId": target_id,
                "udvList": udf_value_list
            },
            token=self.tokenProvider.getAccessToken()
        )["setUdvBatch"]

