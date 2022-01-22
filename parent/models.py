from datetime import datetime
from parent import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(19), nullable=False)
	middle_name = db.Column(db.String(19), nullable=False)
	last_name = db.Column(db.String(19), nullable=False)
	email = db.Column(db.String(19), unique=True, nullable=False)
	exams = db.relationship('Exam', backref='teacher', lazy=True, cascade='all, delete')
	password = db.Column(db.String(119), nullable=False)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)

	def __repr__(self):
		return f"User('{self.id}', '{self.first_name}', '{self.middle_name}', '{self.last_name}', '{self.email}')"

class Group(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	year = db.Column(db.String(19), nullable=False)
	students = db.relationship('Student', backref='group', lazy=True, cascade='all, delete')
	status = db.Column(db.String(19), nullable=False, default='ongoing')
	exams = db.relationship('Exam', backref='group', lazy=True, cascade='all, delete')
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)

	def __repr__(self):
		return f"Group('{self.name}')"

class Subject(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(19), nullable=False)
	categories = db.relationship('Category', backref='subject', lazy=True, cascade='all, delete')
	exams = db.relationship('Exam', backref='subject', lazy=True, cascade='all, delete')
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)

	def __repr__(self):
		return f"Subject('{self.name}')"

class Student(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(19), nullable=False)
	middle_name = db.Column(db.String(19), nullable=False)
	last_name = db.Column(db.String(19), nullable=False)
	email = db.Column(db.String(19), unique=True, nullable=False)
	scores = db.relationship('Score', backref='student', lazy=True, cascade='all, delete')
	analytics = db.relationship('Analytics', backref='student', lazy=True, cascade='all, delete')
	career = db.relationship('Career', backref='student', uselist=False, lazy=True, cascade='all, delete')
	group_id = db.Column(db.Integer, db.ForeignKey('group.id', ondelete='CASCADE'), nullable=False)
	password = db.Column(db.String(119), nullable=False)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)

	

	def __repr__(self):
		return f"Student('{self.first_name}', '{self.middle_name}', '{self.last_name}', '{self.email}')"

class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(19), nullable=False)
	minimum = db.Column(db.Integer, nullable=False)
	maximum = db.Column(db.Integer, nullable=False)
	analytics = db.relationship('Analytics', backref='category', lazy=True, cascade='all, delete')
	questions = db.relationship('Question', backref='category', lazy=True, cascade='all, delete')
	subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)

	def __repr__(self):
		return f"Category('{self.name}', '{self.maximum}', '{self.minimum}')"

class Exam(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	year = db.Column(db.Integer, nullable=False)
	term = db.Column(db.Integer, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
	group_id = db.Column(db.Integer, db.ForeignKey('group.id', ondelete='CASCADE'), nullable=False)
	subject_id = db.Column(db.Integer, db.ForeignKey('subject.id', ondelete='CASCADE'), nullable=False)
	questions = db.relationship('Question', backref='exam', lazy=True, cascade='all, delete')
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)

	def __repr__(self):
		return f"Exam('{self.year}', '{self.term}')"

class Question(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	number = db.Column(db.Integer, nullable=False)
	category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='CASCADE'), nullable=False)
	exam_id = db.Column(db.Integer, db.ForeignKey('exam.id', ondelete='CASCADE'), nullable=False)
	scores = db.relationship('Score', backref='question', lazy=True, cascade='all, delete')
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)

	def __repr__(self):
		return f"Question('{self.number}')"

class Score(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	value = db.Column(db.Integer, nullable=False)
	question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable=False)
	student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete='CASCADE'), nullable=False)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)

	def __repr__(self):
		return f"Score('{self.value}')"

class Analytics(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	student_id = db.Column(db.Float, db.ForeignKey('student.id', ondelete='CASCADE'), nullable=False)
	category_id = db.Column(db.Float, db.ForeignKey('category.id', ondelete='CASCADE'), nullable=False)
	value = db.Column(db.Integer, nullable=False)

class Career(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	student_id = db.Column(db.Float, db.ForeignKey('student.id', ondelete='CASCADE'), nullable=False)
	profession1 = db.Column(db.String(44), nullable=True)
	profession2 = db.Column(db.String(44), nullable=True)
	profession3 = db.Column(db.String(44), nullable=True)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)

	def __repr__(self):
		return f"Career('{self.english_writing}', '{self.english_reading}', '{self.english_language}', '{self.science_state}', '{self.science_outline}', '{self.science_application}', '{self.science_attitude}', '{self.re_outline}', '{self.re_state}', '{self.re_application}', '{self.re_attitude}', '{self.agriculture_state}', '{self.agriculture_outline}', '{self.agriculture_application}', '{self.agriculture_attitude}', '{self.ss_state}', '{self.ss_outline}', '{self.ss_aplication}', '{self.ss_attitude}', '{self.math}', '{self.home_science}', '{self.creative_arts}', '{self.physical_and_health_education}', '{self.profession1}', '{self.profession2}', '{self.profession3}')"

