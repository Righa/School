from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '8a51ff200dfe7b36f2cd17adb19e145e'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.jinja_env.add_extension('jinja2.ext.do')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from parent import routes
