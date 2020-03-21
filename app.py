import os
from time import localtime, strftime
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
# from flask_socketio import SocketIO, join_room, leave_room, send
from sklearn.externals import joblib
import pandas as pd 
import numpy as np 



from wtform_fields import *
from models import *

app = Flask(__name__)
# to keep clientside sessions secure 
app.secret_key =os.environ.get('SECRET')

# Configure database
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL')
# To Access Database in terminal:
# psql (copy postgreslink....)


db = SQLAlchemy(app)

# #Initialize flask socketio
# socketio = SocketIO(app)
# Predefined rooms for chat
ROOMS = ["lounge", "news", "Venture Capitalist", "Angel Investor", "Startup Members"]

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
        
        return redirect(url_for('home')) # calls the chat function 

    return render_template('login.html', form=login_form)

@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    '''Makes sure that user is logged in before accessing product '''
    if not current_user.is_authenticated:
        flash('Please login', 'danger')
        return redirect(url_for('login'))

    return render_template("home.html", username=current_user.username)

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash('You have logged out successfully', 'success') # message, category/label
    return redirect(url_for('login'))

@app.route('/predict', methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        # implement pickle file here
        try:
            # grabs data from form input from the user on home page
            NewYork = float(request.form['NewYork'])
            California = float(request.form['California'])
            Florida = float(request.form['Florida'])
            RnD_Spend = float(request.form['RnD_Spend'])
            Admin_Spend = float(request.form['Admin_Spend'])
            Market_Spend = float(request.form['Market_Spend'])
            # create a list of these values
            pred_args = [NewYork,California,Florida,RnD_Spend,Admin_Spend,Market_Spend]
            # convert list values into an array 
            pred_args_array = np.array(pred_args)
            # reshape the array for onehotencoding 
            new_pred_args_array = pred_args_array.reshape(1, -1)
            # grab model from jupyter notebook from pkl file
            mlr_model = open('multiple_linear_model.pkl', 'rb')
            multiple_linear_regression_model = joblib.load(mlr_model)
            # make prediction on data from form
            model_prediction = multiple_linear_regression_model.predict(new_pred_args_array)
            model_prediction = round(float(model_prediction), 2)

        except ValueError: 
            return "Please Enter Values for the Required fields"

    return render_template('predict.html', prediction=model_prediction)



if __name__ == '__main__':
    app.run(debug=True)