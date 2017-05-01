# GENERAL RULE: laging either yung literal na of that type, or a variable of that type
# list of tokens
# storing and printing of variables, integer muna
# specify sa pagrun ng python yung filename
# not \n sensitive
# string variable value has ""
# CONSIDER ARRAY IN TYPE CHECKING
# KUNG MAY TIME: LINE NUMBER SA PARSING
# TYPE CASTING (kung may time)
# float and int can be stored vice versa
# PAKITA only gets name and literals(not return values from functions such as SAMA)

# PAALALA
# need anong line number ang mali
# wag makalimutan lagyan ng error
# always try except
# yung pakita dapat ay expression??????
# laman ng string ay "<string>"
import sys
filename=sys.argv[-1]
file=open(filename, "r")

variable_names = {}
class Node:
	def __init__(self, type, children=None, leaf=None):
		self.type=type
		if children:
			self.children = children
		else:
			self.children = []
		self.leaf = leaf

def parsing(node):
	if node.type == "program":
		parsing(node.children[0])
		#print(node.children[0].type)
	if(node.type == "body"):
		listnode=node.children
		#print(len(listnode))
		length=len(listnode)
		if(length == 2):
			#print('hallo')
			#print(listnode[0].type)
			parsing(listnode[0])
			#print("doneeee")
			#print(listnode[1].type)
			parsing(listnode[1])
			#print("weeee")
		else:
			parsing(listnode[0])
	if(node.type == 'statement'):
		listnode=node.children
		listleaf=node.leaf 
		if(listleaf[0] == 'pakita'):
			if(listleaf[1][0] == '\"' and listleaf[1][0] == '\"'):
				print(listleaf[1][1:len(listleaf[1])-1], end="")
			elif (variable_names[listleaf[1]][0]) == 'STRING':
				print(variable_names[listleaf[1]][1][1:len(variable_names[listleaf[1]][1])-1], end="")
			else:
				print(variable_names[listleaf[1]][1], end="")
		elif(listleaf[0] == "basa"):			
			if variable_names[listleaf[1]][0]=='INTEGER':
				try:
					temp=input()
					temp=float(temp)
					temp=int(temp)
				except Exception:
					print("Expected type INTEGER for '%s'." % listleaf[1]) #dagdag line
					sys.exit()
				variable_names[listleaf[1]][1] = temp
			elif variable_names[listleaf[1]][0]=='FLOAT':
				try:
					temp=float(input())
				except Exception:
					print("Expected type FLOAT for '%s'." % listleaf[1])
					sys.exit()
				variable_names[listleaf[1]][1] = temp
			elif variable_names[listleaf[1]][0]=='STRING':
				temp=input()
				if temp[0]!='\"' and temp[len(temp)-1]!='\"':
					print("Input string should be enclosed in \"\".")
					sys.exit()
				else:
					variable_names[listleaf[1]][1] = temp
			else:
				print("Parameter '%s' is not valid for BASA." % listleaf[1])
		elif (listleaf[0] == "assignment"):
			listnode = node.children
			length = len(listnode)
			listleaf = node.leaf
			if(length==2):
				a=parsing(listnode[0])
				b=parsing(listnode[1])
				if(variable_names[listleaf[1]][0]== 'ARRAY'):
					if(type(a).__name__ == 'int'):
						if(a >=0 and a<len(variable_names[listleaf[1]][1])):
							variable_names[listleaf[1]][1][a] = b
						else:
							print("Index out of bounds for '%s'." % listleaf[1])
							sys.exit()
					else:
						print("Expected INTEGER type for '%s'." % listleaf[1])
						sys.exit()
				else:
					print("Expected ARRAY type for '%s'." % listleaf[1])
					sys.exit()
			else:				
				a = parsing(listnode[0])
				if variable_names[listleaf[1]][0]=='INTEGER':
					#print(type(t[3]))
					if type(a).__name__!='int' and type(a).__name__!='float':
						print("Expected type INTEGER for '%s'." % listleaf[1]) #dagdag line
						sys.exit()
					else:
						variable_names[listleaf[1]][1] = int(a)
				elif variable_names[listleaf[1]][0]=='FLOAT':
					#print(type(t[3]).__name__)
					if type(a).__name__!='int' and type(a).__name__!='float':
						#print(type(t[3]).__name__)
						print("Expected type FLOAT for '%s'." % listleaf[1])
						sys.exit()
					else:
						if type(a).__name__=='int':
							variable_names[listleaf[1]][1]=float(a)
						else:
							variable_names[listleaf[1]][1] = a
				elif variable_names[listleaf[1]][0]=='STRING':
					if type(a).__name__!='str':
						print("Expected type STRING for '%s'." % listleaf[1])
						sys.exit()
					else:
						variable_names[listleaf[1]][1] = a
					#print(variable_names[listleaf[1]][1])
		elif(listleaf[0] == "push"):
			try:
				temp = variable_names[listleaf[1]][1]
			except LookupError:
				print("Undefined name '%s'" % listleaf[1])
				sys.exit()
			if variable_names[listleaf[1]][0] == 'ARRAY':
				a = parsing(listnode[0])
				variable_names[listleaf[1]][1].append(a)
			else:
				print("Expected ARRAY type for parameter 1 of DAGDAG. Actual type passed for '%s' is " % temp, end="")
				print("'%s'." % variable_names[listleaf[1]][0])
				sys.exit()
	elif(node.type == "expression"):
		listnode = node.children
		listleaf = node.leaf
		if(listleaf[0] == "binop"):
			a = parsing(listnode[0])
			b = parsing(listnode[1])
			if type(a).__name__ == 'str' or type(a).__name__== 'list':
				print("Invalid data types in '%s'." % a)
				sys.exit()
			elif type(b).__name__=='str' or type(b).__name__=='list':
				print("Invalid data types in '%s'." % b)
				sys.exit() 
			else:
				if listleaf[1] == '+': 
					return a + b
				elif listleaf[1] == '-': 
					return a - b
				elif listleaf[1] == '*': 
					return a * b
				elif listleaf[1] == '/': 
					return a / b
				elif listleaf[1] == '^': 
					return a ** b
				elif listleaf[1] == '%':
					return a % b
		elif(listleaf[0] == "uminus"):
			a = parsing(listnode[0])
			return a*-1
		elif(listleaf[0] == "group"):
			return parsing(listnode[0])
		elif(listleaf[0] == "literals"):
			return listleaf[1]
		elif(listleaf[0] == "var"):
			return variable_names[listleaf[1]][1]
		elif(listleaf[0] == "concat"):
			str1 = "" 
			str2 = ""
			try:
				temp1 = variable_names[listleaf[1]]
				#print(temp1)
			except Exception:
				if listleaf[1][0]=='\"' and listleaf[1][len(listleaf[1])-1] =='\"':
					temp1 = listleaf[1][0:len(listleaf[1])-1]
					str1 = temp1
				else:
					print("Undefined name '%s'" % listleaf[1])
					sys.exit()
			try:
				temp2 = variable_names[listleaf[2]]
				#print(temp2)
			except Exception:
				if listleaf[2][0]=='\"' and listleaf[2][len(listleaf[2])-1] =='\"':
					temp2 = listleaf[2][1:len(listleaf[2])]
					str2 = temp2
				else:
					print("Undefined name '%s'" % listleaf[2])
					sys.exit()
			
			if(temp1[0] == 'STRING' and temp2[0] == 'STRING'):
				str1 = temp1[1][0:len(temp1[1])-1]
				str2 = temp2[1][1:len(temp2[1])]
			elif(temp1[0] == 'STRING' and temp2 == str2):
				str1 = temp1[1][0:len(temp1[1])-1]
			elif (temp2[0] == 'STRING' and temp1 == str1):
				str2 = temp2[1][1:len(temp2[1])]
			else:
				print("Expected strings as parameters for SAMA function")
				sys.exit()
			return str1+str2
		elif(listleaf[0] == "strlen"):
			temp=variable_names[listleaf[1]]
			if temp[0] == 'STRING':
				return len(temp[1]) -2
			elif temp[0] == 'ARRAY':
				return len(temp[1])
		elif(listleaf[0] == "substrsearch"):
			str1 = ""
			str2 = ""
			try:
				temp1 = variable_names[listleaf[1]]
				if temp1[0] != 'STRING':
					print("Error at '%s' : Expected parameter 1 of type STRING in HANAP function\n" % listleaf[1])
					sys.exit()
				else:
					str1 = temp1[1]
			except Exception:
				if listleaf[1][0]=='\"' and listleaf[1][len(listleaf[1])-1] =='\"':
					str1 = listleaf[1]
				else:
					print("Undefined name '%s'" % listleaf[1])
					sys.exit()
			try:
				temp2 = variable_names[listleaf[2]]
				if temp2[0] != 'STRING':
					print("Error at '%s' : Expected parameter 2 of type STRING in HANAP function\n" % listleaf[2])
					sys.exit()
				else:
					str2 = temp2[1]
			except Exception:
				if listleaf[2][0]=='\"' and listleaf[2][len(listleaf[2])-1] =='\"':
					str2 = listleaf[2]
				else:
					print("Undefined name '%s'" % listleaf[2])
					sys.exit()
			return str1[1:len(str1)-1].find(str2[1:len(str2)-1])
		elif(listleaf[0] == "stringindexing"):
			index = -1
			str = ""
			try:
				temp = variable_names[listleaf[1]]
				if temp[0] != 'STRING':
					print("Error at '%s' : Expected parameter 1 of type STRING in SA function\n" % listleaf[1])
					sys.exit()
				else:
					str = temp[1][1:len(temp[1])-1]
			except Exception:
				print("Error at '%s' : Expected initialized variable of type STRING" % listleaf[1])
				sys.exit()
			a = parsing(listnode[0])
			if type(a).__name__ == 'int':
				if a < 0 or a > len(str) - 1:
					print("Index out of bounds for SA.")
					sys.exit()
				return "\""+str[a]+"\""
			else:
				print("Index must be of INTEGER type in '%s'." % t[1])
				sys.exit()
		elif(listleaf[0] == "arrayaccess"):
			try:
				temp = variable_names[listleaf[1]]
			except Exception:
				print("Undefined name '%s'." % listleaf[1])
				sys.exit()
			a = parsing(listnode[0])
			if type(a).__name__ == 'int':
				if a < 0 or a > len(variable_names[listleaf[1]][1]) - 1:
					print("Index out of bounds for '%s'." % listleaf[1])
					sys.exit()
				return variable_names[listleaf[1]][1][a]
			else:
				print("Index must be of INTEGER type in '%s'." % listleaf[1])
				sys.exit()
			# while(len(listnode[0].children)!=0):
				# listnode=listnode[0].children
				# if(listnode[0].leaf[0] == 'INTEGER'):
					# variable_names[listnode[0].leaf[1]]=[listnode[0].leaf[0], 0]
					# print(variable_names[listnode[0].leaf[1]])
				# elif(listnode[0].leaf[0] == 'FLOAT'):
					# variable_names[listnode[0].leaf[1]]=[listnode[0].leaf[0], 0.0]
					# print(variable_names[listnode[0].leaf[1]])
				# elif(listnode[0].leaf[0] == 'STRING'):
					# variable_names[listnode[0].leaf[1]]=[listnode[0].leaf[0], ""]
					# print(variable_names[listnode[0].leaf[1]])
				# elif(listnode[0].leaf[0] == 'ARRAY'):
					# variable_names[listnode[0].leaf[1]]=[listnode[0].leaf[0], []]
					# print(variable_names[listnode[0].leaf[1]])

import ply.lex as lex

#list of reserved words
reserved={
	'INTEGER':'INTEGER',
	'FLOAT':'FLOAT',
	'STRING':'STRING',
	'VARIABLES':'VARIABLES',
	'PAKITA':'PAKITA',
	'BASA':'BASA',
	'SAMA' : 'SAMA',
	'HABA' : 'HABA',
	'HANAP' : 'HANAP',
	'SA' : 'SA',
	'DAGDAG' : 'DAGDAG',
	'ARRAY' : 'ARRAY',
	'PAG' : 'PAG',
	'KUNDIPAG' : 'KUNDIPAG',
	'KUNDI' : 'KUNDI'
}

#list of token names
tokens=['NAME', 'LITSTRING', 'LITINTEGER', 'LITFLOAT', 'ISEQUAL', 'LTE', 'GTE', 'LT', 'GT', 'NE', 'EQUAL', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER', 'MODULO']+list(reserved.values())
literals=['{','}','(',')',',','[',']']

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
t_ISEQUAL = r'=='
t_LTE = r'<='
t_GTE = r'>='
t_LT = r'<'
t_GT = r'>'
t_NE = r'!='
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

def t_comma(t):
	r','
	t.type = ','
	return t
	
def t_lsquare(t):
	r'\['
	t.type='['
	return t
	
def t_rsquare(t):
	r'\]'
	t.type=']'
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
	#('nonassoc',  'IFX'), # bring this back later
	('nonassoc', 'KUNDI'),
	('left', 'GT', 'LT', 'GTE', 'LTE', 'ISEQUAL', 'NE'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE', 'MODULO'),
	('right','POWER'),
    ('right','UMINUS') # bring this back later
    )

#list of variable names

#declaring of variables then rest of program
def p_program_completestart(t):
	'''program : init body '''
	t[0] = Node("program", [t[2]],[])
	parsing(t[0])
	
def p_program_initstart(t):
	'''program : init '''
			   
def p_program_bodystart(t):
	'''program : body '''
	t[0] = Node("program", [t[1]],[])
	parsing(t[0])
#pwedeng walang VARIABLES

def p_init_variable(t):
	'''init : VARIABLES '{' vardecnames '}' '''
#dapat may laman

#DAGDAG KAALAMANAN ginawang "" ang value ng empty string
#initializing 0 as value of variables
#when adding to array, type matters. For now, empty array
def p_vardecnames_iternames(t):
	'''vardecnames : INTEGER NAME vardecnames 
				   | FLOAT NAME vardecnames
				   | STRING NAME vardecnames
				   | ARRAY NAME vardecnames 
				   | INTEGER NAME 
				   | FLOAT NAME
				   | STRING NAME
				   | ARRAY NAME'''
	try:
		temp = variable_names[t[2]]
		print("Identifier '%s' is already taken." % t[2])
		sys.exit()
	except Exception:
		if t[1]=='INTEGER':
			variable_names[t[2]]=[t[1], 0]
		elif t[1]=='FLOAT':
			variable_names[t[2]]=[t[1], 0.0]
		elif t[1]=='STRING':
			variable_names[t[2]]=[t[1], "\"\""]
		elif t[1]=='ARRAY':
			variable_names[t[2]]=[t[1], []]


# def p_vardecnames_names(t):
	# '''vardecnames : 
	# '''
	# t[0] = Node("vardecnames",[],[t[1],t[2]])
	# 

#for each statement in rest of program 
def p_body_bodystate(t):
	'''body : body statement '''
	#print("here")
	t[0] = Node("body", [t[1], t[2]],[])
	
def p_body_state(t):
	'''body : statement '''
	t[0] = Node("body", [t[1]],[])
	
#printing sa array, pag may string, ipiprint kasama ang ""
def p_statement_print(t):
	'''statement : PAKITA '(' NAME ')' 
				 | PAKITA '(' LITSTRING ')' '''
	#print(t[3])
	if t[3][0]=='\"' and t[3][len(t[3])-1] =='\"':
		t[0] = Node("statement", [], ["pakita", t[3]])
		#print("hi")
		#print(t[3][1:len(t[3])-1], end="")
	else:
		# try except
		try: 
			temp=variable_names[t[3]]
		except LookupError:
			print("Variable name '%s' not found." % t[3])
			sys.exit()
		t[0] = Node("statement", [], ["pakita",t[3]])
		
def p_statement_read(t):
	#type checking sa basa dapat evaluated muna kung int float string same type
	'''statement : BASA '(' NAME ')' '''
	try:
		temp=variable_names[t[3]]
	except Exception:
		print("Undefined name '%s'" % t[3])
		sys.exit()
	t[0] = Node("statement",[],["basa",t[3]])
def p_statement_assignment(t):
	#remember to check if actual type and expected type are compatible
	#assignment of literal and variables
	'''statement : NAME EQUAL expression
				 | NAME '[' expression ']' EQUAL expression 
	'''
	#to be done in integer operations
	#if variablenames[t[1]][0] == 
	if(t[2] == '='):
		try:
			temp=variable_names[t[1]]
		except Exception:
			print("Undefined name '%s'" % t[1])
			sys.exit()
		t[0] = Node("statement",[t[3]],["assignment",t[1]])
	else:
		try:
			temp=variable_names[t[1]]
		except Exception:
			print("Undefined name '%s'." % t[1])
			sys.exit()
		t[0] = Node("statement",[t[3],t[6]],["assignment",t[1]])
	# #variable_names[t[1]][1] = t[3]
	
def p_statement_push(t):
	''' statement : DAGDAG '(' NAME ',' expression ')' '''
	t[0] = Node("statement", [t[5]], ["push", t[3]])
		
# def p_statement_conditionals(t):
	# '''statement : PAG '(' cond ')' '{' body '}' %prec IFX 
				 # | PAG '(' cond ')' '{' body '}' elseblocks '''
	# flag = true
# def p_elseblocks_elifblocks(t):
	# '''elseblocks : elseifblock
				  # | elseblock '''
				  
# def p_elseblock_else(t):
	# '''elseblock : '''
	# flag = false
# def p_elseifblock_elifblock(t):
	# '''elseifblock : '''
	
# def p_cond_conditions(t):
	# ''' cond : expression ISEQUAL expression 
			 # | expression NE expression 
			 # | expression GTE expression 
			 # | expression LTE expression 
			 # | expression LT expression 
			 # | expression GT expression 
	# '''
	# if (t[2] == "=="):
		# t[0] = t[1] == t [3]
	# elif (t[2] == ">="):
		# t[0] = t[1] >= t[3]
	# elif (t[2] == "<="):
		# t[0] = t[1] <= t[3]
	# elif (t[2] == "!="):
		# t[0] = t[1] != t[3]
	# elif (t[2] == ">"):
		# t[0] = t[1] > t[3]
	# elif (t[2] == "<"):
		# t[0] = t[1] < t[3]
	# else:
		# print("No such ", t[2], " opereator exist")

def p_expression_binop(t):
	'''expression : expression PLUS expression 
				  | expression MINUS expression
				  | expression TIMES expression
				  | expression DIVIDE expression
				  | expression POWER expression 
				  | expression MODULO expression '''
	t[0] = Node("expression",[t[1],t[3]],["binop",t[2]])
		
def p_expression_uminus(t):
	'expression : MINUS expression %prec UMINUS'
	t[0]=Node("expression",[t[2]],["uminus"])
	
def p_expression_group(t):
	'''expression : '(' expression ')' '''
	t[0] = Node("expression",[t[2]],["group"])
	
def p_expression_types(t):
	'''expression : LITSTRING
				  | LITINTEGER
				  | LITFLOAT'''
	t[0]=Node("expression",[],["literals",t[1]])
	
def p_expression_var(t):
	'''expression : NAME'''
	try:
		temp = variable_names[t[1]][1]
	except LookupError:
		print("Undefined name '%s'" % t[1])
		sys.exit()
	t[0] = Node("expression",[],["var", t[1]])
	
#SAMA can't accept 2 literals strings
def p_expression_concat(t):
	'''expression : SAMA '(' NAME ',' NAME ')' 
				  | SAMA '(' NAME ',' LITSTRING ')' 
				  | SAMA '(' LITSTRING ',' NAME ')' ''' 
	t[0] = Node("expression",[],["concat", t[3], t[5]])
	#t[0] = str1 + str2

# Haba only accepts string variables as a paramter
def p_expression_strlength(t):
	''' expression : HABA '(' NAME ')' '''
	try:
		temp = variable_names[t[3]]	
		if(temp[0] != 'STRING' and temp[0]!='ARRAY'):
			print("Expected STRING or ARRAY type on HABA function\n")
			sys.exit()
		
	except Exception: 
		print("Undefined name '%s'" % t[3])
		sys.exit()
	t[0] = Node("expression", [], ["strlen", t[3]])

#HANAP doesn't accept 2 literals as parameter
#DAGDAG KAALAMAN  HANAP follows python find function 
def p_expression_substrsearch(t):
	''' expression : HANAP '(' NAME ',' NAME ')'
				   | HANAP '(' NAME ',' LITSTRING ')'
				   | HANAP '(' LITSTRING ',' NAME ')'
	'''	
	t[0] = Node("expression", [], ["substrsearch", t[3], t[5]])

#Doesn't take literal string
def p_expression_stringdexing(t):
	''' expression : SA '(' NAME ',' expression ')'
	'''
	t[0] = Node("expression", [t[5]], ["stringindexing", t[3]])
	
def p_expression_arrayaccess(t):
	''' expression : NAME '[' expression ']' '''
	t[0] = Node("expression", [t[3]], ["arrayaccess", t[1]])
	
def p_error(t):
	print("Syntax error at line %s"  % t.lineno)
	print("	-> Found '%s' \n" % t.value)
	sys.exit()
	
parser=yacc.yacc()
while True:
	line=file.read()
	if not line:
		file.close()
		break
	else:
		lexer.input(line)
		#while True:
		#	tok=lex.token()
		#	if not tok:
		#		break
		#	else:
		#		print(tok)
		parser.parse(line)