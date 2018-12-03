from test import db,Piece,Writer,List,Rating,Reviews
db.drop_all()
db.create_all()

user = Writer(name="William Shakespeare", 
	about=" an English poet, playwright and actor\n"
	", widely regarded as the greatest writer in the English\n"
	"language and the world's greatest dramatist", 
	password="123")
db.session.add(user)
db.session.commit()

piece = Piece(writerID=1, title="Something", genre="Slice of Life", text="Konnichiwa")
db.session.add(piece)
db.session.commit()

user_list = List(writerID = 1, pieceID = 1)
db.session.add(user_list)
db.session.commit() 

rating = Rating(writerID = 1, pieceID = 1, rate = 1.4)
db.session.add(rating)
db.session.commit()

review = Reviews(writerID = 1, pieceID = 1, text = "it's ayt")
db.session.add(review)
db.session.commit()

