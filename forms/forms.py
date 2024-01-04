# forms/forms.py
from datetime import date

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class TweetForm(FlaskForm):
    tweet_content = TextAreaField('Tweet', validators=[DataRequired()])
    submit = SubmitField('Invia Tweet')


class ProfileImageForm(FlaskForm):
    image_choice = SelectField('Choose Profile Image', choices=[], coerce=str)
    submit = SubmitField('Upload')


class SearchForm(FlaskForm):
    search_query = StringField('Cerca utente', validators=[DataRequired()])
    submit = SubmitField('Cerca')


class UnfollowForm(FlaskForm):
    unfollow_username = StringField('', validators=[DataRequired()])
    submit = SubmitField('Unfollow')


class FollowForm(FlaskForm):
    follow_username = StringField('', validators=[DataRequired()])
    submit = SubmitField('Follow')


class RegistrationForm(FlaskForm):
    first_name = StringField('Nome', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Cognome', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Conferma Password', validators=[DataRequired(), EqualTo('password')])
    birth_date = StringField('Data di Nascita (DD-MM-YYYY)', validators=[DataRequired()])

    # Campo di submit aggiunto
    submit = SubmitField('Registrati')

    def validate_birth_date(self, field):
        from datetime import datetime
        today = date.today()
        age_limit_date = today.replace(year=today.year - 18)

        # Converti la stringa della data in un oggetto datetime.date
        birth_date = datetime.strptime(field.data, '%d-%m-%Y').date()

        if birth_date > age_limit_date:
            raise ValidationError('Devi essere maggiorenne per registrarti.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
