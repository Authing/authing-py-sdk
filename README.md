# Authing - Python

Authing Python SDK 由两部分组成：`ManagementClient` 和 `AuthenticationClient`。`ManagementClient` 中进行的所有操作均以管理员的身份进行，包含管理用户、管理角色、管理权限策略、管理用户池配置等模块。`AuthenticationClient` 中的所有操作以当前终端用户的身份进行，包含登录、注册、修改用户资料、退出登录等方法。

你应该将初始化过后的 `ManagementClient` 实例设置为一个全局变量（只初始化一次），而 `AuthenticationClient` 应该每次请求初始化一个。

Authing Python SDK 同时支持 `python2` 和 `python3`。


  - [安装](#安装)
  - [使用用户管理模块](#使用用户管理模块)
  - [使用用户认证模块](#使用用户认证模块)
  - [错误处理](#错误处理)
  - [私有化部署](#私有化部署)
  - [接口索引](#接口索引)
  - [获取帮助](#获取帮助)


> Authing Python SDK 同时支持 `python2` 和 `python3`。

## 安装

```
pip install authing
```

## 使用用户管理模块

初始化 `ManagementClient` 需要 `user_pool_id`（用户池 ID） 和 `secret`（用户池密钥）:

> 你可以在此[了解如何获取 UserPoolId 和 Secret](https://docs.authing.cn/others/faq.html) .

```python
from authing.v2.management import ManagementClient, ManagementClientOptions

management_client = ManagementClient(
  options=ManagementClientOptions(
    user_pool_id='AUTHING_USERPOOL_ID',
    secret='AUTHING_USERPOOL_SECRET',
))
```

现在 `ManagementClient()` 实例就可以使用了。例如可以获取用户池中的用户列表：

```python
data = management_client.users.list()
```

返回的数据如下：

```json
{
  "totalCount": 1,
  "list": [
    {
      "id": "5f7ddfe62ba819802422362e",
      "arn": "arn:cn:authing:5f7a993eb9b49dcd5c021e40:user:5f7ddfe62ba819802422362e",
      "userPoolId": "5f7a993eb9b49dcd5c021e40",
      "username": "nhxcpzmklk",
      "email": null,
      "emailVerified": false,
      "phone": null,
      "phoneVerified": false,
      "unionid": null,
      "openid": null,
      "nickname": null,
      "registerSource": ["import:manual"],
      "photo": "https://usercontents.authing.cn/authing-avatar.png",
      "password": "a56f21e5659428f9b353be4ed667fc05",
      "oauth": null,
      "token": null,
      "tokenExpiredAt": null,
      "loginsCount": 0,
      "lastLogin": null,
      "lastIP": null,
      "signedUp": "2020-10-07T23:33:58+08:00",
      "blocked": false,
      "isDeleted": false,
      "device": null,
      "browser": null,
      "company": null,
      "name": null,
      "givenName": null,
      "familyName": null,
      "middleName": null,
      "profile": null,
      "preferredUsername": null,
      "website": null,
      "gender": "U",
      "birthdate": null,
      "zoneinfo": null,
      "locale": null,
      "address": null,
      "formatted": null,
      "streetAddress": null,
      "locality": null,
      "region": null,
      "postalCode": null,
      "country": null,
      "createdAt": "2020-10-07T23:33:58+08:00",
      "updatedAt": "2020-10-07T23:33:58+08:00"
    }
  ]
}
```

## 使用用户认证模块

初始化 `AuthenticationClient` 需要 `app_id`（应用 ID）：

> 你可以在此控制台应用列表页面获取 `app_id` 。

```python
from authing.v2.authentication import AuthenticationClient, AuthenticationClientOptions

authentication_client = AuthenticationClient(
  options=AuthenticationClientOptions(
    app_id='AUTHING_APP_ID'
))
```

接下来可以进行注册登录等操作：

```python
username = get_random_string(10)
password = get_random_string(10)
user = authentication_client.login_by_username(
    username=username,
    password=password,
)
```

完成登录之后，`update_profile` 等要求用户登录的方法就可用了：

```python
authentication_client.update_profile({
  'nickname': 'Nick'
})
```

你也可以使用 `token` 参数来初始化 `AuthenticationClient`, 而不需要每次都调用 `login` 方法:

```python
from authing.v2.authentication import AuthenticationClient, AuthenticationClientOptions

authentication_client = AuthenticationClient(
  options=AuthenticationClientOptions(
    app_id='AUTHING_APP_ID',
    token='AUTHING_USER_TOKEN'
))
```

再次执行 `update_profile` 方法，发现也成功了:

```
user = authentication_client.update_profile({
  'nickname': 'Nick'
})
```

## 错误处理

```python
from authing.v2.exceptions import AuthingException

try:
    authentication_client.login_by_username(
        username='bob',
        password='passw0rd',
    )
except AuthingException as e:
    print(e.code) # 2004
    print(e.message) # 用户不存在
```

> 完整的错误代码请见[此文档](https://docs.authing.cn/v2/reference/error-code.html)。

## 私有化部署

**私有化部署**场景需要指定你私有化的 Authing 服务的 GraphQL 端点（**不带协议头和 Path**），如果你不清楚可以联系 Authing IDaaS 服务管理员。

```python
from authing.v2.management import ManagementClient, ManagementClientOptions

management_client = ManagementClient(
  options=ManagementClientOptions(
    user_pool_id='AUTHING_USERPOOL_ID',
    secret='AUTHING_USERPOOL_SECRET',
    host="https://core.you-authing-service.com"
))
```

## 接口索引

认证模块包含以下方法：

- 获取当前用户的用户资料: `get_current_user`
- 使用邮箱注册: `register_by_email`
- 使用用户名注册: `register_by_username`
- 使用手机号验证码注册: `register_by_phone_code`
- 使用邮箱登录: `login_by_email`
- 使用用户名登录: `login_by_username`
- 使用手机号验证码登录 `login_by_phone_code`
- 使用手机号密码登录: `login_by_phone_password`
- 发送邮件: `send_email`
- 发送短信验证码: `send_sms_code`
- 检查 token 的有效状态: `check_login_status`
- 使用手机号验证码重置密码: `reset_password_by_phone_code`
- 使用邮件验证码重置密码: `reset_password_by_email_code`
- 更新用户资料: `update_profile`
- 更新密码: `update_password`
- 更新手机号: `update_phone`
- 更新邮箱: `update_email`
- 刷新 token: `refresh_token`
- 绑定手机号: `bind_phone`
- 解绑手机号: `unbind_phone`
- 添加当前用户自定义字段值: `set_udv`
- 获取当前用户的自定义字段值： `udv`
- 删除当前用户自定义字段值: `remove_udv`

详情请见：

[用户认证模块](https://docs.authing.cn/v2/reference/sdk-for-python/authentication/)

管理模块包含以下子模块：

[管理用户](https://docs.authing.cn/v2/reference/sdk-for-python/management/UsersManagementClient.html)

[管理角色](https://docs.authing.cn/v2/reference/sdk-for-python/management/RolesManagementClient.html)

[管理策略](https://docs.authing.cn/v2/reference/sdk-for-python/management/PoliciesManagementClient.html)

[管理权限、访问控制](https://docs.authing.cn/v2/reference/sdk-for-python/management/AclManagementClient.html)

[管理用户自定义字段](https://docs.authing.cn/v2/reference/sdk-for-python/management/UdfManagementClient.html)

详细的接口文档请见：[认证模块文档](https://docs.authing.co/v2/reference/sdk-for-python/authentication/) 和 [管理模块文档](https://docs.authing.co/v2/reference/sdk-for-python/management/)。
## 获取帮助

Join us on Gitter: [#authing-chat](https://gitter.im/authing-chat/community)
