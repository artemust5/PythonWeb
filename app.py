from flask_bcrypt import Bcrypt,check_password_hash
import bcrypt
from flask import Flask, json, jsonify, request, make_response, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, validate, validates, ValidationError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
# from midels import User
from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.functions import user
from flask_jwt import current_identity

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:root@127.0.0.1/pythonbd'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = '1234'

jwt = JWTManager(app)

db = SQLAlchemy(app)

def get_by_username(username):

    # try:
    user = db.session.query(User).filter_by(username=username).first()
    # except:
    #     return 1
    return user

# def get_by_id(id):
#     user = User.query.filter_by(id=id).first()
#     return user

# def get_by_id_st(id):
#
#     st = Student.query.filter_by(id=id).first()
#
#     return st


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    firstName = db.Column(db.String(100), nullable=True)
    lastName = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return self.name

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_username(cls, username):
        return cls.query.get_or_404(username)

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class UserSchema(Schema):
    id = fields.Integer()
    firstName = fields.String(validate=validate.Length(max=15))
    lastName = fields.String(validate=validate.Length(max=15))
    phone = fields.String(validate=validate.Length(max=15))
    email = fields.Email()
    password = fields.String(validate=validate.Length(max=100))
    username = fields.String(validate=validate.Length(max=15))

    # @validates('phone')
    # def validate_age(self, phone):
    #     if phone > 10:
    #         raise ValidationError('The phone is too long!')

    # @validates('email')
    # def validate_age(self, email):
    #     if email == email:
    #         raise ValidationError('Tis email is exist')

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()

    new_user = User(
        username=data.get('username'),
        firstName=data.get('firstName'),
        lastName=data.get('lastName'),
        phone = data.get('phone'),
        email = data.get('email'),
        password = data.get('password'),

    )

    # User["password"] = Bcrypt(app).generate_password_hash(User["password"], rounds=4).decode('UTF-8')

    new_user.save()

    serializer = UserSchema()

    data = serializer.dump(new_user)

    return jsonify(
        data
    ), 200

@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.get_all()

    serializer = UserSchema(many=True)

    data = serializer.dump(users)

    return jsonify(
        data
    )

@app.route('/user/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):

    current_identity_username = get_jwt_identity()
    user = User.get_by_id(id)

    if current_identity_username != user.username:
        return jsonify('Access is denided')

    serializer = UserSchema()

    data = serializer.dump(user)

    return jsonify(
        data
    ), 200

@app.route('/user/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):

    current_identity_username = get_jwt_identity()
    user_to_update = User.get_by_id(id)

    if current_identity_username != user_to_update.username:
        raise ValidationError('Tis email is exist')

    data = request.get_json()

    user_to_update.firstName = data.get('firstName')
    user_to_update.lastName = data.get('lastName')
    user_to_update.phone = data.get('phone')
    user_to_update.email = data.get('email')

    db.session.commit()

    serializer = UserSchema()

    recipe_data = serializer.dump(user_to_update)

    return jsonify(recipe_data), 200

@app.route('/user/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    current_identity_username = get_jwt_identity()
    user_to_delete = User.get_by_id(id)

    if current_identity_username != user_to_delete.username:
        return jsonify('Access is denided')

    user_to_delete.delete()

    return jsonify({"message": "Deleted"}), 204

@app.errorhandler(404)
def not_found(error):
    return jsonify({"message": "User not found"}), 404

@app.errorhandler(500)
def internal_server(error):
    return jsonify({"message": "There is a problem"}), 500

class Student(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    avarageMark = db.Column(db.Integer(), nullable=False)
    User_id = db.Column(db.Integer(), db.ForeignKey(User.id), nullable=False)

    def __repr__(self):
        return self.name

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class StudentSchema(Schema):
    id = fields.Integer()
    name = fields.String(validate=validate.Length(max=15))
    lastName = fields.String(validate=validate.Length(max=15))
    avarageMark = fields.Integer()
    User_id = fields.Integer()

@app.route('/student', methods=['POST'])
@jwt_required()
def create_student():
    cur_ide = get_jwt_identity()

    cur_use = get_by_username(cur_ide)

    # if cur_use == 1:
    #     return jsonify('invalid user')

    data = request.get_json()

    new_student = Student(
        # id=data.get('id'),
        name=data.get('name'),
        lastName=data.get('lastName'),
        avarageMark=data.get('avarageMark'),
        User_id=data.get('User_id')
    )

    # if cur_use.id != new_student.User_id:
    #     return jsonify('Access is denided') , 400

    new_student.save()

    serializer = StudentSchema()



    data = serializer.dump(new_student)

    return jsonify(
        data
    ), 200

@app.route('/student/<int:id>', methods=['GET'])
def get_student(id):

    student = Student.get_by_id(id)


    serializer = StudentSchema()

    data = serializer.dump(student)

    return jsonify(
        data
    ), 200

@app.route('/student/<int:id>', methods=['PUT'])
@jwt_required()
def update_student(id):
    current_identity_username = get_jwt_identity()
    student_to_update = Student.get_by_id(id)

    cur_use = get_by_username(current_identity_username)

    if cur_use.id != student_to_update.User_id:
        return jsonify('Access is denided')

    data = request.get_json()

    student_to_update.name = data.get('name'),
    student_to_update.lastName = data.get('lastName'),
    student_to_update.avarageMark = data.get('avarageMark'),

    db.session.commit()

    serializer = StudentSchema()

    recipe_data = serializer.dump(student_to_update)

    return jsonify(recipe_data), 200

@app.route('/student/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_student(id):
    current_identity_username = get_jwt_identity()
    student_to_delete = Student.get_by_id(id)

    cur_ide = get_by_username(current_identity_username)

    if cur_ide.id != student_to_delete.User_id:
        return jsonify('Access is denided'),401

    student_to_delete.delete()

    return jsonify({"message": "Deleted"}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({"message": "Student not found"}), 404

@app.errorhandler(500)
def internal_server(error):
    return jsonify({"message": "There is a problem"}), 500



@app.route('/login', methods=['GET','POST'])
def login():

    auth = request.authorization


    if not auth or not auth.username or not auth.password:
        return make_response('could', 401)

    # access_token = create_access_token(identity=auth.username)
    # return jsonify({'token ': access_token})
    #user = session.query(User).filter_by(username=auth.username).first()
    user = get_by_username(auth.username)
    # user =
    # user_obj = user.query.filter_by(username=auth.username).first()

    if (user.password == auth.password):
        token1 = create_access_token(identity=user.username)
        return jsonify(token1)


    return make_response('not',401)




# @app.route('/logout')
# def logout():
#     session.pop('username',None)
#     return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)