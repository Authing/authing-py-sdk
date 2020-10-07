# Authing - Python

- [Installation](#installation)
- [Management SDK Usage](#management-sdk-usage)
  - [Available Management Modules](#available-management-modules)
- [Authentication SDK Usage](#authentication-sdk-usage)
  - [Available Authentication Methods](#available-authentication-methods)

## Installation

You can install the auth0 Python SDK using the following command.

```
pip install authing
```

## Management SDK Usage

To use the management library you will need to instantiate an `ManagementClient` object with a `user_pool_id` and a `secret` (see [here](https://docs.authing.cn/others/faq.html) how to get those): 

```python
from authing.v2.management import ManagementClient, ManagementClientOptions

authing = ManagementClient(
  options=ManagementClientOptions(
    user_pool_id='AUTHING_USERPOOL_ID',
    secret='AUTHING_USERPOOL_SECRET',
))
```

the `ManagementClient()` object is now ready to take orders! Let's see how we can use this to get all users:

```python
totalCount, users = authing.users.list()
```

Which will yield a list of users similar to this:

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

That's it!

### Available Management Modules

- Users `ManagementClient().users`
- Roles `ManagementClient().roles`
- Policies `ManagementClient().policies`

## Authentication SDK Usage

To use the authentication library you will need to instantiate an `AuthenticationClient` object with a `user_pool_id`  (see [here](https://docs.authing.cn/others/faq.html) how to get this): 

```python
from authing.v2.authentication import AuthenticationClient, AuthenticationClientOptions

authing = AuthenticationClient(
  options=AuthenticationClientOptions(
    user_pool_id='AUTHING_USERPOOL_ID'
))
```

Now it's ready to use:

```python
username = get_random_string(10)
password = get_random_string(10)
user = authentication.register_by_username(
    username=username,
    password=password,
)
```

Then you can update userinfo etc:

```
authing.update_profile({
  'nickname': 'Nick'
})
```

And you can also instantiate `AuthenticationClient` with a `access_token` param instead:

```
from authing.v2.authentication import AuthenticationClient, AuthenticationClientOptions

authing = AuthenticationClient(
  options=AuthenticationClientOptions(
    user_pool_id='AUTHING_USERPOOL_ID',
    access_token='AUTHING_USER_TOKEN'
))
```

Then the `update_profile` function is avaliable: 

```
authing.update_profile({
  'nickname': 'Nick'
})
```

It works.

### Available Authentication Methods

- Get Current User's Detail UserInfo: `AuthenticationClient().get_current_user()`
- Register By Email: `AuthenticationClient().register_by_email()`