from flask_sqlalchemy import SQLAlchemy
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
    img_url = db.Column(db.Text, nullable=False, default="/static/default-cat.png")

    def full_name(self):
        """display full name"""
        u = self
        return f"{u.first_name} {u.last_name}"

class Post(db.Model):
    """Post"""
    def __repr__(self):
        """Show info about a user"""
        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.img_url}>"

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.Text, 
                     nullable=False)
    content = db.Column(db.Text, 
                     nullable=False)
    created_at = db.Column(db.Date, nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer, foreign_key=True, nullable=False)