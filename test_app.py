from unittest import TestCase
from app import app
from models import db, connect_db, User, Post, PostTag, Tag

app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test_db'
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']




class ViewsTests(TestCase):

    def setUp(self):
        """Set up before running each test"""

        # Because of key constraints it seems best to just build the db each time you run a test, rather than delete individual elements
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

        self.user_id = blues.id
        self.post_id = post1.id
        self.tag_id = tag1.id

    def teardown(self):
        """any failed test, rollback"""
        db.session.rollback()

    def test_view_blog_posts(self):
        """Check information in the session and html is displayed"""

        with app.test_client() as client:

            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Blogly Recent Posts', html)
            self.assertIn('starting a blog', html)
            self.assertIn('<a href="/tags/1" class="badge badge-primary">cats</a>', html)
