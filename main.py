import ass,lin,loader

x = []#contains the name of the files to be loaded , linker and loaded######location#########
oplen = {}
symTable = {}
globTable = {}
filelen = {}


def runass():#assembling
	ass.test(x)

def runlin():#linking
	lin.linker(x)
def runload():#loading
	loader.loader(x)

x=[]
runass()
oplen =ass
.oplen ;
symTable =ass.symTable ;
globTable =ass.globTable ;
filelen =ass.filelen ;
#print("\n\noplen")
#print(oplen)
#print("\n\nsymTable")
#print(symTable)
#print("\n\nglobTable")
#print(globTable)
#print("\n\nfilelen")
#print(filelen)

runlin()
runload()
