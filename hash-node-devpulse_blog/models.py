from datetime import datetime
import re
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# Association Tables
followers = db.Table(
    "followers",
    db.Column("follower_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("following_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)

article_tags = db.Table(
    "article_tags",
    db.Column("article_id", db.Integer, db.ForeignKey("article.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
)

likes = db.Table(
    "likes",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("article_id", db.Integer, db.ForeignKey("article.id"), primary_key=True),
)

bookmarks = db.Table(
    "bookmarks",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("article_id", db.Integer, db.ForeignKey("article.id"), primary_key=True),
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text, default="")
    website = db.Column(db.String(255), default="")
    github = db.Column(db.String(255), default="")
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    articles = db.relationship("Article", backref="author", lazy=True, cascade="all, delete-orphan")
    comments = db.relationship("Comment", backref="author", lazy=True, cascade="all, delete-orphan")
    history = db.relationship("ReadingHistory", backref="user", lazy=True, cascade="all, delete-orphan")

    following = db.relationship(
        "User",
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.following_id == id),
        backref=db.backref("followers", lazy="dynamic"),
        lazy="dynamic",
    )
    liked_articles = db.relationship("Article", secondary=likes, back_populates="likers", lazy="dynamic")
    saved_articles = db.relationship("Article", secondary=bookmarks, back_populates="savers", lazy="dynamic")

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(60), unique=True, nullable=False)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(220), nullable=False)
    slug = db.Column(db.String(240), unique=True, nullable=False)
    summary = db.Column(db.Text, default="")
    content = db.Column(db.Text, nullable=False)
    cover_image = db.Column(db.String(500), default="")
    is_published = db.Column(db.Boolean, default=True)
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    tags = db.relationship("Tag", secondary=article_tags, backref=db.backref("articles", lazy="dynamic"))
    likers = db.relationship("User", secondary=likes, back_populates="liked_articles", lazy="dynamic")
    savers = db.relationship("User", secondary=bookmarks, back_populates="saved_articles", lazy="dynamic")
    comments = db.relationship("Comment", backref="article", lazy=True, cascade="all, delete-orphan")

    @property
    def reading_time(self):
        words = len(re.findall(r"\b\w+\b", self.content or ""))
        return max(1, round(words / 200))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    article_id = db.Column(db.Integer, db.ForeignKey("article.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class ReadingHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    viewed_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey("article.id"), nullable=False)
    article = db.relationship("Article")