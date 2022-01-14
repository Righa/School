from flask import redirect, request, url_for, render_template, flash
from parent import app, db, bcrypt
from parent.forms import *
from parent.models import *

##landing

@app.route('/')
@app.route('/home')
def home():
	return render_template('index.html', nav='landing')

#@app.route('/home/<dt>')
#def home(dt):
	#User.query.filter_by/filter(x>y)
	#return render_template('index.html', nav='landing')

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

@app.route('/users/update/<id>', methods=['POST', 'GET'])
def update_user(id):
	form = EditUserForm()
	user = User.query.get_or_404(id)
	if form.validate_on_submit():
		user.first_name = form.first_name.data
		user.middle_name = form.middle_name.data
		user.last_name = form.last_name.data
		db.session.commit()
		flash(f'Profile update successful!', 'success')
	elif request.method == 'GET':
		form.first_name.data = user.first_name
		form.middle_name.data = user.middle_name
		form.last_name.data = user.last_name
	return render_template('admin/users.html', nav='dash', page='users', action='update', form=form)

## users delete

@app.route('/users/delete/<id>', methods=['POST', 'GET'])
def delete_user(id):
	return render_template('admin/users.html', nav='dash', page='users', action='delete')

## students create

@app.route('/students/create', methods=['POST', 'GET'])
def create_student():
	form = StudentForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash('welcome').decode('utf-8')
		student = Student(first_name=form.first_name.data, middle_name=form.middle_name.data, last_name=form.last_name.data, email=form.email.data, group_id=form.group.data.id, password=hashed_password)
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

@app.route('/students/update/<id>', methods=['POST', 'GET'])
def update_student(id):
	form = EditStudentForm()
	student = Student.query.get_or_404(id)
	if form.validate_on_submit():
		student.first_name = form.first_name.data
		student.middle_name = form.middle_name.data
		student.last_name = form.last_name.data
		student.group_id = form.group.data.id
		db.session.commit()
		flash(f'Profile update successful!', 'success')
	elif request.method == 'GET':
		form.first_name.data = student.first_name
		form.middle_name.data = student.middle_name
		form.last_name.data = student.last_name
		form.group.data = student.group
	return render_template('admin/students.html', nav='dash', page='students', action='update', form=form)

## students delete

@app.route('/students/delete/<id>', methods=['POST', 'GET'])
def delete_student(id):
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

@app.route('/subjects/update/<id>', methods=['POST', 'GET'])
def update_subject(id):
	form = SubjectForm()
	subject = Subject.query.get_or_404(id)
	if form.validate_on_submit():
		subject.name = form.name.data
		db.session.commit()
		flash('Subject edited successfully', 'success')
	elif request.method == 'GET':
		form.name.data = subject.name
	return render_template('admin/subjects.html', nav='dash', page='subjects', action='update', form=form)

## subjects delete

@app.route('/subjects/delete/<id>', methods=['POST', 'GET'])
def delete_subject(id):
	return render_template('admin/subjects.html', nav='dash', page='subjects', action='delete')

## exams create

@app.route('/exams/create', methods=['POST', 'GET'])
def create_exam():
	form = ExamForm()
	if form.validate_on_submit():
		exam = Exam(year=form.year.data, term=form.term.data, subject_id=form.subject.data.id, group_id=form.group.data.id)
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

@app.route('/exams/update/<id>', methods=['POST', 'GET'])
def update_exam(id):
	form = ExamForm()
	exam = Exam.query.get_or_404(id)
	if form.validate_on_submit():
		exam.year = form.year.data
		exam.term = form.term.data
		exam.subject_id = form.subject.data.id
		exam.group_id = form.group.data.id
		db.session.commit()
		flash('Exam added successfully', 'success')
	elif request.method == 'GET':
		form.year.data = exam.year
		form.term.data = exam.term
		form.subject.data = exam.subject
		form.group.data = exam.group
	return render_template('admin/exams.html', nav='dash', page='exams', action='update', form=form)

## exams delete

@app.route('/exams/delete/<id>', methods=['POST', 'GET'])
def delete_exam(id):
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

@app.route('/careers/update/<id>', methods=['POST', 'GET'])
def update_career(id):
	return render_template('admin/careers.html', nav='dash', page='careers', action='update')

## careers delete

@app.route('/careers/delete/<id>', methods=['POST', 'GET'])
def delete_career(id):
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

@app.route('/alumni/update/<id>', methods=['POST', 'GET'])
def update_alumni(id):
	return render_template('admin/alumni.html', nav='dash', page='alumni', action='update')

## alumni delete

@app.route('/alumni/delete/<id>', methods=['POST', 'GET'])
def delete_alumni(id):
	return render_template('admin/alumni.html', nav='dash', page='alumni', action='delete')
