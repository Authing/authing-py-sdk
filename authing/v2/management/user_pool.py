# coding: utf-8

from ..common.codegen import QUERY
from .types import ManagementClientOptions
from ..common.graphql import GraphqlClient
from .token_provider import ManagementTokenProvider


class UserPoolManagementClient(object):
    """Authing UserPool Management Client"""

    def __init__(self, options, restClient, graphqlClient, tokenProvider, managementClient):

        self.options = options
        self.restClient = restClient
        self.graphqlClient = graphqlClient
        self.tokenProvider = tokenProvider
        self.__super__ = managementClient

    def list_env(self):
        """获取环境变量列表 """
        url = "%s/api/v2/env" % self.options.host
        return self.restClient.request(method='GET', url=url, token=self.tokenProvider.getAccessToken())

    def add_env(self, key, value):
        """添加环境变量"""
        url = "%s/api/v2/env" % self.options.host
        return self.restClient.request(method='POST', url=url, token=self.tokenProvider.getAccessToken(),
                                       json={'key': key,  'value': value})

    def detail(self):
        """查询用户池配置"""
        url = "%s/api/v2/userpools/detail" % self.options.host
        return self.restClient.request(method='GET', url=url, token=self.tokenProvider.getAccessToken())

    def update(self, updates):
        """更新用户池配置

        Args:
            updates(dict): 参数集合
            updates[name](str): 用户池名称
            updates[logo](str): 用户池 logo
            updates[domain](str): 用户池企业应用面板二级域名
            updates[description](str): 描述信息
            updates[emailVerifiedDefault](bool):设置邮箱默认为已验证状态（用户的 emailVerified 字段为 true）
            updates[appSsoEnabled](bool):开启用户池下的应用之间单点登录
            updates[sendWelcomeEmail](bool):用户注册之后是否发送欢迎邮件
            updates[registerDisabled](bool):是否关闭注册，当用户池关闭注册之后，普通用户将无法注册账号，只有管理员能够手动创建账号。
            updates[allowedOrigins](str):安全域配置，安全域（Allowed Origins） 是允许从 JavaScript 向 Authing API
                发出请求的 URL（通常与 CORS 一起使用）。 默认情况下，系统会允许你使用所有网址。 如果需要，此字段允许你输入其他来源。
                你可以通过逐行分隔多个有效 URL，并在子域级别使用通配符（例如：https://*.sample.com）。验证这些 URL 时不考虑查询字符串和哈希信息，
                如果带上了查询字符串和哈希信息系统会自动忽略整个域名。如果有多条请以换行符分隔。
            updates[whitelist](dict):  用户池白名单配置
            updates[whitelist][phoneEnabled](bool):是否开启手机号白名单
            updates[whitelist][emailEnabled](bool):是否开启邮箱白名单
            updates[whitelist][usernameEnabled](bool):是否开启用户名白名单
            updates[tokenExpiresAfter](int):token 过期时间
            updates[loginFailCheck](dict):频繁登录失败限制，开启之后，在规定时间内超过次数后再次登录需要验证码。如果你的业务存在同一区域同一时间段并发登录的场景，请将此检测关闭。
            updates[loginFailCheck][enabled](bool):是否开启
            updates[loginFailCheck][timeInterval](int):检测周期，单位为秒。
            updates[loginFailCheck][limit](int):同一 IP 登录失败次数达到多少次的时候会触发限制条件。
            updates[frequentRegisterCheck](dict):频率注册限制，开启之后同一 IP 频繁注册账号时会触发频率限制，需要等一段时间之后才能重新注册。如果你的业务存在同一区域同一时间段并发注册的场景，请将此检测关闭。
            updates[frequentRegisterCheck][enabled](bool):是否开启
            updates[frequentRegisterCheck][timeInterval](str):检测周期，单位为秒。
            updates[frequentRegisterCheck][limit](str):同一个周期内同一 IP 注册次数达到此数目时会触发频率限制。
        """
        data = self.graphqlClient.request(
            query=QUERY["updateUserpool"],
            params={'input': updates},
            token=self.tokenProvider.getAccessToken(),
        )
        return data["updateUserpool"]

    def remove_env(self, key):
        """删除环境变量"""
        url = "%s/api/v2/env/%s" % (self.options.host, key)
        return self.restClient.request(method='DELETE', url=url, token=self.tokenProvider.getAccessToken())
