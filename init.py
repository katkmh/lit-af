from test import db,Piece,Writer,List,Rating,Reviews
db.drop_all()
db.create_all()

user = Writer(name="William Shakespeare", about="An English poet, playwright and actor, widely regarded as the greatest writer in the English language and the world's greatest dramatist", password="123")
db.session.add(user)

user = Writer(name="Trina Aguilana", about="A fourth-year Computer Science Student in UP Diliman", password="password")
db.session.add(user)

user = Writer(name="Kat Hernandez", about="An Everlasting Friend", password="blessmeachoo")
db.session.add(user)

user = Writer(name="Jin", about="BTS Member/Worldwide Handsome", password="epiphany")
db.session.add(user)

user = Writer(name="Doyoung", 
	about="Neo-Culture Technology", password="simonsays")
db.session.add(user)

db.session.commit()

piece = Piece(writerID=1, title="Sonnet I", genre="Sonnet", text="FROM fairest creatures we desire increase,\nThat thereby beauty's rose might never die, \nBut as the riper should by time decease, \nHis tender heir might bear his memory: \nBut thou, contracted to thine own bright eyes, \nFeed'st thy light'st flame with self-substantial fuel, \nMaking a famine where abundance lies, \nThyself thy foe, to thy sweet self too cruel. \nThou that art now the world's fresh ornament \nAnd only herald to the gaudy spring, \nWithin thine own bud buriest thy content \nAnd, tender churl, makest waste in niggarding. \nPity the world, or else this glutton be, \nTo eat the world's due, by the grave and thee.")
db.session.add(piece)

piece = Piece(writerID=1, title="Sonnet VI", genre="Sonnet", text="Then let not winter's ragged hand deface \nIn thee thy summer, ere thou be distill'd: \nMake sweet some vial; treasure thou some place \nWith beauty's treasure, ere it be self-kill'd. \nThat use is not forbidden usury, \nWhich happies those that pay the willing loan; \nThat's for thyself to breed another thee, \nOr ten times happier, be it ten for one; \nTen times thyself were happier than thou art, \nIf ten of thine ten times refigured thee: \nThen what could death do, if thou shouldst depart, \nLeaving thee living in posterity? \nBe not self-will'd, for thou art much too fair \nTo be death's conquest and make worms thine heir.")
db.session.add(piece)

piece = Piece(writerID=1, title="Sonnet V", genre="Sonnet", text="Those hours, that with gentle work did frame \nThe lovely gaze where every eye doth dwell, \nWill play the tyrants to the very same \nAnd that unfair which fairly doth excel: \nFor never-resting time leads summer on \nTo hideous winter and confounds him there; \nSap cheque'd with frost and lusty leaves quite gone, \nBeauty o'ersnow'd and bareness every where: \nThen, were not summer's distillation left, \nA liquid prisoner pent in walls of glass, \nBeauty's effect with beauty were bereft, \nNor it nor no remembrance what it was: \nBut flowers distill'd though they with winter meet, \nLeese but their show; their substance still lives sweet.")
db.session.add(piece)

piece = Piece(writerID=4, title="Epiphany", genre="Self-love", text="I’m the one I should love in this world \nBitnaneun nareul sojunghan nae yeonghoneul \nIjeya kkaedara so I love me \nJom bujokhaedo neomu areumdaun geol \nI’m the one I should love")
db.session.add(piece)

piece = Piece(writerID=5, title="TOUCH", genre="Fresh", text="(maeil) jogeumsshik sayeogan \n(suthan) neowaye shigan neol hyanghae meomchun\nGirl ppajyeodeul geot gateun touch ne songire hana dul")
db.session.add(piece)

db.session.commit()

user_list = List(writerID = 1, pieceID = 1)
db.session.add(user_list)

user_list = List(writerID = 2, pieceID = 1)
db.session.add(user_list)

user_list = List(writerID = 3, pieceID = 1)
db.session.add(user_list)

user_list = List(writerID = 4, pieceID = 1)
db.session.add(user_list)

user_list = List(writerID = 5, pieceID = 1)
db.session.add(user_list)
db.session.commit() 

rating = Rating(writerID = 2, pieceID = 1, rate = 4)
db.session.add(rating)

rating = Rating(writerID = 3, pieceID = 2, rate = 3)
db.session.add(rating)

rating = Rating(writerID = 2, pieceID = 3, rate = 2)
db.session.add(rating)

rating = Rating(writerID = 4, pieceID = 4, rate = 1.25)
db.session.add(rating)

rating = Rating(writerID = 5, pieceID = 5, rate = 5)
db.session.add(rating)

db.session.commit()

review = Reviews(writerID = 2, pieceID = 3, text = "it's ayt")
db.session.add(review)

review = Reviews(writerID = 3, pieceID = 2, text = "i liked it")
db.session.add(review)

review = Reviews(writerID = 4, pieceID = 1, text = "deep")
db.session.add(review)

review = Reviews(writerID = 5, pieceID = 1, text = "i cried")
db.session.add(review)

review = Reviews(writerID = 2, pieceID = 1, text = "IM SCREAMING")
db.session.add(review)

db.session.commit()

