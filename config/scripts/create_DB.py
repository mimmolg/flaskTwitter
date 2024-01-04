# create_db.py
import json
from datetime import datetime
from flask_bcrypt import Bcrypt
from pymongo import MongoClient


def crea_database(database_name):
    # Connessione al server MongoDB locale sulla porta predefinita 27017
    client = MongoClient('localhost', 27017)

    # Scegli o crea un database
    db = client[database_name]

    print(f"Database '{db}' creato con successo!")


def insert_users(database_name):
    # Connessione al server MongoDB locale sulla porta predefinita 27017
    client = MongoClient('localhost', 27017)

    # Scegli o crea un database
    db = client[database_name]

    print(f"Database '{database_name}' creato con successo!")

    # Utilizza Flask-Bcrypt per l'hashing delle password
    bcrypt = Bcrypt()

    # Leggi i dati utente da un file JSON
    with open('config/scripts/users.json', 'r') as file:
        users_to_insert = json.load(file)

    # Itera attraverso gli utenti e inseriscili nel database
    for user_data in users_to_insert:
        # Esegui l'hash della password
        hashed_password = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')

        # Rimuovi la chiave 'password' dal dizionario (sarà sostituita con l'hash)
        user_data.pop('password')

        # Converte la data di nascita in un oggetto datetime
        user_data['birth_date'] = datetime.strptime(user_data['birth_date'], '%Y-%m-%d')

        # Inserisci l'utente nel database
        db.users.insert_one({
            **user_data,
            'password': hashed_password,
            'birth_date': user_data['birth_date'].strftime('%Y-%m-%d')
        })

    print("Preinserimento completato con successo!")


def insert_tweets(database_name):
    # Connessione al server MongoDB locale sulla porta predefinita 27017
    client = MongoClient('localhost', 27017)

    # Scegli o crea un database
    db = client[database_name]

    # Leggi i dati dei tweet da un file JSON
    with open('config/scripts/tweets.json', 'r') as file:
        tweets_to_insert = json.load(file)

    # Itera attraverso i tweet e inseriscili nel database
    for tweet_data in tweets_to_insert:
        # Converte la data di creazione in un oggetto datetime
        tweet_data['timestamp'] = datetime.strptime(tweet_data['timestamp'], '%Y-%m-%dT%H:%M:%S')

        # Inserisci il tweet nel database
        db.tweets.insert_one(tweet_data)

    print("Preinserimento dei tweet completato con successo!")


def insert_following_followers(database_name):
    # Connessione al server MongoDB locale sulla porta predefinita 27017
    client = MongoClient('localhost', 27017)

    # Scegli o crea un database
    db = client[database_name]

    # Leggi i dati di following e followers da un file JSON
    with open('config/scripts/followers_following.json', 'r') as file:
        data_to_insert = json.load(file)

    # Itera attraverso gli utenti e inserisci following e followers nel database
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
    db = client['demoDB']

    users_collection = db['users']
    tweets_collection = db['tweets']

    users_count = users_collection.count_documents({})
    tweets_count = tweets_collection.count_documents({})

    return users_count == 0 and tweets_count == 0