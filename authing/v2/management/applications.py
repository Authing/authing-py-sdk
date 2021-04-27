# coding: utf-8
from authing.v2.exceptions import AuthingWrongArgumentException


class ApplicationsManagementClient(object):
    """Authing Applications Management Client"""

    def __init__(self, options, graphqlClient, restClient, tokenProvider):
        self.options = options
        self.graphqlClient = graphqlClient
        self.restClient = restClient
        self.tokenProvider = tokenProvider

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