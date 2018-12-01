from flask import render_template
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import LONGTEXT
from flask import request, redirect, url_for, session, abort, flash
import os
from flask_cors import CORS, cross_origin
from sqlalchemy.orm import sessionmaker

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
def start():
	session['logged_in']= False
	return render_template('home.html')

@app.route('/add_piece', methods=['POST'])
def addPiece():
	result = db.session.query(Writer).filter_by(name=session['username']).first()
	title = request.form['title']
	genre = request.form['genre']
	text = request.form['text']

	writer_id = result.writerID

	user = {'username': result.name}
	piece = Piece(writerID=writer_id,title=title,genre=genre,text=text)
	db.session.add(piece)
	db.session.commit()

	return render_template('test.html', user=user)

@app.route('/update_username', methods=['GET', 'POST'])
def updateUserName():
	result = db.session.query(Writer).filter_by(name=session['username']).first()
	newName = request.form['username']

	result.name = newName

	user = {'username': result.name}
	db.session.commit()

	return render_template('test.html', user=user)

@app.route('/update_userpassword', methods=['GET', 'POST'])
def updateUserPassword():
	result = db.session.query(Writer).filter_by(name=session['username']).first()
	newPassword = request.form['password']

	result.password = newPassword

	user = {'username': result.name}
	db.session.commit()

	return render_template('test.html', user=user)

@app.route('/update_userabout', methods=['GET', 'POST'])
def updateUserAbout():
	result = db.session.query(Writer).filter_by(name=session['username']).first()
	newAbout = request.form['about']

	result.about = newAbout

	user = {'username': result.name}
	db.session.commit()

	return render_template('test.html', user=user)

@app.route('/view_profile')
def viewProfile():
	result = db.session.query(Writer).filter_by(name=session['username']).first()
	user = {'username': result.name, 'about' : result.about}
	pieces = db.session.query(Piece).all()
	return render_template('test.html', user=user, pieces=pieces)

@app.route('/view_all_pieces', methods=['POST'])
def viewAllPieces():
	pieces = db.session.query(Piece).all()
	reviews = db.session.query(Reviews).all()
	ratings = db.session.query(Rating).all()
	return render_template('try.html', pieces=pieces, reviews=reviews, ratings=ratings)

# @app.route('/update_piece_title', methods=['POST'])
# def updatePieceTitle():
# 	result = db.session.query(Writer).filter_by(name=session['username']).first()
# 	#tapos query based sa writerID sa list ng pieces 
# 	#then kunin yung title nung piece
# 	#tapos update na 
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.form['username'] == ' ' or request.form['password'] == ' ':
		error = 'Invalid'
		return home()
	else:
		user = {'username': request.form['username']}

		POST_USERNAME = request.form['username']
		POST_PASSWORD = request.form['password']

		result = db.session.query(Writer).filter_by(name=POST_USERNAME, password=POST_PASSWORD).scalar()
		if result:
			session['logged_in'] = True
			session['username'] = POST_USERNAME
			return render_template('test.html', user=user)
		else:
			return start()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.form['username'] == ' ' or request.form['password'] == ' ':
		flash('invalid')
		return start()
	else:
		user = {'username': request.form['username']}
		POST_USERNAME = request.form['username']

		result = db.session.query(Writer).filter_by(name=POST_USERNAME).scalar()

		if result:
			flash('error')
			return start()
		else:
			writer = Writer(name=request.form['username'], about=request.form['about'], password=request.form['password'])
			db.session.add(writer)
			db.session.commit()
			writer_list = List(writerID=writer.writerID)
			db.session.add(writer_list)
			db.session.commit()
			session['logged_in'] = True
			return render_template('test.html', user=user)

@app.route('/logout')
def logout():
	session['logged_in']= False
	session.pop('username', None)
	return start()

if __name__ == '__main__':
	app.secret_key = os.urandom(12)
	app.run()