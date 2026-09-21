from database import db
from flask import Flask
from routes.api import api_bp
from routes.main import main_bp
from routes.public import public_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///builder.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "custom-form-builder-secret-key"

db.init_app(app)

# Register Modular Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(api_bp)
app.register_blueprint(public_bp)

with app.app_context():
  db.create_all()

if __name__ == "__main__":
  app.run(debug=True, port=5000)