"""Seed file for blogly"""

from models import User, Post, Tag, PostTag, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

blues = User(first_name="Blues", last_name="Henderson", img_url="/static/default-cat.png")

db.session.add(blues)

db.session.commit()

post1 = Post(title="I'm starting a blog",content="It's about my cat, Robot", user_id = 1)

db.session.add(post1)

db.session.commit()

tag1 = Tag(name="cats")

db.session.add(tag1)

db.session.commit()

post_tag1 = PostTag(post_id=1, tag_id=1)

db.session.add(post_tag1)

db.session.commit()