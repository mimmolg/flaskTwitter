import datetime
import os
from collections import Counter

from flask import current_app

from routes.auth_routes import mongo


def insert_tweet(username, tweet_content):
    hashtags = extract_hashtags(tweet_content)

    mongo.db.tweets.insert_one({
        'username': username,
        'content': tweet_content,
        'hashtags': hashtags,
        'timestamp': datetime.datetime.now(),
        'likes': [],
        'retweets': 0
    })

    return 'Tweet inviato con successo!'


def get_profile_image_path(username):
    user = mongo.db.users.find_one({'username': username})

    if user:
        # Ottieni il nome del file dell'immagine del profilo dal database
        image_filename = user.get('profile_image_path', '')

        # Componi il percorso relativo all'immagine del profilo all'interno della cartella static
        if image_filename:
            relative_path = f'/static/profile_images/{image_filename}'

            # Verifica se il percorso dell'immagine esiste fisicamente nel filesystem
            full_path = os.path.join(current_app.root_path, 'static', 'profile_images', image_filename)
            if os.path.exists(full_path):
                return relative_path

        # Se l'utente non ha un'immagine del profilo o il percorso non esiste, restituisci il percorso dell'immagine
        # di default
        return '/static/profile_images/default.png'

    # Se l'utente non esiste, restituisci il percorso dell'immagine di default
    return '/static/profile_images/default.png'


# recupera i trending hashtags
def update_trending_hashtags():
    all_tweets = mongo.db.tweets.find()
    all_hashtags = [hashtag.lower() for tweet in all_tweets for hashtag in tweet.get('hashtags', [])]
    trending_hashtags = Counter(all_hashtags).most_common()
    return trending_hashtags


def extract_hashtags(tweet_content):
    return [word[1:] for word in tweet_content.split() if word.startswith('#')]
