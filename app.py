from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint
from auth import require_auth
app = Flask(__name__)
api = Api(app)

# Define Swagger UI setup
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'  # URL to the Swagger JSON file

swagger_ui = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "My API"}  # Swagger UI configuration
)
app.register_blueprint(swagger_ui, url_prefix=SWAGGER_URL)

# Serve Swagger JSON
@app.route('/static/swagger.json')
def swagger_spec():
    spec = {
        "swagger": "2.0",
        "info": {
            "title": "My API",
            "version": "1.0.0",
            "description": "API documentation"
        },
        "securityDefinitions": {
            "BearerAuth": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Enter your Bearer token in the format **Bearer {token}**"
            }
        },
        "security": [
            {"BearerAuth": []}
        ],
        "paths": {
            "/uppercase": {
                "get": {
                    "tags": ["Text Processing"],
                    "parameters": [
                        {
                            "name": "text",
                            "in": "query",
                            "type": "string",
                            "required": True,
                            "description": "The text to be converted to uppercase"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "A successful GET request test",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "text": {
                                        "type": "string",
                                        "description": "The text in uppercase"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    return jsonify(spec)

class UppercaseText(Resource):
    @require_auth
    def get(self):
        """
        This method responds to the GET request for this endpoint and returns the data in uppercase.
        ---
        tags:
        - Text Processing
        parameters:
            - name: text
              in: query
              type: string
              required: true
              description: The text to be converted to uppercase
        responses:
            200:
                description: A successful GET request
                content:
                    application/json:
                      schema:
                        type: object
                        properties:
                            text:
                                type: string
                                description: The text in uppercase
            401:
                description: Unauthorized, missing or invalid token
            403:
                description: Forbidden, invalid token
        """
        text = request.args.get('text')
        if text is None:
            return jsonify({"message": "Missing text query parameter"}), 400
        return jsonify({"text": text.upper()})

api.add_resource(UppercaseText, "/uppercase")

if __name__ == "__main__":
    app.run(debug=True)
