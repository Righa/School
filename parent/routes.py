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
		return redirect(url_for('home'))
	return render_template('login.html', type='Admin Login', nav='nonav', form=form)

@app.route('/student-login', methods=['POST','GET'])
def student_login():
	form = LoginForm()
	return render_template('login.html', type='Student Login', nav='nonav', form=form)





