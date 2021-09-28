# coding: utf-8
from ..exceptions import AuthingWrongArgumentException


class ApplicationsManagementClient(object):
    """Authing Applications Management Client"""

    def __init__(self, options, graphqlClient, restClient, tokenProvider, managementClient):
        self.options = options
        self.graphqlClient = graphqlClient
        self.restClient = restClient
        self.tokenProvider = tokenProvider
        self.__super__ = managementClient

    def list(self, page=1, limit=10):
        """获取应用列表

        Args:
            page(int):页号
            limit(int):每页记录数
        """
        url = "%s/api/v2/applications?page=%s&limit=%s" % (self.options.host, page, limit)

        res = self.restClient.request(
            method="GET",
            url=url,
            token=self.tokenProvider.getAccessToken()
        )

        if res.get("code") == 200:
            return res.get("data")
        else:
            self.options.on_error(res.get("code"), res.get("message"))

    def create(self, name, identifier, redirect_uris, logo=None):
        """创建应用

        Args:
            name(str): 应用名称
            identifier(str): 应用唯一标志符
            redirect_uris(list): 回调链接
            logo(str): Logo图标地址
        """
        if not isinstance(redirect_uris, list):
            raise AuthingWrongArgumentException('empty redirect_uris list')

        url = "%s/api/v2/applications" % self.options.host

        res = self.restClient.request(
            method="POST",
            url=url,
            json={
                "name": name,
                "identifier": identifier,
                "redirectUris": redirect_uris,
                "logo": logo
            },
            token=self.tokenProvider.getAccessToken()
        )

        if res.get("code") == 200:
            return res.get("data")
        else:
            self.options.on_error(res.get("code"), res.get("message"))

    def delete(self, app_id):
        """删除应用

        Args:
            app_id(str):应用id
        """
        url = "%s/api/v2/applications/%s" % (self.options.host, app_id)

        res = self.restClient.request(
            method="DELETE",
            url=url,
            token=self.tokenProvider.getAccessToken()
        )

        code, data, message = res.get("code"), res.get("data"), res.get("message")

        if code == 200:
            return True
        else:
            self.options.on_error(code, message)

    def find_by_id(self, app_id):
        """通过应用 id 查找应用详情"""
        url = "%s/api/v2/applications/%s" % (self.options.host, app_id)

        res = self.restClient.request(
            method="GET",
            url=url,
            token=self.tokenProvider.getAccessToken()
        )

        code, data, message = res.get("code"), res.get("data"), res.get("message")

        if code == 200:
            return data
        else:
            self.options.on_error(code, message)

    def list_resources(self, app_id, page=1, limit=10, resource_type=None):
        """获取资源列表"""
        if resource_type:
            self.__super__.check.resource_type(resource_type)

        self.__super__.check.page_options(page, limit)

        return self.__super__.acl.list_resources(
            namespace=app_id,
            resource_type=resource_type,
            page=page,
            limit=limit
        )

    def create_resource(self, app_id, code, resource_type, actions, description=None):
        """创建资源"""
        self.__super__.check.resource_type(resource_type)

        return self.__super__.acl.create_resource(
            namespace=app_id,
            code=code,
            resource_type=resource_type,
            actions=actions,
            description=description
        )

    def update_resource(self, app_id, code, resource_type=None, actions=None, description=None):
        """更新资源"""
        self.__super__.check.resource_type(resource_type)

        return self.__super__.acl.update_resource(
            namespace=app_id,
            code=code,
            resource_type=resource_type,
            actions=actions,
            description=description
        )

    def delete_resource(self, app_id, code):
        """删除资源"""
        return self.__super__.acl.delete_resource(
            namespace=app_id,
            code=code
        )

    def get_access_policies(self, app_id, page=1, limit=10):
        """获取应用访问控制策略列表"""
        self.__super__.check.page_options(page, limit)

        url = "%s/api/v2/applications/%s/authorization/records" % (self.options.host, app_id)

        return self.restClient.request(
            method="GET",
            url=url,
            token=self.tokenProvider.getAccessToken(),
            auto_parse_result=True,
            params={
                'page': page,
                'limit': limit
            }
        )

    def create_agreement(self, app_id, title, required=True, lang="zh-CN"):
        """创建应用协议"""
        url = "%s/api/v2/applications/%s/agreements" % (self.options.host,app_id)
        data = self.restClient.request(method="POST", url=url, token=self.tokenProvider.getAccessToken(),
                                       json={
                                           'title': title,
                                           'required': required,
                                           'lang': lang
                                       })
        return data

    def list_agreement(self, app_id):
        """应用协议列表"""
        url = "%s/api/v2/applications/%s/agreements" % (self.options.host,app_id)
        data = self.restClient.request(method="GET", url=url, token=self.tokenProvider.getAccessToken())
        return data

    def modify_agreement(self, app_id, agreement_id, title, required=True, lang="zh-CN"):
        """修改应用协议"""
        url = "%s/api/v2/applications/%s/agreements/%s" % (self.options.host, app_id, agreement_id)
        data = self.restClient.request(method="PUT", url=url, token=self.tokenProvider.getAccessToken(),
                                       json={
                                           'title': title,
                                           'required': required,
                                           'lang': lang
                                       })
        return data

    def delete_agreement(self, app_id, agreement_id):
        """删除应用协议"""
        url = "%s/api/v2/applications/%s/agreements/%s" % (self.options.host, app_id, agreement_id)
        data = self.restClient.request(method="DELETE", url=url, token=self.tokenProvider.getAccessToken())
        return data

    def sort_agreement(self, app_id, order):
        """应用协议排序"""
        url = "%s/api/v2/applications/%s/agreements/sort" % (self.options.host, app_id)
        data = self.restClient.request(method="POST", url=url, token=self.tokenProvider.getAccessToken(), json={
            "ids": order
        })
        return data

    def refresh_application_secret(self, app_id):
        """刷新应用密钥"""
        url = "%s/api/v2/application/%s/refresh-secret" % (self.options.host, app_id)
        data = self.restClient.request(method="PATCH", url=url, token=self.tokenProvider.getAccessToken())
        return data

    def active_users(self, app_id, page=1, limit=10):
        """查看应用下已登录用户"""
        url = "%s/api/v2/applications/%s/active-users?page=%s&%s" % (self.options.host, app_id, page, limit)
        data = self.restClient.request(method="GET", url=url, token=self.tokenProvider.getAccessToken())
        return data