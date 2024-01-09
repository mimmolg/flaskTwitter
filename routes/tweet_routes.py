from bson import ObjectId
from flask import Blueprint, redirect, url_for, render_template, session

from forms.forms import TweetForm, SearchForm
from routes.auth_routes import mongo
from utils import (update_trending_hashtags, insert_tweet)  # Assicurati che il nome dell'app sia corretto

tweet_blueprint = Blueprint('tweets', __name__)


@tweet_blueprint.route('/timeline', methods=['GET', 'POST'])
def timeline():
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    success_message = session.pop('success_message', None)

    # Retrieve the users you are following
    user = mongo.db.users.find_one({'username': session['username']})
    following = user.get('following', [])

    # Retrieve tweets of the current user and those they are following
    user_tweets = mongo.db.tweets.find({'username': {'$in': [session['username']] + following}})

    tweet_form = TweetForm()

    search_form = SearchForm()

    good_message = None

    bad_message = None

    # Retrieve trending hashtags
    trending_hashtags = update_trending_hashtags()

    if search_form.validate_on_submit():
        search_query = search_form.search_query.data
        # Execute the logic to search for users in the database
        search_results = list(mongo.db.users.find({
            'username': {'$regex': f'.*{search_query}.*', '$options': 'i'}
        }))

        # If there is exactly one result in the search, redirect directly to the user's profile
        if len(search_results) == 1:
            return redirect(url_for('user_profile.view_profile', username=search_results[0]['username']))
        elif not search_results:
            bad_message = 'Nessun Profilo Trovato !'

    if tweet_form.validate_on_submit():
        good_message = insert_tweet(session['username'], tweet_form.tweet_content.data)

        if good_message:
            return redirect(url_for('tweets.timeline'))

        # Now retrieve trending hashtags again
        trending_hashtags = update_trending_hashtags()

    return render_template('timeline.html', tweets=user_tweets,
                           tweet_form=tweet_form, success_message=success_message,
                           good_message=good_message, trending_hashtags=trending_hashtags,
                           search_form=search_form, bad_message=bad_message)


@tweet_blueprint.route('/repeat_tweet/<page>/<tweet_id>', methods=['POST'])
def repeat_tweet(page, tweet_id):
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    # Get the current tweet from the database
    tweet = mongo.db.tweets.find_one({'_id': ObjectId(tweet_id)})

    # Increment the retweet count
    mongo.db.tweets.update_one({'_id': ObjectId(tweet_id)}, {'$inc': {'retweets': 1}})

    # Redirect based on the page (timeline or profile)
    if page == 'tweets.timeline':
        return redirect(url_for('tweets.timeline'))
    elif page == 'profile':
        return redirect(url_for('user_profile.profile'))
    else:
        # Unknown page, handle as preferred
        return redirect(url_for('user_profile.view_profile', username=tweet['username']))


@tweet_blueprint.route('/like_tweet/<page>/<tweet_id>', methods=['POST'])
def like_tweet(page, tweet_id):
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    # Get the current tweet from the database
    tweet = mongo.db.tweets.find_one({'_id': ObjectId(tweet_id)})

    # Check if the user has already liked the tweet
    if session['username'] in tweet['likes']:
        # if yes, remove the like
        mongo.db.tweets.update_one({'_id': ObjectId(tweet_id)},
                                   {'$pull': {'likes': session['username']}})
    else:
        # if no, add the like
        mongo.db.tweets.update_one({'_id': ObjectId(tweet_id)},
                                   {'$push': {'likes': session['username']}})

    # Redirect based on the page (timeline or profile)
    if page == 'tweets.timeline':
        return redirect(url_for('tweets.timeline'))
    elif page == 'profile':
        return redirect(url_for('user_profile.profile'))
    else:
        return redirect(url_for('user_profile.view_profile', username=tweet['username']))


@tweet_blueprint.route('/hashtag/<hashtag>', methods=['GET'])
def hashtag_tweets(hashtag):
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    # Retrieve all tweets containing the specified hashtag (case-insensitive)
    hashtag_tweetss = list(mongo.db.tweets.find({'hashtags': {'$regex': f'^{hashtag}$', '$options': 'i'}}))

    return render_template('hashtag_tweets.html', hashtag_tweets=hashtag_tweetss,
                           hashtag=hashtag)

