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

@app.route('/', methods=['GET','POST'])
def start():
	session['logged_in']= False
	return render_template('home.html')

#######kailangan muna niya dumaan dito bago sa update piece para makuha yung piece ID
@app.route('/update', methods=['GET', 'POST'])
def update():
	result = db.session.query(Writer).filter_by(name=session['username']).first()
	pieces = db.session.query(Piece).filter_by(writerID=result.writerID).all()
	return render_template('try.html', pieces = pieces)

@app.route('/updatePiece', methods=['GET','POST'])
def updatePiece():

	pieceID = request.form.get('pieceID')
	newtitle = request.form.get('newtitle')
	newgenre = request.form.get('newgenre')
	newtext = request.form.get('newtext')

	select = db.session.query(Piece).filter_by(pieceID=pieceID).first()

	select.title = newtitle
	select.genre = newgenre
	select.text = newtext
	db.session.commit()

	pieces = db.session.query(Piece).all()
	return render_template('try.html', pieces = pieces)

@app.route('/add_piece', methods=['POST'])
def addPiece():
	result = db.session.query(Writer).filter_by(name=session['username']).first()
	title = request.form['title']
	genre = request.form['genre']
	text = request.form['text']

	writer_id = result.writerID
	#insert same title by the same user restriction here
	user = {'username': result.name}
	piece = Piece(writerID=writer_id,title=title,genre=genre,text=text)
	db.session.add(piece)
	db.session.commit()

	return render_template('test.html', user=user)

#kat try mo na padaanin muna dito yung pagnagclick ng edit ng account tapos saka na lang pupunta sa /update_user for the form
@app.route('/dito_muna', methods=['GET', 'POST'])
def ditomuna():
	result = db.session.query(Writer).filter_by(name=session['username']).first()
	user = {'username': result.name, 'password' : result.password, 'about' : result.about}
	pieces = db.session.query(Piece).all()
	return render_template('update_user.html', user=user, pieces=pieces)

@app.route('/update_user', methods=['GET', 'POST'])
def updateUser():
	
	newName = request.form.get('username')
	newPassword = request.form.get('password')
	newAbout = request.form.get('about')

	# if(newName == ""):
	# 	result.name = result.name
	# else:
	# 	result.name = newName
	# if(newPassword == ""):
	# 	result.password = result.password
	# else:
	# 	result.password = newPassword
	# if(newAbout == ""):
	# 	result.about = result.about
	# else:
	# 	result.about = newAbout

	result.name = newName
	result.password = newPassword
	result.about = newAbout
	
	db.session.commit()
	user = {'username': result.name, 'password' : result.password, 'about' : result.about}
	return render_template('update_user.html', user=user, pieces=pieces)

@app.route('/view_profile')
def viewProfile():
	result = db.session.query(Writer).filter_by(name=session['username']).first()
	user = {'username': result.name, 'about' : result.about, 'writerID': result.writerID}
	pieces = db.session.query(Piece).all()
	return render_template('profile.html', user=user, pieces=pieces)


@app.route('/view_all_pieces', methods=['POST'])
def viewAllPieces():
	pieces = db.session.query(Piece).all()
	reviews = db.session.query(Reviews).all()
	ratings = db.session.query(Rating).all()
	return render_template('try.html', pieces=pieces, reviews=reviews, ratings=ratings)

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
			writers = db.session.query(Writer).all()
			pieces = db.session.query(Piece).all()
			return render_template('test.html', user=user, pieces=pieces, writers=writers)
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
			session['username'] = request.form['username']
			return render_template('test.html', user=user)

@app.route('/logout')
def logout():
	session['logged_in']= False
	session.pop('username', None)
	return start()

if __name__ == '__main__':
	app.secret_key = os.urandom(12)
	app.run()