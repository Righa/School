from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FieldList, HiddenField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange, Optional
from parent.models import *


def group_query():
	return Group.query

def subject_query():
	return Subject.query

def category_query():
	return Category.query


class EditUserForm(FlaskForm):
	first_name = StringField('First Name', validators=[DataRequired(), Length(min=3, max=19)])
	middle_name = StringField('Middle Name', validators=[DataRequired(), Length(min=3, max=19)])
	last_name = StringField('Last Name', validators=[DataRequired(), Length(min=3, max=19)])
	submit = SubmitField('Save')

class EditStudentForm(EditUserForm):
	group = QuerySelectField('Group', query_factory=group_query, allow_blank=False, get_label='name')

class UserForm(EditUserForm):
	email = StringField('Email', validators=[DataRequired(), Email()])

	def validate_email(self, email):

		user = User.query.filter_by(email=email.data).first()
		student = Student.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email has already been taken')
		if student:
			raise ValidationError('Email has already been taken')

class StudentForm(UserForm):
	group = QuerySelectField('Group', query_factory=group_query, allow_blank=False, get_label='year')

class ChangePasswordForm(FlaskForm):
	password = PasswordField('Current Password', validators=[DataRequired()])
	new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8, max=15)])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo(new_password, message='Password should match confirmation'), Length(min=8, max=15)])
	submit = SubmitField('Change Password')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=19)])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class SubjectForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(min=3, max=19)])
	submit = SubmitField('Submit')

class ExamForm(FlaskForm):
	year = IntegerField('Year', validators=[NumberRange(min=2021)])
	term = IntegerField('Term', validators=[NumberRange(min=1, max=3)])
	group = QuerySelectField('Group', query_factory=group_query, allow_blank=False, get_label='year')
	subject = QuerySelectField('Subject', query_factory=subject_query, allow_blank=False, get_label='name')
	submit = SubmitField('Submit')

class GroupForm(FlaskForm):
	year = IntegerField('Year', validators=[NumberRange(min=2021)])
	submit = SubmitField('Submit')

class CategoryForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(min=3, max=19)])
	minimum = IntegerField('Minimum Marks')
	maximum = IntegerField('Maximum Marks', validators=[NumberRange(min=1, max=100)])
	submit = SubmitField('Submit')

class QuestionForm(FlaskForm):
	category = QuerySelectField('Category', query_factory=category_query, allow_blank=False, get_label='name')
	number = IntegerField('Number', validators=[NumberRange(min=1, max=50)])
	submit = SubmitField('Submit')

class ScoreForm(FlaskForm):
	submit = SubmitField('Save')
	
