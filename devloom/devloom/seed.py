from app import create_app
from models import db, User, Post, Tag

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Create Admin & Regular User
    admin = User(
        username='admin',
        display_name='Admin User',
        email='admin@devloom.io',
        headline='Lead Architect @ DevLoom',
        bio='Building open-source software and scaling web apps.',
        is_admin=True
    )
    admin.set_password('admin123')

    user = User(
        username='alexdev',
        display_name='Alex Rivera',
        email='alex@devloom.io',
        headline='Full Stack Developer',
        bio='Passionate about Python, JavaScript, and system design.'
    )
    user.set_password('password123')

    db.session.add_all([admin, user])
    db.session.commit()

    # Create Initial Tags
    python_tag = Tag(name='python')
    flask_tag = Tag(name='flask')
    db_tag = Tag(name='database')
    db.session.add_all([python_tag, flask_tag, db_tag])
    db.session.commit()

    # Create Sample Posts
    post1_content = "# Building Modular Applications\n\nModular software architecture splits code into smaller, independent components.\n\n```python\nfrom flask import Flask\n\ndef create_app():\n    app = Flask(__name__)\n    return app\n```\n\n### Key Benefits\n- Clear separation of concerns\n- Easier maintenance and testing\n- Scalable database migrations"

    post1 = Post(
        title='Building Modular Web Applications with Flask',
        slug='building-modular-web-applications-with-flask',
        post_type='Tutorial',
        code_language='python',
        summary='Learn how to structure scalable web applications using Flask blueprints, factory functions, and SQLAlchemy ORM.',
        content=post1_content,
        author_id=admin.id
    )
    post1.tags.extend([python_tag, flask_tag])

    post2_content = "# OS Directory Script\n\nCreate directory trees safely in Python:\n\n```python\nimport os\n\npath = \"devloom/routes\"\nos.makedirs(path, exist_ok=True)\nprint(os.listdir(\"devloom\"))\n```"

    post2 = Post(
        title='Quick Python Directory Traversal & Management',
        slug='quick-python-directory-traversal-management',
        post_type='Snippet',
        code_language='python',
        summary='Handy snippet using the built-in os module to create and manage directory trees programmatically.',
        content=post2_content,
        author_id=user.id
    )
    post2.tags.extend([python_tag, db_tag])

    db.session.add_all([post1, post2])
    db.session.commit()

    print("Database seeded successfully!")