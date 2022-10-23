# coding: utf-8

from .http.ManagementHttpClient import ManagementHttpClient


class ManagementClient(object):
    """Authing Management Client"""

    def __init__(
        self,
        access_key_id,
        access_key_secret,
        host=None,
        timeout=10.0,
        lang=None,
        use_unverified_ssl=False,
    ):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.host = host or "https://api.authing.cn"
        self.timeout = timeout
        self.lang = lang
        self.use_unverified_ssl = use_unverified_ssl
        self.http_client = ManagementHttpClient(
            host=self.host,
            lang=self.lang,
            use_unverified_ssl=self.use_unverified_ssl,
            access_key_id=self.access_key_id,
            access_key_secret=self.access_key_secret,
        )

    def list_users(self, keywords=None, advanced_filter=None, options=None):
        """获取/搜索用户列表


        此接口用于获取用户列表，支持模糊搜索，以及通过用户基础字段、用户自定义字段、用户所在部门、用户历史登录应用等维度筛选用户。

        ### 模糊搜素示例

        模糊搜索默认会从 `phone`, `email`, `name`, `username`, `nickname` 五个字段对用户进行模糊搜索，你也可以通过设置 `options.fuzzySearchOn`
        决定模糊匹配的字段范围：

        ```json
        {
          "keywords": "北京",
          "options": {
            "fuzzySearchOn": [
              "address"
            ]
          }
        }
        ```

        ### 高级搜索示例

        你可以通过 `advancedFilter` 进行高级搜索，高级搜索支持通过用户的基础信息、自定义数据、所在部门、用户来源、登录应用、外部身份源信息等维度对用户进行筛选。
        **且这些筛选条件可以任意组合。**

        #### 筛选状态为禁用的用户

        用户状态（`status`）为字符串类型，可选值为 `Activated` 和 `Suspended`：

        ```json
        {
          "advancedFilter": [
            {
              "field": "status",
              "operator": "EQUAL",
              "value": "Suspended"
            }
          ]
        }
        ```

        #### 筛选邮箱中包含 `@example.com` 的用户

        用户邮箱（`email`）为字符串类型，可以进行模糊搜索：

        ```json
        {
          "advancedFilter": [
            {
              "field": "email",
              "operator": "CONTAINS",
              "value": "@example.com"
            }
          ]
        }
        ```

        #### 根据用户的任意扩展字段进行搜索

        ```json
        {
          "advancedFilter": [
            {
              "field": "some-custom-key",
              "operator": "EQUAL",
              "value": "some-value"
            }
          ]
        }
        ```

        #### 根据用户登录次数筛选

        筛选登录次数大于 10 的用户：

        ```json
        {
          "advancedFilter": [
            {
              "field": "loginsCount",
              "operator": "GREATER",
              "value": 10
            }
          ]
        }
        ```

        筛选登录次数在 10 - 100 次的用户：

        ```json
        {
          "advancedFilter": [
            {
              "field": "loginsCount",
              "operator": "BETWEEN",
              "value": [10, 100]
            }
          ]
        }
        ```

        #### 根据用户上次登录时间进行筛选

        筛选最近 7 天内登录过的用户：

        ```json
        {
          "advancedFilter": [
            {
              "field": "lastLoginTime",
              "operator": "GREATER",
              "value": new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)
            }
          ]
        }
        ```

        筛选在某一段时间内登录过的用户：

        ```json
        {
          "advancedFilter": [
            {
              "field": "lastLoginTime",
              "operator": "BETWEEN",
              "value": [
                new Date(Date.now() - 14 * 24 * 60 * 60 * 1000),
                new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)
              ]
            }
          ]
        }
        ```

        #### 根据用户曾经登录过的应用筛选

        筛选出曾经登录过应用 `appId1` 或者 `appId2` 的用户：

        ```json
        {
          "advancedFilter": [
            {
              "field": "loggedInApps",
              "operator": "IN",
              "value": [
                "appId1",
                "appId2"
              ]
            }
          ]
        }
        ```

        #### 根据用户所在部门进行筛选

        ```json
        {
          "advancedFilter": [
            {
              "field": "department",
              "operator": "IN",
              "value": [
                {
                  "organizationCode": "steamory",
                  "departmentId": "root",
                  "departmentIdType": "department_id",
                  "includeChildrenDepartments": true
                }
              ]
            }
          ]
        }
        ```



                Attributes:
                    keywords (str): 模糊搜索关键字
                    advanced_filter (list): 高级搜索
                    options (dict): 可选项
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/list-users",
            json={
                "keywords": keywords,
                "advancedFilter": advanced_filter,
                "options": options,
            },
        )

    def list_users_legacy(
        self,
        page=None,
        limit=None,
        status=None,
        updated_at_start=None,
        updated_at_end=None,
        with_custom_data=None,
        with_identities=None,
        with_department_ids=None,
    ):
        """获取用户列表

        获取用户列表接口，支持分页，可以选择获取自定义数据、identities 等。

        Attributes:
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            status (str): 账户当前状态，如 已停用、已离职、正常状态、已归档
            updatedAtStart (int): 用户创建、修改开始时间，为精确到秒的 UNIX 时间戳；支持获取从某一段时间之后的增量数据
            updatedAtEnd (int): 用户创建、修改终止时间，为精确到秒的 UNIX 时间戳；支持获取某一段时间内的增量数据。默认为当前时间
            withCustomData (bool): 是否获取自定义数据
            withIdentities (bool): 是否获取 identities
            withDepartmentIds (bool): 是否获取部门 ID 列表
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/list-users",
            params={
                "page": page,
                "limit": limit,
                "status": status,
                "updatedAtStart": updated_at_start,
                "updatedAtEnd": updated_at_end,
                "withCustomData": with_custom_data,
                "withIdentities": with_identities,
                "withDepartmentIds": with_department_ids,
            },
        )

    def get_user(
        self,
        user_id,
        user_id_type=None,
        with_custom_data=None,
        with_identities=None,
        with_department_ids=None,
    ):
        """获取用户信息

                通过用户 ID，获取用户详情，可以选择获取自定义数据、identities、选择指定用户 ID 类型等。

                Attributes:
                    userId (str): 用户 ID
                    userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
        - `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
        - `phone`: 用户手机号
        - `email`: 用户邮箱
        - `username`: 用户名
        - `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
        - `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
        示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。

                    withCustomData (bool): 是否获取自定义数据
                    withIdentities (bool): 是否获取 identities
                    withDepartmentIds (bool): 是否获取部门 ID 列表
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-user",
            params={
                "userId": user_id,
                "userIdType": user_id_type,
                "withCustomData": with_custom_data,
                "withIdentities": with_identities,
                "withDepartmentIds": with_department_ids,
            },
        )

    def get_user_batch(
        self,
        user_ids,
        user_id_type=None,
        with_custom_data=None,
        with_identities=None,
        with_department_ids=None,
    ):
        """批量获取用户信息

                通过用户 ID 列表，批量获取用户信息，可以选择获取自定义数据、identities、选择指定用户 ID 类型等。

                Attributes:
                    userIds (str): 用户 ID 数组
                    userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
        - `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
        - `phone`: 用户手机号
        - `email`: 用户邮箱
        - `username`: 用户名
        - `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
        - `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
        示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。

                    withCustomData (bool): 是否获取自定义数据
                    withIdentities (bool): 是否获取 identities
                    withDepartmentIds (bool): 是否获取部门 ID 列表
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-user-batch",
            params={
                "userIds": user_ids,
                "userIdType": user_id_type,
                "withCustomData": with_custom_data,
                "withIdentities": with_identities,
                "withDepartmentIds": with_department_ids,
            },
        )

    def create_user(
        self,
        status=None,
        email=None,
        phone=None,
        phone_country_code=None,
        username=None,
        external_id=None,
        name=None,
        nickname=None,
        photo=None,
        gender=None,
        email_verified=None,
        phone_verified=None,
        birthdate=None,
        country=None,
        province=None,
        city=None,
        address=None,
        street_address=None,
        postal_code=None,
        company=None,
        browser=None,
        device=None,
        given_name=None,
        family_name=None,
        middle_name=None,
        profile=None,
        preferred_username=None,
        website=None,
        zoneinfo=None,
        locale=None,
        formatted=None,
        region=None,
        password=None,
        salt=None,
        tenant_ids=None,
        otp=None,
        department_ids=None,
        custom_data=None,
        identities=None,
        options=None,
    ):
        """创建用户

        创建用户，邮箱、手机号、用户名必须包含其中一个，邮箱、手机号、用户名、externalId 用户池内唯一，此接口将以管理员身份创建用户因此不需要进行手机号验证码检验等安全检测。

        Attributes:
            status (str): 账户当前状态
            email (str): 邮箱，不区分大小写
            phone (str): 手机号，不带区号。如果是国外手机号，请在 phoneCountryCode 参数中指定区号。
            phone_country_code (str): 手机区号，中国大陆手机号可不填。Authing 短信服务暂不内置支持国际手机号，你需要在 Authing 控制台配置对应的国际短信服务。完整的手机区号列表可参阅 https://en.wikipedia.org/wiki/List_of_country_calling_codes。
            username (str): 用户名，用户池内唯一
            external_id (str): 第三方外部 ID
            name (str): 用户真实名称，不具备唯一性
            nickname (str): 昵称
            photo (str): 头像链接
            gender (str): 性别
            email_verified (bool): 邮箱是否验证
            phone_verified (bool): 手机号是否验证
            birthdate (str): 出生日期
            country (str): 所在国家
            province (str): 所在省份
            city (str): 所在城市
            address (str): 所处地址
            street_address (str): 所处街道地址
            postal_code (str): 邮政编码号
            company (str): 所在公司
            browser (str): 最近一次登录时使用的浏览器 UA
            device (str): 最近一次登录时使用的设备
            given_name (str): 名
            family_name (str): 姓
            middle_name (str): 中间名
            profile (str): Preferred Username
            preferred_username (str): Preferred Username
            website (str): 用户个人网页
            zoneinfo (str): 用户时区信息
            locale (str): Locale
            formatted (str): 标准的完整地址
            region (str): 用户所在区域
            password (str): 用户密码。我们使用 HTTPS 协议对密码进行安全传输，可以在一定程度上保证安全性。如果你还需要更高级别的安全性，我们还支持 RSA256 和国密 SM2 两种方式对密码进行加密。详情见 `passwordEncryptType` 参数。
            salt (str): 加密用户密码的盐
            tenant_ids (list): 租户 ID
            otp (dict): 用户的 OTP 验证器
            department_ids (list): 用户所属部门 ID 列表
            custom_data (dict): 自定义数据，传入的对象中的 key 必须先在用户池定义相关自定义字段
            identities (list): 第三方身份源（建议调用绑定接口进行绑定）
            options (dict): 可选参数
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/create-user",
            json={
                "status": status,
                "email": email,
                "phone": phone,
                "phoneCountryCode": phone_country_code,
                "username": username,
                "externalId": external_id,
                "name": name,
                "nickname": nickname,
                "photo": photo,
                "gender": gender,
                "emailVerified": email_verified,
                "phoneVerified": phone_verified,
                "birthdate": birthdate,
                "country": country,
                "province": province,
                "city": city,
                "address": address,
                "streetAddress": street_address,
                "postalCode": postal_code,
                "company": company,
                "browser": browser,
                "device": device,
                "givenName": given_name,
                "familyName": family_name,
                "middleName": middle_name,
                "profile": profile,
                "preferredUsername": preferred_username,
                "website": website,
                "zoneinfo": zoneinfo,
                "locale": locale,
                "formatted": formatted,
                "region": region,
                "password": password,
                "salt": salt,
                "tenantIds": tenant_ids,
                "otp": otp,
                "departmentIds": department_ids,
                "customData": custom_data,
                "identities": identities,
                "options": options,
            },
        )

    def create_users_batch(self, list, options=None):
        """批量创建用户

        批量创建用户，邮箱、手机号、用户名必须包含其中一个，邮箱、手机号、用户名、externalId 用户池内唯一，此接口将以管理员身份创建用户因此不需要进行手机号验证码检验等安全检测。

        Attributes:
            list (list): 用户列表
            options (dict): 可选参数
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/create-users-batch",
            json={
                "list": list,
                "options": options,
            },
        )

    def update_user(
        self,
        user_id,
        phone_country_code=None,
        name=None,
        nickname=None,
        photo=None,
        external_id=None,
        status=None,
        email_verified=None,
        phone_verified=None,
        birthdate=None,
        country=None,
        province=None,
        city=None,
        address=None,
        street_address=None,
        postal_code=None,
        gender=None,
        username=None,
        email=None,
        phone=None,
        password=None,
        company=None,
        browser=None,
        device=None,
        given_name=None,
        family_name=None,
        middle_name=None,
        profile=None,
        preferred_username=None,
        website=None,
        zoneinfo=None,
        locale=None,
        formatted=None,
        region=None,
        custom_data=None,
        options=None,
    ):
        """修改用户资料

        通过用户 ID，修改用户资料，邮箱、手机号、用户名、externalId 用户池内唯一，此接口将以管理员身份修改用户资料因此不需要进行手机号验证码检验等安全检测。

        Attributes:
            user_id (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            phone_country_code (str): 手机区号，中国大陆手机号可不填。Authing 短信服务暂不内置支持国际手机号，你需要在 Authing 控制台配置对应的国际短信服务。完整的手机区号列表可参阅 https://en.wikipedia.org/wiki/List_of_country_calling_codes。
            name (str): 用户真实名称，不具备唯一性
            nickname (str): 昵称
            photo (str): 头像链接
            external_id (str): 第三方外部 ID
            status (str): 账户当前状态
            email_verified (bool): 邮箱是否验证
            phone_verified (bool): 手机号是否验证
            birthdate (str): 出生日期
            country (str): 所在国家
            province (str): 所在省份
            city (str): 所在城市
            address (str): 所处地址
            street_address (str): 所处街道地址
            postal_code (str): 邮政编码号
            gender (str): 性别
            username (str): 用户名，用户池内唯一
            email (str): 邮箱，不区分大小写
            phone (str): 手机号，不带区号。如果是国外手机号，请在 phoneCountryCode 参数中指定区号。
            password (str): 用户密码。我们使用 HTTPS 协议对密码进行安全传输，可以在一定程度上保证安全性。如果你还需要更高级别的安全性，我们还支持 RSA256 和国密 SM2 两种方式对密码进行加密。详情见 `passwordEncryptType` 参数。
            company (str): 所在公司
            browser (str): 最近一次登录时使用的浏览器 UA
            device (str): 最近一次登录时使用的设备
            given_name (str): 名
            family_name (str): 姓
            middle_name (str): 中间名
            profile (str): Preferred Username
            preferred_username (str): Preferred Username
            website (str): 用户个人网页
            zoneinfo (str): 用户时区信息
            locale (str): Locale
            formatted (str): 标准的完整地址
            region (str): 用户所在区域
            custom_data (dict): 自定义数据，传入的对象中的 key 必须先在用户池定义相关自定义字段
            options (dict): 可选参数
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/update-user",
            json={
                "userId": user_id,
                "phoneCountryCode": phone_country_code,
                "name": name,
                "nickname": nickname,
                "photo": photo,
                "externalId": external_id,
                "status": status,
                "emailVerified": email_verified,
                "phoneVerified": phone_verified,
                "birthdate": birthdate,
                "country": country,
                "province": province,
                "city": city,
                "address": address,
                "streetAddress": street_address,
                "postalCode": postal_code,
                "gender": gender,
                "username": username,
                "email": email,
                "phone": phone,
                "password": password,
                "company": company,
                "browser": browser,
                "device": device,
                "givenName": given_name,
                "familyName": family_name,
                "middleName": middle_name,
                "profile": profile,
                "preferredUsername": preferred_username,
                "website": website,
                "zoneinfo": zoneinfo,
                "locale": locale,
                "formatted": formatted,
                "region": region,
                "customData": custom_data,
                "options": options,
            },
        )

    def update_user_batch(self, list, options=None):
        """批量修改用户资料

        批量修改用户资料，邮箱、手机号、用户名、externalId 用户池内唯一，此接口将以管理员身份修改用户资料因此不需要进行手机号验证码检验等安全检测。

        Attributes:
            list (list): 用户列表
            options (dict): 可选参数
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/update-user-batch",
            json={
                "list": list,
                "options": options,
            },
        )

    def delete_users_batch(self, user_ids, options=None):
        """删除用户

        通过用户 ID 列表，删除用户，支持批量删除，可以选择指定用户 ID 类型等。

        Attributes:
            user_ids (list): 用户 ID 列表
            options (dict): 可选参数
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/delete-users-batch",
            json={
                "userIds": user_ids,
                "options": options,
            },
        )

    def get_user_identities(self, user_id, user_id_type=None):
        """获取用户的外部身份源

                通过用户 ID，获取用户的外部身份源、选择指定用户 ID 类型。

                Attributes:
                    userId (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
                    userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
        - `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
        - `phone`: 用户手机号
        - `email`: 用户邮箱
        - `username`: 用户名
        - `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
        - `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
        示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。

        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-user-identities",
            params={
                "userId": user_id,
                "userIdType": user_id_type,
            },
        )

    def get_user_roles(self, user_id, user_id_type=None, namespace=None):
        """获取用户角色列表

                通过用户 ID，获取用户角色列表，可以选择所属权限分组 code、选择指定用户 ID 类型等。

                Attributes:
                    userId (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
                    userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
        - `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
        - `phone`: 用户手机号
        - `email`: 用户邮箱
        - `username`: 用户名
        - `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
        - `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
        示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。

                    namespace (str): 所属权限分组的 code
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-user-roles",
            params={
                "userId": user_id,
                "userIdType": user_id_type,
                "namespace": namespace,
            },
        )

    def get_user_principal_authentication_info(self, user_id, user_id_type=None):
        """获取用户实名认证信息

                通过用户 ID，获取用户实名认证信息，可以选择指定用户 ID 类型。

                Attributes:
                    userId (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
                    userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
        - `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
        - `phone`: 用户手机号
        - `email`: 用户邮箱
        - `username`: 用户名
        - `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
        - `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
        示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。

        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-user-principal-authentication-info",
            params={
                "userId": user_id,
                "userIdType": user_id_type,
            },
        )

    def reset_user_principal_authentication_info(self, user_id, options=None):
        """删除用户实名认证信息

        通过用户 ID，删除用户实名认证信息，可以选择指定用户 ID 类型等。

        Attributes:
            user_id (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            options (dict): 可选参数
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/reset-user-principal-authentication-info",
            json={
                "userId": user_id,
                "options": options,
            },
        )

    def get_user_departments(
        self,
        user_id,
        user_id_type=None,
        page=None,
        limit=None,
        with_custom_data=None,
        sort_by=None,
        order_by=None,
    ):
        """获取用户部门列表

                通过用户 ID，获取用户部门列表，支持分页，可以选择获取自定义数据、选择指定用户 ID 类型、增序或降序等。

                Attributes:
                    userId (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
                    userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
        - `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
        - `phone`: 用户手机号
        - `email`: 用户邮箱
        - `username`: 用户名
        - `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
        - `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
        示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。

                    page (int): 当前页数，从 1 开始
                    limit (int): 每页数目，最大不能超过 50，默认为 10
                    withCustomData (bool): 是否获取自定义数据
                    sortBy (str): 排序依据，如 部门创建时间、加入部门时间、部门名称、部门标志符
                    orderBy (str): 增序或降序
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-user-departments",
            params={
                "userId": user_id,
                "userIdType": user_id_type,
                "page": page,
                "limit": limit,
                "withCustomData": with_custom_data,
                "sortBy": sort_by,
                "orderBy": order_by,
            },
        )

    def set_user_departments(self, departments, user_id, options=None):
        """设置用户所在部门

        通过用户 ID，设置用户所在部门，可以选择指定用户 ID 类型等。

        Attributes:
            departments (list): 部门信息
            user_id (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            options (dict): 可选参数
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/set-user-departments",
            json={
                "departments": departments,
                "userId": user_id,
                "options": options,
            },
        )

    def get_user_groups(self, user_id, user_id_type=None):
        """获取用户分组列表

                通过用户 ID，获取用户分组列表，可以选择指定用户 ID 类型等。

                Attributes:
                    userId (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
                    userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
        - `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
        - `phone`: 用户手机号
        - `email`: 用户邮箱
        - `username`: 用户名
        - `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
        - `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
        示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。

        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-user-groups",
            params={
                "userId": user_id,
                "userIdType": user_id_type,
            },
        )

    def get_user_mfa_info(self, user_id, user_id_type=None):
        """获取用户 MFA 绑定信息

                通过用户 ID，获取用户 MFA 绑定信息，可以选择指定用户 ID 类型等。

                Attributes:
                    userId (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
                    userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
        - `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
        - `phone`: 用户手机号
        - `email`: 用户邮箱
        - `username`: 用户名
        - `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
        - `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
        示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。

        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-user-mfa-info",
            params={
                "userId": user_id,
                "userIdType": user_id_type,
            },
        )

    def list_archived_users(self, page=None, limit=None, start_at=None):
        """获取已归档的用户列表

        获取已归档的用户列表，支持分页，可以筛选开始时间等。

        Attributes:
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            startAt (int): 开始时间，为精确到秒的 UNIX 时间戳，默认不指定
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/list-archived-users",
            params={
                "page": page,
                "limit": limit,
                "startAt": start_at,
            },
        )

    def kick_users(self, app_ids, user_id, options=None):
        """强制下线用户

        通过用户 ID、App ID 列表，强制让用户下线，可以选择指定用户 ID 类型等。

        Attributes:
            app_ids (list): APP ID 列表
            user_id (str): 用户 ID
            options (dict): 可选参数
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/kick-users",
            json={
                "appIds": app_ids,
                "userId": user_id,
                "options": options,
            },
        )

    def is_user_exists(self, username=None, email=None, phone=None, external_id=None):
        """判断用户是否存在

        根据条件判断用户是否存在，可以筛选用户名、邮箱、手机号、第三方外部 ID 等。

        Attributes:
            username (str): 用户名，用户池内唯一
            email (str): 邮箱，不区分大小写
            phone (str): 手机号，不带区号。如果是国外手机号，请在 phoneCountryCode 参数中指定区号。
            external_id (str): 第三方外部 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/is-user-exists",
            json={
                "username": username,
                "email": email,
                "phone": phone,
                "externalId": external_id,
            },
        )

    def get_user_accessible_apps(self, user_id, user_id_type=None):
        """获取用户可访问的应用

                通过用户 ID，获取用户可访问的应用，可以选择指定用户 ID 类型等。

                Attributes:
                    userId (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
                    userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
        - `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
        - `phone`: 用户手机号
        - `email`: 用户邮箱
        - `username`: 用户名
        - `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
        - `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
        示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。

        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-user-accessible-apps",
            params={
                "userId": user_id,
                "userIdType": user_id_type,
            },
        )

    def get_user_authorized_apps(self, user_id, user_id_type=None):
        """获取用户授权的应用

                通过用户 ID，获取用户授权的应用，可以选择指定用户 ID 类型等。

                Attributes:
                    userId (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
                    userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
        - `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
        - `phone`: 用户手机号
        - `email`: 用户邮箱
        - `username`: 用户名
        - `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
        - `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
        示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。

        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-user-authorized-apps",
            params={
                "userId": user_id,
                "userIdType": user_id_type,
            },
        )

    def has_any_role(self, roles, user_id, options=None):
        """判断用户是否有某个角色

        通过用户 ID，判断用户是否有某个角色，支持传入多个角色，可以选择指定用户 ID 类型等。

        Attributes:
            roles (list): 角色列表
            user_id (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            options (dict): 可选参数
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/has-any-role",
            json={
                "roles": roles,
                "userId": user_id,
                "options": options,
            },
        )

    def get_user_login_history(
        self,
        user_id,
        user_id_type=None,
        app_id=None,
        client_ip=None,
        start=None,
        end=None,
        page=None,
        limit=None,
    ):
        """获取用户的登录历史记录

                通过用户 ID，获取用户登录历史记录，支持分页，可以选择指定用户 ID 类型、应用 ID、开始与结束时间戳等。

                Attributes:
                    userId (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
                    userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
        - `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
        - `phone`: 用户手机号
        - `email`: 用户邮箱
        - `username`: 用户名
        - `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
        - `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
        示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。

                    appId (str): 应用 ID
                    clientIp (str): 客户端 IP
                    start (int): 开始时间戳（毫秒）
                    end (int): 结束时间戳（毫秒）
                    page (int): 当前页数，从 1 开始
                    limit (int): 每页数目，最大不能超过 50，默认为 10
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-user-login-history",
            params={
                "userId": user_id,
                "userIdType": user_id_type,
                "appId": app_id,
                "clientIp": client_ip,
                "start": start,
                "end": end,
                "page": page,
                "limit": limit,
            },
        )

    def get_user_loggedin_apps(self, user_id, user_id_type=None):
        """获取用户曾经登录过的应用

                通过用户 ID，获取用户曾经登录过的应用，可以选择指定用户 ID 类型等。

                Attributes:
                    userId (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
                    userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
        - `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
        - `phone`: 用户手机号
        - `email`: 用户邮箱
        - `username`: 用户名
        - `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
        - `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
        示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。

        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-user-loggedin-apps",
            params={
                "userId": user_id,
                "userIdType": user_id_type,
            },
        )

    def get_user_loggedin_identities(self, user_id, user_id_type=None):
        """获取用户曾经登录过的身份源

                通过用户 ID，获取用户曾经登录过的身份源，可以选择指定用户 ID 类型等。

                Attributes:
                    userId (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
                    userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
        - `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
        - `phone`: 用户手机号
        - `email`: 用户邮箱
        - `username`: 用户名
        - `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
        - `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
        示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。

        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-user-logged-in-identities",
            params={
                "userId": user_id,
                "userIdType": user_id_type,
            },
        )

    def resign_user(self, user_id, user_id_type=None):
        """用户离职

                通过用户 ID，对用户进行离职操作

                Attributes:
                    user_id (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
                    user_id_type (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
        - `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
        - `phone`: 用户手机号
        - `email`: 用户邮箱
        - `username`: 用户名
        - `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
        - `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
        示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。

        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/resign-user",
            json={
                "userId": user_id,
                "userIdType": user_id_type,
            },
        )

    def resign_user_batch(self, user_ids, user_id_type=None):
        """批量用户离职

                通过用户 ID，对用户进行离职操作

                Attributes:
                    user_ids (list): 用户 ID 数组
                    user_id_type (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
        - `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
        - `phone`: 用户手机号
        - `email`: 用户邮箱
        - `username`: 用户名
        - `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
        - `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
        示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。

        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/resign-user-batch",
            json={
                "userIds": user_ids,
                "userIdType": user_id_type,
            },
        )

    def get_user_authorized_resources(
        self, user_id, user_id_type=None, namespace=None, resource_type=None
    ):
        """获取用户被授权的所有资源

                通过用户 ID，获取用户被授权的所有资源，可以选择指定用户 ID 类型等，用户被授权的资源是用户自身被授予、通过分组继承、通过角色继承、通过组织机构继承的集合。

                Attributes:
                    userId (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
                    userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
        - `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
        - `phone`: 用户手机号
        - `email`: 用户邮箱
        - `username`: 用户名
        - `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
        - `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
        示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。

                    namespace (str): 所属权限分组的 code
                    resourceType (str): 资源类型，如 数据、API、菜单、按钮
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-user-authorized-resources",
            params={
                "userId": user_id,
                "userIdType": user_id_type,
                "namespace": namespace,
                "resourceType": resource_type,
            },
        )

    def check_session_status(self, app_id, user_id):
        """检查某个用户在应用下是否具备 Session 登录态

        检查某个用户在应用下是否具备 Session 登录态

        Attributes:
            app_id (str): App ID
            user_id (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/check-session-status",
            json={
                "appId": app_id,
                "userId": user_id,
            },
        )

    def import_otp(self, list):
        """导入用户的 OTP

        导入用户的 OTP

        Attributes:
            list (list): 参数列表
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/import-otp",
            json={
                "list": list,
            },
        )

    def get_organization(self, organization_code, with_custom_data=None):
        """获取组织机构详情

        获取组织机构详情

        Attributes:
            organizationCode (str): 组织 Code（organizationCode）
            withCustomData (bool): 是否获取自定义数据
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-organization",
            params={
                "organizationCode": organization_code,
                "withCustomData": with_custom_data,
            },
        )

    def get_organizations_batch(self, organization_code_list, with_custom_data=None):
        """批量获取组织机构详情

        批量获取组织机构详情

        Attributes:
            organizationCodeList (str): 组织 Code（organizationCode）列表
            withCustomData (bool): 是否获取自定义数据
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-organization-batch",
            params={
                "organizationCodeList": organization_code_list,
                "withCustomData": with_custom_data,
            },
        )

    def list_organizations(
        self, page=None, limit=None, fetch_all=None, with_custom_data=None
    ):
        """获取组织机构列表

        获取组织机构列表，支持分页。

        Attributes:
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            fetchAll (bool): 拉取所有
            withCustomData (bool): 是否获取自定义数据
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/list-organizations",
            params={
                "page": page,
                "limit": limit,
                "fetchAll": fetch_all,
                "withCustomData": with_custom_data,
            },
        )

    def create_organization(
        self,
        organization_name,
        organization_code,
        description=None,
        open_department_id=None,
        i18n=None,
    ):
        """创建组织机构

        创建组织机构，会创建一个只有一个节点的组织机构，可以选择组织描述信息、根节点自定义 ID、多语言等。

        Attributes:
            organization_name (str): 组织名称
            organization_code (str): 组织 code
            description (str): 组织描述信息
            open_department_id (str): 根节点自定义 ID
            i18n (dict): 多语言设置
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/create-organization",
            json={
                "organizationName": organization_name,
                "organizationCode": organization_code,
                "description": description,
                "openDepartmentId": open_department_id,
                "i18n": i18n,
            },
        )

    def update_organization(
        self,
        organization_code,
        description=None,
        open_department_id=None,
        leader_user_ids=None,
        i18n=None,
        organization_new_code=None,
        organization_name=None,
    ):
        """修改组织机构

        通过组织 code，修改组织机构，可以选择部门描述、新组织 code、组织名称等。

        Attributes:
            organization_code (str): 组织 code
            description (str): 部门描述
            open_department_id (str): 根节点自定义 ID
            leader_user_ids (list): 部门负责人 ID
            i18n (dict): 多语言设置
            organization_new_code (str): 新组织 code
            organization_name (str): 组织名称
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/update-organization",
            json={
                "organizationCode": organization_code,
                "description": description,
                "openDepartmentId": open_department_id,
                "leaderUserIds": leader_user_ids,
                "i18n": i18n,
                "organizationNewCode": organization_new_code,
                "organizationName": organization_name,
            },
        )

    def delete_organization(self, organization_code):
        """删除组织机构

        通过组织 code，删除组织机构树。

        Attributes:
            organization_code (str): 组织 code
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/delete-organization",
            json={
                "organizationCode": organization_code,
            },
        )

    def search_organizations(
        self, keywords, page=None, limit=None, with_custom_data=None
    ):
        """搜索组织机构列表

        通过搜索关键词，搜索组织机构列表，支持分页。

        Attributes:
            keywords (str): 搜索关键词，如组织机构名称
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            withCustomData (bool): 是否获取自定义数据
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/search-organizations",
            params={
                "keywords": keywords,
                "page": page,
                "limit": limit,
                "withCustomData": with_custom_data,
            },
        )

    def get_department(
        self,
        organization_code,
        department_id=None,
        department_code=None,
        department_id_type=None,
        with_custom_data=None,
    ):
        """获取部门信息

        通过组织 code 以及 部门 ID 或 部门 code，获取部门信息，可以获取自定义数据。

        Attributes:
            organizationCode (str): 组织 code
            departmentId (str): 部门 ID，根部门传 `root`。departmentId 和 departmentCode 必传其一。
            departmentCode (str): 部门 code。departmentId 和 departmentCode 必传其一。
            departmentIdType (str): 此次调用中使用的部门 ID 的类型
            withCustomData (bool): 是否获取自定义数据
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-department",
            params={
                "organizationCode": organization_code,
                "departmentId": department_id,
                "departmentCode": department_code,
                "departmentIdType": department_id_type,
                "withCustomData": with_custom_data,
            },
        )

    def create_department(
        self,
        parent_department_id,
        name,
        organization_code,
        open_department_id=None,
        description=None,
        code=None,
        is_virtual_node=None,
        i18n=None,
        custom_data=None,
        department_id_type=None,
    ):
        """创建部门

        通过组织 code、部门名称、父部门 ID，创建部门，可以设置多种参数。

        Attributes:
            parent_department_id (str): 父部门 id
            name (str): 部门名称
            organization_code (str): 组织 Code（organizationCode）
            open_department_id (str): 自定义部门 ID，用于存储自定义的 ID
            description (str): 部门描述
            code (str): 部门识别码
            is_virtual_node (bool): 是否是虚拟部门
            i18n (dict): 多语言设置
            custom_data (dict): 部门的扩展字段数据
            department_id_type (str): 此次调用中使用的父部门 ID 的类型
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/create-department",
            json={
                "parentDepartmentId": parent_department_id,
                "name": name,
                "organizationCode": organization_code,
                "openDepartmentId": open_department_id,
                "description": description,
                "code": code,
                "isVirtualNode": is_virtual_node,
                "i18n": i18n,
                "customData": custom_data,
                "departmentIdType": department_id_type,
            },
        )

    def update_department(
        self,
        department_id,
        organization_code,
        leader_user_ids=None,
        description=None,
        code=None,
        i18n=None,
        name=None,
        department_id_type=None,
        parent_department_id=None,
        custom_data=None,
    ):
        """修改部门

        通过组织 code、部门 ID，修改部门，可以设置多种参数。

        Attributes:
            department_id (str): 部门系统 ID（为 Authing 系统自动生成，不可修改）
            organization_code (str): 组织 Code（organizationCode）
            leader_user_ids (list): 部门负责人 ID
            description (str): 部门描述
            code (str): 部门识别码
            i18n (dict): 多语言设置
            name (str): 部门名称
            department_id_type (str): 此次调用中使用的部门 ID 的类型
            parent_department_id (str): 父部门 ID
            custom_data (dict): 自定义数据，传入的对象中的 key 必须先在用户池定义相关自定义字段
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/update-department",
            json={
                "departmentId": department_id,
                "organizationCode": organization_code,
                "leaderUserIds": leader_user_ids,
                "description": description,
                "code": code,
                "i18n": i18n,
                "name": name,
                "departmentIdType": department_id_type,
                "parentDepartmentId": parent_department_id,
                "customData": custom_data,
            },
        )

    def delete_department(
        self, department_id, organization_code, department_id_type=None
    ):
        """删除部门

        通过组织 code、部门 ID，删除部门。

        Attributes:
            department_id (str): 部门系统 ID（为 Authing 系统自动生成，不可修改）
            organization_code (str): 组织 Code（organizationCode）
            department_id_type (str): 此次调用中使用的部门 ID 的类型
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/delete-department",
            json={
                "departmentId": department_id,
                "organizationCode": organization_code,
                "departmentIdType": department_id_type,
            },
        )

    def search_departments(self, keywords, organization_code, with_custom_data=None):
        """搜索部门

        通过组织 code、搜索关键词，搜索部门，可以搜索组织名称等。

        Attributes:
            keywords (str): 搜索关键词，如组织名称等
            organization_code (str): 组织 code
            with_custom_data (bool): 是否获取自定义数据
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/search-departments",
            json={
                "keywords": keywords,
                "organizationCode": organization_code,
                "withCustomData": with_custom_data,
            },
        )

    def list_children_departments(
        self,
        organization_code,
        department_id,
        department_id_type=None,
        exclude_virtual_node=None,
        only_virtual_node=None,
        with_custom_data=None,
    ):
        """获取子部门列表

        通过组织 code、部门 ID，获取子部门列表，可以选择获取自定义数据、虚拟组织等。

        Attributes:
            organizationCode (str): 组织 code
            departmentId (str): 需要获取的部门 ID
            departmentIdType (str): 此次调用中使用的部门 ID 的类型
            excludeVirtualNode (bool): 是否要排除虚拟组织
            onlyVirtualNode (bool): 是否只包含虚拟组织
            withCustomData (bool): 是否获取自定义数据
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/list-children-departments",
            params={
                "organizationCode": organization_code,
                "departmentId": department_id,
                "departmentIdType": department_id_type,
                "excludeVirtualNode": exclude_virtual_node,
                "onlyVirtualNode": only_virtual_node,
                "withCustomData": with_custom_data,
            },
        )

    def list_department_members(
        self,
        organization_code,
        department_id,
        sort_by,
        order_by,
        department_id_type=None,
        include_children_departments=None,
        page=None,
        limit=None,
        with_custom_data=None,
        with_identities=None,
        with_department_ids=None,
    ):
        """获取部门成员列表

        通过组织 code、部门 ID、排序，获取部门成员列表，支持分页，可以选择获取自定义数据、identities 等。

        Attributes:
            organizationCode (str): 组织 code
            departmentId (str): 部门 ID，根部门传 `root`
            sortBy (str): 排序依据
            orderBy (str): 增序还是倒序
            departmentIdType (str): 此次调用中使用的部门 ID 的类型
            includeChildrenDepartments (bool): 是否包含子部门的成员
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            withCustomData (bool): 是否获取自定义数据
            withIdentities (bool): 是否获取 identities
            withDepartmentIds (bool): 是否获取部门 ID 列表
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/list-department-members",
            params={
                "organizationCode": organization_code,
                "departmentId": department_id,
                "sortBy": sort_by,
                "orderBy": order_by,
                "departmentIdType": department_id_type,
                "includeChildrenDepartments": include_children_departments,
                "page": page,
                "limit": limit,
                "withCustomData": with_custom_data,
                "withIdentities": with_identities,
                "withDepartmentIds": with_department_ids,
            },
        )

    def list_department_member_ids(
        self, organization_code, department_id, department_id_type=None
    ):
        """获取部门直属成员 ID 列表

        通过组织 code、部门 ID，获取部门直属成员 ID 列表。

        Attributes:
            organizationCode (str): 组织 code
            departmentId (str): 部门 ID，根部门传 `root`
            departmentIdType (str): 此次调用中使用的部门 ID 的类型
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/list-department-member-ids",
            params={
                "organizationCode": organization_code,
                "departmentId": department_id,
                "departmentIdType": department_id_type,
            },
        )

    def search_department_members(
        self,
        organization_code,
        department_id,
        keywords,
        page=None,
        limit=None,
        department_id_type=None,
        include_children_departments=None,
        with_custom_data=None,
        with_identities=None,
        with_department_ids=None,
    ):
        """搜索部门下的成员

        通过组织 code、部门 ID、搜索关键词，搜索部门下的成员，支持分页，可以选择获取自定义数据、identities 等。

        Attributes:
            organizationCode (str): 组织 code
            departmentId (str): 部门 ID，根部门传 `root`
            keywords (str): 搜索关键词，如成员名称
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            departmentIdType (str): 此次调用中使用的部门 ID 的类型
            includeChildrenDepartments (bool): 是否包含子部门的成员
            withCustomData (bool): 是否获取自定义数据
            withIdentities (bool): 是否获取 identities
            withDepartmentIds (bool): 是否获取部门 ID 列表
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/search-department-members",
            params={
                "organizationCode": organization_code,
                "departmentId": department_id,
                "keywords": keywords,
                "page": page,
                "limit": limit,
                "departmentIdType": department_id_type,
                "includeChildrenDepartments": include_children_departments,
                "withCustomData": with_custom_data,
                "withIdentities": with_identities,
                "withDepartmentIds": with_department_ids,
            },
        )

    def add_department_members(
        self, user_ids, organization_code, department_id, department_id_type=None
    ):
        """部门下添加成员

        通过部门 ID、组织 code，添加部门下成员。

        Attributes:
            user_ids (list): 用户 ID 列表
            organization_code (str): 组织 code
            department_id (str): 部门系统 ID（为 Authing 系统自动生成，不可修改）
            department_id_type (str): 此次调用中使用的部门 ID 的类型
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/add-department-members",
            json={
                "userIds": user_ids,
                "organizationCode": organization_code,
                "departmentId": department_id,
                "departmentIdType": department_id_type,
            },
        )

    def remove_department_members(
        self, user_ids, organization_code, department_id, department_id_type=None
    ):
        """部门下删除成员

        通过部门 ID、组织 code，删除部门下成员。

        Attributes:
            user_ids (list): 用户 ID 列表
            organization_code (str): 组织 code
            department_id (str): 部门系统 ID（为 Authing 系统自动生成，不可修改）
            department_id_type (str): 此次调用中使用的部门 ID 的类型
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/remove-department-members",
            json={
                "userIds": user_ids,
                "organizationCode": organization_code,
                "departmentId": department_id,
                "departmentIdType": department_id_type,
            },
        )

    def get_parent_department(
        self,
        organization_code,
        department_id,
        department_id_type=None,
        with_custom_data=None,
    ):
        """获取父部门信息

        通过组织 code、部门 ID，获取父部门信息，可以选择获取自定义数据等。

        Attributes:
            organizationCode (str): 组织 code
            departmentId (str): 部门 ID
            departmentIdType (str): 此次调用中使用的部门 ID 的类型
            withCustomData (bool): 是否获取自定义数据
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-parent-department",
            params={
                "organizationCode": organization_code,
                "departmentId": department_id,
                "departmentIdType": department_id_type,
                "withCustomData": with_custom_data,
            },
        )

    def is_user_in_department(
        self,
        user_id,
        organization_code,
        department_id,
        department_id_type=None,
        include_children_departments=None,
    ):
        """判断用户是否在某个部门下

        通过组织 code、部门 ID，判断用户是否在某个部门下，可以选择包含子部门。

        Attributes:
            userId (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            organizationCode (str): 组织 code
            departmentId (str): 部门 ID，根部门传 `root`。departmentId 和 departmentCode 必传其一。
            departmentIdType (str): 此次调用中使用的部门 ID 的类型
            includeChildrenDepartments (bool): 是否包含子部门
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/is-user-in-department",
            params={
                "userId": user_id,
                "organizationCode": organization_code,
                "departmentId": department_id,
                "departmentIdType": department_id_type,
                "includeChildrenDepartments": include_children_departments,
            },
        )

    def get_group(self, code):
        """获取分组详情

        通过分组 code，获取分组详情。

        Attributes:
            code (str): 分组 code
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-group",
            params={
                "code": code,
            },
        )

    def list_groups(self, keywords=None, page=None, limit=None):
        """获取分组列表

        获取分组列表，支持分页。

        Attributes:
            keywords (str): 搜索分组 code 或分组名称
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/list-groups",
            params={
                "keywords": keywords,
                "page": page,
                "limit": limit,
            },
        )

    def create_group(self, description, name, code):
        """创建分组

        创建分组，一个分组必须包含分组名称与唯一标志符 code，且必须为一个合法的英文标志符，如 developers。

        Attributes:
            description (str): 分组描述
            name (str): 分组名称
            code (str): 分组 code
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/create-group",
            json={
                "description": description,
                "name": name,
                "code": code,
            },
        )

    def create_groups_batch(self, list):
        """批量创建分组

        批量创建分组，一个分组必须包含分组名称与唯一标志符 code，且必须为一个合法的英文标志符，如 developers。

        Attributes:
            list (list): 批量分组
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/create-groups-batch",
            json={
                "list": list,
            },
        )

    def update_group(self, description, code, name=None, new_code=None):
        """修改分组

        通过分组 code，修改分组，可以修改此分组的 code。

        Attributes:
            description (str): 分组描述
            code (str): 分组 code
            name (str): 分组名称
            new_code (str): 分组新的 code
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/update-group",
            json={
                "description": description,
                "code": code,
                "name": name,
                "newCode": new_code,
            },
        )

    def delete_groups_batch(self, code_list):
        """批量删除分组

        通过分组 code，批量删除分组。

        Attributes:
            code_list (list): 分组 code 列表
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/delete-groups-batch",
            json={
                "codeList": code_list,
            },
        )

    def add_group_members(self, user_ids, code):
        """添加分组成员

        添加分组成员，成员以用户 ID 数组形式传递。

        Attributes:
            user_ids (list): 用户 ID 数组
            code (str): 分组 code
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/add-group-members",
            json={
                "userIds": user_ids,
                "code": code,
            },
        )

    def remove_group_members(self, user_ids, code):
        """批量移除分组成员

        批量移除分组成员，成员以用户 ID 数组形式传递。

        Attributes:
            user_ids (list): 用户 ID 数组
            code (str): 分组 code
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/remove-group-members",
            json={
                "userIds": user_ids,
                "code": code,
            },
        )

    def list_group_members(
        self,
        code,
        page=None,
        limit=None,
        with_custom_data=None,
        with_identities=None,
        with_department_ids=None,
    ):
        """获取分组成员列表

        通过分组 code，获取分组成员列表，支持分页，可以获取自定义数据、identities、部门 ID 列表。

        Attributes:
            code (str): 分组 code
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            withCustomData (bool): 是否获取自定义数据
            withIdentities (bool): 是否获取 identities
            withDepartmentIds (bool): 是否获取部门 ID 列表
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/list-group-members",
            params={
                "code": code,
                "page": page,
                "limit": limit,
                "withCustomData": with_custom_data,
                "withIdentities": with_identities,
                "withDepartmentIds": with_department_ids,
            },
        )

    def get_group_authorized_resources(self, code, namespace=None, resource_type=None):
        """获取分组被授权的资源列表

        通过分组 code，获取分组被授权的资源列表，可以通过资源类型、权限分组 code 筛选。

        Attributes:
            code (str): 分组 code
            namespace (str): 所属权限分组的 code
            resourceType (str): 资源类型
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-group-authorized-resources",
            params={
                "code": code,
                "namespace": namespace,
                "resourceType": resource_type,
            },
        )

    def get_role(self, code, namespace=None):
        """获取角色详情

        通过权限分组内角色 code，获取角色详情。

        Attributes:
            code (str): 权限分组内角色的唯一标识符
            namespace (str): 所属权限分组的 code
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-role",
            params={
                "code": code,
                "namespace": namespace,
            },
        )

    def assign_role(self, targets, code, namespace=None):
        """分配角色

        通过权限分组内角色 code，分配角色，被分配者可以是用户或部门。

        Attributes:
            targets (list): 目标对象
            code (str): 权限分组内角色的唯一标识符
            namespace (str): 所属权限分组的 code
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/assign-role",
            json={
                "targets": targets,
                "code": code,
                "namespace": namespace,
            },
        )

    def revoke_role(self, targets, code, namespace=None):
        """移除分配的角色

        通过权限分组内角色 code，移除分配的角色，被分配者可以是用户或部门。

        Attributes:
            targets (list): 移除角色的目标
            code (str): 权限分组内角色的唯一标识符
            namespace (str): 所属权限分组的 code
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/revoke-role",
            json={
                "targets": targets,
                "code": code,
                "namespace": namespace,
            },
        )

    def get_role_authorized_resources(self, code, namespace=None, resource_type=None):
        """获取角色被授权的资源列表

        通过权限分组内角色 code，获取角色被授权的资源列表。

        Attributes:
            code (str): 权限分组内角色的唯一标识符
            namespace (str): 所属权限分组的 code
            resourceType (str): 资源类型，如 数据、API、按钮、菜单
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-role-authorized-resources",
            params={
                "code": code,
                "namespace": namespace,
                "resourceType": resource_type,
            },
        )

    def list_role_members(
        self,
        code,
        page=None,
        limit=None,
        with_custom_data=None,
        with_identities=None,
        with_department_ids=None,
        namespace=None,
    ):
        """获取角色成员列表

        通过权限分组内内角色 code，获取角色成员列表，支持分页，可以选择或获取自定义数据、identities 等。

        Attributes:
            code (str): 权限分组内角色的唯一标识符
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            withCustomData (bool): 是否获取自定义数据
            withIdentities (bool): 是否获取 identities
            withDepartmentIds (bool): 是否获取部门 ID 列表
            namespace (str): 所属权限分组的 code
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/list-role-members",
            params={
                "page": page,
                "limit": limit,
                "withCustomData": with_custom_data,
                "withIdentities": with_identities,
                "withDepartmentIds": with_department_ids,
                "code": code,
                "namespace": namespace,
            },
        )

    def list_role_departments(self, code, namespace=None, page=None, limit=None):
        """获取角色的部门列表

        通过权限分组内角色 code，获取角色的部门列表，支持分页。

        Attributes:
            code (str): 权限分组内角色的唯一标识符
            namespace (str): 所属权限分组的 code
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/list-role-departments",
            params={
                "code": code,
                "namespace": namespace,
                "page": page,
                "limit": limit,
            },
        )

    def create_role(self, code, namespace=None, description=None):
        """创建角色

        通过权限分组内角色 code，创建角色，可以选择权限分组、角色描述等。

        Attributes:
            code (str): 权限分组内角色的唯一标识符
            namespace (str): 所属权限分组的 code
            description (str): 角色描述
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/create-role",
            json={
                "code": code,
                "namespace": namespace,
                "description": description,
            },
        )

    def list_roles(self, keywords=None, namespace=None, page=None, limit=None):
        """获取角色列表

        获取角色列表，支持分页。

        Attributes:
            keywords (str): 用于根据角色的 code 进行模糊搜索，可选。
            namespace (str): 所属权限分组的 code
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/list-roles",
            params={
                "keywords": keywords,
                "namespace": namespace,
                "page": page,
                "limit": limit,
            },
        )

    def delete_roles_batch(self, code_list, namespace=None):
        """删除角色

        删除角色，可以批量删除。

        Attributes:
            code_list (list): 角色 code 列表
            namespace (str): 所属权限分组的 code
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/delete-roles-batch",
            json={
                "codeList": code_list,
                "namespace": namespace,
            },
        )

    def create_roles_batch(self, list):
        """批量创建角色

        批量创建角色，可以选择权限分组、角色描述等。

        Attributes:
            list (list): 角色列表
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/create-roles-batch",
            json={
                "list": list,
            },
        )

    def update_role(self, new_code, code, namespace=None, description=None):
        """修改角色

        通过权限分组内角色新旧 code，修改角色，可以选择角色描述等。

        Attributes:
            new_code (str): 角色新的权限分组内唯一识别码
            code (str): 权限分组内角色的唯一标识符
            namespace (str): 所属权限分组的 code
            description (str): 角色描述
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/update-role",
            json={
                "newCode": new_code,
                "code": code,
                "namespace": namespace,
                "description": description,
            },
        )

    def list_ext_idp(self, tenant_id=None, app_id=None):
        """获取身份源列表

        获取身份源列表，可以指定 租户 ID 筛选。

        Attributes:
            tenantId (str): 租户 ID
            appId (str): 应用 ID
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/list-ext-idp",
            params={
                "tenantId": tenant_id,
                "appId": app_id,
            },
        )

    def get_ext_idp(self, id, tenant_id=None, app_id=None, type=None):
        """获取身份源详情

        通过 身份源 ID，获取身份源详情，可以指定 租户 ID 筛选。

        Attributes:
            id (str): 身份源 ID
            tenantId (str): 租户 ID
            appId (str): 应用 ID
            type (str): 身份源类型
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-ext-idp",
            params={
                "tenantId": tenant_id,
                "appId": app_id,
                "id": id,
                "type": type,
            },
        )

    def create_ext_idp(self, type, name, tenant_id=None):
        """创建身份源

        创建身份源，可以设置身份源名称、连接类型、租户 ID 等。

        Attributes:
            type (str): 身份源连接类型
            name (str): 身份源名称
            tenant_id (str): 租户 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/create-ext-idp",
            json={
                "type": type,
                "name": name,
                "tenantId": tenant_id,
            },
        )

    def update_ext_idp(self, id, name):
        """更新身份源配置

        更新身份源配置，可以设置身份源 ID 与 名称。

        Attributes:
            id (str): 身份源 ID
            name (str): 名称
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/update-ext-idp",
            json={
                "id": id,
                "name": name,
            },
        )

    def delete_ext_idp(self, id):
        """删除身份源

        通过身份源 ID，删除身份源。

        Attributes:
            id (str): 身份源 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/delete-ext-idp",
            json={
                "id": id,
            },
        )

    def create_ext_idp_conn(
        self,
        fields,
        display_name,
        identifier,
        type,
        ext_idp_id,
        login_only=None,
        logo=None,
    ):
        """在某个已有身份源下创建新连接

        在某个已有身份源下创建新连接，可以设置身份源图标、是否只支持登录等。

        Attributes:
            fields (dict): 连接的自定义配置信息
            display_name (str): 连接在登录页的显示名称
            identifier (str): 身份源连接标识
            type (str): 身份源连接类型
            ext_idp_id (str): 身份源连接 ID
            login_only (bool): 是否只支持登录
            logo (str): 身份源图标
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/create-ext-idp-conn",
            json={
                "fields": fields,
                "displayName": display_name,
                "identifier": identifier,
                "type": type,
                "extIdpId": ext_idp_id,
                "loginOnly": login_only,
                "logo": logo,
            },
        )

    def update_ext_idp_conn(self, fields, display_name, id, logo=None, login_only=None):
        """更新身份源连接

        更新身份源连接，可以设置身份源图标、是否只支持登录等。

        Attributes:
            fields (dict): 身份源连接自定义参数（增量修改）
            display_name (str): 身份源连接显示名称
            id (str): 身份源连接 ID
            logo (str): 身份源连接的图标
            login_only (bool): 是否只支持登录
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/update-ext-idp-conn",
            json={
                "fields": fields,
                "displayName": display_name,
                "id": id,
                "logo": logo,
                "loginOnly": login_only,
            },
        )

    def delete_ext_idp_conn(self, id):
        """删除身份源连接

        通过身份源连接 ID，删除身份源连接。

        Attributes:
            id (str): 身份源连接 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/delete-ext-idp-conn",
            json={
                "id": id,
            },
        )

    def change_ext_idp_conn_state(
        self, app_id, enabled, id, tenant_id=None, app_ids=None
    ):
        """身份源连接开关

        身份源连接开关，可以打开或关闭身份源连接。

        Attributes:
            app_id (str): 应用 ID
            enabled (bool): 是否开启身份源连接
            id (str): 身份源连接 ID
            tenant_id (str): 租户 ID
            app_ids (list): 应用 ID 列表
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/change-ext-idp-conn-state",
            json={
                "appId": app_id,
                "enabled": enabled,
                "id": id,
                "tenantId": tenant_id,
                "appIds": app_ids,
            },
        )

    def change_ext_idp_conn_association_state(self, association, id, tenant_id=None):
        """租户关联身份源

        租户可以关联或取消关联身份源连接。

        Attributes:
            association (bool): 是否关联身份源
            id (str): 身份源连接 ID
            tenant_id (str): 租户 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/change-ext-idp-conn-association-state",
            json={
                "association": association,
                "id": id,
                "tenantId": tenant_id,
            },
        )

    def list_tenant_ext_idp(
        self, tenant_id=None, app_id=None, type=None, page=None, limit=None
    ):
        """租户控制台获取身份源列表

        在租户控制台内获取身份源列表，可以根据 应用 ID 筛选。

        Attributes:
            tenantId (str): 租户 ID
            appId (str): 应用 ID
            type (str): 身份源类型
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/list-tenant-ext-idp",
            params={
                "tenantId": tenant_id,
                "appId": app_id,
                "type": type,
                "page": page,
                "limit": limit,
            },
        )

    def ext_idp_conn_state_by_apps(self, id, tenant_id=None, app_id=None, type=None):
        """身份源下应用的连接详情

        在身份源详情页获取应用的连接情况

        Attributes:
            id (str): 身份源 ID
            tenantId (str): 租户 ID
            appId (str): 应用 ID
            type (str): 身份源类型
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/ext-idp-conn-apps",
            params={
                "tenantId": tenant_id,
                "appId": app_id,
                "id": id,
                "type": type,
            },
        )

    def get_user_base_fields(
        self,
    ):
        """获取用户内置字段列表

        获取用户内置的字段列表

        Attributes:
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-user-base-fields",
        )

    def set_user_base_fields(self, list):
        """修改用户内置字段配置

        修改用户内置字段配置，内置字段不允许修改数据类型、唯一性。

        Attributes:
            list (list): 自定义字段列表
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/set-user-base-fields",
            json={
                "list": list,
            },
        )

    def get_custom_fields(self, target_type):
        """获取自定义字段列表

                通过主体类型，获取用户、部门或角色的自定义字段列表。

                Attributes:
                    targetType (str): 目标对象类型：
        - `USER`: 用户
        - `ROLE`: 角色
        - `GROUP`: 分组
        - `DEPARTMENT`: 部门
            ;该接口暂不支持分组(GROUP)
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-custom-fields",
            params={
                "targetType": target_type,
            },
        )

    def set_custom_fields(self, list):
        """创建/修改自定义字段定义

        创建/修改用户、部门或角色自定义字段定义，如果传入的 key 不存在则创建，存在则更新。

        Attributes:
            list (list): 自定义字段列表
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/set-custom-fields",
            json={
                "list": list,
            },
        )

    def set_custom_data(self, list, target_identifier, target_type, namespace=None):
        """设置自定义字段的值

                给用户、角色或部门设置自定义字段的值，如果存在则更新，不存在则创建。

                Attributes:
                    list (list): 自定义数据列表
                    target_identifier (str): 目标对象的唯一标志符：
        - 如果是用户，为用户的 ID，如 `6343b98b7cfxxx9366e9b7c`
        - 如果是角色，为角色的 code，如 `admin`
        - 如果是分组，为分组的 code，如 `developer`
        - 如果是部门，为部门的 ID，如 `6343bafc019xxxx889206c4c`

                    target_type (str): 目标对象类型：
        - `USER`: 用户
        - `ROLE`: 角色
        - `GROUP`: 分组
        - `DEPARTMENT`: 部门

                    namespace (str): 所属权限分组的 code，当 target_type 为角色的时候需要填写，否则可以忽略
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/set-custom-data",
            json={
                "list": list,
                "targetIdentifier": target_identifier,
                "targetType": target_type,
                "namespace": namespace,
            },
        )

    def get_custom_data(self, target_type, target_identifier, namespace=None):
        """获取用户、分组、角色、组织机构的自定义字段值

                通过筛选条件，获取用户、分组、角色、组织机构的自定义字段值。

                Attributes:
                    targetType (str): 目标对象类型：
        - `USER`: 用户
        - `ROLE`: 角色
        - `GROUP`: 分组
        - `DEPARTMENT`: 部门

                    targetIdentifier (str): 目标对象的唯一标志符：
        - 如果是用户，为用户的 ID，如 `6343b98b7cfxxx9366e9b7c`
        - 如果是角色，为角色的 code，如 `admin`
        - 如果是分组，为分组的 code，如 `developer`
        - 如果是部门，为部门的 ID，如 `6343bafc019xxxx889206c4c`

                    namespace (str): 所属权限分组的 code，当 targetType 为角色的时候需要填写，否则可以忽略
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-custom-data",
            params={
                "targetType": target_type,
                "targetIdentifier": target_identifier,
                "namespace": namespace,
            },
        )

    def create_resource(
        self,
        type,
        code,
        description=None,
        actions=None,
        api_identifier=None,
        namespace=None,
    ):
        """创建资源

        创建资源，可以设置资源的描述、定义的操作类型、URL 标识等。

        Attributes:
            type (str): 资源类型，如数据、API、按钮、菜单
            code (str): 资源唯一标志符
            description (str): 资源描述
            actions (list): 资源定义的操作类型
            api_identifier (str): API 资源的 URL 标识
            namespace (str): 所属权限分组的 code
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/create-resource",
            json={
                "type": type,
                "code": code,
                "description": description,
                "actions": actions,
                "apiIdentifier": api_identifier,
                "namespace": namespace,
            },
        )

    def create_resources_batch(self, list, namespace=None):
        """批量创建资源

        批量创建资源，可以设置资源的描述、定义的操作类型、URL 标识等。

        Attributes:
            list (list): 资源列表
            namespace (str): 所属权限分组的 code
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/create-resources-batch",
            json={
                "list": list,
                "namespace": namespace,
            },
        )

    def get_resource(self, code, namespace=None):
        """获取资源详情

        根据筛选条件，获取资源详情。

        Attributes:
            code (str): 资源唯一标志符
            namespace (str): 所属权限分组的 code
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-resource",
            params={
                "code": code,
                "namespace": namespace,
            },
        )

    def get_resources_batch(self, code_list, namespace=None):
        """批量获取资源详情

        根据筛选条件，批量获取资源详情。

        Attributes:
            codeList (str): 资源 code 列表，批量可以使用逗号分隔
            namespace (str): 所属权限分组的 code
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-resources-batch",
            params={
                "namespace": namespace,
                "codeList": code_list,
            },
        )

    def list_resources(self, namespace=None, type=None, page=None, limit=None):
        """分页获取资源列表

        根据筛选条件，分页获取资源详情列表。

        Attributes:
            namespace (str): 所属权限分组的 code
            type (str): 资源类型
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/list-resources",
            params={
                "namespace": namespace,
                "type": type,
                "page": page,
                "limit": limit,
            },
        )

    def update_resource(
        self,
        code,
        description=None,
        actions=None,
        api_identifier=None,
        namespace=None,
        type=None,
    ):
        """修改资源

        修改资源，可以设置资源的描述、定义的操作类型、URL 标识等。

        Attributes:
            code (str): 资源唯一标志符
            description (str): 资源描述
            actions (list): 资源定义的操作类型
            api_identifier (str): API 资源的 URL 标识
            namespace (str): 所属权限分组的 code
            type (str): 资源类型，如数据、API、按钮、菜单
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/update-resource",
            json={
                "code": code,
                "description": description,
                "actions": actions,
                "apiIdentifier": api_identifier,
                "namespace": namespace,
                "type": type,
            },
        )

    def delete_resource(self, code, namespace=None):
        """删除资源

        通过资源唯一标志符以及所属权限分组，删除资源。

        Attributes:
            code (str): 资源唯一标志符
            namespace (str): 所属权限分组的 code
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/delete-resource",
            json={
                "code": code,
                "namespace": namespace,
            },
        )

    def delete_resources_batch(self, code_list, namespace=None):
        """批量删除资源

        通过资源唯一标志符以及所属权限分组，批量删除资源

        Attributes:
            code_list (list): 资源 code 列表
            namespace (str): 所属权限分组的 code
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/delete-resources-batch",
            json={
                "codeList": code_list,
                "namespace": namespace,
            },
        )

    def associate_tenant_resource(self, app_id, association, code, tenant_id=None):
        """关联/取消关联应用资源到租户

        通过资源唯一标识以及权限分组，关联或取消关联资源到租户

        Attributes:
            app_id (str): 应用 ID
            association (bool): 是否关联应用资源
            code (str): 资源 Code
            tenant_id (str): 租户 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/associate-tenant-resource",
            json={
                "appId": app_id,
                "association": association,
                "code": code,
                "tenantId": tenant_id,
            },
        )

    def create_namespace(self, code, name=None, description=None):
        """创建权限分组

        创建权限分组，可以设置分组名称与描述信息。

        Attributes:
            code (str): 权限分组唯一标志符
            name (str): 权限分组名称
            description (str): 权限分组描述信息
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/create-namespace",
            json={
                "code": code,
                "name": name,
                "description": description,
            },
        )

    def create_namespaces_batch(self, list):
        """批量创建权限分组

        批量创建权限分组，可以分别设置分组名称与描述信息。

        Attributes:
            list (list): 权限分组列表
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/create-namespaces-batch",
            json={
                "list": list,
            },
        )

    def get_namespace(self, code):
        """获取权限分组详情

        通过权限分组唯一标志符，获取权限分组详情。

        Attributes:
            code (str): 权限分组唯一标志符
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-namespace",
            params={
                "code": code,
            },
        )

    def get_namespaces_batch(self, code_list):
        """批量获取权限分组详情

        分别通过权限分组唯一标志符，批量获取权限分组详情。

        Attributes:
            codeList (str): 资源 code 列表，批量可以使用逗号分隔
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-namespaces-batch",
            params={
                "codeList": code_list,
            },
        )

    def update_namespace(self, code, description=None, name=None, new_code=None):
        """修改权限分组信息

        修改权限分组信息，可以修改名称、描述信息以及新的唯一标志符。

        Attributes:
            code (str): 权限分组唯一标志符
            description (str): 权限分组描述信息
            name (str): 权限分组名称
            new_code (str): 权限分组新的唯一标志符
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/update-namespace",
            json={
                "code": code,
                "description": description,
                "name": name,
                "newCode": new_code,
            },
        )

    def delete_namespace(self, code):
        """删除权限分组信息

        通过权限分组唯一标志符，删除权限分组信息。

        Attributes:
            code (str): 权限分组唯一标志符
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/delete-namespace",
            json={
                "code": code,
            },
        )

    def delete_namespaces_batch(self, code_list):
        """批量删除权限分组

        分别通过权限分组唯一标志符，批量删除权限分组。

        Attributes:
            code_list (list): 权限分组 code 列表
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/delete-namespaces-batch",
            json={
                "codeList": code_list,
            },
        )

    def authorize_resources(self, list, namespace=None):
        """授权资源

        将一个/多个资源授权给用户、角色、分组、组织机构等主体，且可以分别指定不同的操作权限。

        Attributes:
            list (list): 授权资源列表
            namespace (str): 所属权限分组的 code
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/authorize-resources",
            json={
                "list": list,
                "namespace": namespace,
            },
        )

    def get_authorized_resources(
        self,
        target_type,
        target_identifier,
        namespace=None,
        resource_type=None,
        resource_list=None,
        with_denied=None,
    ):
        """获取某个主体被授权的资源列表

                根据筛选条件，获取某个主体被授权的资源列表。

                Attributes:
                    targetType (str): 目标对象类型：
        - `USER`: 用户
        - `ROLE`: 角色
        - `GROUP`: 分组
        - `DEPARTMENT`: 部门

                    targetIdentifier (str): 目标对象的唯一标志符：
        - 如果是用户，为用户的 ID，如 `6343b98b7cfxxx9366e9b7c`
        - 如果是角色，为角色的 code，如 `admin`
        - 如果是分组，为分组的 code，如 `developer`
        - 如果是部门，为部门的 ID，如 `6343bafc019xxxx889206c4c`

                    namespace (str): 所属权限分组的 code
                    resourceType (str): 限定资源类型，如数据、API、按钮、菜单
                    resourceList (str): 限定查询的资源列表，如果指定，只会返回所指定的资源列表。
                    withDenied (bool): 是否获取被拒绝的资源
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-authorized-resources",
            params={
                "targetType": target_type,
                "targetIdentifier": target_identifier,
                "namespace": namespace,
                "resourceType": resource_type,
                "resourceList": resource_list,
                "withDenied": with_denied,
            },
        )

    def is_action_allowed(self, action, resource, user_id, namespace=None):
        """判断用户是否对某个资源的某个操作有权限

        判断用户是否对某个资源的某个操作有权限。

        Attributes:
            action (str): 资源对应的操作
            resource (str): 资源标识符
            user_id (str): 用户 ID
            namespace (str): 所属权限分组的 code
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/is-action-allowed",
            json={
                "action": action,
                "resource": resource,
                "userId": user_id,
                "namespace": namespace,
            },
        )

    def get_resource_authorized_targets(
        self, resource, namespace=None, target_type=None, page=None, limit=None
    ):
        """获取资源被授权的主体

                获取资源被授权的主体

                Attributes:
                    resource (str): 资源
                    namespace (str): 权限分组
                    target_type (str): 目标对象类型：
        - `USER`: 用户
        - `ROLE`: 角色
        - `GROUP`: 分组
        - `DEPARTMENT`: 部门

                    page (int): 当前页数，从 1 开始
                    limit (int): 每页数目，最大不能超过 50，默认为 10
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/get-resource-authorized-targets",
            json={
                "resource": resource,
                "namespace": namespace,
                "targetType": target_type,
                "page": page,
                "limit": limit,
            },
        )

    def get_sync_task(self, sync_task_id):
        """获取同步任务详情

        获取同步任务详情

        Attributes:
            syncTaskId (int): 同步任务 ID
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-sync-task",
            params={
                "syncTaskId": sync_task_id,
            },
        )

    def list_sync_tasks(self, page=None, limit=None):
        """获取同步任务列表

        获取同步任务列表

        Attributes:
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/list-sync-tasks",
            params={
                "page": page,
                "limit": limit,
            },
        )

    def create_sync_task(
        self,
        field_mapping,
        sync_task_trigger,
        sync_task_flow,
        client_config,
        sync_task_type,
        sync_task_name,
        organization_code=None,
        provisioning_scope=None,
        timed_scheduler=None,
    ):
        """创建同步任务

                创建同步任务

                Attributes:
                    field_mapping (list): 字段映射配置
                    sync_task_trigger (str): 同步任务触发类型：
        - `manually`: 手动触发执行
        - `timed`: 定时触发
        - `automatic`: 根据事件自动触发

                    sync_task_flow (str): 同步任务数据流向：
        - `upstream`: 作为上游，将数据同步到 Authing
        - `downstream`: 作为下游，将 Authing 数据同步到此系统

                    client_config (dict): 同步任务配置信息
                    sync_task_type (str): 同步任务类型:
        - `lark`: 飞书
        - `lark-international`: 飞书国际版
        - `wechatwork`: 企业微信
        - `dingtalk`: 钉钉
        - `active-directory`: Windows AD
        - `ldap`: LDAP
        - `italent`: 北森
        - `maycur`: 每刻报销
        - `moka`: Moka
        - `fxiaoke`: 纷享销客
        - `xiaoshouyi`: 销售易
        - `kayang`: 嘉扬 HR
        - `scim`: 自定义同步源

                    sync_task_name (str): 同步任务名称
                    organization_code (str): 此同步任务绑定的组织机构。针对上游同步，需执行一次同步任务之后才会绑定组织机构；针对下游同步，创建同步任务的时候就需要设置。
                    provisioning_scope (dict): 同步范围，**只针对下游同步任务有效**。为空表示同步整个组织机构。
                    timed_scheduler (dict): 定时同步时间设置
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/create-sync-task",
            json={
                "fieldMapping": field_mapping,
                "syncTaskTrigger": sync_task_trigger,
                "syncTaskFlow": sync_task_flow,
                "clientConfig": client_config,
                "syncTaskType": sync_task_type,
                "syncTaskName": sync_task_name,
                "organizationCode": organization_code,
                "provisioningScope": provisioning_scope,
                "timedScheduler": timed_scheduler,
            },
        )

    def update_sync_task(
        self,
        sync_task_id,
        sync_task_name=None,
        sync_task_type=None,
        client_config=None,
        sync_task_flow=None,
        sync_task_trigger=None,
        organization_code=None,
        provisioning_scope=None,
        field_mapping=None,
        timed_scheduler=None,
    ):
        """修改同步任务

                修改同步任务

                Attributes:
                    sync_task_id (int): 同步任务 ID
                    sync_task_name (str): 同步任务名称
                    sync_task_type (str): 同步任务类型:
        - `lark`: 飞书
        - `lark-international`: 飞书国际版
        - `wechatwork`: 企业微信
        - `dingtalk`: 钉钉
        - `active-directory`: Windows AD
        - `ldap`: LDAP
        - `italent`: 北森
        - `maycur`: 每刻报销
        - `moka`: Moka
        - `fxiaoke`: 纷享销客
        - `xiaoshouyi`: 销售易
        - `kayang`: 嘉扬 HR
        - `scim`: 自定义同步源

                    client_config (dict): 同步任务配置信息
                    sync_task_flow (str): 同步任务数据流向：
        - `upstream`: 作为上游，将数据同步到 Authing
        - `downstream`: 作为下游，将 Authing 数据同步到此系统

                    sync_task_trigger (str): 同步任务触发类型：
        - `manually`: 手动触发执行
        - `timed`: 定时触发
        - `automatic`: 根据事件自动触发

                    organization_code (str): 此同步任务绑定的组织机构。针对上游同步，需执行一次同步任务之后才会绑定组织机构；针对下游同步，创建同步任务的时候就需要设置。
                    provisioning_scope (dict): 同步范围，**只针对下游同步任务有效**。为空表示同步整个组织机构。
                    field_mapping (list): 字段映射配置
                    timed_scheduler (dict): 定时同步时间设置
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/update-sync-task",
            json={
                "syncTaskId": sync_task_id,
                "syncTaskName": sync_task_name,
                "syncTaskType": sync_task_type,
                "clientConfig": client_config,
                "syncTaskFlow": sync_task_flow,
                "syncTaskTrigger": sync_task_trigger,
                "organizationCode": organization_code,
                "provisioningScope": provisioning_scope,
                "fieldMapping": field_mapping,
                "timedScheduler": timed_scheduler,
            },
        )

    def trigger_sync_task(self, sync_task_id):
        """执行同步任务

        执行同步任务

        Attributes:
            sync_task_id (int): 同步任务 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/trigger-sync-task",
            json={
                "syncTaskId": sync_task_id,
            },
        )

    def get_sync_job(self, sync_job_id):
        """获取同步作业详情

        获取同步作业详情

        Attributes:
            syncJobId (int): 同步作业 ID
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-sync-job",
            params={
                "syncJobId": sync_job_id,
            },
        )

    def list_sync_jobs(self, sync_task_id, page=None, limit=None, sync_trigger=None):
        """获取同步作业详情

                获取同步作业详情

                Attributes:
                    syncTaskId (int): 同步任务 ID
                    page (int): 当前页数，从 1 开始
                    limit (int): 每页数目，最大不能超过 50，默认为 10
                    syncTrigger (str): 同步任务触发类型：
        - `manually`: 手动触发执行
        - `timed`: 定时触发
        - `automatic`: 根据事件自动触发

        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/list-sync-jobs",
            params={
                "syncTaskId": sync_task_id,
                "page": page,
                "limit": limit,
                "syncTrigger": sync_trigger,
            },
        )

    def list_sync_job_logs(
        self,
        sync_job_id,
        page=None,
        limit=None,
        success=None,
        action=None,
        object_type=None,
    ):
        """获取同步作业详情

                获取同步作业详情

                Attributes:
                    syncJobId (int): 同步作业 ID
                    page (int): 当前页数，从 1 开始
                    limit (int): 每页数目，最大不能超过 50，默认为 10
                    success (bool): 根据是否操作成功进行筛选
                    action (str): 根据操作类型进行筛选：
        - `CreateUser`: 创建用户
        - `UpdateUser`: 修改用户信息
        - `DeleteUser`: 删除用户
        - `UpdateUserIdentifier`: 修改用户唯一标志符
        - `ChangeUserDepartment`: 修改用户部门
        - `CreateDepartment`: 创建部门
        - `UpdateDepartment`: 修改部门信息
        - `DeleteDepartment`: 删除部门
        - `MoveDepartment`: 移动部门
        - `UpdateDepartmentLeader`: 同步部门负责人
        - `CreateGroup`: 创建分组
        - `UpdateGroup`: 修改分组
        - `DeleteGroup`: 删除分组
        - `Updateless`: 无更新

                    objectType (str): 操作对象类型:
        - `department`: 部门
        - `user`: 用户

        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/list-sync-job-logs",
            params={
                "syncJobId": sync_job_id,
                "page": page,
                "limit": limit,
                "success": success,
                "action": action,
                "objectType": object_type,
            },
        )

    def list_sync_risk_operations(
        self, sync_task_id, page=None, limit=None, status=None, object_type=None
    ):
        """获取同步风险操作列表

                获取同步风险操作列表

                Attributes:
                    syncTaskId (int): 同步任务 ID
                    page (int): 当前页数，从 1 开始
                    limit (int): 每页数目，最大不能超过 50，默认为 10
                    status (str): 根据执行状态筛选
                    objectType (str): 根据操作对象类型，默认获取所有类型的记录：
        - `department`: 部门
        - `user`: 用户

        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/list-sync-risk-operations",
            params={
                "syncTaskId": sync_task_id,
                "page": page,
                "limit": limit,
                "status": status,
                "objectType": object_type,
            },
        )

    def trigger_sync_risk_operations(self, sync_risk_operation_ids):
        """执行同步风险操作

        执行同步风险操作

        Attributes:
            sync_risk_operation_ids (list): 同步任务风险操作 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/trigger-sync-risk-operations",
            json={
                "syncRiskOperationIds": sync_risk_operation_ids,
            },
        )

    def cancel_sync_risk_operation(self, sync_risk_operation_ids):
        """取消同步风险操作

        取消同步风险操作

        Attributes:
            sync_risk_operation_ids (list): 同步任务风险操作 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/cancel-sync-risk-operation",
            json={
                "syncRiskOperationIds": sync_risk_operation_ids,
            },
        )

    def get_user_action_logs(
        self,
        request_id=None,
        client_ip=None,
        event_type=None,
        user_id=None,
        app_id=None,
        start=None,
        end=None,
        success=None,
        pagination=None,
    ):
        """获取用户行为日志

        可以选择请求 ID、客户端 IP、用户 ID、应用 ID、开始时间戳、请求是否成功、分页参数去获取用户行为日志

        Attributes:
            request_id (str): 请求 ID
            client_ip (str): 客户端 IP
            event_type (str): 事件类型
            user_id (str): 用户 ID
            app_id (str): 应用 ID
            start (int): 开始时间戳
            end (int): 结束时间戳
            success (bool): 请求是否成功
            pagination (dict): 分页
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/get-user-action-logs",
            json={
                "requestId": request_id,
                "clientIp": client_ip,
                "eventType": event_type,
                "userId": user_id,
                "appId": app_id,
                "start": start,
                "end": end,
                "success": success,
                "pagination": pagination,
            },
        )

    def get_admin_audit_logs(
        self,
        request_id=None,
        client_ip=None,
        operation_type=None,
        resource_type=None,
        user_id=None,
        success=None,
        start=None,
        end=None,
        pagination=None,
    ):
        """获取管理员操作日志

        可以选择请求 ID、客户端 IP、操作类型、资源类型、管理员用户 ID、请求是否成功、开始时间戳、结束时间戳、分页来获取管理员操作日志接口

        Attributes:
            request_id (str): 请求 ID
            client_ip (str): 客户端 IP
            operation_type (str): 操作类型
            resource_type (str): 资源类型
            user_id (str): 管理员用户 ID
            success (bool): 请求是否成功
            start (int): 开始时间戳
            end (int): 结束时间戳
            pagination (dict): 分页
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/get-admin-audit-logs",
            json={
                "requestId": request_id,
                "clientIp": client_ip,
                "operationType": operation_type,
                "resourceType": resource_type,
                "userId": user_id,
                "success": success,
                "start": start,
                "end": end,
                "pagination": pagination,
            },
        )

    def get_email_templates(
        self,
    ):
        """获取邮件模版列表

        获取邮件模版列表

        Attributes:
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-email-templates",
        )

    def update_email_template(
        self,
        content,
        sender,
        subject,
        name,
        customize_enabled,
        type,
        expires_in=None,
        redirect_to=None,
        tpl_engine=None,
    ):
        """修改邮件模版

                修改邮件模版

                Attributes:
                    content (str): 邮件内容模版
                    sender (str): 邮件发件人名称
                    subject (str): 邮件主题
                    name (str): 邮件模版名称
                    customize_enabled (bool): 是否启用自定义模版
                    type (str): 模版类型:
        - `WELCOME_EMAIL`: 欢迎邮件
        - `FIRST_CREATED_USER`: 首次创建用户通知
        - `REGISTER_VERIFY_CODE`: 注册验证码
        - `LOGIN_VERIFY_CODE`: 登录验证码
        - `MFA_VERIFY_CODE`: MFA 验证码
        - `INFORMATION_COMPLETION_VERIFY_CODE`: 注册信息补全验证码
        - `FIRST_EMAIL_LOGIN_VERIFY`: 首次邮箱登录验证
        - `CONSOLE_CONDUCTED_VERIFY`: 在控制台发起邮件验证
        - `USER_PASSWORD_UPDATE_REMIND`: 用户到期提醒
        - `ADMIN_RESET_USER_PASSWORD_NOTIFICATION`: 管理员重置用户密码成功通知
        - `USER_PASSWORD_RESET_NOTIFICATION`: 用户密码重置成功通知
        - `RESET_PASSWORD_VERIFY_CODE`: 重置密码验证码
        - `SELF_UNLOCKING_VERIFY_CODE`: 自助解锁验证码
        - `EMAIL_BIND_VERIFY_CODE`: 绑定邮箱验证码
        - `EMAIL_UNBIND_VERIFY_CODE`: 解绑邮箱验证码

                    expires_in (int): 验证码/邮件有效时间，只有验证类邮件才有有效时间。
                    redirect_to (str): 完成邮件验证之后跳转到的地址，只针对 `FIRST_EMAIL_LOGIN_VERIFY` 和 `CONSOLE_CONDUCTED_VERIFY` 类型的模版有效。
                    tpl_engine (str): 模版渲染引擎。Authing 邮件模版目前支持两种渲染引擎：
        - `handlebar`: 详细使用方法请见：[handlebars 官方文档](https://handlebarsjs.com/)
        - `ejs`: 详细使用方法请见：[ejs 官方文档](https://ejs.co/)

        默认将使用 `handlerbar` 作为膜拜渲染引擎。

        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/update-email-template",
            json={
                "content": content,
                "sender": sender,
                "subject": subject,
                "name": name,
                "customizeEnabled": customize_enabled,
                "type": type,
                "expiresIn": expires_in,
                "redirectTo": redirect_to,
                "tplEngine": tpl_engine,
            },
        )

    def preview_email_template(
        self,
        type,
        content=None,
        subject=None,
        sender=None,
        expires_in=None,
        tpl_engine=None,
    ):
        """预览邮件模版

                预览邮件模版

                Attributes:
                    type (str): 模版类型:
        - `WELCOME_EMAIL`: 欢迎邮件
        - `FIRST_CREATED_USER`: 首次创建用户通知
        - `REGISTER_VERIFY_CODE`: 注册验证码
        - `LOGIN_VERIFY_CODE`: 登录验证码
        - `MFA_VERIFY_CODE`: MFA 验证码
        - `INFORMATION_COMPLETION_VERIFY_CODE`: 注册信息补全验证码
        - `FIRST_EMAIL_LOGIN_VERIFY`: 首次邮箱登录验证
        - `CONSOLE_CONDUCTED_VERIFY`: 在控制台发起邮件验证
        - `USER_PASSWORD_UPDATE_REMIND`: 用户到期提醒
        - `ADMIN_RESET_USER_PASSWORD_NOTIFICATION`: 管理员重置用户密码成功通知
        - `USER_PASSWORD_RESET_NOTIFICATION`: 用户密码重置成功通知
        - `RESET_PASSWORD_VERIFY_CODE`: 重置密码验证码
        - `SELF_UNLOCKING_VERIFY_CODE`: 自助解锁验证码
        - `EMAIL_BIND_VERIFY_CODE`: 绑定邮箱验证码
        - `EMAIL_UNBIND_VERIFY_CODE`: 解绑邮箱验证码

                    content (str): 邮件内容模版，可选，如果不传默认使用用户池配置的邮件模版进行渲染。
                    subject (str): 邮件主题，可选，如果不传默认使用用户池配置的邮件模版进行渲染。
                    sender (str): 邮件发件人名称，可选，如果不传默认使用用户池配置的邮件模版进行渲染。
                    expires_in (int): 验证码/邮件有效时间，只有验证类邮件才有有效时间。可选，如果不传默认使用用户池配置的邮件模版进行渲染。
                    tpl_engine (str): 模版渲染引擎。Authing 邮件模版目前支持两种渲染引擎：
        - `handlebar`: 详细使用方法请见：[handlebars 官方文档](https://handlebarsjs.com/)
        - `ejs`: 详细使用方法请见：[ejs 官方文档](https://ejs.co/)

        默认将使用 `handlerbar` 作为膜拜渲染引擎。

        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/preview-email-template",
            json={
                "type": type,
                "content": content,
                "subject": subject,
                "sender": sender,
                "expiresIn": expires_in,
                "tplEngine": tpl_engine,
            },
        )

    def get_email_provider(
        self,
    ):
        """获取第三方邮件服务配置

        获取第三方邮件服务配置

        Attributes:
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-email-provider",
        )

    def config_email_provider(
        self,
        type,
        enabled,
        smtp_config=None,
        send_grid_config=None,
        ali_exmail_config=None,
        tencent_exmail_config=None,
    ):
        """配置第三方邮件服务

                配置第三方邮件服务

                Attributes:
                    type (str): 第三方邮件服务商类型:
        - `custom`: 自定义 SMTP 邮件服务
        - `ali`: [阿里企业邮箱](https://www.ali-exmail.cn/Land/)
        - `qq`: [腾讯企业邮箱](https://work.weixin.qq.com/mail/)
        - `sendgrid`: [SendGrid 邮件服务](https://sendgrid.com/)

                    enabled (bool): 是否启用，如果不启用，将默认使用 Authing 内置的邮件服务
                    smtp_config (dict): SMTP 邮件服务配置
                    send_grid_config (dict): SendGrid 邮件服务配置
                    ali_exmail_config (dict): 阿里企业邮件服务配置
                    tencent_exmail_config (dict): 腾讯企业邮件服务配置
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/config-email-provider",
            json={
                "type": type,
                "enabled": enabled,
                "smtpConfig": smtp_config,
                "sendGridConfig": send_grid_config,
                "aliExmailConfig": ali_exmail_config,
                "tencentExmailConfig": tencent_exmail_config,
            },
        )

    def get_application(self, app_id):
        """获取应用详情

        通过应用 ID，获取应用详情。

        Attributes:
            appId (str): 应用 ID
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-application",
            params={
                "appId": app_id,
            },
        )

    def list_applications(
        self,
        page=None,
        limit=None,
        is_integrate_app=None,
        is_self_built_app=None,
        sso_enabled=None,
        keywords=None,
    ):
        """获取应用列表

        获取应用列表

        Attributes:
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            isIntegrateApp (bool): 是否为集成应用
            isSelfBuiltApp (bool): 是否为自建应用
            ssoEnabled (bool): 是否开启单点登录
            keywords (str): 模糊搜索字符串
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/list-applications",
            params={
                "page": page,
                "limit": limit,
                "isIntegrateApp": is_integrate_app,
                "isSelfBuiltApp": is_self_built_app,
                "ssoEnabled": sso_enabled,
                "keywords": keywords,
            },
        )

    def get_application_simple_info(self, app_id):
        """获取应用简单信息

        通过应用 ID，获取应用简单信息。

        Attributes:
            appId (str): 应用 ID
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-application-simple-info",
            params={
                "appId": app_id,
            },
        )

    def list_application_simple_info(
        self,
        page=None,
        limit=None,
        is_integrate_app=None,
        is_self_built_app=None,
        sso_enabled=None,
        keywords=None,
    ):
        """获取应用简单信息列表

        获取应用简单信息列表

        Attributes:
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            isIntegrateApp (bool): 是否为集成应用
            isSelfBuiltApp (bool): 是否为自建应用
            ssoEnabled (bool): 是否开启单点登录
            keywords (str): 模糊搜索字符串
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/list-application-simple-info",
            params={
                "page": page,
                "limit": limit,
                "isIntegrateApp": is_integrate_app,
                "isSelfBuiltApp": is_self_built_app,
                "ssoEnabled": sso_enabled,
                "keywords": keywords,
            },
        )

    def create_application(
        self,
        app_name,
        template=None,
        template_data=None,
        app_identifier=None,
        app_logo=None,
        app_description=None,
        app_type=None,
        default_protocol=None,
        redirect_uris=None,
        logout_redirect_uris=None,
        init_login_uri=None,
        sso_enabled=None,
        oidc_config=None,
        saml_provider_enabled=None,
        saml_config=None,
        oauth_provider_enabled=None,
        oauth_config=None,
        cas_provider_enabled=None,
        cas_config=None,
        login_config=None,
        register_config=None,
        branding_config=None,
    ):
        """创建应用

        创建应用

        Attributes:
            app_name (str): 应用名称
            template (str): 集成应用模版类型，**集成应用必填**。集成应用只需要填 `template` 和 `templateData` 两个字段，其他的字段将被忽略。
            template_data (str): 集成应用配置信息，**集成应用必填**。
            app_identifier (str): 应用唯一标志，**自建应用必填**。
            app_logo (str): 应用 Logo 链接
            app_description (str): 应用描述信息
            app_type (str): 应用类型
            default_protocol (str): 默认应用协议类型
            redirect_uris (list): 应用登录回调地址
            logout_redirect_uris (list): 应用退出登录回调地址
            init_login_uri (str): 发起登录地址：在 Authing 应用详情点击「体验登录」或在应用面板点击该应用图标时，会跳转到此 URL，默认为 Authing 登录页。
            sso_enabled (bool): 是否开启 SSO 单点登录
            oidc_config (dict): OIDC 协议配置
            saml_provider_enabled (bool): 是否开启 SAML 身份提供商
            saml_config (dict): SAML 协议配置
            oauth_provider_enabled (bool): 是否开启 OAuth 身份提供商
            oauth_config (dict): OAuth2.0 协议配置。【重要提示】不再推荐使用 OAuth2.0，建议切换到 OIDC。
            cas_provider_enabled (bool): 是否开启 CAS 身份提供商
            cas_config (dict): CAS 协议配置
            login_config (dict): 登录配置
            register_config (dict): 注册配置
            branding_config (dict): 品牌化配置
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/create-application",
            json={
                "appName": app_name,
                "template": template,
                "templateData": template_data,
                "appIdentifier": app_identifier,
                "appLogo": app_logo,
                "appDescription": app_description,
                "appType": app_type,
                "defaultProtocol": default_protocol,
                "redirectUris": redirect_uris,
                "logoutRedirectUris": logout_redirect_uris,
                "initLoginUri": init_login_uri,
                "ssoEnabled": sso_enabled,
                "oidcConfig": oidc_config,
                "samlProviderEnabled": saml_provider_enabled,
                "samlConfig": saml_config,
                "oauthProviderEnabled": oauth_provider_enabled,
                "oauthConfig": oauth_config,
                "casProviderEnabled": cas_provider_enabled,
                "casConfig": cas_config,
                "loginConfig": login_config,
                "registerConfig": register_config,
                "brandingConfig": branding_config,
            },
        )

    def delete_application(self, app_id):
        """删除应用

        通过应用 ID，删除应用。

        Attributes:
            app_id (str): 应用 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/delete-application",
            json={
                "appId": app_id,
            },
        )

    def get_application_secret(self, app_id):
        """获取应用密钥

        获取应用密钥

        Attributes:
            appId (str): 应用 ID
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-application-secret",
            params={
                "appId": app_id,
            },
        )

    def refresh_application_secret(self, app_id):
        """刷新应用密钥

        刷新应用密钥

        Attributes:
            app_id (str): 应用 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/refresh-application-secret",
            json={
                "appId": app_id,
            },
        )

    def list_application_active_users(self, app_id, options=None):
        """获取应用当前登录用户

        获取应用当前处于登录状态的用户

        Attributes:
            app_id (str): 应用 ID
            options (dict): 可选项
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/list-application-active-users",
            json={
                "appId": app_id,
                "options": options,
            },
        )

    def get_application_permission_strategy(self, app_id):
        """获取应用默认访问授权策略

        获取应用默认访问授权策略

        Attributes:
            appId (str): 应用 ID
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-application-permission-strategy",
            params={
                "appId": app_id,
            },
        )

    def update_application_permission_strategy(self, permission_strategy, app_id):
        """更新应用默认访问授权策略

        更新应用默认访问授权策略

        Attributes:
            permission_strategy (str): 应用访问授权策略
            app_id (str): 应用 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/update-application-permission-strategy",
            json={
                "permissionStrategy": permission_strategy,
                "appId": app_id,
            },
        )

    def authorize_application_access(self, list, app_id):
        """授权应用访问权限

        给用户、分组、组织或角色授权应用访问权限，如果用户、分组、组织或角色不存在，则跳过，进行下一步授权，不返回报错

        Attributes:
            list (list): 授权主体列表，最多 10 条
            app_id (str): 应用 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/authorize-application-access",
            json={
                "list": list,
                "appId": app_id,
            },
        )

    def revoke_application_access(self, list, app_id):
        """删除应用访问授权记录

        取消给用户、分组、组织或角色的应用访问权限授权,如果传入数据不存在，则返回数据不报错处理。

        Attributes:
            list (list): 授权主体列表，最多 10 条
            app_id (str): 应用 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/revoke-application-access",
            json={
                "list": list,
                "appId": app_id,
            },
        )

    def check_domain_available(self, domain):
        """检测域名是否可用

        检测域名是否可用于创建新应用或更新应用域名

        Attributes:
            domain (str): 域名
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/check-domain-available",
            json={
                "domain": domain,
            },
        )

    def get_security_settings(
        self,
    ):
        """获取安全配置

        无需传参获取安全配置

        Attributes:
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-security-settings",
        )

    def update_security_settings(
        self,
        allowed_origins=None,
        authing_token_expires_in=None,
        verify_code_length=None,
        verify_code_max_attempts=None,
        change_email_strategy=None,
        change_phone_strategy=None,
        cookie_settings=None,
        register_disabled=None,
        register_anomaly_detection=None,
        complete_password_after_pass_code_login=None,
        login_anomaly_detection=None,
        login_require_email_verified=None,
        self_unlock_account=None,
        enable_login_account_switch=None,
        qrcode_login_strategy=None,
    ):
        """修改安全配置

        可选安全域、Authing Token 有效时间（秒）、验证码长度、验证码尝试次数、用户修改邮箱的安全策略、用户修改手机号的安全策略、Cookie 过期时间设置、是否禁止用户注册、频繁注册检测配置、验证码注册后是否要求用户设置密码、未验证的邮箱登录时是否禁止登录并发送认证邮件、用户自助解锁配置、Authing 登录页面是否开启登录账号选择、APP 扫码登录安全配置进行修改安全配置

        Attributes:
            allowed_origins (list): 安全域（CORS）
            authing_token_expires_in (int): Authing Token 有效时间（秒）
            verify_code_length (int): 验证码长度。包含短信验证码、邮件验证码和图形验证码。
            verify_code_max_attempts (int): 验证码尝试次数。在一个验证码有效周期内（默认为 60 s），用户输入验证码错误次数超过此阈值之后，将会导致当前验证码失效，需要重新发送。
            change_email_strategy (dict): 用户修改邮箱的安全策略
            change_phone_strategy (dict): 用户修改手机号的安全策略
            cookie_settings (dict): Cookie 过期时间设置
            register_disabled (bool): 是否禁止用户注册，开启之后，用户将无法自主注册，只能管理员为其创建账号。针对 B2B 和 B2E 类型用户池，默认开启。
            register_anomaly_detection (dict): 频繁注册检测配置
            complete_password_after_pass_code_login (bool): 验证码注册后是否要求用户设置密码（仅针对 Authing 登录页和 Guard 有效，不针对 API 调用）。
            login_anomaly_detection (dict): 登录防暴破配置
            login_require_email_verified (bool): 当使用邮箱登录时，未验证的邮箱登录时是否禁止登录并发送认证邮件。当用户收到邮件并完成验证之后，才能进行登录。
            self_unlock_account (dict): 用户自助解锁配置。注：只有绑定了手机号/邮箱的用户才可以自助解锁
            enable_login_account_switch (bool): Authing 登录页面是否开启登录账号选择
            qrcode_login_strategy (dict): APP 扫码登录安全配置
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/update-security-settings",
            json={
                "allowedOrigins": allowed_origins,
                "authingTokenExpiresIn": authing_token_expires_in,
                "verifyCodeLength": verify_code_length,
                "verifyCodeMaxAttempts": verify_code_max_attempts,
                "changeEmailStrategy": change_email_strategy,
                "changePhoneStrategy": change_phone_strategy,
                "cookieSettings": cookie_settings,
                "registerDisabled": register_disabled,
                "registerAnomalyDetection": register_anomaly_detection,
                "completePasswordAfterPassCodeLogin": complete_password_after_pass_code_login,
                "loginAnomalyDetection": login_anomaly_detection,
                "loginRequireEmailVerified": login_require_email_verified,
                "selfUnlockAccount": self_unlock_account,
                "enableLoginAccountSwitch": enable_login_account_switch,
                "qrcodeLoginStrategy": qrcode_login_strategy,
            },
        )

    def get_global_mfa_settings(
        self,
    ):
        """获取全局多因素认证配置

        无需传参获取全局多因素认证配置

        Attributes:
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-global-mfa-settings",
        )

    def update_global_mfa_settings(self, enabled_factors):
        """修改全局多因素认证配置

        传入 MFA 认证因素列表进行开启,

        Attributes:
            enabled_factors (list): 开启的 MFA 认证因素列表
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/update-global-mfa-settings",
            json={
                "enabledFactors": enabled_factors,
            },
        )

    def get_current_package_info(
        self,
    ):
        """获取套餐详情

        获取当前用户池套餐详情。

        Attributes:
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-current-package-info",
        )

    def get_usage_info(
        self,
    ):
        """获取用量详情

        获取当前用户池用量详情。

        Attributes:
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-usage-info",
        )

    def get_mau_period_usage_history(self, start_time, end_time):
        """获取 MAU 使用记录

        获取当前用户池 MAU 使用记录

        Attributes:
            startTime (str): 起始时间（年月日）
            endTime (str): 截止时间（年月日）
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-mau-period-usage-history",
            params={
                "startTime": start_time,
                "endTime": end_time,
            },
        )

    def get_all_rights_item(
        self,
    ):
        """获取所有权益

        获取当前用户池所有权益

        Attributes:
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-all-rights-items",
        )

    def get_orders(self, page=None, limit=None):
        """获取订单列表

        获取当前用户池订单列表

        Attributes:
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-orders",
            params={
                "page": page,
                "limit": limit,
            },
        )

    def get_order_detail(self, order_no):
        """获取订单详情

        获取当前用户池订单详情

        Attributes:
            orderNo (str): 订单号
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-order-detail",
            params={
                "orderNo": order_no,
            },
        )

    def get_order_pay_detail(self, order_no):
        """获取订单支付明细

        获取当前用户池订单支付明细

        Attributes:
            orderNo (str): 订单号
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-order-pay-detail",
            params={
                "orderNo": order_no,
            },
        )

    def create_pipeline_function(
        self,
        source_code,
        scene,
        func_name,
        func_description=None,
        is_asynchronous=None,
        timeout=None,
        terminate_on_timeout=None,
        enabled=None,
    ):
        """创建 Pipeline 函数

                创建 Pipeline 函数

                Attributes:
                    source_code (str): 函数源代码
                    scene (str): 函数的触发场景：
        - `PRE_REGISTER`: 注册前
        - `POST_REGISTER`: 注册后
        - `PRE_AUTHENTICATION`: 认证前
        - `POST_AUTHENTICATION`: 认证后
        - `PRE_OIDC_ID_TOKEN_ISSUED`: OIDC ID Token 签发前
        - `PRE_OIDC_ACCESS_TOKEN_ISSUED`: OIDC Access Token 签发前
        - `PRE_COMPLETE_USER_INFO`: 补全用户信息前

                    func_name (str): 函数名称
                    func_description (str): 函数描述
                    is_asynchronous (bool): 是否异步执行。设置为异步执行的函数不会阻塞整个流程的执行，适用于异步通知的场景，比如飞书群通知、钉钉群通知等。
                    timeout (int): 函数运行超时时间，要求必须为整数，最短为 1 秒，最长为 60 秒，默认为 3 秒。
                    terminate_on_timeout (bool): 如果函数运行超时，是否终止整个流程，默认为否。
                    enabled (bool): 是否启用此 Pipeline
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/create-pipeline-function",
            json={
                "sourceCode": source_code,
                "scene": scene,
                "funcName": func_name,
                "funcDescription": func_description,
                "isAsynchronous": is_asynchronous,
                "timeout": timeout,
                "terminateOnTimeout": terminate_on_timeout,
                "enabled": enabled,
            },
        )

    def get_pipeline_function(self, func_id):
        """获取 Pipeline 函数详情

        获取 Pipeline 函数详情

        Attributes:
            funcId (str): Pipeline 函数 ID
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-pipeline-function",
            params={
                "funcId": func_id,
            },
        )

    def reupload_pipeline_function(self, func_id):
        """重新上传 Pipeline 函数

        当 Pipeline 函数上传失败时，重新上传 Pipeline 函数

        Attributes:
            func_id (str): Pipeline 函数 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/reupload-pipeline-function",
            json={
                "funcId": func_id,
            },
        )

    def update_pipeline_function(
        self,
        func_id,
        func_name=None,
        func_description=None,
        source_code=None,
        is_asynchronous=None,
        timeout=None,
        terminate_on_timeout=None,
        enabled=None,
    ):
        """修改 Pipeline 函数

        修改 Pipeline 函数

        Attributes:
            func_id (str): Pipeline 函数 ID
            func_name (str): 函数名称
            func_description (str): 函数描述
            source_code (str): 函数源代码。如果修改之后，函数会重新上传。
            is_asynchronous (bool): 是否异步执行。设置为异步执行的函数不会阻塞整个流程的执行，适用于异步通知的场景，比如飞书群通知、钉钉群通知等。
            timeout (int): 函数运行超时时间，最短为 1 秒，最长为 60 秒，默认为 3 秒。
            terminate_on_timeout (bool): 如果函数运行超时，是否终止整个流程，默认为否。
            enabled (bool): 是否启用此 Pipeline
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/update-pipeline-function",
            json={
                "funcId": func_id,
                "funcName": func_name,
                "funcDescription": func_description,
                "sourceCode": source_code,
                "isAsynchronous": is_asynchronous,
                "timeout": timeout,
                "terminateOnTimeout": terminate_on_timeout,
                "enabled": enabled,
            },
        )

    def update_pipeline_order(self, order, scene):
        """修改 Pipeline 函数顺序

                修改 Pipeline 函数顺序

                Attributes:
                    order (list): 新的排序方式，按照函数 ID 的先后顺序进行排列。
                    scene (str): 函数的触发场景：
        - `PRE_REGISTER`: 注册前
        - `POST_REGISTER`: 注册后
        - `PRE_AUTHENTICATION`: 认证前
        - `POST_AUTHENTICATION`: 认证后
        - `PRE_OIDC_ID_TOKEN_ISSUED`: OIDC ID Token 签发前
        - `PRE_OIDC_ACCESS_TOKEN_ISSUED`: OIDC Access Token 签发前
        - `PRE_COMPLETE_USER_INFO`: 补全用户信息前

        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/update-pipeline-order",
            json={
                "order": order,
                "scene": scene,
            },
        )

    def delete_pipeline_function(self, func_id):
        """删除 Pipeline 函数

        删除 Pipeline 函数

        Attributes:
            func_id (str): Pipeline 函数 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/delete-pipeline-function",
            json={
                "funcId": func_id,
            },
        )

    def list_pipeline_functions(self, scene):
        """获取 Pipeline 函数列表

                获取 Pipeline 函数列表

                Attributes:
                    scene (str): 通过函数的触发场景进行筛选（可选，默认返回所有）：
        - `PRE_REGISTER`: 注册前
        - `POST_REGISTER`: 注册后
        - `PRE_AUTHENTICATION`: 认证前
        - `POST_AUTHENTICATION`: 认证后
        - `PRE_OIDC_ID_TOKEN_ISSUED`: OIDC ID Token 签发前
        - `PRE_OIDC_ACCESS_TOKEN_ISSUED`: OIDC Access Token 签发前
        - `PRE_COMPLETE_USER_INFO`: 补全用户信息前

        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/list-pipeline-functions",
            params={
                "scene": scene,
            },
        )

    def get_pipeline_logs(self, func_id, page=None, limit=None):
        """获取 Pipeline 日志

        获取 Pipeline

        Attributes:
            funcId (str): Pipeline 函数 ID
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-pipeline-logs",
            params={
                "funcId": func_id,
                "page": page,
                "limit": limit,
            },
        )

    def create_webhook(
        self, content_type, events, url, name, enabled=None, secret=None
    ):
        """创建 Webhook

        你需要指定 Webhoook 名称、Webhook 回调地址、请求数据格式、用户真实名称来创建 Webhook。还可选是否启用、请求密钥进行创建

        Attributes:
            content_type (str): 请求数据格式
            events (list): 用户真实名称，不具备唯一性。 示例值: 张三
            url (str): Webhook 回调地址
            name (str): Webhook 名称
            enabled (bool): 是否启用
            secret (str): 请求密钥
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/create-webhook",
            json={
                "contentType": content_type,
                "events": events,
                "url": url,
                "name": name,
                "enabled": enabled,
                "secret": secret,
            },
        )

    def list_webhooks(self, page=None, limit=None):
        """获取 Webhook 列表

        获取 Webhook 列表，可选页数、分页大小来获取

        Attributes:
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/list-webhooks",
            params={
                "page": page,
                "limit": limit,
            },
        )

    def update_webhook(
        self,
        webhook_id,
        name=None,
        url=None,
        events=None,
        content_type=None,
        enabled=None,
        secret=None,
    ):
        """修改 Webhook 配置

        需要指定 webhookId，可选 Webhoook 名称、Webhook 回调地址、请求数据格式、用户真实名称、是否启用、请求密钥参数进行修改 webhook

        Attributes:
            webhook_id (str): Webhook ID
            name (str): Webhook 名称
            url (str): Webhook 回调地址
            events (list): 用户真实名称，不具备唯一性。 示例值: 张三
            content_type (str): 请求数据格式
            enabled (bool): 是否启用
            secret (str): 请求密钥
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/update-webhook",
            json={
                "webhookId": webhook_id,
                "name": name,
                "url": url,
                "events": events,
                "contentType": content_type,
                "enabled": enabled,
                "secret": secret,
            },
        )

    def delete_webhook(self, webhook_ids):
        """删除 Webhook

        通过指定多个 webhookId,以数组的形式进行 webhook 的删除,如果 webhookId 不存在,不提示报错

        Attributes:
            webhook_ids (list): webhookId 数组
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/delete-webhook",
            json={
                "webhookIds": webhook_ids,
            },
        )

    def get_webhook_logs(self, webhook_id, page=None, limit=None):
        """获取 Webhook 日志

        通过指定 webhookId，可选 page 和 limit 来获取 webhook 日志,如果 webhookId 不存在,不返回报错信息

        Attributes:
            webhook_id (str): Webhook ID
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/get-webhook-logs",
            json={
                "webhookId": webhook_id,
                "page": page,
                "limit": limit,
            },
        )

    def trigger_webhook(self, webhook_id, request_headers=None, request_body=None):
        """手动触发 Webhook 执行

        通过指定 webhookId，可选请求头和请求体进行手动触发 webhook 执行

        Attributes:
            webhook_id (str): Webhook ID
            request_headers (dict): 请求头
            request_body (dict): 请求体
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/trigger-webhook",
            json={
                "webhookId": webhook_id,
                "requestHeaders": request_headers,
                "requestBody": request_body,
            },
        )

    def get_webhook(self, webhook_id):
        """获取 Webhook 详情

        根据指定的 webhookId 获取 webhook 详情

        Attributes:
            webhookId (str): Webhook ID
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-webhook",
            params={
                "webhookId": webhook_id,
            },
        )

    def get_webhook_event_list(
        self,
    ):
        """获取 Webhook 事件列表

        返回事件列表和分类列表

        Attributes:
        """
        return self.http_client.request(
            method="GET",
            url="/api/v3/get-webhook-event-list",
        )
