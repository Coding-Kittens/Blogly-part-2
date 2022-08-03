"""Blogly application."""

from flask import *
from models import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route('/')
def home_page():
    """ redirects to the users page"""
    return redirect('/users')

@app.route('/users')
def show_users():
    """ Shows the users page wich lists the users on it"""
    users = User.query.all()
    return render_template('users_page.html',users=users)

@app.route('/users/new',methods =['GET'])
def new_user_page():
    """ Shows the create user form """
    return render_template('create_user.html')


@app.route('/users/new',methods=['POST'])
def make_new_user():
    """ makes a new user from the form information then gose back to /users"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    profile_pic = request.form['pic']
    new_user = None

    if profile_pic:
        new_user = User(first_name=first_name,last_name=last_name,image_url=profile_pic)
    else:
        new_user = User(first_name=first_name,last_name=last_name)

    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')


@app.route('/user/<int:user_id>')
def user_page(user_id):
    """ Shows the user whos id was passed in """
    current_user = User.query.get_or_404(user_id)

    return render_template('user.html',current_user=current_user)


@app.route('/user/<int:user_id>/edit',methods=['GET'])
def edit_user_page(user_id):
    """ Shows the edit user form """
    current_user = User.query.get_or_404(user_id)
    return render_template('edit_user.html',current_user=current_user)


@app.route('/user/<int:user_id>/edit',methods=['POST'])
def edit_user(user_id):
    """edits a user with the information from the form """
    current_user = User.query.get_or_404(user_id)

    current_user.first_name = request.form['first_name'] if request.form['first_name'] else current_user.first_name
    current_user.last_name = request.form['last_name'] if request.form['last_name'] else current_user.last_name
    current_user.image_url = request.form['pic'] if request.form['pic'] else current_user.image_url

    db.session.add(current_user)
    db.session.commit()
    return redirect('/users')


@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    """ Deletes a user based on user_id """

    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect('/users')







@app.route('/users/<int:user_id>/posts/new',methods=['GET'])
def new_post_page(user_id):
    """ Shows the form to add a post """
    current_user = User.query.get_or_404(user_id)
    return render_template('add_post.html',current_user=current_user)


@app.route('/users/<int:user_id>/posts/new',methods=['POST'])
def add_post(user_id):
    """ Adds a new post """

    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title,content=content,user_id=user_id)


    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/user/{user_id}')



@app.route('/posts/<int:post_id>')
def post_page(post_id):
    """ Shows a post """
    current_post = Post.query.get_or_404(post_id)
    return render_template('post_page.html',current_post=current_post)



@app.route('/posts/<int:post_id>/edit',methods=['GET'])
def edit_post_page(post_id):
    """ Shows the form to edit a post """
    current_post = Post.query.get_or_404(post_id)
    return render_template('edit_post.html',current_post=current_post)




@app.route('/posts/<int:post_id>/edit',methods=['POST'])
def edit_post(post_id):
    """ Edits a post """

    current_post = Post.query.get_or_404(post_id)
    user_id = current_post.user_id

    current_post.title = request.form['title'] if request.form['title'] else current_post.title
    current_post.content = request.form['content'] if request.form['content'] else current_post.content


    db.session.add(current_post)
    db.session.commit()

    return redirect(f'/posts/{current_post.id}')


@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """ Deletes a post """
    current_post = Post.query.get_or_404(post_id)
    user_id = current_post.user_id
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect(f'/user/{user_id}')
