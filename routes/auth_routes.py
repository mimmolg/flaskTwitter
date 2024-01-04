# auth_routes.py
import datetime

from flask import Blueprint, redirect, url_for, render_template, session, request, flash
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo

from forms.forms import LoginForm, RegistrationForm

mongo = PyMongo()
bcrypt = Bcrypt()
auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error_message = None
    success_message = request.args.get('success_message')  # Recupera il messaggio dalla richiesta per il messaggio
    # di registrazione

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = mongo.db.users.find_one({'username': username})

        if user and bcrypt.check_password_hash(user['password'], password):
            success_message = 'Login eseguito con successo!'
            session['username'] = username
            session['success_message'] = success_message
            return redirect(url_for('tweets.timeline'))
        else:
            error_message = 'Credenziali non valide. Riprova.'

    return render_template('login.html', form=form, error_message=error_message, success_message=success_message)


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    try:
        if form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            username = form.username.data
            password = form.password.data
            birth_date_str = form.birth_date.data

            if birth_date_str:
                birth_date = datetime.datetime.strptime(birth_date_str, '%d-%m-%Y').date()

                # Controlla se esiste già un utente con la stessa email o username
                existing_user = mongo.db.users.find_one({"$or": [{"email": email}, {"username": username}]})
                if existing_user:
                    flash('Email o nome utente già in uso. Scegliere un altro.', 'danger')
                    return render_template('register.html', form=form)

                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

                # Continua con la registrazione
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


@auth_blueprint.route('/logout')
def logout():
    # Elimina tutti i dati della sessione
    session.clear()
    # Reindirizza l'utente alla pagina di login (o alla home page)
    return redirect(url_for('auth.login'))
