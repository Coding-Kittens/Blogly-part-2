"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """ User model """
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    first_name = db.Column(db.Text,nullable = False)
    last_name = db.Column(db.Text,nullable = False)
    image_url = db.Column(db.Text,nullable = False,default ='https://nypost.com/wp-content/uploads/sites/2/2022/07/Cat-feature.jpg')

    def __repr__(self):
        return f'id ={self.id},first_name={self.first_name},last_name={self.last_name},image_url={self.image_url}'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


class Post(db.Model):
    """ Post model for blog posts """
    __tablename__ = 'posts'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(20),nullable = False)
    content = db.Column(db.String(300),nullable = False)
    created_at = db.Column(db.DateTime,nullable = False,default=datetime.datetime.now())
    user_id =db.Column(db.Integer, db.ForeignKey('users.id'),nullable = False)
    user = db.relationship('User',backref ='posts')

    def __repr__(self):
        return f'id ={self.id},title={self.title},content={self.content},created_at={self.created_at},user_id={self.user_id}'
