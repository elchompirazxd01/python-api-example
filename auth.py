from flask import request

def require_auth(func):
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            response = "Invalid Token"
            return 401
        
        parts = auth_header.split()
        if len(parts) != 2 or parts[0] != 'Bearer':
            response = "Invalid Token"
            return 401
        
        token = parts[1]
        if not is_valid_token(token):
            response = "Invalid Token"
            return response, 401
        
        # Call the original function
        return func(*args, **kwargs)
    
    return decorated_function

def is_valid_token(token):
    # Implement your token validation logic here
    valid_tokens = ["your_valid_token_here"]  # Replace with your actual token validation
    return token in valid_tokens
