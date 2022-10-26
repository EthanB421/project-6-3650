
import dictionaries
from sys import argv

def openhack(filename):

	with open(filename, 'r') as hackfile:
		commands = hackfile.readlines()
        
	return commands


def commandCheck(command):
	if '=' in command or ';' in command:
		return 'cInstruct'

	elif command.startswith('@'):
		return 'aInstruct'

	else:
		return 'lInstruct'

#Iterate and parse commands
def commandIterate(commandList):
    binaryValue = []

    for command in commandList:
        if commandCheck(command) == 'aInstruct':
            binaryValue.append(parseA(command))

        elif commandCheck(command) == 'cInstruct':
            binaryValue.append(parseC(command))

        elif commandCheck(command) == 'lInstruct':
            pass

    return binaryValue

#Reformats data
def removeComment(line):
	op = '//'
	index = line.find(op)

	if (index == -1):
		return line

	elif (index == 0):
		return ''

	else:
		line = line[:(index - 1)]

	return line


def removeWhiteSpace(commandList):
	commandList = list(map(removeComment, commandList))
	#List comprehension removes blank spaces and lines from commandList
	commandList = [ i.strip(' ') and i.strip('\n') for i in commandList]

	return commandList
	


#Parse A commands
def parseA(command):
	number = int(command[1:])
	return '0' + "{0:015b}".format(int(command[1:]))

#Parse C commands
def parseC(command):
	if ('='  and ';') in command:
		jump = command[command.find(';')+1:]
		dest = command[0:command.find('=')]
		comp = command[command.find('=')+1:command.find(';')]

	elif '=' in command and ';' not in command:
		jump = 'NULL'
		dest = command[0:command.find('=')]
		comp = command[command.find('=')+1:]

	elif ';' in command and '=' not in command:
		jump = command[command.find(';')+1:]
		dest = 'NULL'
		comp = command[0:command.find(';')]

	return cBinary(jump, dest, comp)


def cBinary(jump, dest, comp):
	#Pulls from the dictionaries file according to jump, dest, and comp parameters
	jumpVal = dictionaries.jump[jump]
	destVal = dictionaries.dest[dest]
	compVal = dictionaries.comp[comp]

	return '111' + jumpVal + destVal + compVal 

# write new hack file
def writehackfile(binlist, filename):
	newfilename = filename[:filename.find('.')+1] + 'hack'
	with open(newfilename, 'w') as f:
		for item in binlist:
  			f.write("%s\n" % item)




script, filename = argv
commandList = openhack(filename)
writehackfile(commandIterate(removeWhiteSpace(commandList)), filename)