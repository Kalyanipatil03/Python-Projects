# models.py
from datetime import datetime
from database import db
from werkzeug.security import check_password_hash, generate_password_hash

# Junction Tables for Many-to-Many Relationships
watchlist = db.Table(
    'watchlist',
    db.Column(
        'user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE')
    ),
    db.Column(
        'movie_id', db.Integer, db.ForeignKey('movies.id', ondelete='CASCADE')
    ),
)


class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password_hash = db.Column(db.String(256), nullable=False)
  is_admin = db.Column(db.Boolean, default=False)

  watchlist = db.relationship('Movie', secondary=watchlist, backref='saved_by')

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)


class Movie(db.Model):
  __tablename__ = 'movies'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(150), nullable=False)
  description = db.Column(db.Text, nullable=False)
  genre = db.Column(db.String(50), nullable=False)
  year = db.Column(db.Integer, nullable=False)
  rating = db.Column(db.Float, default=0.0)
  duration = db.Column(db.String(20), nullable=False)
  poster = db.Column(db.String(300), nullable=False)
  banner = db.Column(db.String(300), nullable=False)
  video_url = db.Column(db.String(300), nullable=False)


class History(db.Model):
  __tablename__ = 'history'
  user_id = db.Column(
      db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True
  )
  movie_id = db.Column(
      db.Integer,
      db.ForeignKey('movies.id', ondelete='CASCADE'),
      primary_key=True,
  )
  watched_at = db.Column(
      db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
  )

  movie = db.relationship('Movie')