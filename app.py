from flask import Flask, render_template, url_for, request, redirect

from wtform_fields import *
from models import *

app = Flask(__name__)
# to keep clientside sessions secure 
app.secret_key = 'replace later'

# Configure database
app.config['SQLALCHEMY_DATABASE_URI']='postgres://nutgejunpisnuf:00c0a8255cc7ecbc5ad01197d0933906b367815398be4ce7811ffc46562f79bf@ec2-35-172-85-250.compute-1.amazonaws.com:5432/d9q7ih6h1mkskb'
db = SQLAlchemy(app)

@app.route("/", methods=['GET', 'POST'])
def index():

    reg_form = RegistrationForm()

    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data 

        # Check username exists
        user_object = User.query.filter_by(username=username).first()
        if user_object: # if user_object exists already
            return "Someone else has taken this username"
        # Add user to DB
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return "Inserted into DB!"

    return render_template("index.html", form=reg_form)


if __name__ == '__main__':
    app.run(debug=True)