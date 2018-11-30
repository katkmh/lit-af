from flask import render_template
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import LONGTEXT
from flask import request, redirect, url_for
import os
from flask_cors import CORS, cross_origin

app = Flask(__name__)
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
	pieceID = db.Column(db.Integer, db.ForeignKey('piece.pieceID'))
	
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
# @app.route('/index')
# def home():
#    user = {'username': request.form['username']}
#    return render_template('test.html', title='Home', user=user)

@app.route('/index', methods=['GET', 'POST'])
@cross_origin()
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] == ' ' or request.form['password'] == ' ':
			error = 'Invalid'
		else:
			return redirect(url_for('Home'))
	return render_template('try.html', title='Login', error=error) 

if __name__ == '__test__':
	app.run()