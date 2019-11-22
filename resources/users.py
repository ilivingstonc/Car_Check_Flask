import models

from flask import Blueprint, jsonify, request ## import the request object
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from playhouse.shortcuts import model_to_dict

user = Blueprint('users', 'user')

@user.route('/register', methods=['POST'])
def register():
    """ Accepts a post request with new user's email and password """
    payload = request.get_json()

    if not payload['email'] or not payload['password']:
        return jsonify(status=400)

    try: 

        models.User.get(models.User.email ** payload['email']) 
        return jsonify(data={}, status={'code': 400, 'message': 'A user with that email already exists.'})
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password'])
        user = models.User.create(**payload)

        login_user(user)

        user_dict = model_to_dict(user)
        print(user_dict)
        print(type(user_dict))

        del user_dict['password']  

        return jsonify(data=user_dict, status={'code': 201, 'message': 'User created'}) 

@user.route('/login', methods=['POST'])
def login():
    """ Route to authenticate user by comparent pw hash from database
        to the hashed password attempt send from client/user
        Requires: Email, password
    """
    payload = request.get_json()

    try: 
        user = models.User.get(models.User.email ** payload['email'])
        user_dict = model_to_dict(user)
        
        if(check_password_hash(user_dict['password'], payload['password'])):
            del user_dict['password']
            login_user(user)
            print('User is:' , user)
            return jsonify(data=user_dict, status={'code': 200, 'message': 'User authenticated'})

        return jsonify(data=user_dict, status={'code': 401, 'message': 'Email or Password is Incorrect'})
    except models.DoesNotExist:
        
        return jsonify(data=user_dict, status={'code': 401, 'message': 'Email or Password is Incorrect'})