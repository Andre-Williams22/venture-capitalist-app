from flask import Flask, render_template, url_for, request, redirect, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

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

#Configure flask login
login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):

    return User.query.get(int(id)) # grabs id as an integer

@app.route("/", methods=['GET', 'POST'])
def index():

    reg_form = RegistrationForm()
    # Updated database if validation is successful
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data 

        hashed_password = pbkdf2_sha256.hash(password)

        # Add user to DB
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        # before redirecting to login route lets send a message to the user to show their registration is successful
        flash('Registered successfully. Please login.', 'success') # matches a bootstrap class for css

        return redirect(url_for('login'))

    return render_template("index.html", form=reg_form)

@app.route("/login", methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    # Allow login if validation success 
    if login_form.validate_on_submit():

        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        
        return redirect(url_for('chat')) # calls the chat function 

    return render_template('login.html', form=login_form)

@app.route("/chat", methods=['GET', 'POST'])
@login_required
def chat():
    '''Makes sure that user is logged in before accessing product '''
    if not current_user.is_authenticated:
        flash('Please login.', 'danger') # message, category/label
        return redirect(url_for('login'))
    return 'chat with me'  

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash('You have logged out successfully', 'success') # message, category/label
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)