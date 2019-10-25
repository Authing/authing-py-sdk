from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='authing',  # 名称
    version='0.15.1',  # 版本
    description="Authing SDK for Python",  # 描述
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='authing sso AaaS IdaaS',
    author='authing',  # 作者
    author_email='xieyang@authing.cn',  # 作者邮箱
    maintainer='authing',
    maintainer_email='xieyang@authing.cn',
    url='https://github.com/Authing/authing-py-sdk',  # 作者链接
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[  # 需求的第三方模块
        'sgqlc',
        'rsa'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
