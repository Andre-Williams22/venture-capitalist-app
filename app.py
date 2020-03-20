from flask import Flask, render_template, url_for, request, redirect
from wtform_fields import *
from models import *

app = Flask(__name__)
# to keep clientside sessions secure 
app.secret_key = 'replace later'

# Configure database
app.config['SQLALCHEMY_DATABASE_URI']='postgres://nutgejunpisnuf:00c0a8255cc7ecbc5ad01197d0933906b367815398be4ce7811ffc46562f79bf@ec2-35-172-85-250.compute-1.amazonaws.com:5432/d9q7ih6h1mkskb'
# To Access Database in terminal:
# psql (copy postgreslink....)

db = SQLAlchemy(app)

@app.route("/", methods=['GET', 'POST'])
def index():

    reg_form = RegistrationForm()
    # Updated database id validation is successful
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data 

        hashed_password = pbkdf2_sha256.hash(password)

        # Add user to DB
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template("index.html", form=reg_form)

@app.route("/login", methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    # Allow login if validation success 
    if login_form.validate_on_submit():
        return 'Logged in'

    return render_template('login.html', form=login_form)


if __name__ == '__main__':
    app.run(debug=True)