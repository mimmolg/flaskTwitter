# auth_routes.py
import datetime

from flask import Blueprint, redirect, url_for, render_template, session, request, flash
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo

from forms.forms import LoginForm, RegistrationForm

# Create instances of Flask extensions
mongo = PyMongo()
bcrypt = Bcrypt()
# Create a Blueprint named 'auth'
auth_blueprint = Blueprint('auth', __name__)


# Route for user login
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error_message = None
    success_message = request.args.get('success_message')  # bring the message from the request for registration success

    if form.validate_on_submit():
        # If the form is submitted and valid
        username = form.username.data
        password = form.password.data

        # Query the database to find the user by username
        user = mongo.db.users.find_one({'username': username})

        # Check if the user exists and the password matches the hashed password
        if user and bcrypt.check_password_hash(user['password'], password):
            success_message = 'Login eseguito con successo!'
            session['username'] = username  # Store the username in the session for tracking authentication
            session['success_message'] = success_message
            return redirect(url_for('tweets.timeline'))  # Redirect to the user's timeline after successful login
        else:
            error_message = 'Credenziali non valide. Riprova.'

    return render_template('login.html', form=form, error_message=error_message, success_message=success_message)


# Route for user registration
@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    try:
        if form.validate_on_submit():
            # If the form is submitted and valid
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            username = form.username.data
            password = form.password.data
            birth_date_str = form.birth_date.data

            if birth_date_str:
                # Convert date from string to datetime.date object
                birth_date = datetime.datetime.strptime(birth_date_str, '%d-%m-%Y').date()

                # Check if there is already a user with the same email or username
                existing_user = mongo.db.users.find_one({"$or": [{"email": email}, {"username": username}]})
                if existing_user:
                    flash('Email o nome utente già in uso. Scegliere un altro.', 'danger')
                    return render_template('register.html', form=form)

                # Generate hashed password for security
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

                # Continue with user registration by inserting data into the database
                mongo.db.users.insert_one({
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'username': username,
                    'password': hashed_password,
                    'birth_date': birth_date.strftime('%Y-%m-%d')
                })

                return redirect(url_for('auth.login',
                                        success_message='Registrazione completata con successo! Ora puoi effettuare '
                                                        'il login'))
    except Exception as e:
        print(e)

    return render_template('register.html', form=form)


# Route for user logout
@auth_blueprint.route('/logout')
def logout():
    # Clear all data stored in the session
    session.clear()
    # Redirect the user to the login page (or home page)
    return redirect(url_for('auth.login'))
