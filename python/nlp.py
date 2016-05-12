import time, random
hour = time.localtime(time.time()).tm_hour

def process(message):
	split_message = message.split()
	query = {}
	subject = ''
	x = 0
	for i in split_message:
		if i.lower() in ['find','who']:
			query['type'] = 'wiki'
			for j in split_message:
				if x == 1:
					subject = subject + ' ' + j
				if j == 'about' or j == 'is':
					x = 1
			if subject[-1] is '?':
				subject = subject[0:-1]
			if subject[0] is ' ':
				subject = subject[1:]
			query['subject'] = subject
        
		elif i.lower() == 'what':
			x = 1
			query['type'] = 'wiki'
			for j in split_message:
				if j.lower() not in ['what','is','by']:
					subject = subject + ' ' + j
					calcwords = ['plus','+','minus','-','multiplied','divided','/']
					if j in calcwords:
						query['type'] = 'calc'
			query['subject'] = subject
			if query['type'] == 'wiki':
						if subject[-1] is '?':
							subject = subject[0:-1]
						if subject[0] is ' ':
							subject = subject[1:]
						query['subject'] = subject
			temp = query['subject']
			if temp[0].isdigit() == True:
				query['type'] = 'calc'
		elif i.lower() in ['message','tell'] :
			x = 1
			p = 1
			query['sender'] = 'sender'
			if i != 'take':
				for j in split_message:
					if j not in ['that','to','message','tell']:
						if p is 1:
							query['recipient'] = j
							p = 2
						else:
							subject = subject + ' ' + j
			query['subject'] = subject
			if query['recipient'] == 'me':
				subject = query['subject']
				if subject[0] == ' ':
					subject = subject[1:]
				if subject[-1] == ' ':
					subject = subject[:-1]
				query['subject'] = subject
				new_query = {}
				new_query['type'] = 'wiki'
				y = 0
				for u in query:
					if u[0:5].lower() == 'about':
						y = 1
					elif u[0:5].lower() == 'somet':
						y = 2
					if y == 1 or y == 2:
						new_query['subject'] = u
				subject = new_query['subject']
				if y == 1:
					subject = subject[6:]
				elif y == 2:
					subject = subject[16:]
				new_query['subject'] = subject
				query = new_query
		elif i.lower() == 'calculate':
			x = 1
			query['type'] = 'calc'
			for j in split_message:
				if j.lower() not in ['calculate','by']:
					subject = subject + ' ' + j
			subject = subject[1:]
			query['subject'] = subject
		if x == 1:
			return query
		else:
                       return  {'type':'error','error':'I do not understand'}

def welcome():
	welcome_greetings = [
		'Hello there',
		'Hola',
		'Hi there',
		'Hey there',
		'Namastey',
		'Hello',
		'Hi',
		'Hey']
	return welcome_greetings[int(random.uniform(0, 4))]
    
def greet():
	if hour > 3 and hour < 8:
		return '(You\'re up rather early)'
	elif hour > 7 and hour < 12:
		return 'Good Morning!'
	elif hour > 11 and hour < 16:
		return 'Good Afternoon!'
	elif hour > 15 and hour < 21:
		return 'Good Evening!'
	elif hour > 22 and hour < 25 or hour > 0 and hour < 4:
		return '(It\'s late)'

def start():
	conversation_starters = [
		'What can I do for you?',
		'What is it that you want me to do?',
		'What do you need me to do?',
		'What do you have for me?',
		'What do you want me to do?',
		'What can I help you with?']
	return conversation_starters[int(random.uniform(0, 5))]

def continue_or_not():
	continue_statements = [
		'Anything else I can help you with?',
		'What else do you want me to do?',
		'What else do you need to get done?',
		'What else do you have for me?',
		'Anything else you want me to do?',
		'What else can I do for you?',
		'Is there something else I can help you with?',
		'Is there something else I can do for you?',
		'Is there anything else I can do for you?']
	return {"type":"continue_or_not","content":continue_statements[int(random.uniform(0, 7))]}

def is_continuing(z):
	continuing_statements = [
		'Yes',
		'yes',
		'You can',
		'you can',
		'Sure',
		'sure',
		'Of course',
		'of course',
		'Surely',
		'surely',
		'Definitely',
		'definitely',
		'Please do',
		'please do']
	for x in continuing_statements:
		if x == z:
			return 1
	return 0

def parting():
	parting_statements_1 = [
		'You know where to find me',
		'Okay',
		'Hope to see you soon',
		'You take care',
		'Have a good one'
		'I\'m always available here']
	parting_statements_2 = [
		'Bye!',
		'Au Revoir!',
		'Ciao!',
		':)']
	return {"type":"parting","content":parting_statements_1[int(random.uniform(0, 4))]+', '+parting_statements_2[int(random.uniform(0, 3))]}

def is_concluding(z):
	conclusive_statements = [
		'Bye',
		'bye',
		'No',
		'no',
		'Nothing',
		'nothing',
		'That\'ll be all',
		'that\'ll be all',
		'Thatll be all',
		'thatll be all',
		'That\'s it',
		'that\'s it',
		'Thats it',
		'thats it',
		'That\'s all',
		'that\'s all',
		'Thats all',
		'thats all',
		'Nope',
		'nope',
		'I\'m done',
		'i\'m done',
		'Im done',
		'im done',
		'You can go',
		'you can go',
		'You may go',
		'you may go'
		'Ho gaya',
		'ho gaya']
	if z in conclusive_statements:
		return True
	return False

def on_load_function():
	return {"type":"welcome","content":""}#"content":welcome()+', '+greet()}
