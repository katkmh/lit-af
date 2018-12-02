from test import db,Piece,Writer,List,Rating,Reviews
db.drop_all()
db.create_all()

user = Writer(name="Trina Aguilana", about="lalalala", password="ayokona")
db.session.add(user)
user = Writer(name="Kat Hernandez", about="sasadasdsasd", password="koreaboo")
db.session.add(user)
user = Writer(name="William Shakespeare", about="Some dead guy.", password="asasas")
db.session.add(user)

db.session.commit()

piece = Piece(writerID=1, title="Something", genre="Slice of Life", text="Konnichiwa")
db.session.add(piece)
piece = Piece(writerID=2, title="What", genre= "Slice of Life", text="Annyeonghaseyo")
db.session.add(piece)
piece = Piece(writerID =3, title= "Romeo and Juliet", genre= "Tragedy", text = "They both died.")
db.session.add(piece)

db.session.commit()

user_list = List(writerID = 1, pieceID = 3)
db.session.add(user_list)
user_list = List(writerID = 2, pieceID = 2)
db.session.add(user_list)
user_list = List(writerID = 3, pieceID = 1)
db.session.add(user_list)

db.session.commit() 

rating = Rating(writerID = 1, pieceID = 2, rate = 1.4)
db.session.add(rating)
rating = Rating(writerID = 2, pieceID = 2, rate = 5)
db.session.add(rating)
rating = Rating(writerID = 3, pieceID = 3, rate = 3.4)
db.session.add(rating)

db.session.commit()

review = Reviews(writerID = 1, pieceID = 1, text = "it's ayt")
db.session.add(review)
review = Reviews(writerID = 2, pieceID = 2, text = "ewan")
db.session.add(review)
review = Reviews(writerID = 3, pieceID = 3, text = "lmao")
db.session.add(review)

db.session.commit()

