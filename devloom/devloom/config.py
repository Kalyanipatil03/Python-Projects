import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'devloom-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///devloom.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False