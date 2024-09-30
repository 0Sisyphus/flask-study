import os

from flask import Flask, request, send_from_directory
from flask_restful import Api, Resource
from werkzeug.utils import secure_filename

app = Flask(__name__)
api = Api(app)

# 设置上传文件的保存目录
UPLOAD_FOLDER = 'upload_dir'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 确保上传目录存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 文件上传
class FileUpload(Resource):
    def post(self):
        # 检查请求中是否包含文件
        if 'file' not in request.files:
            return {'message': 'No file part'}, 400

        file = request.files['file']

        # 如果用户没有选择文件，浏览器也会提交一个空的部分
        if file.filename == '':
            return {'message': 'No selected file'}, 400

        # 保存文件
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        file.save(file_path)

        return {'message': 'File uploaded successfully', 'filename': file.filename}, 201

# 文件下载
class FileDownload(Resource):
    def get(self, filename):
        try:
            # 从上传目录发送文件
            return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
        except FileNotFoundError:
            return {'message': 'File not found'}, 404


api.add_resource(FileUpload, '/upload')
api.add_resource(FileDownload, '/download/<string:filename>')


if __name__ == '__main__':
    app.run(debug=True)
