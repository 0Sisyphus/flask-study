from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 配置数据库 URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:yinuo_dev@10.0.0.214:3306/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db = SQLAlchemy(app)


# 定义模型
class Employees(db.Model):
    __tablename__ = "employees"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), unique=False, nullable=False)
    last_name = db.Column(db.String(50), unique=False, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    department = db.Column(db.String(50), unique=False, nullable=False)
    status = db.Column(db.String(10), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


# 添加用户的路由
@app.route('/add_employee', methods=['POST'])
def add_user():
    data = request.get_json()
    new_employee = Employees(first_name=data['firstName']
                             , last_name=data['lastName']
                             , age=data['age']
                             , department=data['department']
                             , status=data['status'])
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'message': 'Employee added successfully!'}), 201


# 获取所有用户的路由
@app.route('/employees', methods=['GET'])
def get_users():
    employees = Employees.query.all()
    return jsonify([{'id': employee.id, 'firstName': employee.first_name, 'lastName': employee.last_name,
                     'age': employee.age, 'department': employee.department, 'status': employee.status} for employee in
                    employees])


if __name__ == '__main__':
    app.run(debug=True)
