from app import app
from models import db, User, Article, Tag

def seed_data():
    with app.app_context():
        db.create_all()
        if User.query.first():
            print("Database already seeded.")
            return

        # Create Admin and Demo User
        admin = User(
            username="admin", 
            display_name="DevPulse Admin", 
            email="admin@devpulse.local", 
            is_admin=True
        )
        admin.set_password("AdminPass123!")

        demo_user = User(
            username="alex", 
            display_name="Alex Rivera", 
            email="alex@devpulse.local", 
            bio="Full Stack Engineer passionate about Python, Flask and modern web architectures."
        )
        demo_user.set_password("DemoPass123!")

        db.session.add_all([admin, demo_user])
        db.session.flush()

        # Seed Tags
        t_python = Tag(name="Python", slug="python")
        t_flask = Tag(name="Flask", slug="flask")
        t_web = Tag(name="WebDev", slug="webdev")

        db.session.add_all([t_python, t_flask, t_web])
        db.session.flush()

        # Properly formatted markdown content string
        markdown_content = (
            "# Scaling Flask Applications\n\n"
            "Flask is minimal by design, making it ideal for both lightweight applications and scalable products.\n\n"
            "## Modular Blueprints\n\n"
            "Breaking your code into distinct domains (authentication, catalog, admin) maintains clean boundaries.\n\n"
            "```python\n"
            "from flask import Blueprint\n\n"
            "auth_bp = Blueprint('auth', __name__)\n"
            "```\n\n"
            "## ORM Persistence\n\n"
            "Always separate business logic from domain models for cleaner testability and maintenance."
        )

        # Seed Articles
        art1 = Article(
            title="Building Scalable Web Applications with Flask Blueprint Pattern",
            slug="building-scalable-web-applications-with-flask-blueprint-pattern",
            summary="Learn how to structure enterprise-ready Flask applications with modular blueprints and database ORM design.",
            content=markdown_content,
            author_id=demo_user.id,
            is_published=True,
            views=340
        )
        art1.tags.extend([t_python, t_flask, t_web])

        db.session.add(art1)
        db.session.commit()
        print("Database seeded successfully with initial users and posts!")

if __name__ == "__main__":
    seed_data()