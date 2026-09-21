# routes/catalog.py
from database import db
from flask import Blueprint, jsonify, render_template, request, session
from models import History, Movie, User

catalog_bp = Blueprint('catalog', __name__)


@catalog_bp.route('/')
def home():
  movies = Movie.query.order_by(Movie.id.desc()).all()

  # Fetch unique genres for filtering
  genres_query = db.session.query(Movie.genre).distinct().all()
  genres = [g[0] for g in genres_query if g[0]]

  featured = movies[0] if movies else None

  watchlist_ids = []
  if session.get('user_id'):
    user = User.query.get(session['user_id'])
    watchlist_ids = [m.id for m in user.watchlist]

  return render_template(
      'index.html',
      movies=movies,
      genres=genres,
      featured=featured,
      watchlist_ids=watchlist_ids,
  )


@catalog_bp.route('/watchlist')
def watchlist():
  if 'user_id' not in session:
    return render_template('login.html')

  user = User.query.get(session['user_id'])
  user_movies = user.watchlist
  watchlist_ids = [m.id for m in user_movies]

  return render_template(
      'watchlist.html', movies=user_movies, watchlist_ids=watchlist_ids
  )


@catalog_bp.route('/history')
def history():
  if 'user_id' not in session:
    return render_template('login.html')

  history_items = (
      History.query.filter_by(user_id=session['user_id'])
      .order_by(History.watched_at.desc())
      .all()
  )

  return render_template('history.html', history_items=history_items)


@catalog_bp.route('/watch/<int:movie_id>')
def watch(movie_id):
  if 'user_id' not in session:
    return render_template('login.html')

  movie = Movie.query.get_or_404(movie_id)

  history_item = History.query.filter_by(
      user_id=session['user_id'], movie_id=movie_id
  ).first()
  if not history_item:
    history_item = History(user_id=session['user_id'], movie_id=movie_id)
    db.session.add(history_item)
  else:
    db.session.merge(history_item)

  db.session.commit()
  return render_template('watch.html', movie=movie)


@catalog_bp.route('/toggle-watchlist/<int:movie_id>', methods=['POST'])
def toggle_watchlist(movie_id):
  if 'user_id' not in session:
    return jsonify({'error': 'Unauthorized'}), 401

  user = User.query.get(session['user_id'])
  movie = Movie.query.get_or_404(movie_id)

  if movie in user.watchlist:
    user.watchlist.remove(movie)
    added = False
  else:
    user.watchlist.append(movie)
    added = True

  db.session.commit()
  return jsonify({'success': True, 'added': added})