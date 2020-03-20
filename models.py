from flask_sqlalchemy import SQLAlchemy 
from flask_login import UserMixin
db = SQLAlchemy()
# Terminal commands 
# Command D to exit 
# \dt 
# \d users
# table users;


class User(UserMixin, db.Model): # usermixin allows us to modify existing or create new tables in database
    '''User model '''
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)


