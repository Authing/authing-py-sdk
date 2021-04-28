# coding: utf-8
from authing.v2.exceptions import AuthingWrongArgumentException


class ApplicationsManagementClient(object):
    """Authing Applications Management Client"""

    def __init__(self, options, graphqlClient, restClient, tokenProvider, managementClient):
        self.options = options
        self.graphqlClient = graphqlClient
        self.restClient = restClient
        self.tokenProvider = tokenProvider
        self.__super__ = managementClient

    def list(self, page=1, limit=10):
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
        self.__super__.check.resource_type(resource_type)

        return self.__super__.acl.create_resource(
            namespace=app_id,
            code=code,
            resource_type=resource_type,
            actions=actions,
            description=description
        )

    def update_resource(self, app_id, code, resource_type=None, actions=None, description=None):
        self.__super__.check.resource_type(resource_type)

        return self.__super__.acl.create_resource(
            namespace=app_id,
            code=code,
            resource_type=resource_type,
            actions=actions,
            description=description
        )

    def delete_resource(self, app_id, code):

        return self.__super__.acl.delete_resource(
            namespace=app_id,
            code=code
        )

    def get_access_policies(self, app_id, page=1, limit=10):
        self.__super__.check.page_options(page, limit)

        url = "%s/api/v2/applications/%s/authorization/records" % (self.options.host, app_id)

        return self.restClient.request(
            method="GET",
            url=url,
            token=self.tokenProvider.getAccessToken(),
            auto_parse_result=True
        )

    # def enable_access_policy(self, app_id, target_type, target_identifiers, inherit_by_children=None):
