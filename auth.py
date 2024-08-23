from functools import wraps
from flask import request, jsonify

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({"message": "Token is missing or invalid"}), 401
        token = token.split(' ')[1]  # Extract token from "Bearer <token>"

        # Validate the token (for demonstration, we use a hardcoded token)
        if token != "your_secret_token":  # Replace with your actual token validation logic
            return jsonify({"message": "Token is invalid"}), 403

        return f(*args, **kwargs)
    return decorator
