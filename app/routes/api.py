from flask import request, jsonify
from app import app
from app.controllers.user_controller import UserController
from app.models.user import User

user_controller = UserController()

@app.route('/auth', methods=['POST'])
def login():
    data = request.get_json()
    nick = data.get('nick')
    password = data.get('password')
    return jsonify(user_controller.login(nick, password))

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    lastname = data.get('lastname')
    rol = data.get('rol')
    nick = data.get('nick')
    password = data.get('password')
    user = User('', name, lastname, rol, nick, password)
    return jsonify(user_controller.register(user))

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(user_controller.get_users_controller())

@app.route('/update-user', methods=['PUT'])
def update_user():
    data = request.get_json()
    id_user = data.get('id')
    name = data.get('name')
    lastname = data.get('lastname')
    rol = data.get('rol')
    nick = data.get('nick')
    user = User(id_user, name, lastname, rol, nick, '')
    return jsonify(user_controller.update_user_controller(user))

@app.route('/update-passw', methods=['PUT'])
def update_passw():
    data = request.get_json()
    id_user = data.get('id')
    current_passw = data.get('current_passw')
    new_passw = data.get('new_passw')
    return jsonify(user_controller.update_password_user(id_user,current_passw, new_passw))

@app.route('/change-passw', methods=['PUT'])
def change_passw():
    data = request.get_json()
    id_user = data.get('id')
    new_passw = data.get('new_passw')
    return jsonify(user_controller.update_passw_with_admin(id_user, new_passw))

@app.route('/delete-user', methods=['DELETE'])
def delete_user():
    data = request.get_json()
    id_user = data.get('id')
    return jsonify(user_controller.delete_user(id_user))