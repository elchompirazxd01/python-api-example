from functools import wraps
from flask import request, jsonify

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"message": "Missing Authorization Header"}), 401
        
        parts = auth_header.split()
        if len(parts) != 2 or parts[0] != 'Bearer':
            return jsonify({"message": "Invalid Authorization Header Format"}), 401
        
        token = parts[1]
        if not is_valid_token(token):
            return jsonify({"message": "Invalid Token"}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function

def is_valid_token(token):
    # Implement your token validation logic here
    valid_tokens = ["your_valid_token_here"]  # Replace with your actual token validation
    return token in valid_tokens
