import jwt
import datetime
from functools import wraps
from flask import request
from config import Config

# Clave secreta para firmar los tokens JWT
SECRET_KEY = Config.SECRET_KEY

def generate_token(user):
    token = jwt.encode({
        'id': user.id,
        'name': user.name,
        'lastname': user.lastname,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, SECRET_KEY)
    return token

def validate_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {'message': 'Token missing'}, 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return {'message': 'Token expired'}, 401
        except jwt.InvalidTokenError:
            return {'message': 'Invalid token'}, 401
        return func(*args, **kwargs)
    return wrapper