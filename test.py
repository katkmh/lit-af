from flask import render_template
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import LONGTEXT
from flask import request, redirect, url_for, session, abort
import os
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.secret_key = 'my_secret_key'
Bootstrap(app)

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:password@localhost/postgres'
db = SQLAlchemy(app)

class Piece(db.Model):
	pieceID = db.Column(db.Integer,unique=True,nullable=False,primary_key=True, autoincrement=True)
	writerID = db.Column(db.Integer,db.ForeignKey('writer.writerID'),primary_key=True)
	title = db.Column(db.String(100))
	genre = db.Column(db.String(15))
	text = db.Column(db.Text)

	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Writer(db.Model):
	writerID = db.Column(db.Integer,unique=True,nullable=False,primary_key=True,autoincrement=True)
	name = db.Column(db.String(30))
	about = db.Column(db.Text)
	password = db.Column(db.String(30))

	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class List(db.Model):
	listID = db.Column(db.Integer,unique=True,nullable=False,primary_key=True,autoincrement=True)
	writerID = db.Column(db.Integer, db.ForeignKey('writer.writerID'),primary_key=True)
	
	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Rating(db.Model):
	writerID = db.Column(db.Integer, db.ForeignKey('writer.writerID'),primary_key=True)
	pieceID = db.Column(db.Integer, db.ForeignKey('piece.pieceID'),primary_key=True)
	rate = db.Column(db.Float)

	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}
		
class Reviews(db.Model):
	writerID = db.Column(db.Integer, db.ForeignKey('writer.writerID'), primary_key=True)
	pieceID = db.Column(db.Integer, db.ForeignKey('piece.pieceID'), primary_key=True)
	text = db.Column(db.Text)

	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}
		
@app.route('/')
def home():
	session['logged_in']= False
	if not session.get('logged_in'):
		return render_template('home.html')
	else:
		return "test"

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.form['username'] == ' ' or request.form['password'] == ' ':
		error = 'Invalid'
		return home()
	else:
		session['logged_in'] = True
		user = {'username': request.form['username']}
		#######INSERT USER AUTHENTICATION HERE########
		return render_template('test.html', user=user)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	error = None
	if request.form['username'] == ' ' or request.form['password'] == ' ':
		error = 'Invalid'
		return render_template('home.html')
	else:
		user = {'username': request.form['username']}
		writer = Writer(name=request.form['username'], about=request.form['about'], password=request.form['password'])
		db.session.add(writer)
		db.session.commit()
		session['logged_in'] = True
		return render_template('test.html', user=user)

if __name__ == '__main__':
	app.secret_key = os.urandom(12)
	app.run()