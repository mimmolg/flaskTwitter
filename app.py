from flask import Flask, redirect, url_for
from flask_bcrypt import Bcrypt

from config.db_config import DBConfig  # Importa la classe DBConfig dal file db_config.py
from routes.auth_routes import auth_blueprint, mongo
from routes.tweet_routes import tweet_blueprint
from routes.user_profile_routes import user_profile_blueprint
from utils import get_profile_image_path
from config.scripts.create_DB import crea_database, insert_users, insert_tweets, \
    insert_following_followers, is_db_empty  # Importa la funzione crea_database

app = Flask(__name__)
app.config.from_object(DBConfig)  # Usa le configurazioni del database
mongo.init_app(app)
bcrypt = Bcrypt(app)

if is_db_empty():
    # Chiamare la funzione per creare il database
    crea_database('demoDB')
    # Chiamare la funzione per inserire gli utenti nel database
    insert_users('demoDB')
    # Chiamare la funzione per inserire i tweet nel database
    insert_tweets('demoDB')
    # Chiamare la funzione per inserire i segui e seguiti nel database
    insert_following_followers('demoDB')

app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(tweet_blueprint, url_prefix='/tweets')
app.register_blueprint(user_profile_blueprint, url_prefix='/user_profile')


@app.route('/')
def home():
    return redirect(url_for('auth.login'))


# Aggiungi questa funzione context_processor per renderla disponibile nei tuoi template
@app.context_processor
def utility_processor():
    return dict(get_profile_image_path=get_profile_image_path)


if __name__ == '__main__':
    app.run(debug=True)
