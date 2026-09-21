import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import markdown as md
from slugify import slugify

from config import Config
from models import db, User, Post, Comment, Tag, likes, bookmarks

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Custom Jinja Filters
    @app.template_filter('markdown')
    def render_markdown(text):
        if not text:
            return ""
        return md.markdown(text, extensions=['fenced_code', 'tables', 'nl2br'])

    @app.template_filter('timeago')
    def timeago(date):
        if not date:
            return ""
        now = datetime.datetime.utcnow()
        diff = now - date
        seconds = diff.total_seconds()
        
        if seconds < 60:
            return "just now"
        elif seconds < 3600:
            return f"{int(seconds // 60)}m ago"
        elif seconds < 86400:
            return f"{int(seconds // 3600)}h ago"
        elif seconds < 604800:
            return f"{int(seconds // 86400)}d ago"
        else:
            return date.strftime("%b %d, %Y")

    # -------------------------------------------------------------------------
    # ROUTES
    # -------------------------------------------------------------------------

    # 1. Home / Index Page
    @app.route('/')
    def index():
        featured_posts = Post.query.order_by(Post.views.desc()).limit(3).all()
        recent_posts = Post.query.order_by(Post.created_at.desc()).limit(6).all()
        return render_template('index.html', featured_posts=featured_posts, recent_posts=recent_posts)

    # 2. Explore Posts (with search & filtering)
    @app.route('/explore')
    def explore():
        page = request.args.get('page', 1, type=int)
        post_type = request.args.get('type', '')
        query = request.args.get('q', '')

        post_query = Post.query

        if post_type:
            post_query = post_query.filter_by(post_type=post_type)

        if query:
            search_pattern = f"%{query}%"
            search_posts = post_query.filter(
                (Post.title.ilike(search_pattern)) | 
                (Post.summary.ilike(search_pattern)) |
                (Post.content.ilike(search_pattern))
            ).order_by(Post.created_at.desc()).all()
            return render_template('explore.html', search_posts=search_posts, query=query, active_type=post_type)

        pagination = post_query.order_by(Post.created_at.desc()).paginate(page=page, per_page=9, error_out=False)
        return render_template('explore.html', pagination=pagination, query=query, active_type=post_type)

    # 3. View Post Detail
    @app.route('/post/<slug>')
    def post_detail(slug):
        post = Post.query.filter_by(slug=slug).first_or_404()
        post.views += 1
        db.session.commit()
        return render_template('post_detail.html', post=post)

    # 4. Create Post
    @app.route('/post/create', methods=['GET', 'POST'])
    @login_required
    def create_post():
        if request.method == 'POST':
            title = request.form.get('title')
            post_type = request.form.get('post_type')
            code_language = request.form.get('code_language')
            summary = request.form.get('summary')
            content = request.form.get('content')
            tags_input = request.form.get('tags', '')

            base_slug = slugify(title)
            slug = base_slug
            count = 1
            while Post.query.filter_by(slug=slug).first():
                slug = f"{base_slug}-{count}"
                count += 1

            new_post = Post(
                title=title,
                slug=slug,
                post_type=post_type,
                code_language=code_language,
                summary=summary,
                content=content,
                author_id=current_user.id
            )

            if tags_input:
                tag_names = [t.strip().lower() for t in tags_input.split(',') if t.strip()]
                for name in tag_names:
                    tag = Tag.query.filter_by(name=name).first()
                    if not tag:
                        tag = Tag(name=name)
                        db.session.add(tag)
                    new_post.tags.append(tag)

            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('post_detail', slug=new_post.slug))

        return render_template('create_post.html')

    # 5. Add Comment
    @app.route('/post/<int:post_id>/comment', methods=['POST'])
    @login_required
    def add_comment(post_id):
        post = Post.query.get_or_404(post_id)
        content = request.form.get('content')
        if content:
            comment = Comment(content=content, post_id=post.id, author_id=current_user.id)
            db.session.add(comment)
            db.session.commit()
        return redirect(url_for('post_detail', slug=post.slug))

    # 6. AJAX Like Post
    @app.route('/post/<int:post_id>/like', methods=['POST'])
    @login_required
    def toggle_like(post_id):
        post = Post.query.get_or_404(post_id)
        if current_user in post.likers:
            post.likers.remove(current_user)
            liked = False
        else:
            post.likers.append(current_user)
            liked = True
        db.session.commit()
        return jsonify({'liked': liked, 'likes_count': post.likers.count()})

    # 7. AJAX Bookmark Post
    @app.route('/post/<int:post_id>/bookmark', methods=['POST'])
    @login_required
    def toggle_bookmark(post_id):
        post = Post.query.get_or_404(post_id)
        if current_user in post.savers:
            post.savers.remove(current_user)
            saved = False
        else:
            post.savers.append(current_user)
            saved = True
        db.session.commit()
        return jsonify({'saved': saved})

    # 8. User Profile
    @app.route('/u/<username>')
    def profile(username):
        user = User.query.filter_by(username=username).first_or_404()
        posts = Post.query.filter_by(author_id=user.id).order_by(Post.created_at.desc()).all()
        return render_template('profile.html', profile_user=user, posts=posts)

    # 9. Personal Library / Saved Posts
    @app.route('/library')
    @login_required
    def library():
        posts = current_user.saved_posts.order_by(Post.created_at.desc()).all()
        return render_template('library.html', posts=posts)

    # 10. Settings
    @app.route('/settings', methods=['GET', 'POST'])
    @login_required
    def settings():
        if request.method == 'POST':
            current_user.display_name = request.form.get('display_name')
            current_user.headline = request.form.get('headline')
            current_user.bio = request.form.get('bio')
            current_user.github_url = request.form.get('github_url')
            current_user.website_url = request.form.get('website_url')
            db.session.commit()
            flash("Profile updated successfully!")
            return redirect(url_for('settings'))
        return render_template('settings.html')

    # 11. Auth Routes (Login, Register, Logout)
    @app.route('/auth/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for('index'))
            flash("Invalid email or password.")
        return render_template('auth/login.html')

    @app.route('/auth/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form.get('username')
            display_name = request.form.get('display_name')
            email = request.form.get('email')
            password = request.form.get('password')

            if User.query.filter((User.username == username) | (User.email == email)).first():
                flash("Username or email already exists.")
                return redirect(url_for('register'))

            user = User(username=username, display_name=display_name, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('index'))
        return render_template('auth/register.html')

    @app.route('/auth/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    # 12. Admin Dashboard
    @app.route('/admin/dashboard')
    @login_required
    def admin_dashboard():
        if not current_user.is_admin:
            return redirect(url_for('index'))
        stats = {
            'users': User.query.count(),
            'posts': Post.query.count(),
            'comments': Comment.query.count()
        }
        posts = Post.query.order_by(Post.created_at.desc()).all()
        return render_template('admin/dashboard.html', stats=stats, posts=posts)

    @app.route('/admin/post/delete/<int:post_id>', methods=['POST'])
    @login_required
    def delete_post(post_id):
        if not current_user.is_admin:
            return redirect(url_for('index'))
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('admin_dashboard'))

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)