from flask import redirect, request, url_for, render_template, flash, abort, session
from parent import app, db, bcrypt
from parent.forms import *
from parent.models import *
from statistics import mean
from parent.ml import MLModel
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
import secrets
import json
import os

##landing

@app.route('/')
@app.route('/home')
def home():
	return render_template('index.html', nav='landing')

@app.route('/events')
def events():
	return render_template('events.html', nav='landing')

@app.route('/blogs')
def blogs():
	return render_template('blogs.html', nav='landing')
	
@app.route('/contacts')
def contacts():
	return render_template('contacts.html', nav='landing')

## auth

@app.route('/admin-login', methods=['POST','GET'])
def admin_login():
	next_page=request.args.get('next')
	if current_user.is_authenticated and current_user.utype=='admin':
		return redirect(url_for('admin_dash'))
	if next_page=='/student-dash' or next_page=='/reports' or next_page=='/career':
		return redirect(url_for('student_login', next=next_page))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data) and user.utype=='admin':
			login_user(user, remember=form.remember.data)
			if bcrypt.check_password_hash(user.password, 'welcome'):
				flash(f'Login successful!', 'success')
				flash(f'You are advised to change to your prefered secure password on first login', 'info')
				return redirect(url_for('change_password'))
			flash(f'Login successful!', 'success')
			return redirect(next_page) if next_page else redirect(url_for('admin_dash'))
		else:
			flash(f'Unable to login! Please check your credentials', 'danger')
	return render_template('auth/login.html', type='Admin Login', nav='nonav', form=form)

@app.route('/student-login', methods=['POST','GET'])
def student_login():
	next_page=request.args.get('next')
	if current_user.is_authenticated and current_user.utype=='student':
		return redirect(url_for('student_dash'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data) and user.utype=='student':
			login_user(user, remember=form.remember.data)
			if bcrypt.check_password_hash(user.password, 'welcome'):
				flash(f'Login successful!', 'success')
				flash(f'You are advised to change to your prefered secure password on first login', 'info')
				return redirect(url_for('change_password'))
			flash(f'Login successful!', 'success')
			return redirect(next_page) if next_page else redirect(url_for('student_dash'))
		else:
			flash(f'Unable to login! Please check your credentials', 'danger')
	return render_template('auth/login.html', type='Student Login', nav='nonav', form=form)


@app.route('/change-password', methods=['POST','GET'])
@login_required
def change_password():
	form = ChangePasswordForm()
	if form.validate_on_submit():
		if bcrypt.check_password_hash(current_user.password, form.password.data):
			hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
			current_user.password = hashed_password
			db.session.commit()

			flash(f'Password changed successfully!', 'success')

			if current_user.utype == 'admin':
				return redirect(url_for('admin_dash'))
			elif current_user.utype == 'student':
				return redirect(url_for('student_dash'))
			else:
				return redirect(url_for('home'))
		else:
			flash(f'Your password is wrong!', 'danger')
	return render_template('auth/reset_password.html', type='Change Password', nav='nonav', form=form)

## analytics
@app.route('/admin-dash', methods=['GET'])
@login_required
def admin_dash():
	if current_user.utype != 'admin':
		abort(403)
		
	#create object
	class metrics():
		clean=True

	metrics.num_groups = Group.query.count()
	metrics.num_subjects = Subject.query.count()
	metrics.num_current = Group.query.filter_by(status='ongoing').count()
	metrics.num_graduated = Group.query.filter_by(status='alumni').count()

	groups = Group.query.filter_by(status='ongoing')
	metrics.groups = []
	metrics.num_students = 0

	categories = Category.query.all()

	for group in groups:
		outcomes_total=0
		outcomes_captured=0
		tested=0

		group_size=len(group.students)

		for exam in group.exams:
			outcomes_total += len(exam.questions)*group_size

			for question in exam.questions:
				outcomes_captured += len(question.scores)

		if outcomes_total==0:
			group.outcomes=0
		else:
			group.outcomes = int((outcomes_captured/outcomes_total)*100)

		for category in categories:
			found=0
			for exam in group.exams:
				for question in exam.questions:
					if question.category_id == category.id:
						found += 1
			if found > 0:
				tested += 1

		group.untested = int(((len(categories)-tested)/len(categories))*100)

		metrics.num_students += group_size

		metrics.groups.append(group)

	return render_template('admin/analytics.html', nav='dash', page='analytics', metrics=metrics)

## users create

@app.route('/users/create', methods=['POST', 'GET'])
@login_required
def create_user():
	if current_user.utype != 'admin':
		abort(403)
	form = UserForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash('welcome').decode('utf-8')
		user = User(first_name=form.first_name.data, middle_name=form.middle_name.data, last_name=form.last_name.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Registration successful!', 'success')
		return redirect(url_for('create_user'))
	return render_template('admin/users.html', nav='dash', page='users', action='create', form=form)

## users read

@app.route('/users', methods=['POST', 'GET'])
@login_required
def users():
	if current_user.utype != 'admin':
		abort(403)
	users = User.query.filter_by(utype='admin')
	return render_template('admin/users.html', nav='dash', page='users', users=users, action='read')

## users update

@app.route('/users/update/<id>', methods=['POST', 'GET'])
@login_required
def update_user(id):
	if current_user.utype != 'admin':
		abort(403)
	form = EditUserForm()
	user = User.query.get_or_404(id)
	if form.validate_on_submit():
		user.first_name = form.first_name.data
		user.middle_name = form.middle_name.data
		user.last_name = form.last_name.data
		db.session.commit()
		flash(f'User updated successfully!', 'success')
	elif request.method == 'GET':
		form.first_name.data = user.first_name
		form.middle_name.data = user.middle_name
		form.last_name.data = user.last_name
	return render_template('admin/users.html', nav='dash', page='users', action='update', form=form)

## users update profile

def save_pic(pic):
	rand_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(pic.filename)
	pic_fn = rand_hex + f_ext
	pic_path = os.path.join(app.root_path, 'static/profiles', pic_fn)

	output_size = (133, 133)
	i = Image.open(pic)
	i.thumbnail(output_size)

	i.save(pic_path)
	
	return pic_fn

@app.route('/users/profile/update', methods=['POST', 'GET'])
@login_required
def update_user_profile():
	if current_user.utype != 'admin':
		abort(403)
	form = EditUserForm()
	user = current_user
	if form.validate_on_submit():
		if form.photo.data:
			user.photo = save_pic(form.photo.data)
		user.first_name = form.first_name.data
		user.middle_name = form.middle_name.data
		user.last_name = form.last_name.data
		db.session.commit()
		flash(f'Profile update successful!', 'success')
		return redirect(url_for('update_user_profile'))
	elif request.method == 'GET':
		form.first_name.data = user.first_name
		form.middle_name.data = user.middle_name
		form.last_name.data = user.last_name
	return render_template('admin/users.html', nav='dash', action='profile', form=form)

## users delete

@app.route('/users/delete/<id>', methods=['POST', 'GET'])
@login_required
def delete_user(id):
	if current_user.utype != 'admin':
		abort(403)
	user = User.query.get_or_404(id)
	db.session.delete(user)
	db.session.commit()
	flash(f'User has been deleted!', 'success')
	return redirect(url_for('users'))

## students create

@app.route('/students/create', methods=['POST', 'GET'])
@login_required
def create_student():
	if current_user.utype != 'admin':
		abort(403)
	form = StudentForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash('welcome').decode('utf-8')
		user = User(first_name=form.first_name.data, middle_name=form.middle_name.data, last_name=form.last_name.data, email=form.email.data, utype='student', password=hashed_password)
		db.session.add(user)
		user.student = Student(group_id=form.group.data.id)
		db.session.commit()
		flash(f'Registration successful!', 'success')
		return redirect(url_for('create_student'))
	return render_template('admin/students.html', nav='dash', page='students', action='create', form=form)

## students read

@app.route('/students', methods=['POST', 'GET'])
@login_required
def students():
	if current_user.utype != 'admin':
		abort(403)
	groups = Group.query.filter_by(status='ongoing')
	return render_template('admin/students.html', nav='dash', page='students', groups=groups, action='read')

## students update

@app.route('/students/update/<id>', methods=['POST', 'GET'])
@login_required
def update_student(id):
	if current_user.utype != 'admin':
		abort(403)
	form = EditStudentForm()
	student = User.query.get_or_404(id)
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
@login_required
def delete_student(id):
	if current_user.utype != 'admin':
		abort(403)
	student = Student.query.get_or_404(id)
	db.session.delete(student.user)
	db.session.commit()
	flash(f'Student has been deleted!', 'success')
	return redirect(url_for('students'))

## groups create

@app.route('/groups/create', methods=['POST', 'GET'])
@login_required
def create_group():
	if current_user.utype != 'admin':
		abort(403)
	form = GroupForm()
	if form.validate_on_submit():
		group = Group(year=form.year.data)
		db.session.add(group)
		db.session.commit()
		flash(f'Group created!', 'success')
		return redirect(url_for('create_group'))
	return render_template('admin/groups.html', nav='dash', page='users', action='create', form=form)

## groups delete

@app.route('/groups/delete/<id>', methods=['POST', 'GET'])
@login_required
def delete_group(id):
	if current_user.utype != 'admin':
		abort(403)
	group = Group.query.get_or_404(id)
	db.session.delete(group)
	db.session.commit()
	flash(f'Group and its associated students have been deleted!', 'success')
	return redirect(url_for('students'))

## subjects create

@app.route('/subjects/create', methods=['POST', 'GET'])
@login_required
def create_subject():
	if current_user.utype != 'admin':
		abort(403)
	form = SubjectForm()
	if form.validate_on_submit():
		subject = Subject(name=form.name.data)
		db.session.add(subject)
		db.session.commit()
		flash('Subject added successfully', 'success')
		return redirect(url_for('create_subject'))
	return render_template('admin/subjects.html', nav='dash', page='subjects', action='create', form=form)

## subjects read

@app.route('/subjects', methods=['POST', 'GET'])
@login_required
def subjects():
	if current_user.utype != 'admin':
		abort(403)
	subjects = Subject.query.all()
	return render_template('admin/subjects.html', nav='dash', page='subjects', subjects=subjects, action='read')

## subjects update

@app.route('/subjects/update/<id>', methods=['POST', 'GET'])
@login_required
def update_subject(id):
	if current_user.utype != 'admin':
		abort(403)
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
@login_required
def view_subject(id):
	if current_user.utype != 'admin':
		abort(403)
	subject = Subject.query.get_or_404(id)
	return render_template('admin/subjects.html', nav='dash', page='subjects', action='view', subject=subject)

## subjects delete

@app.route('/subjects/delete/<id>', methods=['POST', 'GET'])
@login_required
def delete_subject(id):
	if current_user.utype != 'admin':
		abort(403)
	subject = Subject.query.get_or_404(id)
	db.session.delete(subject)
	db.session.commit()
	flash(f'Subject has been deleted!', 'success')
	return redirect(url_for('subjects'))

## categories create

@app.route('/categories/create/<id>', methods=['POST', 'GET'])
@login_required
def create_category(id):
	if current_user.utype != 'admin':
		abort(403)
	subject = Subject.query.get_or_404(id)
	form = CategoryForm()
	if form.validate_on_submit():
		category = Category(name=form.name.data, minimum=form.minimum.data, maximum=form.maximum.data, subject_id=id)
		db.session.add(category)
		db.session.commit()
		flash('Category added successfully', 'success')
		return redirect(url_for('view_subject', id=id))
	return render_template('admin/categories.html', nav='dash', page='subjects', action='create', form=form)

## categories update

@app.route('/categories/update/<id>', methods=['POST', 'GET'])
@login_required
def update_category(id):
	if current_user.utype != 'admin':
		abort(403)
	category = Category.query.get_or_404(id)
	form = CategoryForm()

	if form.validate_on_submit():
		category.name=form.name.data
		category.minimum=form.minimum.data
		category.maximum=form.maximum.data
		db.session.commit()
		flash('Category updated successfully', 'success')
		return redirect(url_for('view_subject', id=category.subject_id))
	elif request.method == 'GET':
		form.name.data=category.name
		form.minimum.data=category.minimum
		form.maximum.data=category.maximum
	return render_template('admin/categories.html', nav='dash', page='subjects', action='update', form=form)

## categories delete

@app.route('/categories/delete/<id>', methods=['POST', 'GET'])
@login_required
def delete_category(id):
	if current_user.utype != 'admin':
		abort(403)
	category = Category.query.get_or_404(id)
	db.session.delete(category)
	db.session.commit()
	flash(f'Category has been deleted!', 'success')
	return redirect(url_for('subjects'))

## exams create

@app.route('/exams/create', methods=['POST', 'GET'])
@login_required
def create_exam():
	if current_user.utype != 'admin':
		abort(403)
	form = ExamForm()
	if form.validate_on_submit():
		exam = Exam(year=form.year.data, term=form.term.data, user_id=1, subject_id=form.subject.data.id, group_id=form.group.data.id)
		db.session.add(exam)
		db.session.commit()
		flash('Exam added successfully', 'success')
		return redirect(url_for('create_exam'))
	return render_template('admin/exams.html', nav='dash', page='exams', action='create', form=form)

## exams read

@app.route('/exams', methods=['POST', 'GET'])
@login_required
def exams():
	if current_user.utype != 'admin':
		abort(403)
	groups = Group.query.filter_by(status='ongoing')
	return render_template('admin/exams.html', nav='dash', groups=groups, page='exams', action='read')

## exams update

@app.route('/exams/update/<id>', methods=['POST', 'GET'])
@login_required
def update_exam(id):
	if current_user.utype != 'admin':
		abort(403)
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
@login_required
def view_exam(id):
	if current_user.utype != 'admin':
		abort(403)
	exam = Exam.query.get_or_404(id)
	return render_template('admin/exams.html', nav='dash', page='exams', action='view', exam=exam)

## exams delete

@app.route('/exams/delete/<id>', methods=['POST', 'GET'])
@login_required
def delete_exam(id):
	if current_user.utype != 'admin':
		abort(403)
	exam = Exam.query.get_or_404(id)
	db.session.delete(exam)
	db.session.commit()
	flash(f'Exam has been deleted!', 'success')
	return redirect(url_for('exams'))

## questions create

@app.route('/questions/create/<id>', methods=['POST', 'GET'])
@login_required
def create_question(id):
	if current_user.utype != 'admin':
		abort(403)
	form = QuestionForm()
	exam= Exam.query.get(id)
	subject_id = exam.subject_id
	form.category.query = Category.query.filter(Category.subject_id == subject_id)
	if form.validate_on_submit():
		question = Question(number=form.number.data, category_id=form.category.data.id, exam_id=id)
		db.session.add(question)
		db.session.commit()
		flash('Question added successfully', 'success')
		return redirect(url_for('view_exam', id=id))
	return render_template('admin/questions.html', nav='dash', page='exams', action='create', form=form)

## questions update

@app.route('/questions/update/<id>', methods=['POST', 'GET'])
@login_required
def update_question(id):
	if current_user.utype != 'admin':
		abort(403)
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
@login_required
def delete_question(id):
	if current_user.utype != 'admin':
		abort(403)
	question = Question.query.get_or_404(id)
	exam_id = question.exam_id
	db.session.delete(question)
	db.session.commit()
	flash(f'Question has been deleted!', 'success')
	return redirect(url_for('view_exam', id=exam_id))

## scores create

@app.route('/scores/create/<id>', methods=['POST', 'GET'])
@login_required
def create_score(id):
	if current_user.utype != 'admin':
		abort(403)
	exam= Exam.query.get_or_404(id)
	form = ScoreForm()
			
	if request.method == 'POST':
		student_id = request.form['student_id']

		for question in exam.questions:
			if Score.query.filter_by(question_id=question.id, student_id=student_id).first():
				score = Score.query.filter_by(question_id=question.id, student_id=student_id).first()
				score.value=request.form['score['+str(question.number)+']']
				db.session.commit()
			else:
				score = Score(value=request.form['score['+str(question.number)+']'], question_id=question.id, student_id=student_id)
				db.session.add(score)
				db.session.commit()
		flash('Scores have been captured successfully', 'success')
		return redirect(url_for('create_score', id=id))
	return render_template('admin/scores.html', nav='dash', page='exams', action='create', exam=exam, form=form)

## careers create

@app.route('/careers/create/<id>', methods=['POST', 'GET'])
@login_required
def create_careers(id):
	if current_user.utype != 'admin':
		abort(403)
	group = Group.query.get_or_404(id)

	for student in group.students:
		allscores=[]
		for subject in Subject.query.all():
			for category in subject.categories:
				scores=[]
				for question in category.questions:
					for score in Score.query.filter_by(student_id=student.id, question_id=question.id):
						scores.append(score.value)

				if len(scores)>0:
					value=mean(scores)/category.maximum
					allscores.append(value)
					analytics = Analytics(student_id=student.id, category_id=category.id, value=value)
					db.session.add(analytics)
				else:
					flash(category.subject.name + ' ' + category.name + ' is Missing', 'danger')
					return redirect(url_for('careers'))

		#ML application
		if len(allscores) == 23:
			predictions = MLModel.generateSingle(allscores)
			career = Career(student_id=student.id, profession1=predictions[0], profession2=predictions[1], profession3=predictions[2])
			db.session.add(career)
		else:
			flash('Failed! Some strands are missing', 'danger')
			return redirect(url_for('careers'))

		db.session.commit()
	return redirect(url_for('view_careers', id=id))

## careers read

@app.route('/careers', methods=['POST', 'GET'])
@login_required
def careers():
	if current_user.utype != 'admin':
		abort(403)
	groups = Group.query.filter_by(status='ongoing')
	alumni = Group.query.filter_by(status='alumni')
	return render_template('admin/careers.html', nav='dash', page='careers', action='read', groups=groups, alumni=alumni)

## careers view

@app.route('/careers/view/<id>', methods=['POST', 'GET'])
@login_required
def view_careers(id):
	if current_user.utype != 'admin':
		abort(403)
	group = Group.query.get_or_404(id)
	subjects = Subject.query.all()
	return render_template('admin/careers.html', nav='dash', page='careers', action='view', subjects=subjects, group=group)

## careers recreate

@app.route('/careers/recreate/<id>', methods=['POST', 'GET'])
@login_required
def recreate_careers(id):
	if current_user.utype != 'admin':
		abort(403)
	group = Group.query.get_or_404(id)

	return render_template('admin/careers.html', nav='dash', page='careers', action='create')

## careers update

@app.route('/careers/update/<id>', methods=['POST', 'GET'])
@login_required
def create_career(id):
	if current_user.utype != 'admin':
		abort(403)
	career = Career.query.get_or_404(id)

	return render_template('admin/careers.html', nav='dash', page='careers', action='create')

## careers delete

@app.route('/careers/delete/<id>', methods=['POST', 'GET'])
@login_required
def delete_career(id):
	if current_user.utype != 'admin':
		abort(403)
	career = Career.query.get_or_404(id)
	db.session.delete(career)
	db.session.commit()
	flash(f'Career has been deleted!', 'success')
	return redirect(url_for('careers'))

## alumni create

@app.route('/alumni/create/<id>', methods=['POST', 'GET'])
@login_required
def create_alumni(id):
	if current_user.utype != 'admin':
		abort(403)
	group = Group.query.get_or_404(id)
	group.status = 'alumni'
	db.session.commit()
	flash(f'Group has been passed out!', 'success')
	return redirect(url_for('careers'))

## alumni read

@app.route('/alumni', methods=['POST', 'GET'])
@login_required
def alumni():
	if current_user.utype != 'admin':
		abort(403)
	groups = Group.query.filter_by(status='alumni')
	return render_template('admin/alumni.html', nav='dash', page='alumni', action='read', groups=groups)




## student analytics

@app.route('/student-dash', methods=['GET'])
@login_required
def student_dash():
	if current_user.utype != 'student':
		abort(403)
		
	#create object
	class metrics():
		clean=True
	categories = Category.query.all()

	group = current_user.student.group

	outcomes_total=0
	outcomes_captured=0
	tested=0

	group_size=len(group.students)

	for exam in group.exams:
		outcomes_total += len(exam.questions)*group_size

		for question in exam.questions:
			outcomes_captured += len(question.scores)

	if outcomes_total==0:
		group.outcomes=0
	else:
		group.outcomes = int((outcomes_captured/outcomes_total)*100)

	for category in categories:
		found=0
		for exam in group.exams:
			for question in exam.questions:
				if question.category_id == category.id:
					found += 1
		if found > 0:
			tested += 1

	group.untested = int(((len(categories)-tested)/len(categories))*100)

	metrics.outcomes = group.outcomes
	metrics.untested = group.untested


	return render_template('student/analytics.html', nav='dash', page='analytics', metrics=metrics)

## student reports

@app.route('/reports', methods=['GET'])
@login_required
def student_reports():
	if current_user.utype != 'student':
		abort(403)
	return render_template('student/reports.html', nav='dash', page='reports')

## student careers

@app.route('/career', methods=['GET'])
@login_required
def student_careers():
	if current_user.utype != 'student':
		abort(403)
	return render_template('student/careers.html', nav='dash', page='careers')


@app.route('/student/profile/update', methods=['POST', 'GET'])
@login_required
def update_student_profile():
	if current_user.utype != 'student':
		abort(403)
	form = EditUserForm()
	if form.validate_on_submit():
		if form.photo.data:
			current_user.photo = save_pic(form.photo.data)
		current_user.first_name = form.first_name.data
		current_user.middle_name = form.middle_name.data
		current_user.last_name = form.last_name.data
		db.session.commit()
		flash(f'Profile update successful!', 'success')
		return redirect(url_for('update_student_profile'))
	elif request.method == 'GET':
		form.first_name.data = current_user.first_name
		form.middle_name.data = current_user.middle_name
		form.last_name.data = current_user.last_name
	return render_template('student/profile.html', nav='dash', form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('home'))




