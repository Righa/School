from flask import redirect, url_for, render_template, flash
from parent import app, db, bcrypt
from parent.forms import *
from parent.models import *

##landing

@app.route('/')
@app.route('/home')
def home():
	return render_template('index.html', nav='landing')

## auth

@app.route('/admin-login', methods=['POST','GET'])
def admin_login():
	form = LoginForm()
	if form.validate_on_submit():
		flash(f'Login successful!', 'success')
		return redirect(url_for('admin_dash'))
	return render_template('auth/login.html', type='Admin Login', nav='nonav', form=form)

@app.route('/student-login', methods=['POST','GET'])
def student_login():
	form = LoginForm()
	if form.validate_on_submit():
		flash(f'Login successful!', 'success')
		return redirect(url_for('student_dash'))
	return render_template('auth/login.html', type='Student Login', nav='nonav', form=form)

## analytics

@app.route('/admin-dash', methods=['GET'])
def admin_dash():
	return render_template('admin/analytics.html', nav='dash', page='analytics')


@app.route('/student-dash', methods=['GET'])
def student_dash():
	return render_template('student/analytics.html', nav='dash', page='analytics')

## users create

@app.route('/users/create', methods=['POST', 'GET'])
def create_user():
	form = UserForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash('welcome').decode('utf-8')
		user = User(first_name=form.first_name.data, middle_name=form.middle_name.data, last_name=form.last_name.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Registration successful!', 'success')
	return render_template('admin/users.html', nav='dash', page='users', action='create', form=form)

## groups create

@app.route('/groups/create', methods=['POST', 'GET'])
def create_group():
	form = GroupForm()
	if form.validate_on_submit():
		group = Group(name=form.name.data)
		db.session.add(group)
		db.session.commit()
		flash(f'Group created!', 'success')
	return render_template('admin/groups.html', nav='dash', page='users', action='create', form=form)

## users read

@app.route('/users', methods=['POST', 'GET'])
def users():
	users = User.query.all()
	return render_template('admin/users.html', nav='dash', page='users', users=users, action='read')

## users update

@app.route('/users/update', methods=['POST', 'GET'])
def update_user():
	return render_template('admin/users.html', nav='dash', page='users', action='update')

## users delete

@app.route('/users/delete', methods=['POST', 'GET'])
def delete_user():
	return render_template('admin/users.html', nav='dash', page='users', action='delete')

## students create

@app.route('/students/create', methods=['POST', 'GET'])
def create_student():
	form = StudentForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash('welcome').decode('utf-8')
		student = Student(first_name=form.first_name.data, middle_name=form.middle_name.data, last_name=form.last_name.data, email=form.email.data, group_id=1, password=hashed_password)
		db.session.add(student)
		db.session.commit()
		flash(f'Registration successful!', 'success')
	return render_template('admin/students.html', nav='dash', page='students', action='create', form=form)

## students read

@app.route('/students', methods=['POST', 'GET'])
def students():
	students = Student.query.all()
	return render_template('admin/students.html', nav='dash', page='students', students=students, action='read')

## students update

@app.route('/students/update', methods=['POST', 'GET'])
def update_student():
	return render_template('admin/students.html', nav='dash', page='students', action='update')

## students delete

@app.route('/students/delete', methods=['POST', 'GET'])
def delete_student():
	return render_template('admin/students.html', nav='dash', page='students', action='delete')

## subjects create

@app.route('/subjects/create', methods=['POST', 'GET'])
def create_subject():
	form = SubjectForm()
	if form.validate_on_submit():
		subject = Subject(name=form.name.data)
		db.session.add(subject)
		db.session.commit()
		flash('Subject added successfully', 'success')
	return render_template('admin/subjects.html', nav='dash', page='subjects', action='create', form=form)

## subjects read

@app.route('/subjects', methods=['POST', 'GET'])
def subjects():
	subjects = Subject.query.all()
	return render_template('admin/subjects.html', nav='dash', page='subjects', subjects=subjects, action='read')

## subjects update

@app.route('/subjects/update', methods=['POST', 'GET'])
def update_subject():
	return render_template('admin/subjects.html', nav='dash', page='subjects', action='update')

## subjects delete

@app.route('/subjects/delete', methods=['POST', 'GET'])
def delete_subject():
	return render_template('admin/subjects.html', nav='dash', page='subjects', action='delete')

## exams create

@app.route('/exams/create', methods=['POST', 'GET'])
def create_exam():
	form = ExamForm()
	if form.validate_on_submit():
		exam = Exam(year=form.year.data, term=form.term.data, subject_id=1, group_id=1)
		db.session.add(exam)
		db.session.commit()
		flash('Exam added successfully', 'success')
	return render_template('admin/exams.html', nav='dash', page='exams', action='create', form=form)

## exams read

@app.route('/exams', methods=['POST', 'GET'])
def exams():
	exams = Exam.query.all()
	return render_template('admin/exams.html', nav='dash', exams=exams, page='exams', action='read')

## exams update

@app.route('/exams/update', methods=['POST', 'GET'])
def update_exams():
	return render_template('admin/exams.html', nav='dash', page='exams', action='update')

## exams delete

@app.route('/exams/delete', methods=['POST', 'GET'])
def delete_exams():
	return render_template('admin/exams.html', nav='dash', page='exams', action='delete')

## careers create

@app.route('/careers/create', methods=['POST', 'GET'])
def create_career():
	return render_template('admin/careers.html', nav='dash', page='careers', action='create')

## careers read

@app.route('/careers', methods=['POST', 'GET'])
def careers():
	return render_template('admin/careers.html', nav='dash', page='careers', action='read')

## careers update

@app.route('/careers/update', methods=['POST', 'GET'])
def update_career():
	return render_template('admin/careers.html', nav='dash', page='careers', action='update')

## careers delete

@app.route('/careers/delete', methods=['POST', 'GET'])
def delete_career():
	return render_template('admin/careers.html', nav='dash', page='careers', action='delete')

## alumni create

@app.route('/alumni/create', methods=['POST', 'GET'])
def create_alumni():
	return render_template('admin/alumni.html', nav='dash', page='alumni', action='create')

## alumni read

@app.route('/alumni', methods=['POST', 'GET'])
def alumni():
	return render_template('admin/alumni.html', nav='dash', page='alumni', action='read')

## alumni update

@app.route('/alumni/update', methods=['POST', 'GET'])
def update_alumni():
	return render_template('admin/alumni.html', nav='dash', page='alumni', action='update')

## alumni delete

@app.route('/alumni/delete', methods=['POST', 'GET'])
def delete_alumni():
	return render_template('admin/alumni.html', nav='dash', page='alumni', action='delete')
