from sys import *

tokens = []
num_stack = []
symbols = {}

def open_file(filename):
	extension = filename.split(".")
	if extension[1] == "69":
		data = open(filename, "r").read()
		data += "<EOF>"
		return data
	else:
		print("Trantado: Mali ang file extension mo! Dapat .69 ang file extension")
		return ""
def lex(filecontents):
	tok = ""
	state = 0
	isexpr = 0
	varstarted = 0
	var = ""
	STRING = ""
	expr = ""
	n = ""
	filecontents = list(filecontents)
	for char in filecontents:
		tok += char
		if tok == " ":
			if state == 0:
				tok = ""
			else:
				tok = " "
		elif tok == "\n" or tok == "<EOF>":
			if expr != "" and isexpr == 1:
				tokens.append("EXPR:" + expr)
				expr = ""
			elif expr != "" and isexpr == 0:
				tokens.append("NUM:" + expr)
				expr = ""
			elif var != "":
				tokens.append("VAR:" + var)
				var = ""
				varstarted = 0
			tok = ""
		elif tok == "=" and state == 0:
			if expr != "" and isexpr == 0:
				tokens.append("NUM:" + expr)
				expr = ""
			if var != "":
				tokens.append("VAR:" + var)
				var = ""
				varstarted = 0	
			if tokens[-1] == "EQUALS":
				tokens[-1] = "EQEQ"
			else:
				tokens.append("EQUALS")
			tok = ""
		elif tok == "$" and state == 0:
			varstarted = 1
			var += tok
			tok = ""
		elif varstarted == 1:
			if tok == "<" or tok == ">":
				if var != "":
					tokens.append("VAR:" + var)
					var = ""
					varstarted = 0
			var += tok
			tok = ""
		elif tok == "ilabas" or tok == "ILABAS":
			tokens.append("print")
			tok = ""
		elif tok == "PUNASAN" or tok == "punasan":
			tokens.append("ENDIF")
			tok = ""
		elif tok == "pag" or tok == "PAG":
			tokens.append("IF")
			tok = ""
		elif tok == "ituloy" or tok == "ITULOY":
			if expr != "" and isexpr == 0:
				tokens.append("NUM:" + expr)
				expr = ""
			tokens.append("THEN")
			tok = ""
		elif tok == "IPASOK" or tok == "ipasok":
			tokens.append("INPUT")
			tok = ""			
		elif tok == "0" or tok == "1" or tok == "2" or tok == "3" or tok == "4" or tok == "5" or tok == "6" or tok == "7" or tok == "8" or tok == "9":
			expr += tok
			tok = ""
		elif tok == "+" or tok == "-" or tok == "*" or tok == "/" or tok == "(" or tok == ")":
			isexpr = 1
			expr += tok
			tok = ""
		elif tok == "\t":
			tok = ""
		elif tok == "\"" or tok == " \"":
			if state == 0:
				state = 1
			elif state == 1:
				tokens.append("STRING:" + STRING + "\"")
				STRING = ""
				state = 0
				tok = ""
		elif state == 1:
			STRING += tok
			tok = ""
	#print(tokens)
	#return ''
	return tokens
	
def evalExpression(expr):

	return eval(expr)	
						
def doPrint(toPrint):
	if(toPrint[0:6] == "STRING"):
		toPrint = toPrint[8:]
		toPrint = toPrint[:-1]
	elif(toPrint[0:3] == "NUM"):
		toPrint = toPrint[4:]
	elif(toPrint[0:4] == "EXPR"):
		toPrint = evalExpression(toPrint[5:])		
	print(toPrint)

def doASSIGN(varname, varvalue):
	symbols[varname[4:]] = varvalue	
	
def getVARIABLE(varname):
	varname = varname[4:]
	if varname in symbols:
		return symbols[varname]
	else:
		return "TARANTADO: hindi ko kilala yang variable na yan"
		exit()
		
def getINPUT(STRING, varname):
	i = input(STRING[1:-1] + " ")
	symbols[varname] = "STRING:\"" + i + "\""
		
def parse(toks):
	i = 0
	while(i < len(toks)):
		if toks[i] == "ENDIF":
			#print("found and endif")
			i+=1
		elif toks[i] + " " + toks[i+1][0:6] == "print STRING" or toks[i] + " " + toks[i+1][0:3] == "print NUM" or toks[i] + " " + toks[i+1][0:4] == "print EXPR" or toks[i] + " " + toks[i+1][0:3] == "print VAR":
			if toks[i+1][0:6] == "STRING":
				doPrint(toks[i+1])
			elif toks[i+1][0:3] == "NUM":
				doPrint(toks[i+1])
			elif toks[i+1][0:4] == "EXPR":
				doPrint(toks[i+1])
			elif toks[i+1][0:3] == "VAR":
				doPrint(getVARIABLE(toks[i+1]))		
			i+=2
		elif toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:6] == "VAR EQUALS STRING" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS NUM" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:4] == "VAR EQUALS EXPR" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS VAR":
			if toks[i+2][0:6] == "STRING":
				doASSIGN(toks[i],toks[i+2])
			elif toks[i+2][0:3] == "NUM":
				doASSIGN(toks[i],toks[i+2])
			elif toks[i+2][0:4] == "EXPR":
				doASSIGN(toks[i],"NUM:" + str(evalExpression(toks[i+2][5:])))
			elif toks[i+2][0:3] == "VAR":
				doASSIGN(toks[i],getVARIABLE(toks[i+2]))
			i+=3
		elif toks[i] + " " + toks[i+1][0:6] + " " + toks[i+2][0:3] == "INPUT STRING VAR":
			getINPUT(toks[i+1][7:],toks[i+2][4:])
			i+=3
		elif toks[i] + " " + toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3] + " " + toks[i+4] == "IF NUM EQEQ NUM THEN":
			if toks[i+1][4:] != toks[i+3][4:]:
				print("false")
				i+=5
			i+=5
		elif toks[i] + " " + toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3] + " " + toks[i+4] == "IF VAR EQEQ NUM THEN":
			
			#print(toks[i+1][0:3])
			#print(getVARIABLE(toks[i+1])[0:6])
			#print(toks[i+3][0:3])
			if getVARIABLE(toks[i+1]) != toks[i+3]:
				#print("false")
				#print(getVARIABLE(toks[i+1])[8:-1])
				#print(int(toks[i+3][4:]))
				if getVARIABLE(toks[i+1])[8:-1] != toks[i+3][4:]:
					print("false")
					i+=5
			i+=5
		elif toks[i] + " " + toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:6] + " " + toks[i+4] == "IF VAR EQEQ STRING THEN":
			
			#print(toks[i+1][0:3])
			#print(getVARIABLE(toks[i+1]))
			
			if getVARIABLE(toks[i+1]) != toks[i+3]:
				print("false")
				i+=5
			i+=5
	#print(symbols)		
	
def run():
	data = open_file(argv[1])
	toks = lex(data)
	parse(toks)
run()