# list of tokens
# storing and printing of variables, integer muna
# specify sa pagrun ng python yung filename
# not \n sensitive
# string variable value has ""
# CONSIDER ARRAY IN TYPE CHECKING
# KUNG MAY TIME: LINE NUMBER SA PARSING
# TYPE CASTING (kung may time)
# float and int can be stored vice versa

# PAALALA
# need anong line number ang mali
# wag makalimutan lagyan ng error
# always try except

import sys
filename=sys.argv[-1]
file=open(filename, "r")

import ply.lex as lex

#list of reserved words
reserved={
	'INTEGER':'INTEGER',
	'FLOAT':'FLOAT',
	'STRING':'STRING',
	'VARIABLES':'VARIABLES',
	'PAKITA':'PAKITA',
	'BASA':'BASA',
	'IARRAY':'IARRAY',
	'FARRAY':'FARRAY',
	'SARRAY':'SARRAY'
}

#list of token names
tokens=['NAME', 'LITSTRING', 'LITINTEGER', 'LITFLOAT', 'EQUAL', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER', 'MODULO']+list(reserved.values())
literals=['{','}','(',')']

#regular expression rules
def t_LITSTRING(t):
	r'\".*\"'
	str=t.value
	new_str=""
	escaped=0
	for i in range(0, len(str)):
		c=str[i]
		if escaped:
			#print("you there")
			if c=="n":
				c="\n"
			elif c=="t":
				c="\t"
			elif c=="\\":
				#print("you there1")
				c="\\"
			escaped=0
		elif c=="\\":
			#print("ESCAPED")
			escaped=1
			continue		
		new_str+=c
	t.value=new_str
	return t

def t_LITFLOAT(t):
	r'\d+[.]\d+'
	try:
		t.value = float(t.value)
	except ValueError:
		print("Value too large for float.")
		print("Error at line ", end="")
		print(t.lineno)
		sys.exit()
		t.value = 0.0
	return t

def t_LITINTEGER(t):
	r'\d+'
	try:
		t.value = int(t.value)
	except ValueError:
		print("Value to large for integer.")
		print("Error at line ", end="")
		print(t.lineno)
		sys.exit()
		t.value = 0
	return t
	
def t_ID(t):
	r'[A-Z]+'
	t.type=reserved.get(t.value, 'ID') # default value ay ID if hindi siya nasa reserved
	if t.type =='ID':
		print("Illegal character '%s' at line " % t.value, end="")
		print(t.lineno)
		sys.exit()
	else:
		return t

#token names rules
t_NAME=r'[a-z][a-z0-9_]*'
#put EQUAL EQUAL HERE
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_POWER = r'\^'
t_MODULO = r'\%'
t_EQUAL=r'=' #ISAMA SI EQUAL SA TOKEN LIST

def t_lbrace(t):
	r'\{'
	t.type='{'
	return t

def t_rbrace(t):
	r'\}'
	t.type='}'
	return t

def t_lparen(t):
	r'\('
	t.type='('
	return t;
	
def t_rparen(t):
	r'\)'
	t.type=')'
	return t
	
t_ignore=' \t'

#line number count
def t_newline(t):
	r'\n+'
	t.lexer.lineno+=len(t.value)

def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	print("Error at line ", end="")
	print(t.lineno)
	sys.exit()
	#t.lexer.skip(1)

lexer=lex.lex()

import ply.yacc as yacc

precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE', 'MODULO'),
	('right','POWER'),
    ('right','UMINUS'),
    )

#list of variable names
variable_names = {}

#declaring of variables then rest of program
def p_program_start(t):
	'''program : init body 
			   | body 
			   | init '''
			   
#pwedeng walang VARIABLES

def p_init_variable(t):
	'''init : VARIABLES '{' vardecnames '}' '''
#dapat may laman

#initializing 0 as value of variables
#when adding to array, type matters. For now, empty array
def p_vardecnames_names(t):
	'''vardecnames : INTEGER NAME vardecnames 
				 | FLOAT NAME vardecnames
				 | STRING NAME vardecnames
				 | IARRAY NAME vardecnames
				 | FARRAY NAME vardecnames
				 | SARRAY NAME vardecnames
				 | INTEGER NAME 
				 | FLOAT NAME
				 | STRING NAME
				 | IARRAY NAME
				 | FARRAY NAME
				 | SARRAY NAME
	'''
	if t[1]=='INTEGER':
		variable_names[t[2]]=[t[1], 0]
	elif t[1]=='FLOAT':
		variable_names[t[2]]=[t[1], 0.0]
	elif t[1]=='STRING':
		variable_names[t[2]]=[t[1], ""]
	elif t[1]=='IARRAY' or t[1]=='FARRAY' or t[1]=='SARRAY':
		variable_names[t[2]]=[t[1], []]

#for each statement in rest of program 
def p_body_state(t):
	'''body : body statement
			| statement '''
		
def p_statement_print(t):
	'''statement : PAKITA '(' NAME ')' 
				 | PAKITA '(' LITSTRING ')' '''
	#print(t[3])
	if t[3][0]=='\"' and t[3][len(t[3])-1] =='\"':
		#print("hi")
		print(t[3][1:len(t[3])-1], end="")
	else:
		# try except
		try: 
			temp=variable_names[t[3]]
		except LookupError:
			print("Variable name '%s' not found." % t[3])
			sys.exit()
		if variable_names[t[3]][0] == 'STRING':
			#print("hello1")
			print(variable_names[t[3]][1][1:len(variable_names[t[3]][1])-1], end="")
		else:
			print(variable_names[t[3]][1], end="")
		
def p_statement_read(t):
	#type checking sa basa dapat evaluated muna kung int float string same type
	'''statement : BASA '(' NAME ')' '''
	try:
		temp=variable_names[t[3]]
	except Exception:
		print("Undefined name '%s'" % t[1])
		sys.exit()

	if variable_names[t[3]][0]=='INTEGER':
		try:
			temp=input()
			temp=float(temp)
			temp=int(temp)
		except Exception:
			print("Expected type INTEGER for '%s'." % t[3]) #dagdag line
			sys.exit()
		#print(type(t[3]))
		variable_names[t[3]][1] = temp
	elif variable_names[t[3]][0]=='FLOAT':
		try:
			temp=float(input())
		except Exception:
			print("Expected type FLOAT for '%s'." % t[3])
			sys.exit()
		variable_names[t[3]][1] = temp
	elif variable_names[t[3]][0]=='STRING':
		temp=input()
		if temp[0]!='\"' and temp[len(temp)-1]!='\"':
			print("Input string should be enclosed in \"\".")
			sys.exit()
		else:
			variable_names[t[3]][1] = temp
	else:
		print("Parameter '%s' is not valid for BASA." % t[3])
		#variable_names[t[3]][1]=input()
		
def p_statement_assignment(t):
	#remember to check if actual type and expected type are compatible
	#assignment of literal and variables
	'''statement : NAME EQUAL expression'''
	#to be done in integer operations
	#if variablenames[t[1]][0] == 
	try:
		temp=variable_names[t[1]]
	except Exception:
		print("Undefined name '%s'" % t[1])
		sys.exit()

	if variable_names[t[1]][0]=='INTEGER':
		#print(type(t[3]))
		if type(t[3]).__name__!='int' and type(t[3]).__name__!='float':
			print("Expected type INTEGER for '%s'." % t[1]) #dagdag line
			sys.exit()
		else:
			variable_names[t[1]][1] = int(t[3])
	elif variable_names[t[1]][0]=='FLOAT':
		#print(type(t[3]).__name__)
		if type(t[3]).__name__!='int' and type(t[3]).__name__!='float':
			#print(type(t[3]).__name__)
			print("Expected type FLOAT for '%s'." % t[1])
			sys.exit()
		else:
			if type(t[3]).__name__=='int':
				variable_names[t[1]][1]=float(t[3])
			else:
				variable_names[t[1]][1] = t[3]
	elif variable_names[t[1]][0]=='STRING':
		if type(t[3]).__name__!='str':
			print("Expected type STRING for '%s'." % t[1])
			sys.exit()
		else:
			variable_names[t[1]][1] = t[3]
	#variable_names[t[1]][1] = t[3]
	
def p_expression_binop(t):
	'''expression : expression PLUS expression 
				  | expression MINUS expression
				  | expression TIMES expression
				  | expression DIVIDE expression
				  | expression POWER expression 
				  | expression MODULO expression '''
	if type(t[1]).__name__ == 'str' or type(t[1]).__name__== 'list':
		print("Invalid data types in '%s'." % t[1])
		sys.exit()
	elif type(t[3]).__name__=='str' or type(t[3]).__name__=='list':
		print("Invalid data types in '%s'." % t[3])
		sys.exit()
	else:
		if t[2] == '+': 
			t[0] = t[1] + t[3]
		elif t[2] == '-': 
			t[0] = t[1] - t[3]
		elif t[2] == '*': 
			t[0] = t[1] * t[3]
		elif t[2] == '/': 
			t[0] = t[1] / t[3]
		elif t[2] == '^': 
			t[0] = t[1] ** t[3]
		elif t[2] == '%':
			t[0] = t[1] % t[3]
			
	
def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = -t[2]
	
def p_expression_group(t):
    '''expression : '(' expression ')' '''
    t[0] = t[2]
	
def p_expression_types(t):
	'''expression : LITSTRING
				  | LITINTEGER
				  | LITFLOAT'''
	t[0] = t[1]
	
def p_expression_var(t):
	'''expression : NAME'''
	try:
		t[0] = variable_names[t[1]][1]
	except LookupError:
		print("Undefined name '%s'" % t[1])
		sys.exit()
	
	
def p_error(t):
	print("Syntax error at line '%s'" % t.value)
	sys.exit()
	
parser=yacc.yacc()
while True:
	line=file.read()
	if not line:
		file.close()
		break
	else:
		lexer.input(line)
		parser.parse(line)