from flask import Flask
from flask_cors import CORS
from auth_routes import auth_bp

app = Flask(__name__)

# Configure CORS
CORS(app)

# Register the auth blueprint
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
