# authing-py-sdk

---

Authing Python SDK 目前只支持 Python3+。

[Authing 官方文档请点击这里](https://docs.authing.cn/authing/)。

[Python SDK 文档请点这里](https://docs.authing.cn/authing/sdk/sdk-for-python)。

## 安装

---

#### pip

当构建大规模应用时，我们推荐使用`pip`进行安装， 它可以与一些模块打包工具很好地配合使用。
注意，Authing 目前仅能从 pip3 以上安装。

```shell
# latest stable
$ pip install authing
```

## 开始使用

---

首先在目录下新建一个名为 `pub.pem` 的文件，并将以下内容复制到文件中：

```shell
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC4xKeUgQ+Aoz7TLfAfs9+paePb
5KIofVthEopwrXFkp8OCeocaTHt9ICjTT2QeJh6cZaDaArfZ873GPUn00eOIZ7Ae
+TiA2BKHbCvloW3w5Lnqm70iSsUi5Fmu9/2+68GZRH9L7Mlh8cFksCicW2Y2W2uM
GKl64GDcIq3au+aqJQIDAQAB
-----END PUBLIC KEY-----
```

然后初始化 Authing：

```python
from authing.authing import Authing

clientId = 'your_client_id'
secret = 'your_app_secret'

authing = Authing(clientId, secret)

# 如果 Authing 验证 clientId 和 secret 失败，将会抛出一个错误。所以在初始化构造函数的时候，可以使用 try...catch 保证程序不会挂掉。

user = authing.login(**{
    'email': 'test@testmail.com',
    'password': 'testpassword'
})

if user.get('errors'):
    # 出错
else:
    # 未出错

```

[如何获取 ClientId 和 Secret?](https://learn.authing.cn/authing/others/faq#ru-he-huo-qu-client-id-he-client-secret)。

## 错误处理

---

SDK 中的接口返回数据若出错会存在 "errors" 字段，因此可以用如下代码检查是否出错：

```python

result = authing.xxx() # 执行authing的某方法

if result.get('errors'):
    # 出错，如
    """
    {'code': 500, 'message': 'Cast to ObjectId failed for value "5aec1ea610ecb800018db176xx" at path "_id" for model "User"', 'data': None, 'errors': True}
    """
else:
    # 未发生错误，直接使用数据即可，如：
    """
    {'_id': '5aec1ea610ecb800018db176', 'email': 'xieyang@dodora.cn', 'isDeleted': False}
    """

```

## 自定义请求链接

---

如果你私有部署了 Authing，可以通过以下方式初始化 URL：

```python
from authing.authing import Authing

clientId = 'your_client_id'
secret = 'your_app_secret'

authing = Authing(clientId, secret, {
    "oauth": 'https://oauth.your_url.com/graphql',
    "users": 'https://users.your_url.com/graphql'
})
```

了解更多报错的详情，请查看[错误代码列表](https://learn.authing.cn/authing/advanced/error-code)。

[接口相关文档请点击这里](https://docs.authing.cn/authing/sdk/sdk-for-python)。

## 测试

```python
pytest authing/test.py
```

## Get Help

1. Join us on Gitter: [#authing-chat](https://gitter.im/authing-chat/community)
