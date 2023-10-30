# coding: utf-8
import json

from .http.ManagementHttpClient import ManagementHttpClient
from .utils.signatureComposer import getAuthorization
from .utils.wss import handleMessage


class ManagementClient(object):
    """Authing Management Client"""

    def __init__(
            self,
            access_key_id,
            access_key_secret,
            host=None,
            timeout=10.0,
            lang=None,
            use_unverified_ssl=False,
            websocket_host=None,
            websocket_endpoint=None
    ):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.host = host or "https://api.authing.cn"
        self.timeout = timeout
        self.lang = lang
        self.use_unverified_ssl = use_unverified_ssl
        self.websocket_host = websocket_host or "wss://events.authing.cn"
        self.websocket_endpoint = websocket_endpoint or "/events/v1/management/sub"
        self.http_client = ManagementHttpClient(
            host=self.host,
            lang=self.lang,
            use_unverified_ssl=self.use_unverified_ssl,
            access_key_id=self.access_key_id,
            access_key_secret=self.access_key_secret,
        )

    def list_row(self, model_id, keywords=None, conjunction=None, conditions=None, sort=None, page=None, limit=None,
                 fetch_all=None, with_path=None, show_field_id=None, preview_relation=None,
                 get_relation_field_detail=None, scope=None, filter_relation=None, expand=None):
        """数据对象高级搜索

        数据对象高级搜索

        Attributes:
            model_id (str): 功能 id
            keywords (str): 关键字
            conjunction (str): 多个搜索条件的关系：
    - and: 且
    - or:  或
    
            conditions (list): 搜索条件
            sort (list): 排序条件
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            fetch_all (bool): 是否不分页返回所有（仅支持树形结构获取子节点的场景）
            with_path (bool): 是否返回节点的全路径（仅支持树形结构）
            show_field_id (bool): 返回结果中是否使用字段 id 作为 key
            preview_relation (bool): 返回结果中是包含关联数据的预览（前三个）
            get_relation_field_detail (bool): 是否返回关联数据的详细用户信息，当前只支持用户。
            scope (dict): 限定检索范围为被某个功能关联的部分
            filter_relation (dict): 过滤指定关联数据
            expand (list): 获取对应关联数据的详细字段
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/filter',
            json={
                'modelId': model_id,
                'keywords': keywords,
                'conjunction': conjunction,
                'conditions': conditions,
                'sort': sort,
                'page': page,
                'limit': limit,
                'fetchAll': fetch_all,
                'withPath': with_path,
                'showFieldId': show_field_id,
                'previewRelation': preview_relation,
                'getRelationFieldDetail': get_relation_field_detail,
                'scope': scope,
                'filterRelation': filter_relation,
                'expand': expand,
            },
        )

    def get_row(self, model_id, row_id, show_field_id):
        """获取数据对象行信息

        获取数据对象行信息

        Attributes:
            modelId (str): 功能 id
            rowId (str): 行 id
            showFieldId (str): 返回结果中是否使用字段 id 作为 key
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/metadata/get-row',
            params={
                'modelId': model_id,
                'rowId': row_id,
                'showFieldId': show_field_id,
            },
        )

    def get_row_by_value(self, model_id, key, value, show_field_id):
        """根据属性值获取数据对象行信息

        根据属性值获取数据对象行信息，只允许通过唯一性字段进行精确查询。

        Attributes:
            modelId (str): 功能 id
            key (str): 字段 key
            value (str): 字段值
            showFieldId (str): 返回结果中是否使用字段 id 作为 key
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/metadata/get-row-by-value',
            params={
                'modelId': model_id,
                'key': key,
                'value': value,
                'showFieldId': show_field_id,
            },
        )

    def get_row_batch(self, row_ids, model_id):
        """批量获取行信息

        批量获取行信息

        Attributes:
            row_ids (list): 行 id 列表
            model_id (str): 功能 id
        """
        return self.http_client.request(
            method='POST',
            url='/get-row-batch',
            json={
                'rowIds': row_ids,
                'modelId': model_id,
            },
        )

    def create_row(self, data, model_id, row_id=None):
        """添加行

        添加行

        Attributes:
            data (dict): 数据内容
            model_id (str): 功能 id
            row_id (str): 自定义行 id，默认自动生成。最长只允许 32 位。
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/create-row',
            json={
                'data': data,
                'modelId': model_id,
                'rowId': row_id,
            },
        )

    def update_row(self, data, row_id, model_id, show_field_id=None):
        """更新行

        更新行

        Attributes:
            data (dict): 数据内容
            row_id (str): 行 id
            model_id (str): 功能 id
            show_field_id (bool): 响应中键是否为 FieldId
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/update-row',
            json={
                'data': data,
                'rowId': row_id,
                'modelId': model_id,
                'showFieldId': show_field_id,
            },
        )

    def remove_row(self, row_id_list, model_id, recursive=None):
        """删除行

        删除行

        Attributes:
            row_id_list (list): 行 id
            model_id (str): 功能 id
            recursive (bool): 如果当前行有子节点，是否递归删除，默认为 false。当为 false 时，如果有子节点，会提示错误。
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/remove-row',
            json={
                'rowIdList': row_id_list,
                'modelId': model_id,
                'recursive': recursive,
            },
        )

    def create_model(self, parent_key, enable, type, description, name, data_type=None):
        """创建数据对象

        利用此接口可以创建一个自定义的数据对象，定义数据对象的基本信息

        Attributes:
            parent_key (str): 父级菜单
            enable (bool): 功能是否启用:
    - true: 启用
    - false: 不启用
    
            type (str): 功能类型：
    - user: 用户
    - post: 岗位
    - group: 用户组
    - ueba: ueba
    - department: 树状结构数据
    - organization: 组织
    - device: 设备
    - custom: 自定义
    
            description (str): 功能描述
            name (str): 功能名称
            data_type (str): 数据类型：
    - list: 列表类型数据
    - tree: 树状结构数据
    
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/create-model',
            json={
                'parentKey': parent_key,
                'enable': enable,
                'type': type,
                'description': description,
                'name': name,
                'dataType': data_type,
            },
        )

    def get_model(self, id):
        """获取数据对象详情

        利用功能 id ，获取数据对象的详细信息

        Attributes:
            id (str): 功能 id 可以从控制台页面获取
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/metadata/get-model',
            params={
                'id': id,
            },
        )

    def list_model(self, ):
        """获取数据对象列表

        获取数据对象列表

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/metadata/list-model',
        )

    def remove_model(self, id):
        """删除数据对象

        根据请求的功能 id ，删除对应的数据对象

        Attributes:
            id (str): 功能 id 可以从控制台页面获取
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/remove-model',
            json={
                'id': id,
            },
        )

    def update_model(self, config, field_order, type, parent_key, enable, description, name, id):
        """更新数据对象

        更新对应功能 id 的数据对象信息

        Attributes:
            config (dict): 详情页配置
            field_order (str): 字段序
            type (str): 功能类型
            parent_key (str): 父级菜单
            enable (bool): 功能是否启用
            description (str): 功能描述
            name (str): 功能名称
            id (str): 功能 id
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/update-model',
            json={
                'config': config,
                'fieldOrder': field_order,
                'type': type,
                'parentKey': parent_key,
                'enable': enable,
                'description': description,
                'name': name,
                'id': id,
            },
        )

    def create_field(self, user_visible, relation_optional_range, relation_show_key, relation_multiple, relation_type,
                     for_login, fuzzy_search, drop_down, format, regexp, min, max, max_length, unique, require, default,
                     help, editable, show, type, key, name, model_id):
        """创建数据对象的字段

        创建相关数据对象的字段，配置字段信息及基本校验规则

        Attributes:
            user_visible (bool): 用户中心是否显示，仅在 user 模块下有意义:
    - true: 用户中心展示
    - false: 用户中心不展示
    
            relation_optional_range (dict): 关联数据可选范围
            relation_show_key (str): 关联数据要展示的属性
            relation_multiple (bool): 关联关系是否为 1-N:
    - true: 是 1-N 的关系
    - false: 不是 1-N 的关系
    
            relation_type (str): 关联类型
            for_login (bool): 是否可用于登录，仅在 user 模块下有意义:
    - true: 用于登录
    - false: 不用于登录
    
            fuzzy_search (bool): 是否支持模糊搜索:
    - true: 支持模糊搜索
    - false: 不支持模糊搜索
    
            drop_down (dict): 下拉菜单选项
            format (int): 前端格式化显示规则:
            regexp (str): 字符串的校验匹配规则
            min (int): 如果类型是数字表示数字下限，如果类型是日期表示开始日期
            max (int): 如果类型是数字表示数字上限，如果类型是日期表示结束日期
            max_length (int): 字符串长度限制
            unique (bool): 是否唯一:
    - true: 唯一
    - false: 不唯一
    
            require (bool): 是否必填:
    - true: 必填
    - false: 不必填
    
            default (dict): 默认值
            help (str): 帮助说明
            editable (bool): 是否可编辑:
    - true: 可编辑
    - false: 不可编辑
    
            show (bool): 是否展示:
    - true: 展示
    - false: 不展示
    
            type (str): 字段类型:
    - 1: 单行文本
    - 2: 多行文本
    - 3: 数字
    - 4: 布尔类型
    - 5: 日期
    - 6: 枚举
    - 7: 关联类型
    - 8: 反向关联数据展示
    
            key (str): 字段属性名
            name (str): 字段名称
            model_id (str): 功能 id
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/create-field',
            json={
                'userVisible': user_visible,
                'relationOptionalRange': relation_optional_range,
                'relationShowKey': relation_show_key,
                'relationMultiple': relation_multiple,
                'relationType': relation_type,
                'forLogin': for_login,
                'fuzzySearch': fuzzy_search,
                'dropDown': drop_down,
                'format': format,
                'regexp': regexp,
                'min': min,
                'max': max,
                'maxLength': max_length,
                'unique': unique,
                'require': require,
                'default': default,
                'help': help,
                'editable': editable,
                'show': show,
                'type': type,
                'key': key,
                'name': name,
                'modelId': model_id,
            },
        )

    def update_field(self, user_visible, relation_optional_range, relation_show_key, for_login, fuzzy_search, drop_down,
                     format, regexp, min, max, max_length, unique, require, default, help, editable, show, name,
                     model_id, id):
        """更新数据对象的字段

        更新相关数据对象的字段信息及基本校验规则

        Attributes:
            user_visible (bool): 用户中心是否显示，仅在 user 模块下有意义:
    - true: 用户中心展示
    - false: 用户中心不展示
    
            relation_optional_range (dict): 关联数据可选范围
            relation_show_key (str): 关联数据要展示的属性
            for_login (bool): 是否可用于登录，仅在 user 模块下有意义:
    - true: 用于登录
    - false: 不用于登录
    
            fuzzy_search (bool): 是否支持模糊搜索:
    - true: 支持模糊搜索
    - false: 不支持模糊搜索
    
            drop_down (list): 下拉菜单选项
            format (int): 前端格式化规则
            regexp (str): 字符串的校验匹配规则
            min (int): 如果类型是数字表示数字下限，如果类型是日期表示开始日期
            max (int): 如果类型是数字表示数字上限，如果类型是日期表示结束日期
            max_length (int): 字符串长度限制
            unique (bool): 是否唯一:
    - true: 唯一
    - false: 不唯一
    
            require (bool): 是否必填:
    - true: 必填
    - false: 不必填
    
            default (dict): 默认值
            help (str): 帮助说明
            editable (bool): 是否可编辑:
    - true: 可编辑
    - false: 不可编辑
    
            show (bool): 是否展示:
    - true: 展示
    - false: 不展示
    
            name (str): 字段名称
            model_id (str): 功能 id
            id (str): 字段 id
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/update-field',
            json={
                'userVisible': user_visible,
                'relationOptionalRange': relation_optional_range,
                'relationShowKey': relation_show_key,
                'forLogin': for_login,
                'fuzzySearch': fuzzy_search,
                'dropDown': drop_down,
                'format': format,
                'regexp': regexp,
                'min': min,
                'max': max,
                'maxLength': max_length,
                'unique': unique,
                'require': require,
                'default': default,
                'help': help,
                'editable': editable,
                'show': show,
                'name': name,
                'modelId': model_id,
                'id': id,
            },
        )

    def remote_field(self, model_id, id):
        """删除数据对象的字段

        根据功能字段 id 、功能 id 、字段属性名删除对应的字段

        Attributes:
            model_id (str): 功能 id
            id (str): 功能字段 id
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/remove-field',
            json={
                'modelId': model_id,
                'id': id,
            },
        )

    def list_field(self, model_id):
        """获取数据对象字段列表

        获取数据对象字段列表

        Attributes:
            modelId (str): 功能 id
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/metadata/list-field',
            params={
                'modelId': model_id,
            },
        )

    def export_meatdata(self, id_list, model_id):
        """导出全部数据

        导出全部数据

        Attributes:
            id_list (list): 导出范围
            model_id (str): 功能 id
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/export',
            json={
                'idList': id_list,
                'modelId': model_id,
            },
        )

    def import_metadata(self, file, model_id):
        """导入数据

        导入数据

        Attributes:
            file (str): 导入的 excel 文件地址
            model_id (str): 功能 id
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/import',
            json={
                'file': file,
                'modelId': model_id,
            },
        )

    def get_import_template(self, model_id):
        """获取导入模板

        获取导入模板

        Attributes:
            modelId (str): 功能 id
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/metadata/get-import-template',
            params={
                'modelId': model_id,
            },
        )

    def create_operate(self, show, icon, config, operate_name, operate_key, model_id):
        """创建自定义操作

        创建自定义操作

        Attributes:
            show (bool): 是否展示:
    - true: 展示
    - true: 不展示
    
            icon (str): 图标
            config (dict): 操作配置
            operate_name (str): 操作名称
            operate_key (str): 操作类型:
    - openPage: 打开一个网页
    
            model_id (str): modelId
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/create-operate',
            json={
                'show': show,
                'icon': icon,
                'config': config,
                'operateName': operate_name,
                'operateKey': operate_key,
                'modelId': model_id,
            },
        )

    def remove_operate(self, custom_config, model_id, id):
        """移除自定义操作

        移除自定义操作

        Attributes:
            custom_config (dict): 执行时自定义参数
            model_id (str): 功能 id
            id (str): 自定义操作 id
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/remove-operate',
            json={
                'customConfig': custom_config,
                'modelId': model_id,
                'id': id,
            },
        )

    def execute_operate(self, custom_config, model_id, id):
        """执行自定义操作

        执行自定义操作

        Attributes:
            custom_config (dict): 执行时自定义参数
            model_id (str): 功能 id
            id (str): 自定义操作 id
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/execute-operate',
            json={
                'customConfig': custom_config,
                'modelId': model_id,
                'id': id,
            },
        )

    def copy_operate(self, custom_config, model_id, id):
        """复制自定义操作

        复制自定义操作

        Attributes:
            custom_config (dict): 执行时自定义参数
            model_id (str): 功能 id
            id (str): 自定义操作 id
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/copy-operate',
            json={
                'customConfig': custom_config,
                'modelId': model_id,
                'id': id,
            },
        )

    def list_operate(self, model_id, keywords=None, page=None, limit=None):
        """操作管理列表(分页)

        操作管理列表(分页)

        Attributes:
            modelId (str): model Id
            keywords (str): 搜索功能名称
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/metadata/list-operate',
            params={
                'keywords': keywords,
                'modelId': model_id,
                'page': page,
                'limit': limit,
            },
        )

    def list_operate_all(self, model_id):
        """全部操作管理列表

        全部操作管理列表

        Attributes:
            modelId (str): model Id
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/metadata/all-operate',
            params={
                'modelId': model_id,
            },
        )

    def update_operate(self, icon, config, operate_name, operate_key, show, model_id, id):
        """更新操作管理

        更新操作管理

        Attributes:
            icon (str): 图标
            config (dict): 操作配置
            operate_name (str): 操作名称
            operate_key (str): 操作 Key 值
            show (bool): 是否展示:
    - true: 展示
    - true: 不展示
    
            model_id (str): modelId
            id (str): id
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/update-operate',
            json={
                'icon': icon,
                'config': config,
                'operateName': operate_name,
                'operateKey': operate_key,
                'show': show,
                'modelId': model_id,
                'id': id,
            },
        )

    def get_relation_info(self, id_list, model_id):
        """获取关联数据详情

        获取关联数据详情

        Attributes:
            id_list (list): 关联 id 列表
            model_id (str): 功能 id
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/get-relation-info',
            json={
                'idList': id_list,
                'modelId': model_id,
            },
        )

    def create_row_relation(self, value_list, row_id, field_id, model_id):
        """创建行关联数据

        创建行关联数据

        Attributes:
            value_list (list): 关联数据
            row_id (str): 行 id
            field_id (str): 字段 id
            model_id (str): 功能 id
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/create-row-relation',
            json={
                'valueList': value_list,
                'rowId': row_id,
                'fieldId': field_id,
                'modelId': model_id,
            },
        )

    def get_relation_value(self, model_id, field_id, row_id, page=None, limit=None):
        """获取行关联数据

        获取行关联数据

        Attributes:
            modelId (str): 功能 id
            fieldId (str): 字段 id
            rowId (str): 行 id
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/metadata/get-row-relation',
            params={
                'modelId': model_id,
                'fieldId': field_id,
                'rowId': row_id,
                'page': page,
                'limit': limit,
            },
        )

    def remove_relation_value(self, value, field_ids, row_id, model_id):
        """删除行关联数据

        删除行关联数据

        Attributes:
            value (str): 关联数据
            field_ids (list): 字段 id
            row_id (str): 行 id
            model_id (str): 功能 id
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/remove-row-relation',
            json={
                'value': value,
                'fieldIds': field_ids,
                'rowId': row_id,
                'modelId': model_id,
            },
        )

    def export_model(self, model_id):
        """导出数据对象

        导出数据对象

        Attributes:
            model_id (str): 功能 id
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/export/model',
            json={
                'modelId': model_id,
            },
        )

    def import_model(self, file):
        """导入数据对象

        导入数据对象

        Attributes:
            file (str): 导入的 json 文件地址
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/import/model',
            json={
                'file': file,
            },
        )

    def capture(self, data, model_id=None):
        """UEBA 上传

        UEBA 上传

        Attributes:
            data (dict): 数据内容
            model_id (str): 功能 id，如果不存在则会使用数据库中查到的第一个 type 为 ueba 的功能
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/metadata/ueba/capture',
            json={
                'data': data,
                'modelId': model_id,
            },
        )

    def post_list(self, keywords=None, skip_count=None, page=None, limit=None, with_metadata=None,
                  with_custom_data=None, flat_custom_data=None):
        """岗位列表

        岗位列表

        Attributes:
            keywords (str): 搜索岗位 code 或名称
            skipCount (bool): 是否统计岗位关联的部门数和用户数
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            withMetadata (bool): 是否展示元数据内容
            withCustomData (bool): 是否获取自定义数据
            flatCustomData (bool): 是否拍平扩展字段
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-post',
            params={
                'keywords': keywords,
                'skipCount': skip_count,
                'page': page,
                'limit': limit,
                'withMetadata': with_metadata,
                'withCustomData': with_custom_data,
                'flatCustomData': flat_custom_data,
            },
        )

    def get_post(self, code, with_custom_data=None):
        """获取岗位

        获取岗位

        Attributes:
            code (str): 岗位 code
            withCustomData (bool): 是否获取自定义数据
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-post',
            params={
                'code': code,
                'withCustomData': with_custom_data,
            },
        )

    def get_user_posts(self, user_id, with_custom_data=None):
        """获取用户关联岗位

        获取用户关联的所有岗位

        Attributes:
            userId (str): 用户 id
            withCustomData (bool): 是否获取自定义数据
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-posts',
            params={
                'userId': user_id,
                'withCustomData': with_custom_data,
            },
        )

    def get_user_post(self, user_id, with_custom_data=None):
        """获取用户关联岗位

        此接口只会返回一个岗位，已废弃，请使用 /api/v3/get-user-posts 接口

        Attributes:
            userId (str): 用户 id
            withCustomData (bool): 是否获取自定义数据
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-post',
            params={
                'userId': user_id,
                'withCustomData': with_custom_data,
            },
        )

    def get_post_by_id(self, id_list=None, with_custom_data=None):
        """获取岗位信息

        根据岗位 id 获取岗位详情

        Attributes:
            id_list (str): 部门 id 列表
            with_custom_data (bool): 是否获取自定义数据
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-post-by-id',
            json={
                'idList': id_list,
                'withCustomData': with_custom_data,
            },
        )

    def create_post(self, code, name, description=None, department_id_list=None):
        """创建岗位

        创建岗位

        Attributes:
            code (str): 分组 code
            name (str): 分组名称
            description (str): 分组描述
            department_id_list (str): 部门 id 列表
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-post',
            json={
                'code': code,
                'name': name,
                'description': description,
                'departmentIdList': department_id_list,
            },
        )

    def update_post(self, code, name, description=None, department_id_list=None):
        """更新岗位信息

        更新岗位信息

        Attributes:
            code (str): 分组 code
            name (str): 分组名称
            description (str): 分组描述
            department_id_list (str): 部门 id 列表
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-post',
            json={
                'code': code,
                'name': name,
                'description': description,
                'departmentIdList': department_id_list,
            },
        )

    def remove_post(self, code):
        """删除岗位

        删除岗位

        Attributes:
            code (str): 分组 code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/remove-post',
            json={
                'code': code,
            },
        )

    def set_user_posts(self, post_ids, user_id):
        """用户设置岗位

        一次性给用户设置岗位：如果之前的岗位不在传入的列表中，会进行移除；如果有新增的岗位，会加入到新的岗位；如果不变，则不进行任何操作。

        Attributes:
            post_ids (list): 岗位 id 列表
            user_id (str): 用户 id
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/set-user-posts',
            json={
                'postIds': post_ids,
                'userId': user_id,
            },
        )

    def user_connection_post(self, user_id, post_id):
        """用户关联岗位

        用户关联岗位

        Attributes:
            user_id (str): 用户 id
            post_id (str): 部门 id
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/user-connection-post',
            json={
                'userId': user_id,
                'postId': post_id,
            },
        )

    def delete_device(self, user_id, id):
        """移除绑定(用户详情页)

        移除绑定(用户详情页)。

        Attributes:
            user_id (str): 用户 ID
            id (str): 数据行 id，创建设备时返回的 `id`
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-device-by-user',
            json={
                'userId': user_id,
                'id': id,
            },
        )

    def suspend_device(self, end_time, user_id, id):
        """挂起设备(用户详情页)

        挂起设备(用户详情页)。

        Attributes:
            end_time (str): 挂起到期时间，时间戳(毫秒)
            user_id (str): 用户 ID
            id (str): 数据行 id，创建设备时返回的 `id`
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/suspend-device-by-user',
            json={
                'endTime': end_time,
                'userId': user_id,
                'id': id,
            },
        )

    def disable_device(self, id, user_id):
        """停用设备(用户详情页)

        停用设备(用户详情页)。

        Attributes:
            id (str): 数据行 id，创建设备时返回的 `id`
            user_id (str): 用户 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/disable-device-by-user',
            json={
                'id': id,
                'userId': user_id,
            },
        )

    def enable_device(self, id, user_id):
        """启用设备(用户详情页)

        启用设备(用户详情页)。

        Attributes:
            id (str): 数据行 id，创建设备时返回的 `id`
            user_id (str): 用户 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/enable-device-by-user',
            json={
                'id': id,
                'userId': user_id,
            },
        )

    def get_device_status(self, id):
        """获取设备状态

        获取设备状态。

        Attributes:
            id (str): 数据行 id，创建设备时返回的 `id`
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/device-status',
            json={
                'id': id,
            },
        )

    def list_public_accounts(self, keywords=None, advanced_filter=None, search_query=None, options=None):
        """获取/搜索公共账号列表

        
此接口用于获取用户列表，支持模糊搜索，以及通过用户基础字段、用户自定义字段、用户所在部门、用户历史登录应用等维度筛选用户。

### 模糊搜素示例

模糊搜索默认会从 `phone`, `email`, `name`, `username`, `nickname` 五个字段对用户进行模糊搜索，你也可以通过设置 `options.fuzzySearchOn`
决定模糊匹配的字段范围：

```json
{
  "keywords": "北京",
  "options": {
    "fuzzySearchOn": [
      "address"
    ]
  }
}
```

### 高级搜索示例

你可以通过 `advancedFilter` 进行高级搜索，高级搜索支持通过用户的基础信息、自定义数据、所在部门、用户来源、登录应用、外部身份源信息等维度对用户进行筛选。
**且这些筛选条件可以任意组合。**

#### 筛选状态为禁用的用户

用户状态（`status`）为字符串类型，可选值为 `Activated` 和 `Suspended`： 

```json
{
  "advancedFilter": [
    {
      "field": "status",
      "operator": "EQUAL",
      "value": "Suspended"
    }
  ]
}
```

#### 筛选邮箱中包含 `@example.com` 的用户

用户邮箱（`email`）为字符串类型，可以进行模糊搜索：

```json
{
  "advancedFilter": [
    {
      "field": "email",
      "operator": "CONTAINS",
      "value": "@example.com"
    }
  ]
}
```

#### 根据用户的任意扩展字段进行搜索

```json
{
  "advancedFilter": [
    {
      "field": "some-custom-key",
      "operator": "EQUAL",
      "value": "some-value"
    }
  ]
}
```

#### 根据用户登录次数筛选

筛选登录次数大于 10 的用户：

```json
{
  "advancedFilter": [
    {
      "field": "loginsCount",
      "operator": "GREATER",
      "value": 10
    }
  ]
}
```

筛选登录次数在 10 - 100 次的用户：

```json
{
  "advancedFilter": [
    {
      "field": "loginsCount",
      "operator": "BETWEEN",
      "value": [10, 100]
    }
  ]
}
```

#### 根据用户上次登录时间进行筛选

筛选最近 7 天内登录过的用户：

```json
{
  "advancedFilter": [
    {
      "field": "lastLoginTime",
      "operator": "GREATER",
      "value": new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)
    }
  ]
}
```

筛选在某一段时间内登录过的用户：

```json
{
  "advancedFilter": [
    {
      "field": "lastLogin",
      "operator": "BETWEEN",
      "value": [
        Date.now() - 14 * 24 * 60 * 60 * 1000,
        Date.now() - 7 * 24 * 60 * 60 * 1000
      ]
    }
  ]
}
```

#### 根据用户曾经登录过的应用筛选

筛选出曾经登录过应用 `appId1` 或者 `appId2` 的用户：

```json
{
  "advancedFilter": [
    {
      "field": "loggedInApps",
      "operator": "IN",
      "value": [
        "appId1",
        "appId2"
      ]
    }
  ]
}
```

#### 根据用户所在部门进行筛选

```json
{
  "advancedFilter": [
    {
      "field": "department",
      "operator": "IN",
      "value": [
        {
          "organizationCode": "steamory",
          "departmentId": "root",
          "departmentIdType": "department_id",
          "includeChildrenDepartments": true
        }
      ]
    }
  ]
}
```

  

        Attributes:
            keywords (str): 模糊搜索关键字
            advanced_filter (list): 高级搜索
            search_query (dict): 使用 ES 查询语句执行搜索命令
            options (dict): 可选项
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/list-public-accounts',
            json={
                'keywords': keywords,
                'advancedFilter': advanced_filter,
                'searchQuery': search_query,
                'options': options,
            },
        )

    def get_public_account(self, user_id, user_id_type=None, with_custom_data=None, with_department_ids=None):
        """获取公共账号信息

        通过公共账号用户 ID，获取公共账号详情，可以选择获取自定义数据、选择指定用户 ID 类型等。

        Attributes:
            userId (str): 公共账号用户 ID
            userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
- `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
- `phone`: 用户手机号
- `email`: 用户邮箱
- `username`: 用户名
- `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段

            withCustomData (bool): 是否获取自定义数据
            withDepartmentIds (bool): 是否获取部门 ID 列表
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-public-account',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
                'withCustomData': with_custom_data,
                'withDepartmentIds': with_department_ids,
            },
        )

    def get_public_account_batch(self, user_ids, user_id_type=None, with_custom_data=None, with_department_ids=None):
        """批量获取公共账号信息

        通过公共账号用户 ID 列表，批量获取公共账号信息，可以选择获取自定义数据、选择指定用户 ID 类型等。

        Attributes:
            userIds (str): 公共账号用户 ID 数组
            userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
- `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
- `phone`: 用户手机号
- `email`: 用户邮箱
- `username`: 用户名
- `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段

            withCustomData (bool): 是否获取自定义数据
            withDepartmentIds (bool): 是否获取部门 ID 列表
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-public-account-batch',
            params={
                'userIds': user_ids,
                'userIdType': user_id_type,
                'withCustomData': with_custom_data,
                'withDepartmentIds': with_department_ids,
            },
        )

    def create_public_account(self, status=None, email=None, phone=None, phone_country_code=None, username=None,
                              external_id=None, name=None, nickname=None, photo=None, gender=None, email_verified=None,
                              phone_verified=None, birthdate=None, country=None, province=None, city=None, address=None,
                              street_address=None, postal_code=None, company=None, browser=None, device=None,
                              given_name=None, family_name=None, middle_name=None, profile=None,
                              preferred_username=None, website=None, zoneinfo=None, locale=None, formatted=None,
                              region=None, password=None, salt=None, otp=None, department_ids=None, custom_data=None,
                              identity_number=None, options=None):
        """创建公共账号

        创建公共账号，邮箱、手机号、用户名必须包含其中一个，邮箱、手机号、用户名、externalId 用户池内唯一，此接口将以管理员身份创建公共账号用户因此不需要进行手机号验证码检验等安全检测。  

        Attributes:
            status (str): 账户当前状态
            email (str): 邮箱，不区分大小写
            phone (str): 手机号，不带区号。如果是国外手机号，请在 phoneCountryCode 参数中指定区号。
            phone_country_code (str): 手机区号，中国大陆手机号可不填。Authing 短信服务暂不内置支持国际手机号，你需要在 Authing 控制台配置对应的国际短信服务。完整的手机区号列表可参阅 https://en.wikipedia.org/wiki/List_of_country_calling_codes。
            username (str): 用户名，用户池内唯一
            external_id (str): 第三方外部 ID
            name (str): 用户真实名称，不具备唯一性
            nickname (str): 昵称
            photo (str): 头像链接
            gender (str): 性别
            email_verified (bool): 邮箱是否验证
            phone_verified (bool): 手机号是否验证
            birthdate (str): 出生日期
            country (str): 所在国家
            province (str): 所在省份
            city (str): 所在城市
            address (str): 所处地址
            street_address (str): 所处街道地址
            postal_code (str): 邮政编码号
            company (str): 所在公司
            browser (str): 最近一次登录时使用的浏览器 UA
            device (str): 最近一次登录时使用的设备
            given_name (str): 名
            family_name (str): 姓
            middle_name (str): 中间名
            profile (str): Preferred Username
            preferred_username (str): Preferred Username
            website (str): 用户个人网页
            zoneinfo (str): 用户时区信息
            locale (str): Locale
            formatted (str): 标准的完整地址
            region (str): 用户所在区域
            password (str): 用户密码，默认为明文。我们使用 HTTPS 协议对密码进行安全传输，可以在一定程度上保证安全性。如果你还需要更高级别的安全性，我们还支持 RSA256 和国密 SM2 两种方式对密码进行加密。详情见 `passwordEncryptType` 参数。
            salt (str): 加密用户密码的盐
            otp (dict): 公共账号的 OTP 验证器
            department_ids (list): 用户所属部门 ID 列表
            custom_data (dict): 自定义数据，传入的对象中的 key 必须先在用户池定义相关自定义字段
            identity_number (str): 用户身份证号码
            options (dict): 可选参数
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-public-account',
            json={
                'status': status,
                'email': email,
                'phone': phone,
                'phoneCountryCode': phone_country_code,
                'username': username,
                'externalId': external_id,
                'name': name,
                'nickname': nickname,
                'photo': photo,
                'gender': gender,
                'emailVerified': email_verified,
                'phoneVerified': phone_verified,
                'birthdate': birthdate,
                'country': country,
                'province': province,
                'city': city,
                'address': address,
                'streetAddress': street_address,
                'postalCode': postal_code,
                'company': company,
                'browser': browser,
                'device': device,
                'givenName': given_name,
                'familyName': family_name,
                'middleName': middle_name,
                'profile': profile,
                'preferredUsername': preferred_username,
                'website': website,
                'zoneinfo': zoneinfo,
                'locale': locale,
                'formatted': formatted,
                'region': region,
                'password': password,
                'salt': salt,
                'otp': otp,
                'departmentIds': department_ids,
                'customData': custom_data,
                'identityNumber': identity_number,
                'options': options,
            },
        )

    def create_public_accounts_batch(self, list, options=None):
        """批量创建公共账号

        批量创建公共账号，邮箱、手机号、用户名必须包含其中一个，邮箱、手机号、用户名、externalId 用户池内唯一，此接口将以管理员身份创建公共账号用户因此不需要进行手机号验证码检验等安全检测。

        Attributes:
            list (list): 公共账号列表
            options (dict): 可选参数
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-public-accounts-batch',
            json={
                'list': list,
                'options': options,
            },
        )

    def update_public_account(self, user_id, phone_country_code=None, name=None, nickname=None, photo=None,
                              external_id=None, status=None, email_verified=None, phone_verified=None, birthdate=None,
                              country=None, province=None, city=None, address=None, street_address=None,
                              postal_code=None, gender=None, username=None, email=None, phone=None, password=None,
                              company=None, browser=None, device=None, given_name=None, family_name=None,
                              middle_name=None, profile=None, preferred_username=None, website=None, zoneinfo=None,
                              locale=None, formatted=None, region=None, identity_number=None, custom_data=None,
                              options=None):
        """修改公共账号资料

        通过公共账号用户 ID，修改公共账号资料，邮箱、手机号、用户名、externalId 用户池内唯一，此接口将以管理员身份修改公共账号资料因此不需要进行手机号验证码检验等安全检测。

        Attributes:
            user_id (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            phone_country_code (str): 手机区号，中国大陆手机号可不填。Authing 短信服务暂不内置支持国际手机号，你需要在 Authing 控制台配置对应的国际短信服务。完整的手机区号列表可参阅 https://en.wikipedia.org/wiki/List_of_country_calling_codes。
            name (str): 用户真实名称，不具备唯一性
            nickname (str): 昵称
            photo (str): 头像链接
            external_id (str): 第三方外部 ID
            status (str): 账户当前状态
            email_verified (bool): 邮箱是否验证
            phone_verified (bool): 手机号是否验证
            birthdate (str): 出生日期
            country (str): 所在国家
            province (str): 所在省份
            city (str): 所在城市
            address (str): 所处地址
            street_address (str): 所处街道地址
            postal_code (str): 邮政编码号
            gender (str): 性别
            username (str): 用户名，用户池内唯一
            email (str): 邮箱，不区分大小写
            phone (str): 手机号，不带区号。如果是国外手机号，请在 phoneCountryCode 参数中指定区号。
            password (str): 用户密码，默认为明文。我们使用 HTTPS 协议对密码进行安全传输，可以在一定程度上保证安全性。如果你还需要更高级别的安全性，我们还支持 RSA256 和国密 SM2 两种方式对密码进行加密。详情见 `passwordEncryptType` 参数。
            company (str): 所在公司
            browser (str): 最近一次登录时使用的浏览器 UA
            device (str): 最近一次登录时使用的设备
            given_name (str): 名
            family_name (str): 姓
            middle_name (str): 中间名
            profile (str): Preferred Username
            preferred_username (str): Preferred Username
            website (str): 用户个人网页
            zoneinfo (str): 用户时区信息
            locale (str): Locale
            formatted (str): 标准的完整地址
            region (str): 用户所在区域
            identity_number (str): 用户身份证号码
            custom_data (dict): 自定义数据，传入的对象中的 key 必须先在用户池定义相关自定义字段
            options (dict): 可选参数
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-public-account',
            json={
                'userId': user_id,
                'phoneCountryCode': phone_country_code,
                'name': name,
                'nickname': nickname,
                'photo': photo,
                'externalId': external_id,
                'status': status,
                'emailVerified': email_verified,
                'phoneVerified': phone_verified,
                'birthdate': birthdate,
                'country': country,
                'province': province,
                'city': city,
                'address': address,
                'streetAddress': street_address,
                'postalCode': postal_code,
                'gender': gender,
                'username': username,
                'email': email,
                'phone': phone,
                'password': password,
                'company': company,
                'browser': browser,
                'device': device,
                'givenName': given_name,
                'familyName': family_name,
                'middleName': middle_name,
                'profile': profile,
                'preferredUsername': preferred_username,
                'website': website,
                'zoneinfo': zoneinfo,
                'locale': locale,
                'formatted': formatted,
                'region': region,
                'identityNumber': identity_number,
                'customData': custom_data,
                'options': options,
            },
        )

    def update_public_account_batch(self, list, options=None):
        """批量修改公共账号资料

        批量修改公共账号资料，邮箱、手机号、用户名、externalId 用户池内唯一，此接口将以管理员身份修改公共账号资料因此不需要进行手机号验证码检验等安全检测。

        Attributes:
            list (list): 公共账号列表
            options (dict): 可选参数
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-public-account-batch',
            json={
                'list': list,
                'options': options,
            },
        )

    def delete_public_accounts_batch(self, user_ids, options=None):
        """批量删除公共账号

        通过公共账号 ID 列表，删除公共账号，支持批量删除，可以选择指定用户 ID 类型等。

        Attributes:
            user_ids (list): 公共账号用户 ID 列表
            options (dict): 可选参数
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-public-accounts-batch',
            json={
                'userIds': user_ids,
                'options': options,
            },
        )

    def kick_public_accounts(self, app_ids, user_id, options=None):
        """强制下线公共账号

        通过公共账号 ID、App ID 列表，强制让公共账号下线，可以选择指定公共账号 ID 类型等。

        Attributes:
            app_ids (list): APP ID 列表
            user_id (str): 公共账号 ID
            options (dict): 可选参数
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/kick-public-accounts',
            json={
                'appIds': app_ids,
                'userId': user_id,
                'options': options,
            },
        )

    def change_into_public_account(self, user_id):
        """个人账号转换为公共账号

        通过用户 ID，把个人账号转换为公共账号。

        Attributes:
            user_id (str): 公共账号 rowId
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/transfer-into-public-account',
            json={
                'userId': user_id,
            },
        )

    def get_public_accounts_of_user(self, user_id):
        """获取用户的公共账号列表

        通过用户 ID，获取用户的公共账号列表。

        Attributes:
            userId (str): 用户 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-public-accounts-of-user',
            params={
                'userId': user_id,
            },
        )

    def get_users_of_public_account(self, public_account_id):
        """公共账号的用户列表

        通过公共账号 ID，获取用户列表。

        Attributes:
            publicAccountId (str): 公共账号 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-users-of-public-account',
            params={
                'publicAccountId': public_account_id,
            },
        )

    def bind_users_public_account(self, public_account_id, user_ids):
        """公共账号绑定批量用户

        使用公共账号绑定批量用户

        Attributes:
            public_account_id (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            user_ids (list): 用户 ID 数组
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/set-public-account-of-users',
            json={
                'publicAccountId': public_account_id,
                'userIds': user_ids,
            },
        )

    def setuser_of_public_account(self, user_id, public_account_ids):
        """用户绑定批量公共账号

        用户绑定批量公共账号

        Attributes:
            user_id (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            public_account_ids (list): 用户 ID 数组
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/set-user-of-public-accounts',
            json={
                'userId': user_id,
                'publicAccountIds': public_account_ids,
            },
        )

    def unbind_users_public_account(self, user_id, public_account_id):
        """公共账号解绑用户

        公共账号解绑用户

        Attributes:
            user_id (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            public_account_id (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/unbind-public-account-of-user',
            json={
                'userId': user_id,
                'publicAccountId': public_account_id,
            },
        )

    def get_organization(self, organization_code, with_custom_data=None, with_post=None, tenant_id=None):
        """获取组织机构详情

        获取组织机构详情

        Attributes:
            organizationCode (str): 组织 Code（organizationCode）
            withCustomData (bool): 是否获取自定义数据
            withPost (bool): 是否获取 部门信息
            tenantId (str): 租户 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-organization',
            params={
                'organizationCode': organization_code,
                'withCustomData': with_custom_data,
                'withPost': with_post,
                'tenantId': tenant_id,
            },
        )

    def get_organizations_batch(self, organization_code_list, with_custom_data=None, with_post=None, tenant_id=None):
        """批量获取组织机构详情

        批量获取组织机构详情

        Attributes:
            organizationCodeList (str): 组织 Code（organizationCode）列表
            withCustomData (bool): 是否获取自定义数据
            withPost (bool): 是否获取 部门信息
            tenantId (str): 租户 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-organization-batch',
            params={
                'organizationCodeList': organization_code_list,
                'withCustomData': with_custom_data,
                'withPost': with_post,
                'tenantId': tenant_id,
            },
        )

    def list_organizations(self, page=None, limit=None, fetch_all=None, with_custom_data=None, with_post=None,
                           tenant_id=None, status=None):
        """获取组织机构列表

        获取组织机构列表，支持分页。

        Attributes:
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            fetchAll (bool): 拉取所有
            withCustomData (bool): 是否获取自定义数据
            withPost (bool): 是否获取 部门信息
            tenantId (str): 租户 ID
            status (bool): 组织的状态
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-organizations',
            params={
                'page': page,
                'limit': limit,
                'fetchAll': fetch_all,
                'withCustomData': with_custom_data,
                'withPost': with_post,
                'tenantId': tenant_id,
                'status': status,
            },
        )

    def create_organization(self, metadata, organization_name, organization_code, description=None,
                            open_department_id=None, i18n=None, tenant_id=None, post_id_list=None):
        """创建组织机构

        创建组织机构，会创建一个只有一个节点的组织机构，可以选择组织描述信息、根节点自定义 ID、多语言等。

        Attributes:
            metadata (dict): 元数据信息
            organization_name (str): 组织名称
            organization_code (str): 组织 code
            description (str): 组织描述信息
            open_department_id (str): 根节点自定义 ID
            i18n (dict): 多语言设置
            tenant_id (str): 租户 ID
            post_id_list (list): 岗位 id 列表
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-organization',
            json={
                'metadata': metadata,
                'organizationName': organization_name,
                'organizationCode': organization_code,
                'description': description,
                'openDepartmentId': open_department_id,
                'i18n': i18n,
                'tenantId': tenant_id,
                'postIdList': post_id_list,
            },
        )

    def update_organization(self, organization_code, description=None, open_department_id=None, leader_user_ids=None,
                            i18n=None, tenant_id=None, organization_new_code=None, organization_name=None,
                            post_id_list=None):
        """修改组织机构

        通过组织 code，修改组织机构，可以选择部门描述、新组织 code、组织名称等。

        Attributes:
            organization_code (str): 组织 code
            description (str): 部门描述
            open_department_id (str): 根节点自定义 ID
            leader_user_ids (list): 部门负责人 ID
            i18n (dict): 多语言设置
            tenant_id (str): 租户 ID
            organization_new_code (str): 新组织 code
            organization_name (str): 组织名称
            post_id_list (list): 岗位 id 列表
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-organization',
            json={
                'organizationCode': organization_code,
                'description': description,
                'openDepartmentId': open_department_id,
                'leaderUserIds': leader_user_ids,
                'i18n': i18n,
                'tenantId': tenant_id,
                'organizationNewCode': organization_new_code,
                'organizationName': organization_name,
                'postIdList': post_id_list,
            },
        )

    def delete_organization(self, organization_code, tenant_id=None):
        """删除组织机构

        通过组织 code，删除组织机构树。

        Attributes:
            organization_code (str): 组织 code
            tenant_id (str): 租户 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-organization',
            json={
                'organizationCode': organization_code,
                'tenantId': tenant_id,
            },
        )

    def search_organizations(self, keywords, page=None, limit=None, with_custom_data=None, tenant_id=None):
        """搜索组织机构列表

        通过搜索关键词，搜索组织机构列表，支持分页。

        Attributes:
            keywords (str): 搜索关键词，如组织机构名称
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            withCustomData (bool): 是否获取自定义数据
            tenantId (str): 租户 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/search-organizations',
            params={
                'keywords': keywords,
                'page': page,
                'limit': limit,
                'withCustomData': with_custom_data,
                'tenantId': tenant_id,
            },
        )

    def update_organization_status(self, root_node_id, status=None):
        """更新组织机构状态

        

        Attributes:
            root_node_id (str): 组织 id
            status (str): 状态
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-organization-status',
            json={
                'rootNodeId': root_node_id,
                'status': status,
            },
        )

    def get_department(self, organization_code=None, department_id=None, department_code=None, department_id_type=None,
                       with_custom_data=None, flat_custom_data=None, tenant_id=None):
        """获取部门信息

        通过组织 code 以及 部门 ID 或 部门 code，获取部门信息，可以获取自定义数据。

        Attributes:
            organizationCode (str): 组织 code
            departmentId (str): 部门 ID，根部门传 `root`。departmentId 和 departmentCode 必传其一。
            departmentCode (str): 部门 code。departmentId 和 departmentCode 必传其一。
            departmentIdType (str): 此次调用中使用的部门 ID 的类型
            withCustomData (bool): 是否获取自定义数据
            flatCustomData (bool): 是否拍平扩展字段
            tenantId (str): 租户 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-department',
            params={
                'organizationCode': organization_code,
                'departmentId': department_id,
                'departmentCode': department_code,
                'departmentIdType': department_id_type,
                'withCustomData': with_custom_data,
                'flatCustomData': flat_custom_data,
                'tenantId': tenant_id,
            },
        )

    def create_department(self, organization_code, name, parent_department_id, metadata, open_department_id=None,
                          description=None, code=None, is_virtual_node=None, i18n=None, custom_data=None,
                          department_id_type=None, post_id_list=None, tenant_id=None):
        """创建部门

        通过组织 code、部门名称、父部门 ID，创建部门，可以设置多种参数。

        Attributes:
            organization_code (str): 组织 Code（organizationCode）
            name (str): 部门名称
            parent_department_id (str): 父部门 id
            metadata (dict): 元数据信息
            open_department_id (str): 自定义部门 ID，用于存储自定义的 ID
            description (str): 部门描述
            code (str): 部门识别码
            is_virtual_node (bool): 是否是虚拟部门
            i18n (dict): 多语言设置
            custom_data (dict): 部门的扩展字段数据
            department_id_type (str): 此次调用中使用的父部门 ID 的类型
            post_id_list (list): 岗位 id 列表
            tenant_id (str): 租户 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-department',
            json={
                'organizationCode': organization_code,
                'name': name,
                'parentDepartmentId': parent_department_id,
                'metadata': metadata,
                'openDepartmentId': open_department_id,
                'description': description,
                'code': code,
                'isVirtualNode': is_virtual_node,
                'i18n': i18n,
                'customData': custom_data,
                'departmentIdType': department_id_type,
                'postIdList': post_id_list,
                'tenantId': tenant_id,
            },
        )

    def update_department(self, organization_code, department_id, leader_user_ids=None, description=None, code=None,
                          i18n=None, status=None, name=None, department_id_type=None, parent_department_id=None,
                          custom_data=None, post_id_list=None, tenant_id=None):
        """修改部门

        通过组织 code、部门 ID，修改部门，可以设置多种参数。

        Attributes:
            organization_code (str): 组织 Code（organizationCode）
            department_id (str): 部门系统 ID（为 Authing 系统自动生成，不可修改）
            leader_user_ids (list): 部门负责人 ID
            description (str): 部门描述
            code (str): 部门识别码
            i18n (dict): 多语言设置
            status (bool): 部门状态
            name (str): 部门名称
            department_id_type (str): 此次调用中使用的部门 ID 的类型
            parent_department_id (str): 父部门 ID
            custom_data (dict): 自定义数据，传入的对象中的 key 必须先在用户池定义相关自定义字段
            post_id_list (list): 岗位 id 列表
            tenant_id (str): 租户 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-department',
            json={
                'organizationCode': organization_code,
                'departmentId': department_id,
                'leaderUserIds': leader_user_ids,
                'description': description,
                'code': code,
                'i18n': i18n,
                'status': status,
                'name': name,
                'departmentIdType': department_id_type,
                'parentDepartmentId': parent_department_id,
                'customData': custom_data,
                'postIdList': post_id_list,
                'tenantId': tenant_id,
            },
        )

    def delete_department(self, organization_code, department_id, department_id_type=None, tenant_id=None):
        """删除部门

        通过组织 code、部门 ID，删除部门。

        Attributes:
            organization_code (str): 组织 Code（organizationCode）
            department_id (str): 部门系统 ID（为 Authing 系统自动生成，不可修改）
            department_id_type (str): 此次调用中使用的部门 ID 的类型
            tenant_id (str): 租户 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-department',
            json={
                'organizationCode': organization_code,
                'departmentId': department_id,
                'departmentIdType': department_id_type,
                'tenantId': tenant_id,
            },
        )

    def search_departments(self, keywords, organization_code, with_custom_data=None, tenant_id=None):
        """搜索部门

        通过组织 code、搜索关键词，搜索部门，可以搜索组织名称等。

        Attributes:
            keywords (str): 搜索关键词，如组织名称等
            organization_code (str): 组织 code
            with_custom_data (bool): 是否获取自定义数据
            tenant_id (str): 租户 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/search-departments',
            json={
                'keywords': keywords,
                'organizationCode': organization_code,
                'withCustomData': with_custom_data,
                'tenantId': tenant_id,
            },
        )

    def search_departments_list(self, organization_code, with_custom_data=None, with_post=None, page=None, limit=None,
                                advanced_filter=None, sort_by=None, order_by=None, sort=None, tenant_id=None):
        """搜索部门

        通过组织 code、搜索关键词，搜索部门，可以搜索组织名称等。

        Attributes:
            organization_code (str): 组织 code
            with_custom_data (bool): 是否获取自定义数据
            with_post (bool): 是否获取 部门信息
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            advanced_filter (list): 高级搜索
            sort_by (str): 排序依据，如 更新时间或创建时间
            order_by (str): 增序或降序
            sort (list): 排序设置，可以设置多项按照多个字段进行排序
            tenant_id (str): 租户 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/search-departments-list',
            json={
                'organizationCode': organization_code,
                'withCustomData': with_custom_data,
                'withPost': with_post,
                'page': page,
                'limit': limit,
                'advancedFilter': advanced_filter,
                'sortBy': sort_by,
                'orderBy': order_by,
                'sort': sort,
                'tenantId': tenant_id,
            },
        )

    def list_children_departments(self, organization_code, department_id, status=None, department_id_type=None,
                                  exclude_virtual_node=None, only_virtual_node=None, with_custom_data=None,
                                  tenant_id=None):
        """获取子部门列表

        通过组织 code、部门 ID，获取子部门列表，可以选择获取自定义数据、虚拟组织等。

        Attributes:
            organizationCode (str): 组织 code
            departmentId (str): 需要获取的部门 ID
            status (bool): 部门的状态
            departmentIdType (str): 此次调用中使用的部门 ID 的类型
            excludeVirtualNode (bool): 是否要排除虚拟组织
            onlyVirtualNode (bool): 是否只包含虚拟组织
            withCustomData (bool): 是否获取自定义数据
            tenantId (str): 租户 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-children-departments',
            params={
                'organizationCode': organization_code,
                'departmentId': department_id,
                'status': status,
                'departmentIdType': department_id_type,
                'excludeVirtualNode': exclude_virtual_node,
                'onlyVirtualNode': only_virtual_node,
                'withCustomData': with_custom_data,
                'tenantId': tenant_id,
            },
        )

    def get_all_departments(self, organization_code, department_id=None, department_id_type=None,
                            with_custom_data=None):
        """获取所有部门列表

        获取所有部门列表，可以用于获取某个组织下的所有部门列表。

        Attributes:
            organizationCode (str): 组织 code
            departmentId (str): 部门 ID，不填写默认为 `root` 根部门 ID
            departmentIdType (str): 此次调用中使用的部门 ID 的类型
            withCustomData (bool): 是否获取自定义数据
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-all-departments',
            params={
                'organizationCode': organization_code,
                'departmentId': department_id,
                'departmentIdType': department_id_type,
                'withCustomData': with_custom_data,
            },
        )

    def list_department_members(self, organization_code, department_id, sort_by=None, order_by=None,
                                department_id_type=None, include_children_departments=None, page=None, limit=None,
                                with_custom_data=None, with_identities=None, with_department_ids=None, tenant_id=None):
        """获取部门成员列表

        通过组织 code、部门 ID、排序，获取部门成员列表，支持分页，可以选择获取自定义数据、identities 等。

        Attributes:
            organizationCode (str): 组织 code
            departmentId (str): 部门 ID，根部门传 `root`
            sortBy (str): 排序依据
            orderBy (str): 增序还是倒序
            departmentIdType (str): 此次调用中使用的部门 ID 的类型
            includeChildrenDepartments (bool): 是否包含子部门的成员
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            withCustomData (bool): 是否获取自定义数据
            withIdentities (bool): 是否获取 identities
            withDepartmentIds (bool): 是否获取部门 ID 列表
            tenantId (str): 租户 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-department-members',
            params={
                'organizationCode': organization_code,
                'departmentId': department_id,
                'sortBy': sort_by,
                'orderBy': order_by,
                'departmentIdType': department_id_type,
                'includeChildrenDepartments': include_children_departments,
                'page': page,
                'limit': limit,
                'withCustomData': with_custom_data,
                'withIdentities': with_identities,
                'withDepartmentIds': with_department_ids,
                'tenantId': tenant_id,
            },
        )

    def list_department_member_ids(self, organization_code, department_id, department_id_type=None, tenant_id=None):
        """获取部门直属成员 ID 列表

        通过组织 code、部门 ID，获取部门直属成员 ID 列表。

        Attributes:
            organizationCode (str): 组织 code
            departmentId (str): 部门 ID，根部门传 `root`
            departmentIdType (str): 此次调用中使用的部门 ID 的类型
            tenantId (str): 租户 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-department-member-ids',
            params={
                'organizationCode': organization_code,
                'departmentId': department_id,
                'departmentIdType': department_id_type,
                'tenantId': tenant_id,
            },
        )

    def search_department_members(self, organization_code, department_id, keywords, page=None, limit=None,
                                  department_id_type=None, include_children_departments=None, with_custom_data=None,
                                  with_identities=None, with_department_ids=None, tenant_id=None):
        """搜索部门下的成员

        通过组织 code、部门 ID、搜索关键词，搜索部门下的成员，支持分页，可以选择获取自定义数据、identities 等。

        Attributes:
            organizationCode (str): 组织 code
            departmentId (str): 部门 ID，根部门传 `root`
            keywords (str): 搜索关键词，如成员名称
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            departmentIdType (str): 此次调用中使用的部门 ID 的类型
            includeChildrenDepartments (bool): 是否包含子部门的成员
            withCustomData (bool): 是否获取自定义数据
            withIdentities (bool): 是否获取 identities
            withDepartmentIds (bool): 是否获取部门 ID 列表
            tenantId (str): 租户 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/search-department-members',
            params={
                'organizationCode': organization_code,
                'departmentId': department_id,
                'keywords': keywords,
                'page': page,
                'limit': limit,
                'departmentIdType': department_id_type,
                'includeChildrenDepartments': include_children_departments,
                'withCustomData': with_custom_data,
                'withIdentities': with_identities,
                'withDepartmentIds': with_department_ids,
                'tenantId': tenant_id,
            },
        )

    def add_department_members(self, user_ids, organization_code, department_id, department_id_type=None,
                               tenant_id=None):
        """部门下添加成员

        通过部门 ID、组织 code，添加部门下成员。

        Attributes:
            user_ids (list): 用户 ID 列表
            organization_code (str): 组织 code
            department_id (str): 部门系统 ID（为 Authing 系统自动生成，不可修改）
            department_id_type (str): 此次调用中使用的部门 ID 的类型
            tenant_id (str): 租户 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/add-department-members',
            json={
                'userIds': user_ids,
                'organizationCode': organization_code,
                'departmentId': department_id,
                'departmentIdType': department_id_type,
                'tenantId': tenant_id,
            },
        )

    def remove_department_members(self, user_ids, organization_code, department_id, department_id_type=None,
                                  tenant_id=None):
        """部门下删除成员

        通过部门 ID、组织 code，删除部门下成员。

        Attributes:
            user_ids (list): 用户 ID 列表
            organization_code (str): 组织 code
            department_id (str): 部门系统 ID（为 Authing 系统自动生成，不可修改）
            department_id_type (str): 此次调用中使用的部门 ID 的类型
            tenant_id (str): 租户 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/remove-department-members',
            json={
                'userIds': user_ids,
                'organizationCode': organization_code,
                'departmentId': department_id,
                'departmentIdType': department_id_type,
                'tenantId': tenant_id,
            },
        )

    def get_parent_department(self, organization_code, department_id, department_id_type=None, with_custom_data=None,
                              tenant_id=None):
        """获取父部门信息

        通过组织 code、部门 ID，获取父部门信息，可以选择获取自定义数据等。

        Attributes:
            organizationCode (str): 组织 code
            departmentId (str): 部门 ID
            departmentIdType (str): 此次调用中使用的部门 ID 的类型
            withCustomData (bool): 是否获取自定义数据
            tenantId (str): 租户 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-parent-department',
            params={
                'organizationCode': organization_code,
                'departmentId': department_id,
                'departmentIdType': department_id_type,
                'withCustomData': with_custom_data,
                'tenantId': tenant_id,
            },
        )

    def is_user_in_department(self, user_id, organization_code, department_id, department_id_type=None,
                              include_children_departments=None, tenant_id=None):
        """判断用户是否在某个部门下

        通过组织 code、部门 ID，判断用户是否在某个部门下，可以选择包含子部门。

        Attributes:
            userId (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            organizationCode (str): 组织 code
            departmentId (str): 部门 ID，根部门传 `root`。departmentId 和 departmentCode 必传其一。
            departmentIdType (str): 此次调用中使用的部门 ID 的类型
            includeChildrenDepartments (bool): 是否包含子部门
            tenantId (str): 租户 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/is-user-in-department',
            params={
                'userId': user_id,
                'organizationCode': organization_code,
                'departmentId': department_id,
                'departmentIdType': department_id_type,
                'includeChildrenDepartments': include_children_departments,
                'tenantId': tenant_id,
            },
        )

    def get_department_by_id(self, department_id, tenant_id=None, with_custom_data=None):
        """根据部门id查询部门

        根据部门id查询部门

        Attributes:
            departmentId (str): 部门 ID
            tenantId (str): 租户 ID
            withCustomData (bool): 是否获取自定义数据
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-department-by-id',
            params={
                'departmentId': department_id,
                'tenantId': tenant_id,
                'withCustomData': with_custom_data,
            },
        )

    def create_department_tree(self, name, children=None, members=None, tenant_id=None):
        """根据组织树批量创建部门

        根据组织树批量创建部门，部门名称不存在时会自动创建

        Attributes:
            name (str): 部门名称
            children (list): 子部门
            members (dict): 部门成员
            tenant_id (str): 租户 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-department-tree',
            json={
                'name': name,
                'children': children,
                'members': members,
                'tenantId': tenant_id,
            },
        )

    def get_department_sync_relations(self, organization_code, department_id=None, department_id_type=None,
                                      with_custom_data=None, tenant_id=None):
        """获取部门绑定的第三方同步关系

        如果在 Authing 中的部门进行了上下游同步，此接口可以用于查询出在第三方的关联用户信息

        Attributes:
            organizationCode (str): 组织 code
            departmentId (str): 部门 ID，根部门传 `root`。departmentId 和 departmentCode 必传其一。
            departmentIdType (str): 此次调用中使用的部门 ID 的类型
            withCustomData (bool): 是否获取自定义数据
            tenantId (str): 租户 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-department-sync-relations',
            params={
                'organizationCode': organization_code,
                'departmentId': department_id,
                'departmentIdType': department_id_type,
                'withCustomData': with_custom_data,
                'tenantId': tenant_id,
            },
        )

    def delete_department_sync_relations(self, provider, department_id, organization_code, department_id_type=None):
        """删除部门同步关联关系

        如果在 Authing 中的部门进行了上下游同步，此接口可以用于删除某个部门在指定身份源下的关联关系。

        Attributes:
            provider (str): 外部身份源类型，如：
- `wechatwork`: 企业微信
- `dingtalk`: 钉钉
- `lark`: 飞书
- `welink`: Welink
- `ldap`: LDAP
- `active-directory`: Windows AD
- `italent`: 北森
- `xiaoshouyi`: 销售易
- `maycur`: 每刻报销
- `scim`: SCIM
- `moka`: Moka HR
    
            department_id (str): 部门 ID，根部门传 `root`
            organization_code (str): 组织 code
            department_id_type (str): 此次调用中使用的部门 ID 的类型
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-department-sync-relations',
            json={
                'provider': provider,
                'departmentId': department_id,
                'organizationCode': organization_code,
                'departmentIdType': department_id_type,
            },
        )

    def update_node_status(self, status, department_id):
        """更新部门状态

        启用和禁用部门

        Attributes:
            status (bool): 部门状态
            department_id (str): 需要获取的部门 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-department-status',
            json={
                'status': status,
                'departmentId': department_id,
            },
        )

    def list_users(self, keywords=None, advanced_filter=None, search_query=None, options=None):
        """获取/搜索用户列表

        
此接口用于获取用户列表，支持模糊搜索，以及通过用户基础字段、用户自定义字段、用户所在部门、用户历史登录应用等维度筛选用户。

### 模糊搜素示例

模糊搜索默认会从 `phone`, `email`, `name`, `username`, `nickname` 五个字段对用户进行模糊搜索，你也可以通过设置 `options.fuzzySearchOn`
决定模糊匹配的字段范围：

```json
{
  "keywords": "北京",
  "options": {
    "fuzzySearchOn": [
      "address"
    ]
  }
}
```

### 高级搜索示例

你可以通过 `advancedFilter` 进行高级搜索，高级搜索支持通过用户的基础信息、自定义数据、所在部门、用户来源、登录应用、外部身份源信息等维度对用户进行筛选。
**且这些筛选条件可以任意组合。**

#### 筛选状态为禁用的用户

用户状态（`status`）为字符串类型，可选值为 `Activated` 和 `Suspended`： 

```json
{
  "advancedFilter": [
    {
      "field": "status",
      "operator": "EQUAL",
      "value": "Suspended"
    }
  ]
}
```

#### 筛选邮箱中包含 `@example.com` 的用户

用户邮箱（`email`）为字符串类型，可以进行模糊搜索：

```json
{
  "advancedFilter": [
    {
      "field": "email",
      "operator": "CONTAINS",
      "value": "@example.com"
    }
  ]
}
```

#### 根据用户的任意扩展字段进行搜索

```json
{
  "advancedFilter": [
    {
      "field": "some-custom-key",
      "operator": "EQUAL",
      "value": "some-value"
    }
  ]
}
```

#### 根据用户登录次数筛选

筛选登录次数大于 10 的用户：

```json
{
  "advancedFilter": [
    {
      "field": "loginsCount",
      "operator": "GREATER",
      "value": 10
    }
  ]
}
```

筛选登录次数在 10 - 100 次的用户：

```json
{
  "advancedFilter": [
    {
      "field": "loginsCount",
      "operator": "BETWEEN",
      "value": [10, 100]
    }
  ]
}
```

#### 根据用户上次登录时间进行筛选

筛选最近 7 天内登录过的用户：

```json
{
  "advancedFilter": [
    {
      "field": "lastLoginTime",
      "operator": "GREATER",
      "value": new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)
    }
  ]
}
```

筛选在某一段时间内登录过的用户：

```json
{
  "advancedFilter": [
    {
      "field": "lastLogin",
      "operator": "BETWEEN",
      "value": [
        Date.now() - 14 * 24 * 60 * 60 * 1000,
        Date.now() - 7 * 24 * 60 * 60 * 1000
      ]
    }
  ]
}
```

#### 根据用户曾经登录过的应用筛选

筛选出曾经登录过应用 `appId1` 或者 `appId2` 的用户：

```json
{
  "advancedFilter": [
    {
      "field": "loggedInApps",
      "operator": "IN",
      "value": [
        "appId1",
        "appId2"
      ]
    }
  ]
}
```

#### 根据用户所在部门进行筛选

```json
{
  "advancedFilter": [
    {
      "field": "department",
      "operator": "IN",
      "value": [
        {
          "organizationCode": "steamory",
          "departmentId": "root",
          "departmentIdType": "department_id",
          "includeChildrenDepartments": true
        }
      ]
    }
  ]
}
```

  

        Attributes:
            keywords (str): 模糊搜索关键字
            advanced_filter (list): 高级搜索
            search_query (dict): 使用 ES 查询语句执行搜索命令
            options (dict): 可选项
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/list-users',
            json={
                'keywords': keywords,
                'advancedFilter': advanced_filter,
                'searchQuery': search_query,
                'options': options,
            },
        )

    def list_users_legacy(self, page=None, limit=None, status=None, updated_at_start=None, updated_at_end=None,
                          with_custom_data=None, with_post=None, with_identities=None, with_department_ids=None):
        """获取用户列表

        获取用户列表接口，支持分页，可以选择获取自定义数据、identities 等。

        Attributes:
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            status (str): 账户当前状态，如 已停用、已离职、正常状态、已归档
            updatedAtStart (int): 用户创建、修改开始时间，为精确到秒的 UNIX 时间戳；支持获取从某一段时间之后的增量数据
            updatedAtEnd (int): 用户创建、修改终止时间，为精确到秒的 UNIX 时间戳；支持获取某一段时间内的增量数据。默认为当前时间
            withCustomData (bool): 是否获取自定义数据
            withPost (bool): 是否获取 部门信息
            withIdentities (bool): 是否获取 identities
            withDepartmentIds (bool): 是否获取部门 ID 列表
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-users',
            params={
                'page': page,
                'limit': limit,
                'status': status,
                'updatedAtStart': updated_at_start,
                'updatedAtEnd': updated_at_end,
                'withCustomData': with_custom_data,
                'withPost': with_post,
                'withIdentities': with_identities,
                'withDepartmentIds': with_department_ids,
            },
        )

    def get_user(self, user_id, user_id_type=None, flat_custom_data=None, with_custom_data=None, with_post=None,
                 with_identities=None, with_department_ids=None):
        """获取用户信息

        通过用户 ID，获取用户详情，可以选择获取自定义数据、identities、选择指定用户 ID 类型等。

        Attributes:
            userId (str): 用户 ID
            userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
- `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
- `phone`: 用户手机号
- `email`: 用户邮箱
- `username`: 用户名
- `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
- `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。
- `sync_relation`: 用户的外部身份源信息，格式为 `<provier>:<userIdInIdp>`，其中 `<provier>` 为同步身份源类型，如 wechatwork, lark；`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`lark:ou_8bae746eac07cd2564654140d2a9ac61`。

            flatCustomData (bool): 是否拍平扩展字段
            withCustomData (bool): 是否获取自定义数据
            withPost (bool): 是否获取 部门信息
            withIdentities (bool): 是否获取 identities
            withDepartmentIds (bool): 是否获取部门 ID 列表
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
                'flatCustomData': flat_custom_data,
                'withCustomData': with_custom_data,
                'withPost': with_post,
                'withIdentities': with_identities,
                'withDepartmentIds': with_department_ids,
            },
        )

    def get_user_batch(self, user_ids, user_id_type=None, with_custom_data=None, flat_custom_data=None,
                       with_identities=None, with_department_ids=None):
        """批量获取用户信息

        通过用户 ID 列表，批量获取用户信息，可以选择获取自定义数据、identities、选择指定用户 ID 类型等。

        Attributes:
            userIds (str): 用户 ID 数组
            userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
- `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
- `phone`: 用户手机号
- `email`: 用户邮箱
- `username`: 用户名
- `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
- `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。
- `sync_relation`: 用户的外部身份源信息，格式为 `<provier>:<userIdInIdp>`，其中 `<provier>` 为同步身份源类型，如 wechatwork, lark；`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`lark:ou_8bae746eac07cd2564654140d2a9ac61`。

            withCustomData (bool): 是否获取自定义数据
            flatCustomData (bool): 是否拍平扩展字段
            withIdentities (bool): 是否获取 identities
            withDepartmentIds (bool): 是否获取部门 ID 列表
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-batch',
            params={
                'userIds': user_ids,
                'userIdType': user_id_type,
                'withCustomData': with_custom_data,
                'flatCustomData': flat_custom_data,
                'withIdentities': with_identities,
                'withDepartmentIds': with_department_ids,
            },
        )

    def user_field_decrypt(self, data, private_key):
        """用户属性解密

        接口接收加密信息，返回解密信息

        Attributes:
            data (list): 用户需要解密的属性列表
            private_key (str): 私钥，通过控制台安全设置-数据安全-数据加密获取
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/users/field/decrypt',
            json={
                'data': data,
                'privateKey': private_key,
            },
        )

    def create_user(self, status=None, email=None, phone=None, phone_country_code=None, username=None, external_id=None,
                    name=None, nickname=None, photo=None, gender=None, email_verified=None, phone_verified=None,
                    birthdate=None, country=None, province=None, city=None, address=None, street_address=None,
                    postal_code=None, company=None, browser=None, device=None, given_name=None, family_name=None,
                    middle_name=None, profile=None, preferred_username=None, website=None, zoneinfo=None, locale=None,
                    formatted=None, region=None, password=None, salt=None, tenant_ids=None, otp=None,
                    department_ids=None, custom_data=None, metadata_source=None, identities=None, identity_number=None,
                    options=None):
        """创建用户

        创建用户，邮箱、手机号、用户名必须包含其中一个，邮箱、手机号、用户名、externalId 用户池内唯一，此接口将以管理员身份创建用户因此不需要进行手机号验证码检验等安全检测。  

        Attributes:
            status (str): 账户当前状态
            email (str): 邮箱，不区分大小写
            phone (str): 手机号，不带区号。如果是国外手机号，请在 phoneCountryCode 参数中指定区号。
            phone_country_code (str): 手机区号，中国大陆手机号可不填。Authing 短信服务暂不内置支持国际手机号，你需要在 Authing 控制台配置对应的国际短信服务。完整的手机区号列表可参阅 https://en.wikipedia.org/wiki/List_of_country_calling_codes。
            username (str): 用户名，用户池内唯一
            external_id (str): 第三方外部 ID
            name (str): 用户真实名称，不具备唯一性
            nickname (str): 昵称
            photo (str): 头像链接
            gender (str): 性别
            email_verified (bool): 邮箱是否验证
            phone_verified (bool): 手机号是否验证
            birthdate (str): 出生日期
            country (str): 所在国家
            province (str): 所在省份
            city (str): 所在城市
            address (str): 所处地址
            street_address (str): 所处街道地址
            postal_code (str): 邮政编码号
            company (str): 所在公司
            browser (str): 最近一次登录时使用的浏览器 UA
            device (str): 最近一次登录时使用的设备
            given_name (str): 名
            family_name (str): 姓
            middle_name (str): 中间名
            profile (str): Preferred Username
            preferred_username (str): Preferred Username
            website (str): 用户个人网页
            zoneinfo (str): 用户时区信息
            locale (str): Locale
            formatted (str): 标准的完整地址
            region (str): 用户所在区域
            password (str): 用户密码，默认为明文。我们使用 HTTPS 协议对密码进行安全传输，可以在一定程度上保证安全性。如果你还需要更高级别的安全性，我们还支持 RSA256 和国密 SM2 两种方式对密码进行加密。详情见 `passwordEncryptType` 参数。
            salt (str): 加密用户密码的盐
            tenant_ids (list): 租户 ID
            otp (dict): 用户的 OTP 验证器
            department_ids (list): 用户所属部门 ID 列表
            custom_data (dict): 自定义数据，传入的对象中的 key 必须先在用户池定义相关自定义字段
            metadata_source (dict): 数据对象数据，传入的对象中的 key 必须先在用户池定义相关自定义字段
            identities (list): 第三方身份源（建议调用绑定接口进行绑定）
            identity_number (str): 用户身份证号码
            options (dict): 可选参数
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-user',
            json={
                'status': status,
                'email': email,
                'phone': phone,
                'phoneCountryCode': phone_country_code,
                'username': username,
                'externalId': external_id,
                'name': name,
                'nickname': nickname,
                'photo': photo,
                'gender': gender,
                'emailVerified': email_verified,
                'phoneVerified': phone_verified,
                'birthdate': birthdate,
                'country': country,
                'province': province,
                'city': city,
                'address': address,
                'streetAddress': street_address,
                'postalCode': postal_code,
                'company': company,
                'browser': browser,
                'device': device,
                'givenName': given_name,
                'familyName': family_name,
                'middleName': middle_name,
                'profile': profile,
                'preferredUsername': preferred_username,
                'website': website,
                'zoneinfo': zoneinfo,
                'locale': locale,
                'formatted': formatted,
                'region': region,
                'password': password,
                'salt': salt,
                'tenantIds': tenant_ids,
                'otp': otp,
                'departmentIds': department_ids,
                'customData': custom_data,
                'metadataSource': metadata_source,
                'identities': identities,
                'identityNumber': identity_number,
                'options': options,
            },
        )

    def create_users_batch(self, list, options=None):
        """批量创建用户

        批量创建用户，邮箱、手机号、用户名必须包含其中一个，邮箱、手机号、用户名、externalId 用户池内唯一，此接口将以管理员身份创建用户因此不需要进行手机号验证码检验等安全检测。

        Attributes:
            list (list): 用户列表
            options (dict): 可选参数
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-users-batch',
            json={
                'list': list,
                'options': options,
            },
        )

    def update_user(self, user_id, phone_country_code=None, name=None, nickname=None, photo=None, external_id=None,
                    status=None, email_verified=None, phone_verified=None, birthdate=None, country=None, province=None,
                    city=None, address=None, street_address=None, postal_code=None, gender=None, username=None,
                    email=None, phone=None, password=None, company=None, browser=None, device=None, given_name=None,
                    family_name=None, middle_name=None, profile=None, preferred_username=None, website=None,
                    zoneinfo=None, locale=None, formatted=None, region=None, identity_number=None, custom_data=None,
                    options=None):
        """修改用户资料

        通过用户 ID，修改用户资料，邮箱、手机号、用户名、externalId 用户池内唯一，此接口将以管理员身份修改用户资料因此不需要进行手机号验证码检验等安全检测。

        Attributes:
            user_id (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            phone_country_code (str): 手机区号，中国大陆手机号可不填。Authing 短信服务暂不内置支持国际手机号，你需要在 Authing 控制台配置对应的国际短信服务。完整的手机区号列表可参阅 https://en.wikipedia.org/wiki/List_of_country_calling_codes。
            name (str): 用户真实名称，不具备唯一性
            nickname (str): 昵称
            photo (str): 头像链接
            external_id (str): 第三方外部 ID
            status (str): 账户当前状态
            email_verified (bool): 邮箱是否验证
            phone_verified (bool): 手机号是否验证
            birthdate (str): 出生日期
            country (str): 所在国家
            province (str): 所在省份
            city (str): 所在城市
            address (str): 所处地址
            street_address (str): 所处街道地址
            postal_code (str): 邮政编码号
            gender (str): 性别
            username (str): 用户名，用户池内唯一
            email (str): 邮箱，不区分大小写
            phone (str): 手机号，不带区号。如果是国外手机号，请在 phoneCountryCode 参数中指定区号。
            password (str): 用户密码，默认为明文。我们使用 HTTPS 协议对密码进行安全传输，可以在一定程度上保证安全性。如果你还需要更高级别的安全性，我们还支持 RSA256 和国密 SM2 两种方式对密码进行加密。详情见 `passwordEncryptType` 参数。
            company (str): 所在公司
            browser (str): 最近一次登录时使用的浏览器 UA
            device (str): 最近一次登录时使用的设备
            given_name (str): 名
            family_name (str): 姓
            middle_name (str): 中间名
            profile (str): Preferred Username
            preferred_username (str): Preferred Username
            website (str): 用户个人网页
            zoneinfo (str): 用户时区信息
            locale (str): Locale
            formatted (str): 标准的完整地址
            region (str): 用户所在区域
            identity_number (str): 用户身份证号码
            custom_data (dict): 自定义数据，传入的对象中的 key 必须先在用户池定义相关自定义字段
            options (dict): 可选参数
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-user',
            json={
                'userId': user_id,
                'phoneCountryCode': phone_country_code,
                'name': name,
                'nickname': nickname,
                'photo': photo,
                'externalId': external_id,
                'status': status,
                'emailVerified': email_verified,
                'phoneVerified': phone_verified,
                'birthdate': birthdate,
                'country': country,
                'province': province,
                'city': city,
                'address': address,
                'streetAddress': street_address,
                'postalCode': postal_code,
                'gender': gender,
                'username': username,
                'email': email,
                'phone': phone,
                'password': password,
                'company': company,
                'browser': browser,
                'device': device,
                'givenName': given_name,
                'familyName': family_name,
                'middleName': middle_name,
                'profile': profile,
                'preferredUsername': preferred_username,
                'website': website,
                'zoneinfo': zoneinfo,
                'locale': locale,
                'formatted': formatted,
                'region': region,
                'identityNumber': identity_number,
                'customData': custom_data,
                'options': options,
            },
        )

    def update_user_batch(self, list, options=None):
        """批量修改用户资料

        批量修改用户资料，邮箱、手机号、用户名、externalId 用户池内唯一，此接口将以管理员身份修改用户资料因此不需要进行手机号验证码检验等安全检测。

        Attributes:
            list (list): 用户列表
            options (dict): 可选参数
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-user-batch',
            json={
                'list': list,
                'options': options,
            },
        )

    def delete_users_batch(self, user_ids, options=None):
        """批量删除用户

        通过用户 ID 列表，删除用户，支持批量删除，可以选择指定用户 ID 类型等。

        Attributes:
            user_ids (list): 用户 ID 列表
            options (dict): 可选参数
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-users-batch',
            json={
                'userIds': user_ids,
                'options': options,
            },
        )

    def get_user_identities(self, user_id, user_id_type=None):
        """获取用户的外部身份源

        通过用户 ID，获取用户的外部身份源、选择指定用户 ID 类型。

        Attributes:
            userId (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
- `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
- `phone`: 用户手机号
- `email`: 用户邮箱
- `username`: 用户名
- `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
- `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。
- `sync_relation`: 用户的外部身份源信息，格式为 `<provier>:<userIdInIdp>`，其中 `<provier>` 为同步身份源类型，如 wechatwork, lark；`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`lark:ou_8bae746eac07cd2564654140d2a9ac61`。

        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-identities',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def get_user_roles(self, user_id, user_id_type=None, namespace=None):
        """获取用户角色列表

        通过用户 ID，获取用户角色列表，可以选择所属权限分组 code、选择指定用户 ID 类型等。

        Attributes:
            userId (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
- `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
- `phone`: 用户手机号
- `email`: 用户邮箱
- `username`: 用户名
- `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
- `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。
- `sync_relation`: 用户的外部身份源信息，格式为 `<provier>:<userIdInIdp>`，其中 `<provier>` 为同步身份源类型，如 wechatwork, lark；`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`lark:ou_8bae746eac07cd2564654140d2a9ac61`。

            namespace (str): 所属权限分组(权限空间)的 Code
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-roles',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
                'namespace': namespace,
            },
        )

    def get_user_principal_authentication_info(self, user_id, user_id_type=None):
        """获取用户实名认证信息

        通过用户 ID，获取用户实名认证信息，可以选择指定用户 ID 类型。

        Attributes:
            userId (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
- `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
- `phone`: 用户手机号
- `email`: 用户邮箱
- `username`: 用户名
- `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
- `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。
- `sync_relation`: 用户的外部身份源信息，格式为 `<provier>:<userIdInIdp>`，其中 `<provier>` 为同步身份源类型，如 wechatwork, lark；`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`lark:ou_8bae746eac07cd2564654140d2a9ac61`。

        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-principal-authentication-info',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def reset_user_principal_authentication_info(self, user_id, options=None):
        """删除用户实名认证信息

        通过用户 ID，删除用户实名认证信息，可以选择指定用户 ID 类型等。

        Attributes:
            user_id (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            options (dict): 可选参数
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/reset-user-principal-authentication-info',
            json={
                'userId': user_id,
                'options': options,
            },
        )

    def get_user_departments(self, user_id, user_id_type=None, page=None, limit=None, with_custom_data=None,
                             with_department_paths=None, sort_by=None, order_by=None):
        """获取用户部门列表

        通过用户 ID，获取用户部门列表，支持分页，可以选择获取自定义数据、选择指定用户 ID 类型、增序或降序等。

        Attributes:
            userId (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
- `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
- `phone`: 用户手机号
- `email`: 用户邮箱
- `username`: 用户名
- `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
- `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。
- `sync_relation`: 用户的外部身份源信息，格式为 `<provier>:<userIdInIdp>`，其中 `<provier>` 为同步身份源类型，如 wechatwork, lark；`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`lark:ou_8bae746eac07cd2564654140d2a9ac61`。

            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            withCustomData (bool): 是否获取自定义数据
            withDepartmentPaths (bool): 是否获取部门路径
            sortBy (str): 排序依据，如 部门创建时间、加入部门时间、部门名称、部门标志符
            orderBy (str): 增序或降序
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-departments',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
                'page': page,
                'limit': limit,
                'withCustomData': with_custom_data,
                'withDepartmentPaths': with_department_paths,
                'sortBy': sort_by,
                'orderBy': order_by,
            },
        )

    def set_user_departments(self, user_id, departments, options=None):
        """设置用户所在部门

        通过用户 ID，设置用户所在部门，可以选择指定用户 ID 类型等。

        Attributes:
            user_id (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            departments (list): 部门信息
            options (dict): 可选参数
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/set-user-departments',
            json={
                'userId': user_id,
                'departments': departments,
                'options': options,
            },
        )

    def get_user_groups(self, user_id, user_id_type=None):
        """获取用户分组列表

        通过用户 ID，获取用户分组列表，可以选择指定用户 ID 类型等。

        Attributes:
            userId (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
- `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
- `phone`: 用户手机号
- `email`: 用户邮箱
- `username`: 用户名
- `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
- `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。
- `sync_relation`: 用户的外部身份源信息，格式为 `<provier>:<userIdInIdp>`，其中 `<provier>` 为同步身份源类型，如 wechatwork, lark；`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`lark:ou_8bae746eac07cd2564654140d2a9ac61`。

        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-groups',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def get_user_mfa_info(self, user_id, user_id_type=None):
        """获取用户 MFA 绑定信息

        通过用户 ID，获取用户 MFA 绑定信息，可以选择指定用户 ID 类型等。

        Attributes:
            userId (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
- `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
- `phone`: 用户手机号
- `email`: 用户邮箱
- `username`: 用户名
- `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
- `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。
- `sync_relation`: 用户的外部身份源信息，格式为 `<provier>:<userIdInIdp>`，其中 `<provier>` 为同步身份源类型，如 wechatwork, lark；`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`lark:ou_8bae746eac07cd2564654140d2a9ac61`。

        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-mfa-info',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def list_archived_users(self, page=None, limit=None, start_at=None):
        """获取已归档的用户列表

        获取已归档的用户列表，支持分页，可以筛选开始时间等。

        Attributes:
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            startAt (int): 开始时间，为精确到秒的 UNIX 时间戳，默认不指定
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-archived-users',
            params={
                'page': page,
                'limit': limit,
                'startAt': start_at,
            },
        )

    def kick_users(self, app_ids, user_id, options=None):
        """强制下线用户

        通过用户 ID、App ID 列表，强制让用户下线，可以选择指定用户 ID 类型等。

        Attributes:
            app_ids (list): APP ID 列表
            user_id (str): 用户 ID
            options (dict): 可选参数
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/kick-users',
            json={
                'appIds': app_ids,
                'userId': user_id,
                'options': options,
            },
        )

    def is_user_exists(self, username=None, email=None, phone=None, external_id=None):
        """判断用户是否存在

        根据条件判断用户是否存在，可以筛选用户名、邮箱、手机号、第三方外部 ID 等。

        Attributes:
            username (str): 用户名，用户池内唯一
            email (str): 邮箱，不区分大小写
            phone (str): 手机号，不带区号。如果是国外手机号，请在 phoneCountryCode 参数中指定区号。
            external_id (str): 第三方外部 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/is-user-exists',
            json={
                'username': username,
                'email': email,
                'phone': phone,
                'externalId': external_id,
            },
        )

    def get_user_accessible_apps(self, user_id, user_id_type=None):
        """获取用户可访问的应用

        通过用户 ID，获取用户可访问的应用，可以选择指定用户 ID 类型等。

        Attributes:
            userId (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
- `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
- `phone`: 用户手机号
- `email`: 用户邮箱
- `username`: 用户名
- `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
- `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。
- `sync_relation`: 用户的外部身份源信息，格式为 `<provier>:<userIdInIdp>`，其中 `<provier>` 为同步身份源类型，如 wechatwork, lark；`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`lark:ou_8bae746eac07cd2564654140d2a9ac61`。

        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-accessible-apps',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def get_user_authorized_apps(self, user_id, user_id_type=None):
        """获取用户授权的应用

        通过用户 ID，获取用户授权的应用，可以选择指定用户 ID 类型等。

        Attributes:
            userId (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
- `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
- `phone`: 用户手机号
- `email`: 用户邮箱
- `username`: 用户名
- `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
- `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。
- `sync_relation`: 用户的外部身份源信息，格式为 `<provier>:<userIdInIdp>`，其中 `<provier>` 为同步身份源类型，如 wechatwork, lark；`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`lark:ou_8bae746eac07cd2564654140d2a9ac61`。

        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-authorized-apps',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def has_any_role(self, roles, user_id, options=None):
        """判断用户是否有某个角色

        通过用户 ID，判断用户是否有某个角色，支持传入多个角色，可以选择指定用户 ID 类型等。

        Attributes:
            roles (list): 角色列表
            user_id (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            options (dict): 可选参数
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/has-any-role',
            json={
                'roles': roles,
                'userId': user_id,
                'options': options,
            },
        )

    def get_user_login_history(self, user_id, user_id_type=None, app_id=None, client_ip=None, start=None, end=None,
                               page=None, limit=None):
        """获取用户的登录历史记录

        通过用户 ID，获取用户登录历史记录，支持分页，可以选择指定用户 ID 类型、应用 ID、开始与结束时间戳等。

        Attributes:
            userId (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
- `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
- `phone`: 用户手机号
- `email`: 用户邮箱
- `username`: 用户名
- `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
- `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。
- `sync_relation`: 用户的外部身份源信息，格式为 `<provier>:<userIdInIdp>`，其中 `<provier>` 为同步身份源类型，如 wechatwork, lark；`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`lark:ou_8bae746eac07cd2564654140d2a9ac61`。

            appId (str): 应用 ID
            clientIp (str): 客户端 IP
            start (int): 开始时间戳（毫秒）
            end (int): 结束时间戳（毫秒）
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-login-history',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
                'appId': app_id,
                'clientIp': client_ip,
                'start': start,
                'end': end,
                'page': page,
                'limit': limit,
            },
        )

    def get_user_loggedin_apps(self, user_id, user_id_type=None):
        """获取用户曾经登录过的应用

        通过用户 ID，获取用户曾经登录过的应用，可以选择指定用户 ID 类型等。

        Attributes:
            userId (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
- `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
- `phone`: 用户手机号
- `email`: 用户邮箱
- `username`: 用户名
- `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
- `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。
- `sync_relation`: 用户的外部身份源信息，格式为 `<provier>:<userIdInIdp>`，其中 `<provier>` 为同步身份源类型，如 wechatwork, lark；`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`lark:ou_8bae746eac07cd2564654140d2a9ac61`。

        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-loggedin-apps',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def get_user_loggedin_identities(self, user_id, user_id_type=None):
        """获取用户曾经登录过的身份源

        通过用户 ID，获取用户曾经登录过的身份源，可以选择指定用户 ID 类型等。

        Attributes:
            userId (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
- `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
- `phone`: 用户手机号
- `email`: 用户邮箱
- `username`: 用户名
- `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
- `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。
- `sync_relation`: 用户的外部身份源信息，格式为 `<provier>:<userIdInIdp>`，其中 `<provier>` 为同步身份源类型，如 wechatwork, lark；`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`lark:ou_8bae746eac07cd2564654140d2a9ac61`。

        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-logged-in-identities',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def resign_user(self, user_id, user_id_type=None):
        """离职用户

        离职用户。离职操作会进行以下操作：

- 离职后该成员授权、部门、角色、分组、岗位关系将被删除；
- 离职后将保留用户基本信息，同时账号将被禁用，无法登录应用；如果需要彻底删除账号，请调用删除接口。

该操作不可恢复，请谨慎操作！
    

        Attributes:
            user_id (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            user_id_type (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
- `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
- `phone`: 用户手机号
- `email`: 用户邮箱
- `username`: 用户名
- `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
- `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。
- `sync_relation`: 用户的外部身份源信息，格式为 `<provier>:<userIdInIdp>`，其中 `<provier>` 为同步身份源类型，如 wechatwork, lark；`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`lark:ou_8bae746eac07cd2564654140d2a9ac61`。

        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/resign-user',
            json={
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def resign_user_batch(self, user_ids, user_id_type=None):
        """批量离职用户

        批量离职用户。离职操作会进行以下操作：

- 离职后该成员授权、部门、角色、分组、岗位关系将被删除；
- 离职后将保留用户基本信息，同时账号将被禁用，无法登录应用；如果需要彻底删除账号，请调用删除接口。

该操作不可恢复，请谨慎操作！
    

        Attributes:
            user_ids (list): 用户 ID 数组
            user_id_type (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
- `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
- `phone`: 用户手机号
- `email`: 用户邮箱
- `username`: 用户名
- `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
- `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。
- `sync_relation`: 用户的外部身份源信息，格式为 `<provier>:<userIdInIdp>`，其中 `<provier>` 为同步身份源类型，如 wechatwork, lark；`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`lark:ou_8bae746eac07cd2564654140d2a9ac61`。

        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/resign-user-batch',
            json={
                'userIds': user_ids,
                'userIdType': user_id_type,
            },
        )

    def get_user_authorized_resources(self, user_id, user_id_type=None, namespace=None, resource_type=None):
        """获取用户被授权的所有资源

        通过用户 ID，获取用户被授权的所有资源，可以选择指定用户 ID 类型等，用户被授权的资源是用户自身被授予、通过分组继承、通过角色继承、通过组织机构继承的集合。

        Attributes:
            userId (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
- `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
- `phone`: 用户手机号
- `email`: 用户邮箱
- `username`: 用户名
- `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
- `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。
- `sync_relation`: 用户的外部身份源信息，格式为 `<provier>:<userIdInIdp>`，其中 `<provier>` 为同步身份源类型，如 wechatwork, lark；`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`lark:ou_8bae746eac07cd2564654140d2a9ac61`。

            namespace (str): 所属权限分组(权限空间)的 Code
            resourceType (str): 资源类型，如 数据、API、菜单、按钮
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-authorized-resources',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
                'namespace': namespace,
                'resourceType': resource_type,
            },
        )

    def check_session_status(self, app_id, user_id):
        """检查某个用户在应用下是否具备 Session 登录态

        检查某个用户在应用下是否具备 Session 登录态

        Attributes:
            app_id (str): App ID
            user_id (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/check-session-status',
            json={
                'appId': app_id,
                'userId': user_id,
            },
        )

    def import_otp(self, list):
        """导入用户的 OTP

        导入用户的 OTP

        Attributes:
            list (list): 参数列表
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/import-otp',
            json={
                'list': list,
            },
        )

    def get_otp_secret_by_user(self, user_id, user_id_type=None):
        """获取用户绑定 OTP 的秘钥

        通过用户 ID，获取用户绑定 OTP 的秘钥。可以选择指定用户 ID 类型等。

        Attributes:
            userId (str): 用户 ID
            userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
- `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
- `phone`: 用户手机号
- `email`: 用户邮箱
- `username`: 用户名
- `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
- `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。
- `sync_relation`: 用户的外部身份源信息，格式为 `<provier>:<userIdInIdp>`，其中 `<provier>` 为同步身份源类型，如 wechatwork, lark；`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`lark:ou_8bae746eac07cd2564654140d2a9ac61`。

        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-otp-secret-by-user',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def get_user_password_ciphertext(self, user_id, user_id_type=None):
        """获取用户自定义加密的密码

        此功能主要是用户在控制台配置加基于 RSA、SM2 等加密的密钥后，加密用户的密码。

        Attributes:
            user_id (str): 用户 ID
            user_id_type (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
- `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
- `phone`: 用户手机号
- `email`: 用户邮箱
- `username`: 用户名
- `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
- `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。
- `sync_relation`: 用户的外部身份源信息，格式为 `<provier>:<userIdInIdp>`，其中 `<provier>` 为同步身份源类型，如 wechatwork, lark；`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`lark:ou_8bae746eac07cd2564654140d2a9ac61`。

        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-user-password-ciphertext',
            json={
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def link_identity(self, user_id_in_idp, user_id, ext_idp_id, type=None, is_social=None):
        """给用户绑定一个身份信息

        用户池管理员手动将来自外部身份源的身份信息绑定到用户上。绑定完成后，可以用执行过绑定操作的身份源登录到对应的 Authing 用户。

        Attributes:
            user_id_in_idp (str): 必传，用户在该外部身份源的唯一标识，需要从外部身份源的认证返回值中获取。
            user_id (str): 必传，进行绑定操作的 Authing 用户 ID。
            ext_idp_id (str): 必传，身份源 ID，用于指定该身份属于哪个身份源。
            type (str): 非必传，表示该条身份的具体类型，可从用户身份信息的 type 字段中获取。如果不传，默认为 generic
            is_social (bool): 已废弃，可任意传入，未来将移除该字段。
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/link-identity',
            json={
                'userIdInIdp': user_id_in_idp,
                'userId': user_id,
                'extIdpId': ext_idp_id,
                'type': type,
                'isSocial': is_social,
            },
        )

    def unlink_identity(self, user_id, ext_idp_id, type=None, is_social=None):
        """解除绑定用户在身份源下的所有身份信息

        解除绑定用户在某个身份源下的所有身份信息。解绑后，将无法使用执行过解绑操作的身份源登录到对应的 Authing 用户，除非重新绑定身份信息。

        Attributes:
            user_id (str): 必传，进行绑定操作的 Authing 用户 ID。
            ext_idp_id (str): 必传，身份源 ID，用于指定该身份属于哪个身份源。
            type (str): 非必传，表示该条身份的具体类型，可从用户身份信息的 type 字段中获取。如果不传，默认为 generic
            is_social (bool): 已废弃，可任意传入，未来将移除该字段。
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/unlink-identity',
            json={
                'userId': user_id,
                'extIdpId': ext_idp_id,
                'type': type,
                'isSocial': is_social,
            },
        )

    def set_users_mfa_status(self, mfa_trigger_data, user_id, user_id_type=None):
        """设置用户 MFA 状态

        设置用户 MFA 状态，即 MFA 触发数据。

        Attributes:
            mfa_trigger_data (dict): MFA Factor 列表
            user_id (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            user_id_type (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
- `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
- `phone`: 用户手机号
- `email`: 用户邮箱
- `username`: 用户名
- `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
- `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。
- `sync_relation`: 用户的外部身份源信息，格式为 `<provier>:<userIdInIdp>`，其中 `<provier>` 为同步身份源类型，如 wechatwork, lark；`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`lark:ou_8bae746eac07cd2564654140d2a9ac61`。

        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/set-mfa-status',
            json={
                'mfaTriggerData': mfa_trigger_data,
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def get_user_mfa_status(self, user_id, user_id_type=None):
        """获取用户 MFA 状态

        获取用户 MFA 状态，即 MFA 触发数据。

        Attributes:
            userId (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
- `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
- `phone`: 用户手机号
- `email`: 用户邮箱
- `username`: 用户名
- `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
- `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。
- `sync_relation`: 用户的外部身份源信息，格式为 `<provier>:<userIdInIdp>`，其中 `<provier>` 为同步身份源类型，如 wechatwork, lark；`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`lark:ou_8bae746eac07cd2564654140d2a9ac61`。

        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-mfa-status',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def get_user_sync_relations(self, user_id, user_id_type=None):
        """获取用户绑定的第三方同步关系

        如果在 Authing 中的用户进行了上下游同步，此接口可以用于查询出在第三方的关联用户信息

        Attributes:
            userId (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
- `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
- `phone`: 用户手机号
- `email`: 用户邮箱
- `username`: 用户名
- `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
- `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。
- `sync_relation`: 用户的外部身份源信息，格式为 `<provier>:<userIdInIdp>`，其中 `<provier>` 为同步身份源类型，如 wechatwork, lark；`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`lark:ou_8bae746eac07cd2564654140d2a9ac61`。

        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-sync-relations',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def delete_user_sync_relations(self, provider, user_id, user_id_type=None):
        """删除用户同步关联关系

        如果在 Authing 中的用户进行了上下游同步，此接口可以用于删除某个用户在指定身份源下的关联关系。

        Attributes:
            provider (str): 外部身份源类型，如：
- `wechatwork`: 企业微信
- `dingtalk`: 钉钉
- `lark`: 飞书
- `welink`: Welink
- `ldap`: LDAP
- `active-directory`: Windows AD
- `italent`: 北森
- `xiaoshouyi`: 销售易
- `maycur`: 每刻报销
- `scim`: SCIM
- `moka`: Moka HR
    
            user_id (str): 用户 ID
            user_id_type (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
- `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
- `phone`: 用户手机号
- `email`: 用户邮箱
- `username`: 用户名
- `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
- `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。
- `sync_relation`: 用户的外部身份源信息，格式为 `<provier>:<userIdInIdp>`，其中 `<provier>` 为同步身份源类型，如 wechatwork, lark；`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`lark:ou_8bae746eac07cd2564654140d2a9ac61`。

        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-user-sync-relations',
            json={
                'provider': provider,
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def get_public_account_roles(self, user_id, user_id_type=None, namespace=None):
        """获取公共账号的角色列表

        通过用户 ID，获取用户角色列表，可以选择所属权限分组 code、选择指定用户 ID 类型等。

        Attributes:
            userId (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
- `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
- `phone`: 用户手机号
- `email`: 用户邮箱
- `username`: 用户名
- `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
- `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。
- `sync_relation`: 用户的外部身份源信息，格式为 `<provier>:<userIdInIdp>`，其中 `<provier>` 为同步身份源类型，如 wechatwork, lark；`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`lark:ou_8bae746eac07cd2564654140d2a9ac61`。

            namespace (str): 所属权限分组(权限空间)的 code
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-roles-of-public-account',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
                'namespace': namespace,
            },
        )

    def get_public_accounts_of_role(self, role_id):
        """获取角色的公共账号列表

        通过角色 ID，获取用户的公共账号列表。

        Attributes:
            roleId (str): 角色 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-public-accounts-of-role',
            params={
                'roleId': role_id,
            },
        )

    def bind_public_account_of_roles(self, role_ids, user_id):
        """公共账号绑定批量角色

        公共账号绑定批量角色

        Attributes:
            role_ids (list): 角色 IDs
            user_id (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/set-public-account-of-roles',
            json={
                'roleIds': role_ids,
                'userId': user_id,
            },
        )

    def get_public_accounts_of_group(self, group_id):
        """获取分组的公共账号列表

        通过分组 ID，获取用户的公共账号列表。

        Attributes:
            groupId (str): 分组 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-public-accounts-of-group',
            params={
                'groupId': group_id,
            },
        )

    def get_groups_of_public_account(self, user_id, user_id_type=None):
        """获取公共账号分组列表

        通过公共账号 ID，获取公共账号分组列表，可以选择指定用户 ID 类型等。

        Attributes:
            userId (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
- `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
- `phone`: 用户手机号
- `email`: 用户邮箱
- `username`: 用户名
- `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
- `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。
- `sync_relation`: 用户的外部身份源信息，格式为 `<provier>:<userIdInIdp>`，其中 `<provier>` 为同步身份源类型，如 wechatwork, lark；`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`lark:ou_8bae746eac07cd2564654140d2a9ac61`。

        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-groups-of-public-account',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def get_public_account_of_groups(self, group_ids, user_id):
        """公共账号添加批量分组

        公共账号通过分组 ID 添加批量分组

        Attributes:
            group_ids (list): 群组 ID 列表
            user_id (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/set-public-account-of-groups',
            json={
                'groupIds': group_ids,
                'userId': user_id,
            },
        )

    def get_public_accounts_of_department(self, department_id):
        """获取部门的公共账号列表

        通过部门 ID，获取用户的公共账号列表。

        Attributes:
            departmentId (str): 部门 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-public-accounts-of-department',
            params={
                'departmentId': department_id,
            },
        )

    def get_public_account_departments(self, user_id, user_id_type=None, page=None, limit=None, with_custom_data=None,
                                       with_department_paths=None, sort_by=None, order_by=None):
        """获取公共账号的部门列表

        通过用户 ID，获取用户部门列表，支持分页，可以选择获取自定义数据、选择指定用户 ID 类型、增序或降序等。

        Attributes:
            userId (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
- `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
- `phone`: 用户手机号
- `email`: 用户邮箱
- `username`: 用户名
- `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
- `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。
- `sync_relation`: 用户的外部身份源信息，格式为 `<provier>:<userIdInIdp>`，其中 `<provier>` 为同步身份源类型，如 wechatwork, lark；`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`lark:ou_8bae746eac07cd2564654140d2a9ac61`。

            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            withCustomData (bool): 是否获取自定义数据
            withDepartmentPaths (bool): 是否获取部门路径
            sortBy (str): 排序依据，如 部门创建时间、加入部门时间、部门名称、部门标志符
            orderBy (str): 增序或降序
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-departments-of-public-account',
            params={
                'userId': user_id,
                'userIdType': user_id_type,
                'page': page,
                'limit': limit,
                'withCustomData': with_custom_data,
                'withDepartmentPaths': with_department_paths,
                'sortBy': sort_by,
                'orderBy': order_by,
            },
        )

    def set_public_account_of_departments(self, user_id, departments, options=None):
        """设置公共账号所在部门

        设置公共账号所在部门。

        Attributes:
            user_id (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            departments (list): 部门信息
            options (dict): 可选参数
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/set-public-account-of-departments',
            json={
                'userId': user_id,
                'departments': departments,
                'options': options,
            },
        )

    def resign_public_account_batch(self, user_ids, user_id_type=None):
        """批量离职用户

        批量离职用户。离职操作会进行以下操作：

- 离职后该成员授权、部门、角色、分组、岗位关系将被删除；
- 离职后将保留用户基本信息，同时账号将被禁用，无法登录应用；如果需要彻底删除账号，请调用删除接口。

该操作不可恢复，请谨慎操作！
    

        Attributes:
            user_ids (list): 用户 ID 数组
            user_id_type (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
- `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
- `phone`: 用户手机号
- `email`: 用户邮箱
- `username`: 用户名
- `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
- `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。
- `sync_relation`: 用户的外部身份源信息，格式为 `<provier>:<userIdInIdp>`，其中 `<provier>` 为同步身份源类型，如 wechatwork, lark；`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`lark:ou_8bae746eac07cd2564654140d2a9ac61`。

        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/resign-public-account-batch',
            json={
                'userIds': user_ids,
                'userIdType': user_id_type,
            },
        )

    def get_post_of_public_user(self, user_id):
        """获取公共账号的岗位

        获取公共账号的岗位

        Attributes:
            userId (str): 用户 id
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-post-of-public-account',
            params={
                'userId': user_id,
            },
        )

    def get_public_accounts_of_post(self, post_id):
        """获取岗位的公共账号列表

        通过岗位 ID，获取用户的公共账号列表。

        Attributes:
            postId (str): 岗位 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-public-accounts-of-post',
            params={
                'postId': post_id,
            },
        )

    def set_public_account_ofn_post(self, user_id, post_id):
        """设置公共账号的岗位

        设置公共账号关联的岗位

        Attributes:
            user_id (str): 用户 id
            post_id (str): 部门 id
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/set-public-account-of-post',
            json={
                'userId': user_id,
                'postId': post_id,
            },
        )

    def unbind_public_account_of_post(self, user_id, post_id):
        """解绑公共账号关联岗位

        解绑公共账号关联岗位

        Attributes:
            user_id (str): 用户 id
            post_id (str): 部门 id
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/unbind-public-account-of-post',
            json={
                'userId': user_id,
                'postId': post_id,
            },
        )

    def get_sync_task(self, sync_task_id):
        """获取同步任务详情

        获取同步任务详情

        Attributes:
            syncTaskId (int): 同步任务 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-sync-task',
            params={
                'syncTaskId': sync_task_id,
            },
        )

    def list_sync_tasks(self, page=None, limit=None):
        """获取同步任务列表

        获取同步任务列表

        Attributes:
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-sync-tasks',
            params={
                'page': page,
                'limit': limit,
            },
        )

    def create_sync_task(self, field_mapping, sync_task_trigger, sync_task_flow, client_config, sync_task_type,
                         sync_task_name, organization_code=None, provisioning_scope=None, timed_scheduler=None):
        """创建同步任务

        创建同步任务

        Attributes:
            field_mapping (list): 字段映射配置
            sync_task_trigger (str): 同步任务触发类型：
- `manually`: 手动触发执行
- `timed`: 定时触发
- `automatic`: 根据事件自动触发

            sync_task_flow (str): 同步任务数据流向：
- `upstream`: 作为上游，将数据同步到 Authing
- `downstream`: 作为下游，将 Authing 数据同步到此系统
    
            client_config (dict): 同步任务配置信息
            sync_task_type (str): 同步任务类型:
- `lark`: 飞书
- `lark-international`: 飞书国际版
- `wechatwork`: 企业微信
- `dingtalk`: 钉钉
- `active-directory`: Windows AD
- `ldap`: LDAP
- `italent`: 北森
- `maycur`: 每刻报销
- `moka`: Moka
- `fxiaoke`: 纷享销客
- `xiaoshouyi`: 销售易
- `kayang`: 嘉扬 HR
- `scim`: 自定义同步源
    
            sync_task_name (str): 同步任务名称
            organization_code (str): 此同步任务绑定的组织机构。针对上游同步，需执行一次同步任务之后才会绑定组织机构；针对下游同步，创建同步任务的时候就需要设置。
            provisioning_scope (dict): 同步范围，**只针对下游同步任务有效**。为空表示同步整个组织机构。
            timed_scheduler (dict): 定时同步时间设置
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-sync-task',
            json={
                'fieldMapping': field_mapping,
                'syncTaskTrigger': sync_task_trigger,
                'syncTaskFlow': sync_task_flow,
                'clientConfig': client_config,
                'syncTaskType': sync_task_type,
                'syncTaskName': sync_task_name,
                'organizationCode': organization_code,
                'provisioningScope': provisioning_scope,
                'timedScheduler': timed_scheduler,
            },
        )

    def update_sync_task(self, sync_task_id, sync_task_name=None, sync_task_type=None, client_config=None,
                         sync_task_flow=None, sync_task_trigger=None, organization_code=None, provisioning_scope=None,
                         field_mapping=None, timed_scheduler=None):
        """修改同步任务

        修改同步任务

        Attributes:
            sync_task_id (int): 同步任务 ID
            sync_task_name (str): 同步任务名称
            sync_task_type (str): 同步任务类型:
- `lark`: 飞书
- `lark-international`: 飞书国际版
- `wechatwork`: 企业微信
- `dingtalk`: 钉钉
- `active-directory`: Windows AD
- `ldap`: LDAP
- `italent`: 北森
- `maycur`: 每刻报销
- `moka`: Moka
- `fxiaoke`: 纷享销客
- `xiaoshouyi`: 销售易
- `kayang`: 嘉扬 HR
- `scim`: 自定义同步源
    
            client_config (dict): 同步任务配置信息
            sync_task_flow (str): 同步任务数据流向：
- `upstream`: 作为上游，将数据同步到 Authing
- `downstream`: 作为下游，将 Authing 数据同步到此系统
    
            sync_task_trigger (str): 同步任务触发类型：
- `manually`: 手动触发执行
- `timed`: 定时触发
- `automatic`: 根据事件自动触发

            organization_code (str): 此同步任务绑定的组织机构。针对上游同步，需执行一次同步任务之后才会绑定组织机构；针对下游同步，创建同步任务的时候就需要设置。
            provisioning_scope (dict): 同步范围，**只针对下游同步任务有效**。为空表示同步整个组织机构。
            field_mapping (list): 字段映射配置
            timed_scheduler (dict): 定时同步时间设置
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-sync-task',
            json={
                'syncTaskId': sync_task_id,
                'syncTaskName': sync_task_name,
                'syncTaskType': sync_task_type,
                'clientConfig': client_config,
                'syncTaskFlow': sync_task_flow,
                'syncTaskTrigger': sync_task_trigger,
                'organizationCode': organization_code,
                'provisioningScope': provisioning_scope,
                'fieldMapping': field_mapping,
                'timedScheduler': timed_scheduler,
            },
        )

    def trigger_sync_task(self, sync_task_id):
        """执行同步任务

        执行同步任务

        Attributes:
            sync_task_id (int): 同步任务 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/trigger-sync-task',
            json={
                'syncTaskId': sync_task_id,
            },
        )

    def get_sync_job(self, sync_job_id):
        """获取同步作业详情

        获取同步作业详情

        Attributes:
            syncJobId (int): 同步作业 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-sync-job',
            params={
                'syncJobId': sync_job_id,
            },
        )

    def list_sync_jobs(self, sync_task_id, page=None, limit=None, sync_trigger=None):
        """获取同步作业详情

        获取同步作业详情

        Attributes:
            syncTaskId (int): 同步任务 ID
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            syncTrigger (str): 同步任务触发类型：
- `manually`: 手动触发执行
- `timed`: 定时触发
- `automatic`: 根据事件自动触发

        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-sync-jobs',
            params={
                'syncTaskId': sync_task_id,
                'page': page,
                'limit': limit,
                'syncTrigger': sync_trigger,
            },
        )

    def list_sync_job_logs(self, sync_job_id, page=None, limit=None, success=None, action=None, object_type=None):
        """获取同步作业详情

        获取同步作业详情

        Attributes:
            syncJobId (int): 同步作业 ID
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            success (bool): 根据是否操作成功进行筛选
            action (str): 根据操作类型进行筛选：
- `CreateUser`: 创建用户
- `UpdateUser`: 修改用户信息
- `DeleteUser`: 删除用户
- `UpdateUserIdentifier`: 修改用户唯一标志符
- `ChangeUserDepartment`: 修改用户部门
- `CreateDepartment`: 创建部门
- `UpdateDepartment`: 修改部门信息
- `DeleteDepartment`: 删除部门
- `MoveDepartment`: 移动部门
- `UpdateDepartmentLeader`: 同步部门负责人
- `CreateGroup`: 创建分组
- `UpdateGroup`: 修改分组
- `DeleteGroup`: 删除分组
- `Updateless`: 无更新
    
            objectType (str): 操作对象类型:
- `department`: 部门
- `user`: 用户
    
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-sync-job-logs',
            params={
                'syncJobId': sync_job_id,
                'page': page,
                'limit': limit,
                'success': success,
                'action': action,
                'objectType': object_type,
            },
        )

    def list_sync_risk_operations(self, sync_task_id, page=None, limit=None, status=None, object_type=None):
        """获取同步风险操作列表

        获取同步风险操作列表

        Attributes:
            syncTaskId (int): 同步任务 ID
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            status (str): 根据执行状态筛选
            objectType (str): 根据操作对象类型，默认获取所有类型的记录：
- `department`: 部门
- `user`: 用户
    
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-sync-risk-operations',
            params={
                'syncTaskId': sync_task_id,
                'page': page,
                'limit': limit,
                'status': status,
                'objectType': object_type,
            },
        )

    def trigger_sync_risk_operations(self, sync_risk_operation_ids):
        """执行同步风险操作

        执行同步风险操作

        Attributes:
            sync_risk_operation_ids (list): 同步任务风险操作 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/trigger-sync-risk-operations',
            json={
                'syncRiskOperationIds': sync_risk_operation_ids,
            },
        )

    def cancel_sync_risk_operation(self, sync_risk_operation_ids):
        """取消同步风险操作

        取消同步风险操作

        Attributes:
            sync_risk_operation_ids (list): 同步任务风险操作 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/cancel-sync-risk-operation',
            json={
                'syncRiskOperationIds': sync_risk_operation_ids,
            },
        )

    def get_group(self, code, with_custom_data=None):
        """获取分组详情

        通过分组 code，获取分组详情。

        Attributes:
            code (str): 分组 code
            withCustomData (bool): 是否获取自定义数据
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-group',
            params={
                'code': code,
                'withCustomData': with_custom_data,
            },
        )

    def list_groups(self, keywords=None, page=None, limit=None, with_metadata=None, with_custom_data=None,
                    flat_custom_data=None):
        """获取分组列表

        获取分组列表，支持分页。

        Attributes:
            keywords (str): 搜索分组 code 或分组名称
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            withMetadata (bool): 是否展示元数据内容
            withCustomData (bool): 是否获取自定义数据
            flatCustomData (bool): 是否拍平扩展字段
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-groups',
            params={
                'keywords': keywords,
                'page': page,
                'limit': limit,
                'withMetadata': with_metadata,
                'withCustomData': with_custom_data,
                'flatCustomData': flat_custom_data,
            },
        )

    def get_all_groups(self, fetch_members=None, with_custom_data=None):
        """获取所有分组

        获取所有分组

        Attributes:
            fetchMembers (bool): 是否获取成员列表
            withCustomData (bool): 是否获取自定义数据
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-all-groups',
            params={
                'fetchMembers': fetch_members,
                'withCustomData': with_custom_data,
            },
        )

    def create_group(self, type, description, name, code, custom_data=None):
        """创建分组

        创建分组，一个分组必须包含分组名称与唯一标志符 code，且必须为一个合法的英文标志符，如 developers。

        Attributes:
            type (str): 分组类型
            description (str): 分组描述
            name (str): 分组名称
            code (str): 分组 code
            custom_data (dict): 自定义数据，传入的对象中的 key 必须先在用户池定义相关自定义字段
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-group',
            json={
                'type': type,
                'description': description,
                'name': name,
                'code': code,
                'customData': custom_data,
            },
        )

    def create_or_update_group(self, type, description, name, code):
        """创建或修改分组

        不存在时则创建，存在时则进行更新。

        Attributes:
            type (str): 分组类型
            description (str): 分组描述
            name (str): 分组名称
            code (str): 分组 code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-or-update-group',
            json={
                'type': type,
                'description': description,
                'name': name,
                'code': code,
            },
        )

    def create_groups_batch(self, list):
        """批量创建分组

        批量创建分组，一个分组必须包含分组名称与唯一标志符 code，且必须为一个合法的英文标志符，如 developers。

        Attributes:
            list (list): 批量分组
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-groups-batch',
            json={
                'list': list,
            },
        )

    def update_group(self, description, code, name=None, new_code=None, custom_data=None):
        """修改分组

        通过分组 code，修改分组，可以修改此分组的 code。

        Attributes:
            description (str): 分组描述
            code (str): 分组 code
            name (str): 分组名称
            new_code (str): 分组新的 code
            custom_data (dict): 自定义数据，传入的对象中的 key 必须先在用户池定义相关自定义字段
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-group',
            json={
                'description': description,
                'code': code,
                'name': name,
                'newCode': new_code,
                'customData': custom_data,
            },
        )

    def delete_groups_batch(self, code_list):
        """批量删除分组

        通过分组 code，批量删除分组。

        Attributes:
            code_list (list): 分组 code 列表
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-groups-batch',
            json={
                'codeList': code_list,
            },
        )

    def add_group_members(self, user_ids, code):
        """添加分组成员

        添加分组成员，成员以用户 ID 数组形式传递。

        Attributes:
            user_ids (list): 用户 ID 数组
            code (str): 分组 code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/add-group-members',
            json={
                'userIds': user_ids,
                'code': code,
            },
        )

    def remove_group_members(self, user_ids, code):
        """批量移除分组成员

        批量移除分组成员，成员以用户 ID 数组形式传递。

        Attributes:
            user_ids (list): 用户 ID 数组
            code (str): 分组 code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/remove-group-members',
            json={
                'userIds': user_ids,
                'code': code,
            },
        )

    def list_group_members(self, code, page=None, limit=None, with_custom_data=None, with_identities=None,
                           with_department_ids=None):
        """获取分组成员列表

        通过分组 code，获取分组成员列表，支持分页，可以获取自定义数据、identities、部门 ID 列表。

        Attributes:
            code (str): 分组 code
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            withCustomData (bool): 是否获取自定义数据
            withIdentities (bool): 是否获取 identities
            withDepartmentIds (bool): 是否获取部门 ID 列表
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-group-members',
            params={
                'code': code,
                'page': page,
                'limit': limit,
                'withCustomData': with_custom_data,
                'withIdentities': with_identities,
                'withDepartmentIds': with_department_ids,
            },
        )

    def get_group_authorized_resources(self, code, namespace=None, resource_type=None):
        """获取分组被授权的资源列表

        通过分组 code，获取分组被授权的资源列表，可以通过资源类型、权限分组 code 筛选。

        Attributes:
            code (str): 分组 code
            namespace (str): 所属权限分组(权限空间)的 Code
            resourceType (str): 资源类型
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-group-authorized-resources',
            params={
                'code': code,
                'namespace': namespace,
                'resourceType': resource_type,
            },
        )

    def get_role(self, code, namespace=None):
        """获取角色详情

        通过权限分组内角色 code，获取角色详情。

        Attributes:
            code (str): 权限分组(权限空间)内角色的唯一标识符
            namespace (str): 所属权限分组(权限空间)的 Code
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-role',
            params={
                'code': code,
                'namespace': namespace,
            },
        )

    def assign_role(self, targets, code, end_time=None, enable_time=None, namespace=None):
        """单个角色批量授权

        通过权限分组内角色 code，分配角色，被分配者可以是用户或部门。

        Attributes:
            targets (list): 目标对象
            code (str): 权限分组内角色的唯一标识符
            end_time (int): 主体过期时间毫秒值, 为 null 时永久有效
            enable_time (int): 主体加入时间毫秒值, 为 null 时立即加入
            namespace (str): 所属权限分组的 code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/assign-role',
            json={
                'targets': targets,
                'code': code,
                'endTime': end_time,
                'enableTime': enable_time,
                'namespace': namespace,
            },
        )

    def assign_role_batch(self, targets, roles):
        """批量分配角色

        批量分配角色，被分配者可以是用户，可以是部门

        Attributes:
            targets (list): 分配角色的目标列表
            roles (list): 角色信息列表
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/assign-role-batch',
            json={
                'targets': targets,
                'roles': roles,
            },
        )

    def revoke_role(self, targets, code, namespace=None):
        """移除分配的角色

        通过权限分组内角色 code，移除分配的角色，被分配者可以是用户或部门。

        Attributes:
            targets (list): 移除角色的目标
            code (str): 权限分组内角色的唯一标识符
            namespace (str): 所属权限分组的 code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/revoke-role',
            json={
                'targets': targets,
                'code': code,
                'namespace': namespace,
            },
        )

    def revoke_role_batch(self, targets, roles):
        """批量移除分配的角色

        批量移除分配的角色，被分配者可以是用户，可以是部门

        Attributes:
            targets (list): 移除角色的目标列表
            roles (list): 角色信息列表
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/revoke-role-batch',
            json={
                'targets': targets,
                'roles': roles,
            },
        )

    def get_role_authorized_resources(self, code, namespace=None, resource_type=None):
        """获取角色被授权的资源列表

        通过权限分组内角色 code，获取角色被授权的资源列表。

        Attributes:
            code (str): 权限分组内角色的唯一标识符
            namespace (str): 所属权限分组的 code
            resourceType (str): 资源类型，如 数据、API、按钮、菜单
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-role-authorized-resources',
            params={
                'code': code,
                'namespace': namespace,
                'resourceType': resource_type,
            },
        )

    def list_role_members(self, code, page=None, limit=None, with_custom_data=None, with_identities=None,
                          with_department_ids=None, namespace=None):
        """获取角色成员列表

        通过权限分组内内角色 code，获取角色成员列表，支持分页，可以选择或获取自定义数据、identities 等。

        Attributes:
            code (str): 权限分组内角色的唯一标识符
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            withCustomData (bool): 是否获取自定义数据
            withIdentities (bool): 是否获取 identities
            withDepartmentIds (bool): 是否获取部门 ID 列表
            namespace (str): 所属权限分组的 code
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-role-members',
            params={
                'page': page,
                'limit': limit,
                'withCustomData': with_custom_data,
                'withIdentities': with_identities,
                'withDepartmentIds': with_department_ids,
                'code': code,
                'namespace': namespace,
            },
        )

    def list_role_departments(self, code, namespace=None, page=None, limit=None):
        """获取角色的部门列表

        通过权限分组内角色 code，获取角色的部门列表，支持分页。

        Attributes:
            code (str): 权限分组内角色的唯一标识符
            namespace (str): 所属权限分组的 code
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-role-departments',
            params={
                'code': code,
                'namespace': namespace,
                'page': page,
                'limit': limit,
            },
        )

    def create_role(self, code, name=None, namespace=None, description=None, disable_time=None):
        """创建角色

        通过权限分组（权限空间）内角色 code，创建角色，可以选择权限分组、角色描述、角色名称等。

        Attributes:
            code (str): 权限分组（权限空间）内角色的唯一标识符
            name (str): 权限分组（权限空间）内角色名称
            namespace (str): 所属权限分组(权限空间)的 code
            description (str): 角色描述
            disable_time (str): 角色自动禁止时间，单位毫秒, 如果传null表示永久有效
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-role',
            json={
                'code': code,
                'name': name,
                'namespace': namespace,
                'description': description,
                'disableTime': disable_time,
            },
        )

    def list_roles(self, page=None, limit=None, keywords=None, namespace=None):
        """获取角色列表

        获取角色列表，支持分页、支持根据权限分组（权限空间）筛选

        Attributes:
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            keywords (str): 用于根据角色的 code 或者名称进行模糊搜索，可选。
            namespace (str): 所属权限分组(权限空间)的 code
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-roles',
            params={
                'page': page,
                'limit': limit,
                'keywords': keywords,
                'namespace': namespace,
            },
        )

    def delete_roles_batch(self, code_list, namespace=None):
        """单个权限分组（权限空间）内删除角色

        单个权限分组（权限空间）内删除角色，可以批量删除。

        Attributes:
            code_list (list): 角色 code 列表
            namespace (str): 所属权限分组(权限空间)的 code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-roles-batch',
            json={
                'codeList': code_list,
                'namespace': namespace,
            },
        )

    def create_roles_batch(self, list):
        """批量创建角色

        批量创建角色，可以选择权限分组、角色描述等。

        Attributes:
            list (list): 角色列表
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-roles-batch',
            json={
                'list': list,
            },
        )

    def update_role(self, name, new_code, code, namespace=None, description=None, status=None, disable_time=None):
        """修改角色

        通过权限分组(权限空间）内角色新旧 Code，修改角色，可以选择角色名称、角色描述等。

        Attributes:
            name (str): 权限分组（权限空间）角色名称
            new_code (str): 角色新的权限分组（权限空间）内唯一识别码
            code (str): 权限分组(权限空间）内角色的唯一标识符
            namespace (str): 所属权限分组(权限空间)的 code
            description (str): 角色描述
            status (str): 角色状态，ENABLE-表示正常，DISABLE-表示禁止
            disable_time (str): 角色自动禁止时间，单位毫秒, 如果传null表示永久有效
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-role',
            json={
                'name': name,
                'newCode': new_code,
                'code': code,
                'namespace': namespace,
                'description': description,
                'status': status,
                'disableTime': disable_time,
            },
        )

    def delete_roles(self, role_list):
        """跨权限分组（空间）删除角色

        跨权限分组（空间）删除角色，可以批量删除。

        Attributes:
            role_list (list): 角色 Code 和 namespace 列表
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/multiple-namespace-delete-roles-batch',
            json={
                'roleList': role_list,
            },
        )

    def check_params_namespace(self, code, namespace, name=None):
        """校验角色 Code 或者名称是否可用

        通过用户池 ID、权限空间 Code和角色 Code,或者用户池 ID、权限空间名称和角色名称查询是否可用。

        Attributes:
            code (str): 权限分组（权限空间）内角色的唯一标识符
            namespace (str): 所属权限分组(权限空间)的 Code
            name (str): 权限分组（权限空间）内角色名称
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/check-role-params',
            json={
                'code': code,
                'namespace': namespace,
                'name': name,
            },
        )

    def list_role_assignments(self, role_code, page=None, limit=None, query=None, namespace_code=None,
                              target_type=None):
        """获取角色授权列表

        获取角色授权列表。

        Attributes:
            roleCode (str): 角色 code,只能使用字母、数字和 -_，最多 50 字符
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            query (str): 按角色 Code 或者角色名称查询
            namespaceCode (str): 权限空间code
            targetType (str): 目标类型，接受用户，部门
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-role-assignments',
            params={
                'page': page,
                'limit': limit,
                'query': query,
                'roleCode': role_code,
                'namespaceCode': namespace_code,
                'targetType': target_type,
            },
        )

    def create_admin_role(self, name, code, description=None):
        """创建管理员角色

        通过角色 code、角色名称进行创建管理员角色，可以选择角色描述

        Attributes:
            name (str): 管理员角色名称
            code (str): 管理员角色的唯一标识符
            description (str): 角色描述
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-admin-role',
            json={
                'name': name,
                'code': code,
                'description': description,
            },
        )

    def delete_admin_roles_batch(self, code_list):
        """删除管理员自定义角色

        删除管理员自定义角色，支持批量删除。

        Attributes:
            code_list (list): 角色 code 列表
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-admin-roles',
            json={
                'codeList': code_list,
            },
        )

    def list_ext_idp(self, tenant_id=None, app_id=None):
        """获取身份源列表

        获取身份源列表，可以指定 租户 ID 筛选。

        Attributes:
            tenantId (str): 租户 ID
            appId (str): 应用 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-ext-idp',
            params={
                'tenantId': tenant_id,
                'appId': app_id,
            },
        )

    def get_ext_idp(self, id, tenant_id=None, app_id=None, type=None):
        """获取身份源详情

        通过 身份源 ID，获取身份源详情，可以指定 租户 ID 筛选。

        Attributes:
            id (str): 身份源 ID
            tenantId (str): 租户 ID
            appId (str): 应用 ID
            type (str): 身份源类型
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-ext-idp',
            params={
                'tenantId': tenant_id,
                'appId': app_id,
                'id': id,
                'type': type,
            },
        )

    def create_ext_idp(self, name, type, tenant_id=None):
        """创建身份源

        创建身份源，可以设置身份源名称、连接类型、租户 ID 等。

        Attributes:
            name (str): 身份源名称
            type (str): 身份源连接类型
            tenant_id (str): 租户 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-ext-idp',
            json={
                'name': name,
                'type': type,
                'tenantId': tenant_id,
            },
        )

    def update_ext_idp(self, name, id, tenant_id=None):
        """更新身份源配置

        更新身份源配置，可以设置身份源 ID 与 名称。

        Attributes:
            name (str): 名称
            id (str): 身份源 ID
            tenant_id (str): 租户 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-ext-idp',
            json={
                'name': name,
                'id': id,
                'tenantId': tenant_id,
            },
        )

    def delete_ext_idp(self, id, tenant_id=None):
        """删除身份源

        通过身份源 ID，删除身份源。

        Attributes:
            id (str): 身份源 ID
            tenant_id (str): 租户 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-ext-idp',
            json={
                'id': id,
                'tenantId': tenant_id,
            },
        )

    def create_ext_idp_conn(self, ext_idp_id, type, identifier, display_name, fields, login_only=None, logo=None,
                            tenant_id=None):
        """在某个已有身份源下创建新连接

        在某个已有身份源下创建新连接，可以设置身份源图标、是否只支持登录等。

        Attributes:
            ext_idp_id (str): 身份源连接 ID
            type (str): 身份源连接类型
            identifier (str): 身份源连接标识
            display_name (str): 连接在登录页的显示名称
            fields (dict): 连接的自定义配置信息
            login_only (bool): 是否只支持登录
            logo (str): 身份源图标
            tenant_id (str): 租户 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-ext-idp-conn',
            json={
                'extIdpId': ext_idp_id,
                'type': type,
                'identifier': identifier,
                'displayName': display_name,
                'fields': fields,
                'loginOnly': login_only,
                'logo': logo,
                'tenantId': tenant_id,
            },
        )

    def update_ext_idp_conn(self, id, display_name, fields, logo=None, login_only=None, tenant_id=None):
        """更新身份源连接

        更新身份源连接，可以设置身份源图标、是否只支持登录等。

        Attributes:
            id (str): 身份源连接 ID
            display_name (str): 身份源连接显示名称
            fields (dict): 身份源连接自定义参数（增量修改）
            logo (str): 身份源连接的图标
            login_only (bool): 是否只支持登录
            tenant_id (str): 租户 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-ext-idp-conn',
            json={
                'id': id,
                'displayName': display_name,
                'fields': fields,
                'logo': logo,
                'loginOnly': login_only,
                'tenantId': tenant_id,
            },
        )

    def delete_ext_idp_conn(self, id, tenant_id=None):
        """删除身份源连接

        通过身份源连接 ID，删除身份源连接。

        Attributes:
            id (str): 身份源连接 ID
            tenant_id (str): 租户 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-ext-idp-conn',
            json={
                'id': id,
                'tenantId': tenant_id,
            },
        )

    def change_ext_idp_conn_state(self, id, enabled, app_id, tenant_id=None, app_ids=None):
        """身份源连接开关

        身份源连接开关，可以打开或关闭身份源连接。

        Attributes:
            id (str): 身份源连接 ID
            enabled (bool): 是否开启身份源连接
            app_id (str): 应用 ID
            tenant_id (str): 租户 ID
            app_ids (list): 应用 ID 列表
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/change-ext-idp-conn-state',
            json={
                'id': id,
                'enabled': enabled,
                'appId': app_id,
                'tenantId': tenant_id,
                'appIds': app_ids,
            },
        )

    def change_ext_idp_conn_association_state(self, id, association, tenant_id=None):
        """租户关联身份源

        租户可以关联或取消关联身份源连接。

        Attributes:
            id (str): 身份源连接 ID
            association (bool): 是否关联身份源
            tenant_id (str): 租户 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/change-ext-idp-conn-association-state',
            json={
                'id': id,
                'association': association,
                'tenantId': tenant_id,
            },
        )

    def list_tenant_ext_idp(self, tenant_id=None, app_id=None, type=None, page=None, limit=None):
        """租户控制台获取身份源列表

        在租户控制台内获取身份源列表，可以根据 应用 ID 筛选。

        Attributes:
            tenantId (str): 租户 ID
            appId (str): 应用 ID
            type (str): 身份源类型
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-tenant-ext-idp',
            params={
                'tenantId': tenant_id,
                'appId': app_id,
                'type': type,
                'page': page,
                'limit': limit,
            },
        )

    def ext_idp_conn_state_by_apps(self, id, tenant_id=None, app_id=None, type=None):
        """身份源下应用的连接详情

        在身份源详情页获取应用的连接情况

        Attributes:
            id (str): 身份源 ID
            tenantId (str): 租户 ID
            appId (str): 应用 ID
            type (str): 身份源类型
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/ext-idp-conn-apps',
            params={
                'tenantId': tenant_id,
                'appId': app_id,
                'id': id,
                'type': type,
            },
        )

    def get_user_base_fields(self, ):
        """获取用户内置字段列表

        获取用户内置的字段列表

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-user-base-fields',
        )

    def list_user_base_fields(self, target_type, data_type, tenant_id=None, page=None, limit=None, user_visible=None,
                              admin_visible=None, access_control=None, keyword=None, lang=None):
        """获取用户内置字段列表

        获取用户内置的字段列表

        Attributes:
            targetType (str): 目标对象类型：
- `USER`: 用户
- `ROLE`: 角色
- `GROUP`: 分组
- `DEPARTMENT`: 部门
    ;该接口暂不支持分组(GROUP)
            dataType (str): 字段类型
            tenantId (str): 租户 ID
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            userVisible (bool): 用户是否可见
            adminVisible (bool): 管理员是否可见
            accessControl (bool): 访问控制
            keyword (str): 搜索关键词
            lang (str): 搜索语言
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-user-base-fields',
            params={
                'tenantId': tenant_id,
                'targetType': target_type,
                'dataType': data_type,
                'page': page,
                'limit': limit,
                'userVisible': user_visible,
                'adminVisible': admin_visible,
                'accessControl': access_control,
                'keyword': keyword,
                'lang': lang,
            },
        )

    def set_user_base_fields(self, list):
        """修改用户内置字段配置

        修改用户内置字段配置，内置字段不允许修改数据类型、唯一性。

        Attributes:
            list (list): 自定义字段列表
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/set-user-base-fields',
            json={
                'list': list,
            },
        )

    def get_custom_fields(self, target_type, tenant_id=None):
        """获取自定义字段列表

        通过主体类型，获取用户、部门或角色的自定义字段列表。

        Attributes:
            targetType (str): 目标对象类型：
- `USER`: 用户
- `ROLE`: 角色
- `GROUP`: 分组
- `DEPARTMENT`: 部门
    ;该接口暂不支持分组(GROUP)
            tenantId (str): 租户 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-custom-fields',
            params={
                'targetType': target_type,
                'tenantId': tenant_id,
            },
        )

    def list_cust_fields(self, target_type, data_type, tenant_id=None, page=None, limit=None, user_visible=None,
                         admin_visible=None, access_control=None, keyword=None, lang=None):
        """获取自定义字段列表

        通过主体类型，获取用户、部门或角色的自定义字段列表。

        Attributes:
            targetType (str): 目标对象类型：
- `USER`: 用户
- `ROLE`: 角色
- `GROUP`: 分组
- `DEPARTMENT`: 部门
    ;该接口暂不支持分组(GROUP)
            dataType (str): 字段类型
            tenantId (str): 租户 ID
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            userVisible (bool): 用户是否可见
            adminVisible (bool): 管理员是否可见
            accessControl (bool): 访问控制
            keyword (str): 搜索关键词
            lang (str): 搜索语言
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-custom-fields',
            params={
                'tenantId': tenant_id,
                'targetType': target_type,
                'dataType': data_type,
                'page': page,
                'limit': limit,
                'userVisible': user_visible,
                'adminVisible': admin_visible,
                'accessControl': access_control,
                'keyword': keyword,
                'lang': lang,
            },
        )

    def set_custom_fields(self, list, tenant_id=None):
        """创建/修改自定义字段定义

        创建/修改用户、部门或角色自定义字段定义，如果传入的 key 不存在则创建，存在则更新。

        Attributes:
            list (list): 自定义字段列表
            tenant_id (str): 租户 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/set-custom-fields',
            json={
                'list': list,
                'tenantId': tenant_id,
            },
        )

    def delete_custom_fields(self, tenant_id, list):
        """删除自定义字段定义

        删除用户、部门或角色自定义字段定义。

        Attributes:
            tenant_id (str): 租户 ID
            list (list): 自定义字段列表
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-custom-fields',
            json={
                'tenantId': tenant_id,
                'list': list,
            },
        )

    def set_custom_data(self, list, target_identifier, target_type, tenant_id=None, namespace=None):
        """设置自定义字段的值

        给用户、角色或部门设置自定义字段的值，如果存在则更新，不存在则创建。

        Attributes:
            list (list): 自定义数据列表
            target_identifier (str): 目标对象的唯一标志符：
- 如果是用户，为用户的 ID，如 `6343b98b7cfxxx9366e9b7c`
- 如果是角色，为角色的 code，如 `admin`
- 如果是分组，为分组的 code，如 `developer`
- 如果是部门，为部门的 ID，如 `6343bafc019xxxx889206c4c`
        
            target_type (str): 目标对象类型：
- `USER`: 用户
- `ROLE`: 角色
- `GROUP`: 分组
- `DEPARTMENT`: 部门
    
            tenant_id (str): 租户 ID
            namespace (str): 所属权限分组的 code，当 target_type 为角色的时候需要填写，否则可以忽略
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/set-custom-data',
            json={
                'list': list,
                'targetIdentifier': target_identifier,
                'targetType': target_type,
                'tenantId': tenant_id,
                'namespace': namespace,
            },
        )

    def get_custom_data(self, tenant_id, target_type, target_identifier, namespace=None):
        """获取用户、分组、角色、组织机构的自定义字段值

        通过筛选条件，获取用户、分组、角色、组织机构的自定义字段值。

        Attributes:
            tenantId (str): 租户 ID
            targetType (str): 目标对象类型：
- `USER`: 用户
- `ROLE`: 角色
- `GROUP`: 分组
- `DEPARTMENT`: 部门
    
            targetIdentifier (str): 目标对象的唯一标志符：
- 如果是用户，为用户的 ID，如 `6343b98b7cfxxx9366e9b7c`
- 如果是角色，为角色的 code，如 `admin`
- 如果是分组，为分组的 code，如 `developer`
- 如果是部门，为部门的 ID，如 `6343bafc019xxxx889206c4c`
        
            namespace (str): 所属权限分组的 code，当 targetType 为角色的时候需要填写，否则可以忽略
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-custom-data',
            params={
                'tenantId': tenant_id,
                'targetType': target_type,
                'targetIdentifier': target_identifier,
                'namespace': namespace,
            },
        )

    def create_resource(self, type, code, description=None, name=None, actions=None, api_identifier=None,
                        namespace=None):
        """创建资源

        创建资源，可以设置资源的描述、定义的操作类型、URL 标识等。

        Attributes:
            type (str): 资源类型，如数据、API、按钮、菜单
            code (str): 资源唯一标志符
            description (str): 资源描述
            name (str): 资源名称
            actions (list): 资源定义的操作类型
            api_identifier (str): API 资源的 URL 标识
            namespace (str): 所属权限分组(权限空间)的 Code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-resource',
            json={
                'type': type,
                'code': code,
                'description': description,
                'name': name,
                'actions': actions,
                'apiIdentifier': api_identifier,
                'namespace': namespace,
            },
        )

    def create_resources_batch(self, list, namespace=None):
        """批量创建资源

        批量创建资源，可以设置资源的描述、定义的操作类型、URL 标识等。

        Attributes:
            list (list): 资源列表
            namespace (str): 所属权限分组(权限空间)的 Code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-resources-batch',
            json={
                'list': list,
                'namespace': namespace,
            },
        )

    def get_resource(self, code, namespace=None):
        """获取资源详情

        根据筛选条件，获取资源详情。

        Attributes:
            code (str): 资源唯一标志符
            namespace (str): 所属权限分组(权限空间)的 Code
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-resource',
            params={
                'code': code,
                'namespace': namespace,
            },
        )

    def get_resources_batch(self, code_list, namespace=None):
        """批量获取资源详情

        根据筛选条件，批量获取资源详情。

        Attributes:
            codeList (str): 资源 code 列表，批量可以使用逗号分隔
            namespace (str): 所属权限分组(权限空间)的 Code
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-resources-batch',
            params={
                'namespace': namespace,
                'codeList': code_list,
            },
        )

    def list_common_resource(self, page=None, limit=None, keyword=None, namespace_code_list=None):
        """分页获取常规资源列表

        根据筛选条件，分页获取常规资源详情列表。

        Attributes:
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            keyword (str): 查询条件
            namespaceCodeList (str): 权限空间列表
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-common-resource',
            params={
                'page': page,
                'limit': limit,
                'keyword': keyword,
                'namespaceCodeList': namespace_code_list,
            },
        )

    def list_resources(self, namespace=None, type=None, page=None, limit=None):
        """分页获取资源列表

        根据筛选条件，分页获取资源详情列表。

        Attributes:
            namespace (str): 所属权限分组(权限空间)的 Code
            type (str): 资源类型
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-resources',
            params={
                'namespace': namespace,
                'type': type,
                'page': page,
                'limit': limit,
            },
        )

    def update_resource(self, code, description=None, name=None, actions=None, api_identifier=None, namespace=None,
                        type=None):
        """修改资源

        修改资源，可以设置资源的描述、定义的操作类型、URL 标识等。

        Attributes:
            code (str): 资源唯一标志符
            description (str): 资源描述
            name (str): 资源名称
            actions (list): 资源定义的操作类型
            api_identifier (str): API 资源的 URL 标识
            namespace (str): 所属权限分组(权限空间)的 Code
            type (str): 资源类型，如数据、API、按钮、菜单
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-resource',
            json={
                'code': code,
                'description': description,
                'name': name,
                'actions': actions,
                'apiIdentifier': api_identifier,
                'namespace': namespace,
                'type': type,
            },
        )

    def delete_resource(self, code, namespace=None):
        """删除资源

        通过资源唯一标志符以及所属权限分组，删除资源。

        Attributes:
            code (str): 资源唯一标志符
            namespace (str): 所属权限分组(权限空间)的 Code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-resource',
            json={
                'code': code,
                'namespace': namespace,
            },
        )

    def delete_resources_batch(self, namespace=None, code_list=None, ids=None):
        """批量删除资源

        通过资源唯一标志符以及所属权限分组，批量删除资源

        Attributes:
            namespace (str): 所属权限分组(权限空间)的 Code
            code_list (list): 资源 Code 列表
            ids (list): 资源 Id 列表
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-resources-batch',
            json={
                'namespace': namespace,
                'codeList': code_list,
                'ids': ids,
            },
        )

    def batch_delete_common_resource(self, ids):
        """批量删除资源

        通过资源id批量删除资源

        Attributes:
            ids (list): 资源 id 列表
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-common-resources-batch',
            json={
                'ids': ids,
            },
        )

    def associate_tenant_resource(self, code, association, app_id, tenant_id=None):
        """关联/取消关联应用资源到租户

        通过资源唯一标识以及权限分组，关联或取消关联资源到租户

        Attributes:
            code (str): 资源 Code
            association (bool): 是否关联应用资源
            app_id (str): 应用 ID
            tenant_id (str): 租户 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/associate-tenant-resource',
            json={
                'code': code,
                'association': association,
                'appId': app_id,
                'tenantId': tenant_id,
            },
        )

    def create_namespace(self, code, name=None, description=None):
        """创建权限分组

        创建权限分组，可以设置权限分组名称、Code 和描述信息。

        Attributes:
            code (str): 权限分组唯一标志符
            name (str): 权限分组名称
            description (str): 权限分组描述信息
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-namespace',
            json={
                'code': code,
                'name': name,
                'description': description,
            },
        )

    def create_namespaces_batch(self, list):
        """批量创建权限分组

        批量创建权限分组，可以分别设置权限分组名称、Code 和描述信息。

        Attributes:
            list (list): 权限分组列表
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-namespaces-batch',
            json={
                'list': list,
            },
        )

    def get_namespace(self, code):
        """获取权限分组详情

        通过权限分组唯一标志符(Code)，获取权限分组详情。

        Attributes:
            code (str): 权限分组唯一标志符
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-namespace',
            params={
                'code': code,
            },
        )

    def get_namespaces_batch(self, code_list):
        """批量获取权限分组详情

        分别通过权限分组唯一标志符(Code)，批量获取权限分组详情。

        Attributes:
            codeList (str): 权限分组 code 列表，批量可以使用逗号分隔
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-namespaces-batch',
            params={
                'codeList': code_list,
            },
        )

    def update_namespace(self, code, description=None, name=None, new_code=None):
        """修改权限分组信息

        修改权限分组信息，可以修改名称、描述信息以及新的唯一标志符(NewCode)。

        Attributes:
            code (str): 权限分组唯一标志符
            description (str): 权限分组描述信息
            name (str): 权限分组名称
            new_code (str): 权限分组新的唯一标志符
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-namespace',
            json={
                'code': code,
                'description': description,
                'name': name,
                'newCode': new_code,
            },
        )

    def delete_namespace(self, code):
        """删除权限分组信息

        通过权限分组唯一标志符(Code)，删除权限分组信息。

        Attributes:
            code (str): 权限分组唯一标志符
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-namespace',
            json={
                'code': code,
            },
        )

    def delete_namespaces_batch(self, code_list):
        """批量删除权限分组

        分别通过权限分组唯一标志符(Code)，批量删除权限分组。

        Attributes:
            code_list (list): 权限分组 code 列表
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-namespaces-batch',
            json={
                'codeList': code_list,
            },
        )

    def list_namespaces(self, page=None, limit=None, keywords=None):
        """分页获取权限分组列表

        根据筛选条件，分页获取权限分组列表。

        Attributes:
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            keywords (str): 搜索权限分组 Code
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-namespaces',
            params={
                'page': page,
                'limit': limit,
                'keywords': keywords,
            },
        )

    def list_namespace_roles(self, code, page=None, limit=None, keywords=None):
        """分页权限分组下所有的角色列表

        根据筛选条件，分页获取权限分组下所有的角色列表。

        Attributes:
            code (str): 权限分组唯一标志符
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            keywords (str): 角色 Code 或者名称
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-namespace-roles',
            params={
                'page': page,
                'limit': limit,
                'code': code,
                'keywords': keywords,
            },
        )

    def authorize_resources(self, list, namespace=None):
        """授权资源

        将一个/多个资源授权给用户、角色、分组、组织机构等主体，且可以分别指定不同的操作权限。

        Attributes:
            list (list): 授权资源列表
            namespace (str): 所属权限分组(权限空间)的 Code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/authorize-resources',
            json={
                'list': list,
                'namespace': namespace,
            },
        )

    def get_authorized_resources(self, target_type, target_identifier, namespace=None, resource_type=None,
                                 resource_list=None, with_denied=None):
        """获取某个主体被授权的资源列表

        根据筛选条件，获取某个主体被授权的资源列表。

        Attributes:
            targetType (str): 目标对象类型：
- `USER`: 用户
- `ROLE`: 角色
- `GROUP`: 分组
- `DEPARTMENT`: 部门
    
            targetIdentifier (str): 目标对象的唯一标志符：
- 如果是用户，为用户的 ID，如 `6343b98b7cfxxx9366e9b7c`
- 如果是角色，为角色的 code，如 `admin`
- 如果是分组，为分组的 code，如 `developer`
- 如果是部门，为部门的 ID，如 `6343bafc019xxxx889206c4c`
        
            namespace (str): 所属权限分组(权限空间)的 Code
            resourceType (str): 限定资源类型，如数据、API、按钮、菜单
            resourceList (str): 限定查询的资源列表，如果指定，只会返回所指定的资源列表。

resourceList 参数支持前缀匹配，例如：
- 授权了一个资源为 `books:123`，可以通过 `books:*` 来匹配；
- 授权了一个资源为 `books:fictions_123`，可以通过 `books:fictions_` 来匹配；

            withDenied (bool): 是否获取被拒绝的资源
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-authorized-resources',
            params={
                'targetType': target_type,
                'targetIdentifier': target_identifier,
                'namespace': namespace,
                'resourceType': resource_type,
                'resourceList': resource_list,
                'withDenied': with_denied,
            },
        )

    def is_action_allowed(self, user_id, action, resource, namespace=None):
        """判断用户是否对某个资源的某个操作有权限

        判断用户是否对某个资源的某个操作有权限。

        Attributes:
            user_id (str): 用户 ID
            action (str): 资源对应的操作
            resource (str): 资源标识符
            namespace (str): 所属权限分组(权限空间)的 Code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/is-action-allowed',
            json={
                'userId': user_id,
                'action': action,
                'resource': resource,
                'namespace': namespace,
            },
        )

    def get_resource_authorized_targets(self, resource, namespace=None, target_type=None, page=None, limit=None):
        """获取资源被授权的主体

        获取资源被授权的主体

        Attributes:
            resource (str): 资源
            namespace (str): 权限分组
            target_type (str): 目标对象类型：
- `USER`: 用户
- `ROLE`: 角色
- `GROUP`: 分组
- `DEPARTMENT`: 部门
    
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-resource-authorized-targets',
            json={
                'resource': resource,
                'namespace': namespace,
                'targetType': target_type,
                'page': page,
                'limit': limit,
            },
        )

    def get_user_action_logs(self, request_id=None, client_ip=None, event_type=None, user_id=None, app_id=None,
                             start=None, end=None, success=None, pagination=None):
        """获取用户行为日志

        可以选择请求 ID、客户端 IP、用户 ID、应用 ID、开始时间戳、请求是否成功、分页参数来获取用户行为日志

        Attributes:
            request_id (str): 请求 ID
            client_ip (str): 客户端 IP
            event_type (str): 事件类型，用户的一系列操作，比如 login、logout、register、verifyMfa 等
            user_id (str): 用户 ID
            app_id (str): 应用 ID
            start (int): 开始时间戳
            end (int): 结束时间戳
            success (bool): 请求是否成功
            pagination (dict): 分页
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-user-action-logs',
            json={
                'requestId': request_id,
                'clientIp': client_ip,
                'eventType': event_type,
                'userId': user_id,
                'appId': app_id,
                'start': start,
                'end': end,
                'success': success,
                'pagination': pagination,
            },
        )

    def get_admin_audit_logs(self, request_id=None, client_ip=None, operation_type=None, resource_type=None,
                             user_id=None, success=None, start=None, end=None, pagination=None):
        """获取管理员操作日志

        可以选择请求 ID、客户端 IP、操作类型、资源类型、管理员用户 ID、请求是否成功、开始时间戳、结束时间戳、分页来获取管理员操作日志接口

        Attributes:
            request_id (str): 请求 ID
            client_ip (str): 客户端 IP
            operation_type (str): 操作类型，例如 create、update、delete、login 等
            resource_type (str): 资源类型，例如 DATA、API、BUTTON 等
            user_id (str): 管理员用户 ID
            success (bool): 请求是否成功
            start (int): 开始时间戳
            end (int): 结束时间戳
            pagination (dict): 分页
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-admin-audit-logs',
            json={
                'requestId': request_id,
                'clientIp': client_ip,
                'operationType': operation_type,
                'resourceType': resource_type,
                'userId': user_id,
                'success': success,
                'start': start,
                'end': end,
                'pagination': pagination,
            },
        )

    def get_email_templates(self, ):
        """获取邮件模版列表

        获取邮件模版列表

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-email-templates',
        )

    def update_email_template(self, content, sender, subject, name, customize_enabled, type, expires_in=None,
                              redirect_to=None, tpl_engine=None):
        """修改邮件模版

        修改邮件模版

        Attributes:
            content (str): 邮件内容模版
            sender (str): 邮件发件人名称
            subject (str): 邮件主题
            name (str): 邮件模版名称
            customize_enabled (bool): 是否启用自定义模版
            type (str): 模版类型:
- `WELCOME_EMAIL`: 欢迎邮件
- `FIRST_CREATED_USER`: 首次创建用户通知
- `REGISTER_VERIFY_CODE`: 注册验证码
- `LOGIN_VERIFY_CODE`: 登录验证码
- `MFA_VERIFY_CODE`: MFA 验证码
- `INFORMATION_COMPLETION_VERIFY_CODE`: 注册信息补全验证码
- `FIRST_EMAIL_LOGIN_VERIFY`: 首次邮箱登录验证
- `CONSOLE_CONDUCTED_VERIFY`: 在控制台发起邮件验证
- `USER_PASSWORD_UPDATE_REMIND`: 用户到期提醒
- `ADMIN_RESET_USER_PASSWORD_NOTIFICATION`: 管理员重置用户密码成功通知
- `USER_PASSWORD_RESET_NOTIFICATION`: 用户密码重置成功通知
- `RESET_PASSWORD_VERIFY_CODE`: 重置密码验证码
- `SELF_UNLOCKING_VERIFY_CODE`: 自助解锁验证码
- `EMAIL_BIND_VERIFY_CODE`: 绑定邮箱验证码
- `EMAIL_UNBIND_VERIFY_CODE`: 解绑邮箱验证码
    
            expires_in (int): 验证码/邮件有效时间，只有验证类邮件才有有效时间。
            redirect_to (str): 完成邮件验证之后跳转到的地址，只针对 `FIRST_EMAIL_LOGIN_VERIFY` 和 `CONSOLE_CONDUCTED_VERIFY` 类型的模版有效。
            tpl_engine (str): 模版渲染引擎。Authing 邮件模版目前支持两种渲染引擎：
- `handlebar`: 详细使用方法请见：[handlebars 官方文档](https://handlebarsjs.com/)
- `ejs`: 详细使用方法请见：[ejs 官方文档](https://ejs.co/)

默认将使用 `handlerbar` 作为模版渲染引擎。
    
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-email-template',
            json={
                'content': content,
                'sender': sender,
                'subject': subject,
                'name': name,
                'customizeEnabled': customize_enabled,
                'type': type,
                'expiresIn': expires_in,
                'redirectTo': redirect_to,
                'tplEngine': tpl_engine,
            },
        )

    def preview_email_template(self, type, content=None, subject=None, sender=None, expires_in=None, tpl_engine=None):
        """预览邮件模版

        预览邮件模版

        Attributes:
            type (str): 模版类型:
- `WELCOME_EMAIL`: 欢迎邮件
- `FIRST_CREATED_USER`: 首次创建用户通知
- `REGISTER_VERIFY_CODE`: 注册验证码
- `LOGIN_VERIFY_CODE`: 登录验证码
- `MFA_VERIFY_CODE`: MFA 验证码
- `INFORMATION_COMPLETION_VERIFY_CODE`: 注册信息补全验证码
- `FIRST_EMAIL_LOGIN_VERIFY`: 首次邮箱登录验证
- `CONSOLE_CONDUCTED_VERIFY`: 在控制台发起邮件验证
- `USER_PASSWORD_UPDATE_REMIND`: 用户到期提醒
- `ADMIN_RESET_USER_PASSWORD_NOTIFICATION`: 管理员重置用户密码成功通知
- `USER_PASSWORD_RESET_NOTIFICATION`: 用户密码重置成功通知
- `RESET_PASSWORD_VERIFY_CODE`: 重置密码验证码
- `SELF_UNLOCKING_VERIFY_CODE`: 自助解锁验证码
- `EMAIL_BIND_VERIFY_CODE`: 绑定邮箱验证码
- `EMAIL_UNBIND_VERIFY_CODE`: 解绑邮箱验证码
    
            content (str): 邮件内容模版，可选，如果不传默认使用用户池配置的邮件模版进行渲染。
            subject (str): 邮件主题，可选，如果不传默认使用用户池配置的邮件模版进行渲染。
            sender (str): 邮件发件人名称，可选，如果不传默认使用用户池配置的邮件模版进行渲染。
            expires_in (int): 验证码/邮件有效时间，只有验证类邮件才有有效时间。可选，如果不传默认使用用户池配置的邮件模版进行渲染。
            tpl_engine (str): 模版渲染引擎。Authing 邮件模版目前支持两种渲染引擎：
- `handlebar`: 详细使用方法请见：[handlebars 官方文档](https://handlebarsjs.com/)
- `ejs`: 详细使用方法请见：[ejs 官方文档](https://ejs.co/)

默认将使用 `handlerbar` 作为模版渲染引擎。
    
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/preview-email-template',
            json={
                'type': type,
                'content': content,
                'subject': subject,
                'sender': sender,
                'expiresIn': expires_in,
                'tplEngine': tpl_engine,
            },
        )

    def get_email_provider(self, ):
        """获取第三方邮件服务配置

        获取第三方邮件服务配置

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-email-provider',
        )

    def config_email_provider(self, type, enabled, smtp_config=None, send_grid_config=None, ali_exmail_config=None,
                              tencent_exmail_config=None):
        """配置第三方邮件服务

        配置第三方邮件服务

        Attributes:
            type (str): 第三方邮件服务商类型:
- `custom`: 自定义 SMTP 邮件服务
- `ali`: [阿里企业邮箱](https://www.ali-exmail.cn/Land/)
- `qq`: [腾讯企业邮箱](https://work.weixin.qq.com/mail/)
- `sendgrid`: [SendGrid 邮件服务](https://sendgrid.com/)
    
            enabled (bool): 是否启用，如果不启用，将默认使用 Authing 内置的邮件服务
            smtp_config (dict): SMTP 邮件服务配置
            send_grid_config (dict): SendGrid 邮件服务配置
            ali_exmail_config (dict): 阿里企业邮件服务配置
            tencent_exmail_config (dict): 腾讯企业邮件服务配置
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/config-email-provider',
            json={
                'type': type,
                'enabled': enabled,
                'smtpConfig': smtp_config,
                'sendGridConfig': send_grid_config,
                'aliExmailConfig': ali_exmail_config,
                'tencentExmailConfig': tencent_exmail_config,
            },
        )

    def get_application(self, app_id):
        """获取应用详情

        通过应用 ID，获取应用详情。

        Attributes:
            appId (str): 应用 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-application',
            params={
                'appId': app_id,
            },
        )

    def detail_auth_subject(self, target_id, target_type, app_id):
        """主体授权详情

        主体授权详情

        Attributes:
            targetId (str): 主体 id
            targetType (str): 主体类型
            appId (str): 应用 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-subject-auth-detail',
            params={
                'targetId': target_id,
                'targetType': target_type,
                'appId': app_id,
            },
        )

    def list_auth_subject(self, target_type, target_id, app_name=None, app_type_list=None, effect=None, enabled=None):
        """主体授权列表

        主体授权列表

        Attributes:
            target_type (str): 主体类型
            target_id (str): 主体 id
            app_name (str): 应用名称
            app_type_list (list): 应用类型列表
            effect (list): 操作类型列表
            enabled (bool): 开关
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/list-subject-auth',
            json={
                'targetType': target_type,
                'targetId': target_id,
                'appName': app_name,
                'appTypeList': app_type_list,
                'effect': effect,
                'enabled': enabled,
            },
        )

    def list_auth_application(self, app_id, page=None, limit=None, target_name=None, target_type_list=None, effect=None,
                              enabled=None):
        """应用授权列表

        应用授权列表

        Attributes:
            app_id (str): 应用 ID
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            target_name (str): 主体名称
            target_type_list (list): 主体类型列表, USER/ORG/ROLE/GROUP
            effect (str): 操作，ALLOW/DENY
            enabled (bool): 授权是否生效开关,
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/list-applications-auth',
            json={
                'appId': app_id,
                'page': page,
                'limit': limit,
                'targetName': target_name,
                'targetTypeList': target_type_list,
                'effect': effect,
                'enabled': enabled,
            },
        )

    def enabled_auth(self, enabled, id):
        """更新授权开关

        更新授权开关

        Attributes:
            enabled (bool): 授权是否生效开关,
            id (str): 授权 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-auth-enabled',
            json={
                'enabled': enabled,
                'id': id,
            },
        )

    def delete_auth(self, auth_ids):
        """批量删除应用授权

        批量删除应用授权

        Attributes:
            authIds (str): 授权 ID
        """
        return self.http_client.request(
            method='DELETE',
            url='/api/v3/batch-applications-auth',
            params={
                'authIds': auth_ids,
            },
        )

    def list_applications(self, page=None, limit=None, is_integrate_app=None, is_self_built_app=None, sso_enabled=None,
                          keywords=None, all=None):
        """获取应用列表

        获取应用列表

        Attributes:
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            isIntegrateApp (bool): 是否为集成应用
            isSelfBuiltApp (bool): 是否为自建应用
            ssoEnabled (bool): 是否开启单点登录
            keywords (str): 模糊搜索字符串
            all (bool): 搜索应用，true：搜索所有应用, 默认为 false
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-applications',
            params={
                'page': page,
                'limit': limit,
                'isIntegrateApp': is_integrate_app,
                'isSelfBuiltApp': is_self_built_app,
                'ssoEnabled': sso_enabled,
                'keywords': keywords,
                'all': all,
            },
        )

    def get_application_simple_info(self, app_id):
        """获取应用简单信息

        通过应用 ID，获取应用简单信息。

        Attributes:
            appId (str): 应用 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-application-simple-info',
            params={
                'appId': app_id,
            },
        )

    def list_application_simple_info(self, page=None, limit=None, is_integrate_app=None, is_self_built_app=None,
                                     sso_enabled=None, keywords=None):
        """获取应用简单信息列表

        获取应用简单信息列表

        Attributes:
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            isIntegrateApp (bool): 是否为集成应用
            isSelfBuiltApp (bool): 是否为自建应用
            ssoEnabled (bool): 是否开启单点登录
            keywords (str): 模糊搜索字符串
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-application-simple-info',
            params={
                'page': page,
                'limit': limit,
                'isIntegrateApp': is_integrate_app,
                'isSelfBuiltApp': is_self_built_app,
                'ssoEnabled': sso_enabled,
                'keywords': keywords,
            },
        )

    def create_application(self, app_name, template=None, template_data=None, app_identifier=None, app_logo=None,
                           app_description=None, app_type=None, default_protocol=None, redirect_uris=None,
                           logout_redirect_uris=None, init_login_uri=None, sso_enabled=None, oidc_config=None,
                           saml_provider_enabled=None, saml_config=None, oauth_provider_enabled=None, oauth_config=None,
                           cas_provider_enabled=None, cas_config=None, login_config=None, register_config=None,
                           branding_config=None):
        """创建应用

        创建应用

        Attributes:
            app_name (str): 应用名称
            template (str): 集成应用模版类型，**集成应用必填**。集成应用只需要填 `template` 和 `templateData` 两个字段，其他的字段将被忽略。
            template_data (str): 集成应用配置信息，**集成应用必填**。
            app_identifier (str): 应用唯一标志，**自建应用必填**。
            app_logo (str): 应用 Logo 链接
            app_description (str): 应用描述信息
            app_type (str): 应用类型
            default_protocol (str): 默认应用协议类型
            redirect_uris (list): 应用登录回调地址
            logout_redirect_uris (list): 应用退出登录回调地址
            init_login_uri (str): 发起登录地址：在 Authing 应用详情点击「体验登录」或在应用面板点击该应用图标时，会跳转到此 URL，默认为 Authing 登录页。
            sso_enabled (bool): 是否开启 SSO 单点登录
            oidc_config (dict): OIDC 协议配置
            saml_provider_enabled (bool): 是否开启 SAML 身份提供商
            saml_config (dict): SAML 协议配置
            oauth_provider_enabled (bool): 是否开启 OAuth 身份提供商
            oauth_config (dict): OAuth2.0 协议配置。【重要提示】不再推荐使用 OAuth2.0，建议切换到 OIDC。
            cas_provider_enabled (bool): 是否开启 CAS 身份提供商
            cas_config (dict): CAS 协议配置
            login_config (dict): 登录配置
            register_config (dict): 注册配置
            branding_config (dict): 品牌化配置
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-application',
            json={
                'appName': app_name,
                'template': template,
                'templateData': template_data,
                'appIdentifier': app_identifier,
                'appLogo': app_logo,
                'appDescription': app_description,
                'appType': app_type,
                'defaultProtocol': default_protocol,
                'redirectUris': redirect_uris,
                'logoutRedirectUris': logout_redirect_uris,
                'initLoginUri': init_login_uri,
                'ssoEnabled': sso_enabled,
                'oidcConfig': oidc_config,
                'samlProviderEnabled': saml_provider_enabled,
                'samlConfig': saml_config,
                'oauthProviderEnabled': oauth_provider_enabled,
                'oauthConfig': oauth_config,
                'casProviderEnabled': cas_provider_enabled,
                'casConfig': cas_config,
                'loginConfig': login_config,
                'registerConfig': register_config,
                'brandingConfig': branding_config,
            },
        )

    def delete_application(self, app_id):
        """删除应用

        通过应用 ID，删除应用。

        Attributes:
            app_id (str): 应用 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-application',
            json={
                'appId': app_id,
            },
        )

    def get_application_secret(self, app_id):
        """获取应用密钥

        获取应用密钥

        Attributes:
            appId (str): 应用 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-application-secret',
            params={
                'appId': app_id,
            },
        )

    def refresh_application_secret(self, app_id):
        """刷新应用密钥

        刷新应用密钥

        Attributes:
            app_id (str): 应用 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/refresh-application-secret',
            json={
                'appId': app_id,
            },
        )

    def list_application_active_users(self, app_id, options=None):
        """获取应用当前登录用户

        获取应用当前处于登录状态的用户

        Attributes:
            app_id (str): 应用 ID
            options (dict): 可选项
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/list-application-active-users',
            json={
                'appId': app_id,
                'options': options,
            },
        )

    def get_application_permission_strategy(self, app_id):
        """获取应用默认访问授权策略

        获取应用默认访问授权策略

        Attributes:
            appId (str): 应用 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-application-permission-strategy',
            params={
                'appId': app_id,
            },
        )

    def update_application_permission_strategy(self, permission_strategy, app_id):
        """更新应用默认访问授权策略

        更新应用默认访问授权策略

        Attributes:
            permission_strategy (str): 应用访问授权策略
            app_id (str): 应用 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-application-permission-strategy',
            json={
                'permissionStrategy': permission_strategy,
                'appId': app_id,
            },
        )

    def authorize_application_access(self, app_id, list):
        """授权应用访问权限

        给用户、分组、组织或角色授权应用访问权限，如果用户、分组、组织或角色不存在，则跳过，进行下一步授权，不返回报错

        Attributes:
            app_id (str): 应用 ID
            list (list): 授权主体列表，最多 10 条
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/authorize-application-access',
            json={
                'appId': app_id,
                'list': list,
            },
        )

    def revoke_application_access(self, app_id, list):
        """删除应用访问授权记录

        取消给用户、分组、组织或角色的应用访问权限授权,如果传入数据不存在，则返回数据不报错处理。

        Attributes:
            app_id (str): 应用 ID
            list (list): 授权主体列表，最多 10 条
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/revoke-application-access',
            json={
                'appId': app_id,
                'list': list,
            },
        )

    def check_domain_available(self, domain):
        """检测域名是否可用

        检测域名是否可用于创建新应用或更新应用域名

        Attributes:
            domain (str): 域名
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/check-domain-available',
            json={
                'domain': domain,
            },
        )

    def list_tenant_applications(self, page, limit, keywords, sso_enabled):
        """获取租户应用列表

        获取应用列表，可以指定 租户 ID 筛选。

        Attributes:
            page (str): 获取应用列表的页码
            limit (str): 每页获取的应用数量
            keywords (str): 搜索关键字
            sso_enabled (bool): 应用是否加入单点登录
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-tenant-applications',
            params={
                'page': page,
                'limit': limit,
                'keywords': keywords,
                'sso_enabled': sso_enabled,
            },
        )

    def update_login_page_config(self, update):
        """更新应用登录页配置

        通过应用 ID 更新登录页配置。

        Attributes:
            update (dict): 应用登录配置更新内容
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-login-page-config',
            json={
                'update': update,
            },
        )

    def userpoll_tenant_config(self, ):
        """获取用户池租户配置信息

        根据用户池 ID 获取用户池多租户配置信息

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/userpool-tenant-config',
        )

    def update_user_pool_tenant_config(self, update):
        """更新用户池租户配置信息

        更新用户池多租户配置内登录信息

        Attributes:
            update (dict): 应用登录配置更新内容
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-userpool-tenant-config',
            json={
                'update': update,
            },
        )

    def update_tenant_qr_code_state(self, enabled):
        """更新租户控制台扫码登录状态

        更新租户控制台扫码登录状态

        Attributes:
            enabled (bool): 是否允许开启扫码登录
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-userpool-tenant-appqrcode-state',
            json={
                'enabled': enabled,
            },
        )

    def change_userpool_tenan_ext_idp_conn_state(self, enabled, conn_ids):
        """设置用户池多租户身份源连接

        设置用户池多租户身份源连接，支持同时设置多个身份源连接，支持设置连接和取消连接

        Attributes:
            enabled (bool): 是否开启身份源连接
            conn_ids (list): 身份源连接 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/change-userpool-tenant-ext-idp-conn-state',
            json={
                'enabled': enabled,
                'connIds': conn_ids,
            },
        )

    def update_application_mfa_settings(self, app_id, enabled_factors=None, disabled_factors=None):
        """修改应用多因素认证配置

        传入 MFA 认证因素列表进行开启或关闭

        Attributes:
            app_id (str): 所属应用 ID
            enabled_factors (list): 开启的 MFA 认证因素列表
            disabled_factors (list): 关闭的 MFA 认证因素列表
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-application-mfa-settings',
            json={
                'appId': app_id,
                'enabledFactors': enabled_factors,
                'disabledFactors': disabled_factors,
            },
        )

    def get_mfa_trigger_data(self, app_id, user_id, user_id_type=None):
        """获取应用下用户 MFA 触发数据

        获取应用下用户 MFA 触发数据。

        Attributes:
            appId (str): 所属应用 ID
            userId (str): 用户唯一标志，可以是用户 ID、用户名、邮箱、手机号、外部 ID、在外部身份源的 ID。
            userIdType (str): 用户 ID 类型，默认值为 `user_id`，可选值为：
- `user_id`: Authing 用户 ID，如 `6319a1504f3xxxxf214dd5b7`
- `phone`: 用户手机号
- `email`: 用户邮箱
- `username`: 用户名
- `external_id`: 用户在外部系统的 ID，对应 Authing 用户信息的 `externalId` 字段
- `identity`: 用户的外部身份源信息，格式为 `<extIdpId>:<userIdInIdp>`，其中 `<extIdpId>` 为 Authing 身份源的 ID，`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`62f20932716fbcc10d966ee5:ou_8bae746eac07cd2564654140d2a9ac61`。
- `sync_relation`: 用户的外部身份源信息，格式为 `<provier>:<userIdInIdp>`，其中 `<provier>` 为同步身份源类型，如 wechatwork, lark；`<userIdInIdp>` 为用户在外部身份源的 ID。
示例值：`lark:ou_8bae746eac07cd2564654140d2a9ac61`。

        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-mfa-trigger-data',
            params={
                'appId': app_id,
                'userId': user_id,
                'userIdType': user_id_type,
            },
        )

    def create_asa_account(self, account_info, app_id):
        """创建 ASA 账号

        在某一应用下创建 ASA 账号

        Attributes:
            account_info (dict): 账号信息，一般为包含 "account", "password" key 的键值对
            app_id (str): 所属应用 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-asa-account',
            json={
                'accountInfo': account_info,
                'appId': app_id,
            },
        )

    def create_asa_account_batch(self, list, app_id):
        """批量创建 ASA 账号

        在某一应用下批量创建 ASA 账号

        Attributes:
            list (list): 账号列表
            app_id (str): 所属应用 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-asa-accounts-batch',
            json={
                'list': list,
                'appId': app_id,
            },
        )

    def update_asa_account(self, account_info, account_id, app_id):
        """更新 ASA 账号

        更新某个 ASA 账号信息

        Attributes:
            account_info (dict): 账号信息，一般为包含 "account", "password" key 的键值对
            account_id (str): ASA 账号 ID
            app_id (str): 所属应用 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-asa-account',
            json={
                'accountInfo': account_info,
                'accountId': account_id,
                'appId': app_id,
            },
        )

    def list_asa_account(self, app_id, page=None, limit=None):
        """获取 ASA 账号列表

        分页获取某一应用下的 ASA 账号列表

        Attributes:
            appId (str): 所属应用 ID
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-asa-accounts',
            params={
                'appId': app_id,
                'page': page,
                'limit': limit,
            },
        )

    def get_asa_account(self, app_id, account_id):
        """获取 ASA 账号

        根据 ASA 账号 ID 获取账号详细信息

        Attributes:
            appId (str): 所属应用 ID
            accountId (str): ASA 账号 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-asa-account',
            params={
                'appId': app_id,
                'accountId': account_id,
            },
        )

    def get_asa_account_batch(self, account_ids, app_id):
        """批量获取 ASA 账号

        根据 ASA 账号 ID 列表批量获取账号详细信息

        Attributes:
            account_ids (list): ASA 账号 ID 列表
            app_id (str): 所属应用 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-asa-accounts-batch',
            json={
                'accountIds': account_ids,
                'appId': app_id,
            },
        )

    def delete_asa_account(self, account_id, app_id):
        """删除 ASA 账号

        通过 ASA 账号 ID 删除 ASA 账号

        Attributes:
            account_id (str): ASA 账号 ID
            app_id (str): 所属应用 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-asa-account',
            json={
                'accountId': account_id,
                'appId': app_id,
            },
        )

    def delete_asa_account_batch(self, account_ids, app_id):
        """批量删除 ASA 账号

        通过 ASA 账号 ID 批量删除 ASA 账号

        Attributes:
            account_ids (list): ASA 账号 ID 列表
            app_id (str): 所属应用 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-asa-accounts-batch',
            json={
                'accountIds': account_ids,
                'appId': app_id,
            },
        )

    def assign_asa_account(self, app_id, account_id, targets):
        """分配 ASA 账号

        分配 ASA 账号给用户、组织、分组或角色

        Attributes:
            app_id (str): 所属应用 ID
            account_id (str): 要关联的账号 ID
            targets (list): 关联对象列表
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/assign-asa-account',
            json={
                'appId': app_id,
                'accountId': account_id,
                'targets': targets,
            },
        )

    def unassign_asa_account(self, app_id, account_id, targets):
        """取消分配 ASA 账号

        取消分配给用户、组织、分组或角色的  ASA 账号

        Attributes:
            app_id (str): 所属应用 ID
            account_id (str): 要关联的账号 ID
            targets (list): 关联对象列表
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/unassign-asa-account',
            json={
                'appId': app_id,
                'accountId': account_id,
                'targets': targets,
            },
        )

    def get_asa_account_assigned_targets(self, app_id, account_id, page=None, limit=None):
        """获取 ASA 账号分配的主体列表

        根据 ASA 账号 ID 分页获取账号被分配的主体列表

        Attributes:
            appId (str): 所属应用 ID
            accountId (str): ASA 账号 ID
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-asa-account-assigned-targets',
            params={
                'appId': app_id,
                'accountId': account_id,
                'page': page,
                'limit': limit,
            },
        )

    def get_assigned_account(self, app_id, target_type, target_identifier):
        """获取主体被分配的 ASA 账号

        根据主体类型和标识获取直接分配给主体的 ASA 账号

        Attributes:
            appId (str): 所属应用 ID
            targetType (str): 目标对象类型：
- `USER`: 用户
- `ROLE`: 角色
- `GROUP`: 分组
- `DEPARTMENT`: 部门
    
            targetIdentifier (str): 目标对象的唯一标志符：
- 如果是用户，为用户的 ID，如 `6343b98b7cfxxx9366e9b7c`
- 如果是角色，为角色的 code，如 `admin`
- 如果是分组，为分组的 code，如 `developer`
- 如果是部门，为部门的 ID，如 `6343bafc019xxxx889206c4c`
        
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-assigned-account',
            params={
                'appId': app_id,
                'targetType': target_type,
                'targetIdentifier': target_identifier,
            },
        )

    def get_security_settings(self, ):
        """获取安全配置

        无需传参获取安全配置

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-security-settings',
        )

    def update_security_settings(self, allowed_origins=None, authing_token_expires_in=None, verify_code_length=None,
                                 verify_code_max_attempts=None, change_email_strategy=None, change_phone_strategy=None,
                                 cookie_settings=None, register_disabled=None, register_anomaly_detection=None,
                                 complete_password_after_pass_code_login=None, login_anomaly_detection=None,
                                 login_require_email_verified=None, self_unlock_account=None,
                                 enable_login_account_switch=None, qrcode_login_strategy=None):
        """修改安全配置

        可选安全域、Authing Token 有效时间（秒）、验证码长度、验证码尝试次数、用户修改邮箱的安全策略、用户修改手机号的安全策略、Cookie 过期时间设置、是否禁止用户注册、频繁注册检测配置、验证码注册后是否要求用户设置密码、未验证的邮箱登录时是否禁止登录并发送认证邮件、用户自助解锁配置、Authing 登录页面是否开启登录账号选择、APP 扫码登录安全配置进行修改安全配置

        Attributes:
            allowed_origins (list): 安全域（CORS）
            authing_token_expires_in (int): Authing Token 有效时间（秒）
            verify_code_length (int): 验证码长度。包含短信验证码、邮件验证码和图形验证码。
            verify_code_max_attempts (int): 验证码尝试次数。在一个验证码有效周期内（默认为 60 s），用户输入验证码错误次数超过此阈值之后，将会导致当前验证码失效，需要重新发送。
            change_email_strategy (dict): 用户修改邮箱的安全策略
            change_phone_strategy (dict): 用户修改手机号的安全策略
            cookie_settings (dict): Cookie 过期时间设置
            register_disabled (bool): 是否禁止用户注册，开启之后，用户将无法自主注册，只能管理员为其创建账号。针对 B2B 和 B2E 类型用户池，默认开启。
            register_anomaly_detection (dict): 频繁注册检测配置
            complete_password_after_pass_code_login (bool): 验证码注册后是否要求用户设置密码（仅针对 Authing 登录页和 Guard 有效，不针对 API 调用）。
            login_anomaly_detection (dict): 登录防暴破配置
            login_require_email_verified (bool): 当使用邮箱登录时，未验证的邮箱登录时是否禁止登录并发送认证邮件。当用户收到邮件并完成验证之后，才能进行登录。
            self_unlock_account (dict): 用户自助解锁配置。注：只有绑定了手机号/邮箱的用户才可以自助解锁
            enable_login_account_switch (bool): Authing 登录页面是否开启登录账号选择
            qrcode_login_strategy (dict): APP 扫码登录安全配置
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-security-settings',
            json={
                'allowedOrigins': allowed_origins,
                'authingTokenExpiresIn': authing_token_expires_in,
                'verifyCodeLength': verify_code_length,
                'verifyCodeMaxAttempts': verify_code_max_attempts,
                'changeEmailStrategy': change_email_strategy,
                'changePhoneStrategy': change_phone_strategy,
                'cookieSettings': cookie_settings,
                'registerDisabled': register_disabled,
                'registerAnomalyDetection': register_anomaly_detection,
                'completePasswordAfterPassCodeLogin': complete_password_after_pass_code_login,
                'loginAnomalyDetection': login_anomaly_detection,
                'loginRequireEmailVerified': login_require_email_verified,
                'selfUnlockAccount': self_unlock_account,
                'enableLoginAccountSwitch': enable_login_account_switch,
                'qrcodeLoginStrategy': qrcode_login_strategy,
            },
        )

    def get_global_mfa_settings(self, ):
        """获取全局多因素认证配置

        无需传参获取全局多因素认证配置

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-global-mfa-settings',
        )

    def update_global_mfa_settings(self, enabled_factors):
        """修改全局多因素认证配置

        传入 MFA 认证因素列表进行开启,

        Attributes:
            enabled_factors (list): 开启的 MFA 认证因素列表
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-global-mfa-settings',
            json={
                'enabledFactors': enabled_factors,
            },
        )

    def create_tenant(self, name, app_ids, logo=None, description=None, reject_hint=None, source_app_id=None,
                      enterprise_domains=None, expire_time=None, mau_amount=None, member_amount=None,
                      admin_amount=None):
        """创建租户

        

        Attributes:
            name (str): 租户名
            app_ids (list): 租户关联的应用 ID
            logo (list): 租户 logo
            description (str): 租户描述
            reject_hint (str): 用户被租户拒绝登录时显示的提示文案
            source_app_id (str): 租户来源的应用 ID，该值不存在时代表租户来源为 Authing 控制台
            enterprise_domains (list): 企业邮箱域名
            expire_time (str): 租户过期时间
            mau_amount (int): 租户 MAU 上限
            member_amount (int): 租户成员上限
            admin_amount (int): 租户管理员上限
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-tenant',
            json={
                'name': name,
                'appIds': app_ids,
                'logo': logo,
                'description': description,
                'rejectHint': reject_hint,
                'sourceAppId': source_app_id,
                'enterpriseDomains': enterprise_domains,
                'expireTime': expire_time,
                'mauAmount': mau_amount,
                'memberAmount': member_amount,
                'adminAmount': admin_amount,
            },
        )

    def update_tenant(self, tenant_id, name=None, app_ids=None, logo=None, description=None, reject_hint=None,
                      source_app_id=None):
        """更新租户数据

        此接口用于更新租户基本信息。

        Attributes:
            tenant_id (str): 租户 ID
            name (str): 租户名
            app_ids (list): 租户关联的应用 ID
            logo (list): 租户 logo
            description (str): 租户描述
            reject_hint (str): 用户被租户拒绝登录时显示的提示文案
            source_app_id (str): 租户来源的应用 ID，该值不存在时代表租户来源为 Authing 控制台
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-tenant',
            json={
                'tenantId': tenant_id,
                'name': name,
                'appIds': app_ids,
                'logo': logo,
                'description': description,
                'rejectHint': reject_hint,
                'sourceAppId': source_app_id,
            },
        )

    def delete_tenant(self, tenant_id):
        """删除租户

        此接口用于删除租户。

        Attributes:
            tenant_id (str): 租户 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-tenant',
            json={
                'tenantId': tenant_id,
            },
        )

    def list_tenants(self, keywords=None, with_members_count=None, with_app_detail=None, with_creator_detail=None,
                     with_source_app_detail=None, page=None, limit=None, source=None):
        """获取/搜索租户列表

        此接口用于获取租户列表，支持模糊搜索。

        Attributes:
            keywords (str): 搜索关键字
            withMembersCount (bool): 是否增加返回租户成员统计
            withAppDetail (bool): 增加返回租户下 app 简单信息
            withCreatorDetail (bool): 增加返回租户下创建者简单信息
            withSourceAppDetail (bool): 增加返回租户下来源 app 简单信息
            page (str): 页码
            limit (str): 每页获取的数据量
            source (): 租户来源
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-tenants',
            params={
                'keywords': keywords,
                'withMembersCount': with_members_count,
                'withAppDetail': with_app_detail,
                'withCreatorDetail': with_creator_detail,
                'withSourceAppDetail': with_source_app_detail,
                'page': page,
                'limit': limit,
                'source': source,
            },
        )

    def get_tenant_little_info(self, tenant_id, with_members_count=None, with_app_detail=None, with_creator_detail=None,
                               with_source_app_detail=None):
        """获取租户一点点的信息

        根据租户 ID 获取租户一点点的详情

        Attributes:
            tenantId (str): 租户 ID
            withMembersCount (bool): 是否增加返回租户成员统计
            withAppDetail (bool): 增加返回租户关联应用简单信息
            withCreatorDetail (bool): 增加返回租户下创建者简单信息
            withSourceAppDetail (bool): 增加返回租户来源应用简单信息
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-tenant-little-info',
            params={
                'tenantId': tenant_id,
                'withMembersCount': with_members_count,
                'withAppDetail': with_app_detail,
                'withCreatorDetail': with_creator_detail,
                'withSourceAppDetail': with_source_app_detail,
            },
        )

    def get_tenant(self, tenant_id, with_members_count=None, with_app_detail=None, with_creator_detail=None,
                   with_source_app_detail=None):
        """获取租户详情

        根据租户 ID 获取租户详情

        Attributes:
            tenantId (str): 租户 ID
            withMembersCount (bool): 是否增加返回租户成员统计
            withAppDetail (bool): 增加返回租户关联应用简单信息
            withCreatorDetail (bool): 增加返回租户下创建者简单信息
            withSourceAppDetail (bool): 增加返回租户来源应用简单信息
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-tenant',
            params={
                'tenantId': tenant_id,
                'withMembersCount': with_members_count,
                'withAppDetail': with_app_detail,
                'withCreatorDetail': with_creator_detail,
                'withSourceAppDetail': with_source_app_detail,
            },
        )

    def import_tenant(self, excel_url):
        """导入租户

        此接口用于 Excel 导入租户。

        Attributes:
            excel_url (str): excel path 地址
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/import-tenant',
            json={
                'excelUrl': excel_url,
            },
        )

    def import_tenant_history(self, page=None, limit=None):
        """导入租户历史

        此接口用于 Excel 导入租户的历史查询。

        Attributes:
            page (str): 页码
            limit (str): 每页获取的数据量
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/import-tenant-history',
            params={
                'page': page,
                'limit': limit,
            },
        )

    def import_tenant_notify_user(self, import_id, page=None, limit=None):
        """导入租户通知用户列表

        此接口用于查询导入租户通知用户列表。

        Attributes:
            importId (str): 导入记录 id
            page (str): 页码
            limit (str): 每页获取的数据量
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/import-tenant-notify-user',
            params={
                'importId': import_id,
                'page': page,
                'limit': limit,
            },
        )

    def send_email_batch(self, admin_name, import_id, users):
        """导入租户通知邮箱用户

        此接口用于批量发送邮件通知。

        Attributes:
            admin_name (str): 管理员名
            import_id (int): 导入 id
            users (list): 需要邮件通知的管理员
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/send-email-batch',
            json={
                'adminName': admin_name,
                'importId': import_id,
                'users': users,
            },
        )

    def send_sms_batch(self, admin_name, import_id, users):
        """导入租户短信通知用户

        此接口用于批量发送短信通知。

        Attributes:
            admin_name (str): 管理员名
            import_id (int): 导入 id
            users (list): 需要短信通知的管理员
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/send-sms-batch',
            json={
                'adminName': admin_name,
                'importId': import_id,
                'users': users,
            },
        )

    def list_tenant_admin(self, tenant_id, keywords=None, page=None, limit=None):
        """获取租户管理员列表

        此接口用于获取租户成员列表，支持模糊搜索。

        Attributes:
            tenant_id (str): 租户 ID
            keywords (str): 搜索关键字
            page (str): 页码
            limit (str): 每页获取的数据量
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/list-tenant-admin',
            json={
                'tenantId': tenant_id,
                'keywords': keywords,
                'page': page,
                'limit': limit,
            },
        )

    def set_tenant_admin(self, tenant_id, link_user_ids=None, member_ids=None):
        """设置租户管理员

        此接口用于根据用户 ID 或租户成员 ID 设置租户管理员。

        Attributes:
            tenant_id (str): 租户 ID
            link_user_ids (list): 关联的用户池级别的用户 ID
            member_ids (list): 租户成员 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/set-tenant-admin',
            json={
                'tenantId': tenant_id,
                'linkUserIds': link_user_ids,
                'memberIds': member_ids,
            },
        )

    def delete_tenant_admin(self, tenant_id, link_user_id=None, member_id=None):
        """取消设置租户管理员

        此接口用于根据用户 ID 或租户成员 ID 取消设置租户管理员。

        Attributes:
            tenant_id (str): 租户 ID
            link_user_id (str): 关联的用户池级别的用户 ID
            member_id (str): 租户成员 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-tenant-admin',
            json={
                'tenantId': tenant_id,
                'linkUserId': link_user_id,
                'memberId': member_id,
            },
        )

    def delete_tenant_user(self, tenant_id, link_user_ids=None, member_ids=None):
        """批量移除租户成员

        此接口用于根据用户 ID 或租户成员 ID 批量移除租户成员。

        Attributes:
            tenant_id (str): 租户 ID
            link_user_ids (list): 关联的用户池级别的用户 ID
            member_ids (list): 租户成员 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-tenant-user',
            json={
                'tenantId': tenant_id,
                'linkUserIds': link_user_ids,
                'memberIds': member_ids,
            },
        )

    def generate_invite_tenant_user_link(self, validity_term, emails, app_id, tenant_id=None):
        """生成一个邀请租户成员的链接

        此接口用于生成一个邀请租户成员的链接。appId 为用户注册成功后要访问的应用 ID

        Attributes:
            validity_term (str): 链接有效期
            emails (list): 要邀请的用户邮箱
            app_id (str): 应用 ID
            tenant_id (str): 租户 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/generate-invite-tenant-user-link',
            json={
                'validityTerm': validity_term,
                'emails': emails,
                'appId': app_id,
                'tenantId': tenant_id,
            },
        )

    def list_invite_tennat_user_records(self, keywords, page, limit):
        """获取可访问的租户控制台列表

        根据用户 ID 获取可访问的租户控制台列表

        Attributes:
            keywords (str): 搜索关键字
            page (str): 页码
            limit (str): 每页获取的数据量
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-invite-tenant-user-records',
            params={
                'keywords': keywords,
                'page': page,
                'limit': limit,
            },
        )

    def list_multiple_tenant_admin(self, keywords=None, page=None, limit=None):
        """获取多租户管理员用户列表

        根据用户池 ID 获取某个用户池内拥有多租户管理权限的用户列表

        Attributes:
            keywords (str): 搜索关键字
            page (str): 页码
            limit (str): 每页获取的数据量
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-multiple-tenant-admins',
            params={
                'keywords': keywords,
                'page': page,
                'limit': limit,
            },
        )

    def create_multiple_tenant_admin(self, tenant_ids, user_id, api_authorized=None, send_phone_notification=None,
                                     send_email_notification=None):
        """创建多租户管理员用户

        根据用户 ID 创建一个用户池内拥有多租户管理权限的用户

        Attributes:
            tenant_ids (list): 租户 ID
            user_id (str): 用户 ID
            api_authorized (bool): 是否授权
            send_phone_notification (bool): SMS 通知
            send_email_notification (bool): Email 通知
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-multiple-tenant-admin',
            json={
                'tenantIds': tenant_ids,
                'userId': user_id,
                'apiAuthorized': api_authorized,
                'sendPhoneNotification': send_phone_notification,
                'sendEmailNotification': send_email_notification,
            },
        )

    def get_multiple_tenant_admin(self, user_id):
        """获取多租户管理员用户列表

        根据用户池 ID 获取某个用户池内拥有多租户管理权限的用户列表

        Attributes:
            userId (str): 用户 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-multiple-tenant-admin',
            params={
                'userId': user_id,
            },
        )

    def list_tenant_cooperators(self, keywords=None, external=None, page=None, limit=None):
        """获取协作管理员用户列表

        根据用户池 ID 获取某个用户池内拥有协作管理员能力的用户列表

        Attributes:
            keywords (str): 搜索关键字
            external (bool): 是否外部
            page (str): 页码
            limit (str): 每页获取的数据量
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-tenant-cooperators',
            params={
                'keywords': keywords,
                'external': external,
                'page': page,
                'limit': limit,
            },
        )

    def get_tenant_cooperator(self, user_id):
        """获取一个协调管理员

        根据用户池 ID 获取某个协调管理员的列表

        Attributes:
            userId (str): 用户 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-tenant-cooperator',
            params={
                'userId': user_id,
            },
        )

    def get_tenant_cooperator_menu(self, user_id):
        """获取一个协调管理员拥有的列表

        根据用户池 ID 获取某个协调管理员的列表

        Attributes:
            userId (str): 用户 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-tenant-cooperator-menu',
            params={
                'userId': user_id,
            },
        )

    def create_tenant_cooperator(self, policies, user_id, api_authorized=None, send_phone_notification=None,
                                 send_email_notification=None):
        """创建协调管理员

        创建一个协调管理员

        Attributes:
            policies (list): 策略
            user_id (str): 用户 ID
            api_authorized (bool): 是否授权 API
            send_phone_notification (bool): SMS 通知
            send_email_notification (bool): Email 通知
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-tenant-cooperator',
            json={
                'policies': policies,
                'userId': user_id,
                'apiAuthorized': api_authorized,
                'sendPhoneNotification': send_phone_notification,
                'sendEmailNotification': send_email_notification,
            },
        )

    def get_tenant_by_code(self, code):
        """获取租户详情

        根据租户 Code 获取租户详情

        Attributes:
            code (str): 租户 Code
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-tenant-by-code',
            params={
                'code': code,
            },
        )

    def send_invite_tenant_user_email(self, ):
        """发送邀请租户用户邮件

        向多个邮箱发送邀请成为租户用户的邮件

        Attributes:
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/send-invite-tenant-user-email',
            json={
            },
        )

    def add_tenant_users(self, link_user_ids, tenant_id):
        """添加租户成员

        根据用户 ID 批量添加租户成员

        Attributes:
            link_user_ids (list): 关联的用户池级别的用户 ID
            tenant_id (str): 租户 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/add-tenant-users',
            json={
                'linkUserIds': link_user_ids,
                'tenantId': tenant_id,
            },
        )

    def remove_tenant_users(self, tenant_id, link_user_ids=None, member_ids=None):
        """批量移除租户成员

        此接口用于根据用户 ID 或租户成员 ID 批量移除租户成员。

        Attributes:
            tenant_id (str): 租户 ID
            link_user_ids (list): 关联的用户池级别的用户 ID
            member_ids (list): 租户成员 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/remove-tenant-users',
            json={
                'tenantId': tenant_id,
                'linkUserIds': link_user_ids,
                'memberIds': member_ids,
            },
        )

    def update_tenant_user(self, updates, tenant_id, link_user_id=None, member_id=None):
        """更新租户成员

        此接口用于根据用户 ID 或租户成员 ID 更新租户成员。

        Attributes:
            updates (dict): 要更新的租户成员信息
            tenant_id (str): 租户 ID
            link_user_id (str): 关联的用户池级别的用户 ID
            member_id (str): 租户成员 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-tenant-user',
            json={
                'updates': updates,
                'tenantId': tenant_id,
                'linkUserId': link_user_id,
                'memberId': member_id,
            },
        )

    def create_tenant_user(self, tenant_id, gender, email=None, phone=None, phone_country_code=None, username=None,
                           name=None, nickname=None, photo=None, birthdate=None, country=None, province=None, city=None,
                           address=None, street_address=None, postal_code=None, given_name=None, family_name=None,
                           middle_name=None, preferred_username=None, password=None, salt=None, options=None):
        """创建租户成员

        创建租户成员，邮箱、手机号、用户名必须包含其中一个，邮箱、手机号、用户名、externalId 用户池内唯一，此接口将以管理员身份创建用户因此不需要进行手机号验证码检验等安全检测。

        Attributes:
            tenant_id (str): 租户 ID
            gender (str): 性别:
- `M`: 男性，`male`
- `F`: 女性，`female`
- `U`: 未知，`unknown`
  
            email (str): 邮箱，不区分大小写
            phone (str): 手机号，不带区号。如果是国外手机号，请在 phoneCountryCode 参数中指定区号。
            phone_country_code (str): 手机区号，中国大陆手机号可不填。Authing 短信服务暂不内置支持国际手机号，你需要在 Authing 控制台配置对应的国际短信服务。完整的手机区号列表可参阅 https://en.wikipedia.org/wiki/List_of_country_calling_codes。
            username (str): 用户名，用户池内唯一
            name (str): 用户真实名称，不具备唯一性
            nickname (str): 昵称
            photo (str): 头像链接
            birthdate (str): 出生日期
            country (str): 所在国家
            province (str): 所在省份
            city (str): 所在城市
            address (str): 所处地址
            street_address (str): 所处街道地址
            postal_code (str): 邮政编码号
            given_name (str): 名
            family_name (str): 姓
            middle_name (str): 中间名
            preferred_username (str): Preferred Username
            password (str): 用户密码，默认为明文。我们使用 HTTPS 协议对密码进行安全传输，可以在一定程度上保证安全性。如果你还需要更高级别的安全性，我们还支持 RSA256 和国密 SM2 两种方式对密码进行加密。详情见 `passwordEncryptType` 参数。
            salt (str): 加密用户密码的盐
            options (dict): 可选参数
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-tenant-user',
            json={
                'tenantId': tenant_id,
                'gender': gender,
                'email': email,
                'phone': phone,
                'phoneCountryCode': phone_country_code,
                'username': username,
                'name': name,
                'nickname': nickname,
                'photo': photo,
                'birthdate': birthdate,
                'country': country,
                'province': province,
                'city': city,
                'address': address,
                'streetAddress': street_address,
                'postalCode': postal_code,
                'givenName': given_name,
                'familyName': family_name,
                'middleName': middle_name,
                'preferredUsername': preferred_username,
                'password': password,
                'salt': salt,
                'options': options,
            },
        )

    def list_tenant_users(self, tenant_id, keywords=None, options=None):
        """获取/搜索租户成员列表

        
此接口用于获取用户列表，支持模糊搜索，以及通过用户基础字段、用户自定义字段、用户所在部门、用户历史登录应用等维度筛选用户。

### 模糊搜素示例

模糊搜索默认会从 `phone`, `email`, `name`, `username`, `nickname` 五个字段对用户进行模糊搜索，你也可以通过设置 `options.fuzzySearchOn`
决定模糊匹配的字段范围：

```json
{
  "keywords": "北京",
  "options": {
    "fuzzySearchOn": [
      "address"
    ]
  }
}
```

### 高级搜索示例

你可以通过 `advancedFilter` 进行高级搜索，高级搜索支持通过用户的基础信息、自定义数据、所在部门、用户来源、登录应用、外部身份源信息等维度对用户进行筛选。
**且这些筛选条件可以任意组合。**

#### 筛选邮箱中包含 `@example.com` 的用户

用户邮箱（`email`）为字符串类型，可以进行模糊搜索：

```json
{
  "advancedFilter": [
    {
      "field": "email",
      "operator": "CONTAINS",
      "value": "@example.com"
    }
  ]
}
```


#### 根据用户登录次数筛选

筛选登录次数大于 10 的用户：

```json
{
  "advancedFilter": [
    {
      "field": "loginsCount",
      "operator": "GREATER",
      "value": 10
    }
  ]
}
```

筛选登录次数在 10 - 100 次的用户：

```json
{
  "advancedFilter": [
    {
      "field": "loginsCount",
      "operator": "BETWEEN",
      "value": [10, 100]
    }
  ]
}
```

#### 根据用户上次登录时间进行筛选

筛选最近 7 天内登录过的用户：

```json
{
  "advancedFilter": [
    {
      "field": "lastLoginTime",
      "operator": "GREATER",
      "value": new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)
    }
  ]
}
```

筛选在某一段时间内登录过的用户：

```json
{
  "advancedFilter": [
    {
      "field": "lastLoginTime",
      "operator": "BETWEEN",
      "value": [
        Date.now() - 14 * 24 * 60 * 60 * 1000,
        Date.now() - 7 * 24 * 60 * 60 * 1000
      ]
    }
  ]
}
```

#### 根据用户曾经登录过的应用筛选

筛选出曾经登录过应用 `appId1` 或者 `appId2` 的用户：

```json
{
  "advancedFilter": [
    {
      "field": "loggedInApps",
      "operator": "IN",
      "value": [
        "appId1",
        "appId2"
      ]
    }
  ]
}
```

#### 根据用户所在部门进行筛选

```json
{
  "advancedFilter": [
    {
      "field": "department",
      "operator": "IN",
      "value": [
        {
          "organizationCode": "steamory",
          "departmentId": "root",
          "departmentIdType": "department_id",
          "includeChildrenDepartments": true
        }
      ]
    }
  ]
}
```

  

        Attributes:
            tenant_id (str): 租户 ID
            keywords (str): 搜索关键字
            options (dict): 可选项
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/list-tenant-users',
            json={
                'tenantId': tenant_id,
                'keywords': keywords,
                'options': options,
            },
        )

    def get_tenant_user(self, tenant_id, link_user_id=None, member_id=None):
        """获取单个租户成员

        根据用户 ID 或租户成员 ID 获取租户成员信息

        Attributes:
            tenantId (str): 租户 ID
            linkUserId (str): 关联的用户池级别的用户 ID
            memberId (str): 租户成员 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-tenant-user',
            params={
                'tenantId': tenant_id,
                'linkUserId': link_user_id,
                'memberId': member_id,
            },
        )

    def add_tenant_department_members(self, organization_code, department_id, department_id_type=None,
                                      link_user_ids=None, member_ids=None, tenant_id=None):
        """租户部门下添加成员

        通过部门 ID、组织 code，添加部门下成员。

        Attributes:
            organization_code (str): 组织 code
            department_id (str): 部门系统 ID（为 Authing 系统自动生成，不可修改）
            department_id_type (str): 此次调用中使用的部门 ID 的类型
            link_user_ids (list): 关联的用户池级别的用户 ID
            member_ids (list): 租户成员 ID
            tenant_id (str): 租户 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/add-tenant-department-members',
            json={
                'organizationCode': organization_code,
                'departmentId': department_id,
                'departmentIdType': department_id_type,
                'linkUserIds': link_user_ids,
                'memberIds': member_ids,
                'tenantId': tenant_id,
            },
        )

    def remove_tenant_department_members(self, organization_code, department_id, department_id_type=None,
                                         link_user_ids=None, member_ids=None, tenant_id=None):
        """租户部门下删除成员

        通过部门 ID、组织 code，删除部门下成员。

        Attributes:
            organization_code (str): 组织 code
            department_id (str): 部门系统 ID（为 Authing 系统自动生成，不可修改）
            department_id_type (str): 此次调用中使用的部门 ID 的类型
            link_user_ids (list): 关联的用户池级别的用户 ID
            member_ids (list): 租户成员 ID
            tenant_id (str): 租户 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/remove-tenant-department-members',
            json={
                'organizationCode': organization_code,
                'departmentId': department_id,
                'departmentIdType': department_id_type,
                'linkUserIds': link_user_ids,
                'memberIds': member_ids,
                'tenantId': tenant_id,
            },
        )

    def create_permission_namespace(self, name, code, description=None):
        """创建权限空间

        创建权限空间,可以设置权限空间名称、Code 和描述信息。

        Attributes:
            name (str): 权限空间名称
            code (str): 权限空间 Code
            description (str): 权限空间描述
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-permission-namespace',
            json={
                'name': name,
                'code': code,
                'description': description,
            },
        )

    def create_permission_namespaces_batch(self, list):
        """批量创建权限空间

        批量创建权限空间，可以分别设置权限空间名称、Code 和描述信息。

        Attributes:
            list (list): 权限空间列表
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-permission-namespaces-batch',
            json={
                'list': list,
            },
        )

    def get_permission_namespace(self, code):
        """获取权限空间详情

        通过权限空间唯一标志符(Code)，获取权限空间详情。

        Attributes:
            code (str): 权限空间 Code
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-permission-namespace',
            params={
                'code': code,
            },
        )

    def get_permission_namespaces_batch(self, codes):
        """批量获取权限空间详情列表

        分别通过权限空间唯一标志符(Code)，获取权限空间详情。

        Attributes:
            codes (str): 权限空间 code 列表，批量可以使用逗号分隔
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-permission-namespaces-batch',
            params={
                'codes': codes,
            },
        )

    def list_permission_namespaces(self, page=None, limit=None, query=None):
        """分页获取权限空间列表

        分页获取权限空间列表。

        Attributes:
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            query (str): 权限空间 name
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-permission-namespaces',
            params={
                'page': page,
                'limit': limit,
                'query': query,
            },
        )

    def update_permission_namespace(self, code, name=None, new_code=None, description=None):
        """修改权限空间

        修改权限空间，可以修改权限空间名称、权限空间描述信息以及权限空间新的唯一标志符(Code)。

        Attributes:
            code (str): 权限分组老的唯一标志符 Code
            name (str): 权限空间名称
            new_code (str): 权限分组新的唯一标志符 Code
            description (str): 权限空间描述
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-permission-namespace',
            json={
                'code': code,
                'name': name,
                'newCode': new_code,
                'description': description,
            },
        )

    def delete_permission_namespace(self, code):
        """删除权限空间

        通过权限空间唯一标志符(Code)，删除权限空间信息。

        Attributes:
            code (str): 权限空间 Code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-permission-namespace',
            json={
                'code': code,
            },
        )

    def delete_permission_namespaces_batch(self, codes):
        """批量删除权限空间

        分别通过权限空间唯一标志符(Code)，批量删除权限空间信息。

        Attributes:
            codes (list): 权限分组 code 列表
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-permission-namespaces-batch',
            json={
                'codes': codes,
            },
        )

    def check_permission_namespace_exists(self, code=None, name=None):
        """校验权限空间 Code 或者名称是否可用

        通过用户池 ID 和权限空间 Code,或者用户池 ID 和权限空间名称查询是否可用。

        Attributes:
            code (str): 权限空间 Code
            name (str): 权限空间名称
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/check-permission-namespace-exists',
            json={
                'code': code,
                'name': name,
            },
        )

    def list_permission_namespace_roles(self, code, page=None, limit=None, query=None):
        """分页查询权限空间下所有的角色列表

        分页查询权限空间下所有的角色列表，分页获取权限空间下所有的角色列表。

        Attributes:
            code (str): 权限分组唯一标志符 Code
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            query (str): 角色 Code 或者名称
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-permission-namespace-roles',
            params={
                'page': page,
                'limit': limit,
                'code': code,
                'query': query,
            },
        )

    def create_data_resource(self, actions, struct, type, resource_code, resource_name, namespace_code,
                             description=None):
        """创建数据资源（推荐、重点）

        
  ## 描述
  该接口用于创建数据资源，当你存在需要被设置权限的数据，根据它们的数据类型，创建对应类型的数据资源，目前我们支持：字符串、数组、树三种类型。
  ## 注意
  请求体中的 `struct` 字段需要根据不同的资源类型传入不同的数据结构，具体请参考下面的示例
## 请求示例
### 创建字符串类型数据资源示例
当你的数据仅用一个字符串就可以表示时，可以使用此类型，例如：一个 API、一个用户 ID 等。
以下是创建一个表示 '/resource/create' API 的数据资源示例：
```json
{
  "namespaceCode": "examplePermissionNamespace",
  "resourceName": "createResource API",
  "description": "这是 createResource API",
  "resourceCode": "createResourceAPI",
  "type": "STRING",
  "struct": "/resource/create",
  "actions": ["access"]
}
```

### 创建数组类型数据资源示例
当你的数据是一组同类型的数据时，可以使用此类型，例如：一组文档链接、一组门禁卡号等。
以下是创建一个表示一组门禁卡号的数据资源示例：
```json
{
  "namespaceCode": "examplePermissionNamespace",
  "resourceName": "一组门禁卡号",
  "description": "这是一组门禁卡号",
  "resourceCode": "accessCardNumber",
  "type": "ARRAY",
  "struct": ["accessCardNumber1", "accessCardNumber2", "accessCardNumber3"],
  "actions": ["get", "update"]
}
```

### 创建树类型数据资源示例
当你的数据是具备层级关系时，可以使用此类型，例如：组织架构、文件夹结构等。
以下是创建一个表示公司组织架构的数据资源示例：
```json
{
  "namespaceCode": "examplePermissionNamespace",
  "resourceName": "Authing",
  "description": "这是 Authing 的组织架构",
  "resourceCode": "authing",
  "type": "TREE",
  "struct": [
    {
      "name": "产品",
      "code": "product",
      "value": "product",
      "children": [
        {
          "name": "产品经理",
          "code": "productManager",
          "value": "pm"
        },
        {
          "name": "设计",
          "code": "design",
          "value": "ui"
        }
      ]
    },
    {
      "name": "研发",
      "code": "researchAndDevelopment",
      "value": "rd"
    }
  ],
  "actions": ["get", "update", "delete"]
}
```
  

        Attributes:
            actions (list): 数据资源权限操作列表
            struct (): 数据资源结构，支持字符串（STRING）、树结构（TREE）和数组结构（ARRAY）。
            type (str): 数据资源类型，目前支持树结构（TREE）、字符串（STRING）、数组（ARRAY）
            resource_code (str): 数据资源 Code, 权限空间内唯一
            resource_name (str): 数据资源名称, 权限空间内唯一
            namespace_code (str): 数据资源所属的权限空间 Code
            description (str): 数据资源描述
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-data-resource',
            json={
                'actions': actions,
                'struct': struct,
                'type': type,
                'resourceCode': resource_code,
                'resourceName': resource_name,
                'namespaceCode': namespace_code,
                'description': description,
            },
        )

    def create_data_resource_by_string(self, actions, struct, resource_code, resource_name, namespace_code,
                                       description=None):
        """创建字符串数据资源

        当你仅需要创建字符串类型数据资源时，可以使用此 API，我们固定了数据资源类型，你无需在传入 `type` 字符段，注意：`struct` 字段只能够传入字符串类型数据。

        Attributes:
            actions (list): 数据资源权限操作列表
            struct (str): 字符串数据资源节点
            resource_code (str): 数据资源 Code, 权限空间内唯一
            resource_name (str): 数据资源名称, 权限空间内唯一
            namespace_code (str): 数据策略所在的权限空间 Code
            description (str): 数据资源描述
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-string-data-resource',
            json={
                'actions': actions,
                'struct': struct,
                'resourceCode': resource_code,
                'resourceName': resource_name,
                'namespaceCode': namespace_code,
                'description': description,
            },
        )

    def create_data_resource_by_array(self, actions, struct, resource_code, resource_name, namespace_code,
                                      description=None):
        """创建数组数据资源

        当你仅需要创建数组类型数据资源时，可以使用此 API，我们固定了数据资源类型，你无需在传入 `type` 字符段，注意：`struct` 字段只能够传入数组类型数据。

        Attributes:
            actions (list): 数据资源权限操作列表
            struct (list): 数组数据资源节点
            resource_code (str): 数据资源 Code, 权限空间内唯一
            resource_name (str): 数据资源名称, 权限空间内唯一
            namespace_code (str): 数据策略所在的权限空间 Code
            description (str): 数据资源描述
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-array-data-resource',
            json={
                'actions': actions,
                'struct': struct,
                'resourceCode': resource_code,
                'resourceName': resource_name,
                'namespaceCode': namespace_code,
                'description': description,
            },
        )

    def create_data_resource_by_tree(self, actions, struct, resource_code, resource_name, namespace_code,
                                     description=None):
        """创建树数据资源

        当你仅需要创建树类型数据资源时，可以使用此 API，我们固定了数据资源类型，你无需在传入 `type` 字符段，注意：`struct` 要按照树类型数据资源结构进行传入，请参考示例。

        Attributes:
            actions (list): 数据资源权限操作列表
            struct (list): 树数据资源节点
            resource_code (str): 数据资源 Code, 权限空间内唯一
            resource_name (str): 数据资源名称, 权限空间内唯一
            namespace_code (str): 数据策略所在的权限空间 Code
            description (str): 数据资源描述
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-tree-data-resource',
            json={
                'actions': actions,
                'struct': struct,
                'resourceCode': resource_code,
                'resourceName': resource_name,
                'namespaceCode': namespace_code,
                'description': description,
            },
        )

    def list_data_resources(self, page=None, limit=None, query=None, namespace_codes=None):
        """获取数据资源列表

        获取数据资源列表,可通过数据资源名称、数据资源 Code 和数据资源所属权限空间 Code 列表进行指定筛选。

        Attributes:
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            query (str): 关键字搜索，可以是数据资源名称或者数据资源 Code
            namespaceCodes (str): 权限数据所属权限空间 Code 列表
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-data-resources',
            params={
                'page': page,
                'limit': limit,
                'query': query,
                'namespaceCodes': namespace_codes,
            },
        )

    def get_data_resource(self, namespace_code, resource_code):
        """获取数据资源详情

        获取数据资源,通过数据资源 ID 查询对应的数据资源信息,包含数据资源名称、数据资源 Code、数据资源类型（TREE、STRING、ARRAY）、数据资源所属权限空间 ID、数据资源所属权限空间 Code 以及数据资源操作列表等基本信息。

        Attributes:
            namespaceCode (str): 数据资源所属的权限空间 Code
            resourceCode (str): 数据资源 Code, 权限空间内唯一
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-data-resource',
            params={
                'namespaceCode': namespace_code,
                'resourceCode': resource_code,
            },
        )

    def update_data_resource(self, resource_code, namespace_code, resource_name=None, description=None, struct=None,
                             actions=None):
        """修改数据资源

        修改数据资源,根据权限空间 Code 和数据资源 Code 查询原始信息,只允许修改数据资源名称、描述和数据资源节点。

        Attributes:
            resource_code (str): 数据资源 Code, 权限空间内唯一
            namespace_code (str): 数据资源所属的权限空间 Code
            resource_name (str): 数据资源名称, 权限空间内唯一
            description (str): 数据资源描述
            struct (): 数据资源结构，支持字符串（STRING）、树结构（TREE）和数组结构（ARRAY）。
            actions (list): 数据资源权限操作列表
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-data-resource',
            json={
                'resourceCode': resource_code,
                'namespaceCode': namespace_code,
                'resourceName': resource_name,
                'description': description,
                'struct': struct,
                'actions': actions,
            },
        )

    def delete_data_resource(self, resource_code, namespace_code):
        """删除数据资源

        删除数据资源,根据数据资源 ID 删除对应的数据资源信息。

        Attributes:
            resource_code (str): 数据资源 Code, 权限空间内唯一
            namespace_code (str): 数据资源所属的权限空间 Code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-data-resource',
            json={
                'resourceCode': resource_code,
                'namespaceCode': namespace_code,
            },
        )

    def check_data_resource_exists(self, namespace_code, resource_name=None, resource_code=None):
        """检查数据资源 Code 或者名称是否可用

        检查数据资源名称或者 Code 在权限空间内是否有效,通过数据资源名称或者数据资源 Code 以及所属权限空间 Code,判断在指定的权限空间内是否可用。

### 数据资源 Code 有效示例

- 入参

```json
{
  "namespaceCode": "examplePermissionNamespace",
  "resourceCode": "test"
}
```

- 出参

```json
{
  "statusCode": 200,
  "message": "操作成功",
  "apiCode": 0,
  "data": {
      "isValid": "true"
    }
}
```

### 数据资源名称有效示例

- 入参

```json
{
  "namespaceCode": "examplePermissionNamespace",
  "resourceName": "test"
}
```

- 出参

```json
{
  "statusCode": 200,
  "message": "操作成功",
  "apiCode": 0,
  "data": {
      "isValid": "true"
    }
}
```

### 数据资源 Code 无效示例

- 入参

```json
{
  "namespaceCode": "examplePermissionNamespace",
  "resourceCode": "test"
}
```

- 出参

```json
{
  "statusCode": 200,
  "message": "操作成功",
  "apiCode": 0,
  "requestId": "934108e5-9fbf-4d24-8da1-c330328abd6c",
  "data": {
      "isValid": "false",
      "message": "data resource code already exist"
  }
}
```
  

        Attributes:
            namespaceCode (str): 数据资源所属的权限空间 Code
            resourceName (str): 数据资源名称, 权限空间内唯一
            resourceCode (str): 数据资源 Code, 权限空间内唯一
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/check-data-resource-exists',
            params={
                'namespaceCode': namespace_code,
                'resourceName': resource_name,
                'resourceCode': resource_code,
            },
        )

    def create_data_policy(self, statement_list, policy_name, description=None):
        """创建数据策略（重点）

        
  ## 描述
  该接口用于创建数据策略，通过数据策略你可以将一组数据资源及其指定的操作进行绑定到一起，共同授权给主体。
  ## 注意
为了方便使用，`permissions` 字段我们基于路径的方式提供了快捷的写法，如：
- 数组、字符串资源：权限空间 code/数据资源 code/数据资源某一 action（如果表示所有操作，则使用`*`替代action）
- 树类型资源：权限空间 code/数据资源 code/node code 1/node code 1_1/.../数据资源某一 action

## 请求示例
假设我们要对一名研发人员进行授权，首先创建 3 个数据资源如下：
```json
{
  "namespaceCode": "examplePermissionNamespace",
  "resourceName": "服务器",
  "resourceCode": "server_2023",
  "type": "STRING",
  "struct": "server_2023",
  "actions": ["read", "write"]
}
```
```json
{
  "namespaceCode": "examplePermissionNamespace",
  "resourceName": "研发知识库",
  "description": "",
  "resourceCode": "rd_document",
  "type": "STRING",
  "struct": "https://www.authing.com/rd_document",
  "actions": ["read", "write", "share"]
}
```
```json
{
  "namespaceCode": "examplePermissionNamespace",
  "resourceName": "研发内部平台菜单",
  "description": "这是研发使用的内部平台菜单",
  "resourceCode": "rd_internal_platform",
  "type": "TREE",
  "struct": [
    {
      "name": "部署",
      "code": "deploy",
      "children": [
        {
          "name": "生产环境",
          "code": "prod"
        },
        {
          "name": "测试环境",
          "code": "test"
        }
      ]
    },
    {
      "name": "数据库",
      "code": "db"
      "children": [
        {
          "name": "查询",
          "code": "query"
        },
        {
          "name": "导出",
          "code": "export"
        }
      ]
    }
  ],
  "actions": ["access", "execute"]
}
```
我们分配一台服务器：server_2023 给他使用，他可以在上面进行任意操作，同时他可以阅读、编辑研发知识库，最后他可以在研发内部平台中进行部署测试环境，但是不能够导出数据库数据。
```json
{
  "policyName": "研发人员策略",
  "description": "这是一个示例数据策略",
  "statementList": [
    {
      "effect": "ALLOW",
      "permissions": [ 
        "examplePermissionNamespaceCode/server_2023/*",
        "examplePermissionNamespaceCode/rd_document/read",
        "examplePermissionNamespaceCode/rd_document/write",
        "examplePermissionNamespaceCode/rd_internal_platform/deploy/test/execute"
       ]
    },
    {
      "effect": "DENY",
      "permissions": [ 
        "examplePermissionNamespaceCode/rd_internal_platform/db/export/execute"
      ]
    }
  ]
}
```


        Attributes:
            statement_list (list): 数据权限列表，策略下数据资源权限列表
            policy_name (str): 数据策略名称，用户池唯一
            description (str): 数据策略描述
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-data-policy',
            json={
                'statementList': statement_list,
                'policyName': policy_name,
                'description': description,
            },
        )

    def list_data_polices(self, page=None, limit=None, query=None):
        """获取数据策略列表

        分页查询数据策略列表，也可通过关键字搜索数据策略名称或者数据策略 Code 进行模糊查找。

        Attributes:
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            query (str): 数据策略名称关键字搜索
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-data-policies',
            params={
                'page': page,
                'limit': limit,
                'query': query,
            },
        )

    def list_simple_data_polices(self, page=None, limit=None, query=None):
        """获取数据策略简略信息列表

        分页获取数据策略简略信息列表，通过关键字搜索数据策略名称或者数据策略 Code 进行模糊查找出数据策略 ID、数据策略名称和数据策略描述信息。

        Attributes:
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            query (str): 数据策略名称关键字搜索
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-simple-data-policies',
            params={
                'page': page,
                'limit': limit,
                'query': query,
            },
        )

    def get_data_policy(self, policy_id):
        """获取数据策略详情

        获取数据策略详情，通过数据策略 ID 获取对应数据策略信息,包含数据策略 ID、数据策略名称、数据策略描述、数据策略下所有的数据权限列表等信息。

        Attributes:
            policyId (str): 数据策略 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-data-policy',
            params={
                'policyId': policy_id,
            },
        )

    def update_data_policy(self, policy_id, policy_name=None, description=None, statement_list=None):
        """修改数据策略

        修改数据策略，通过数据策略名称、数据策略描述和相关的数据资源等字段修改数据策略信息。

        Attributes:
            policy_id (str): 数据策略 ID
            policy_name (str): 数据策略名称，用户池唯一
            description (str): 数据策略描述
            statement_list (list): 数据权限列表，每个策略下所有的数据权限
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-data-policy',
            json={
                'policyId': policy_id,
                'policyName': policy_name,
                'description': description,
                'statementList': statement_list,
            },
        )

    def delete_data_policy(self, policy_id):
        """删除数据策略

        删除数据策略，通过数据策略 ID 删除对应的策略,同时也删除数据策略和对应的数据资源等关系数据。

        Attributes:
            policy_id (str): 数据策略 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-data-policy',
            json={
                'policyId': policy_id,
            },
        )

    def check_data_policy_exists(self, policy_name):
        """检查数据策略名称是否可用

        通过数据策略名称查询用户池内是否有效。

        Attributes:
            policyName (str): 数据策略名称，用户池唯一
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/check-data-policy-exists',
            params={
                'policyName': policy_name,
            },
        )

    def list_data_policy_targets(self, policy_id, page=None, limit=None, query=None, target_type=None):
        """获取数据策略授权的主体列表

        获取数据策略授权的主体列表，通过授权主体类型、数据策略 ID 和数据资源 ID 查找授权主体列表。

        Attributes:
            policyId (str): 数据策略 ID
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            query (str): 主体名称
            targetType (str): 主体类型,包括 USER、GROUP、ROLE、ORG 四种类型
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-data-policy-targets',
            params={
                'policyId': policy_id,
                'page': page,
                'limit': limit,
                'query': query,
                'targetType': target_type,
            },
        )

    def authorize_data_policies(self, target_list, policy_ids):
        """授权数据策略

        数据策略创建主体授权，通过授权主体和数据策略进行相互授权。

        Attributes:
            target_list (list): 数据权限列表，每个策略下所有的数据权限
            policy_ids (list): 数据策略 id 列表
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/authorize-data-policies',
            json={
                'targetList': target_list,
                'policyIds': policy_ids,
            },
        )

    def revoke_data_policy(self, target_type, target_identifier, policy_id):
        """删除数据策略授权

        删除数据策略授权，通过授权主体 ID、授权主体类型和数据策略 ID 进行删除。

        Attributes:
            target_type (str): 主体类型,包括 USER、GROUP、ROLE、ORG 四种类型
            target_identifier (str): 主体 ID ，包含用户 ID、用户组 ID、角色 ID、组织机构 ID
            policy_id (str): 数据策略 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/revoke-data-policy',
            json={
                'targetType': target_type,
                'targetIdentifier': target_identifier,
                'policyId': policy_id,
            },
        )

    def get_user_permission_list(self, user_ids, namespace_codes=None):
        """获取用户权限列表

        
  ## 描述
  该接口用于查询某些用户在某些权限空间的数据资源的权限数据。
我们的鉴权接口针对不同的鉴权场景有多种，区别在于在所处的场景下能够传递的参数列表以及不同形式的出参，**当你需要查询某些用户的所有权限时**可以使用此接口，
## 注意
接口提供了两个数组类型的入参`userIds`和`namespaceCodes`来支持批量查询（注意：namespaceCodes 是可选的）。
## 场景举例
假如你的业务场景是用户登录后能看到他所有可以访问或者进行其他操作的文档、人员信息、设备信息等资源，那么你可以在用户登录后调用此接口查询用户的所有权限。
## 请求示例
### 查询单个用户权限列表示例
注意：在此接口的返回参数中，树类型的数据资源权限返回是按照**路径**的方式返回的
- 入参
  
```json
{
    "userIds": [
      "6301ceaxxxxxxxxxxx27478"  
    ]
}
```

- 出参
  
```json
{
  "statusCode": 200, 
  "message": "操作成功", 
  "apiCode": 20001, 
  "data": {
    "userPermissionList": [
      {
        "userId": "6301ceaxxxxxxxxxxx27478", 
        "namespaceCode": "examplePermissionNamespace", 
        "resourceList": [
          {
            "resourceCode": "strCode",
            "resourceType": "STRING",
            "strAuthorize": {
              "value": "示例字符串资源", 
              "actions": [
                "read", 
                "post", 
                "get", 
                "write"
              ]
            }
          },
          {
            "resourceCode": "arrayCode", 
            "resourceType": "ARRAY",
            "arrAuthorize": {
              "values": [
                "示例数据资源1",
                "示例数据资源2"
              ], 
              "actions": [
                "read", 
                "post", 
                "get", 
                "write"
              ]
            }
          }, 
          {
            "resourceCode": "treeCode", 
            "resourceType": "TREE",
            "treeAuthorize": {
              "authList": [
                {
                  "nodePath": "/treeChildrenCode/treeChildrenCode1", 
                  "nodeActions": [
                    "read", 
                    "get"
                  ], 
                  "nodeName": "treeChildrenName1", 
                  "nodeValue": "treeChildrenValue1"
                }, 
                {
                  "nodePath": "/treeChildrenCode/treeChildrenCode2", 
                  "nodeActions": [
                    "read", 
                    "get"
                  ], 
                  "nodeName": "treeChildrenName2", 
                  "nodeValue": "treeChildrenValue2"
                }, 
                {
                  "nodePath": "/treeChildrenCode/treeChildrenCode3", 
                  "nodeActions": [
                    "read"
                  ], 
                  "nodeName": "treeChildrenName3", 
                  "nodeValue": "treeChildrenValue3"
                }
              ]
            }
          }
        ]
      }
    ]
  }
}
```

### 查询多个用户权限列表示例

- 入参

```json
{
  "userIds": [
    "6301ceaxxxxxxxxxxx27478",
    "6121ceaxxxxxxxxxxx27312"
  ]
}
```

- 出参

```json
{
  "statusCode": 200, 
  "message": "操作成功", 
  "apiCode": 20001, 
  "data": {
    "userPermissionList": [
      {
        "userId": "6301ceaxxxxxxxxxxx27478", 
        "namespaceCode": "examplePermissionNamespace1", 
        "resourceList": [
          {
            "resourceCode": "strCode",
            "resourceType": "STRING",
            "strAuthorize": {
              "value": "示例字符串资源", 
              "actions": [
                "read", 
                "post", 
                "get", 
                "write"
              ]
            }
          }
        ]
      }, 
      {
        "userId": "6121ceaxxxxxxxxxxx27312", 
        "namespaceCode": "examplePermissionNamespace2", 
        "resourceList": [
          {
            "resourceCode": "arrayCode", 
            "resourceType": "ARRAY",
            "arrAuthorize": {
              "values": [
                "示例数组资源1", 
                "示例数组资源2"
              ], 
              "actions": [
                "read", 
                "post", 
                "get", 
                "write"
              ]
            }
          }
        ]
      }
    ]
  }
}
```

### 查询多个用户在多个权限空间下权限列表示例

- 入参

```json
{
  "userIds": [
    "6301ceaxxxxxxxxxxx27478",
    "6121ceaxxxxxxxxxxx27312"
  ],
  "namespaceCodes": [
    "examplePermissionNamespace1",
    "examplePermissionNamespace2"
  ]
}
```

- 出参

```json
{
  "statusCode": 200, 
  "message": "操作成功", 
  "apiCode": 20001, 
  "data": {
    "userPermissionList": [
      {
        "userId": "6301ceaxxxxxxxxxxx27478", 
        "namespaceCode": "examplePermissionNamespace1", 
        "resourceList": [
          {
            "resourceCode": "strCode1", 
            "resourceType": "STRING",
            "strAuthorize": {
              "value": "示例字符串资源", 
              "actions": [
                "read", 
                "post", 
                "get", 
                "write"
              ]
            }
          }
        ]
      }, 
      {
        "userId": "6121ceaxxxxxxxxxxx27312", 
        "namespaceCode": "examplePermissionNamespace2", 
        "resourceList": [
          {
            "resourceCode": "arrayCode", 
            "resourceType": "ARRAY",
            "arrAuthorize": {
              "values": [
                "示例数组资源1", 
                "示例数组资源2"
              ], 
              "actions": [
                "read", 
                "post", 
                "get", 
                "write"
              ]
            }
          }
        ]
      }
    ]
  }
}
```
  

        Attributes:
            user_ids (list): 用户 ID 列表
            namespace_codes (list): 权限空间 Code 列表
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-user-permission-list',
            json={
                'userIds': user_ids,
                'namespaceCodes': namespace_codes,
            },
        )

    def check_permission(self, resources, action, user_id, namespace_code, judge_condition_enabled=None,
                         auth_env_params=None):
        """判断用户权限（重点）

        
  ## 描述
  当你需要判断用户是否拥有某些资源的指定权限时可以使用此接口
  ## 注意
  - 该接口通过传递资源 code 定位对应的数据资源（如果是树类型，则需要传递节点的完整 code 路径）。
  - 如果你在配置数据策略时配置了**环境属性**的条件判断，那么需要设置参数`judgeConditionEnabled`为`true`（默认为 false），并且通过参数`authEnvParams`传递请求时所处的环境信息（如 IP、设备类型、系统类型等），否则条件判断会不生效，导致数据策略不生效。

## 场景举例
用户在删除某条数据时，需要判断他是否拥有此资源的删除权限，则可以使用此接口。

## 请求示例
### 判断用户对字符串和数组资源权限示例（无条件判断）

- 入参

```json
{
  "namespaceCode": "examplePermissionNamespace",
  "userId": "63721xxxxxxxxxxxxdde14a3",
  "action": "get",
  "resources":["strResourceCode1", "arrayResourceCode1"]
}
```

- 出参

```json
{
  "statusCode": 200,
  "message": "操作成功",
  "apiCode": 20001,
  "data": {
      "checkResultList": [
          {
              "namespaceCode": "examplePermissionNamespace",
              "resource": "strResourceCode1",
              "action": "get",
              "enabled": true
          },
          {
              "namespaceCode": "examplePermissionNamespace",
              "resource": "arrayResourceCode1",
              "action": "get",
              "enabled": true
          }
      ]
  }
}
```

### 判断用户对字符串和数组资源权限示例（开启条件判断）

- 入参

```json
{
  "namespaceCode": "examplePermissionNamespace",
  "userId": "63721xxxxxxxxxxxxdde14a3",
  "action": "get",
  "resources": ["strResourceCode1", "arrayResourceCode1"],
  "judgeConditionEnabled": true,
  "authEnvParams":{
      "ip":"110.96.0.0",
      "city":"北京",
      "province":"北京",
      "country":"中国",
      "deviceType":"PC",
      "systemType":"ios",
      "browserType":"IE",
      "requestDate":"2022-12-26 17:40:00"
  }
}
```

- 出参

```json
{
  "statusCode": 200,
  "message": "操作成功",
  "apiCode": 20001,
  "data": {
      "checkResultList": [
          {
              "namespaceCode": "examplePermissionNamespace",
              "resource": "strResourceCode1",
              "action": "get",
              "enabled": false
          },
          {
              "namespaceCode": "examplePermissionNamespace",
              "resource": "arrayResourceCode1",
              "action": "get",
              "enabled": false
          }
      ]
  }
}
```

### 判断用户对树资源权限示例

- 入参

```json
{
  "namespaceCode": "examplePermissionNamespace",
  "userId": "63721xxxxxxxxxxxxdde14a3",
  "action": "get",
  "resources":["treeResourceCode1/StructCode1/resourceStructChildrenCode1", "treeResourceCode2/StructCode1/resourceStructChildrenCode1"]
}
```

- 出参

```json
{
  "statusCode": 200,
  "message": "操作成功",
  "apiCode": 20001,
  "data":{
    "checkResultList": [{
      "namespaceCode": "examplePermissionNamespace",
      "action": "get",
      "resource": "treeResourceCode1/StructCode1/resourceStructChildrenCode1",
      "enabled": true     
    },{
      "namespaceCode": "examplePermissionNamespace",
      "action": "get",
      "resource": "treeResourceCode2/StructCode1/resourceStructChildrenCode1",
      "enabled": true     
    }]
  }
}
```
  

        Attributes:
            resources (list): 资源路径列表,**树资源需到具体树节点**
            action (str): 数据资源权限操作, read、get、write 等动作
            user_id (str): 用户 ID
            namespace_code (str): 权限空间 Code
            judge_condition_enabled (bool): 是否开启条件判断，默认 false 不开启
            auth_env_params (dict): 条件环境属性，若开启条件判断则使用
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/check-permission',
            json={
                'resources': resources,
                'action': action,
                'userId': user_id,
                'namespaceCode': namespace_code,
                'judgeConditionEnabled': judge_condition_enabled,
                'authEnvParams': auth_env_params,
            },
        )

    def check_external_user_permission(self, resources, action, external_id, namespace_code,
                                       judge_condition_enabled=None, auth_env_params=None):
        """判断外部用户权限

        
  ## 描述
  当你的用户是外部用户，需要判断其是否拥有某资源的某一权限时，可以使用此接口，通过`externalId`来传递用户的 ID
  

        Attributes:
            resources (list): 资源路径列表,**树资源需到具体树节点**
            action (str): 数据资源权限操作, read、get、write 等动作
            external_id (str): 外部用户 ID
            namespace_code (str): 权限空间 Code
            judge_condition_enabled (bool): 是否开启条件判断，默认 true 开启
            auth_env_params (dict): 条件环境属性，若开启条件判断则使用
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/check-external-user-permission',
            json={
                'resources': resources,
                'action': action,
                'externalId': external_id,
                'namespaceCode': namespace_code,
                'judgeConditionEnabled': judge_condition_enabled,
                'authEnvParams': auth_env_params,
            },
        )

    def get_user_resource_permission_list(self, resources, user_id, namespace_code):
        """获取用户拥有某些资源的权限列表（推荐）

        
  ## 描述
  当你需要查询某一用户拥有指定的资源列表的权限时，可以使用此接口。
  ## 注意
  该接口需要你传递指定的资源 code（如果是树类型资源则需要传递节点的完整 code 路径），此接口性能更佳，推荐使用。
  ## 请求示例
### 获取用户字符串和数组资源权限示例

- 入参
  
```json
{
  "namespaceCode": "examplePermissionNamespace",
  "userId": "63721xxxxxxxxxxxxdde14a3",
  "resources":["strResourceCode1", "arrayResourceCode1"]
}
```

- 出参

```json
{

  "statusCode": 200,
  "message": "操作成功",
  "apiCode": 20001,
  "data":{
    "permissionList": [{
      "namespaceCode": "examplePermissionNamespace",
      "actions": ["read","get"],  
      "resource": "strResourceCode1"
    },{
      "namespaceCode": "examplePermissionNamespace",
      "actions": ["read","update","delete"], 
      "resource": "arrayResourceCode1"
    }]
  }
}
```
  
### 获取用户树资源权限示例
  
- 入参
  
```json
{
  "namespaceCode": "examplePermissionNamespace",
  "userId": "63721xxxxxxxxxxxxdde14a3",
  "resources":["treeResourceCode1/StructCode1/resourceStructChildrenCode1", "treeResourceCode2/StructCode1/resourceStructChildrenCode1"]
}
```

- 出参

```json
{
  "statusCode": 200,
  "message": "操作成功",
  "apiCode": 20001,
  "data":{
    "permissionList": [{
      "namespaceCode": "examplePermissionNamespace",
      "actions": ["read", "update", "delete"],
      "resource": "treeResourceCode1/StructCode1/resourceStructChildrenCode1"
    },{
      "namespaceCode": "examplePermissionNamespace",
      "actions": ["read", "get", "delete"],     
      "resource": "treeResourceCode2/StructCode1/resourceStructChildrenCode1"
    }]
  }
}
```
  

        Attributes:
            resources (list): 资源路径列表,**树资源需到具体树节点**
            user_id (str): 用户 ID
            namespace_code (str): 权限空间 Code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-user-resource-permission-list',
            json={
                'resources': resources,
                'userId': user_id,
                'namespaceCode': namespace_code,
            },
        )

    def list_resource_targets(self, resources, actions, namespace_code):
        """获取拥有某些资源权限的用户列表

        
  ## 描述
  当你需要获取拥有指定资源的权限的用户时，可以使用此接口。
  ## 场景举例
  假如你的业务场景是：想看看当前文档能够编辑的用户列表，那么你可以使用此接口。
  ## 请求示例
### 获取字符串和数组资源被授权的用户列表示例

- 入参
    
```json
{
  "namespaceCode": "examplePermissionNamespace",
  "actions": ["get", "update", "read"],
  "resources":["strResourceCode1", "arrayResourceCode1"]
}
```
  
- 出参
  
```json
{
  "statusCode": 200,
  "message": "操作成功",
  "apiCode": 20001,
  "data":{
    "authUserList": [{
      "resource": "strResourceCode1",
      "actionAuthList": [{
        "userIds": ["63721xxxxxxxxxxxxdde14a3"],
        "action": "get"
      },{
        "userIds": ["63721xxxxxxxxxxxxdde14a3"],
        "action": "update"
      },{
        "userIds": ["63721xxxxxxxxxxxxdde14a3"],
        "action": "read"
      }]  
    },{
      "resource": "arrayResourceCode1",
      "actionAuthList": [{
      "userIds": ["63721xxxxxxxxxxxxdde14a3"],
        "action": "get"
      },{
        "userIds": ["63721xxxxxxxxxxxxdde14a3"],
        "action": "update"
      },{
        "userIds": ["63721xxxxxxxxxxxxdde14a3"],
        "action": "read"
      }] 
    }]
  }
}
```
    
### 获取树资源被授权的用户列表示例
    
- 入参
    
```json
{
  "namespaceCode": "examplePermissionNamespace",
  "actions": ["get", "update", "delete"],
  "resources":["treeResourceCode1/StructCode1/resourceStructChildrenCode1", "treeResourceCode2/StructCode1/resourceStructChildrenCode1"]
}
```
  
- 出参
  
```json
{
  "statusCode": 200,
  "message": "操作成功",
  "apiCode": 20001,
  "data":{
    "authUserList": [{
      "resource": "treeResourceCode1/StructCode1/resourceStructChildrenCode1",
      "actionAuthList": [{
        "userIds": ["63721xxxxxxxxxxxxdde14a3"],
        "action": "get"
      },{
        "userIds": ["63721xxxxxxxxxxxxdde14a3"],
        "action": "update"
      },{
        "userIds": ["63721xxxxxxxxxxxxdde14a3"],
        "action": "delete"
      }]  
    },{
      "resource": "treeResourceCode2/StructCode1/resourceStructChildrenCode1",
      "actionAuthList": [{
        "userIds": ["63721xxxxxxxxxxxxdde14a3"],
        "action": "get"
      },{
        "userIds": ["63721xxxxxxxxxxxxdde14a3"],
        "action": "update"
      },{
        "userIds": ["63721xxxxxxxxxxxxdde14a3"],
        "action": "delete"
      }] 
    }]
  }
}
```
  

        Attributes:
            resources (list): 数据策略所属的数据资源路径列表
            actions (list): 数据资源权限操作列表
            namespace_code (str): 权限空间 Code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/list-resource-targets',
            json={
                'resources': resources,
                'actions': actions,
                'namespaceCode': namespace_code,
            },
        )

    def get_user_resource_struct(self, resource_code, user_id, namespace_code):
        """获取用户拥有指定资源的权限及资源结构信息

        
  ## 描述
  当你需要获取用户拥有某一资源的权限并且需要这个资源的结构信息（树类型资源返回树结构，数组类型资源返回数组、字符串类型返回字符串）则可以使用此接口。
  ## 注意
  由于其他接口对树类型资源的返回参数格式是按照路径的方式返回的，所以我们提供此此接口，按照完整的树结构形式返回。
  ## 请求示例
### 获取用户授权字符串数据资源示例
  
- 入参

```json
{
  "namespaceCode": "examplePermissionNamespace",
  "userId": "63721xxxxxxxxxxxxdde14a3",
  "resourceCode": "exampleStrResourceCode"
}
```

- 出参

```json
{
  "statusCode": 200,
  "message": "操作成功",
  "apiCode": 20001,
  "data":{
    "namespaceCode": "exampleNamespaceCode",
    "resourceCode": "exampleStrResourceCode",
    "resourceType": "STRING",
    "strResourceAuthAction":{
      "value": "strTestValue",
      "actions": ["get","delete"]
    }
  }
}
```


### 获取用户授权数据数组资源示例
  
- 入参

```json
{
  "namespaceCode": "examplePermissionNamespace",
  "userId": "63721xxxxxxxxxxxxdde14a3",
  "resourceCode": "exampleArrResourceCode"
}
```

- 出参

```json
{
  "statusCode": 200,
  "message": "操作成功",
  "apiCode": 20001,
  "data":{
    "namespaceCode": "exampleNamespaceCode",
    "resourceCode": "exampleArrResourceCode",
    "resourceType": "ARRAY",
    "arrResourceAuthAction":{
      "values": ["arrTestValue1","arrTestValue2","arrTestValue3"],
      "actions": ["get","delete"]
    }
  }
}
```


### 获取用户授权树数据资源示例
  
- 入参

```json
{
  "namespaceCode": "examplePermissionNamespace",
  "userId": "63721xxxxxxxxxxxxdde14a3",
  "resourceCode": "exampleTreeResourceCode"
}
```

- 出参

```json
{
  "statusCode": 200,
  "message": "操作成功",
  "apiCode": 20001,
  "data":{
    "namespaceCode": "exampleNamespaceCode",
    "resourceCode": "exampleArrResourceCode",
    "resourceType": "TREE",
    "treeResourceAuthAction":{
        "nodeAuthActionList":[{
            "code": "tree11",
            "name": "tree11",
            "value": "test11Value",
            "actions": ["get","delete"],
            "children": [{
              "code": "tree111",
              "name": "tree111",
              "value": "test111Value",
              "actions": ["update","read"],
            }]
        },{
            "code": "tree22",
            "name": "tree22",
            "value": "test22Value",
            "actions": ["get","delete"]
        }]
    }
  }
}
```
  

        Attributes:
            resource_code (str): 数据资源 Code
            user_id (str): 用户 ID 
            namespace_code (str): 权限空间 Code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-user-resource-struct',
            json={
                'resourceCode': resource_code,
                'userId': user_id,
                'namespaceCode': namespace_code,
            },
        )

    def get_external_user_resource_struct(self, resource_code, external_id, namespace_code):
        """获取外部用户拥有指定资源的权限及资源结构信息

        
  ## 描述
  当你需要获取外部用户（通过参数`externalId`参数传递外部用户 ID）拥有某一资源的权限并且需要这个资源的结构信息（树类型资源返回树结构，数组类型资源返回数组、字符串类型返回字符串）则可以使用此接口。
  ## 请求示例
### 获取用户授权字符串数据资源示例
  
- 入参

```json
{
  "namespaceCode": "examplePermissionNamespace",
  "externalId": "63721xxxxxxxxxxxxdde14a3",
  "resourceCode": "exampleStrResourceCode"
}
```

- 出参

```json
{
  "statusCode": 200,
  "message": "操作成功",
  "apiCode": 20001,
  "data":{
    "namespaceCode": "exampleNamespaceCode",
    "resourceCode": "exampleStrResourceCode",
    "resourceType": "STRING",
    "strResourceAuthAction":{
      "value": "strTestValue",
      "actions": ["get","delete"]
    }
  }
}
```


### 获取用户授权数据数组资源示例
  
- 入参

```json
{
  "namespaceCode": "examplePermissionNamespace",
  "externalId": "63721xxxxxxxxxxxxdde14a3",
  "resourceCode": "exampleArrResourceCode"
}
```

- 出参

```json
{
  "statusCode": 200,
  "message": "操作成功",
  "apiCode": 20001,
  "data":{
    "namespaceCode": "exampleNamespaceCode",
    "resourceCode": "exampleArrResourceCode",
    "resourceType": "ARRAY",
    "arrResourceAuthAction":{
      "values": ["arrTestValue1","arrTestValue2","arrTestValue3"],
      "actions": ["get","delete"]
    }
  }
}
```


### 获取用户授权树数据资源示例
  
- 入参

```json
{
  "namespaceCode": "examplePermissionNamespace",
  "externalId": "63721xxxxxxxxxxxxdde14a3",
  "resourceCode": "exampleTreeResourceCode"
}
```

- 出参

```json
{
  "statusCode": 200,
  "message": "操作成功",
  "apiCode": 20001,
  "data":{
    "namespaceCode": "exampleNamespaceCode",
    "resourceCode": "exampleArrResourceCode",
    "resourceType": "TREE",
    "treeResourceAuthAction":{
        "nodeAuthActionList":[{
            "code": "tree11",
            "name": "tree11",
            "value": "test11Value",
            "actions": ["get","delete"],
            "children": [{
              "code": "tree111",
              "name": "tree111",
              "value": "test111Value",
              "actions": ["update","read"],
            }]
        },{
            "code": "tree22",
            "name": "tree22",
            "value": "test22Value",
            "actions": ["get","delete"]
        }]
    }
  }
}
```
  

        Attributes:
            resource_code (str): 资源 Code
            external_id (str): 外部用户 ID
            namespace_code (str): 权限空间 Code
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-external-user-resource-struct',
            json={
                'resourceCode': resource_code,
                'externalId': external_id,
                'namespaceCode': namespace_code,
            },
        )

    def check_user_same_level_permission(self, resource_node_codes, resource, action, user_id, namespace_code,
                                         judge_condition_enabled=None, auth_env_params=None):
        """判断用户在树资源同层级下的权限（推荐）

        
  ## 描述
  此接口用于判断用户是否拥有某一树资源的**同层级下**部分的节点的某种权限。由于树类型资源比较常用，所以我们基于“判断用户是否拥有资源权限”的业务场景，新增了针对判断树这种类型资源节点权限的接口。
  ## 注意
  我们通过`resource`参数定位到树类型数据资源的某一层级（所以该参数是按照`资源 code/节点 code 路径`格式进行传递的），并通过`resourceNodeCodes`参数定位到是当前曾经的哪些节点。
  ## 场景举例
假如你的业务场景是：当在一个文件系统中，用户在删除某一文件夹下某些文件，需要判断他是否拥有这些文件的删除权限，则可以使用此接口。
## 请求示例
### 判断用户在树资源同层级权限示例（无条件判断）

```json
{
  "namespaceCode": "examplePermissionNamespace",
  "userId": "63721xxxxxxxxxxxxdde14a3",
  "action": "read",
  "resource": "treeResourceCode/structCode",
  "resourceNodeCodes": ["resourceStructChildrenCode1","resourceStructChildrenCode2","resourceStructChildrenCode3"]
}
```

### 判断用户在树资源同层级权限示例（开启条件判断）

```json
{
  "namespaceCode": "examplePermissionNamespace",
  "userId": "63721xxxxxxxxxxxxdde14a3",
  "action": "read",
  "resource": "treeResourceCode/structCode",
  "resourceNodeCodes": ["resourceStructChildrenCode1","resourceStructChildrenCode2","resourceStructChildrenCode3"],
  "judgeConditionEnabled": true,
  "authEnvParams":{
      "ip":"110.96.0.0",
      "city":"北京",
      "province":"北京",
      "country":"中国",
      "deviceType":"PC",
      "systemType":"ios",
      "browserType":"IE",
      "requestDate":"2022-12-26 17:40:00"
  }
}
```
  

        Attributes:
            resource_node_codes (list): 当前树资源路径子节点 Code
            resource (str): 树资源路径,允许多层级路径，示例如下所示
- treeResourceCode
- treeResourceCode/structCode
- treeResourceCode/structCode/struct1Code
- treeResourceCode/.../structCode
            action (str): 数据资源权限操作
            user_id (str): 用户 ID
            namespace_code (str): 权限空间 Code
            judge_condition_enabled (bool): 是否开启条件判断，默认 false 不开启
            auth_env_params (dict): 条件环境属性，若开启条件判断则使用
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/check-user-same-level-permission',
            json={
                'resourceNodeCodes': resource_node_codes,
                'resource': resource,
                'action': action,
                'userId': user_id,
                'namespaceCode': namespace_code,
                'judgeConditionEnabled': judge_condition_enabled,
                'authEnvParams': auth_env_params,
            },
        )

    def list_permission_view(self, page=None, limit=None, keyword=None):
        """获取权限视图数据列表

        
  ## 描述
  此接口用于导出菜单：权限管理 -> 数据权限 -> 权限试图列表数据，如果你需要拉取我们数据权限的授权数据（所有用户拥有的所有资源的所有权限），则可以使用此接口。
  

        Attributes:
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            keyword (str): 关键字搜索,可以支持 userName 搜索
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/list-permission-view/data',
            json={
                'page': page,
                'limit': limit,
                'keyword': keyword,
            },
        )

    def get_current_package_info(self, ):
        """获取套餐详情

        获取当前用户池套餐详情。

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-current-package-info',
        )

    def get_usage_info(self, ):
        """获取用量详情

        获取当前用户池用量详情。

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-usage-info',
        )

    def get_mau_period_usage_history(self, start_time, end_time):
        """获取 MAU 使用记录

        获取当前用户池 MAU 使用记录

        Attributes:
            startTime (str): 起始时间（年月日）
            endTime (str): 截止时间（年月日）
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-mau-period-usage-history',
            params={
                'startTime': start_time,
                'endTime': end_time,
            },
        )

    def get_all_rights_item(self, ):
        """获取所有权益

        获取当前用户池所有权益

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-all-rights-items',
        )

    def get_orders(self, page=None, limit=None):
        """获取订单列表

        获取当前用户池订单列表

        Attributes:
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-orders',
            params={
                'page': page,
                'limit': limit,
            },
        )

    def get_order_detail(self, order_no):
        """获取订单详情

        获取当前用户池订单详情

        Attributes:
            orderNo (str): 订单号
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-order-detail',
            params={
                'orderNo': order_no,
            },
        )

    def get_order_pay_detail(self, order_no):
        """获取订单支付明细

        获取当前用户池订单支付明细

        Attributes:
            orderNo (str): 订单号
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-order-pay-detail',
            params={
                'orderNo': order_no,
            },
        )

    def create_event_app(self, logo, name, identifier):
        """创建自定义事件应用

        创建自定义事件应用

        Attributes:
            logo (str): 应用 logo
            name (str): 应用名称
            identifier (str): 应用唯一标志
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-event-app',
            json={
                'logo': logo,
                'name': name,
                'identifier': identifier,
            },
        )

    def list_event_apps(self, ):
        """获取事件应用列表

        获取事件应用列表

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-event-apps',
        )

    def list_events(self, page=None, limit=None, app=None):
        """获取事件列表

        获取 Authing 服务支持的所有事件列表

        Attributes:
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
            app (str): 应用类型
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-events',
            params={
                'page': page,
                'limit': limit,
                'app': app,
            },
        )

    def define_event(self, event_description, event_type):
        """定义自定义事件

        在 Authing 事件中心定义自定义事件

        Attributes:
            event_description (str): 事件描述
            event_type (str): 事件类型
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/define-event',
            json={
                'eventDescription': event_description,
                'eventType': event_type,
            },
        )

    def verify_event(self, event_type, event_data):
        """推送自定义事件

        向 Authing 事件中心推送自定义事件

        Attributes:
            event_type (str): 事件类型
            event_data (dict): 事件体
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/pub-event',
            json={
                'eventType': event_type,
                'eventData': event_data,
            },
        )

    def pub_user_event(self, event_type, event_data):
        """认证端推送自定义事件

        认证端向 Authing 事件中心推送自定义事件

        Attributes:
            event_type (str): 事件类型
            event_data (dict): 事件体
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/pub-userEvent',
            json={
                'eventType': event_type,
                'eventData': event_data,
            },
        )

    def add_whitelist(self, type, list=None):
        """创建注册白名单

        你需要指定注册白名单类型以及数据，来进行创建

        Attributes:
            type (str): 白名单类型
            list (list): 类型参数
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/add-whitelist',
            json={
                'type': type,
                'list': list,
            },
        )

    def list_whitelists(self, type):
        """获取注册白名单列表

        获取注册白名单列表，可选页数、分页大小来获取

        Attributes:
            type (str): 白名单类型
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-whitelist',
            params={
                'type': type,
            },
        )

    def delete_whitelist(self, type, list=None):
        """删除注册白名单

        通过指定多个注册白名单数据,以数组的形式进行注册白名单的删除

        Attributes:
            type (str): 白名单类型
            list (list): 类型参数
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-whitelist',
            json={
                'type': type,
                'list': list,
            },
        )

    def find_ip_list(self, ip_type, page=None, limit=None):
        """获取 ip 列表

        分页获取 ip 列表

        Attributes:
            ipType (str): IP 类型
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/ip-list',
            params={
                'page': page,
                'limit': limit,
                'ipType': ip_type,
            },
        )

    def add(self, expire_at, limit_list, remove_type, add_type, ip_type, ips):
        """创建 ip 名单

        创建 ip 名单

        Attributes:
            expire_at (str): 添加时间
            limit_list (list): 限制类型，FORBID_LOGIN-禁止登录，FORBID_REGISTER-禁止注册，SKIP_MFA-跳过 MFA
            remove_type (str): 删除类型，MANUAL-手动，SCHEDULE-策略删除
            add_type (str): 添加类型，MANUAL-手动，SCHEDULE-策略添加
            ip_type (str): ip类型，WHITE-白名单，BLACK-黑名单
            ips (str): ip, 多个IP以逗号分割
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/ip-list',
            json={
                'expireAt': expire_at,
                'limitList': limit_list,
                'removeType': remove_type,
                'addType': add_type,
                'ipType': ip_type,
                'ips': ips,
            },
        )

    def delete_by_id(self, id):
        """删除 ip 名单

        删除 ip 名单

        Attributes:
            id (str): 
        """
        return self.http_client.request(
            method='DELETE',
            url='/api/v3/ip-list/{id}',
        )

    def find_user_list(self, user_list_type, page=None, limit=None):
        """获取用户列表

        分页获取用户列表

        Attributes:
            userListType (str): IP 类型
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/user-list',
            params={
                'page': page,
                'limit': limit,
                'userListType': user_list_type,
            },
        )

    def add_user(self, expire_at, limit_list, remove_type, add_type, user_list_type, user_ids):
        """创建用户名单

        创建用户名单

        Attributes:
            expire_at (int): 过期时间
            limit_list (list): 限制类型，FORBID_LOGIN-禁止登录，FORBID_REGISTER-禁止注册，SKIP_MFA-跳过 MFA
            remove_type (str): 删除类型，MANUAL-手动，SCHEDULE-策略删除
            add_type (str): 添加类型，MANUAL-手动，SCHEDULE-策略添加
            user_list_type (str): 用户名单类型，WHITE-白名单，BLACK-黑名单
            user_ids (list): userId, 多个 userId 以逗号分割
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/user-list',
            json={
                'expireAt': expire_at,
                'limitList': limit_list,
                'removeType': remove_type,
                'addType': add_type,
                'userListType': user_list_type,
                'userIds': user_ids,
            },
        )

    def delete_user_list_by_id(self, id):
        """删除用户名单

        删除用户 名单

        Attributes:
            id (str): 
        """
        return self.http_client.request(
            method='DELETE',
            url='/api/v3/user-list/{id}',
        )

    def find_risk_list_policy(self, opt_object, page=None, limit=None):
        """获取风险策略列表

        分页获取风险策略列表

        Attributes:
            optObject (str): 策略操作对象，目前只有 ip
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/risk-list-policy',
            params={
                'page': page,
                'limit': limit,
                'optObject': opt_object,
            },
        )

    def add_risk_list_policy(self, limit_list, action, remove_type, event_state_type, count_thr, time_range, user_cond,
                             ip_cond, user_range, ip_range, opt_object):
        """创建风险策略

        创建风险策略

        Attributes:
            limit_list (str): 限制类型列表,FORBID_LOGIN-禁止登录，FORBID_REGISTER-禁止注册
            action (str): 策略动作, ADD_IP_BLACK_LIST-添加IP黑名单，ADD_USER_BLACK_LIST-添加用户黑名单
            remove_type (str): 移除类型，MANUAL-手动，SCHEDULE-策略, 目前只有手动
            event_state_type (str): 事件状态类型，password_wrong-密码错误，account_wrong-账号错误
            count_thr (int): 次数阈值
            time_range (int): 时间范围，最近多少分钟
            user_cond (str): IP条件, NO_LIMIT-不限制，ONE-单个用户，与 ipCond 二者取一个
            ip_cond (str): IP条件, NO_LIMIT-不限制，ONE-单个IP，与 userCond 二者取一个
            user_range (str): 操作USER的范围, ALL-所有，NOT_IN_WHITE_LIST-不在白名单中，与 ipRange 二者取一个
            ip_range (str): 操作IP的范围, ALL-所有，NOT_IN_WHITE_LIST-不在白名单中，与 userRange 二者取一个
            opt_object (str): 策略操作对象，目前只有 ip
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/risk-list-policy',
            json={
                'limitList': limit_list,
                'action': action,
                'removeType': remove_type,
                'eventStateType': event_state_type,
                'countThr': count_thr,
                'timeRange': time_range,
                'userCond': user_cond,
                'ipCond': ip_cond,
                'userRange': user_range,
                'ipRange': ip_range,
                'optObject': opt_object,
            },
        )

    def delete_risk_list_policy_by_id(self, id):
        """删除风险策略

        删除风险策略

        Attributes:
            id (str): 
        """
        return self.http_client.request(
            method='DELETE',
            url='/api/v3/risk-list-policy/{id}',
        )

    def create_device(self, device_unique_id, type, custom_data, name=None, version=None, hks=None, fde=None, hor=None,
                      sn=None, producer=None, mod=None, os=None, imei=None, meid=None, description=None, language=None,
                      cookie=None, user_agent=None):
        """新增设备

        创建新设备。

        Attributes:
            device_unique_id (str): 设备唯一标识
            type (str): 设备类型
            custom_data (dict): 自定义数据, 自定义数据的属性对应在元数据里自定义的字段
            name (str): 设备名称
            version (str): 系统版本
            hks (str): 硬件存储秘钥
            fde (str): 磁盘加密
            hor (bool): 硬件越狱
            sn (str): 设备序列号
            producer (str): 制造商
            mod (str): 设备模组
            os (str): 设备系统
            imei (str): 国际识别码
            meid (str): 设备识别码
            description (str): 设备描述
            language (str): 设备语言
            cookie (bool): 是否开启 Cookies
            user_agent (str): 用户代理
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-device',
            json={
                'deviceUniqueId': device_unique_id,
                'type': type,
                'customData': custom_data,
                'name': name,
                'version': version,
                'hks': hks,
                'fde': fde,
                'hor': hor,
                'sn': sn,
                'producer': producer,
                'mod': mod,
                'os': os,
                'imei': imei,
                'meid': meid,
                'description': description,
                'language': language,
                'cookie': cookie,
                'userAgent': user_agent,
            },
        )

    def find_last_login_apps_by_device_ids(self, device_ids, user_id=None):
        """最近登录应用

        根据设备唯一标识获取最近登录的应用列表。

        Attributes:
            device_ids (list): 设备唯一标识列表
            user_id (str): 用户 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-last-login-apps-by-deviceIds',
            json={
                'deviceIds': device_ids,
                'userId': user_id,
            },
        )

    def create_verify_device(self, device_unique_id, type, custom_data, name=None, version=None, hks=None, fde=None,
                             hor=None, sn=None, producer=None, mod=None, os=None, imei=None, meid=None,
                             description=None, language=None, cookie=None, user_agent=None):
        """新增 verify 设备

        创建 verify 新设备。

        Attributes:
            device_unique_id (str): 设备唯一标识
            type (str): 设备类型
            custom_data (dict): 自定义数据, 自定义数据的属性对应在元数据里自定义的字段
            name (str): 设备名称
            version (str): 系统版本
            hks (str): 硬件存储秘钥
            fde (str): 磁盘加密
            hor (bool): 硬件越狱
            sn (str): 设备序列号
            producer (str): 制造商
            mod (str): 设备模组
            os (str): 设备系统
            imei (str): 国际识别码
            meid (str): 设备识别码
            description (str): 设备描述
            language (str): 设备语言
            cookie (bool): 是否开启 Cookies
            user_agent (str): 用户代理
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/authing-verify/create-device',
            json={
                'deviceUniqueId': device_unique_id,
                'type': type,
                'customData': custom_data,
                'name': name,
                'version': version,
                'hks': hks,
                'fde': fde,
                'hor': hor,
                'sn': sn,
                'producer': producer,
                'mod': mod,
                'os': os,
                'imei': imei,
                'meid': meid,
                'description': description,
                'language': language,
                'cookie': cookie,
                'userAgent': user_agent,
            },
        )

    def create_pipeline_function(self, source_code, scene, func_name, func_description=None, is_asynchronous=None,
                                 timeout=None, terminate_on_timeout=None, enabled=None):
        """创建 Pipeline 函数

        创建 Pipeline 函数

        Attributes:
            source_code (str): 函数源代码
            scene (str): 函数的触发场景：
- `PRE_REGISTER`: 注册前
- `POST_REGISTER`: 注册后
- `PRE_AUTHENTICATION`: 认证前
- `POST_AUTHENTICATION`: 认证后
- `PRE_OIDC_ID_TOKEN_ISSUED`: OIDC ID Token 签发前
- `PRE_OIDC_ACCESS_TOKEN_ISSUED`: OIDC Access Token 签发前
- `PRE_COMPLETE_USER_INFO`: 补全用户信息前
    
            func_name (str): 函数名称
            func_description (str): 函数描述
            is_asynchronous (bool): 是否异步执行。设置为异步执行的函数不会阻塞整个流程的执行，适用于异步通知的场景，比如飞书群通知、钉钉群通知等。
            timeout (int): 函数运行超时时间，要求必须为整数，最短为 1 秒，最长为 60 秒，默认为 3 秒。
            terminate_on_timeout (bool): 如果函数运行超时，是否终止整个流程，默认为否。
            enabled (bool): 是否启用此 Pipeline
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-pipeline-function',
            json={
                'sourceCode': source_code,
                'scene': scene,
                'funcName': func_name,
                'funcDescription': func_description,
                'isAsynchronous': is_asynchronous,
                'timeout': timeout,
                'terminateOnTimeout': terminate_on_timeout,
                'enabled': enabled,
            },
        )

    def get_pipeline_function(self, func_id):
        """获取 Pipeline 函数详情

        获取 Pipeline 函数详情

        Attributes:
            funcId (str): Pipeline 函数 ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-pipeline-function',
            params={
                'funcId': func_id,
            },
        )

    def reupload_pipeline_function(self, func_id):
        """重新上传 Pipeline 函数

        当 Pipeline 函数上传失败时，重新上传 Pipeline 函数

        Attributes:
            func_id (str): Pipeline 函数 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/reupload-pipeline-function',
            json={
                'funcId': func_id,
            },
        )

    def update_pipeline_function(self, func_id, func_name=None, func_description=None, source_code=None,
                                 is_asynchronous=None, timeout=None, terminate_on_timeout=None, enabled=None):
        """修改 Pipeline 函数

        修改 Pipeline 函数

        Attributes:
            func_id (str): Pipeline 函数 ID
            func_name (str): 函数名称
            func_description (str): 函数描述
            source_code (str): 函数源代码。如果修改之后，函数会重新上传。
            is_asynchronous (bool): 是否异步执行。设置为异步执行的函数不会阻塞整个流程的执行，适用于异步通知的场景，比如飞书群通知、钉钉群通知等。
            timeout (int): 函数运行超时时间，最短为 1 秒，最长为 60 秒，默认为 3 秒。
            terminate_on_timeout (bool): 如果函数运行超时，是否终止整个流程，默认为否。
            enabled (bool): 是否启用此 Pipeline
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-pipeline-function',
            json={
                'funcId': func_id,
                'funcName': func_name,
                'funcDescription': func_description,
                'sourceCode': source_code,
                'isAsynchronous': is_asynchronous,
                'timeout': timeout,
                'terminateOnTimeout': terminate_on_timeout,
                'enabled': enabled,
            },
        )

    def update_pipeline_order(self, order, scene):
        """修改 Pipeline 函数顺序

        修改 Pipeline 函数顺序

        Attributes:
            order (list): 新的排序方式，按照函数 ID 的先后顺序进行排列。
            scene (str): 函数的触发场景：
- `PRE_REGISTER`: 注册前
- `POST_REGISTER`: 注册后
- `PRE_AUTHENTICATION`: 认证前
- `POST_AUTHENTICATION`: 认证后
- `PRE_OIDC_ID_TOKEN_ISSUED`: OIDC ID Token 签发前
- `PRE_OIDC_ACCESS_TOKEN_ISSUED`: OIDC Access Token 签发前
- `PRE_COMPLETE_USER_INFO`: 补全用户信息前
    
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-pipeline-order',
            json={
                'order': order,
                'scene': scene,
            },
        )

    def delete_pipeline_function(self, func_id):
        """删除 Pipeline 函数

        删除 Pipeline 函数

        Attributes:
            func_id (str): Pipeline 函数 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-pipeline-function',
            json={
                'funcId': func_id,
            },
        )

    def list_pipeline_functions(self, scene):
        """获取 Pipeline 函数列表

        获取 Pipeline 函数列表

        Attributes:
            scene (str): 通过函数的触发场景进行筛选（可选，默认返回所有）：
- `PRE_REGISTER`: 注册前
- `POST_REGISTER`: 注册后
- `PRE_AUTHENTICATION`: 认证前
- `POST_AUTHENTICATION`: 认证后
- `PRE_OIDC_ID_TOKEN_ISSUED`: OIDC ID Token 签发前
- `PRE_OIDC_ACCESS_TOKEN_ISSUED`: OIDC Access Token 签发前
- `PRE_COMPLETE_USER_INFO`: 补全用户信息前
    
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-pipeline-functions',
            params={
                'scene': scene,
            },
        )

    def get_pipeline_logs(self, func_id, page=None, limit=None):
        """获取 Pipeline 日志

        获取 Pipeline 

        Attributes:
            funcId (str): Pipeline 函数 ID
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-pipeline-logs',
            params={
                'funcId': func_id,
                'page': page,
                'limit': limit,
            },
        )

    def create_webhook(self, content_type, events, url, name, enabled=None, secret=None):
        """创建 Webhook

        你需要指定 Webhook 名称、Webhook 回调地址、请求数据格式、用户真实名称来创建 Webhook。还可选是否启用、请求密钥进行创建

        Attributes:
            content_type (str): 请求数据格式
            events (list): 用户真实名称，不具备唯一性。 示例值: 张三
            url (str): Webhook 回调地址
            name (str): Webhook 名称
            enabled (bool): 是否启用
            secret (str): 请求密钥
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-webhook',
            json={
                'contentType': content_type,
                'events': events,
                'url': url,
                'name': name,
                'enabled': enabled,
                'secret': secret,
            },
        )

    def list_webhooks(self, page=None, limit=None):
        """获取 Webhook 列表

        获取 Webhook 列表，可选页数、分页大小来获取

        Attributes:
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-webhooks',
            params={
                'page': page,
                'limit': limit,
            },
        )

    def update_webhook(self, webhook_id, name=None, url=None, events=None, content_type=None, enabled=None,
                       secret=None):
        """修改 Webhook 配置

        需要指定 webhookId，可选 Webhook 名称、Webhook 回调地址、请求数据格式、用户真实名称、是否启用、请求密钥参数进行修改 webhook

        Attributes:
            webhook_id (str): Webhook ID
            name (str): Webhook 名称
            url (str): Webhook 回调地址
            events (list): 用户真实名称，不具备唯一性。 示例值: 张三
            content_type (str): 请求数据格式
            enabled (bool): 是否启用
            secret (str): 请求密钥
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-webhook',
            json={
                'webhookId': webhook_id,
                'name': name,
                'url': url,
                'events': events,
                'contentType': content_type,
                'enabled': enabled,
                'secret': secret,
            },
        )

    def delete_webhook(self, webhook_ids):
        """删除 Webhook

        通过指定多个 webhookId,以数组的形式进行 webhook 的删除,如果 webhookId 不存在,不提示报错

        Attributes:
            webhook_ids (list): webhookId 数组
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-webhook',
            json={
                'webhookIds': webhook_ids,
            },
        )

    def get_webhook_logs(self, webhook_id, page=None, limit=None):
        """获取 Webhook 日志

        通过指定 webhookId，可选 page 和 limit 来获取 webhook 日志,如果 webhookId 不存在,不返回报错信息

        Attributes:
            webhook_id (str): Webhook ID
            page (int): 当前页数，从 1 开始
            limit (int): 每页数目，最大不能超过 50，默认为 10
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/get-webhook-logs',
            json={
                'webhookId': webhook_id,
                'page': page,
                'limit': limit,
            },
        )

    def trigger_webhook(self, webhook_id, request_headers=None, request_body=None):
        """手动触发 Webhook 执行

        通过指定 webhookId，可选请求头和请求体进行手动触发 webhook 执行

        Attributes:
            webhook_id (str): Webhook ID
            request_headers (dict): 请求头
            request_body (dict): 请求体
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/trigger-webhook',
            json={
                'webhookId': webhook_id,
                'requestHeaders': request_headers,
                'requestBody': request_body,
            },
        )

    def get_webhook(self, webhook_id):
        """获取 Webhook 详情

        根据指定的 webhookId 获取 webhook 详情

        Attributes:
            webhookId (str): Webhook ID
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-webhook',
            params={
                'webhookId': webhook_id,
            },
        )

    def get_webhook_event_list(self, ):
        """获取 Webhook 事件列表

        返回事件列表和分类列表

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-webhook-event-list',
        )

    def get_bind_pwd(self, ):
        """生成 LDAP Server 管理员密码

        生成 LDAP Server 管理员密码

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-ldap-server-random-pwd',
        )

    def query_ldap_config_info(self, ):
        """获取 LDAP server 配置信息

        获取 LDAP server 配置信息

        Attributes:
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-ldap-server-config',
        )

    def update_ldap_config_info(self, bind_pwd=None):
        """更新 LDAP server 配置信息

        更新 LDAP server 配置信息

        Attributes:
            bind_pwd (str): bindDn 密码
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-ldap-server-config',
            json={
                'bindPwd': bind_pwd,
            },
        )

    def save_ldap_config_info(self, ldap_domain, link_url=None):
        """初始化/重启 LDAP server

        初始化/重启 LDAP server

        Attributes:
            ldap_domain (str): LDAP 域名
            link_url (str): LDAP host
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/enable-ldap-server',
            json={
                'ldapDomain': ldap_domain,
                'linkUrl': link_url,
            },
        )

    def disable_ldap_server(self, enabled):
        """关闭 LDAP server 服务，关闭前必须先初始化

        关闭 LDAP server 服务，关闭前必须先初始化

        Attributes:
            enabled (bool): 开关是否开启
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/disable-ldap-server',
            json={
                'enabled': enabled,
            },
        )

    def query_ldap_log(self, type, page, limit, connection=None, operation_number=None, error_code=None, message=None,
                       start_time=None, end_time=None):
        """LDAP server 日志查询

        LDAP server 日志查询

        Attributes:
            type (int): 类型：1 访问日志，2 错误日志
            page (int): 当前页,从 1 开始
            limit (int): 每页条数
            connection (int): 连接标识
            operationNumber (int): 操作码
            errorCode (int): 错误码
            message (str): 消息内容
            startTime (int): 开始时间-时间戳
            endTime (int): 结束时间-时间戳
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-ldap-server-log',
            params={
                'type': type,
                'connection': connection,
                'operationNumber': operation_number,
                'errorCode': error_code,
                'message': message,
                'startTime': start_time,
                'endTime': end_time,
                'page': page,
                'limit': limit,
            },
        )

    def query_ldap_sub_entries(self, page, limit, dn=None):
        """LDAP server 根据 DN 查询下一级

        LDAP server 根据 DN 查询下一级

        Attributes:
            page (int): 当前页,从 1 开始
            limit (int): 每页条数
            dn (str): 当前 DN
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-ldap-sub-entries',
            params={
                'dn': dn,
                'page': page,
                'limit': limit,
            },
        )

    def get_access_key_list(self, user_id=None, tenant_id=None, type=None, status=None):
        """获取协作管理员 AK/SK 列表

        根据协作管理员 Id 获取协作管理员下所有的 AK/SK 列表

        Attributes:
            userId (str): 密钥所属用户 ID
            tenantId (str): 密钥所属租户 ID
            type (str): 密钥类型
            status (str): AccessKey 状态，activated：已激活，staging：分级（可轮换），revoked：已撤销
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/list-access-key',
            params={
                'userId': user_id,
                'tenantId': tenant_id,
                'type': type,
                'status': status,
            },
        )

    def get_access_key(self, user_id, access_key_id):
        """获取协作管理员 AK/SK 详细信息

        获取协作管理员 AK/SK 详细信息,根据协作管理员 ID 和 accessKeyId 获取对应 AK/SK 的详细信息。

        Attributes:
            userId (str): 用户 ID
            accessKeyId (str): accessKeyId
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/get-access-key',
            params={
                'userId': user_id,
                'accessKeyId': access_key_id,
            },
        )

    def create_access_key(self, type, user_id=None, tenant_id=None):
        """创建协作管理员的 AK/SK

        创建协作管理员的 AK/SK,根据协作管理员 ID 生成指定的 AK/SK。

        Attributes:
            type (str): 密钥类型
            user_id (str): 密钥所属用户 ID
            tenant_id (str): 密钥所属租户 ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/create-access-key',
            json={
                'type': type,
                'userId': user_id,
                'tenantId': tenant_id,
            },
        )

    def delete_access_key(self, access_key_id):
        """删除协作管理员的 AK/SK

        删除协作管理员的 AK/SK,根据所选择的 AK/SK 的 accessKeyId 进行指定删除。

        Attributes:
            access_key_id (str): accessKeyId
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/delete-access-key',
            json={
                'accessKeyId': access_key_id,
            },
        )

    def update_access_key(self, enable, access_key_id):
        """更新一个管理员 AccessKey

        根据 AccessKeyId 更新一个管理员 AccessKey，目前只支持更新 status，status 支持 activated / revoked

        Attributes:
            enable (bool): 密钥是否生效
            access_key_id (str): AccessKey ID
        """
        return self.http_client.request(
            method='POST',
            url='/api/v3/update-access-key',
            json={
                'enable': enable,
                'accessKeyId': access_key_id,
            },
        )

    def get_verify_config_app(self, keywords=None):
        """获取 verify-config-app 列表

        获取 verify-config-app 列表

        Attributes:
            keywords (str): 搜索关键字
        """
        return self.http_client.request(
            method='GET',
            url='/api/v3/verify-config-app',
            params={
                'keywords': keywords,
            },
        )

    def sub_event(self, event_code, callback):
        """订阅事件

        订阅 authing 公共事件或自定义事件

        Attributes:
            eventCode (str): 事件编码
            callback (callable): 回调函数
        """
        assert event_code, "eventCode 不能为空"
        assert callable(callback), "callback 必须为可执行函数"
        authorization = getAuthorization(self.access_key_id, self.access_key_secret)
        # print("authorization:"+authorization)
        eventUri = self.websocket_host + self.websocket_endpoint + "?code=" + event_code
        # print("eventUri:"+eventUri)
        handleMessage(eventUri, callback, authorization)

    def put_event(self, event_code, data):
        """发布自定义事件

        发布事件

        Attributes:
            event_code (str): 事件编码
            data (json): 事件体
        """
        return self.http_client.request(
            method="POST",
            url="/api/v3/pub-event",
            json={
                "eventType": event_code,
                "eventData": json.dumps(data)
            },
        )
