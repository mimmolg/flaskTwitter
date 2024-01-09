import datetime
import os
from collections import Counter

from flask import current_app

from routes.auth_routes import mongo


# Function to insert a tweet into the database
def insert_tweet(username, tweet_content):
    # Extract hashtags from the tweet content
    hashtags = extract_hashtags(tweet_content)

    # Insert the tweet data into the 'tweets' collection in the database
    mongo.db.tweets.insert_one({
        'username': username,
        'content': tweet_content,
        'hashtags': hashtags,
        'timestamp': datetime.datetime.now(),
        'likes': [],
        'retweets': 0
    })

    return 'Tweet inviato con successo!'


# Function to get the profile image path for a given username
def get_profile_image_path(username):
    # Find the user document in the 'users' collection in the database
    user = mongo.db.users.find_one({'username': username})

    if user:
        # Get the profile image file name from the database
        image_filename = user.get('profile_image_path', '')

        # Compose the relative path to the profile image within the 'static' folder
        if image_filename:
            relative_path = f'/static/profile_images/{image_filename}'

            # Check if the image path physically exists in the filesystem
            full_path = os.path.join(current_app.root_path, 'static', 'profile_images', image_filename)
            if os.path.exists(full_path):
                return relative_path

        # If the user doesn't have a profile image or the path doesn't exist, return the default image path
        return '/static/profile_images/default.png'

    # If the user doesn't exist, return the default image path
    return '/static/profile_images/default.png'


# Function to update and retrieve trending hashtags
def update_trending_hashtags():
    # Retrieve all tweets from the 'tweets' collection in the database
    all_tweets = mongo.db.tweets.find()

    # Extract all hashtags from the tweets and count their occurrences
    all_hashtags = [hashtag.lower() for tweet in all_tweets for hashtag in tweet.get('hashtags', [])]
    trending_hashtags = Counter(all_hashtags).most_common()
    return trending_hashtags


# Function to extract hashtags from tweet content
def extract_hashtags(tweet_content):
    return [word[1:] for word in tweet_content.split() if word.startswith('#')]
