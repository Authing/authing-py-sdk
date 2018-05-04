from setuptools import setup, find_packages  
  
setup(  
      name='authing-py-sdk',   #名称  
      version='0.1.0',  #版本  
      description="Authing SDK for Python", #描述  
      keywords='authing,',  
      author='authing',  #作者  
      author_email='xieyang@dodora.cn', #作者邮箱  
      url='https://github.com/authing', #作者链接  
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests', 'test']),  
      include_package_data=True,  
      zip_safe=False,  
      install_requires=[      #需求的第三方模块  
        'requests',
        'sgqlc'
      ], 
)  