from setuptools import setup, find_packages  
  
setup(  
      name='authing',   #名称  
      version='0.1.3',  #版本  
      description="Authing SDK for Python", #描述  
      keywords='authing sso AaaS IdaaS',  
      author='authing',  #作者  
      author_email='xieyang@dodora.cn', #作者邮箱  
      url='https://github.com/Authing/authing-py-sdk', #作者链接  
      packages=find_packages(),  
      include_package_data=True,  
      zip_safe=False,  
      install_requires=[      #需求的第三方模块  
        'sgqlc'
      ], 
)  
