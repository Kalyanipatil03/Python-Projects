# routes/auth.py
from database import db
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')

    if not username or not email or len(password) < 6:
      flash('Please fill all fields. Password must be at least 6 characters.')
      return render_template('register.html')

    if User.query.filter((User.username == username) | (User.email == email)).first():
      flash('Username or email already exists.')
      return render_template('register.html')

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    flash('Account created successfully! Please log in.')
    return redirect(url_for('auth.login'))

  return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    identifier = request.form.get('identifier', '').strip()
    password = request.form.get('password', '')

    user = User.query.filter(
        (User.username == identifier) | (User.email == identifier)
    ).first()

    if user and user.check_password(password):
      session['user_id'] = user.id
      session['username'] = user.username
      session['is_admin'] = user.is_admin
      return redirect(url_for('catalog.home'))

    flash('Invalid credentials.')

  return render_template('login.html')


@auth_bp.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('auth.login'))