import jwt
import datetime
from flask import request, jsonify, current_app, g
from functools import wraps

SECRET_KEY = 'supersecretkey'  # Troque para um segredo seguro em produção

def generate_token(username, role):
    payload = {
        'username': username,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    # Compatibilidade: PyJWT 2.x retorna str, 1.x retorna bytes
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split(' ')[1]
            if not token:
                return jsonify({'error': 'Token ausente'}), 401
            data = decode_token(token)
            if not data:
                return jsonify({'error': 'Token inválido ou expirado'}), 401
            if role and data['role'] != role:
                return jsonify({'error': 'Permissão negada'}), 403
            g.user = data
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Usuários de exemplo (em produção, use banco de dados)
USERS = {
    'admin': {'password': 'admin123', 'role': 'admin'},
    'user': {'password': 'user123', 'role': 'user'}
}

def register_auth_routes(app):
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        user = USERS.get(username)
        if user and user['password'] == password:
            token = generate_token(username, user['role'])
            return jsonify({'token': token})
        return jsonify({'error': 'Credenciais inválidas'}), 401

    @app.route('/me', methods=['GET'])
    @login_required()
    def me():
        return jsonify({'user': g.user})
