import werkzeug
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

parser = reqparse.RequestParser()
parser.add_argument("age", type=int, required=True)
parser.add_argument("name", type=str, help="name cannot be null", required=True)

# 指定help信息，在解析类型错误时返回
# 在解析时，required=True 表示必须有该参数，否则报错
# 在默认的情况下，required=False 表示可以没有该参数，没有该参数时，返回None

# 如果你想接受一个键的多个值作为列表，你可以通过 action='append'
parser.add_argument("like", type=str, help="str cannot be converted", action='append')
# 如果你想接受一个键的多个值作为字典，你可以通过 action='append_list'

# 如果你想在解析后将其放在不同的位置，你可以通过 dest 参数
parser.add_argument("other_like", type=str, help="other_like cannot be converted", required=True, dest='otherLike')

# 参数位置
# Look only in the POST body
parser.add_argument('queryName', type=str, location='form')

# Look only in the querystring
parser.add_argument('PageSize', type=int, location='args')

# From the request headers
parser.add_argument('User-Agent', location='headers')

# From http cookies
parser.add_argument('session_id', location='cookies')

# From file uploads
parser.add_argument('picture', type=werkzeug.datastructures.FileStorage, location='files')

# 多个位置
parser.add_argument('text', location=['form', 'json', 'cookies'])
# 如果参数位置列表包含headers 位置，则参数名称将不再不区分大小写，并且必须与其标题大小写名称相匹配（请参阅str.title()）。
# 指定 location='headers'（不是列表）将保留不区分大小写。

# 解析器的继承
parser.add_argument('foo', type=int)
parser_copy = parser.copy()
# 新增
parser_copy.add_argument("other_name", type=str, help="other_name cannot be converted", required=True)
# 替换
parser_copy.replace_argument('foo', required=True, location='json')
# 删除
parser_copy.remove_argument('foo')

# 参数错误时，默认返回第一个报错，如果想将所有报错一同返回
parser_copy = reqparse.RequestParser(bundle_errors=True)

# 应用程序配置键是“BUNDLE_ERRORS”， RequestParser实例中的选项会被覆盖。例如
app_bundle = Flask(__name__)
app_bundle.config['BUNDLE_ERRORS'] = True

app = Flask(__name__)
api = Api(app)


class ArgParse(Resource):
    def post(self):
        args = parser.parse_args()
        return args


api.add_resource(ArgParse, '/arg')

if __name__ == '__main__':
    app.run(debug=True)
