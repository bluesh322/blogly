"""Seed file for blogly"""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
blues = User(first_name="Blues", last_name="Henderson", img_url="/static/default-cat.png")
jerry = User(first_name="Jerry", last_name="Irvin")

db.session.add(blues)
db.session.add(jerry)

db.session.commit()