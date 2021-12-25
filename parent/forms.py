from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=3, max=19)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=19)])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

	submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=19)])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Sign In')
