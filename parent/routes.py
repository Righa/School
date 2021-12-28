from flask import redirect, url_for, render_template, flash
from parent import app
from parent.forms import LoginForm
from parent.models import User



@app.route('/')
@app.route('/home')
def home():
	return render_template('index.html', nav='landing')

@app.route('/admin-login', methods=['POST','GET'])
def admin_login():
	form = LoginForm()
	if form.validate_on_submit():
		flash(f'Login successful!', 'success')
		return redirect(url_for('admin_dash'))
	return render_template('login.html', type='Admin Login', nav='nonav', form=form)

@app.route('/student-login', methods=['POST','GET'])
def student_login():
	form = LoginForm()
	if form.validate_on_submit():
		flash(f'Login successful!', 'success')
		return redirect(url_for('student_dash'))
	return render_template('login.html', type='Student Login', nav='nonav', form=form)


@app.route('/admin-dash', methods=['GET'])
def admin_dash():
	return render_template('admin-dash.html', nav='dash')


@app.route('/student-dash', methods=['GET'])
def student_dash():
	return render_template('student-dash.html', nav='dash')


