# coding: utf-8

from ..common.codegen import QUERY
from .types import ManagementClientOptions
from ..common.graphql import GraphqlClient
from .token_provider import ManagementTokenProvider


class PolicyManagementClient(object):
    """Authing Policy Management Client"""

    def __init__(self, options, graphqlClient, tokenProvider, managementClient):
        # type:(ManagementClientOptions,GraphqlClient,ManagementTokenProvider) -> PolicyManagementClient

        self.options = options
        self.graphqlClient = graphqlClient
        self.tokenProvider = tokenProvider
        self.__super__ = managementClient

    def list(self, page=1, limit=10):
        """获取策略列表

        Args:
            page (int): 页码数，从 1 开始，默认为 1 。
            limit (int): 每页个数，默认为 10 。
        """
        data = self.graphqlClient.request(
            query=QUERY["policies"],
            params={"page": page, "limit": limit},
            token=self.tokenProvider.getAccessToken(),
        )
        return data["policies"]

    def create(self, code, statements, description=None):
        """添加策略"""
        data = self.graphqlClient.request(
            query=QUERY["createPolicy"],
            params={"code": code, "description": description, "statements": statements},
            token=self.tokenProvider.getAccessToken(),
        )
        return data["createPolicy"]

    def detail(self, code):
        # type:(int) -> any
        """获取策略详情"""
        data = self.graphqlClient.request(
            query=QUERY["policy"],
            params={
                "code": code,
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["policy"]

    def update(self, code, statements, description=None):
        # type:(str,any,str) -> any
        """修改策略"""
        data = self.graphqlClient.request(
            query=QUERY["updatePolicy"],
            params={"code": code, "description": description, "statements": statements},
            token=self.tokenProvider.getAccessToken(),
        )
        return data["updatePolicy"]

    def delete(self, code):
        # type:(int) -> any
        """删除策略"""
        data = self.graphqlClient.request(
            query=QUERY["deletePolicy"],
            params={
                "code": code,
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["deletePolicy"]

    def delete_many(self, code_list):
        """批量删除策略"""
        data = self.graphqlClient.request(
            query=QUERY["deletePolicies"],
            params={
                "codeList": code_list,
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["deletePolicies"]

    def list_assignments(self, code, page=1, limit=10):
        """获取策略授权记录"""
        data = self.graphqlClient.request(
            query=QUERY["policyAssignments"],
            params={"code": code, "page": page, "limit": limit},
            token=self.tokenProvider.getAccessToken(),
        )
        return data["policyAssignments"]

    def add_assignments(self, policies, targetType, targetIdentifiers):
        """添加策略授权"""
        data = self.graphqlClient.request(
            query=QUERY["addPolicyAssignments"],
            params={
                "policies": policies,
                "targetType": targetType,
                "targetIdentifiers": targetIdentifiers,
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["addPolicyAssignments"]

    def remove_assignments(self, policies, targetType, targetIdentifiers):
        """撤销策略授权"""
        data = self.graphqlClient.request(
            query=QUERY["removePolicyAssignments"],
            params={
                "policies": policies,
                "targetType": targetType,
                "targetIdentifiers": targetIdentifiers,
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["removePolicyAssignments"]

    def enable_assignment(self, policy, target_type, target_identifier, namespace=None):
        """设置策略授权状态为开启

        Args:
            policy(str): 策略
            target_type(str): 策略类型 可选值为 USER (用户), ROLE (角色), GROUP（分组）, ORG（组织机构）
            target_identifier(str): 目标ID
            namespace(str):命名空间
        """
        self.__super__.check.target_type(target_type)
        data = self.graphqlClient.request(
            query=QUERY["enablePolicyAssignment"],
            params={
                "policy": policy,
                "targetType": target_type,
                "targetIdentifier": target_identifier,
                "namespace": namespace
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["enablePolicyAssignment"]

    def disable_assignment(self, policy, target_type, target_identifier, namespace=None):
        """设置策略授权状态为关闭

        Args:
            policy(str): 策略
            target_type(str): 策略类型 可选值为 USER (用户), ROLE (角色), GROUP（分组）, ORG（组织机构）
            target_identifier(str): 目标ID
            namespace(str):命名空间
        """
        self.__super__.check.target_type(target_type)
        data = self.graphqlClient.request(
            query=QUERY["disbalePolicyAssignment"],
            params={
                "policy": policy,
                "targetType": target_type,
                "targetIdentifier": target_identifier,
                "namespace": namespace
            },
            token=self.tokenProvider.getAccessToken(),
        )
        return data["disbalePolicyAssignment"]