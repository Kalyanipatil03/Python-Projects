# routes/admin.py
from database import db
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from models import Movie, User

admin_bp = Blueprint('admin', __name__)


def admin_required(fn):
  def wrapper(*args, **kwargs):
    if not session.get('is_admin'):
      flash('Admin access required.')
      return redirect(url_for('catalog.home'))
    return fn(*args, **kwargs)

  wrapper.__name__ = fn.__name__
  return wrapper


@admin_bp.route('/admin')
@admin_required
def dashboard():
  users = User.query.all()
  movies = Movie.query.order_by(Movie.id.desc()).all()
  return render_template('admin.html', users=users, movies=movies)


@admin_bp.route('/admin/movie/add', methods=['POST'])
@admin_required
def add_movie():
  new_movie = Movie(
      title=request.form.get('title'),
      description=request.form.get('description'),
      genre=request.form.get('genre'),
      year=int(request.form.get('year', 2026)),
      rating=float(request.form.get('rating', 8.0)),
      duration=request.form.get('duration'),
      poster=request.form.get('poster'),
      banner=request.form.get('banner'),
      video_url=request.form.get('video_url'),
  )
  db.session.add(new_movie)
  db.session.commit()
  flash('Movie added successfully!')
  return redirect(url_for('admin.dashboard'))


@admin_bp.route('/admin/movie/delete/<int:movie_id>', methods=['POST'])
@admin_required
def delete_movie(movie_id):
  movie = Movie.query.get_or_404(movie_id)
  db.session.delete(movie)
  db.session.commit()
  flash('Movie removed.')
  return redirect(url_for('admin.dashboard'))