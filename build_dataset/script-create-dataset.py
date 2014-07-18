import sqlite3
import csv
import os
import datetime
import re
import string
import operator
from django.utils.encoding import smart_str
from HTMLParser import HTMLParser
from badgesDict import badges

def getUsersAnswersAcceptedQuery(user, date):
	return "SELECT Posts.OwnerUserId AS UserId, count(Posts.Id) AS UsersAnswersAccepted FROM Posts INNER JOIN Votes ON Posts.Id = Votes.PostId WHERE Posts.PostTypeId = 2 AND Posts.OwnerUserId = " + user + " AND date(Votes.CreationDate) < date(\'" + date + "\') AND Votes.VoteTypeId = 1"

def getUsersQuestionsAcceptedQuery(user, date):
	return "SELECT Posts.OwnerUserId AS UserId, count(Posts.Id) AS UsersQuestionsAccepted FROM Posts INNER JOIN Votes ON Posts.AcceptedAnswerId = Votes.PostId WHERE Posts.PostTypeId = 1 AND Posts.AcceptedAnswerId IS NOT NULL  AND Posts.OwnerUserId = " + user + " AND date(Votes.CreationDate) < date(\'" + date + "\') AND Votes.VoteTypeId = 1"

def getUsersQuestionsAcceptedQuery2(user, date):
	return "SELECT Posts.OwnerUserId AS UserId, count(Posts.Id) AS UsersQuestionsAccepted FROM Posts INNER JOIN Votes ON Posts.AcceptedAnswerId = Votes.PostId WHERE Posts.PostTypeId = 1 AND Posts.AcceptedAnswerId IS NOT NULL  AND Posts.OwnerUserId = " + user + " AND Votes.CreationDate < date(\'" + date + "\') AND Votes.VoteTypeId = 1"

# Estrae il numero di upvotes, prima di una certa data (@Date), ottenuti dalle domande postate da un certo utente (@User) */
def getQuestUpVotes(user, date):
	return "SELECT Posts.OwnerUserId AS UserId, count(Posts.Id) AS UpVotesQuest FROM Posts INNER JOIN Votes ON Posts.Id = Votes.PostId WHERE Posts.PostTypeId = 1 AND Votes.VoteTypeId = 2 AND date(Votes.CreationDate) < date(\'" + date + "\') AND Posts.OwnerUserId = " + user

# Estrae il numero di downvotes, prima di una certa data (@Date), ottenuti dalle domande postate da un certo utente (@User) */
def getQuestDownVotes(user, date):
	return "SELECT Posts.OwnerUserId AS UserId, count(Posts.Id) AS DownVotesQuest FROM Posts INNER JOIN Votes ON Posts.Id = Votes.PostId WHERE Posts.PostTypeId = 1 AND Votes.VoteTypeId = 3 AND date(Votes.CreationDate) < date(\'" + date + "\') AND Posts.OwnerUserId = " + user

# Estrae il numero di upvotes, prima di una certa data (@Date), ottenuti dalle risposte postate da un certo utente (@User) */
def getAnswUpVotes(user, date):
	return "SELECT Posts.OwnerUserId AS UserId, count(Posts.Id) AS UpVotesAnsw FROM Posts INNER JOIN Votes ON Posts.Id = Votes.PostId WHERE Posts.PostTypeId = 2 AND Votes.VoteTypeId = 2 AND date(Votes.CreationDate) < date(\'" + date + "\') AND Posts.OwnerUserId = " + user

# Estrae il numero di downvotes, prima di una certa data (@Date), ottenuti dalle risposte postate da un certo utente (@User) */
def getAnswDownVotes(user, date):
	return "SELECT Posts.OwnerUserId AS UserId, count(Posts.Id) AS DownVotesAnsw FROM Posts INNER JOIN Votes ON Posts.Id = Votes.PostId WHERE Posts.PostTypeId = 2 AND Votes.VoteTypeId = 3 AND date(Votes.CreationDate) < date(\'" + date + "\') AND Posts.OwnerUserId = " + user

# Estrae l'insieme dei badge sbloccati da un utente (@User) prima di una certa data (@Date) */
def getBadges(user, date):
	return "SELECT Badges.UserId, Badges.Name FROM Badges WHERE Badges.Date < \'" + date + "\' AND Badges.UserId = " + user

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def del_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def del_code(html):
	return re.sub('\<code>(.*?)\</code>', '', html)

def clean_body(html):
	return del_tags(del_code(html))

def del_punctuation(text):
	return text.translate(string.maketrans ("" , ""), string.punctuation)

def text_length(text):
	text_cleaned_punc = del_punctuation(text)
	text_cleaned = re.findall(r"[\w']+", text_cleaned_punc)
	#text_cleaned = text_cleaned_punc.split(" ")
	word = 0
	for w in text_cleaned:
		if w == "":
			word = word
		elif w == "\n":
			word = word
		elif w == "\t":
			word = word
		else:
			word += 1 
	return word

# Restituisce tutti i titoli e tutti i corpi, presenti nel file in input, fusi in un'unica variabile
def get_corpus(file_name):
	dict_reader = csv.DictReader(open(file_name, 'r'))
	
	corpus = ""

	for row in dict_reader:
		body = row['Body']
		title = row['Title']

		body_cleaned = del_punctuation(clean_body(body))
		title_cleaned = del_punctuation(clean_body(title))
		
		corpus = corpus + title_cleaned + " " + body_cleaned
		
	
	return corpus

def create_dictionary(file_name, output):
	print "Processing..."
	dict_reader = csv.DictReader(open(file_name, 'r'))

	dictionary = {}
	n_word = 0

	for row in dict_reader:
		body = row['Body']
		title = row['Title']
		
		try:
			body_cleaned = del_punctuation(clean_body(smart_str(body)))
			title_cleaned = del_punctuation(clean_body(smart_str(title)))

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
			continue
		

		
	print "Number of words ", n_word

	for key in dictionary.keys():
		dictionary[key] = float(dictionary[key])/float(n_word)

	sorted_dict = sorted(dictionary, key=dictionary.get, reverse=True)

	w = csv.writer(open(output, "w"))
	for elem in sorted_dict:
		w.writerow([elem,dictionary[elem]])

	print "Done..."

	return sorted_dict

def execute_param_query(db, query):
	conn = sqlite3.connect(db)
	c = conn.cursor()
	result_set = c.execute(query)
	return result_set

def weekday(file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'))
	
	head = dict_reader.fieldnames
	head.append('Weekday')
	head.append('GMTHour')
	DayL = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
	dict_writer = csv.DictWriter(open(output_file, 'w'), head)
	dict_writer.writerow(dict((fn,fn) for fn in head)) #Scrive gli header
	
	for row in dict_reader:
		date = row['PostCreationDate']
		d = date.split('T')
		dat = d[0].split('-')
		hou = d[1].split(':')
		hour = hou[0]
		
		row['GMTHour'] = hour

		print "Anno: ", dat[0]
		print "Mese: ", dat[1]
		print "Giorno: ", dat[2]
			
		weekday = DayL[datetime.date(int(dat[0]),int(dat[1]),int(dat[2])).weekday()] + ""
		row['Weekday'] = weekday
		dict_writer.writerow(row)
	
	return 'Done'

def accepted(file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'))
	
	head = dict_reader.fieldnames
	head.append('Accepted')
	
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), head)
	dict_writer.writerow(dict((fn,fn) for fn in head)) #Scrive gli header
	
	for row in dict_reader:
		
		accepted = 'yes'
		if row['PostAcceptedAnswerId'] == 'None':
			accepted = 'no'
		row['Accepted'] = accepted
		
		dict_writer.writerow(row)
	
	return 'Done'

def clean_len_code_body_title(file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'))
	
	head = dict_reader.fieldnames
	head.append('BodyCleaned')
	head.append('BodyLength')
	head.append('TitleLength')
	head.append('CodeSnippet')
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), head)
	dict_writer.writerow(dict((fn,fn) for fn in head)) #Scrive gli header
	
	for row in dict_reader:
		body = row['Body']
		title = row['Title']
		try:
			

			body_cleaned = clean_body(body)
			row['BodyCleaned'] = body_cleaned

			row['TitleLength'] = text_length(title)
			row['BodyLength'] = text_length(body_cleaned)

			code_snippet = "no"
			if '<code>' in body:
				code_snippet = "yes"

			row['CodeSnippet'] = code_snippet
		except Exception:
			continue
		dict_writer.writerow(row)
	
	return 'Done'

def score(db, file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'))
	
	head = dict_reader.fieldnames
	head.append('QuestionScore')
	head.append('AnswerScore')
	
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), head)
	dict_writer.writerow(dict((fn,fn) for fn in head)) #Scrive gli header
	
	for row in dict_reader:
		user = row['UserId']
		date = row['PostCreationDate']
		result_set4 = execute_param_query(db, getQuestUpVotes(user, date))
		result_set5 = execute_param_query(db, getQuestDownVotes(user, date))
		result_set6 = execute_param_query(db, getAnswUpVotes(user, date))
		result_set7 = execute_param_query(db, getAnswDownVotes(user, date))
		
		for tup in result_set4:
			q_up = tup[1]
		for tup in result_set5:
			q_down = tup[1]
		for tup in result_set6:
			a_up = tup[1]
		for tup in result_set7:
			a_down = tup[1]
		
		q_score = q_up - q_down
		a_score = a_up - a_down
			
		row['QuestionScore'] = q_score
		row['AnswerScore'] = a_score


		dict_writer.writerow(row)
	
	return 'Done'

def badge(db, file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'))
	
	head = dict_reader.fieldnames
	head.append('BronzeBadge')
	head.append('SilverBadge')
	head.append('GoldBadge')
	
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), head)
	dict_writer.writerow(dict((fn,fn) for fn in head)) #Scrive gli header
	
	for row in dict_reader:
		user = row['UserId']
		date = row['PostCreationDate']
		result_set = execute_param_query(db, getBadges(user, date))
		
		bronze = 0
		silver = 0
		gold = 0

		for tup in result_set:
			if badges.has_key(tup[1]):
				if badges[tup[1]] == 'Bronze':
					bronze += 1
				if badges[tup[1]] == 'Silver':
					silver += 1
				if badges[tup[1]] == 'Gold':
					gold += 1
			#else:
			#	p_badges.append(tup[1])
					
		row['BronzeBadge'] = bronze
		row['SilverBadge'] = silver
		row['GoldBadge'] = gold
			

		dict_writer.writerow(row)
	
	return 'Done'


def users_answ_acc(db, file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'))
	
	head = dict_reader.fieldnames
	head.append('UsersAnswersAccepted')
	
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), head)
	dict_writer.writerow(dict((fn,fn) for fn in head)) #Scrive gli header
	
	for row in dict_reader:
		user = row['UserId']
		date = row['PostCreationDate']
		result_set = execute_param_query(db, getUsersAnswersAcceptedQuery(user, date))
		
		for tup in result_set:
			row['UsersAnswersAccepted'] = tup[1]		

		dict_writer.writerow(row)
	
	return 'Done'
	
def users_quest_acc(db, file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'))
	
	head = dict_reader.fieldnames
	head.append('UsersQuestionsAccepted')
	
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), head)
	dict_writer.writerow(dict((fn,fn) for fn in head)) #Scrive gli header
	
	for row in dict_reader:
		user = row['UserId']
		date = row['PostCreationDate']
		result_set = execute_param_query(db, getUsersQuestionsAcceptedQuery(user, date))
		
		for tup in result_set:
			row['UsersQuestionsAccepted'] = tup[1]

		dict_writer.writerow(row)
	
	return 'Done'

def p_badges(db, file_name):
	dict_reader = csv.DictReader(open(file_name, 'r'))
	new_badges = open("badges.txt", 'w')

	p_badges = []

	for row in dict_reader:
		user = row['UserId']
		date = row['PostCreationDate']
		
		print "User: ",user
		print "Date: ",date,"\n"
		if user != 'None':
			
			result_set8 = execute_param_query(db, getBadges(user, date))
		
			bronze = 0
			silver = 0
			gold = 0

			for tup in result_set8:
				if badges.has_key(tup[1]):
					if badges[tup[1]] == 'Bronze':
						bronze += 1
					if badges[tup[1]] == 'Silver':
						silver += 1
					if badges[tup[1]] == 'Gold':
						gold += 1
				else:
					if tup[1] in p_badges:
						print ""
					else:
						p_badges.append(tup[1])
						new_badges.write(tup[1]+"\n")
					
			row['BronzeBadge'] = bronze
			row['SilverBadge'] = silver
			row['GoldBadge'] = gold
			
		#dict_writer.writerow(row)
	new_badges.close()
	print p_badges
	return 'Done'

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
				#new_badges.write(tup[0]+"\n")
				
	p_badges.sort()
	for elem in p_badges:
		new_badges.write(elem+"\n")
	new_badges.close()
	print p_badges
	return 'Done'

def save_csv(result_set):
	f = open('result.csv', 'w')
	writer = csv.writer(f)
	
	desc = result_set.description # Prende i campi della tabella
	fields = []
	for d in desc:
		fields = fields + [d[0]]

	writer.writerow(fields)

	for row in result_set: # Prende i record della tabella
		row_to_write = []
		for c in row:
			row_to_write = row_to_write + [smart_str(c)]
		writer.writerow(row_to_write)

	return 'Done'

questions_query = "SELECT Id AS PostId, Title, Body, Tags, CreationDate AS PostCreationDate, OwnerUserId AS UserId, AcceptedAnswerId AS PostAcceptedAnswerId FROM Posts WHERE Posts.PostTypeId = 1 AND Posts.OwnerUserId IS NOT NULL"
#save_csv(execute_param_query('stackoverflow.db', questions_query))
#create_dictionary('stackoverflow_posts.csv', 'stackoverflow_posts_dict.csv')
#build_dataset('academia.dump.db', 'result-set.csv', 'test.csv')
#p_badges('academia.dump.db', 'result-set.csv')
#print text_length('As from title. What kind of visa class do I have to apply for, in order to work as an academic in Japan ?')

# Build the stackoverflow dataset
#weekday('so_questions.csv', 'so_questions_week.csv')
#accepted('so_questions_week.csv', 'so_questions_acc.csv')
#os.remove('so_questions_week.csv')
#clean_len_code_body_title('so_questions_acc.csv', 'so_questions_len.csv')
#os.remove('so_questions_acc.csv')
#score('stackoverflow.db', 'so_questions_len.csv', 'so_questions_sco.csv')
#os.remove('so_questions_len.csv')
#badges('stackoverflow.db', 'so_questions_sco.csv', 'so_questions_badg.csv')
#os.remove('so_questions_sco.csv')
#users_answ_acc('stackoverflow.db', 'so_questions_badg.csv', 'so_questions_answacc.csv')
#os.remove('so_questions_badg.csv')
#users_quest_acc('stackoverflow.db', 'so_questions_answacc.csv', 'so_questions_final.csv')
#os.remove('so_questions_answacc.csv')

# Build the academia dataset
#weekday('ac_questions.csv', 'ac_questions_week.csv')
#accepted('ac_questions_week.csv', 'ac_questions_acc.csv')
#os.remove('ac_questions_week.csv')
#clean_len_code_body_title('ac_questions_acc.csv', 'ac_questions_len.csv')
#os.remove('ac_questions_acc.csv')
#score('academia.dump.db', 'ac_questions_len.csv', 'ac_questions_sco.csv')
#os.remove('ac_questions_len.csv')
#badge('academia.dump.db', 'ac_questions_sco.csv', 'ac_questions_badg.csv')
#os.remove('ac_questions_sco.csv')
#users_answ_acc('academia.dump.db', 'ac_questions_badg.csv', 'ac_questions_answacc.csv')
#os.remove('ac_questions_badg.csv')
#users_quest_acc('academia.dump.db', 'ac_questions_answacc.csv', 'ac_questions_final.csv')
#os.remove('ac_questions_answacc.csv')
