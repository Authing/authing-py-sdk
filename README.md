# Authing - Python

Authing Python SDK 由两部分组成：`ManagementClient` 和 `AuthenticationClient`。`ManagementClient` 中进行的所有操作均以管理员的身份进行，包含管理用户、管理角色、管理权限策略、管理用户池配置等模块。`AuthenticationClient` 中的所有操作以当前终端用户的身份进行，包含登录、注册、修改用户资料、退出登录等方法。

你应该将初始化过后的 `ManagementClient` 实例设置为一个全局变量（只初始化一次），而 `AuthenticationClient` 应该每次请求初始化一个。

- [安装](#安装)
- [使用 ManagementClient](#使用-managementclient)
  - [可用的 Management 模块](#可用的-management-模块)
- [使用 AuthenticationClient](#使用-authenticationclient)
  - [可用的 Authentication 方法](#可用的-authentication-方法)

## 安装

```
pip install authing
```

## 使用 ManagementClient

初始化 `ManagementClient` 需要 `user_pool_id`（用户池 ID） 和 `secret`（用户池密钥）:

> 你可以在此[了解如何获取 UserPoolId 和 Secret](https://docs.authing.cn/others/faq.html) .

```python
from authing.v2.management import ManagementClient, ManagementClientOptions

authing = ManagementClient(
  options=ManagementClientOptions(
    user_pool_id='AUTHING_USERPOOL_ID',
    secret='AUTHING_USERPOOL_SECRET',
))
```

现在 `ManagementClient()` 实例就可以使用了。例如可以获取用户池中的用户列表：

```python
data = authing.users.list()
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
      "registerSource": [
        "import:manual"
      ],
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
      "updatedAt": "2020-10-07T23:33:58+08:00",
    }
  ]
}
```


### 可用的 Management 模块

- Users `ManagementClient().users`
- Roles `ManagementClient().roles`
- Policies `ManagementClient().policies`
- Access Control: `ManagementClient().acl`

## 使用 AuthenticationClient

初始化 `ManagementClient` 需要 `user_pool_id`（用户池 ID）：

> 你可以在此[了解如何获取 UserPoolId](https://docs.authing.cn/others/faq.html) .


```python
from authing.v2.authentication import AuthenticationClient, AuthenticationClientOptions

authing = AuthenticationClient(
  options=AuthenticationClientOptions(
    user_pool_id='AUTHING_USERPOOL_ID'
))
```

接下来可以进行注册登录等操作：

```python
username = get_random_string(10)
password = get_random_string(10)
user = authentication.login_by_username(
    username=username,
    password=password,
)
```

完成登录之后，`update_profile` 等要求用户登录的方法就可用了：

```python
authing.update_profile({
  'nickname': 'Nick'
})
```

你也可以使用 `access_token` 参数来初始化 `AuthenticationClient`, 而不需要每次都调用 `login` 方法:

```python
from authing.v2.authentication import AuthenticationClient, AuthenticationClientOptions

authing = AuthenticationClient(
  options=AuthenticationClientOptions(
    user_pool_id='AUTHING_USERPOOL_ID',
    access_token='AUTHING_USER_TOKEN'
))
```

再次执行 `update_profile` 方法，发现也成功了:

```
user = authing.update_profile({
  'nickname': 'Nick'
})
```

### 可用的 Authentication 方法

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
