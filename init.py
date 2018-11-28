from test import db,Piece,Writer,List,Rating,Reviews
db.create_all()

piece = Piece(pieceID = 2000, writerID = 1, title= "A Bitch is Tired", genre= "Slice of Life", text = "And then she was tired")
db.session.add(piece)
piece = Piece(pieceID = 2001, writerID = 2, title= "A Koreaboo's Journey", genre= "Slice of Life", text = "Annyeonghaseyo")
db.session.add(piece)
piece = Piece(pieceID = 2002, writerID = 3, title= "Romeo and Juliet", genre= "Tragedy", text = "They both died.")
db.session.add(piece)

db.session.commit()

user = Writer(writerID = 1, name = "Trina Aguilana", about = "Jaehyun", listID = 1000, password = "ayokona")
db.session.add(user)
user = Writer(writerID = 2, name = "Kat Hernandez", about = "Doyoung", listID = 1001, password = "koreaboo")
db.session.add(user)
user = Writer(writerID = 3, name = "William Shakespeare", about = "Some dead guy.", listID = 1002, password = NULL)
db.session.add(user)

db.session.commit()

user_list = List(listID = 1000, writerID = 1, pieceID = 2000)
db.session.add(user_list)
user_list = List(listID = 1001, writerID = 2, pieceID = 2001)
db.session.add(user_list)
user_list = List(listID = 1002, writerID = 3, pieceID = 2000)
db.session.add(user_list)

db.session.commit() 

rating = Rating(writerID = 1, pieceID = 2000, rate = 1.4)
db.session.add(rating)
rating = Rating(writerID = 1, pieceID = 2001, rate = 5)
db.session.add(rating)
rating = Rating(writerID = 2, pieceID = 2000, rate = 3.4)
db.session.add(rating)

db.session.commit()

review = Reviews(writerID = 1, pieceID = 2000, text = "it's ayt")
db.session.add(review)
review = Reviews(writerID = 1, pieceID = 2001, text = "ewan")
db.session.add(review)
review = Reviews(writerID = 2, pieceID = 2000, text = "lmao")
db.session.add(review)

db.session.commit()

