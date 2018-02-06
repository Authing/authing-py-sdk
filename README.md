# authing-py-sdk

----------

Authing Python SDk目前只支持Python3+。

[官方文档请点击这里](https://docs.authing.cn)。

## 安装

----------

#### pip

当构建大规模应用时，我们推荐使用```pip```进行安装， 它可以与一些模块打包工具很好地配合使用。

``` shell
# latest stable
$ pip install authing
```

## 开始使用

----------

``` python
from authing import Authing

clientId = 'your_client_id'
secret = 'your_app_secret'

authing = Authing(clientId, secret)

auth_result = authing.auth()

if auth_result:
    try:
        user = authing.login({
            'email': 'test@testmail.com',
            'password': 'testpassword'
        })
        # 取得用户的登录信息
    except Exception as e:
        # 登录失败
        raise e
else:
    # clientId和secret认证失败

```

[怎样获取client ID ?](https://docs.authing.cn/#/quick_start/howto)。

了解更多报错的详情，请查看[错误代码](https://docs.authing.cn/#/quick_start/error_code)。

获取Client ID和Client Secret，请[点击这里](https://docs.authing.cn/#/quick_start/howto)。

[完整官方文档请点击这里](https://docs.authing.cn)。
