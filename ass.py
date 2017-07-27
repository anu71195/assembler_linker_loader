import re

oplen = {}
symTable = {}
globTable = {}
filelen = {}





def calculatelen():	#from file lenopcodes.cf stores all the assembly language commands in it and the length of those comands
	inputFile = open('lenopcodes.cf',"r")
	code = inputFile.read()
	lines = code.split('\n')
	for line in lines :
		line = line.lstrip().rstrip()
		if line != '' :
			oplen[line.split(' ')[0]] = int(line.split(' ')[1])

def isvariable(line):
	var = re.compile(r'var (.+*)=(.+*)')



def tryInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


#this means compiling a regular expression r is for raw string
#* here means any string including empty
#+ means any string except empty string
#hash tells the preceeding one is the address
def test( fileNames ):			
	calculatelen()
	#print(oplen)
	glo = re.compile(r'glob var (.*)=(.*)') #declaring global variable
	ext = re.compile(r'extern(.*)')#external variable
	var = re.compile(r'var (.*)=(.*)')#declaring variable
	add = re.compile(r'(.+)=(.+)\+(.+)')#addition
	sub = re.compile(r'(.+)=(.+)\-(.+)')#subtraction
	ana = re.compile(r'(.+)=(.+)\&(.+)')#and operation
	ora = re.compile(r'(.+)=(.+)\|(.+)')#or operation
	slop = re.compile(r'loop(.+)')#start loop
	elop = re.compile(r'endloop(.*)')#end loop
	ifgt = re.compile(r'if (.*)>(.*)')#greater than "if" condition
	ifgte = re.compile(r'endif(.*)')#end of if condition
	ifeq = re.compile(r'if (.*)=(.*)')#equal to "if" condition
	for fileName in fileNames :
#		print(fileName)
#		print(fileNames)
		inputFile = open(fileName, "r")
		fileName = fileName.split('.')[0]
		outFile = open(fileName+'.l','w')
		code = inputFile.read()
		lines = code.split('\n')
		newCode = []
		memaddr = 0
		loopctr = 0
		ifctr = 0
		ifjmp = {}
		symTable[fileName] = {}
		globTable[fileName] = {}
		for line in lines :
			line = line.lstrip().rstrip()
			if var.match(line):
				symTable[fileName][var.match(line).group(1).lstrip().rstrip()] = '#'+str(memaddr + 3)
				newCode.append('JMP #'+str(memaddr+4))#unconditional jump(jump has memory requirement of 3bytes)#########################
				newCode.append('DB '+var.match(line).group(2).lstrip().rstrip())#define bytes(1 byte)
				memaddr = memaddr + 4
			elif glo.match(line):
				symTable[fileName][glo.match(line).group(1).lstrip().rstrip()] = '#'+str(memaddr + 3)
				globTable[fileName][glo.match(line).group(1).lstrip().rstrip()] = '#'+str(memaddr + 3)
				newCode.append('JMP #'+str(memaddr+4))############
				newCode.append('DB '+glo.match(line).group(2).lstrip().rstrip())
				memaddr = memaddr + 4
			elif ext.match(line):
				symTable[fileName][ext.match(line).group(1).lstrip().rstrip()] = '$'+str(ext.match(line).group(1).lstrip().rstrip())
			elif add.match(line):#x=y+z
				x = add.match(line).group(1).lstrip().rstrip()
				y = add.match(line).group(2).lstrip().rstrip()
				z = add.match(line).group(3).lstrip().rstrip()
				if tryInt(y) and tryInt(z):
					newCode.append('MVI A,'+y)#move immediate value in the register A(A is for accumulator)
					newCode.append('ADI '+z)#add immediate value to the accumulator
					newCode.append('STA '+str(symTable[fileName][x]))#copies the data byte from the accumulator in the memory location specified by the immediate address
					memaddr += oplen['MVI']
					memaddr += oplen['ADI']
					memaddr += oplen['STA']
				elif tryInt(y) and not tryInt(z):#if z is a variable
					newCode.append('LDA '+str(symTable[fileName][z]))# contents of immediate address is loaded in the accumulator
					newCode.append('ADI '+y)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['ADI']
					memaddr += oplen['STA']
				elif tryInt(z) and not tryInt(y):#if y is a variable
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('ADI '+z)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['ADI']
					memaddr += oplen['STA']
				elif not tryInt(y) and not tryInt(z):#if y and z both are variable
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('MOV B,A')#moving contents of register A into register B
					newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('ADD B')#adding contents of B into the contents of A
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['MOV']
					memaddr += oplen['LDA']
					memaddr += oplen['ADD']
					memaddr += oplen['STA']
			elif sub.match(line):#x=y-z
				x = sub.match(line).group(1).lstrip().rstrip()
				y = sub.match(line).group(2).lstrip().rstrip()
				z = sub.match(line).group(3).lstrip().rstrip()
				if tryInt(y) and tryInt(z):
					newCode.append('MVI A,'+y)
					newCode.append('SUI '+z)#subtract immediate from the accumulator
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['MVI']
					memaddr += oplen['SUI']
					memaddr += oplen['STA']
				elif tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('MOV B,A')
					newCode.append('MVI A,'+y)
					newCode.append('SUB B')
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['MOV']
					memaddr += oplen['MVI']
					memaddr += oplen['SUB']
					memaddr += oplen['STA']
				elif tryInt(z) and not tryInt(y):
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('SUI '+z)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['SUI']
					memaddr += oplen['STA']
				elif not tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('MOV B,A')
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('SUB B')
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['MOV']
					memaddr += oplen['LDA']
					memaddr += oplen['SUB']
					memaddr += oplen['STA']
			elif ana.match(line):#x=y&z
				x = ana.match(line).group(1).lstrip().rstrip()
				y = ana.match(line).group(2).lstrip().rstrip()
				z = ana.match(line).group(3).lstrip().rstrip()
				if tryInt(y) and tryInt(z):
					newCode.append('MVI A,'+y)
					newCode.append('ANI '+z)#and the immediate value with the contents in the Accumulator
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['MVI']
					memaddr += oplen['ANI']
					memaddr += oplen['STA']
				elif tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('ANI '+y)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['ANI']
					memaddr += oplen['STA']
				elif tryInt(z) and not tryInt(y):
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('ANI '+z)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['ANI']
					memaddr += oplen['STA']
				elif not tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('MOV B,A')
					newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('ANA B')#and the contents of register B with register A
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['MOV']
					memaddr += oplen['LDA']
					memaddr += oplen['ANA']
					memaddr += oplen['STA']
			elif ora.match(line):#x=y|z
				x = ora.match(line).group(1).lstrip().rstrip()
				y = ora.match(line).group(2).lstrip().rstrip()
				z = ora.match(line).group(3).lstrip().rstrip()
				if tryInt(y) and tryInt(z):
					newCode.append('MVI A,'+y)
					newCode.append('ORI '+z)#or the immediate value with the contents of the accumulator
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['MVI']
					memaddr += oplen['ORI']
					memaddr += oplen['STA']
				elif tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('ORI '+y)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['ORI']
					memaddr += oplen['STA']
				elif tryInt(z) and not tryInt(y):
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('ORI '+z)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['ORI']
					memaddr += oplen['STA']
				elif not tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('MOV B,A')
					newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('ORA B')#or the contents of register B with the contents in Accumulator
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['MOV']
					memaddr += oplen['LDA']
					memaddr += oplen['ORA']
					memaddr += oplen['STA']
			elif slop.match(line):#loop x
				x = slop.match(line).group(1).lstrip().rstrip()
				if tryInt(x):
					newCode.append('PUSH D')#push D into the stack
					newCode.append('MVI E,'+x)#counter is stored in register #
					memaddr += oplen['PUSH']
					memaddr += oplen['MVI']
					symTable[fileName][loopctr] = '#' + str(memaddr)
					loopctr += 1#number of nested loops+1
				# else:
				# 	newCode.append('PUSH E')
				# 	newCode.append('MVI E,'+str(symTable[fileName][x]))
				# 	memaddr += oplen['PUSH']
				# 	memaddr += oplen['MVI']
				# 	symTable[fileName][loopctr] = memaddr
				# 	loopctr += 1
			elif elop.match(line):#endloop 
				newCode.append('MOV A,E')
				newCode.append('SUI 1')#decreament of counter
				newCode.append('MOV E,A')#counter updated into the register
				newCode.append('JNZ '+str(symTable[fileName][loopctr-1]))#conditional jump (if accumulator non equal to zero then jump to the immediate address)
				newCode.append('POP D')#pop one element from staack to tell the end of one loop syntactically successfully
				loopctr -= 1#number of nested loops+1
				memaddr += oplen['MOV']
				memaddr += oplen['SUI']
				memaddr += oplen['MOV']
				memaddr += oplen['JNZ']
				memaddr += oplen['POP']
			elif ifgt.match(line):#x>y
				x = ifgt.match(line).group(1).lstrip().rstrip()
				y = ifgt.match(line).group(2).lstrip().rstrip()
				newCode.append('LDA '+str(symTable[fileName][x]))
				newCode.append('MOV B,A')
				newCode.append('LDA '+str(symTable[fileName][y]))
				newCode.append('SUB B')
				newCode.append('JNS &&&'+str(ifctr))#if conditional statement fails i.e. y>x (NS is for no sign)(&&& and further string will be replaced later)
				newCode.append('JZ &&&'+str(ifctr))#if conditional statement fails i.e. y=x(&&& and further string will be replaced later)
				ifctr += 1# number of if conditions+1
				memaddr += oplen['LDA']
				memaddr += oplen['MOV']
				memaddr += oplen['LDA']
				memaddr += oplen['SUB']
				memaddr += oplen['JNS']
				memaddr += oplen['JZ']
			elif ifeq.match(line):#x=y
				x = ifeq.match(line).group(1).lstrip().rstrip()
				y = ifeq.match(line).group(2).lstrip().rstrip()
				newCode.append('LDA '+str(symTable[fileName][x]))
				newCode.append('MOV B,A')
				newCode.append('LDA '+str(symTable[fileName][y]))
				newCode.append('SUB B')
				newCode.append('JNZ &&&'+str(ifctr))#if conditional statement fails(&&& and further string will be replaced later)
				ifctr += 1# number of if conditions+1
				memaddr += oplen['LDA']
				memaddr += oplen['MOV']
				memaddr += oplen['LDA']
				memaddr += oplen['SUB']
				memaddr += oplen['JNZ']
			elif ifgte.match(line):#endif
				ifjmp[ifctr-1] = memaddr#storing the address where the endif condition is for the ifctr^th if condition
			
		outFile.write('\n'.join(newCode))#file with all the instruction is created with some replacements lefts
		outFile.close()
		filelen[fileName] = memaddr
		################################
		inputFile = open(fileName+'.l','r')
		code = inputFile.read()
		lines = code.split('\n')
		newCode = []
		for line in lines :
			if '&&&' in line:#replacing the &&& and preceeding instruction with the correct address
				tag = line.split(' ')[1]
				linenum = tag.split('&&&')[1].lstrip().rstrip()
				linenum = int(linenum)
				newtag = '#'+str(ifjmp[linenum])
				newCode.append(line.replace(tag, newtag))
			else:
				newCode.append(line)
		outFile = open(fileName+'.li','w')
		outFile.write('\n'.join(newCode))
		outFile.close()
		
