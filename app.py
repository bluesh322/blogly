from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

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
    return redirect("/users")

@app.route('/users')
def index():
    """Displays list of users"""
    users = User.query.order_by(User.last_name.asc()).all()
    return render_template('index.html', users=users)

@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    """Show user details"""
    user = User.query.get_or_404(user_id)
    return render_template("details.html", user=user)

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
