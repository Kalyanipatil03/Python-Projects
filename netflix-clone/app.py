# app.py
from database import db
from flask import Flask
from routes.admin import admin_bp
from routes.auth import auth_bp
from routes.catalog import catalog_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'streamflix-modern-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///netflix.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(catalog_bp)
app.register_blueprint(admin_bp)

if __name__ == '__main__':
  with app.app_context():
    db.create_all()
  app.run(debug=True, port=5000)