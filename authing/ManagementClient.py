from .ManagementClientOptions import ManagementClientOptions

class ManagementClient(object):
    """Authing Management Client"""
    def __init__(self, options):
        # type:(ManagementClientOptions) -> ManagementClient
        self.options = options

    def get_management_token(self, dto):
        """获取 Management API Token

        获取 Management API Token
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/get-management-token',
            body=dto,
            mediaType='application/json',
        )

    def get_user(self, dto):
        """获取用户信息

        获取用户信息
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/get-user',
            body=dto,
            mediaType='application/json',
        )

    def get_user_batch(self, dto):
        """批量获取用户信息

        根据用户 id 批量获取用户信息
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/get-user-batch',
            body=dto,
            mediaType='application/json',
        )

    def list_users(self, dto):
        """获取用户列表

        获取用户列表接口，支持分页
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/list-users',
            body=dto,
            mediaType='application/json',
        )

    def get_user_identities(self, dto):
        """获取用户的外部身份源

        获取用户的外部身份源
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/get-user-identities',
            body=dto,
            mediaType='application/json',
        )

    def get_user_custom_data(self, dto):
        """获取用户自定义数据

        获取用户自定义数据
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/get-user-custom-data',
            body=dto,
            mediaType='application/json',
        )

    def set_user_custom_data(self, dto):
        """设置用户自定义数据

        设置用户自定义数据
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/set-user-custom-data',
            body=dto,
            mediaType='application/json',
        )

    def get_user_roles(self, dto):
        """获取用户角色列表

        获取用户角色列表
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/get-user-roles',
            body=dto,
            mediaType='application/json',
        )

    def get_principal_authentication_info(self, dto):
        """获取用户实名认证信息 

        获取用户实名认证信息 
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/get-user-principal-authentication-info',
            body=dto,
            mediaType='application/json',
        )

    def reset_principal_authentication_info(self, dto):
        """删除用户实名认证信息 

        删除用户实名认证信息 
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/reset-user-principal-authentication-info',
            body=dto,
            mediaType='application/json',
        )

    def get_user_departments(self, dto):
        """获取用户部门列表

        获取用户部门列表
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/get-user-departments',
            body=dto,
            mediaType='application/json',
        )

    def set_user_department(self, dto):
        """设置用户所在部门 

        设置用户所在部门 
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/set-user-departments',
            body=dto,
            mediaType='application/json',
        )

    def get_user_groups(self, dto):
        """获取用户分组列表

        获取用户分组列表
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/get-user-groups',
            body=dto,
            mediaType='application/json',
        )

    def delete_user_batch(self, dto):
        """删除用户

        删除用户（支持批量删除）
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/delete-users-batch',
            body=dto,
            mediaType='application/json',
        )

    def get_user_mfa_info(self, dto):
        """获取用户 MFA 绑定信息

        获取用户 MFA 绑定信息
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/get-user-mfa-info',
            body=dto,
            mediaType='application/json',
        )

    def list_archived_users(self, dto):
        """获取已归档的用户列表

        获取已归档的用户列表
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/list-archived-users',
            body=dto,
            mediaType='application/json',
        )

    def kick_users(self, dto):
        """强制下线用户

        强制下线用户
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/kick-users',
            body=dto,
            mediaType='application/json',
        )

    def is_user_exists(self, dto):
        """判断用户是否存在

        根据条件判断用户是否存在
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/is-user-exists',
            body=dto,
            mediaType='application/json',
        )

    def create_user(self, dto):
        """创建用户

        创建用户，邮箱、手机号、用户名必须包含其中一个
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/create-user',
            body=dto,
            mediaType='application/json',
        )

    def create_user_batch(self, dto):
        """批量创建用户

        批量创建用户
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/create-users-batch',
            body=dto,
            mediaType='application/json',
        )

    def update_user(self, dto):
        """修改用户资料

        修改用户资料
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/update-user',
            body=dto,
            mediaType='application/json',
        )

    def get_user_accessible_apps(self, dto):
        """获取用户可访问应用

        获取用户可访问应用
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/get-user-accessible-apps',
            body=dto,
            mediaType='application/json',
        )

    def get_user_authorized_apps(self, dto):
        """获取用户授权的应用

        获取用户授权的应用
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/get-user-authorized-apps',
            body=dto,
            mediaType='application/json',
        )

    def has_any_role(self, dto):
        """判断用户是否有某个角色

        判断用户是否有某个角色，支持同时传入多个角色进行判断
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/has-any-role',
            body=dto,
            mediaType='application/json',
        )

    def get_user_login_history(self, dto):
        """获取用户的登录历史记录

        获取用户登录历史记录
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/get-user-login-history',
            body=dto,
            mediaType='application/json',
        )

    def get_user_logged_in_apps(self, dto):
        """获取用户曾经登录过的应用

        获取用户曾经登录过的应用
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/get-user-loggedin-apps',
            body=dto,
            mediaType='application/json',
        )

    def get_user_authorized_resources(self, dto):
        """获取用户被授权的所有资源，用户被授权的资源是用户自身被授予、通过分组继承、通过角色继承、通过组织机构继承的集合

        获取用户被授权的所有资源
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/get-user-authorized-resources',
            body=dto,
            mediaType='application/json',
        )

    def get_group(self, dto):
        """获取分组详情

        通过分组 code 获取分组详情
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/get-group',
            body=dto,
            mediaType='application/json',
        )

    def get_group_list(self, dto):
        """获取分组列表

        获取分组列表接口，支持分页
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/list-groups',
            body=dto,
            mediaType='application/json',
        )

    def create_group(self, dto):
        """创建分组

        
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/create-group',
            body=dto,
            mediaType='application/json',
        )

    def create_group_batch(self, dto):
        """批量创建分组

        
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/create-groups-batch',
            body=dto,
            mediaType='application/json',
        )

    def update_group(self, dto):
        """修改分组

        
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/update-group',
            body=dto,
            mediaType='application/json',
        )

    def delete_groups(self, dto):
        """删除分组

        
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/delete-groups-batch',
            body=dto,
            mediaType='application/json',
        )

    def add_group_members(self, dto):
        """添加分组成员

        
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/add-group-members',
            body=dto,
            mediaType='application/json',
        )

    def remove_group_members(self, dto):
        """移除分组成员

        
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/remove-group-members',
            body=dto,
            mediaType='application/json',
        )

    def list_group_members(self, dto):
        """获取分组成员列表

        
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/list-group-members',
            body=dto,
            mediaType='application/json',
        )

    def get_group_authorized_resources(self, dto):
        """获取分组被授权的资源列表

        
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/get-group-authorized-resources',
            body=dto,
            mediaType='application/json',
        )

    def get_role(self, dto):
        """获取角色详情

        获取角色详情
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/get-role',
            body=dto,
            mediaType='application/json',
        )

    def assign_role(self, dto):
        """分配角色

        分配角色，被分配者可以是用户，可以是部门
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/assign-role',
            body=dto,
            mediaType='application/json',
        )

    def assign_role_batch(self, dto):
        """分配角色

        分配角色，被分配者可以是用户，可以是部门
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/assign-role-batch',
            body=dto,
            mediaType='application/json',
        )

    def revoke_role(self, dto):
        """分配角色

        分配角色，被分配者可以是用户，可以是部门
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/revoke-role',
            body=dto,
            mediaType='application/json',
        )

    def revoke_role_batch(self, dto):
        """分配角色

        分配角色，被分配者可以是用户，可以是部门
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/revoke-role-batch',
            body=dto,
            mediaType='application/json',
        )

    def get_role_authorized_resources(self, dto):
        """角色被授权的资源列表

        角色被授权的资源列表
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/get-role-authorized-resources',
            body=dto,
            mediaType='application/json',
        )

    def list_role_members(self, dto):
        """获取角色成员列表

        获取角色成员列表
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/list-role-members',
            body=dto,
            mediaType='application/json',
        )

    def list_departments(self, dto):
        """获取角色的部门列表

        获取角色的部门列表
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/list-role-departments',
            body=dto,
            mediaType='application/json',
        )

    def create_role(self, dto):
        """创建角色

        创建角色
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/create-role',
            body=dto,
            mediaType='application/json',
        )

    def list_roles(self, dto):
        """获取角色列表

        获取角色列表
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/list-roles',
            body=dto,
            mediaType='application/json',
        )

    def delete_roles(self, dto):
        """删除角色

        删除角色
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/delete-roles-batch',
            body=dto,
            mediaType='application/json',
        )

    def create_roles_batch(self, dto):
        """批量创建角色

        批量创建角色
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/create-roles-batch',
            body=dto,
            mediaType='application/json',
        )

    def update_role(self, dto):
        """修改角色

        修改角色
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/update-role',
            body=dto,
            mediaType='application/json',
        )

    def list_organizations(self, dto):
        """获取顶层组织机构列表

        获取顶层组织机构列表
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/list-organizations',
            body=dto,
            mediaType='application/json',
        )

    def create_organization(self, dto):
        """创建顶层组织机构

        创建顶层组织机构
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/create-organization',
            body=dto,
            mediaType='application/json',
        )

    def update_organization(self, dto):
        """修改顶层组织机构

        修改顶层组织机构
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/update-organization',
            body=dto,
            mediaType='application/json',
        )

    def delete_organization(self, dto):
        """删除顶层组织机构

        删除顶层组织机构
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/delete-organization',
            body=dto,
            mediaType='application/json',
        )

    def get_department(self, dto):
        """获取部门信息

        获取部门信息
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/get-department',
            body=dto,
            mediaType='application/json',
        )

    def create_department(self, dto):
        """创建部门

        创建部门
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/create-department',
            body=dto,
            mediaType='application/json',
        )

    def update_department(self, dto):
        """修改部门

        修改部门
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/update-department',
            body=dto,
            mediaType='application/json',
        )

    def delete_department(self, dto):
        """删除部门

        删除部门
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/delete-department',
            body=dto,
            mediaType='application/json',
        )

    def search_departments(self, dto):
        """搜索部门

        搜索部门
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/search-departments',
            body=dto,
            mediaType='application/json',
        )

    def list_children_departments(self, dto):
        """获取子部门列表

        获取子部门列表
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/list-children-departments',
            body=dto,
            mediaType='application/json',
        )

    def list_department_members(self, dto):
        """获取部门直属成员列表

        获取部门直属成员列表
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/list-department-members',
            body=dto,
            mediaType='application/json',
        )

    def list_department_member_ids(self, dto):
        """获取部门直属成员 ID 列表

        获取部门直属成员 ID 列表
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/list-department-member-ids',
            body=dto,
            mediaType='application/json',
        )

    def add_department_members(self, dto):
        """部门下添加成员

        部门下添加成员
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/add-department-members',
            body=dto,
            mediaType='application/json',
        )

    def remove_department_members(self, dto):
        """部门下删除成员

        部门下删除成员
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/remove-department-members',
            body=dto,
            mediaType='application/json',
        )

    def get_parent_department(self, dto):
        """获取父部门信息

        获取父部门信息
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/get-parent-department',
            body=dto,
            mediaType='application/json',
        )

    def get_custom_fields(self, dto):
        """获取用户池配置的扩展字段列表

        获取用户池配置的扩展字段列表
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/get-custom-fields',
            body=dto,
            mediaType='application/json',
        )

    def set_custom_fields(self, dto):
        """创建扩展字段

        创建扩展字段
        """
        return self.httpClient.request(
            method='POST',
            url='/api/v3/set-custom-fields',
            body=dto,
            mediaType='application/json',
        )

