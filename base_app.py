import os

from flask import Flask, render_template, redirect, url_for, request, make_response, session
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route("/hello/<name>")
def hello(name):
    return "Hello %s !" % name


@app.route('/blog/<int:postID>')
def show_blog(postID):
    return 'Blog Number % d' % postID


@app.route('/rev/<float:revNo>')
def revision(revNo):
    return 'Revision Number % d' % revNo


# 有效访问：http://127.0.0.1:5000/flask
# 无效访问：http://127.0.0.1:5000/flask/
@app.route('/flask')
def hello_flask():
    return 'Hello flask'


# 有效访问：http://127.0.0.1:5000/python、http://127.0.0.1:5000/python/
@app.route('/python/')
def hello_python():
    return 'Revision python'


# 模版
@app.route('/temp/index')
def temp_index():
    return render_template('index.html')


@app.route('/temp/index2')
def temp_index2():
    age = 15
    name = 'lee'
    t_list = [1, 5, 6, 4, 3]
    t_dict = {
        'name': 'durant',
        'age': 18
    }
    return render_template('index2.html',
                           age=age,
                           name=name,
                           my_list=t_list,
                           my_dict=t_dict)


# 重定向
@app.route('/url/ret')
def url_ret():
    return redirect(url_for("temp_index2"))


# form表单
@app.route('/result', methods=["POST"])
def result():
    rst = request.form
    return render_template("result.html", result=rst)


"""
设置cookies
"""


@app.route("/set_cookies")
def set_cookie():
    resp = make_response('success')
    resp.set_cookie("aaa_key", "aaa_value", max_age=3600)
    return resp


@app.route("/get_cookies")
def get_cookie():
    cookies_get = request.cookies.get("aaa_key")
    print(cookies_get)
    if cookies_get == None:
        return make_response("Not found")
    return cookies_get


@app.route("/del_cookies")
def del_cookies():
    response = make_response("del success")
    response.delete_cookie("aaa_key")
    return response


"""
设置session
"""
app.secret_key = '123456'


@app.route("/index")
def index():
    if 'username' in session:
        user = session['username']
        return "登录用户名是：" + user + '<br>' + "<br><a href = '/logout'>点击这里注销</a><br>"
    return "您暂未登录, <br><a href = '/login'>点击这里登录</a><br>"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('login.html')


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


"""
文件上传
"""
app.config['UPLOAD_FOLDER'] = 'upload_dir/'


@app.route("/upload/index")
def upload_index():
    return render_template('upload.html')


@app.route("/uploader", methods=['GET', 'POST'])
def uploader():
    if request.method == "POST":
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        return 'file upload success'
    if request.method == "GET":
        return render_template('upload.html')


if __name__ == '__main__ ':
    app.run(host='127.0.0.1', debug=True)
