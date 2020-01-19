import ssl
import sys, traceback

from bson import ObjectId
from flask import request
from response import response
from db import mongo_config
from passlib.apps import custom_app_context as pwd_context
# required create_access_token and decode_token for JWT token
from flask_jwt_extended import create_access_token, decode_token


def sign_up():
    '''created this function to get data for register user'''
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        # Legacy Python that doesn't verify HTTPS certificates by default
        pass
    else:
        # Handle target environment that doesn't support HTTPS verification
        ssl._create_default_https_context = _create_unverified_https_context
    if request.method == 'POST':
        error = []
        payload_data = request.json
        username = payload_data.get('username', '')
        password = payload_data.get('password', '')
        email_id = payload_data.get('emailId', '')
        if len(username) == 0:
            username_error = {
                'error': 'username required',
                'value': 'empty'
            } 
            error.append(username_error)
        if len(password) == 0:
            password_error = {
                'error': 'password required',
                'value': 'empty'
            }
            error.append(password_error)
        if len(email_id) == 0:
            email_error = {
                'error': 'emailId required',
                'value': 'empty'
            }
            error.append(email_error)
        if len(error) == 0:
            try:
                connection_db = mongo_config.db_connection()
                users_db = connection_db['users']
                query = {"username": {"$eq": username}, "email_id": {"$eq": email_id}}
                user_exist = list(users_db.find(query))
                if len(user_exist) == 0:
                    register_user = {"username": username, "email_id": email_id, "password": pwd_context.hash(password)}
                    users_db.insert(register_user)
                    return response.return_response('', "user registered successfully.", 200)
                else:
                    return response.return_response('Error occured.', "user already exists.", 200)
            except Exception as err:
                print('Error occurred in sign_up function, Error Details : - ' + str(
                    traceback.format_exception(*sys.exc_info())), flush=True)
                return response.return_response("Error occured", err, 200)
        else:
            return response.return_response("Error occured", "Please provide details.", 200, data=error)
    elif request.method == 'GET':
        return response.return_response("Error occured", "Only POST request allowed", 200)


def login():
    '''created this function to get data for register user'''
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        # Legacy Python that doesn't verify HTTPS certificates by default
        pass
    else:
        # Handle target environment that doesn't support HTTPS verification
        ssl._create_default_https_context = _create_unverified_https_context
    if request.method == 'POST':
        error = []
        payload_data = request.json
        username = payload_data.get('username', '')
        password = payload_data.get('password', '')
        if len(username) == 0:
            username_error = {
                'error': 'username required',
                'value': 'empty'
            }
            error.append(username_error)
        if len(password) == 0:
            password_error = {
                'error': 'password required',
                'value': 'empty'
            }
            error.append(password_error)

        if len(error) == 0:
            try:
                connection_db = mongo_config.db_connection()
                users_db = connection_db['users']
                query = {"username": {"$eq": username}}
                user_exist = list(users_db.find(query))
                if len(user_exist) != 0:
                    login_pass = pwd_context.verify(password, user_exist[0]['password'])
                    if login_pass:
                        tok_value = str(user_exist[0]['_id']) # using mongo id for JWT identity, to identify distinct required once required using Token 
                        result = [{
                            'token': create_access_token(identity=tok_value)
                        }]
                        return response.return_response('', "user login successfully.", 200, data=result)
                    else:
                        return response.return_response('', "password not matching.", 200)
                else:
                    return response.return_response('Error occured.', "user not registered.", 200)
            except Exception as err:
                print('Error occurred in login function, Error Details : - ' + str(
                    traceback.format_exception(*sys.exc_info())), flush=True)
                return response.return_response("Error occured", err, 200)
        else:
            return response.return_response("Error occured", "Please provide details.", 200, data=error)
    elif request.method == 'GET':
        return response.return_response("Error occured", "Only POST request allowed", 200)


def profile():
    '''created this function to get data for register user'''
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        # Legacy Python that doesn't verify HTTPS certificates by default
        pass
    else:
        # Handle target environment that doesn't support HTTPS verification
        ssl._create_default_https_context = _create_unverified_https_context
    if request.method == 'GET':
        try:
            # if token is authorized, your control will be here.
            # you can read authorization from header
            token_value = request.headers.get('Authorization', '')
            # replace for decoding
            token_value = token_value.replace('Bearer ', '')
            # use predefined function to decode the authorization and get the identity which we set while creating token in login section.
            identity = decode_token(token_value)['identity']
            if len(identity) != 0:
                connection_db = mongo_config.db_connection()
                users_db = connection_db['users']
                query = {'_id': ObjectId(identity)}
                user_exist = list(users_db.find(query))
                if len(user_exist) != 0:
                    result = user_exist[0]
                    del result['password']
                    return response.return_response('', "user profile data.", 200, data=[result])
                else:
                    return response.return_response('Error occured.', "user not found.", 200)
            else:
                return response.return_response('Error occured.', "Please provide token to access the API.", 200)
        except Exception as err:
            print('Error occurred in profile function, Error Details : - ' + str(
                traceback.format_exception(*sys.exc_info())), flush=True)
            return response.return_response("Error occured", err, 200)
    elif request.method == 'GET':
        return response.return_response("Error occured", "Only POST request allowed", 200)


def validate_user(username, password):
    try:
        connection_db = mongo_config.db_connection()
        users_db = connection_db['users']
        if len(username) != 0:
            query = {"username": username}
        user_exist = users_db.find(query)
        for x in user_exist:
            if pwd_context.verify(password, x['password']):
                return True
        return False
    except:
        return False