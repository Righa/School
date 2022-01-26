from parent import db, bcrypt
from parent.models import *
import random


hashed_password = bcrypt.generate_password_hash('welcome').decode('utf-8')

users = [
	User(first_name='Lawrence', middle_name='Mwaino', last_name='Righa', email='lawrence@mail.com', password=hashed_password),
	User(first_name='Amos', middle_name='Kiunga', last_name='Kalue', email='amos@mail.com', password=hashed_password),
	User(first_name='Collen', middle_name='Ruma', last_name='Malowa', email='collen@mail.com', password=hashed_password),
	User(first_name='Ruby', middle_name='Ras', last_name='Ghambi', email='ruby@mail.com', password=hashed_password),
	User(first_name='Moses', middle_name='Goa', last_name='Gatumi', email='moses@mail.com', password=hashed_password),
	User(first_name='Betty', middle_name='Mayaya', last_name='Chihumi', email='betty@mail.com', password=hashed_password),
	User(first_name='Clinton', middle_name='Mrabai', last_name='Vasso', email='vasso@mail.com', password=hashed_password),
	User(first_name='Mary', middle_name='Matome', last_name='Maghema', email='mary@mail.com', password=hashed_password),
	User(first_name='Gregory', middle_name='Kisaghu', last_name='Mghemi', email='gregory@mail.com', password=hashed_password),
	User(first_name='Don', middle_name='Mass', last_name='Illi', email='donmass@mail.com', password=hashed_password)
]

groups = [Group(year=2019), Group(year=2020), Group(year=2021), Group(year=2022)]

subjects = [
	Subject(name='English'),
	Subject(name='Science'),
	Subject(name='Religious Education'),
	Subject(name='Agriculture'),
	Subject(name='Social Studies'),
	Subject(name='Mathematics'),
	Subject(name='Home Science'),
	Subject(name='Creative Arts'),
	Subject(name='Physical and Health')
]

categories = [
	Category(name='Writing', minimum=0, maximum=10, subject_id=1),
	Category(name='Reading', minimum=0, maximum=10, subject_id=1),
	Category(name='Language', minimum=0, maximum=10, subject_id=1),
	Category(name='State', minimum=0, maximum=10, subject_id=2),
	Category(name='Outline', minimum=0, maximum=10, subject_id=2),
	Category(name='Application', minimum=0, maximum=10, subject_id=2),
	Category(name='Attitude', minimum=0, maximum=10, subject_id=2),
	Category(name='Outline', minimum=0, maximum=10, subject_id=3),
	Category(name='State', minimum=0, maximum=10, subject_id=3),
	Category(name='Application', minimum=0, maximum=10, subject_id=3),
	Category(name='Attitude', minimum=0, maximum=10, subject_id=3),
	Category(name='State', minimum=0, maximum=10, subject_id=4),
	Category(name='Outline', minimum=0, maximum=10, subject_id=4),
	Category(name='Application', minimum=0, maximum=10, subject_id=4),
	Category(name='Attitude', minimum=0, maximum=10, subject_id=4),
	Category(name='State', minimum=0, maximum=10, subject_id=5),
	Category(name='Outline', minimum=0, maximum=10, subject_id=5),
	Category(name='Application', minimum=0, maximum=10, subject_id=5),
	Category(name='Attitude', minimum=0, maximum=10, subject_id=5),
	Category(name='General', minimum=0, maximum=10, subject_id=6),
	Category(name='General', minimum=0, maximum=10, subject_id=7),
	Category(name='General', minimum=0, maximum=10, subject_id=8),
	Category(name='General', minimum=0, maximum=10, subject_id=9)
]

students = [
	User(first_name='Jane', middle_name='Sam', last_name='Doe', utype='student', email='janedoe@mail.com', password=hashed_password),
	User(first_name='Noah', middle_name='Yonas', last_name='Taye', utype='student', email='taye@mail.com', password=hashed_password),
	User(first_name='Olivia', middle_name='Abel', last_name='Liya', utype='student', email='liya@mail.com', password=hashed_password),
	User(first_name='Emma', middle_name='Amadi', last_name='Aida', utype='student', email='aida@mail.com', password=hashed_password),
	User(first_name='Oliver', middle_name='Aaron', last_name='Shango', utype='student', email='shango@mail.com', password=hashed_password),
	User(first_name='Ava', middle_name='Ahmed', last_name='Nyala', utype='student', email='nyala@mail.com', password=hashed_password),
	User(first_name='Elijah', middle_name='Negasi', last_name='Omari', utype='student', email='omari@mail.com', password=hashed_password),
	User(first_name='Chalotte', middle_name='Kofi', last_name='Zala', utype='student', email='zala@mail.com', password=hashed_password),
	User(first_name='William', middle_name='Abraham', last_name='Kojo', utype='student', email='kojo@mail.com', password=hashed_password),
	User(first_name='Sophia', middle_name='Hakim', last_name='Mazaa', utype='student', email='mazaa@mail.com', password=hashed_password),
	User(first_name='James', middle_name='Kaleb', last_name='Jonathan', utype='student', email='jonathan@mail.com', password=hashed_password),
	User(first_name='Amelia', middle_name='Alimayu', last_name='Marjani', utype='student', email='marjani@mail.com', password=hashed_password),
	User(first_name='Benjamin', middle_name='Salana', last_name='Jemal', utype='student', email='jemal@mail.com', password=hashed_password),
	User(first_name='Isabella', middle_name='Panya', last_name='Kia', utype='student', email='kia@mail.com', password=hashed_password),
	User(first_name='Lucas', middle_name='Ajani', last_name='Ephrem', utype='student', email='ephrem@mail.com', password=hashed_password),
	User(first_name='Mia', middle_name='Amari', last_name='Dani', utype='student', email='dani@mail.com', password=hashed_password),
	User(first_name='Henry', middle_name='Chinua', last_name='Emanuel', utype='student', email='emanuel@mail.com', password=hashed_password),
	User(first_name='Evelyn', middle_name='Gyasi', last_name='Eshe', utype='student', email='eshe@mail.com', password=hashed_password),
	User(first_name='Alexander', middle_name='Zesiro', last_name='Djimon', utype='student', email='djimon@mail.com', password=hashed_password),
	User(first_name='Harper', middle_name='Barack', last_name='Genet', utype='student', email='genet@mail.com', password=hashed_password),
	User(first_name='Linda', middle_name='Ebo', last_name='Kamali', utype='student', email='kamali@mail.com', password=hashed_password),
	User(first_name='Richard', middle_name='Haji', last_name='Zenebe', utype='student', email='zenebe@mail.com', password=hashed_password),
	User(first_name='Thomas', middle_name='Kato', last_name='Daniel', utype='student', email='daniel@mail.com', password=hashed_password),
	User(first_name='Nancy', middle_name='Selassie', last_name='Nuru', utype='student', email='nuru@mail.com', password=hashed_password),
	User(first_name='Ashley', middle_name='Negus', last_name='Ife', utype='student', email='ife@mail.com', password=hashed_password)
]

exams = [
	Exam(year=2019, term=1, user_id=1, subject_id=1, group_id=1),
	Exam(year=2019, term=1, user_id=1, subject_id=2, group_id=1),
	Exam(year=2019, term=1, user_id=1, subject_id=3, group_id=1),
	Exam(year=2019, term=1, user_id=1, subject_id=4, group_id=1),
	Exam(year=2019, term=1, user_id=1, subject_id=5, group_id=1),
	Exam(year=2019, term=1, user_id=1, subject_id=6, group_id=1),
	Exam(year=2019, term=1, user_id=1, subject_id=7, group_id=1),
	Exam(year=2019, term=1, user_id=1, subject_id=8, group_id=1),
	Exam(year=2019, term=1, user_id=1, subject_id=9, group_id=1),
	Exam(year=2020, term=1, user_id=1, subject_id=1, group_id=2),
	Exam(year=2020, term=1, user_id=1, subject_id=2, group_id=2),
	Exam(year=2020, term=1, user_id=1, subject_id=3, group_id=2),
	Exam(year=2020, term=1, user_id=1, subject_id=4, group_id=2),
	Exam(year=2020, term=1, user_id=1, subject_id=5, group_id=2),
	Exam(year=2020, term=1, user_id=1, subject_id=6, group_id=2),
	Exam(year=2020, term=1, user_id=1, subject_id=7, group_id=2),
	Exam(year=2020, term=1, user_id=1, subject_id=8, group_id=2),
	Exam(year=2020, term=1, user_id=1, subject_id=9, group_id=2),
	Exam(year=2021, term=1, user_id=1, subject_id=1, group_id=3),
	Exam(year=2021, term=1, user_id=1, subject_id=2, group_id=3),
	Exam(year=2021, term=1, user_id=1, subject_id=3, group_id=3),
	Exam(year=2021, term=1, user_id=1, subject_id=4, group_id=3),
	Exam(year=2021, term=1, user_id=1, subject_id=5, group_id=3),
	Exam(year=2021, term=1, user_id=1, subject_id=6, group_id=3),
	Exam(year=2021, term=1, user_id=1, subject_id=7, group_id=3),
	Exam(year=2021, term=1, user_id=1, subject_id=8, group_id=3),
	Exam(year=2021, term=1, user_id=1, subject_id=9, group_id=3),
	Exam(year=2022, term=1, user_id=1, subject_id=1, group_id=4),
	Exam(year=2022, term=1, user_id=1, subject_id=2, group_id=4),
	Exam(year=2022, term=1, user_id=1, subject_id=3, group_id=4),
	Exam(year=2022, term=1, user_id=1, subject_id=4, group_id=4),
	Exam(year=2022, term=1, user_id=1, subject_id=5, group_id=4),
	Exam(year=2022, term=1, user_id=1, subject_id=6, group_id=4),
	Exam(year=2022, term=1, user_id=1, subject_id=7, group_id=4),
	Exam(year=2022, term=1, user_id=1, subject_id=8, group_id=4),
	Exam(year=2022, term=1, user_id=1, subject_id=9, group_id=4)
]

questions = [
	Question(number=1, category_id=1, exam_id=1),
	Question(number=2, category_id=2, exam_id=1),
	Question(number=3, category_id=3, exam_id=1),
	Question(number=1, category_id=4, exam_id=2),
	Question(number=2, category_id=5, exam_id=2),
	Question(number=3, category_id=6, exam_id=2),
	Question(number=4, category_id=7, exam_id=2),
	Question(number=1, category_id=8, exam_id=3),
	Question(number=2, category_id=9, exam_id=3),
	Question(number=3, category_id=10, exam_id=3),
	Question(number=4, category_id=11, exam_id=3),
	Question(number=1, category_id=12, exam_id=4),
	Question(number=2, category_id=13, exam_id=4),
	Question(number=3, category_id=14, exam_id=4),
	Question(number=4, category_id=15, exam_id=4),
	Question(number=1, category_id=16, exam_id=5),
	Question(number=2, category_id=17, exam_id=5),
	Question(number=3, category_id=18, exam_id=5),
	Question(number=4, category_id=19, exam_id=5),
	Question(number=1, category_id=20, exam_id=6),
	Question(number=1, category_id=21, exam_id=7),
	Question(number=1, category_id=22, exam_id=8),
	Question(number=1, category_id=23, exam_id=9),
	Question(number=1, category_id=1, exam_id=10),
	Question(number=2, category_id=2, exam_id=10),
	Question(number=3, category_id=3, exam_id=10),
	Question(number=1, category_id=4, exam_id=11),
	Question(number=2, category_id=5, exam_id=11),
	Question(number=3, category_id=6, exam_id=11),
	Question(number=4, category_id=7, exam_id=11),
	Question(number=1, category_id=8, exam_id=12),
	Question(number=2, category_id=9, exam_id=12),
	Question(number=3, category_id=10, exam_id=12),
	Question(number=4, category_id=11, exam_id=12),
	Question(number=1, category_id=12, exam_id=13),
	Question(number=2, category_id=13, exam_id=13),
	Question(number=3, category_id=14, exam_id=13),
	Question(number=4, category_id=15, exam_id=13),
	Question(number=1, category_id=16, exam_id=14),
	Question(number=2, category_id=17, exam_id=14),
	Question(number=3, category_id=18, exam_id=14),
	Question(number=4, category_id=19, exam_id=14),
	Question(number=1, category_id=20, exam_id=15),
	Question(number=1, category_id=21, exam_id=16),
	Question(number=1, category_id=22, exam_id=17),
	Question(number=1, category_id=23, exam_id=18),
	Question(number=1, category_id=1, exam_id=19),
	Question(number=2, category_id=2, exam_id=19),
	Question(number=3, category_id=3, exam_id=19),
	Question(number=1, category_id=4, exam_id=20),
	Question(number=2, category_id=5, exam_id=20),
	Question(number=3, category_id=6, exam_id=20),
	Question(number=4, category_id=7, exam_id=20),
	Question(number=1, category_id=8, exam_id=21),
	Question(number=2, category_id=9, exam_id=21),
	Question(number=3, category_id=10, exam_id=21),
	Question(number=4, category_id=11, exam_id=21),
	Question(number=1, category_id=12, exam_id=22),
	Question(number=2, category_id=13, exam_id=22),
	Question(number=3, category_id=14, exam_id=22),
	Question(number=4, category_id=15, exam_id=22),
	Question(number=1, category_id=16, exam_id=23),
	Question(number=2, category_id=17, exam_id=23),
	Question(number=3, category_id=18, exam_id=23),
	Question(number=4, category_id=19, exam_id=23),
	Question(number=1, category_id=20, exam_id=24),
	Question(number=1, category_id=21, exam_id=25),
	Question(number=1, category_id=22, exam_id=26),
	Question(number=1, category_id=23, exam_id=27),
	Question(number=1, category_id=1, exam_id=28),
	Question(number=2, category_id=2, exam_id=28),
	Question(number=3, category_id=3, exam_id=28),
	Question(number=1, category_id=4, exam_id=29),
	Question(number=2, category_id=5, exam_id=29),
	Question(number=3, category_id=6, exam_id=29),
	Question(number=4, category_id=7, exam_id=29),
	Question(number=1, category_id=8, exam_id=30),
	Question(number=2, category_id=9, exam_id=30),
	Question(number=3, category_id=10, exam_id=30),
	Question(number=4, category_id=11, exam_id=30),
	Question(number=1, category_id=12, exam_id=31),
	Question(number=2, category_id=13, exam_id=31),
	Question(number=3, category_id=14, exam_id=31),
	Question(number=4, category_id=15, exam_id=31),
	Question(number=1, category_id=16, exam_id=32),
	Question(number=2, category_id=17, exam_id=32),
	Question(number=3, category_id=18, exam_id=32),
	Question(number=4, category_id=19, exam_id=32),
	Question(number=1, category_id=20, exam_id=33),
	Question(number=1, category_id=21, exam_id=34),
	Question(number=1, category_id=22, exam_id=35),
	Question(number=1, category_id=23, exam_id=36),
]


def seed():
	db.drop_all()
	db.create_all()

	print('Database Cleared!')

	for user in users:
		db.session.add(user)
	for group in groups:
		db.session.add(group)
	for subject in subjects:
		db.session.add(subject)
	db.session.commit()

	for category in categories:
		db.session.add(category)
	for stdnt in students:
		db.session.add(stdnt)
	for exam in exams:
		db.session.add(exam)
	db.session.commit()

	grp = 1
	for stu in User.query.filter_by(utype='student'):
		if grp > 3:
			grp = 1
		stu.student=Student(user_id=stu.id, group_id=grp)
		grp += 1
	
	for question in questions:
		db.session.add(question)
	db.session.commit()

	for mgroup in Group.query.all():
		for student in mgroup.students:
			for exam in mgroup.exams:
				for question in exam.questions:
					score=Score(value=random.randint(0,10), question_id=question.id, student_id=student.id)
					db.session.add(score)
	db.session.commit()
	
	print('Seeding Complete!')
