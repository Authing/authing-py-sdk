# Authing - Python

[Authing](https://authing.co) 身份云 `Python` 语言客户端，同时支持 Python2 和 Python3，包含 [Authing Open API](https://core.authing.cn/openapi/) 所有 Management API 的请求方法。

此模块一般用于后端服务器环境，以管理员（Administrator）的身份进行请求，用于管理 Authing 用户、角色、分组、组织机构等资源；一般来说，你在 Authing 控制台中能做的所有操作，都能用此模块完成。

如果你需要以终端用户（End User）的身份进行登录、注册、登出等操作，请使用 [TODO](TODO) .

## 安装

```bash
pip install authing
```

## 初始化

初始化 `ManagementClient` 需要使用 `accessKeyId` 和 `accessKeySecret` 参数:

```typescript
from authing import ManagementClient, ManagementClientOptions

management_client = ManagementClient(
    options=ManagementClientOptions(
        access_key_id="6250f12d5xxxx69bcfcf784b",
        access_key_secret="4ae78d3e579a6xxxx01aeca7b1e29ec2",
    )
)
```

`ManagementClient` 会自动从 Authing 服务器获取  Management API Token，并通过返回的 Token 过期时间自动对 Token 进行缓存。

完整的参数和释义如下：

- `access_key_id`: Authing 用户池 ID;
- `access_key_secret`: Authing 用户池密钥;
- `timeout`: 超时时间，单位为 ms，默认为 10000 ms;
- `host`: Authing 服务器地址，默认为 `https://api.authing.cn`。如果你使用的是 Authing 公有云版本，请忽略此参数。如果你使用的是私有化部署的版本，此参数必填，格式如下: https://authing-api.my-authing-service.com（最后不带斜杠 /）。
- `lang`: 接口 Message 返回语言格式（可选），可选值为 zh-CN 和 en-US，默认为 zh-CN。
- `use_unverified_ssl`: 不校验 ssl 证书，默认为 false。

## 快速开始

初始化完成 `ManagementClient`  之后，你可以获取 `ManagementClient` 的实例，然后调用此实例上的方法。例如：

- 获取用户列表

```typescript
data = management_client.list_users(
    page=1,
    limit=10
)
```

- 创建角色

```typescript
data = management_client.create_role(
  code='admin',
  description='管理员',
  namespace='default'
);
```

完整的接口列表，你可以在 [Authing Open API](https://core.authing.cn/openapi/) 中获取。


## 错误处理


`ManagementClient` 中的每个方法，遵循统一的返回结构：

- `code`: 请求是否成功状态码，当 `code` 为 200 时，表示操作成功，非 200 全部为失败。
- `errorCode`: 细分错误码，当 `code` 非 200 时，可通过此错误码得到具体的错误类型。完整的错误码列表，请见：[TODO](TODO)。
- `message`: 具体的错误信息。
- `data`: 具体返回的接口数据。

一般情况下，如果你只需要判断操作是否成功，只需要对比一下 `code` 是否为 200。如果非 200，可以在代码中通抛出异常或者任何你项目中使用的异常处理方式。

```python
data = await management_client.get_user(
  userId="62559df6b2xxxx259877b5f4"
)

code, error_code, message = data.get('code'), data.get('error_code'), data.get('message')
if (code !== 200) {
  raise Exception(message); # 抛出异常，由全局异常捕捉中间件进行异常捕捉
}

// 继续你的业务逻辑 ...
```

## 私有化部署


如果你使用的是私有化部署的 Authing IDaaS 服务，需要指定此 Authing 私有化实例的 `host`，如：

```python
from authing import ManagementClient, ManagementClientOptions

management_client = ManagementClient(
    options=ManagementClientOptions(
        access_key_id="6250f12d5xxxx69bcfcf784b",
        access_key_secret="4ae78d3e579a6xxxx01aeca7b1e29ec2",
    )
)
```

如果你不清楚如何获取，可以联系 Authing IDaaS 服务管理员。


## 获取帮助

有任何疑问，可以在 Authing 论坛提出: [#authing-forum](https://forum.authing.cn/)
