# 自定义字段和输入
from flask import Flask
from flask_restful import marshal_with, reqparse, Resource, Api


# odd number
def odd_number(value):
    if value % 2 == 0:
        raise ValueError('{} is not an odd number'.format(value))
    return value

# 将外部参数转换为内部表示
def task_status(value):
    if value not in  ["init", "in-progress", "completed"]:
        raise ValueError('{} is not a valid status'.format(value))
    statuses = ["init", "in-progress", "completed"]
    return statuses.index(value)


class CustomField(Resource):
    def post(self, **kwargs):
        parser = reqparse.RequestParser()
        parser.add_argument('OddNumber', type=odd_number, required=True, location='json')
        parser.add_argument('Status', type=task_status, required=True, location='json')
        args = parser.parse_args()
        return {
            'OddNumber': args.OddNumber,
            'Status': args.Status,
        }

app = Flask(__name__)
api = Api(app)
api.add_resource(CustomField, '/custom_field')

if __name__ == '__main__':
    app.run(debug=True)

# todo 学习 文件上传、下载，导出等

