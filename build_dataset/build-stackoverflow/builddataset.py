import MySQLdb
import sqlite3
import csv
import os
import datetime
import time
import re
import string
import operator
import threading
from HTMLParser import HTMLParser
from badgesDict import badges



def getUsersAnswersAcceptedQuery(user, date):
	return "SELECT ownerID AS UserID, count(postID) AS UsersAnswersAccepted FROM acceptedanswer_mv WHERE ownerID = " + user + " AND ts_voteDate < date(\'" + date + "\')"

def getUsersQuestionsAcceptedQuery(user, date):
	return "SELECT ownerID AS UserID, count(postID) AS UsersQuestionsAccepted FROM questwithacceptedanswer_mv WHERE ownerID = " + user + " AND ts_voteDate < date(\'" + date + "\')"

# Estrae il numero di upvotes, prima di una certa data (@Date), ottenuti dalle domande postate da un certo utente (@User) */
def getQuestUpVotes(user, date):
	return "SELECT u_ownerID as UserID, count(u_voteID) as UpVotesQuest FROM questionupvotes_mv WHERE u_ownerID = " + user + " AND uts_voteDate < date(\'" + date + "\')"

# Estrae il numero di downvotes, prima di una certa data (@Date), ottenuti dalle domande postate da un certo utente (@User) */
def getQuestDownVotes(user, date):
	return "SELECT d_ownerID as UserID, count(d_voteID) as DownVotesQuest FROM questiondownvotes_mv WHERE d_ownerID = " + user + " AND dts_voteDate < date(\'" + date + "\')"
	
# Estrae il numero di upvotes, prima di una certa data (@Date), ottenuti dalle risposte postate da un certo utente (@User) */
def getAnswUpVotes(user, date):
	return "SELECT u_ownerID as UserID, count(u_voteID) as UpVotesAnsw FROM answerupvotes_mv WHERE u_ownerID = " + user + " AND uts_voteDate < date(\'" + date + "\')"
	
# Estrae il numero di downvotes, prima di una certa data (@Date), ottenuti dalle risposte postate da un certo utente (@User) */
def getAnswDownVotes(user, date):
	return "SELECT d_ownerID as UserID, count(d_voteID) as AnswerDownvotesScore FROM answerdownvotes_mv WHERE d_ownerID = " + user + " AND dts_voteDate < date(\'" + date + "\')"
	
# commenti di un utente di una domanda (@PostId) prima della data di accettazione (@Date)
def getUsersCommentsBeforeAccDate(postid, vote_date):
	return "SELECT c_Id, c_text FROM userscommentsquestions_mv WHERE c_ts_creationDate < \'" + vote_date + "\' AND q_Id = " + postid

# commenti di un utente di una domanda (@PostId)
def getUsersComments(postid):
	return "SELECT c_Id, c_text FROM userscommentsquestions_mv WHERE q_Id = " + postid

# Estrae l'insieme dei badge sbloccati da un utente (@User) prima di una certa data (@Date) */
def getBadges(user, date):
	return "SELECT Badges.UserId, Badges.Name FROM Badges WHERE Badges.UserId = " + user + " AND Badges.Date < \'" + date + "\'" 


# Classe utilizzata dalla funzione del_tags per parserizzare
# il codice html 
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

# Elimina i tag html del testo passato come parametro
#
# parametri:
#	text: testo da analizzare
#
# output:
#	testo del parametro text senza tag html
def del_tags(text):
    s = MLStripper()
    s.feed(text)
    return s.get_data()

# Elimina, dal testo passato come parametro, i pezzi racchiusi
# tra i tag <code> </code> (code snippet)
#
# parametri:
#	text: testo da analizzare
#
# output:
#	testo del parametro text senza code snippet
def del_code(text):
	return re.sub('<code>[\s\S.]+?</code>', ' ', text)

# Elimina, dal testo passato come parametro, i tag html
# ed il code snippet
#
# parametri:
#	text: testo da analizzare
#
# output:
#	testo del parametro text senza tag html e senza code snippet
def clean_body(text):
	return del_tags(del_code(text))

# Calcola il numero di parole contenute nel testo passato come parametro
#
# parametri:
#	text: testo da analizzare
#
# output:
#	numero di parole trovate nel parametro text
def text_length(text):
	text_splitted = re.findall(r"[\w']+", text)
	word = len(text_splitted)
	
	return word

# Calcola il numero di link contenuti nel testo passato come parametro
#
# parametri:
#	text: testo da analizzare
#
# output:
#	numero di link trovati nel parametro text
def link_count(text):
	links = re.findall("<a href", text)
	n_links = len(links)

	return n_links

# Costruisce un dizionario, ordinato per frequenza descrescente,
# delle parole contenute nei testi del file passato in input.
# La frequenza viene calcolata come il numero di volte che la parola
# compare nelle istanze diviso il numero di parole totali.
# Prima di calcolare le frequenze, i testi vengono ripuliti dai tag html
# e dal code snippet.
#
# parametri:
#	file_name: file in formato csv con i campi 'Title' e 'Body' (da i quali prende il testo)
#	output: file csv con la colonna delle parole e la colonna delle frequenze
def create_dictionary(file_name, output):
	print "Processing..."
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';')

	dictionary = {}
	n_word = 0
	skipped = 0
	for row in dict_reader:
		body = row['Body']
		title = row['Title']
		
		try:
			body_cleaned = clean_body(body)
			title_cleaned = clean_body(title)

			corpus = body_cleaned + " " + title_cleaned

			words = re.findall(r"[\w']+", corpus)
		
			for word in words:
				word = word.lower()
				if word == "":
					n_word = n_word
				elif word == "\n":
					n_word = n_word
				elif word == "\t":
					n_word = n_word
				else:
					n_word += 1
					if dictionary.has_key(word):
						dictionary[word] += 1
					else:
						dictionary[word] = 1
		except Exception:
			skipped += 1
			continue
		

	print "Number of skipped posts  ", skipped	
	print "Number of words ", n_word

	for key in dictionary.keys():
		dictionary[key] = float(dictionary[key])/float(n_word)

	sorted_dict = sorted(dictionary, key=dictionary.get, reverse=True)

	w = csv.writer(open(output, "w"), delimiter=';')
	for elem in sorted_dict:
		w.writerow([elem,dictionary[elem]])

	print "Done..."

	return sorted_dict

# Esegue la query sul database (mysql), passati in input, e ritorna il result set
#
# parametri:
#	database: stringa con il nome del database che si vuole interrogare (es.: 'stackoverflow')
#	query: stringa con la query (in sql) da eseguire sul database
#
# output:
#	result set 
def execute_param_query(database, query):
	conn = MySQLdb.connect(host="localhost",user="root",
                  passwd="root",db=database)
	c = conn.cursor()
	c.execute(query)
	c.fetchall()
	return c

# Calcola, dato il campo che contiene la data e l'ora, il
# giorno della settimana e l'ora
#
# parametri:
#	file_name: nome del file csv da cui leggere la data; tale
#				file deve contenere almeno i campi 'PostId' e 'PostCreationDate';
#				il formato della data, del campo 'PostCreationDate', è
#				del tipo '2014-01-30 21:30'
#	output_file: nome del file csv su cui scrivere i risultati; conterrà
#					i campi:
#					- 'PostId'
#					- 'Weekday' con valori: 'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'
#					- 'GMTHour' che contiene solo l'ora e quindi può assumere
#							valori: 00,01,02,03,...,23
def weekday(file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';') # DELIMITER
	
	head = dict_reader.fieldnames
	f = ['PostId', 'Weekday', 'GMTHour']
	#head.append('Weekday')
	#head.append('GMTHour')
	DayL = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=f)  # DELIMITER
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header
	count = 0
	for row in dict_reader:
		r = {}
		r['PostId'] = row['PostId']
		date = row['PostCreationDate']
		d = date.split(' ')
		dat = d[0].split('-')
		hou = d[1].split(':')
		hour = hou[0]
		
		r['GMTHour'] = hour

		print "Anno: ", dat[0]
		print "Mese: ", dat[1]
		print "Giorno: ", dat[2]
			
		weekday = DayL[datetime.date(int(dat[0]),int(dat[1]),int(dat[2])).weekday()] + ""
		r['Weekday'] = weekday
		dict_writer.writerow(r)
		count += 1
	
	print 'Post processed: ', count
	return 'Done'

# Calcola i 
#
# parametri:
#	file_name: nome del file csv da leggere; deve contenere almeno i campi:
#				- 'PostId'
#				- 'PostAcceptedAnswerId' id della risposta accettata se c'è, None 
#					altrimenti
#				- 'AnswerCount' numero delle risposte alla domanda
#	output_file: nome del file su cui scrivere i riusltati, conterrà i campi:
#				- 'PostId'
#				- 'Accepted' con valori 'yes' se il campo PostAcceptedAnswerId contiene
#					un id, 'no'	se contiene 'None'
#				- 'HasAnswer' con valori 'yes' se il campo 'AnswerCount' ha una valore
#					maggiore di zero, 'no' altrimenti
#				- 'NoAnswer' con valori 'yes' se il campo 'AnswerCount' ha un valore 
#					uguale a zero, 'no' altrimenti
def accepted(file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';')  # DELIMITER
	
	head = dict_reader.fieldnames
	f = ['PostId', 'Accepted', 'HasAnswer', 'NoAnswer']
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=f)  # DELIMITER
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header
	count = 0
	for row in dict_reader:
		r = {}
		r['PostId'] = row['PostId']
		accepted = 'yes'
		hasanswer = 'no'
		noanswer = 'no'
		if row['PostAcceptedAnswerId'] == 'None':
			accepted = 'no'
		if int(row['AnswerCount']) > 0:
			hasanswer = 'yes'
		if int(row['AnswerCount']) == 0:
			noanswer = 'yes'

		r['Accepted'] = accepted
		r['HasAnswer'] = hasanswer
		r['NoAnswer'] = noanswer
		
		dict_writer.writerow(r)
		count += 1

	print 'Post processed: ', count
	return 'Done'

# Calcola la lunghezza del corpo e del titolo, se il corpo contiene del codice e
# ripulisce il corpo dai tag e dal code snippet
#
# parametri:
#	file_name: nome del file csv da cui leggere, deve contenere almeno i campi:
#				- 'PostId'
#				- 'Title' campo testuale con il titolo del post
#				- 'Body' campo testuale con il corpo del post
#	output_file: nome del file csv su cui scrivere i risultati e contiene, oltre
#		a tutti i campi del file preso in input, i campi:
#				- 'PostId'
#				- 'Body' il corpo del post ripulito dai tag html e dal code snippet
#				- 'TitleLength' numero di parole del campo 'Title'
#				- 'BodyLength' numero di parole del campo 'Body'
#				- 'CodeSnippet' con valori 'yes' se 'Body' contiene del code snippet, 'no'
#					altrimenti
def clean_len_code_body_title(file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'))
	
	head = dict_reader.fieldnames
	head.append('BodyLength')
	head.append('TitleLength')
	head.append('CodeSnippet')
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), head)
	dict_writer.writerow(dict((fn,fn) for fn in head)) #Scrive gli header
	count = 0
	for row in dict_reader:
		
		body = row['Body']
		title = row['Title']
		try:
			

			body_cleaned = clean_body(body.decode('unicode_escape').encode('ascii','ignore'))
			
			row['Body'] = body_cleaned

			row['TitleLength'] = text_length(title)
			row['BodyLength'] = text_length(body_cleaned)

			code_snippet = "no"
			if '<code>' in body:
				code_snippet = "yes"

			row['CodeSnippet'] = code_snippet
			count += 1
		except Exception:
			continue
		dict_writer.writerow(row)
	print 'Post processed: ', count
	return 'Done'

# Calcola gli up vote delle domande dell'utente prima della data di creazione del post
#
# parametri:
#	db: stringa con il nome del database da cui leggere
#	file_name: nome del file csv da cui leggere, deve contenere almeno i campi:
#			- 'PostId'
#			- 'UserId' id dell'utente che ha postato la domanda
#			- 'PostCreationDate' data di creazione del post in formato '2014-01-30 21:30'
#	output_file: nome del file csv su cui scrivere i risultati, contiene i campi:
#			- 'PostId'
#			- 'QuestionUpVotes' numero degli up vote delle domande dell'utente prima della
#				data in 'PostCreationDate'
def scorequp(db, file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';')
	
	head = dict_reader.fieldnames
	f = ['PostId', 'QuestionUpVotes']
		
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=f)
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header
	count = 0
	for row in dict_reader:
		r = {}
		r['PostId'] = row['PostId']
		user = row['UserId']
		date = row['PostCreationDate']
		
		result_set4 = execute_param_query(db, getQuestUpVotes(user, date))
		
		for tup in result_set4:
			q_up = tup[1]
		
		r['QuestionUpVotes'] = q_up

		dict_writer.writerow(r)
		count += 1
	
	print 'Post processed: ', count
	return 'Done'

# Calcola i down vote delle domande dell'utente prima della data di creazione del post
#
# parametri:
#	db: stringa con il nome del database da cui leggere
#	file_name: nome del file csv da cui leggere, deve contenere almeno i campi:
#			- 'PostId'
#			- 'UserId' id dell'utente che ha postato la domanda
#			- 'PostCreationDate' data di creazione del post in formato '2014-01-30 21:30'
#	output_file: nome del file csv su cui scrivere i risultati, contiene i campi:
#			- 'PostId'
#			- 'QuestionDownVotes' numero dei down vote delle domande dell'utente prima della
#				data in 'PostCreationDate'
def scoreqdown(db, file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';')
	
	head = dict_reader.fieldnames
	f = ['PostId', 'QuestionDownVotes']
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=f)
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header
	
	for row in dict_reader:
		r = {}
		r['PostId'] = row['PostId']
		user = row['UserId']
		date = row['PostCreationDate']
		
		result_set5 = execute_param_query(db, getQuestDownVotes(user, date))
		
		for tup in result_set5:
			q_down = tup[1]
		
		r['QuestionDownVotes'] = q_down

		dict_writer.writerow(r)
	
	return 'Done'

# Calcola lo score delle domande come il numero degli up vote meno il numero di down 
# vote prima della data di creazione del post
#
# parametri:
#	db:  stringa con il nome del database da cui leggere
#	file_name: nome del file csv da cui leggere, deve contenere almeno i campi:
#			- 'PostId'
#			- 'UserId' id dell'utente che ha postato la domanda
#			- 'PostCreationDate' data di creazione del post in formato '2014-01-30 21:30'
#	output_file: nome del file csv su cui scrivere i risultati, contiene i campi:
#			- 'PostId'
#			- 'QuestionScore' numero degli up vote meno il numero dei down vote delle 
#				domande dell'utente prima della data in 'PostCreationDate'
def scorequestion(db, file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'))
	
	head = dict_reader.fieldnames
	f = ['PostId', 'QuestionScore']
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), f)
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header
	count = 0
	for row in dict_reader:
		r = {}
		r['PostId'] = row['PostId']
		user = row['UserId']
		date = row['PostCreationDate']
		
		result_set4 = execute_param_query(db, getQuestUpVotes(user, date))
		result_set5 = execute_param_query(db, getQuestDownVotes(user, date))
		
		for tup in result_set4:
			q_up = tup[1]
		for tup in result_set5:
			q_down = tup[1]

		q_score = q_up - q_down
		
		r['QuestionScore'] = q_score

		dict_writer.writerow(r)
		count += 1
	
	print 'Post processed: ', count
	return 'Done'

# Calcola gli up vote delle risposte dell'utente prima della data di creazione del post
#
# parametri:
#	db: stringa con il nome del database da cui leggere
#	file_name: nome del file csv da cui leggere, deve contenere almeno i campi:
#			- 'PostId'
#			- 'UserId' id dell'utente che ha postato la domanda
#			- 'PostCreationDate' data di creazione del post in formato '2014-01-30 21:30'
#	output_file: nome del file csv su cui scrivere i risultati, contiene i campi:
#			- 'PostId'
#			- 'AnswerUpVotes' numero degli up vote delle risposte dell'utente prima della
#				data in 'PostCreationDate'
def scoreaup(db, file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';')
	
	head = dict_reader.fieldnames
	f = ['PostId', 'AnswerUpVotes']
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=f)
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header
	
	for row in dict_reader:
		r = {}
		r['PostId'] = row['PostId']
		user = row['UserId']
		date = row['PostCreationDate']
		
		result_set6 = execute_param_query(db, getAnswUpVotes(user, date))
		
		for tup in result_set6:
			a_up = tup[1]
		
		r['AnswerUpVotes'] = a_up

		dict_writer.writerow(r)
	
	return 'Done'

# Calcola i down vote delle risposte dell'utente prima della data di creazione del post
#
# parametri:
#	db: stringa con il nome del database da cui leggere
#	file_name: nome del file csv da cui leggere, deve contenere almeno i campi:
#			- 'PostId'
#			- 'UserId' id dell'utente che ha postato la domanda
#			- 'PostCreationDate' data di creazione del post in formato '2014-01-30 21:30'
#	output_file: nome del file csv su cui scrivere i risultati, contiene i campi:
#			- 'PostId'
#			- 'AnswerDownVotes' numero dei down vote delle risposte dell'utente prima della
#				data in 'PostCreationDate'
def scoreadown(db, file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';')
	
	head = dict_reader.fieldnames
	f = ['PostId', 'AnswerDownVotes']
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=f)
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header
	
	for row in dict_reader:
		r = {}
		r['PostId'] = row['PostId']
		user = row['UserId']
		date = row['PostCreationDate']
		
		result_set7 = execute_param_query(db, getAnswDownVotes(user, date))
		
		for tup in result_set7:
			a_down = tup[1]
		
		r['AnswerDownVotes'] = a_down


		dict_writer.writerow(r)
	
	return 'Done'

# Calcola lo score delle risposte come il numero degli up vote meno il numero di down 
# vote prima della data di creazione del post
#
# parametri:
#	db: stringa con il nome del database da cui leggere
#	file_name: nome del file csv da cui leggere, deve contenere almeno i campi:
#			- 'PostId'
#			- 'UserId' id dell'utente che ha postato la domanda
#			- 'PostCreationDate' data di creazione del post in formato '2014-01-30 21:30'
#	output_file: nome del file csv su cui scrivere i risultati, contiene i campi:
#			- 'PostId'
#			- 'AnswerScore' numero degli up vote meno il numero dei down vote delle 
#				risposte dell'utente prima della data in 'PostCreationDate'
def scoreanswer(db, file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'))
	
	head = dict_reader.fieldnames
	f = ['PostId', 'AnswerScore']
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), f)
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header
	count = 0
	for row in dict_reader:
		r = {}
		r['PostId'] = row['PostId']
		user = row['UserId']
		date = row['PostCreationDate']
		print user
		print date
		print "start queries"
		result_set6 = execute_param_query(db, getAnswUpVotes(user, date))
		result_set7 = execute_param_query(db, getAnswDownVotes(user, date))
		print "end queries"
		
		for tup in result_set6:
			a_up = tup[1]
		for tup in result_set7:
			a_down = tup[1]
		
		a_score = a_up - a_down
		
		r['AnswerScore'] = a_score

		dict_writer.writerow(r)
		count += 1
	
	print 'Post processed: ', count
	return 'Done'

# Calcola lo score delle domande e delle risposte
#
# parametri:
#	file_name: nome del file csv da cui leggere, deve contenere almeno i campi:
#		- 'PostId'
#		- 'QuestionUpVotes' numero degli up vote delle domande postate dall'utente 
#			prima della data di creazione della domanda
#		- 'QuestionDownVotes' numero dei down vote delle domande postate dall'utente 
#			prima della data di creazione della domanda
#		- 'AnswerUpVotes' numero degli up vote delle risposte postate dall'utente 
#			prima della data di creazione della domanda
#		- 'AnswerDownVotes'	numero dei down vote delle risposte postate dall'utente 
#			prima della data di creazione della domanda
#	output_file: nome del file csv su cui scrivere i risultati e contiene, oltre a tutti
#		i campi del csv preso in input, i campi:
#		- 'PostId'
#		- 'QuestionScore' risultato della sottrazione tra il campo 'QuestionUpVotes' e il
#			campo 'QuestionDownVotes'
#		- 'AnswerScore' risultato della sottrazione tra il campo 'AnswerUpVotes' e il
#			campo 'AnswerDownVotes'
def score(file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'))
	
	head = dict_reader.fieldnames
	head.append('QuestionScore')
	head.append('AnswerScore')
	
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), head)
	dict_writer.writerow(dict((fn,fn) for fn in head)) #Scrive gli header
	
	for row in dict_reader:
		q_up = int(row['QuestionUpVotes'])
		q_down = int(row['QuestionDownVotes'])
		a_up = int(row['AnswerUpVotes'])
		a_down = int(row['AnswerDownVotes'])

		q_score = q_up - q_down
		a_score = a_up - a_down
			
		row['QuestionScore'] = q_score
		row['AnswerScore'] = a_score

		dict_writer.writerow(row)
	
	return 'Done'

# Calcola lo score delle domande
#
# parametri:
#	file_name: nome del file csv da cui leggere, deve contenere almeno i campi:
#		- 'PostId'
#		- 'QuestionUpVotes' numero degli up vote delle domande postate dall'utente 
#			prima della data di creazione della domanda
#		- 'QuestionDownVotes' numero dei down vote delle domande postate dall'utente 
#			prima della data di creazione della domanda
#	output_file: nome del file csv su cui scrivere i risultati e contiene i campi:
#		- 'PostId'
#		- 'QuestionScore' risultato della sottrazione tra il campo 'QuestionUpVotes' e il
#			campo 'QuestionDownVotes'
def calculate_quest_score(file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';')
	
	head = dict_reader.fieldnames
	f = ['PostId', 'QuestionScore']
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=f)
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header
	
	for row in dict_reader:
		r = {}
		r['PostId'] = row['PostId']
		q_up = row['QuestionUpVotes']
		q_down = row['QuestionDownVotes']
		
		q_score = int(q_up) - int(q_down)
			
		r['QuestionScore'] = q_score

		dict_writer.writerow(r)
	
	return 'Done'

# Calcola lo score delle risposte
#
# parametri:
#	file_name: nome del file csv da cui leggere, deve contenere almeno i campi:
#		- 'PostId'
#		- 'AnswerUpVotes' numero degli up vote delle risposte postate dall'utente 
#			prima della data di creazione della domanda
#		- 'AnswerDownVotes'	numero dei down vote delle risposte postate dall'utente 
#			prima della data di creazione della domanda
#	output_file: nome del file csv su cui scrivere i risultati e contiene i campi:
#		- 'PostId'
#		- 'AnswerScore' risultato della sottrazione tra il campo 'AnswerUpVotes' e il
#			campo 'AnswerDownVotes'
def calculate_answ_score(file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';')
	
	head = dict_reader.fieldnames
	f = ['PostId', 'AnswerScore']
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=f)
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header
	
	for row in dict_reader:
		r = {}
		r['PostId'] = row['PostId']
		a_up = row['AnswerUpVotes']
		a_down = row['AnswerDownVotes']

		a_score = int(a_up) - int(a_down)
			
		r['AnswerScore'] = a_score

		dict_writer.writerow(r)
	
	return 'Done'

# Calcola il numero di badge di tipo gold, silver e bronze ottenuti dall'utente prima 
# della data di creazione della domanda
# 
# parametri:
#	db: stringa con il nome del database da cui leggere
#	file_name: nome del file csv da cui leggere, deve contenere almeno i campi:
#			- 'PostId'
#			- 'UserId' id dell'utente che ha postato la domanda
#			- 'PostCreationDate' data di creazione del post in formato '2014-01-30 21:30'
#	output_file: nome del file csv su cui scrivere i risultati, contiene i campi:
#			- 'PostId'
#			- 'BronzeBadge' numero di badge bronzo
#			- 'SilverBadge' numero di badge argento
#			- 'GoldBadge' numero di badge oro
def badge(db, file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';')
	
	head = dict_reader.fieldnames
	f = ['PostId', 'BronzeBadge', 'SilverBadge', 'GoldBadge']
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=f)
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header
	count = 0
	for row in dict_reader:
		r = {}
		r['PostId'] = row['PostId']
		user = row['UserId']
		date = row['PostCreationDate']
		print "start query"
		result_set = execute_param_query(db, getBadges(user, date))
		print "end query"
		
		bronze = 0
		silver = 0
		gold = 0
		tag_badges = {}

		for tup in result_set:
			if badges.has_key(tup[1]): # The badge is predefined
				if badges[tup[1]] == 'Bronze':
					bronze += 1
				if badges[tup[1]] == 'Silver':
					silver += 1
				if badges[tup[1]] == 'Gold':
					gold += 1
			else: # The badge is not predefined, is a tag badge, then count the number of occurencies
				if tag_badges.has_key(tup[1]):
					tag_badges[tup[1]] += 1
				else:
					tag_badges[tup[1]] = 1

					
		for tag in tag_badges:
			if tag_badges[tag] == 1:
				bronze += 1
			if tag_badges[tag] == 2:
				bronze += 1
				silver += 1
			if tag_badges[tag] == 3:
				bronze += 1
				silver += 1
				gold += 1

		r['BronzeBadge'] = bronze
		r['SilverBadge'] = silver
		r['GoldBadge'] = gold
			

		dict_writer.writerow(r)
		count += 1
	
	print 'Post processed: ', count
	return 'Done'

# Calcola il numero di badge ottenuti dall'utente prima della data di creazione della domanda
# 
# parametri:
#	db: stringa con il nome del database da cui leggere
#	file_name: nome del file csv da cui leggere, deve contenere almeno i campi:
#			- 'PostId'
#			- 'UserId' id dell'utente che ha postato la domanda
#			- 'PostCreationDate' data di creazione del post in formato '2014-01-30 21:30'
#	output_file: nome del file csv su cui scrivere i risultati, contiene i campi:
#			- 'PostId'
#			- 'NumberOfBadges' numero di badge
def badge_nodist(db, file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';')
	
	head = dict_reader.fieldnames
	f = ['PostId', 'NumberOfBadges']	
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=f)
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header
	count = 0
	for row in dict_reader:
		r = {}
		r['PostId'] = row['PostId']
		user = row['UserId']
		date = row['PostCreationDate']
		
		result_set = execute_param_query(db, getBadges(user, date))
		
		n_badges = 0

		for tup in result_set:
			n_badges += 1			
					
		r['NumberOfBadges'] = n_badges	

		dict_writer.writerow(r)
		count += 1
	
	print 'Post processed: ', count
	return 'Done'

# Calcola il numero di risposte date dall'utente che sono state accettate prima della data 
# di creazione della domanda 
# 
# parametri:
#	db: stringa con il nome del database da cui leggere
#	file_name: nome del file csv da cui leggere, deve contenere almeno i campi:
#			- 'PostId'
#			- 'UserId' id dell'utente che ha postato la domanda
#			- 'PostCreationDate' data di creazione del post in formato '2014-01-30 21:30'
#	output_file: nome del file csv su cui scrivere i risultati, contiene i campi:
#			- 'PostId'
#			- 'UsersAnswersAccepted' numero di risposte date dall'utente 'UserId' prima
#				della data in 'PostCreationDate' 
def users_answ_acc(db, file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';')
	
	head = dict_reader.fieldnames
	
	f = ['PostId', 'UsersAnswersAccepted']
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=f)
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header
	count = 0
	for row in dict_reader:
		r = {}
		r['PostId'] = row['PostId']
		user = row['UserId']
		date = row['PostCreationDate']
		
		result_set = execute_param_query(db, getUsersAnswersAcceptedQuery(user, date))
		
		for tup in result_set:
			r['UsersAnswersAccepted'] = tup[1]		

		dict_writer.writerow(r)
		count += 1
	
	print 'Post processed: ', count
	return 'Done'

# Calcola il numero di domande fatte dall'utente che hanno ricevuto una risposta accettata 
# prima della data di creazione della domanda 
# 
# parametri:
#	db: stringa con il nome del database da cui leggere
#	file_name: nome del file csv da cui leggere, deve contenere almeno i campi:
#			- 'PostId'
#			- 'UserId' id dell'utente che ha postato la domanda
#			- 'PostCreationDate' data di creazione del post in formato '2014-01-30 21:30'
#	output_file: nome del file csv su cui scrivere i risultati, contiene i campi:
#			- 'PostId'
#			- 'UsersQuestionsAccepted' numero di risposte date dall'utente 'UserId' prima
#				della data in 'PostCreationDate' 	
def users_quest_acc(db, file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';')
	
	head = dict_reader.fieldnames
	f = ['PostId', 'UsersQuestionsAccepted']
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=f)
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header
	count = 0
	for row in dict_reader:
		r = {}
		r['PostId'] = row['PostId']
		user = row['UserId']
		date = row['PostCreationDate']
		result_set = execute_param_query(db, getUsersQuestionsAcceptedQuery(user, date))
		
		for tup in result_set:
			r['UsersQuestionsAccepted'] = tup[1]

		dict_writer.writerow(r)
		count += 1
	
	print 'Post processed: ', count
	return 'Done'

# Lista i badge di tipo tag presenti nel database
#
# parametri:
#	db: stringa con il nome del database da cui leggere
#	outfile: nome del file txt su cui scrivere la lista dei badge di tipo tag in ordine
#		alfabetico
def tag_badges(db, outfile):
	new_badges = open(outfile, 'w')

	p_badges = []

	result_set = execute_param_query(db, "SELECT DISTINCT Name FROM Badges")
		
	for tup in result_set:
		if badges.has_key(tup[0]):
			print ""
		else:
			if tup[0] in p_badges:
				print ""
			else:
				p_badges.append(tup[0])
				
	p_badges.sort()
	for elem in p_badges:
		new_badges.write(elem+"\n")
	new_badges.close()
	print p_badges
	return 'Done'

# Salva il result set (risultato di una query) in un file in formato csv
#
# parametri:
#	result_set: oggetto ritornato dalla funzione execute_param_query
#	filename: nome del file in formato csv su cui scrivere il result_set,
#		il file conterrà gli stessi campi del result set
#
# NON GESTISCE I CARATTERI UNICODE. NON UTILIZZARE
def save_csv(result_set, filename):
	f = open(filename, 'w')
	
	writer = csv.writer(f)
	
	desc = result_set.description # Prende i campi della tabella
	fields = []
	for d in desc:
		fields = fields + [d[0]]

	writer.writerow(fields)

	for row in result_set: # Prende i record della tabella
		row_to_write = []
		for c in row:
			if c != '':
				row_to_write = row_to_write + [str(c)]
		writer.writerow(row_to_write)

	return 'Done'

# Salva il result set (risultato di una query) in un file in formato csv
#
# parametri:
#	result_set: oggetto ritornato dalla funzione execute_param_query, tale
#		result set deve contenere almeno il campo 'Body'
#	filename: nome del file in formato csv su cui scrivere il result_set,
#		il file conterrà: 
#			- gli stessi campi del result set con il campo 'Body' ripulito 
#				dai tag html e dal code snippet
#			- il campo 'CodeSnippet' che avrà valore 'yes' se il campo 'Body'
#				contiene il tag <code>, 'no' altrimenti
def save_csv_code_snip(result_set, filename):
	f = open(filename, 'w')
	
	writer = csv.writer(f, delimiter=';') # DELIMITER
	print result_set

	desc = result_set.description # Prende i campi della tabella

	i = 0
	body_field = 0
	fields = []
	for d in desc:
		if 'Body' in d[0]:
			body_field = i
		fields = fields + [d[0]]
		i += 1
	fields.append('CodeSnippet')

	writer.writerow(fields)
	total = 0
	count = 0
	for row in result_set: # Prende i record della tabella
		total += 1
		row_to_write = []
		i = 0
		#try:
		code_snippet = "no"
		for c in row:				
			if i == body_field:
				try:
					body_cleaned = clean_body(c.decode('unicode_escape').encode('ascii','ignore'))
				except UnicodeDecodeError:
					print count
					try:
						body_cleaned = clean_body(unicode(c).encode('ascii', 'ignore'))
					except Exception:	
						body_cleaned = clean_body(unicode(c, errors='ignore'))
					
				if '<code>' in str(c):
					code_snippet = "yes"
					
				try:
					row_to_write = row_to_write + [body_cleaned.decode('unicode_escape').encode('ascii','ignore')]
				except UnicodeDecodeError:
					print count
					try:
						row_to_write = row_to_write + [unicode(body_cleaned).encode('ascii', 'ignore')]
					except Exception:	
						row_to_write = row_to_write + [unicode(body_cleaned, errors='ignore')]
					
				count += 1
			else:
				row_to_write = row_to_write + [str(c)]
			i += 1
		row_to_write = row_to_write + [code_snippet]
		writer.writerow(row_to_write)
		
		#except Exception, e:
		#	i += 1
		#	print body_cleaned
		#	print e

	print "Total post",total
	print "Post processed ",count
	return 'Done'

# Calcola la lunghezza del titolo e del corpo, in termini di numero di parole,
# dei post passati come input
#
# parametri:
#	file_name: nome del file csv da cui leggere titolo e corpo, deve contenere
#		almeno i campi:
#			- 'PostId'
#			- 'Title' campo contenente il titolo 
#			- 'Body' campo contenente il corpo
#	output_file: nome del file csv su cui scrivere i risultati, conterrà i campi:
#			- 'PostId'
#			- 'TitleLength' numero di parole del campo 'Title'
#			- 'BodyLength' numero di parole del campo 'Body'
def len_body_title(file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';') # DELIMITER
	
	head = dict_reader.fieldnames
	f = ['PostId', 'BodyLength', 'TitleLength']
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=f) # DELIMITER
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header
	count = 0
	for row in dict_reader:
		r = {}
		r['PostId'] = row['PostId']
		body = row['Body']
		title = row['Title']
		try:
			r['TitleLength'] = text_length(title)
			r['BodyLength'] = text_length(body)

			count += 1
		except Exception:
			continue
		dict_writer.writerow(r)
	print 'Post processed: ', count
	return 'Done'

# Divide, per istanze, un file csv in n file csv con stessa dimensione.
# Sel il file in input ha m righe e lo si vuole dividere in n file,
# allora si avranno i primi n-1 file con k istanze
#		k = int(m/n)	#con int() si indica la prate intera della divisione
# e l'ultimo file con le restanti istanze.
#
# Esempio: se il file che si vuole dividere contiene 4221 istanze e lo si 
# vuole dividere in 4 file, allora verrano creati 3 tre file (con nomi: 
# 1.csv, 2.csv, 3.csv) con 1055 istanze ed un file (con nome 4.csv) con
# le restanti 1056 istanze.
#
# parametri:
#	file_name: nome del file csv da splittare
#	out_dir: nome della directory nella quale scrivere gli n file splittati
#	n: numero di file da creare nella directory out_dir
def split(file_name, out_dir, n):
	os.mkdir(out_dir)	

	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';')
	n_rows = len(list(csv.reader(open(file_name), delimiter=';'))) - 1
	
	head = dict_reader.fieldnames
	
	n_rows_splitted = int(float(n_rows)/float(n))

	print n_rows_splitted

	count_segm = 0
	count_row = 0
	
	for row in dict_reader:
		if count_row == 0:
			count_segm += 1
			f = open(out_dir+str(count_segm)+'.csv', 'w')
			dict_writer = csv.DictWriter(f, delimiter=';', fieldnames=head)
			dict_writer.writerow(dict((fn,fn) for fn in head)) #Scrive gli header
			print "Segment ",count_segm
		
		dict_writer.writerow(row)
		count_row += 1
		
		if count_row == n_rows_splitted:
			if count_segm < n:
				count_row = 0
	
	return 'Done'

# Esegue una funzione, come thread, che prende in input il nome
# del database, il nome del file csv da cui leggere ed il nome 
# del file csv su cui scrivere. run_threads avvierà tanti thread
# quanti sono i file csv contenuti nella directory da cui leggere.
# In particolare, run_threads, è usata per avviare la stessa funzione 
# da eseguire sui file csv splittati dalla funzione split().
#
# parametri:
#	input_dir: nome della directory che contiene i file di output
#		della funzione split()
#	out_dir: nome della directory nella quale scrivere i file di output
#	func: nome della funzione che si vuole eseguire, sono ammesse solo 
#		le funzioni che prendono in input il nome di un database (parametro db),
#		il nome del file csv da cui leggere ed il nome del file csv su cui 
#		scrivere
#	db: nome del database
def run_threads(input_dir, out_dir, func, db):
	input_files = os.listdir(input_dir)	#restituisce i file in input_dir in ordine alfabetico
	input_files.sort() #si assicura che siano in ordine alfabetico
	os.mkdir(out_dir)
	for s in input_files:
		o = s.replace('.csv', '_out.csv') 
		
		print o
		t = threading.Thread(target=func, args=(db, input_dir+s, out_dir+o)) 
		#thread_list.append(t)
		t.start()
		
	return 'Done'

# Concatena, per istanze, i file csv che trova nella directory, passata in
# input, in un unico file csv.
#
# parametri:
#	input_dir: nome della directory dalla quale leggere i file csv da concatenare
#	out_file: nome del file csv su cui scrivere 
def m(input_dir, out_file):
	files = os.listdir(input_dir)
	files.sort()
	
	first = True
	
	for f in files:
		seg = csv.DictReader(open(input_dir+f, 'r'), delimiter=';')
		if first == True:
			head = seg.fieldnames
			out = csv.DictWriter(open(out_file, 'w'), delimiter=';', fieldnames=head)
			out.writerow(dict((fn,fn) for fn in head)) #Scrive gli header	
			first = False
		
		
		print f
		for row in seg:
			#print row
			out.writerow(row)

# Crea il file csv da dare in input alle funzioni che calcolano lo score di
# sentiment e le frequenze delle classi LIWC.
#
# parametri:
#	input_file: nome del file csv da cui leggere, deve contenere almeno i campi:
#			- 'PostId'
#			- 'Title' titolo del post
#			- 'Body' corpo del post
#	output_file: nome del file csv su cui scrivere, conterrà i campi:
#			- 'PostId'
#			- 'Corpus' che ha la concatenazione del campo 'Title' con il campo 'Body'
def dataset_liwc_senti(input_file, output_file):
	dict_reader = csv.DictReader(open(input_file, 'r'), delimiter=',') # DELIMITER
	
	head = dict_reader.fieldnames
	f = ['PostId', 'Corpus']
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=f) # DELIMITER
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header
	
	count = 0
	for row in dict_reader:
		r = {}
		r['PostId'] = row['PostId']
		body = row['Body']
		title = row['Title']
		try:
			corpus = title + " " + body
			
			try:
				r['Corpus'] = corpus.decode('unicode_escape').encode('ascii','ignore')
			except UnicodeDecodeError:
				print r['PostId']
				try:
					r['Corpus'] = unicode(corpus).encode('ascii', 'ignore')
				except Exception:
					r['Corpus'] = unicode(corpus, errors='ignore')

			
		except Exception:
			dict_writer.writerow(r)
			continue
		dict_writer.writerow(r)
	print 'Post processed: ', count
	return 'Done'

# Converte il campo che contiene il giorno della settimana in un campo a due 
# valori che indica se il giorno fa parte del weekend o meno, in particolare
# 'Monday'		-> 'Weekday',
# 'Tuesday'		-> 'Weekday',
# 'Wednesday'	-> 'Weekday',
# 'Thursday'	-> 'Weekday',
# 'Friday'		-> 'Weekday',
# 'Saturday'	-> 'Weekend',
# 'Sunday'		-> 'Weekend'
#
# Converte il campo che contiene solo l'ora in un campo che indica la fascia 
# oraria come mattina, pomeriggio, sera e notte. In particolare
# '06','07','08','09','10','11'	-> 'Morning',
# '12','13','14','15','16','17'	-> 'Afternoon',
# '18','19','20','21','22'		-> 'Evening',
# '23','00','01','02','03','04','05' -> 'Night'
#
# Converte i campi che contengono gli score di sentiment dalle scale 
# [1,...,5] di score positivo e [-1,...,-5] di score negativo in una
# unica scala [0,...4]
#
# parametri:
#	input_file: nome del file da cui leggere, deve contenere almeno i campi:
#			- 'Weekday' che può contenere valori {'Monday','Tuesday','Wednesday',
#				'Thursday','Friday','Saturday','Sunday'}
#			- 'GMTHour' che può contenere valori {'00','01','02','03','04','05',
#				'06','07','08','09','10','11','12','13','14','15','16','17','18',
#				'19','20','21','22','23'}
#			- 'SentimentNegativeScore' con valori da -1 a -5
#			- 'SentimentPositiveScore' con valori da 1 a 5
#	output_file: nome del file csv su cui scrivere, conterrà tutti i campi del file
#		input_file, con i campi 'Weekday', 'GMTHour', 'SentimentNegativeScore' e
#		'SentimentPositiveScore' convertiti
def conv_senti_weekday_time(input_file, output_file):
	dict_reader = csv.DictReader(open(input_file, 'r'), delimiter=';') # DELIMITER
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=dict_reader.fieldnames) # DELIMITER
	dict_writer.writerow(dict((fn,fn) for fn in dict_reader.fieldnames)) #Scrive gli header
	
	wd = {'Monday':'Weekday',
		'Tuesday':'Weekday',
		'Wednesday':'Weekday',
		'Thursday':'Weekday',
		'Friday':'Weekday',
		'Saturday':'Weekend',
		'Sunday':'Weekend'}

	time = {'06':'Morning','07':'Morning','08':'Morning','09':'Morning','10':'Morning','11':'Morning',
			'12':'Afternoon','13':'Afternoon','14':'Afternoon','15':'Afternoon','16':'Afternoon','17':'Afternoon',
			'18':'Evening','19':'Evening','20':'Evening','21':'Evening','22':'Evening',
			'23':'Night','00':'Night','01':'Night','02':'Night','03':'Night','04':'Night','05':'Night'}

	#count = 0
	for row in dict_reader:
		
		row['SentimentNegativeScore'] = str((int(row['SentimentNegativeScore']) * -1) - 1)
		row['SentimentPositiveScore'] = str(int(row['SentimentPositiveScore']) - 1)

		row['Weekday'] = wd[row['Weekday']]
		
		row['GMTHour'] = time[row['GMTHour']]
		
		dict_writer.writerow(row)

# Definiamo, per ogni domanda, i commenti che l'utente, autore della domanda, ha 
# aggiunto prima della data di accettazione della risposta. Nel caso non ci fosse
# una risposta accettata vengono considerati tutti i commenti che l'autore ha 
# aggiunto alla sua domanda.
# La funzione calcola il numero ed il testo di tali commenti.
#
# parametri:
#	database: nome del database da interrogare
#	output_file: nome del file csv su cui scrivere i risultati, conterrà i campi:
#			- 'PostId'
#			- 'NumberOfUsersComments' numero di commenti
#			- 'TextOfUsersComments' testo dei commenti trovati
def userscommentsonquestions_dataset(database, output_file):
	
	# Inizializza il csv da scrivere
	fieldnames = ['PostId' , 'NumberOfUsersComments', 'TextOfUsersComments']
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=fieldnames) # DELIMITER
	dict_writer.writerow(dict((fn,fn) for fn in fieldnames)) #Scrive gli header

	# Query per ottenere tutte le domande con la relativa data di accettazione della risposta nel caso ci sia
	query_questions_voteDate = "select * from (select postId, ownerId, ts_voteDate from  questwithacceptedanswer_mv union select q_postID as postId, q_ownerID as ownerId, null from questions_mv) questions group by postId"
	questions = execute_param_query(database, query_questions_voteDate)
	
	
	for row in questions:
		# row[0] = postId
		# row[1] = ownerId
		# row[2] = ts_voteDate

		comments = []
		w_row = {}
		w_row['PostId'] = row[0]
		if str(row[2]) != 'None':
			comments = execute_param_query(database, getUsersCommentsBeforeAccDate(str(row[0]), str(row[2])))
		else:
			comments = execute_param_query(database, getUsersComments(str(row[0])))

		
		w_row['NumberOfUsersComments'] = str(comments.rowcount)
		w_row['TextOfUsersComments'] = str()
		for comm in comments:
			# comm[0] = c_Id
			# comm[1] = c_text
			w_row['TextOfUsersComments'] += ' ' + comm[1]
			#w_row['TextOfUsersComments'] += ' ' + unicode(comm[1], errors='ignore')
		
		dict_writer.writerow(w_row)

# Converte le scale di sentiment score 
# da [1,...5] a [0,...4] per lo score positivo
# da [-1,...,-5] a [0,...,-4] per lo score negativo
#
# parametri:
#	input_file: nome del file csv da cui leggere, deve contenere almeno i campi:
#			- 'SentimentPositiveScore' score di sentiment positivo del post
#			- 'SentimentNegativeScore' score di sentiment negativo del post
#			- 'CommentSentimentPositiveScore' score di sentiment positivo dei commenti
#			- 'CommentSentimentNegativeScore' score di sentiment negativo dei commenti
def shift_sentiscore(input_file, output_file):
	dict_reader = csv.DictReader(open(input_file, 'r'), delimiter=';') # DELIMITER
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=dict_reader.fieldnames) # DELIMITER
	dict_writer.writerow(dict((fn,fn) for fn in dict_reader.fieldnames)) #Scrive gli header

	for row in dict_reader:
		if row['SentimentPositiveScore'] != '0':
			row['SentimentPositiveScore'] = str(int(row['SentimentPositiveScore']) - 1)

		if row['CommentSentimentPositiveScore'] != '0':
			row['CommentSentimentPositiveScore'] = str(int(row['CommentSentimentPositiveScore']) - 1)
		
		if row['SentimentNegativeScore'] != '0':
			row['SentimentNegativeScore'] = str(int(row['SentimentNegativeScore']) + 1)

		if row['CommentSentimentNegativeScore'] != '0':
			row['CommentSentimentNegativeScore'] = str(int(row['CommentSentimentNegativeScore']) + 1)
		
		dict_writer.writerow(row)
		
# Dummy coding delle colonne che rappresentano variabili categoriche.
# In particolare una colonna che rappresenta una variabile categorica con n possibili valori,
# viene convertita in n colonne che rappresentano variabili binarie con valori 0,1.
# 
# parametri:
#	input_file: nome del file csv da cui leggere
#	output_file: nome del file csv su cui scrivere, conterrà tutti i campi del file input_file
#		ed in più, per ogni colonna che si vuole convertire le colonne codificate
#	cols_to_convert: vettore con i nomi delle colonne da codificare
def categoric_to_binary(input_file, output_file, cols_to_convert=['Weekday', 'GMTHour', 'Topic']):
	dict_reader = csv.DictReader(open(input_file, 'r'), delimiter=';') # DELIMITER
	
	f = []
	for header in dict_reader.fieldnames:
		if header not in rm_columns:
			f.append(header)

	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=f) # DELIMITER
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header

	for row in dict_reader:
		row_cleaned = {}
		for field in row.keys():
			if field not in rm_columns:
				row_cleaned[field] = row[field]
		#break
		dict_writer.writerow(row_cleaned)

# Salva il result set calcolando la lunghezza del titolo e del corpo
#
# parametri:
#	result_set: oggetto ritornato dalla funzione execute_param_query, tale
#		result set deve contenere almeno il campo 'Body'
#	filename: nome del file in formato csv su cui scrivere il result_set,
#		il file conterrà: 
#			- gli stessi campi del result set con il campo 'Body' ripulito 
#				dai tag html e dal code snippet
#			- il campo 'TitleLength' con il numero di parole del campo Title
#			- il campo 'BodyLength' con il numero di parole del campo Body
def save_csv_body_title_len(result_set, filename):
	f = open(filename, 'w')
	writer = csv.writer(f)
	#print result_set

	desc = result_set.description # Prende i campi della tabella

	i = 0
	body_field = 0
	fields = [] # crea il vettore che contiene gli header da scrivere nel csv di output
	for d in desc:
		if 'Body' in d[0]:
			body_field = i # conserva l'indice del campo Body
		if 'Title' in d[0]:
			title_field = i # conserva l'indice del campo Title
		fields = fields + [d[0]]
		i += 1
	fields.append('TitleLength')
	fields.append('BodyLength')

	writer.writerow(fields) # scrive gli header sul csv
	total = 0
	count = 0
	for row in result_set: # Cicla sui record della tabella
		total += 1
		row_to_write = []
		i = 0
		
		blen = 0
		tlen = 0
		for c in row:				
			if i == body_field:
				body = ''
				try:
					body = c.decode('unicode_escape').encode('ascii','ignore')
				except UnicodeDecodeError:
					try:
						body = unicode(c).encode('ascii', 'ignore')
					except Exception:
						body = unicode(c, errors='ignore')

				body_cleaned = clean_body(body) 
				blen = text_length(body_cleaned)

				row_to_write = row_to_write + [body_cleaned]
				count += 1

			elif i == title_field:
				tlen = text_length(c)
				row_to_write = row_to_write + [c]
			else:
				row_to_write = row_to_write + [str(c)]
			i += 1
		row_to_write = row_to_write + [str(tlen)]
		row_to_write = row_to_write + [str(blen)]
		writer.writerow(row_to_write)
	

	print "Total post",total
	print "Post processed ",count
	return 'Done'


questions_query = "SELECT q_postID AS PostId, q_title AS Title, q_body AS Body, q_tags AS Tags, q_postDate AS PostCreationDate, q_ownerID AS UserId, q_acceptedAnswerId AS PostAcceptedAnswerId, q_answerCount AS AnswerCount FROM questions_mv"

questions_query_id_body_title_tags = "SELECT q_postID AS PostId, q_title AS Title, q_body AS Body, q_tags AS Tags FROM questions_mv"
