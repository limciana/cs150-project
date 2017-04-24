# list of tokens
# storing and printing of variables, integer muna
# specify sa pagrun ng python yung filename

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
tokens=['NAME', 'LITSTRING']+list(reserved.values())
literals=['{','}','(',')']

#regular expression rules
def t_ID(t):
	r'[A-Z]+'
	t.type=reserved.get(t.value, 'ID') # default value ay ID if hindi siya nasa reserved
	return t
	
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

#token names rules
t_NAME=r'[a-z][a-z0-9_]*'
#put EQUAL EQUAL HERE
#t_EQUAL=r'=' #ISAMA SI EQUAL SA TOKEN LIST

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
	t.lexer.skip(1)

lexer=lex.lex()

import ply.yacc as yacc

#list of variable names
variable_names = {}

#declaring of variables then rest of program
def p_program_start(t):
	'''program : init body '''

def p_init_variable(t):
	'''init : VARIABLES '{' vardecnames '}' '''

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
		print(variable_names[t[3]][1], end="")
		
def p_statement_read(t):
	#type checking sa basa dapat evaluated muna kung int float string same type
	'''statement : BASA '(' NAME ')' '''
	if variable_names[t[3]][0] == 'INTEGER' or variable_names[t[3]][0] == 'FLOAT' or variable_names[t[3]][0] == 'STRING':
		variable_names[t[3]][1]=input()
		
#def p_statement_assignment(t):
	#remember to check if actual type and expected type are compatible
	#'''statement : NAME EQUAL expression'''
	#to be done in integer operations
	
def p_error(t):
	print("Syntax error at '%s'" % t.value)
	
parser=yacc.yacc()
while True:
	line=file.read()
	if not line:
		file.close()
		break
	else:
		lexer.input(line)
		parser.parse(line)