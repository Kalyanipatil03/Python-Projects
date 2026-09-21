import os
import re
import secrets
import markdown
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy import or_, func

from config import Config
from models import db, User, Article, Tag, Comment, ReadingHistory

app = Flask(__name__)
app.config.from_object(Config)

os.makedirs(os.path.join(app.root_path, "instance"), exist_ok=True)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Utility Helpers
def generate_slug(text):
    clean = re.sub(r"[^a-zA-Z0-9\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "-", clean) or secrets.token_hex(4)

def parse_tags(tag_string):
    tag_objs = []
    for raw in (tag_string or "").split(","):
        clean_name = raw.strip().lstrip("#")[:40]
        if not clean_name:
            continue
        slug = generate_slug(clean_name)
        tag = Tag.query.filter_by(slug=slug).first()
        if not tag:
            tag = Tag(name=clean_name, slug=slug)
            db.session.add(tag)
        tag_objs.append(tag)
    return tag_objs[:5]

@app.template_filter("markdown")
def render_markdown(text):
    return markdown.markdown(text or "", extensions=["fenced_code", "tables"])

@app.template_filter("timeago")
def timeago(dt):
    if not dt:
        return ""
    delta = int((datetime.utcnow() - dt).total_seconds())
    if delta < 60:
        return "just now"
    if delta < 3600:
        return f"{delta // 60}m ago"
    if delta < 86400:
        return f"{delta // 3600}h ago"
    return dt.strftime("%b %d, %Y")

# ---------- Routes ----------

@app.route("/")
def index():
    featured = Article.query.filter_by(is_published=True).order_by(Article.views.desc()).first()
    articles = Article.query.filter_by(is_published=True).order_by(Article.created_at.desc()).limit(10).all()
    trending = Article.query.filter_by(is_published=True).order_by(Article.views.desc()).limit(5).all()
    tags = Tag.query.order_by(func.random()).limit(8).all()
    return render_template("home.html", featured=featured, articles=articles, trending=trending, tags=tags)

@app.route("/explore")
def explore():
    page = request.args.get("page", 1, type=int)
    pagination = Article.query.filter_by(is_published=True).order_by(Article.created_at.desc()).paginate(page=page, per_page=9, error_out=False)
    return render_template("explore.html", pagination=pagination, query=None, search_articles=[])

@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    articles = []
    if query:
        pattern = f"%{query}%"
        articles = Article.query.filter_by(is_published=True).filter(
            or_(Article.title.ilike(pattern), Article.summary.ilike(pattern), Article.content.ilike(pattern))
        ).order_by(Article.created_at.desc()).all()
    return render_template("explore.html", pagination=None, search_articles=articles, query=query)

@app.route("/post/<slug>")
def article_detail(slug):
    article = Article.query.filter_by(slug=slug, is_published=True).first_or_404()
    article.views += 1
    if current_user.is_authenticated:
        history = ReadingHistory.query.filter_by(user_id=current_user.id, article_id=article.id).first()
        if history:
            history.viewed_at = datetime.utcnow()
        else:
            db.session.add(ReadingHistory(user_id=current_user.id, article_id=article.id))
    db.session.commit()
    return render_template("article.html", article=article)

@app.route("/user/<username>")
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    user_articles = Article.query.filter_by(author_id=user.id, is_published=True).order_by(Article.created_at.desc()).all()
    return render_template("profile.html", profile_user=user, articles=user_articles)

@app.route("/auth/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=True)
            return redirect(url_for("index"))
        flash("Invalid email or password.", "error")
    return render_template("auth/login.html")

@app.route("/auth/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        display_name = request.form.get("display_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        
        if User.query.filter(or_(User.email == email, User.username == username)).first():
            flash("Username or Email already registered.", "error")
        else:
            new_user = User(username=username, display_name=display_name, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("index"))
    return render_template("auth/register.html")

@app.route("/auth/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/write", methods=["GET", "POST"])
@login_required
def write():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        summary = request.form.get("summary", "").strip()
        cover_image = request.form.get("cover_image", "").strip()
        is_published = request.form.get("is_published") == "true"
        
        slug = generate_slug(title)
        article = Article(
            title=title,
            slug=slug,
            content=content,
            summary=summary,
            cover_image=cover_image,
            is_published=is_published,
            author_id=current_user.id
        )
        article.tags = parse_tags(request.form.get("tags", ""))
        db.session.add(article)
        db.session.commit()
        return redirect(url_for("article_detail", slug=article.slug) if is_published else url_for("dashboard"))
    return render_template("editor.html")

@app.route("/dashboard")
@login_required
def dashboard():
    user_articles = Article.query.filter_by(author_id=current_user.id).order_by(Article.created_at.desc()).all()
    return render_template("dashboard.html", articles=user_articles)

@app.route("/post/<int:article_id>/like", methods=["POST"])
@login_required
def toggle_like(article_id):
    article = Article.query.get_or_404(article_id)
    if current_user in article.likers:
        article.likers.remove(current_user)
        liked = False
    else:
        article.likers.append(current_user)
        liked = True
    db.session.commit()
    return jsonify({"liked": liked, "likes_count": article.likers.count()})

@app.route("/admin")
@login_required
def admin():
    if not current_user.is_admin:
        abort(403)
    stats = {
        "users": User.query.count(),
        "articles": Article.query.count(),
        "published": Article.query.filter_by(is_published=True).count(),
    }
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    return render_template("admin/dashboard.html", stats=stats, users=recent_users)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)