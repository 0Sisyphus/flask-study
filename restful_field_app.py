import json
import random
from datetime import datetime

from flask import Flask
from flask_restful import Resource, fields, marshal_with, marshal, Api

resource_fields = {
    'name': fields.String,
    'address': fields.String,
    'date_updated': fields.DateTime(dt_format='rfc822')
}


# 使用marshal_with配置返回数据信息
class FieldGet(Resource):
    @marshal_with(resource_fields, envelope='resource')
    def get(self, **kwargs):
        return db_get_todo()


# 和上述装饰器等价
class FieldGet2(Resource):
    def get(self, **kwargs):
        return marshal(db_get_todo(), resource_fields), 200


# 重命名属性
fields_rename = {
    'username': fields.String(attribute='name'),
    'address': fields.String,
}

# 处理上述取值方式，还可以有如下取值方式
fields_rename2 = {
    'username': fields.String(attribute=lambda x: x._private_name),
    'address': fields.String,
}

fields_rename3 = {
    'username': fields.String(attribute='people_list.0.person_dictionary.name'),
    'address': fields.String,
}


class Rename(Resource):
    @marshal_with(fields_rename, envelope='data')
    def get(self, **kwargs):
        return db_get_todo()


# 设置默认值
fields_default = {
    'name': fields.String(default='Anonymous User'),
    'address': fields.String,
}


class Default(Resource):
    @marshal_with(fields_default, envelope='data')
    def get(self, **kwargs):
        return {
            'address': 'hangzhou'
        }


# 自定义转换
class UrgentItem(fields.Raw):
    def format(self, value):
        return "Urgent" if value & 0x01 else "Normal"


class UnreadItem(fields.Raw):
    def format(self, value):
        return "Unread" if value & 0x02 else "Read"


format_fields = {
    'name': fields.String,
    'priority': UrgentItem(attribute='flags'),
    'status': UnreadItem(attribute='flags'),
}


class Format(Resource):
    @marshal_with(format_fields, envelope='data')
    def get(self, **kwargs):
        return {
            'name': "lee",
            "flags": 0x01
        }


# 获取url
class RandomNumber(fields.Raw):
    def output(self, key, obj):
        return random.random()


url_fields = {
    'name': fields.String,
    # todo_resource is the endpoint name when you called api.add_resource()
    'uri': fields.Url('urlGet'),
    'random': RandomNumber,
}


class URLGet(Resource):
    @marshal_with(url_fields, envelope='data')
    def get(self, **kwargs):
        return {
            'name': "lee",
        }


app = Flask(__name__)
api = Api(app)

api.add_resource(FieldGet, '/field/get')
api.add_resource(FieldGet2, '/field/get2')
api.add_resource(Rename, '/field/rename')
api.add_resource(Default, '/field/default')
api.add_resource(Format, '/field/format')
api.add_resource(URLGet, '/field/url/get', endpoint='urlGet')


def db_get_todo():
    return {
        'name': 'lee',
        'age': 18,
        'address': 'hangzhou',
        'date_updated': datetime.now()
    }




if __name__ == '__main__':
    app.run(debug=True)
