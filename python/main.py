#!/usr/bin/python3
print("Content-Type: text/html")
print()

import json
import MySQLdb
import sys
import wiki
import ssl
import cgi
import calculator
import nlp

def analyze(data):
	query = nlp.process(data)
	response = {}
	if(query['type'] == "wiki"):
		response = encyclopedia(query['subject'])
	if(query['type'] == "calc"):
		response = calculator.main(query['subject'])
	if(query['type'] == "error"):
		response = query
	return response

def encyclopedia(data):
	connection = MySQLdb.connect (host = "127.0.0.1", user = "root", passwd = "", db = "dutchman")
	cursor = connection.cursor ()
	cursor.execute ("SELECT response from Wikipedia WHERE query=%s",[data])
	respond = cursor.fetchall()
	response = {}
	response['type'] = 'wiki'
	if respond:
		response['content'] = respond[0][0]
		cursor.execute ("SELECT url from Wikipedia WHERE query=%s",[data])
		respond = cursor.fetchall()
		if respond:
			response['url'] = respond[0][0]
		cursor.execute ("SELECT title from Wikipedia WHERE query=%s",[data])
		respond = cursor.fetchall()
		if respond:
			response['title'] = respond[0][0]
	if 'title' not in response:
		response = wiki.info(data)
		if response['type'] == 'wiki':
			try:
				cursor.execute("INSERT INTO Wikipedia VALUES (%s,%s,%s,%s)",(data,response['title'],response['content'],response['url']))
				connection.commit()
			except:
				x = 1
	cursor.close ()
	connection.close
	return response

form = cgi.FieldStorage()
message = form.getvalue("message", "error")
response = {}
if message[-1] == '\n':
	message = message[:-1]
if message == "welcome":
	response  = nlp.on_load_function()
	response['content'] = response['content'] + ' ' + nlp.start()
elif message == "continue_or_not":
	response  = nlp.continue_or_not()
elif nlp.is_concluding(message):
	response = nlp.parting()
else:	
	response = analyze(message)
print(json.dumps(response))
sys.exit()
