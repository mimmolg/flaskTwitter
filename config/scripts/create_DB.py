# create_db.py
import json
from datetime import datetime
from flask_bcrypt import Bcrypt
from pymongo import MongoClient


def crea_database(database_name):
    # Connect to the local MongoDB server on the default port 27017
    client = MongoClient('localhost', 27017)

    # Choose or create a database
    db = client[database_name]

    print(f"Database '{db}' creato con successo!")


def insert_users(database_name):
    client = MongoClient('localhost', 27017)

    db = client[database_name]

    print(f"Database '{database_name}' creato con successo!")

    # Use Flask-Bcrypt for password hashing
    bcrypt = Bcrypt()

    # Read user data from a JSON file
    with open('config/script/users.json', 'r') as file:
        users_to_insert = json.load(file)

    # Iterate through users and insert them into the database
    for user_data in users_to_insert:
        # Generate the password hash
        hashed_password = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')

        # Remove the 'password' key from the dictionary (it will be replaced with the hash)
        user_data.pop('password')

        # Convert the date to a datetime object
        user_data['birth_date'] = datetime.strptime(user_data['birth_date'], '%Y-%m-%d')

        # Insert the user into the database
        db.users.insert_one({
            **user_data,
            'password': hashed_password,
            'birth_date': user_data['birth_date'].strftime('%Y-%m-%d')
        })

    print("Preinserimento completato con successo!")


def insert_tweets(database_name):
    client = MongoClient('localhost', 27017)

    db = client[database_name]

    # Read tweet data from a JSON file
    with open('config/script/tweets.json', 'r') as file:
        tweets_to_insert = json.load(file)

    # Iterate through tweets and insert them into the database
    for tweet_data in tweets_to_insert:
        # Convert the creation date to a datetime object
        tweet_data['timestamp'] = datetime.strptime(tweet_data['timestamp'], '%Y-%m-%dT%H:%M:%S')

        # Insert the tweet into the database
        db.tweets.insert_one(tweet_data)

    print("Preinserimento dei tweet completato con successo!")


def insert_following_followers(database_name):
    client = MongoClient('localhost', 27017)

    db = client[database_name]

    # Read following and followers data from a JSON file
    with open('config/script/followers_following.json', 'r') as file:
        data_to_insert = json.load(file)

    # Iterate through users and insert following and followers into the database
    for user_data in data_to_insert['users']:
        username = user_data['username']

        if 'following' in user_data:
            following_list = user_data['following']
            db.users.update_one({'username': username}, {'$set': {'following': following_list}})

        if 'followers' in user_data:
            followers_list = user_data['followers']
            db.users.update_one({'username': username}, {'$set': {'followers': followers_list}})

    print("Preinserimento di following e followers completato con successo!")


def is_db_empty():
    client = MongoClient('localhost', 27017)

    # Choose the 'demoDB' database
    db = client['demoDB']

    # Get references to the 'users' and 'tweets' collections in the 'demoDB' database
    users_collection = db['users']
    tweets_collection = db['tweets']

    # Count the number of documents in the 'users' and 'tweets' collections
    users_count = users_collection.count_documents({})
    tweets_count = tweets_collection.count_documents({})

    # Return True if both collections are empty, otherwise return False
    return users_count == 0 and tweets_count == 0
