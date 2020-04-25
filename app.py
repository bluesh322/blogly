from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'somemoregoodfun'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
sess = db.session # I don't wanna type db.session all the time

@app.route('/')
def show_index():
    """Redirects to /users"""
    posts_by_recent = Post.query.order_by(Post.created_at.asc()).limit(5).from_self().all()
    return render_template("blogly.html", posts_by_recent=posts_by_recent)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

# ------------------------------------------User ROUTES------------------------------------------------------------------------

@app.route('/users')
def index():
    """Displays list of users"""
    users = User.query.order_by(User.last_name.asc()).all()
    return render_template('index.html', users=users)

@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    """Show user details"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user_id).all()
    return render_template("user-details.html", user=user, posts=posts)

@app.route('/users/new')
def show_add_user_form():
    """Show add user form"""
    return render_template("addUser.html")

@app.route('/users/new', methods=["POST"])
def submit_new_user():
    """Submits new user form and redirects back to users"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    img_url = request.form["img_url"]
    img_url = img_url if img_url != '' else None

    new_user = User(first_name=first_name, last_name=last_name, img_url=img_url)
    sess.add(new_user)
    sess.commit()

    return redirect(f"/users")

@app.route('/users/<int:user_id>/edit')
def show_edit_user_form(user_id):
    """Show edit user form"""
    user = User.query.get_or_404(user_id)
    return render_template("editUser.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def submit_edit_user(user_id):
    """Submits edit user form and redirects back to users"""
    action = request.form.get("save")
    if action == "save":
        edit_user = User.query.get_or_404(user_id)
        edit_user.first_name = request.form["first_name"]
        edit_user.last_name = request.form["last_name"]
        edit_user.img_url = request.form["img_url"]

        sess.add(edit_user)
        sess.commit()

        return redirect(f"/users")
    else: 
        return redirect(f"/users")

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Show add user form"""
    rem = User.query.filter(User.id == user_id).delete()
    if rem == 1:
        sess.commit()
    else: 
        # if you manually input an invalid id rem should not be 1
        sess.rollback()
    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def add_post(user_id):
    """Show add post form"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("addPost.html", user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def submit_add_post(user_id):
    """Show add post form"""
    action = request.form.get("add")
    tags = Tag.query.all()
    tag_list = [tag.id if request.form.get(f"tag_{tag.id}") else False for tag in tags]
    if action == "add":
        
        title = request.form["title"]
        content = request.form["content"]

        new_post = Post(title=title, content=content, user_id=user_id)
        print(new_post)

        sess.add(new_post)
        sess.commit()

        for tag in tag_list:
            if tag != False:
                new_post_tag = PostTag(post_id=new_post.id, tag_id=tag)
                sess.add(new_post_tag)
                sess.commit()

        return redirect(f"/users/{user_id}")
    else: 
        return redirect(f"/users/{user_id}")
    

# ------------------------------------------POST ROUTES------------------------------------------------------------------------

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show details of a post"""

    post = Post.query.filter(Post.id == post_id).first()
    return render_template("post-details.html", post=post)
    
@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """Show edit user form"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    tag_checked = [tag.name for tag in post.tags]
    return render_template("editPost.html", post=post, tags=tags, tag_checked=tag_checked)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def submit_edit_post(post_id):
    """Submits edit user form and redirects back to users"""
    action = request.form.get("save")
    tags = Tag.query.all()
    tag_list = [tag.id if request.form.get(f"tag_{tag.id}") else False for tag in tags]
    if action == "save":
        edit_post = Post.query.get_or_404(post_id)
        edit_post.title = request.form["title"]
        edit_post.content = request.form["content"]
        tag_checked = [tag.id for tag in edit_post.tags]

        sess.add(edit_post)
        sess.commit()

        for tag in tag_list:
            if tag != False and tag not in tag_checked:
                new_post_tag = PostTag(post_id=post_id, tag_id=tag)
                sess.add(new_post_tag)
                sess.commit()

        return redirect(f"/posts/{post_id}")
    else: 
        return redirect(f"/posts/{post_id}")

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Show add user form"""
    post = Post.query.get(post_id)
    user_id = post.user_id
    rem = Post.query.filter(Post.id == post_id).delete()
    
    if rem == 1:
        sess.commit()
    else: 
        # if you manually input an invalid id rem should not be 1
        sess.rollback()
    return redirect(f'/users/{user_id}')

# ------------------------------------------TAG ROUTES------------------------------------------------------------------------

@app.route('/tags')
def show_tags():
    """Show tag names"""
    tags = Tag.query.all()
    return render_template("tags.html", tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag_detail(tag_id):
    """Show tag names"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tag-details.html", tag=tag)

@app.route('/tags/new')
def show_add_tag_form():
    """Show add user form"""
    return render_template("addTag.html")

@app.route('/tags/new', methods=["POST"])
def submit_new_tag():
    """Submits new user form and redirects back to users"""
    name = request.form["name"]

    new_tag = Tag(name=name)
    sess.add(new_tag)
    sess.commit()

    return redirect(f"/tags")

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):
    """Show edit tag form"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("editTag.html", tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def submit_edit_tag(tag_id):
    """Submits edit tag form and redirects back to tags"""
    action = request.form.get("save")
    if action == "save":
        edit_tag = Tag.query.get_or_404(tag_id)
        edit_tag.name = request.form["name"]

        sess.add(edit_tag)
        sess.commit()

        return redirect(f"/tags")
    else: 
        return redirect(f"/tags")

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    """Show add tag form"""
    rem = Tag.query.filter(Tag.id == tag_id).first()
    rem.posts.clear()
    sess.add(rem)
    sess.commit()
    rem = Tag.query.filter(Tag.id == tag_id).delete()

    if rem == 1:
        sess.commit()
    else: 
        # if you manually input an invalid id rem should not be 1
        sess.rollback()

    return redirect('/tags')