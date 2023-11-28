from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
import os
import boto3
import hashlib
from botocore.exceptions import ClientError

app = Flask(__name__)
api = Api(app)

# Initialize AWS Secrets Manager client
secrets_manager = boto3.client('secretsmanager', region_name='us-east-1')

# Fetch the authentication token from Secrets Manager
def get_auth_token():
    try:
        response = secrets_manager.get_secret_value(SecretId='arn:aws:secretsmanager:us-east-1:737256812804:secret:my_flask_api-SDezXM')
        secret_data = response['SecretString']
        return secret_data.get("AUTH_TOKEN")
    except Exception as e:
        print(f"Error retrieving authentication token from Secrets Manager: {e}")
        return None

# Fetch the authentication token on application startup
AUTH_TOKEN = get_auth_token()

# Set the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://your_username:your_password@your_host:your_port/your_database_name')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

def authenticate_request():
    auth_token = request.headers.get("AUTH_TOKEN")
    if auth_token != AUTH_TOKEN:
        return False
    return True

# Example API endpoint using Flask-RESTful
class UserResource(Resource):
    def post(self):
        if not authenticate_request():
            return jsonify({"error": "Unauthorized"}), 401

        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({"error": "Username already exists"}), 400

        # Create a new user
        new_user = User(username=username, password=hashlib.sha1((username + password).encode()).hexdigest())
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User created successfully", "user_id": new_user.user_id}), 201
      
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            return jsonify({"user_id": user.user_id, "username": user.username})
        return jsonify({"error": "User not found"}), 404

    def put(self, user_id):
        if not authenticate_request():
            return jsonify({"error": "Unauthorized"}), 401

        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        user = User.query.get(user_id)
        if user:
            user.username = username
            user.password = hashlib.sha1((username + password).encode()).hexdigest()
            db.session.commit()
            return jsonify({"message": f"User with ID {user_id} updated successfully"})
        return jsonify({"error": "User not found"}), 404

    def delete(self, user_id):
        if not authenticate_request():
            return jsonify({"error": "Unauthorized"}), 401

        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": f"User with ID {user_id} deleted successfully"})
        return jsonify({"error": "User not found"}), 404

api.add_resource(UserResource, '/v1/user/<int:user_id>')

if __name__ == '__main__':
    # Apply database migrations
    with app.app_context():
        db.create_all()

    app.run(debug=False, host='0.0.0.0')
