import ply.lex as lex
import ply.yacc as yacc
import math
def text_to_num(text):
	num_words = {}
	units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen",
	]
	tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
	scales = ["hundred", "thousand", "million", "billion", "trillion"]
	num_words["and"] = (1, 0)

	for index, word in enumerate(units): 
		num_words[word] = (1, index)
	for index, word in enumerate(tens): 
        	num_words[word] = (1, index * 10)
	for index, word in enumerate(scales):   
		num_words[word] = (10 ** (index * 3 or 2), 0)
	
	current = result = 0

	scale, increment = num_words[word]
	current = current * scale + increment
	if scale > 100:
		result += current
		current = 0
	number = result + current	
	return int(number)

def main(s):
	error = []
	multtext = ('multiplied','multiplied by','times','into','multiplies','multiplies by',)
	divtext = ('by','divided by','divide by','divides','divided',)
	powtext = ('power','raised to','raised',)

	tokens = ('ALPHANUM','NUMBER','PLUS','MINUS','TIMES','DIVIDE','LPAREN','RPAREN','POWER','LOG','FACTORIAL','TRIGO')

	t_PLUS      = r'(\+)|((?i)plus)'
	t_TRIGO     = r'(((?i)sin)|((?i)cos)|((?i)tan)|((?i)cosec)|((?i)cot)|((?i)sec))'
	t_FACTORIAL = r'(!)|((?i)factorial)'
	t_MINUS     = r'(-)|((?i)minus)'
	t_TIMES     = r'(\*)|((?i)multiplie(d|s)(\ by)?|(?i)time(s|\ of)?|(?i)into)'
	t_DIVIDE    = r'(/)|((?i)divide(d|s)?(\ by)?|(?i)by)'
	t_POWER     = r'(\^)|((?i)raised(\ to)?|(?i)power)'
	t_LOG       = r'(?i)log(\ of)?'
	t_LPAREN    = r'\('
	t_RPAREN    = r'\)'
	def t_ALPHANUM(t):
		r'((zero|one|two|three|fourteen|five|sixteen|seventeen|eighteen|nineteen|ten|eleven|twelve|thirteen|four|fifteen|sixty\
        	|seventy|eighty|ninety|twenty|thirty|forty|fifty|six|seven|eigh|nine|hundred|thousand|million|billion|trillion|and)(\s?))+'
		return t
	def t_NUMBER(t):
		r'\d+'
		try:
			t.value = int(t.value)
		except ValueError:
			t.value = 0
		return t
	def t_error(t):
		error.append(t.value)
		t.lexer.skip(1)
	t_ignore = ' \t'
	lexer = lex.lex()
	lexer.input(s)
	precedence = (('left','PLUS','MINUS'),('left','TIMES','DIVIDE'),('left','LOG','TRIGO'),('left','POWER','FACTORIAL'),('right','UMINUS'),)
	def p_expression_binop(t):
		'''expression : expression PLUS expression
		   	      | expression MINUS expression
			      | expression TIMES expression
			      | expression POWER expression
			      | expression DIVIDE expression'''
		if t[2]   == '+' or 'plus' in t[2].lower()   : t[0] = t[1] + t[3]
		elif t[2] == '-' or "minus" in t[2].lower()  : t[0] = t[1] - t[3]
		elif t[2] == '*' or  t[2].lower() in multtext: t[0] = t[1] * t[3]	
		elif t[2] == '/' or  t[2].lower() in divtext : t[0] = t[1] / t[3]
		elif t[2] == '^' or  t[2].lower() in powtext : t[0] = t[1] ** t[3]

	def p_expression_uminus(t):
		'expression : MINUS expression %prec UMINUS'
		t[0] = -t[2]

	def p_expression_group(t):
		'expression : LPAREN expression RPAREN'
		t[0] = t[2]
	def p_expression_number(t):
		'expression : NUMBER'
		t[0] = t[1]
	
	def p_expresssion_unop(t):
		'''expression : LOG expression
			      | TRIGO expression'''
		if 'log' in t[1].lower(): t[0]   = math.log(t[2])
		if 'sin' in t[1].lower(): t[0]   = math.sin(math.radians(t[2]))
		if 'cos' in t[1].lower(): t[0]   = math.cos(math.radians(t[2]))
		if 'tan' in t[1].lower(): t[0]   = math.tan(math.radians(t[2]))
		if 'cosec' in t[1].lower(): t[0] = math.cosec(math.radians(t[2]))
		if 'cot' in t[1].lower(): t[0]   = math.cot(math.radians(t[2]))
		if 'sec' in t[1].lower(): t[0]   = math.sec(math.radians(t[2]))
	def p_expression_factorial(t):
		'expression : expression FACTORIAL'
		t[0] = math.factorial(t[1])

	def p_expression_alphanum(t):
		'expression : ALPHANUM'
		t[0] = text_to_num(t[1])

	def p_error(t):
		return ""
	
	parser = yacc.yacc(write_tables = 0, debug = 0)
	answer = parser.parse(s)
	if error and answer:
		error = " ".join(error)
		if (len(error)/len(s)) > 0.15:
			answer = ""
	response = {}
	response['type'] = 'calc'
	response['title'] = s 
	response['content'] = answer
	return response
