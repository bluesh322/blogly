"""Seed file for blogly"""

from models import User, Post, Tag, PostTag, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
blues = User(first_name="Blues", last_name="Henderson", img_url="/static/default-cat.png")
jerry = User(first_name="Jerry", last_name="Irvin")
katie = User(first_name="Katie", last_name="Drago")
travis = User(first_name="Travis", last_name="Allan")
ellie = User(first_name="Eleanor", last_name="Carl")
sarah = User(first_name="Sarah", last_name="Brown")

db.session.add(blues)
db.session.add(jerry)
db.session.add(katie)
db.session.add(travis)
db.session.add(ellie)
db.session.add(sarah)


db.session.commit()

post1 = Post(title="I'm starting a blog",content="It's about my cat, Robot", user_id = 1)
post2 = Post(title="Sup its Jerry!", content="I want to make music, but being poor don't help", user_id=2)
post3 = Post(title="I'm the best around",content="My dog told me so.", user_id = 1)
post4 = Post(title="You can't make this up!", content="They want dogs in space!", user_id=2)
post5 = Post(title="It's just a cat in a bag",content="Just look at him, next week he'll be in a box", user_id = 1)
post6 = Post(title="Oops, I did it again", content="I shrunk my car to the size of a hot wheel, what am I gonna do now?", user_id=1)
post7 = Post(title="All dogs go to heaven",content="I'mma have a lot of dogs waiting for me in heaven", user_id = 5)
post8 = Post(title="Make up why you like make up", content="it's not that complicated I look great!", user_id=3)
post9 = Post(title="Anime is the only way",content="I've been hard crushing on the lead character in my hero academia for years!", user_id = 6)
post10 = Post(title="Music makes me mad", content="It's so big and small at the same time", user_id=4)



db.session.add(post1)
db.session.add(post2)
db.session.add(post3)
db.session.add(post4)
db.session.add(post5)
db.session.add(post6)
db.session.add(post7)
db.session.add(post8)
db.session.add(post9)
db.session.add(post10)

db.session.commit()

tag1 = Tag(name="sunsets")
tag2 = Tag(name="music")
tag3 = Tag(name="anime")
tag4 = Tag(name="cats")

db.session.add(tag1)
db.session.add(tag2)
db.session.add(tag3)
db.session.add(tag4)

db.session.commit()

post_tag1 = PostTag(post_id=10, tag_id=2)
post_tag2 = PostTag(post_id=9, tag_id=3)
post_tag3 = PostTag(post_id=5, tag_id=4)
post_tag4 = PostTag(post_id=1, tag_id=4)
post_tag5 = PostTag(post_id=1, tag_id=3)

db.session.add(post_tag1)
db.session.add(post_tag2)
db.session.add(post_tag3)
db.session.add(post_tag4)
db.session.add(post_tag5)


db.session.commit()

