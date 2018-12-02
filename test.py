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
	pieceID = db.Column(db.Integer, db.ForeignKey('piece.pieceID'),primary_key=True)

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

#######kailangan muna niya dumaan dito bago sa add piece
@app.route('/add-piece_form', methods=['GET', 'POST'])
def addPieceForm():
	result = db.session.query(Writer).filter_by(name=session['username']).first()
	user = {'username': result.name, 'about' : result.about, 'writerID': result.writerID}
	pieces = db.session.query(Piece).all()
	return render_template('add_piece.html', user=user, pieces=pieces)

#######kailangan muna niya dumaan dito bago sa update piece para makuha yung piece ID
@app.route('/update-piece_form', methods=['GET', 'POST'])
def updatePieceForm():
	result = db.session.query(Writer).filter_by(name=session['username']).first()
	user = {'username': result.name, 'about' : result.about, 'writerID': result.writerID}
	# pieces = db.session.query(Piece).filter_by(writerID=result.writerID).all()
	pieces = db.session.query(Piece).all()
	return render_template('update_piece.html', user=user, pieces = pieces)

########gawin ko na lang muna the same as yung sa update na may dinadaanan
@app.route('/delete-piece_form', methods=['GET', 'POST'])
def deletePieceForm():
	result = db.session.query(Writer).filter_by(name=session['username']).first()
	user = {'username': result.name, 'about':result.about, 'writerID' :result.writerID}
	pieces = db.session.query(Piece).all()

	return render_template('profile.html', user=user, pieces=pieces)

@app.route('/delete_piece', methods=['GET', 'POST'])
def deletePiece():
	result = db.session.query(Writer).filter_by(name=session['username']).first()
	pieceID = request.form.get('pieceID')

	user = {'username': result.name, 'about' : result.about, 'writerID': result.writerID}
	select = db.session.query(Piece).filter_by(pieceID=pieceID).first()

	db.session.delete(piece)
	db.session.commit()

	pieces = db.session.query(Piece).all()
	return render_template('profile.html', user=user, pieces=pieces)

############################add reviews###############################################
#so since kailangan ng pieceID kailangan nung update piece may hidden ulit siya sa form
@app.route('/add-review_form', methods=['GET', 'POST'])
def addReviewForm():
	result = db.session.query(Writer).filter_by(name=session['username']).first()
	user = {'username': result.name, 'about' : result.about, 'writerID': result.writerID}
	pieces = db.session.query(Piece).all()
	reviews = db.session.query(Reviews).all()
	return render_template('add_review.html', user=user, pieces=pieces, reviews=reviews)

@app.route('/add_review', methods=['POST'])
def addReview():
	result = db.session.query(Writer).filter_by(name=session['username']).first()
	pieceID = request.form.get('pieceID')
	text = request.form.get('text')
	writer_id = result.writerID
	#insert same title by the same user restriction here
	user = {'username': result.name, 'about' : result.about, 'writerID': result.writerID}
	review = Reviews(writerID = result.writerID, pieceID = pieceID, text =text)

	db.session.add(review)
	db.session.commit()
	pieces = db.session.query(Piece).all()
	reviews = db.session.query(Reviews).all()
	return render_template('profile.html', user=user, pieces=pieces, reviews=reviews)
##########################################################################33
@app.route('/delete-review_form', methods=['GET', 'POST'])
def deleteReviewForm():
	result = db.session.query(Writer).filter_by(name=session['username']).first()
	user = {'username': result.name, 'about':result.about, 'writerID' :result.writerID}
	pieces = db.session.query(Piece).all()
	reviews = db.session.query(Reviews).all()
	return render_template('profile.html', user=user, pieces=pieces, reviews=reviews)

@app.route('/delete_review', methods=['GET', 'POST'])
def deleteReview():
	result = db.session.query(Writer).filter_by(name=session['username']).first()
	pieceID = request.form.get('pieceID')

	user = {'username': result.name, 'about' : result.about, 'writerID': result.writerID}
	select = db.session.query(Reviews).filter_by(writerID=result.writerID,pieceID=pieceID).first()

	db.session.delete(select)
	db.session.commit()

	pieces = db.session.query(Piece).all()
	reviews = db.session.query(Reviews).all()
	return render_template('profile.html', user=user, pieces=pieces, reviews=reviews)

@app.route('/update-review_form', methods=['GET', 'POST'])
def updateReviewForm():
	result = db.session.query(Writer).filter_by(name=session['username']).first()
	user = {'username': result.name, 'about' : result.about, 'writerID': result.writerID}
	pieces = db.session.query(Piece).all()
	reviews = db.session.query(Reviews).all()
	return render_template('add_review.html', user=user, pieces=pieces, reviews=reviews)

@app.route('/update_review', methods=['GET', 'POST'])
def updateReview():
	result = db.session.query(Writer).filter_by(name=session['username']).first()
	pieceID = request.form.get('pieceID')
	newtext = request.form.get('text')

	user = {'username': result.name, 'about' : result.about, 'writerID': result.writerID}
	select = db.session.query(Reviews).filter_by(writerID=result.writerID,pieceID=pieceID).first()

	select.text = newtext
	db.session.commit()
	
	pieces = db.session.query(Piece).all()
	reviews = db.session.query(Reviews).all()
	return render_template('profile.html', user=user, pieces=pieces, reviews=reviews)
############################add rating##############################
@app.route('/add-rating_form', methods=['GET', 'POST'])
def addRatingForm():
	result = db.session.query(Writer).filter_by(name=session['username']).first()
	user = {'username': result.name, 'about' : result.about, 'writerID': result.writerID}
	pieces = db.session.query(Piece).all()
	ratings = db.session.query(Rating).all()
	return render_template('add_rating.html', user=user, pieces=pieces, ratings=ratings)

@app.route('/add_rating', methods=['POST'])
def addRating():
	result = db.session.query(Writer).filter_by(name=session['username']).first()
	pieceID = request.form.get('pieceID')
	rating = request.form.get('rating')
	writer_id = result.writerID
	
	user = {'username': result.name, 'about' : result.about, 'writerID': result.writerID}
	rating = Rating(writerID = result.writerID, pieceID = pieceID, rate=rating)

	db.session.add(rating)
	db.session.commit()
	pieces = db.session.query(Piece).all()
	ratings = db.session.query(Rating).all()
	return render_template('profile.html', user=user, pieces=pieces, ratings=rating)

########################addtoList##############
@app.route('/add-to-list_form', methods=['GET', 'POST'])
def addToListForm():
	result = db.session.query(Writer).filter_by(name=session['username']).first()
	user = {'username': result.name, 'about' : result.about, 'writerID': result.writerID}
	pieces = db.session.query(Piece).all()
	all_list = db.session.query(List).all()
	writers = db.session.query(Writer).all()
	return render_template('profile.html', user=user, pieces=pieces, all_list=all_list, writers=writers)

@app.route('/add_to-list', methods=['GET', 'POST'])
def addToList():
	result = db.session.query(Writer).filter_by(name=session['username']).first()
	user = {'username': result.name, 'about' : result.about, 'writerID': result.writerID}
	pieceID = request.form.get('pieceID')
	select = db.session.query(Piece).filter_by(pieceID=pieceID).first()

	piece = List(listID=result.writerID, writerID=result.writerID, pieceID=select.pieceID)

	pieces = db.session.query(Piece).all()
	all_list = db.session.query(List).all()
	writers = db.session.query(Writer).all()
	return render_template('profile.html', user=user, pieces=pieces, all_list=all_list, writers=writers)
############################

@app.route('/update_piece', methods=['GET','POST'])
def updatePiece():
	result = db.session.query(Writer).filter_by(name=session['username']).first()
	pieceID = request.form.get('pieceID')
	newtitle = request.form.get('title')
	newgenre = request.form.get('genre')
	newtext = request.form.get('text')
	user = {'username': result.name, 'about' : result.about, 'writerID': result.writerID}
	select = db.session.query(Piece).filter_by(pieceID=pieceID).first()

	select.title = newtitle
	select.genre = newgenre
	select.text = newtext
	db.session.commit()

	pieces = db.session.query(Piece).all()
	return render_template('profile.html', user=user, pieces=pieces)

@app.route('/add_piece', methods=['POST'])
def addPiece():
	result = db.session.query(Writer).filter_by(name=session['username']).first()
	title = request.form['title']
	genre = request.form['genre']
	text = request.form['text']

	writer_id = result.writerID
	#insert same title by the same user restriction here
	user = {'username': result.name, 'about' : result.about, 'writerID': result.writerID}
	piece = Piece(writerID=writer_id,title=title,genre=genre,text=text)
	db.session.add(piece)
	db.session.commit()
	pieces = db.session.query(Piece).all()
	return render_template('profile.html', user=user, pieces=pieces)
	# return render_template('add_piece.html', user=user)

@app.route('/dito_muna', methods=['GET', 'POST'])
def ditomuna():
	result = db.session.query(Writer).filter_by(name=session['username']).first()
	user = {'username': result.name, 'password' : result.password, 'about' : result.about}
	pieces = db.session.query(Piece).all()
	return render_template('update_user.html', user=user, pieces=pieces)

@app.route('/update_user', methods=['GET', 'POST'])
def updateUser():
	result = db.session.query(Writer).filter_by(name=session['username']).first()
	newName = request.form.get('username')
	newPassword = request.form.get('password')
	newAbout = request.form.get('about')

	result.name = newName
	result.password = newPassword
	result.about = newAbout
	
	db.session.commit()
	user = {'username': result.name, 'password' : result.password, 'about' : result.about, 'writerID': result.writerID}
	pieces = db.session.query(Piece).all()
	return render_template('profile.html', user=user, pieces=pieces)

@app.route('/view_profile')
def viewProfile():
	result = db.session.query(Writer).filter_by(name=session['username']).first()
	user = {'username': result.name, 'about' : result.about, 'writerID': result.writerID}
	writers = db.session.query(Writer).all()
	pieces = db.session.query(Piece).all()
	all_list = db.session.query(List).all()
	return render_template('profile.html', user=user, pieces=pieces, all_list=all_list, writers=writers)

@app.route('/view_all_pieces', methods=['POST'])
def viewAllPieces():
	writers = db.session.query(Writer).all()
	pieces = db.session.query(Piece).all()
	reviews = db.session.query(Reviews).all()
	ratings = db.session.query(Rating).all()
	return render_template('try.html', pieces=pieces, reviews=reviews, ratings=ratings, writers=writers)

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
			pieces = db.session.query(Piece).all()
			return render_template('test.html', user=user, pieces=pieces)

@app.route('/logout')
def logout():
	session['logged_in']= False
	session.pop('username', None)
	return start()

if __name__ == '__main__':
	app.secret_key = os.urandom(12)
	app.run()