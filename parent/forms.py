from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from parent.models import *


def group_query():
	return Group.query


class UserForm(FlaskForm):
	first_name = StringField('First Name', validators=[DataRequired(), Length(min=3, max=19)])
	middle_name = StringField('Middle Name', validators=[DataRequired(), Length(min=3, max=19)])
	last_name = StringField('Last Name', validators=[DataRequired(), Length(min=3, max=19)])
	email = StringField('Email', validators=[DataRequired(), Email()])

	def validate_email(self, email):

		user = User.query.filter_by(email=email.data).first()
		student = Student.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email has already been taken')
		if student:
			raise ValidationError('Email has already been taken')
	submit = SubmitField('Register')

class StudentForm(FlaskForm):
	first_name = StringField('First Name', validators=[DataRequired(), Length(min=3, max=19)])
	middle_name = StringField('Middle Name', validators=[DataRequired(), Length(min=3, max=19)])
	last_name = StringField('Last Name', validators=[DataRequired(), Length(min=3, max=19)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	group = QuerySelectField('Group', query_factory=group_query, allow_blank=False, get_label='name')

	def validate_email(self, email):

		user = User.query.filter_by(email=email.data).first()
		student = Student.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email has already been taken')
		if student:
			raise ValidationError('Email has already been taken')
	submit = SubmitField('Register')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=19)])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Sign In')


class SubjectForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(min=3, max=19)])
	submit = SubmitField('Submit')

class ExamForm(FlaskForm):
	year = StringField('Year', validators=[DataRequired(), Length(min=3, max=19)])
	term = StringField('Term', validators=[DataRequired(), Length(min=1, max=19)])
	submit = SubmitField('Submit')

class GroupForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(min=3, max=19)])
	submit = SubmitField('Submit')

class CategoryForm(FlaskForm):
	name = StringField('First Name', validators=[DataRequired(), Length(min=3, max=19)])
	minimum = StringField('Maximum Marks', validators=[DataRequired(), Length(min=3, max=19)])
	maximum = StringField('Minimum Marks', validators=[DataRequired(), Length(min=3, max=19)])
	submit = SubmitField('Submit')

class QuestionForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(min=3, max=19)])
	submit = SubmitField('Submit')

class ScoreForm(FlaskForm):
	value = StringField('Value', validators=[DataRequired(), Length(min=3, max=19)])
	submit = SubmitField('Submit')
	
