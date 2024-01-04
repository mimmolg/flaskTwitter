import os

from flask import Blueprint, render_template, url_for, session
from werkzeug.utils import redirect

from forms.forms import FollowForm, TweetForm, UnfollowForm, ProfileImageForm
from routes.auth_routes import mongo
from utils import get_profile_image_path, insert_tweet

user_profile_blueprint = Blueprint('user_profile', __name__)


@user_profile_blueprint.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    user_tweets = list(mongo.db.tweets.find({'username': session['username']}))
    user = mongo.db.users.find_one({'username': session['username']})
    following = user.get('following', [])
    follow_form = FollowForm()
    tweet_form = TweetForm()
    unfollow_form = UnfollowForm()
    profile_image_form = ProfileImageForm()

    good_message = None
    warning_message = None
    danger_message = None

    if tweet_form.validate_on_submit():
        good_message = insert_tweet(session['username'], tweet_form.tweet_content.data)

        if good_message:
            return redirect(url_for('user_profile.profile'))

    if unfollow_form.validate_on_submit():
        unfollow_username = unfollow_form.unfollow_username.data

        if unfollow_username == session['username']:
            danger_message = 'Non puoi smettere di seguire te stesso.'
        elif unfollow_username not in following:
            warning_message = f'Non stai seguendo {unfollow_username}.'
        else:
            mongo.db.users.update_one({'username': session['username']},
                                      {'$pull': {'following': unfollow_username}})
            mongo.db.users.update_one({'username': unfollow_username},
                                      {'$pull': {'followers': session['username']}})
            good_message = f'Hai smesso di seguire {unfollow_username}.'

    if follow_form.validate_on_submit():
        follow_username = follow_form.follow_username.data
        user_to_follow = mongo.db.users.find_one({'username': follow_username})

        if user_to_follow and follow_username != session['username']:
            if follow_username not in following:
                mongo.db.users.update_one({'username': session['username']},
                                          {'$push': {'following': follow_username}})
                mongo.db.users.update_one({'username': follow_username},
                                          {'$push': {'followers': session['username']}})
                good_message = f'Hai iniziato a seguire {follow_username}.'

            else:
                warning_message = f'Hai già seguito {follow_username}.'
        elif follow_username == session['username']:
            danger_message = 'Non puoi seguire te stesso.'
        else:
            danger_message = f'L\'utente {follow_username} non esiste.'

    user = mongo.db.users.find_one({'username': session['username']})
    updated_following = list(user.get('following', []))
    updated_followers = list(user.get('followers', []))

    # Aggiorna le opzioni per il campo image_choice con le immagini nella cartella predefinita
    images_folder = 'static/profile_images'  # Sostituisci con il percorso reale della tua cartella
    image_choices = [(image, image) for image in os.listdir(images_folder) if image.endswith(('.jpg', '.jpeg', '.png'))]
    profile_image_form.image_choice.choices = image_choices

    if profile_image_form.validate_on_submit():
        # Ottieni il nome del file selezionato dall'utente
        selected_image = profile_image_form.image_choice.data

        # Se l'utente ha effettivamente selezionato un'immagine
        if selected_image:
            # Aggiorna il percorso dell'immagine nel database con il nome dell'immagine selezionata
            mongo.db.users.update_one({'username': session['username']},
                                      {'$set': {'profile_image_path': selected_image}})

    # Assegna direttamente il percorso dell'immagine del profilo alla variabile
    profile_image_path = get_profile_image_path(session['username'])

    return render_template('profile.html', tweets=user_tweets, following=updated_following,
                           followers=updated_followers,
                           profile_image_path=profile_image_path,
                           follow_form=follow_form, tweet_form=tweet_form,
                           unfollow_form=unfollow_form,
                           profile_image_form=profile_image_form,
                           good_message=good_message, warning_message=warning_message, danger_message=danger_message)


@user_profile_blueprint.route('/followers/<username>')
def followers(username):
    # Ottieni la lista dei followers dell'utente specificato dal parametro username
    user = mongo.db.users.find_one({'username': username})

    if user is None:
        # Utente non trovato, puoi gestire questa situazione come preferisci
        return render_template('login.html')

    followers_list = user.get('followers', [])
    return render_template('followers.html', followers_list=followers_list, username=username)


@user_profile_blueprint.route('/following/<username>')
def get_following(username):
    # Ottieni la lista dei following dell'utente specificato dal parametro username
    user = mongo.db.users.find_one({'username': username})

    if user is None:
        # Utente non trovato, puoi gestire questa situazione come preferisci
        return render_template('login.html')

    following_list = user.get('following', [])
    return render_template('following.html', following_list=following_list, username=username)


@user_profile_blueprint.route('/view_profile/<username>')
def view_profile(username):
    # Controlla se l'utente è autenticato
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    # Recupera l'utente della sessione
    current_user = mongo.db.users.find_one({'username': session['username']})

    # Recupera l'utente del profilo
    user = mongo.db.users.find_one({'username': username})

    # Recupera i tweet dell'utente del profilo
    user_tweets = list(mongo.db.tweets.find({'username': username}))

    # Recupera i followers e i following dell'utente del profilo
    followers_list = user.get('followers', [])
    following_list = user.get('following', [])

    # Verifica se l'utente della sessione sta cercando il proprio profilo
    if current_user and current_user['username'] == user['username']:
        # L'utente della sessione sta cercando il proprio profilo
        return redirect(url_for('user_profile.profile'))

    else:
        # L'utente della sessione sta cercando il profilo di un altro utente
        return render_template('user_profile.html', user=user, tweets=user_tweets, followers=followers_list,
                               following=following_list)
