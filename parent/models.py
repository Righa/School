from datetime import datetime
from parent import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(19), nullable=False)
	middle_name = db.Column(db.String(19), nullable=False)
	last_name = db.Column(db.String(19), nullable=False)
	email = db.Column(db.String(19), unique=True, nullable=False)
	password = db.Column(db.String(119), nullable=False)

	def __repr__(self):
		return f"User('{self.id}', '{self.first_name}', '{self.middle_name}', '{self.last_name}', '{self.email}')"

class Group(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(19), nullable=False)
	students = db.relationship('Student', backref='group', lazy=True)
	exams = db.relationship('Exam', backref='group', lazy=True)

	def __repr__(self):
		return f"Group('{self.name}')"

class Subject(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(19), nullable=False)
	categories = db.relationship('Category', backref='subject', lazy=True)
	exams = db.relationship('Exam', backref='subject', lazy=True)

	def __repr__(self):
		return f"Subject('{self.name}')"

class Student(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(19), nullable=False)
	middle_name = db.Column(db.String(19), nullable=False)
	last_name = db.Column(db.String(19), nullable=False)
	email = db.Column(db.String(19), unique=True, nullable=False)
	scores = db.relationship('Score', backref='student', lazy=True)
	careers = db.relationship('Career', backref='student', lazy=True)
	group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
	password = db.Column(db.String(119), nullable=False)

	

	def __repr__(self):
		return f"Student('{self.first_name}', '{self.middle_name}', '{self.last_name}', '{self.email}')"

class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(19), nullable=False)
	minimum = db.Column(db.Integer, nullable=False)
	maximum = db.Column(db.Integer, nullable=False)
	questions = db.relationship('Question', backref='category', lazy=True)
	subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)

	def __repr__(self):
		return f"Category('{self.name}', '{self.maximum}', '{self.minimum}')"

class Exam(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	year = db.Column(db.Integer, nullable=False)
	term = db.Column(db.Integer, nullable=False)
	group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
	subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
	questions = db.relationship('Question', backref='exam', lazy=True)

	def __repr__(self):
		return f"Exam('{self.year}', '{self.term}')"

class Question(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
	exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)
	scores = db.relationship('Score', backref='question', lazy=True)

	def __repr__(self):
		return f"Question('{self.id}')"

class Score(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	value = db.Column(db.Integer, nullable=False)
	question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
	student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)

	def __repr__(self):
		return f"Score('{self.value}')"

class Career(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
	english_writing = db.Column(db.Integer, nullable=False)
	english_reading = db.Column(db.Integer, nullable=False)
	english_language = db.Column(db.Integer, nullable=False)
	science_state = db.Column(db.Integer, nullable=False)
	science_outline = db.Column(db.Integer, nullable=False)
	science_application = db.Column(db.Integer, nullable=False)
	science_attitude = db.Column(db.Integer, nullable=False)
	re_outline = db.Column(db.Integer, nullable=False)
	re_state = db.Column(db.Integer, nullable=False)
	re_application = db.Column(db.Integer, nullable=False)
	re_attitude = db.Column(db.Integer, nullable=False)
	agriculture_state = db.Column(db.Integer, nullable=False)
	agriculture_outline = db.Column(db.Integer, nullable=False)
	agriculture_application = db.Column(db.Integer, nullable=False)
	agriculture_attitude = db.Column(db.Integer, nullable=False)
	ss_state = db.Column(db.Integer, nullable=False)
	ss_outline = db.Column(db.Integer, nullable=False)
	ss_aplication = db.Column(db.Integer, nullable=False)
	ss_attitude = db.Column(db.Integer, nullable=False)
	math = db.Column(db.Integer, nullable=False)
	home_science = db.Column(db.Integer, nullable=False)
	creative_arts = db.Column(db.Integer, nullable=False)
	physical_and_health_education = db.Column(db.Integer, nullable=False)
	profession1 = db.Column(db.Integer, nullable=True)
	profession2 = db.Column(db.Integer, nullable=True)
	profession3 = db.Column(db.Integer, nullable=True)

	def __repr__(self):
		return f"Career('{self.english_writing}', '{self.english_reading}', '{self.english_language}', '{self.science_state}', '{self.science_outline}', '{self.science_application}', '{self.science_attitude}', '{self.re_outline}', '{self.re_state}', '{self.re_application}', '{self.re_attitude}', '{self.agriculture_state}', '{self.agriculture_outline}', '{self.agriculture_application}', '{self.agriculture_attitude}', '{self.ss_state}', '{self.ss_outline}', '{self.ss_aplication}', '{self.ss_attitude}', '{self.math}', '{self.home_science}', '{self.creative_arts}', '{self.physical_and_health_education}', '{self.profession1}', '{self.profession2}', '{self.profession3}')"

