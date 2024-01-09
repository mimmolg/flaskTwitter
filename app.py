from flask import Flask, redirect, url_for
from flask_bcrypt import Bcrypt

from config.db_config import DBConfig  # Import the DBConfig class from the db_config.py file
from routes.auth_routes import auth_blueprint, mongo
from routes.tweet_routes import tweet_blueprint
from routes.user_profile_routes import user_profile_blueprint
from utils import get_profile_image_path
from config.scripts.create_DB import crea_database, insert_users, insert_tweets, \
    insert_following_followers, is_db_empty  # Import the crea_database function

app = Flask(__name__)
app.config.from_object(DBConfig)  # Use the database configurations
mongo.init_app(app)
bcrypt = Bcrypt(app)

if is_db_empty():
    # Call the function to create the database
    crea_database('demoDB')
    # Call the function to insert users into the database
    insert_users('demoDB')
    # Call the function to insert tweets into the database
    insert_tweets('demoDB')
    # Call the function to insert following and followers into the database
    insert_following_followers('demoDB')

app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(tweet_blueprint, url_prefix='/tweets')
app.register_blueprint(user_profile_blueprint, url_prefix='/user_profile')


@app.route('/')
def home():
    return redirect(url_for('auth.login'))


# Add this context_processor function to make it available in your templates
@app.context_processor
def utility_processor():
    return dict(get_profile_image_path=get_profile_image_path)


if __name__ == '__main__':
    app.run()
