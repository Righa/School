from flask import redirect, request, url_for, render_template, flash
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

## users view

@app.route('/users/view/<id>', methods=['POST', 'GET'])
def view_user(id):
	return render_template('admin/users.html', nav='dash', page='users', action='view')

## users delete

@app.route('/users/delete/<id>', methods=['POST', 'GET'])
def delete_user(id):
	user = User.query.get_or_404(id)
	user.delete()
	db.session.commit()
	flash(f'User has been deleted!', 'success')
	return redirect(url_for('users'))

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

## students view

@app.route('/students/view/<id>', methods=['POST', 'GET'])
def view_student(id):
	return render_template('admin/students.html', nav='dash', page='students', action='view')

## students delete

@app.route('/students/delete/<id>', methods=['POST', 'GET'])
def delete_student(id):
	student = Student.query.get_or_404(id)
	student.delete()
	db.session.commit()
	flash(f'Student has been deleted!', 'success')
	return redirect(url_for('users'))

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

## subjects view

@app.route('/subjects/view/<id>', methods=['POST', 'GET'])
def view_subject(id):
	return render_template('admin/subjects.html', nav='dash', page='subjects', action='view')

## subjects delete

@app.route('/subjects/delete/<id>', methods=['POST', 'GET'])
def delete_subject(id):
	subject = Subject.query.get_or_404(id)
	subject.delete()
	db.session.commit()
	flash(f'Subject has been deleted!', 'success')
	return redirect(url_for('users'))

## categories create

@app.route('/categories/create/<id>', methods=['POST', 'GET'])
def create_category(id):
	subject = Subject.query.get_or_404(id)
	form = CategoryForm()
	if form.validate_on_submit():
		category = Category(name=form.name.data, minimum=form.minimum.data, maximum=form.maximum.data, subject_id=id)
		db.session.add(category)
		db.session.commit()
		flash('Category added successfully', 'success')
	return render_template('admin/categories.html', nav='dash', page='subjects', action='create', form=form)

## categories update

@app.route('/categories/update/<id>', methods=['POST', 'GET'])
def update_category(id):
	category = Category.query.get_or_404(id)
	form = QuestionForm()
	if form.validate_on_submit():
		category.name=form.name.data
		category.minimum=form.minimum.data
		category.maximum=form.maximum.data
		db.session.commit()
		flash('Category updated successfully', 'success')
	elif request.method == 'GET':
		form.name.data=category.name
		form.minimum.data=category.minimum
		form.maximum.data=category.maximum
	return render_template('admin/categories.html', nav='dash', page='subjects', action='update', form=form)

## categories delete

@app.route('/categories/delete/<id>', methods=['POST', 'GET'])
def delete_category(id):
	category = Category.query.get_or_404(id)
	category.delete()
	db.session.commit()
	flash(f'Category has been deleted!', 'success')
	return redirect(url_for('users'))

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
		flash('Exam updated successfully', 'success')
	elif request.method == 'GET':
		form.year.data = exam.year
		form.term.data = exam.term
		form.subject.data = exam.subject
		form.group.data = exam.group
	return render_template('admin/exams.html', nav='dash', page='exams', action='update', form=form)

## exams view

@app.route('/exams/view/<id>', methods=['POST', 'GET'])
def view_exam(id):
	return render_template('admin/exams.html', nav='dash', page='exams', action='view')

## exams delete

@app.route('/exams/delete/<id>', methods=['POST', 'GET'])
def delete_exam(id):
	exam = Exam.query.get_or_404(id)
	exam.delete()
	db.session.commit()
	flash(f'Exam has been deleted!', 'success')
	return redirect(url_for('users'))

## questions create

@app.route('/questions/create/<id>', methods=['POST', 'GET'])
def create_question(id):
	form = QuestionForm()
	exam= Exam.query.get(id)
	subject_id = exam.subject_id
	form.category.query = Category.query.filter(Category.subject_id == subject_id)
	if form.validate_on_submit():
		question = Question(number=form.number.data, category_id=form.category.data.id, exam_id=id)
		db.session.add(question)
		db.session.commit()
		flash('Question added successfully', 'success')
	return render_template('admin/questions.html', nav='dash', page='exams', action='create', form=form)

## questions update

@app.route('/questions/update/<id>', methods=['POST', 'GET'])
def update_question(id):
	question = Question.query.get_or_404(id)
	form = QuestionForm()
	if form.validate_on_submit():
		question.category_id = form.category.data.id
		db.session.commit()
		flash('Question updated successfully', 'success')
	elif request.method == 'GET':
		form.category.data = question.category
		form.exam.data = question.exam
	return render_template('admin/questions.html', nav='dash', page='exams', action='update', form=form)

## questions delete

@app.route('/questions/delete/<id>', methods=['POST', 'GET'])
def delete_question(id):
	question = Question.query.get_or_404(id)
	question.delete()
	db.session.commit()
	flash(f'Question has been deleted!', 'success')
	return redirect(url_for('exams'))

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

## careers view

@app.route('/careers/view/<id>', methods=['POST', 'GET'])
def view_career(id):
	return render_template('admin/careers.html', nav='dash', page='careers', action='view')

## careers delete

@app.route('/careers/delete/<id>', methods=['POST', 'GET'])
def delete_career(id):
	career = Career.query.get_or_404(id)
	career.delete()
	db.session.commit()
	flash(f'Career has been deleted!', 'success')
	return redirect(url_for('careers'))

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

## alumni view

@app.route('/alumni/view/<id>', methods=['POST', 'GET'])
def view_alumni(id):
	return render_template('admin/alumni.html', nav='dash', page='alumni', action='view')

## alumni delete

@app.route('/alumni/delete/<id>', methods=['POST', 'GET'])
def delete_alumni(id):
	alumni = Alumni.query.get_or_404(id)
	alumni.delete()
	db.session.commit()
	flash(f'Alumni has been deleted!', 'success')
	return redirect(url_for('alumni'))
