# seed.py
from app import app
from database import db
from models import Movie, User


def seed_data():
  with app.app_context():
    # 1. Create tables if they don't exist
    db.create_all()

    # 2. Seed Default Admin
    if not User.query.filter_by(username='admin').first():
      admin = User(
          username='admin', email='admin@streamflix.local', is_admin=True
      )
      admin.set_password('Admin@12345')
      db.session.add(admin)

    # 3. Seed Sample Movies
    if Movie.query.count() == 0:
      sample_movies = [
          Movie(
              title='The Last Horizon',
              description=(
                  'A rescue pilot races across a storm-covered planet.'
              ),
              genre='Adventure',
              year=2025,
              rating=8.4,
              duration='2h 08m',
              poster='https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=700&q=80',
              banner='https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1600&q=85',
              video_url='https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4',
          ),
          Movie(
              title='Midnight Code',
              description=(
                  'A young programmer discovers a hidden message in an old'
                  ' archive.'
              ),
              genre='Thriller',
              year=2024,
              rating=8.1,
              duration='1h 52m',
              poster='https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=700&q=80',
              banner='https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=1600&q=85',
              video_url='https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4',
          ),
          Movie(
              title='Neon City',
              description='A detective follows a trail through a futuristic city.',
              genre='Action',
              year=2025,
              rating=8.6,
              duration='2h 16m',
              poster='https://images.unsplash.com/photo-1519608487953-e999c86e7455?w=700&q=80',
              banner='https://images.unsplash.com/photo-1519608487953-e999c86e7455?w=1600&q=85',
              video_url='https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4',
          ),
      ]
      db.session.add_all(sample_movies)

    db.session.commit()
    print('Database seeded successfully!')


if __name__ == '__main__':
  seed_data()