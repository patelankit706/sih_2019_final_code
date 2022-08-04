from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from datetime import datetime
from flaskblog.models import User


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class LabsReport(FlaskForm):
    uID=StringField('Unique ID',validators=[DataRequired(), Length(min=4, max=50)])
    grossCalorificValue= FloatField(" Gross Calorific Value ",validators=[DataRequired()])
    netCalorificValue= FloatField(" Net Calorific Value ",validators=[DataRequired()])
    submit= SubmitField(' Submit ')


class GenerateUID(FlaskForm):
    bID =StringField('Enter BuyerID',validators=[DataRequired(), Length(min=4, max=50)])
    submit= SubmitField(' Generate UID ')

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enter details')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class GenerateForm(FlaskForm):
    uID =StringField('Enter UID',validators=[DataRequired(), Length(min=4, max=50)])
    submit= SubmitField(' Fill Form ')
