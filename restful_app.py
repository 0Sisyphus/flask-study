from flask import Flask, request, url_for, redirect
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


# 资源可以绑定多个url
# 可以设置端点名称 endpoint
api.add_resource(HelloWorld, '/', '/hello', endpoint='index')


# 其他资源使用端点名称访问路径
class HelloRedirect(Resource):
    def get(self):
        # 重定向
        return redirect(url_for('index'))

api.add_resource(HelloRedirect, '/redirect')

todos = {}


class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        # Default to 200 OK
        # return {todo_id: todos[todo_id]}
        # Set the response code to 201 and return custom headers
        return {todo_id: todos[todo_id]}, 201, {'Etag': 'some-opaque-string'}


# http://localhost:5000/todo1 -d "data=Remember the milk"
api.add_resource(TodoSimple, '/<string:todo_id>')


if __name__ == '__main__':
    app.run(debug=True)
