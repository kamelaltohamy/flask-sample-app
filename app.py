import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
import hashlib

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///T:/test_L/flaskr/chapter3/snap.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'putheretrjurtrandom---secretkey'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
flask_bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40),unique=True)
    email = db.Column(db.String(255),unique=True)
    _password = db.Column(db.String(60))
    created_on = db.Column(db.DateTime,default=datetime.datetime.utcnow)

    def __repr__(self):
        return  "< User {!r} >".format(self.username)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)

    @hybrid_property
    def password(self):
        return self._password
    
    @password.setter
    def password(self,password):
        self._password = flask_bcrypt.generate_password_hash(password)


class Snap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    extension = db.Column(db.String(12))
    content = db.Column(db.Text())
    hash_key = db.Column(db.String(40),unique=True)
    created_on = db.Column(db.DateTime,default = datetime.datetime.utcnow,index=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    user = db.relationship('User',backref=db.backref('snaps',lazy='dynamic'))

    


    # def __init__(self,user_id,name,content,extension):
    #     self.user_id = user_id
    #     self.name= name
    #     self.content = content
    #     self.extension = extension
    #     self.created_on = datetime.datetime.utcnow()
    #     self.hash_key = hashlib.sha1(self.content+ str(self.created_on)).hexdigest()
    
    def __repr__(self):
        return '<Snap  {!r}>'.format(self.id)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from views import *
from forms import *
if __name__ == "__main__":
    app.run(debug = True)
