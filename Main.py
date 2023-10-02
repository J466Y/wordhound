import lexEngine.lexengine as LE
import os
import time
import subprocess
import client as cli
import translate
import expander
subprocess.call('clear')
print ('''
                              `                                     
            `'+++++.       '+'+     `'+`+++.   :+    +,++++++'`           
           ''++++++++       .++:    ;++  .+:   ++`  `+  ,+' `++           
          ++++++++++'.      .++'    +'+   ++  `++:  :+  :+:  ;+,          
         '+'+++++++++,      :+++   ;+++   ++  +:++  +;  ;+,  '+.          
        `++'++.   ;+'`      :+,+   +`++   ++  + '+  +   '+. ,++           
        ;++++      ;;  `    ;'`+'`,+ ++   '+ ,' '+`,+   ''+++;            
        ++++    ``     ,`   '; +' +, +'   ;+.+. .+,';   ++ ++.            
        +'+    +++'   ,:`   +: ++`+  +'   ,+:+   +'+`   ++ .++            
        ++    #++'   ,::`   +, .++: `+;   `++'   +++    ++  #+`           
        #   ` `.`   .:::`   +. `'+` .+:    ++    '+'    ++  .'+           
        ,  `:      ,::::    +`  +'  :+,    #+    :+,   `++   +#           
           :::`   ,::::,                                                  
           ::::::::::::`         
           :::::::::::.            
           .:::::::::.               
            `::::::,`              
                `         
Presents : 
                ''')

print ('''
$$\      $$\                           $$\ $$\   $$\                                     $$\ 
$$ | $\  $$ |                          $$ |$$ |  $$ |                                    $$ |
$$ |$$$\ $$ | $$$$$$\   $$$$$$\   $$$$$$$ |$$ |  $$ | $$$$$$\  $$\   $$\ $$$$$$$\   $$$$$$$ |
$$ $$ $$\$$ |$$  __$$\ $$  __$$\ $$  __$$ |$$$$$$$$ |$$  __$$\ $$ |  $$ |$$  __$$\ $$  __$$ |
$$$$  _$$$$ |$$ /  $$ |$$ |  \__|$$ /  $$ |$$  __$$ |$$ /  $$ |$$ |  $$ |$$ |  $$ |$$ /  $$ |
$$$  / \$$$ |$$ |  $$ |$$ |      $$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |
$$  /   \$$ |\$$$$$$  |$$ |      \$$$$$$$ |$$ |  $$ |\$$$$$$  |\$$$$$$  |$$ |  $$ |\$$$$$$$ |
\__/     \__| \______/ \__|       \_______|\__|  \__| \______/  \______/ \__|  \__| \_______|

''')
time.sleep(2)
def main():
	
	while True:
		subprocess.call("clear") 
		choice = int(input('''
=== WELCOME TO WORDHOUND ===

[+] Please select option:
	
	1. Generate Dictionary
	2. Expand or Translate Existing dictionary

	99. Exit
\n> '''))
		if choice == 1:
			generation()
		elif choice == 2:
			manipulate()
		else:
			return

def manipulate():
	os.system("clear")
	choice = int(input('''
[+] Please select option:
	
	1. Translate Dictionary
	2. Expand Dictionary (Tries to derive keywords from related terms)

\n> '''))
	if choice == 1:
		translateDict()
	else:
		expand()

def expand():
	loc = input('[+] Please input the location of dictionary\n> ').replace("\'", "").strip()

	while not(os.path.exists(loc)):
		print ()
		loc = input("[x] {0} doesn't seem to exist, try again.\n> ".format(loc))

	print ("[-] Beginning Expansion...")
	e = expander.expand(loc, loc+"-EXPANDED")
	e.expand()

	
def translateDict():
	print ()
	loc =input('[+] Please input the location of dictionary\n> ').replace("\'", "").replace("\"", "").strip()
	while not(os.path.exists(loc.replace("\'", "".replace("\"", "")))):
		loc = input("[x] That doesn't seem to exist, try again.\n")
	f = open('languages.data', 'r')
	x = f.readlines()
	choices = x[:]
	f.close()
	
	for i in range(len(x)):
		print ("\t{0}. {1}".format(i,x[i].split('\t')[0]))
	choice = int(input("[+] Please select the language to translate to (e.g. 12):\n> "))
	lang = choices[choice].split('\t')[1]
	t = translate.Translator(lang.strip())
	f = open(loc, 'r')
	x = f.read()
	f.close()
	
	translated = t.translate(x)
	f = open(loc+"-{0}".format(lang.upper()).strip(), 'w')
	f.write(translated.encode('utf8'))
	f.close()
	print ("[+] Dictionary translated, saved to {0}...".format(loc+"-{0}".format(lang.upper())))
	raw_input()
	os.system("clear")


def generation():
		string, options = createJob()
		print ('''
=== WELCOME TO WORDHOUND ===

[+] Please select industry:
''')			
		choice = int(input(string + "\n\t99. Exit\n> "))-1
		if choice == 98:
			subprocess.call('clear')
			print ("[-] Thanks for using *WordHound*.\n\t@tehnlulz")
			return
		if choice >= len(options):
			createNewIndustry()
		else:
			industrySelected(options[choice])
		print ("Press enter to continue...")
		raw_input()
	
def industrySelected(industry):
	subprocess.call("clear")
	count = 1
	options = ""
	print('''
=== {0} ==='''.format(industry))
	optionsList = []
	#print(returnDirs("data/industries/"+industry+'/'))
	for dirname in returnDirs("data/industries/"+industry+'/'):
		options += '\t'+str(count) + ". " + dirname + '\n'
		optionsList.append(dirname)
		count+=1
	options += '\n\t'+str(count) + ". Create new client\n"
	options +=  '\t'+str(count+1) + ". Generate industry correlated dictionary\n"
	options +=  '\t'+str(count+2) + ". Generate concatenated industry dictionary\n"
	choice = int(input(options + "\n> "))
	if choice == count:
		createNewClient(industry)
	elif choice == (count+1):
		generateIndustryDictionary(industry)
	elif choice == (count+2):
		generateCollatedDictionary(industry)
	else:
		clientSelected(optionsList[choice-1], industry)

def generateCollatedDictionary(industry):
	currInds = []
	for dirname in returnDirs("data/industries/"+industry+'/'):
		if os.path.exists("data/industries/"+industry+'/'+dirname+'/'+"PdfDictionary.txt"):
			currInds.append("data/industries/"+industry+'/'+dirname+'/'+"PdfDictionary.txt")
		if os.path.exists("data/industries/"+industry+'/'+dirname+'/'+"WebsiteDictionary.txt"):
			currInds.append("data/industries/"+industry+'/'+dirname+'/'+"WebsiteDictionary.txt")
		if os.path.exists("data/industries/"+industry+'/'+dirname+'/'+"TxtDictionary.txt"):
			currInds.append("data/industries/"+industry+'/'+dirname+'/'+"TxtDictionary.txt")
		if os.path.exists("data/industries/"+industry+'/'+dirname+'/'+"TwitterSearchTermDictionary.txt"):
			currInds.append("data/industries/"+industry+'/'+dirname+'/'+"TwitterSearchTermDictionary.txt")
		if os.path.exists("data/industries/"+industry+'/'+dirname+'/'+"TwitterHandleDictionary.txt"):
			currInds.append("data/industries/"+industry+'/'+dirname+'/'+"TwitterHandleDictionary.txt")
	lex = LE.lexengine("", "data/industries/"+industry+'/'+"CollatedDictionary.txt", False)
	print ("[+] Beginning dictionary collation...\n")
	lex.collateDicts(currInds)
def generateIndustryDictionary(industry):
	currInds = []
	for dirname in returnDirs("data/industries/"+industry+'/'):
		if os.path.exists("data/industries/"+industry+'/'+dirname+'/'+"PdfDictionary.txt"):
			currInds.append("data/industries/"+industry+'/'+dirname+'/'+"PdfDictionary.txt")
		if os.path.exists("data/industries/"+industry+'/'+dirname+'/'+"WebsiteDictionary.txt"):
			currInds.append("data/industries/"+industry+'/'+dirname+'/'+"WebsiteDictionary.txt")
		if os.path.exists("data/industries/"+industry+'/'+dirname+'/'+"TxtDictionary.txt"):
			currInds.append("data/industries/"+industry+'/'+dirname+'/'+"TxtDictionary.txt")
		if os.path.exists("data/industries/"+industry+'/'+dirname+'/'+"TwitterSearchTermDictionary.txt"):
			currInds.append("data/industries/"+industry+'/'+dirname+'/'+"TwitterSearchTermDictionary.txt")
		if os.path.exists("data/industries/"+industry+'/'+dirname+'/'+"TwitterHandleDictionary.txt"):
			currInds.append("data/industries/"+industry+'/'+dirname+'/'+"TwitterHandleDictionary.txt")
	lex = LE.lexengine("", "data/industries/"+industry+'/'+"IndustryDictionary.txt", False)
	print ("[+] Beginning dictionary aggregation...\n")
	lex.aggregateDict(currInds)

def generateClientDictionary(clientName):
	currDicts = []
	if os.path.exists(client.workingDirectory + 'PdfDictionary.txt'):
			currDicts.append("data/industries/"+industry+'/'+dirname+'/'+"PdfDictionary.txt")
	if os.path.exists(client.workingDirectory + 'TxtDictionary.txt'):
			currDicts.append("data/industries/"+industry+'/'+dirname+'/'+"TxtDictionary.txt")
	if os.path.exists(client.workingDirectory + 'WebsiteDictionary.txt'):
			currDicts.append("data/industries/"+industry+'/'+dirname+'/'+"WebsiteDictionary.txt")
	if os.path.exists(client.workingDirectory + 'TwitterHandleDictionary.txt'):
			currDicts.append("data/industries/"+industry+'/'+dirname+'/'+"TwitterHandleDictionary.txt")
	if os.path.exists(client.workingDirectory + 'TwitterSearchTermDictionary.txt'):
			currDicts.append("data/industries/"+industry+'/'+dirname+'/'+"TwitterSearchTermDictionary.txt")
def returnDirs(path):
	results = []
	for (dirpath, dirnames, filenames) in os.walk(path):
		results.extend(dirnames)
		return results

def clientSelected(clientName, industry):
	subprocess.call("clear")
	c = cli.client(industry, "", clientName, "", "data/industries/" + industry +'/' + clientName +'/')
	newClientOptions(c)
	pass
def createNewClient(industry):
	subprocess.call("clear")
	print('''
=== CREATE NEW CLIENT ===

''')	
	name = ""
	while len(name) == 0:
		name = input("[+] Please enter client name (can be pseudonym):\n> ")
	c = cli.client(industry, "", name, "", "data/industries/" + industry +'/' + name +'/')
	print ("[-] New client added...")
	time.sleep(1)
	newClientOptions(c)

def newClientOptions(client):
	subprocess.call("clear")
	print('''
=== CLIENT OPTIONS ===

[+] Please choose an option:
''')	

	choice = 0
	while(choice not in ['1', '2', '3', '4', '5','6']):
		choice = input("""1. Generate Dictionary from website.
		2. Generate Dictionary from Text file. 
		3. Generate Dictionary from pdf.
		4. Generate Dictionary from twitter search term.
		5. Generate Dictionary from Reddit
		\n6. Generate aggregate client dictionary.\n> """)

		if choice == '1':
			url = input("[-] Please enter the URL of website to be crawled:\n> ")
			#print "[-] Please enter the domain of client (Put a \'.\' for all links):"
			#domain = raw_input()
			client.url = url
			client.domain = ""
			recursionLevel = input("[-] How many levels of recursion should I crawl? (Default=2):\n> ")
			client.buildDictionary(int(recursionLevel))
			break
		elif choice == '2':
			path = input("[-] Please give the path of the text file to process:\n> ")
			client.buildDictionaryText(path)
			break
		elif choice == '3':
			path = input("[-] Please give the path of the pdf to process:\n> ")
			client.buildDictionaryPdf(path)
			break
		#elif choice == '4':
		#	print "[-] Please enter the user's handle(without the '@'):"
		#	handle = raw_input()
		#	client.buildDictionaryFromTwitterUsername(handle)
		elif choice == '4':
			term = input("[-] Please enter the search term:\n> ")
			client.buildDictionaryFromTwitterSearchTerm(term)
			break
		elif choice == '5':
			subs = input("[-] Please enter any number of subreddits, seperated by a comma\n(e.g. battlefield, netsec, til)\n> ").replace(" ","")
			subs = subs.split(',')
			subprocess.call("clear")
			client.buildDictionaryReddit(subs)
		elif choice == '6':
			print ("[-] Beginning dictionary aggregation")
			client.buildAggregate()
			break
def createNewIndustry():
	subprocess.call("clear")
	print('''
=== CREATE NEW INDUSTRY ===

''')	
	name = ""
	while len(name)==0:
		name = input("[+] Please enter industry name:\n> ")
	if not os.path.exists("data/industries/"+name): os.makedirs("data/industries/"+name)
	print ("[-] New Industry added...")
	time.sleep(1)
	subprocess.call("clear")

def createJob():
	subprocess.call("clear")
	count = 1
	options = ""
	optionsList = []
	for (dirpath, dirnames, filenames) in os.walk("data/industries"):
		optionsList.extend(dirnames)
		break
	for i in optionsList:
		
		options += '\t'+str(count) + ". {0}\n".format(i)
		count +=1
	options += '\n\t'+str(count) + ". Create new industry\n"
	#print optionsList
	return options, optionsList
main()
