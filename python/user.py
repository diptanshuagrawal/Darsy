import MySQLdb

def login(email, password):
	connection = MySQLdb.connect (host = "127.0.0.1", user = "root", passwd = "")
	cursor = connection.cursor ()
	cursor.close()
	connection.close ()

def new_user(name,email):	
	connection = MySQLdb.connect (host = "127.0.0.1", user = "root", passwd = "")
	cursor = connection.cursor ()
	cursor.execute("SELECT ID FROM dutchman.Users WHERE Email=%s",[email])
	existing_user = cursor.fetchall()
	
	if len(existing_user) is not 0:
		print("Existing User")
		return
		
	cursor.execute("INSERT INTO dutchman.Users(Name,Email) VALUES(%s,%s)",(name,email))
	connection.commit()
	cursor.execute("SELECT ID FROM dutchman.Users WHERE Email=%s",[email])
	ID = cursor.fetchall()
	ID = ID[0][0]
	command = "CREATE TABLE "+ email
	query = ("CREATE DATABASE " + email,)
	query.append(command + ".inbox (ID INT NOT NULL AUTO_INCREMENT, message VARCHAR(2000) NOT NULL, recipient VARCHAR(200),read INT NOT NULL)")
	query.append(command + ".outbox (ID INT NOT NULL AUTO_INCREMENT, message VARCHAR(2000) NOT NULL, sender VARCHAR(200),read INT NOT NULL))")
	query.append(command + ".queries (ID INT NOT NULL AUTO_INCREMENT, message VARCHAR(2000) NOT NULL, response VARCHAR(2000))")
	query.append(command + ".friends (SR INT NOT NULL AUTO_INCREMENT, ID INT NOT NULL)")
	cursor.executemany(query) 
	cursor.close()
	connection.close ()
	
def send_message(sender,recipient,message):
	connection = MySQLdb.connect (host = "127.0.0.1", user = "root", passwd = "")
	cursor = connection.cursor ()
	cursor.execute("INSERT INTO " +sender+ ".outbox (message,recipient) VALUES(%s,%s)",(message,recipient));
	cursor.execute("INSERT INTO " +recipient+ ".inbox (message,sender) VALUES(%s,%s)",(message,sender));
	connection.commit()
	cursor.close ()
	connection.close ()

def recieve_message(recipient):
	connection = MySQLdb.connect (host = "127.0.0.1", user = "root", passwd = "")
	cursor = connection.cursor ()
	query = "SELECT * FROM " +recipient".inbox"
	cursor.execute(query)
	messages = cursor.fetchall()
	connection.commit()
	cursor.close ()
	connection.close ()

def add_friend(user, friend):
	connection = MySQLdb.connect (host = "127.0.0.1", user = "root", passwd = "")
	cursor = connection.cursor ()
	cursor.execute("INSERT INTO " +user+ ".friend (ID) VALUES(%s)",[friend])
	connection.commit()
	cursor.close ()
	connection.close ()