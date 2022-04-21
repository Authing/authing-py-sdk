# coding: utf-8

from .ManagementClientOptions import ManagementClientOptions
from .HttpClient import HttpClient


class ManagementClient(object):
    """Authing Management Client"""

    def __init__(self, options):
        # type:(ManagementClientOptions) -> ManagementClient
        self.options = options
        self.http_client = HttpClient(self.options)

    def get_management_token(self, access_key_secret, access_key_id):
        """获取 Management API Token

        获取 Management API Token

        Attributes:
            access_key_secret (str): AccessKey Secret: 如果是以用户池全局 AK/SK 初始化，为用户池密钥；如果是以协作管理员的 AK/SK 初始化，为协作管理员的 SK。
            access_key_id (str): AccessKey ID: 如果是以用户池全局 AK/SK 初始化，为用户池 ID；如果是以协作管理员的 AK/SK 初始化，为协作管理员的 AccessKey ID。
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/get-management-token",
            json={
                "accessKeySecret": access_key_secret,
                "accessKeyId": access_key_id,
            },
        )

    def get_user(
        self,
        user_id=None,
        phone=None,
        email=None,
        username=None,
        external_id=None,
        options=None,
    ):
        """获取用户信息

        获取用户信息

        Attributes:
            user_id (str): 用户 ID
            phone (str): 手机号
            email (str): 邮箱
            username (str): 用户名
            external_id (str): 原系统 ID
            options (dict): 可选参数
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/get-user",
            json={
                "userId": user_id,
                "phone": phone,
                "email": email,
                "username": username,
                "externalId": external_id,
                "options": options,
            },
        )

    def get_user_batch(self, user_ids, options=None):
        """批量获取用户信息

        根据用户 id 批量获取用户信息

        Attributes:
            user_ids (list): 用户 ID 数组
            options (dict): 可选参数
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/get-user-batch",
            json={
                "userIds": user_ids,
                "options": options,
            },
        )

    def list_users(self, options=None):
        """获取用户列表

        获取用户列表接口，支持分页

        Attributes:
            options (dict): 可选参数
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/list-users",
            json={
                "options": options,
            },
        )

    def get_user_identities(self, user_id):
        """获取用户的外部身份源

        获取用户的外部身份源

        Attributes:
            user_id (str): 用户 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/get-user-identities",
            json={
                "userId": user_id,
            },
        )

    def get_user_roles(self, user_id, namespace=None):
        """获取用户角色列表

        获取用户角色列表

        Attributes:
            user_id (str): 用户 ID
            namespace (str): 所属权限分组的 code
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/get-user-roles",
            json={
                "userId": user_id,
                "namespace": namespace,
            },
        )

    def get_principal_authentication_info(self, user_id):
        """获取用户实名认证信息

        获取用户实名认证信息

        Attributes:
            user_id (str): 用户 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/get-user-principal-authentication-info",
            json={
                "userId": user_id,
            },
        )

    def reset_principal_authentication_info(self, user_id):
        """删除用户实名认证信息

        删除用户实名认证信息

        Attributes:
            user_id (str): 用户 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/reset-user-principal-authentication-info",
            json={
                "userId": user_id,
            },
        )

    def get_user_departments(self, user_id):
        """获取用户部门列表

        获取用户部门列表

        Attributes:
            user_id (str): 用户 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/get-user-departments",
            json={
                "userId": user_id,
            },
        )

    def set_user_department(self, departments, user_id):
        """设置用户所在部门

        设置用户所在部门

        Attributes:
            departments (list): 部门信息
            user_id (str): 用户 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/set-user-departments",
            json={
                "departments": departments,
                "userId": user_id,
            },
        )

    def get_user_groups(self, user_id):
        """获取用户分组列表

        获取用户分组列表

        Attributes:
            user_id (str): 用户 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/get-user-groups",
            json={
                "userId": user_id,
            },
        )

    def delete_user_batch(self, user_ids):
        """删除用户

        删除用户（支持批量删除）

        Attributes:
            user_ids (list): 用户 ID 列表
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/delete-users-batch",
            json={
                "userIds": user_ids,
            },
        )

    def get_user_mfa_info(self, user_id):
        """获取用户 MFA 绑定信息

        获取用户 MFA 绑定信息

        Attributes:
            user_id (str): 用户 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/get-user-mfa-info",
            json={
                "userId": user_id,
            },
        )

    def list_archived_users(self, options=None):
        """获取已归档的用户列表

        获取已归档的用户列表

        Attributes:
            options (dict): 可选参数
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/list-archived-users",
            json={
                "options": options,
            },
        )

    def kick_users(self, app_ids, user_id):
        """强制下线用户

        强制下线用户

        Attributes:
            app_ids (list): APP ID 集合
            user_id (str): 用户 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/kick-users",
            json={
                "appIds": app_ids,
                "userId": user_id,
            },
        )

    def is_user_exists(self, username=None, email=None, phone=None, external_id=None):
        """判断用户是否存在

        根据条件判断用户是否存在

        Attributes:
            username (str): 用户名，用户池内唯一
            email (str): 邮箱
            phone (str): 手机号
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

    def create_user(
        self,
        status=None,
        email=None,
        phone=None,
        phone_country_code=None,
        username=None,
        name=None,
        nickname=None,
        photo=None,
        gender=None,
        email_verified=None,
        phone_verified=None,
        external_id=None,
        department_ids=None,
        custom_data=None,
        password=None,
        tenant_ids=None,
        identities=None,
        options=None,
    ):
        """创建用户

        创建用户，邮箱、手机号、用户名必须包含其中一个

        Attributes:
            status (str): 账户当前状态
            email (str): 邮箱
            phone (str): 手机号
            phone_country_code (str): 手机区号
            username (str): 用户名，用户池内唯一
            name (str): 用户真实名称，不具备唯一性
            nickname (str): 昵称
            photo (str): 头像链接
            gender (str): 性别
            email_verified (bool): 邮箱是否验证
            phone_verified (bool): 手机号是否验证
            external_id (str): 第三方外部 ID
            department_ids (list): 用户所属部门 ID 列表
            custom_data (dict): 自定义数据，传入的对象中的 key 必须先在用户池定义相关自定义字段
            password (str): 密码。必须通过加密方式进行加密。
            tenant_ids (list): 租户 ID
            identities (list): 第三方身份源（建议调用绑定接口进行绑定）
            options (dict): 附加选项
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
                "name": name,
                "nickname": nickname,
                "photo": photo,
                "gender": gender,
                "emailVerified": email_verified,
                "phoneVerified": phone_verified,
                "externalId": external_id,
                "departmentIds": department_ids,
                "customData": custom_data,
                "password": password,
                "tenantIds": tenant_ids,
                "identities": identities,
                "options": options,
            },
        )

    def create_user_batch(self, list, options=None):
        """批量创建用户

        批量创建用户

        Attributes:
            list (list): 批量用户
            options (dict): 附加选项
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
        gender=None,
        username=None,
        email=None,
        phone=None,
        password=None,
        custom_data=None,
    ):
        """修改用户资料

        修改用户资料

        Attributes:
            user_id (str): 用户 ID
            phone_country_code (str): 手机区号
            name (str): 用户真实名称，不具备唯一性
            nickname (str): 昵称
            photo (str): 头像链接
            external_id (str): 第三方外部 ID
            status (str): 账户当前状态
            email_verified (bool): 邮箱是否验证
            phone_verified (bool): 手机号是否验证
            gender (str): 性别
            username (str): 用户名，用户池内唯一
            email (str): 邮箱
            phone (str): 手机号
            password (str): 密码。必须通过加密方式进行加密。
            custom_data (dict): 自定义数据，传入的对象中的 key 必须先在用户池定义相关自定义字段
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
                "gender": gender,
                "username": username,
                "email": email,
                "phone": phone,
                "password": password,
                "customData": custom_data,
            },
        )

    def get_user_accessible_apps(self, user_id):
        """获取用户可访问应用

        获取用户可访问应用

        Attributes:
            user_id (str): 用户 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/get-user-accessible-apps",
            json={
                "userId": user_id,
            },
        )

    def get_user_authorized_apps(self, user_id):
        """获取用户授权的应用

        获取用户授权的应用

        Attributes:
            user_id (str): 用户 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/get-user-authorized-apps",
            json={
                "userId": user_id,
            },
        )

    def has_any_role(self, has_any_role):
        """判断用户是否有某个角色

        判断用户是否有某个角色，支持同时传入多个角色进行判断

        Attributes:
            has_any_role (bool): 是否拥有其中某一个角色
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/has-any-role",
            json={
                "hasAnyRole": has_any_role,
            },
        )

    def get_user_login_history(
        self, user_id, app_id=None, client_ip=None, start=None, end=None, options=None
    ):
        """获取用户的登录历史记录

        获取用户登录历史记录

        Attributes:
            user_id (str): 用户 ID
            app_id (str): 应用 ID
            client_ip (str): 客户端 IP
            start (int): 开始时间戳（毫秒）
            end (int): 结束时间戳（毫秒）
            options (dict): 可选参数
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/get-user-login-history",
            json={
                "userId": user_id,
                "appId": app_id,
                "clientIp": client_ip,
                "start": start,
                "end": end,
                "options": options,
            },
        )

    def get_user_logged_in_apps(self, user_id):
        """获取用户曾经登录过的应用

        获取用户曾经登录过的应用

        Attributes:
            user_id (str): 用户 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/get-user-loggedin-apps",
            json={
                "userId": user_id,
            },
        )

    def get_user_authorized_resources(self, user_id, options=None):
        """获取用户被授权的所有资源

        获取用户被授权的所有资源，用户被授权的资源是用户自身被授予、通过分组继承、通过角色继承、通过组织机构继承的集合

        Attributes:
            user_id (str): 用户 ID
            options (dict): 可选参数
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/get-user-authorized-resources",
            json={
                "userId": user_id,
                "options": options,
            },
        )

    def get_group(self, code):
        """获取分组详情

        通过分组 code 获取分组详情

        Attributes:
            code (str): 分组 code
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/get-group",
            json={
                "code": code,
            },
        )

    def get_group_list(self, options=None):
        """获取分组列表

        获取分组列表接口，支持分页

        Attributes:
            options (dict): 可选参数
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/list-groups",
            json={
                "options": options,
            },
        )

    def create_group(self, description, name, code):
        """创建分组



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

    def create_group_batch(self, list):
        """批量创建分组



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

    def update_group(self, new_code, description, name, code):
        """修改分组



        Attributes:
            new_code (str): 分组新的 code
            description (str): 分组描述
            name (str): 分组名称
            code (str): 分组 code
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/update-group",
            json={
                "newCode": new_code,
                "description": description,
                "name": name,
                "code": code,
            },
        )

    def delete_groups(self, code_list):
        """删除分组



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
        """移除分组成员



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

    def list_group_members(self, code, options=None):
        """获取分组成员列表



        Attributes:
            code (str): 分组 code
            options (dict): 可选参数
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/list-group-members",
            json={
                "code": code,
                "options": options,
            },
        )

    def get_group_authorized_resources(self, code, namespace=None, resource_type=None):
        """获取分组被授权的资源列表



        Attributes:
            code (str): 分组 code
            namespace (str): 所属权限分组的 code
            resource_type (str): 资源类型
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/get-group-authorized-resources",
            json={
                "code": code,
                "namespace": namespace,
                "resourceType": resource_type,
            },
        )

    def get_role(self, code, namespace=None):
        """获取角色详情

        获取角色详情

        Attributes:
            code (str): 角色唯一标识符
            namespace (str): 所属权限分组的 code
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/get-role",
            json={
                "code": code,
                "namespace": namespace,
            },
        )

    def assign_role(self, targets, code, namespace=None):
        """分配角色

        分配角色，被分配者可以是用户，可以是部门

        Attributes:
            targets (list): 目标对象
            code (str): 分组 code，识别码
            namespace (str): 权限分组
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

    def assign_role_batch(self, targets, roles):
        """分配角色

        分配角色，被分配者可以是用户，可以是部门

        Attributes:
            targets (list): 部门信息
            roles (list): 角色信息
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/assign-role-batch",
            json={
                "targets": targets,
                "roles": roles,
            },
        )

    def revoke_role(self, targets, code, namespace=None):
        """分配角色

        分配角色，被分配者可以是用户，可以是部门

        Attributes:
            targets (list): 部门信息
            code (str): 分组 code，识别码
            namespace (str): 权限分组
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

    def revoke_role_batch(self, targets, roles):
        """分配角色

        分配角色，被分配者可以是用户，可以是部门

        Attributes:
            targets (list): 目标信息
            roles (list): 角色信息
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/revoke-role-batch",
            json={
                "targets": targets,
                "roles": roles,
            },
        )

    def get_role_authorized_resources(self, code, namespace=None, resource_type=None):
        """角色被授权的资源列表

        角色被授权的资源列表

        Attributes:
            code (str): 分组 code，识别码
            namespace (str): 权限分组
            resource_type (str): 资源类型
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/get-role-authorized-resources",
            json={
                "code": code,
                "namespace": namespace,
                "resourceType": resource_type,
            },
        )

    def list_role_members(self, code, namespace=None, options=None):
        """获取角色成员列表

        获取角色成员列表

        Attributes:
            code (str): 角色唯一标识符
            namespace (str): 权限分组的 code
            options (dict): 可选参数
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/list-role-members",
            json={
                "code": code,
                "namespace": namespace,
                "options": options,
            },
        )

    def list_departments(self, code, namespace=None, options=None):
        """获取角色的部门列表

        获取角色的部门列表

        Attributes:
            code (str): 部门唯一标识符
            namespace (str): 权限分组的 code
            options (dict): 可选参数
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/list-role-departments",
            json={
                "code": code,
                "namespace": namespace,
                "options": options,
            },
        )

    def create_role(self, code, namespace=None, description=None):
        """创建角色

        创建角色

        Attributes:
            code (str): 角色 code
            namespace (str): 角色 namespace
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

    def list_roles(self, namespace, options=None):
        """获取角色列表

        获取角色列表

        Attributes:
            namespace (str): 角色 namespace
            options (dict): 可选参数
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/list-roles",
            json={
                "namespace": namespace,
                "options": options,
            },
        )

    def delete_roles(self, code_list, namespace=None):
        """删除角色

        删除角色

        Attributes:
            code_list (list): 角色 code 集合
            namespace (str): 权限分组的 code
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

        批量创建角色

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

        修改角色

        Attributes:
            new_code (str): 新的角色 code
            code (str): 角色 code
            namespace (str): 权限分组
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

    def list_organizations(self, options=None):
        """获取顶层组织机构列表

        获取顶层组织机构列表

        Attributes:
            options (dict): 可选参数
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/list-organizations",
            json={
                "options": options,
            },
        )

    def create_organization(self, organization_name, organization_code):
        """创建顶层组织机构

        创建顶层组织机构

        Attributes:
            organization_name (str): 组织名称
            organization_code (str): 组织 code
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/create-organization",
            json={
                "organizationName": organization_name,
                "organizationCode": organization_code,
            },
        )

    def update_organization(
        self, organization_code, organization_new_code=None, organization_name=None
    ):
        """修改顶层组织机构

        修改顶层组织机构

        Attributes:
            organization_code (str): 组织 code
            organization_new_code (str): 新组织 code
            organization_name (str): 组织名称
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/update-organization",
            json={
                "organizationCode": organization_code,
                "organizationNewCode": organization_new_code,
                "organizationName": organization_name,
            },
        )

    def delete_organization(self, organization_code):
        """删除顶层组织机构

        删除顶层组织机构

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

    def get_department(self, department_id, organization_code):
        """获取部门信息

        获取部门信息

        Attributes:
            department_id (str): 部门 id，根部门传 `root`
            organization_code (str): 组织 code
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/get-department",
            json={
                "departmentId": department_id,
                "organizationCode": organization_code,
            },
        )

    def create_department(
        self,
        organization_code,
        name,
        parent_department_id,
        code=None,
        leader_user_id=None,
    ):
        """创建部门

        创建部门

        Attributes:
            organization_code (str): 组织 code
            name (str): 部门名称
            parent_department_id (str): 父部门 id
            code (str): 部门识别码
            leader_user_id (str): 部门负责人 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/create-department",
            json={
                "organizationCode": organization_code,
                "name": name,
                "parentDepartmentId": parent_department_id,
                "code": code,
                "leaderUserId": leader_user_id,
            },
        )

    def update_department(
        self,
        organization_code,
        name,
        parent_department_id,
        department_id,
        code=None,
        leader_user_id=None,
    ):
        """修改部门

        修改部门

        Attributes:
            organization_code (str): 组织 code
            name (str): 部门名称
            parent_department_id (str): 父部门 id
            department_id (str): 部门 ID
            code (str): 部门识别码
            leader_user_id (str): 部门负责人 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/update-department",
            json={
                "organizationCode": organization_code,
                "name": name,
                "parentDepartmentId": parent_department_id,
                "departmentId": department_id,
                "code": code,
                "leaderUserId": leader_user_id,
            },
        )

    def delete_department(self, organization_code, department_id):
        """删除部门

        删除部门

        Attributes:
            organization_code (str): 组织 code
            department_id (str): 部门 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/delete-department",
            json={
                "organizationCode": organization_code,
                "departmentId": department_id,
            },
        )

    def search_departments(self, search, organization_code):
        """搜索部门

        搜索部门

        Attributes:
            search (str): 搜索关键词
            organization_code (str): 组织 code
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/search-departments",
            json={
                "search": search,
                "organizationCode": organization_code,
            },
        )

    def list_children_departments(self, department_id, organization_code):
        """获取子部门列表

        获取子部门列表

        Attributes:
            department_id (str): 部门 ID
            organization_code (str): 组织 code
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/list-children-departments",
            json={
                "departmentId": department_id,
                "organizationCode": organization_code,
            },
        )

    def list_department_members(self, department_id, organization_code, options=None):
        """获取部门直属成员列表

        获取部门直属成员列表

        Attributes:
            department_id (str): 部门 id，根部门传 `root`
            organization_code (str): 组织 code
            options (dict): 可选参数
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/list-department-members",
            json={
                "departmentId": department_id,
                "organizationCode": organization_code,
                "options": options,
            },
        )

    def list_department_member_ids(self, department_id, organization_code):
        """获取部门直属成员 ID 列表

        获取部门直属成员 ID 列表

        Attributes:
            department_id (str): 部门 ID
            organization_code (str): 组织 code
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/list-department-member-ids",
            json={
                "departmentId": department_id,
                "organizationCode": organization_code,
            },
        )

    def add_department_members(self, department_id, organization_code, user_ids):
        """部门下添加成员

        部门下添加成员

        Attributes:
            department_id (str): 部门 ID
            organization_code (str): 组织 code
            user_ids (list): 用户 ID 列表
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/add-department-members",
            json={
                "departmentId": department_id,
                "organizationCode": organization_code,
                "userIds": user_ids,
            },
        )

    def remove_department_members(self, department_id, organization_code, user_ids):
        """部门下删除成员

        部门下删除成员

        Attributes:
            department_id (str): 部门 ID
            organization_code (str): 组织 code
            user_ids (list): 用户 ID 列表
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/remove-department-members",
            json={
                "departmentId": department_id,
                "organizationCode": organization_code,
                "userIds": user_ids,
            },
        )

    def get_parent_department(self, department_id, organization_code):
        """获取父部门信息

        获取父部门信息

        Attributes:
            department_id (str): 部门 id
            organization_code (str): 组织 code
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/get-parent-department",
            json={
                "departmentId": department_id,
                "organizationCode": organization_code,
            },
        )

    def list_ext_idp(self, tenant_id=None):
        """获取身份源列表

        获取身份源列表

        Attributes:
            tenant_id (str): 租户 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/list-ext-idp",
            json={
                "tenantId": tenant_id,
            },
        )

    def get_ext_idp(self, id, tenant_id=None):
        """获取身份源详情

        获取身份源详情

        Attributes:
            id (str): 身份源 id
            tenant_id (str): 租户 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/get-ext-idp",
            json={
                "id": id,
                "tenantId": tenant_id,
            },
        )

    def create_ext_idp(self, type, name, tenant_id=None):
        """创建身份源

        创建身份源

        Attributes:
            type (str): 身份源连接类型
            name (str): 名称
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

        更新身份源配置

        Attributes:
            id (str): 连接 ID
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
        """删除身份源配置

        删除身份源配置

        Attributes:
            id (str): 连接 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/delete-ext-idp",
            json={
                "id": id,
            },
        )

    def create_ext_idp_conn(
        self, fields, logo, identifier, type, ext_idp_id, display_name=None
    ):
        """在某个已有身份源下创建新连接

        在某个已有身份源下创建新连接

        Attributes:
            fields (dict): 连接的自定义配置信息
            logo (str): 身份源图标
            identifier (str): 身份源连接标识
            type (str): 身份源连接类型
            ext_idp_id (str): 身份源连接 id
            display_name (str): 连接在登录页的显示名称
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/create-ext-idp-conn",
            json={
                "fields": fields,
                "logo": logo,
                "identifier": identifier,
                "type": type,
                "extIdpId": ext_idp_id,
                "displayName": display_name,
            },
        )

    def update_ext_idp_conn(
        self,
        login_only,
        association_mode,
        logo,
        fields,
        display_name,
        id,
        challenge_binding_methods=None,
    ):
        """更新身份源连接

        更新身份源连接

        Attributes:
            login_only (bool): 是否只支持登录
            association_mode (str): 关联模式
            logo (str): 图标
            fields (dict): 身份源连接自定义参数
            display_name (str): 身份源连接显示名称
            id (str): 连接 ID
            challenge_binding_methods (list): 绑定方式
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/update-ext-idp-conn",
            json={
                "loginOnly": login_only,
                "associationMode": association_mode,
                "logo": logo,
                "fields": fields,
                "displayName": display_name,
                "id": id,
                "challengeBindingMethods": challenge_binding_methods,
            },
        )

    def delete_ext_idp_conn(self, id):
        """删除身份源配置

        删除身份源配置

        Attributes:
            id (str): 连接 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/delete-ext-idp-conn",
            json={
                "id": id,
            },
        )

    def change_conn_state(self, tenant_id, app_id, enabled, id):
        """身份源连接开关

        身份源连接开关

        Attributes:
            tenant_id (str): 租户 ID
            app_id (str): 应用 ID
            enabled (bool): 是否开启身份源连接
            id (str): 连接 ID
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/enable-ext-idp-conn",
            json={
                "tenantId": tenant_id,
                "appId": app_id,
                "enabled": enabled,
                "id": id,
            },
        )

    def get_custom_fields(self, target_type):
        """获取用户池配置的扩展字段列表

        获取用户池配置的扩展字段列表

        Attributes:
            target_type (str): 主体类型，目前支持用户和角色
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/get-custom-fields",
            json={
                "targetType": target_type,
            },
        )

    def set_custom_fields(self, list):
        """创建扩展字段

        创建扩展字段

        Attributes:
            list (list): 扩展字段列表
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/set-custom-fields",
            json={
                "list": list,
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

        创建资源

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

        批量创建资源

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

        获取资源详情

        Attributes:
            code (str): 资源唯一标志符
            namespace (str): 所属权限分组的 code
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/get-resource",
            json={
                "code": code,
                "namespace": namespace,
            },
        )

    def get_resources_batch(self, code_list, namespace=None):
        """批量获取资源详情

        批量获取资源详情

        Attributes:
            code_list (list): 资源 code 列表
            namespace (str): 所属权限分组的 code
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/get-resources-batch",
            json={
                "codeList": code_list,
                "namespace": namespace,
            },
        )

    def list_resources(self, namespace=None, type=None, options=None):
        """分页获取资源列表

        分页获取资源列表

        Attributes:
            namespace (str): 所属权限分组的 code
            type (str): 资源类型
            options (dict): 可选参数
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/list-resources",
            json={
                "namespace": namespace,
                "type": type,
                "options": options,
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

        修改资源（Pratial Update）

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

        删除资源

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

        批量删除资源

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

    def create_namespace(self, code, name=None, description=None):
        """创建权限分组

        创建权限分组

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
        """创建权限分组

        创建权限分组

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

        获取权限分组详情

        Attributes:
            code (str): 权限分组唯一标志符
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/get-namespace",
            json={
                "code": code,
            },
        )

    def get_namespaces_batch(self, code_list):
        """批量获取权限分组详情

        批量获取权限分组详情

        Attributes:
            code_list (list): 权限分组 code 列表
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/get-namespaces-batch",
            json={
                "codeList": code_list,
            },
        )

    def update_namespace(self, code, description=None, name=None, new_code=None):
        """修改权限分组信息

        修改权限分组信息

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

    def dekete_namespace(self, code):
        """删除权限分组信息

        删除权限分组信息

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

    def dekete_namespaces_batch(self, code_list):
        """批量删除权限分组信息

        批量删除权限分组信息

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

        给多个主体同时授权多个资源

        Attributes:
            list (list): 授权列表
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

    def get_target_authorized_resources(
        self, target_identifier, target_type, namespace=None, resource_type=None
    ):
        """获取某个主体被授权的资源列表

        获取某个主体被授权的资源列表

        Attributes:
            target_identifier (str): 目标对象唯一标志符
            target_type (str): 目标对象类型
            namespace (str): 所属权限分组的 code
            resource_type (str): 资源类型，如数据、API、按钮、菜单
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/get-authorized-resources",
            json={
                "targetIdentifier": target_identifier,
                "targetType": target_type,
                "namespace": namespace,
                "resourceType": resource_type,
            },
        )
