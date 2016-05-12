import wikipedia

def info(topic):
	response = {}
	response["type"] = "wiki"
	try:
		page = wikipedia.page(topic)
		response['title'] = page.title
		response['url'] = page.url
		response['content'] = wikipedia.summary(page.title,sentences = 5)
		if len(response['content']) < 200:
			response['content'] = wikipedia.summary(page.title,sentences = 10)
	except Exception as error:
		ename = type(error).__name__
		if ename == 'DisambiguationError':
			page = wikipedia.page(error.options[0])
			response['title'] = page.title
			response['url'] = page.url
			response['content'] = wikipedia.summary(page.title,sentences = 2)
			if len(response['content']) < 200:
				response['content'] = wikipedia.summary(page.title,sentences = 10)
		elif ename == 'HTTPTimeoutError':
			response['type'] = "error"
			response['error'] = "I couldn't reach wikipedia"
		elif ename == 'PageError':
			response['type'] = "error"
			response['error'] = "I couldn't find anything on wikipedia"
		else:
			response['type'] = "error"
			response['error'] = "Unknown error occured while reaching wikipedia" 

	return response


