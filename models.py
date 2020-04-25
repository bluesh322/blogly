from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)

# Models go below


class User(db.Model):
    """User"""

    # @classmethod
    # def get_by_species(cls, species):
    #     return cls.query.filter_by(species=species).all()
    def __repr__(self):
        """Show info about a user"""
        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.img_url}>"

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.Text,
                           nullable=False)
    last_name = db.Column(db.Text,
                          nullable=False)
    img_url = db.Column(db.Text, nullable=False,
                        default="/static/default-cat.png")

    def full_name(self):
        """display full name"""
        u = self
        return f"{u.first_name} {u.last_name}"


class Post(db.Model):
    """Post"""

    def __repr__(self):
        """Show info about a user"""
        p = self
        return f"<Post {p.id} {p.title} {p.content} {p.created_at} {p.user_id}>"

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.Text,
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)

    user = db.relationship("User", backref=backref(
        "posts", cascade="all, delete-orphan"))

    # post_tag = db.relationship("PostTag", backref="post", cascade="all, delete")

    tags = db.relationship("Tag", secondary="posts_tags", backref="posts", cascade="all, delete")


class PostTag(db.Model):
    """PostTag"""

    def __repr__(self):
        """Show info about a post_tag"""
        p = self
        return f"<PostTag {p.post_id} {p.tag_id}>"

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey(
        "posts.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)


class Tag(db.Model):
    """Tag"""

    def __repr__(self):
        """Show info about a tag"""
        t = self
        return f"<Tag {t.id} {t.name}>"

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True)
    name = db.Column(db.Text,
                     nullable=False)

    # post_tag = db.relationship("PostTag", backref="tag", cascade="all, delete")
