from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()
# Terminal commands 
# Command D to exit 
# \dt 
# \d users
# table users;


class User(db.Model):
    '''User model '''
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)


