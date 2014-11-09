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
from django.utils.encoding import smart_str
from HTMLParser import HTMLParser
from badgesDict import badges



def getUsersAnswersAcceptedQuery(user, date):
	return "SELECT ownerID AS UserID, count(postID) AS UsersAnswersAccepted FROM acceptedanswer_mv WHERE ownerID = " + user + " AND ts_voteDate < date(\'" + date + "\')"
	#return "SELECT Posts.OwnerUserId AS UserId, count(Posts.Id) AS UsersAnswersAccepted FROM Posts INNER JOIN Votes ON Posts.Id = Votes.PostId WHERE Posts.PostTypeId = 2 AND Posts.OwnerUserId = " + user + " AND date(Votes.CreationDate) < date(\'" + date + "\') AND Votes.VoteTypeId = 1"

def getUsersQuestionsAcceptedQuery(user, date):
	return "SELECT ownerID AS UserID, count(postID) AS UsersQuestionsAccepted FROM questwithacceptedanswer_mv WHERE ownerID = " + user + " AND ts_voteDate < date(\'" + date + "\')"
	#return "SELECT Posts.OwnerUserId AS UserId, count(Posts.Id) AS UsersQuestionsAccepted FROM Posts INNER JOIN Votes ON Posts.AcceptedAnswerId = Votes.PostId WHERE Posts.PostTypeId = 1 AND Posts.AcceptedAnswerId IS NOT NULL  AND Posts.OwnerUserId = " + user + " AND date(Votes.CreationDate) < date(\'" + date + "\') AND Votes.VoteTypeId = 1"

# Estrae il numero di upvotes, prima di una certa data (@Date), ottenuti dalle domande postate da un certo utente (@User) */
def getQuestUpVotes(user, date):
	return "SELECT u_ownerID as UserID, count(u_voteID) as UpVotesQuest FROM questionupvotes_mv WHERE u_ownerID = " + user + " AND uts_voteDate < date(\'" + date + "\')"
	#return "SELECT Posts.OwnerUserId AS UserId, count(Posts.Id) AS UpVotesQuest FROM Posts INNER JOIN Votes ON Posts.Id = Votes.PostId WHERE Posts.PostTypeId = 1 AND Votes.VoteTypeId = 2 AND date(Votes.CreationDate) < date(\'" + date + "\') AND Posts.OwnerUserId = " + user

# Estrae il numero di downvotes, prima di una certa data (@Date), ottenuti dalle domande postate da un certo utente (@User) */
def getQuestDownVotes(user, date):
	return "SELECT d_ownerID as UserID, count(d_voteID) as DownVotesQuest FROM questiondownvotes_mv WHERE d_ownerID = " + user + " AND dts_voteDate < date(\'" + date + "\')"
	#return "SELECT Posts.OwnerUserId AS UserId, count(Posts.Id) AS DownVotesQuest FROM Posts INNER JOIN Votes ON Posts.Id = Votes.PostId WHERE Posts.PostTypeId = 1 AND Votes.VoteTypeId = 3 AND date(Votes.CreationDate) < date(\'" + date + "\') AND Posts.OwnerUserId = " + user

# Estrae il numero di upvotes, prima di una certa data (@Date), ottenuti dalle risposte postate da un certo utente (@User) */
def getAnswUpVotes(user, date):
	return "SELECT u_ownerID as UserID, count(u_voteID) as UpVotesAnsw FROM answerupvotes_mv WHERE u_ownerID = " + user + " AND uts_voteDate < date(\'" + date + "\')"
	#return "SELECT Posts.OwnerUserId AS UserId, count(Posts.Id) AS UpVotesAnsw FROM Posts INNER JOIN Votes ON Posts.Id = Votes.PostId WHERE Posts.PostTypeId = 2 AND Votes.VoteTypeId = 2 AND date(Votes.CreationDate) < date(\'" + date + "\') AND Posts.OwnerUserId = " + user

# Estrae il numero di downvotes, prima di una certa data (@Date), ottenuti dalle risposte postate da un certo utente (@User) */
def getAnswDownVotes(user, date):
	return "SELECT d_ownerID as UserID, count(d_voteID) as AnswerDownvotesScore FROM answerdownvotes_mv WHERE d_ownerID = " + user + " AND dts_voteDate < date(\'" + date + "\')"
	#return "SELECT Posts.OwnerUserId AS UserId, count(Posts.Id) AS DownVotesAnsw FROM Posts INNER JOIN Votes ON Posts.Id = Votes.PostId WHERE Posts.PostTypeId = 2 AND Votes.VoteTypeId = 3 AND date(Votes.CreationDate) < date(\'" + date + "\') AND Posts.OwnerUserId = " + user

# commenti di un utente di una domanda (@PostId) prima della data di accettazione (@Date)
def getUsersCommentsBeforeAccDate(postid, vote_date):
	return "SELECT c_Id, c_text FROM userscommentsquestions_mv WHERE c_ts_creationDate < \'" + vote_date + "\' AND q_Id = " + postid

# commenti di un utente di una domanda (@PostId)
def getUsersComments(postid):
	return "SELECT c_Id, c_text FROM userscommentsquestions_mv WHERE q_Id = " + postid


# Estrae l'insieme dei badge sbloccati da un utente (@User) prima di una certa data (@Date) */
def getBadges(user, date):
	return "SELECT Badges.UserId, Badges.Name FROM Badges WHERE Badges.UserId = " + user + " AND Badges.Date < \'" + date + "\'" 

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
	return re.sub('<code>[\s\S.]+?</code>', ' ', html)

def clean_body(html):
	return del_tags(del_code(html))

def del_punctuation(text):
	return text.translate(string.maketrans ("" , ""), string.punctuation) # http://www.tutorialspoint.com/python/string_translate.htm

def text_length(text):
	#text_cleaned_punc = del_punctuation(text)
	#text_cleaned = re.findall(r"[\w']+", text_cleaned_punc)
	text_splitted = re.findall(r"[\w']+", text)
	word = len(text_splitted)
	
	return word

def create_dictionary(file_name, output):
	print "Processing..."
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';')

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

	w = csv.writer(open(output, "w"), delimiter=';')
	for elem in sorted_dict:
		w.writerow([elem,dictionary[elem]])

	print "Done..."

	return sorted_dict

def execute_param_query(database, query):
	#conn = sqlite3.connect(db)
	conn = MySQLdb.connect(host="localhost",user="root",
                  passwd="root",db=database)
	c = conn.cursor()
	c.execute(query)
	c.fetchall()
	return c

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

def accepted(file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';')  # DELIMITER
	
	head = dict_reader.fieldnames
	f = ['PostId', 'Accepted', 'HasAnswer', 'NoAnswer']
	#head.append('Accepted')
	
	
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

def clean_len_code_body_title(file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'))
	
	head = dict_reader.fieldnames
	#f = ['PostId', 'BodyLength', 'TitleLength', 'CodeSnippet']
	#head.append('BodyCleaned')
	head.append('BodyLength')
	head.append('TitleLength')
	head.append('CodeSnippet')
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), head)
	dict_writer.writerow(dict((fn,fn) for fn in head)) #Scrive gli header
	count = 0
	for row in dict_reader:
		#r = {}
		#r['PostId'] = row['PostId']
		body = row['Body']
		title = row['Title']
		try:
			

			body_cleaned = clean_body(body.decode('unicode_escape').encode('ascii','ignore'))
			#r['BodyCleaned'] = body_cleaned
			row['Body'] = body_cleaned

			#r['TitleLength'] = text_length(title)
			#r['BodyLength'] = text_length(body_cleaned)
			row['TitleLength'] = text_length(title)
			row['BodyLength'] = text_length(body_cleaned)

			code_snippet = "no"
			if '<code>' in body:
				code_snippet = "yes"

			#r['CodeSnippet'] = code_snippet
			row['CodeSnippet'] = code_snippet
			count += 1
		except Exception:
			continue
		dict_writer.writerow(row)
	print 'Post processed: ', count
	return 'Done'

def scorequp(db, file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';')
	
	head = dict_reader.fieldnames
	f = ['PostId', 'QuestionUpVotes']
	#head.append('QuestionUpVotes')
	
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=f)
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header
	count = 0
	for row in dict_reader:
		r = {}
		r['PostId'] = row['PostId']
		user = row['UserId']
		date = row['PostCreationDate']
		#print user
		#print date
		#print "start queries"
		result_set4 = execute_param_query(db, getQuestUpVotes(user, date))
		#print "end queries"
		
		for tup in result_set4:
			q_up = tup[1]
		
		r['QuestionUpVotes'] = q_up

		dict_writer.writerow(r)
		count += 1
	
	print 'Post processed: ', count
	return 'Done'

def scoreqdown(db, file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';')
	
	head = dict_reader.fieldnames
	f = ['PostId', 'QuestionDownVotes']
	#head.append('QuestionDownVotes')
	
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=f)
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header
	
	for row in dict_reader:
		r = {}
		r['PostId'] = row['PostId']
		user = row['UserId']
		date = row['PostCreationDate']
		#print user
		#print date
		#print "start queries"
		result_set5 = execute_param_query(db, getQuestDownVotes(user, date))
		#print "end queries"
		
		for tup in result_set5:
			q_down = tup[1]
		
		r['QuestionDownVotes'] = q_down

		dict_writer.writerow(r)
	
	return 'Done'

def scorequestion(db, file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'))
	
	head = dict_reader.fieldnames
	f = ['PostId', 'QuestionScore']
	#head.append('QuestionScore')
	
	
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
		result_set4 = execute_param_query(db, getQuestUpVotes(user, date))
		result_set5 = execute_param_query(db, getQuestDownVotes(user, date))
		print "end queries"
		
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


def scoreaup(db, file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';')
	
	head = dict_reader.fieldnames
	#head.append('AnswerUpVotes')
	f = ['PostId', 'AnswerUpVotes']
	
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=f)
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header
	
	for row in dict_reader:
		r = {}
		r['PostId'] = row['PostId']
		user = row['UserId']
		date = row['PostCreationDate']
		#print user
		#print date
		#print "start queries"
		result_set6 = execute_param_query(db, getAnswUpVotes(user, date))
		#print "end queries"
		
		for tup in result_set6:
			a_up = tup[1]
		
		r['AnswerUpVotes'] = a_up

		dict_writer.writerow(r)
	
	return 'Done'

def scoreadown(db, file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';')
	
	head = dict_reader.fieldnames
	f = ['PostId', 'AnswerDownVotes']
	#head.append('AnswerDownVotes')
	
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=f)
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header
	
	for row in dict_reader:
		r = {}
		r['PostId'] = row['PostId']
		user = row['UserId']
		date = row['PostCreationDate']
		#print user
		#print date
		#print "start queries"
		result_set7 = execute_param_query(db, getAnswDownVotes(user, date))
		#print "end queries"
		
		for tup in result_set7:
			a_down = tup[1]
		
		r['AnswerDownVotes'] = a_down


		dict_writer.writerow(r)
	
	return 'Done'

def scoreanswer(db, file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'))
	
	head = dict_reader.fieldnames
	f = ['PostId', 'AnswerScore']
	#head.append('AnswerScore')
	
	
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


def score(file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'))
	
	head = dict_reader.fieldnames
	head.append('QuestionScore')
	head.append('AnswerScore')
	
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), head)
	dict_writer.writerow(dict((fn,fn) for fn in head)) #Scrive gli header
	
	for row in dict_reader:
		q_up = row['QuestionUpVotes']
		q_down = row['QuestionDownVotes']
		a_up = row['AnswerUpVotes']
		a_down = row['AnswerDownVotes']

		q_score = q_up - q_down
		a_score = a_up - a_down
			
		row['QuestionScore'] = q_score
		row['AnswerScore'] = a_score

		dict_writer.writerow(row)
	
	return 'Done'

def calculate_quest_score(file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';')
	
	head = dict_reader.fieldnames
	f = ['PostId', 'QuestionScore']
	#head.append('QuestionScore')
	
	
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

def calculate_answ_score(file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';')
	
	head = dict_reader.fieldnames
	f = ['PostId', 'AnswerScore']
	#head.append('AnswerScore')
	
	
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


def users_answ_acc(db, file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';')
	
	head = dict_reader.fieldnames
	#print 'PostId',head
	f = ['PostId', 'UsersAnswersAccepted']
	#f.append('PostId')
	#f.append('UsersAnswersAccepted')
	
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=f)
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header
	count = 0
	for row in dict_reader:
		r = {}
		r['PostId'] = row['PostId']
		user = row['UserId']
		date = row['PostCreationDate']
		print r['PostId']
		print 'Start query'
		result_set = execute_param_query(db, getUsersAnswersAcceptedQuery(user, date))
		print 'End query'
		
		for tup in result_set:
			r['UsersAnswersAccepted'] = tup[1]		

		dict_writer.writerow(r)
		count += 1
	
	print 'Post processed: ', count
	return 'Done'
	
def users_quest_acc(db, file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';')
	
	head = dict_reader.fieldnames
	f = ['PostId', 'UsersQuestionsAccepted']
	#head.append('UsersQuestionsAccepted')
	
	
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

def save_csv(result_set, filename):
	f = open(filename, 'w')
	
	writer = csv.writer(f)
	print result_set
	
	desc = result_set.description # Prende i campi della tabella
	fields = []
	for d in desc:
		fields = fields + [d[0]]

	writer.writerow(fields)

	for row in result_set: # Prende i record della tabella
		row_to_write = []
		for c in row:
			if c != '':
				row_to_write = row_to_write + [smart_str(c)]
		writer.writerow(row_to_write)

	return 'Done'

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
						body_cleaned = clean_body(unicode(c).encode('ascii', 'ingore'))
					except Exception:	
						body_cleaned = clean_body(smart_str(c))
				#body_cleaned = clean_body(c) #smart_str(c))
				
					
				if '<code>' in smart_str(c):
					code_snippet = "yes"
					
				try:
					row_to_write = row_to_write + [body_cleaned.decode('unicode_escape').encode('ascii','ignore')]
				except UnicodeDecodeError:
					print count
					try:
						row_to_write = row_to_write + [unicode(body_cleaned).encode('ascii', 'ingore')]
					except Exception:	
						row_to_write = row_to_write + [smart_str(body_cleaned)]
					
				count += 1
			else:
				row_to_write = row_to_write + [smart_str(c)]
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

def len_body_title(file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';') # DELIMITER
	
	head = dict_reader.fieldnames
	f = ['PostId', 'BodyLength', 'TitleLength']
	#head.append('BodyCleaned')
	#head.append('BodyLength')
	#head.append('TitleLength')
	#head.append('CodeSnippet')
	
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

def run_threads(input_dir, out_dir, func, db):
	input_files = os.listdir(input_dir)			
	os.mkdir(out_dir)
	for s in input_files:
		o = s.replace('.csv', '_out.csv') 
		
		print o
		t = threading.Thread(target=func, args=(db, input_dir+s, out_dir+o)) 
		#thread_list.append(t)
		t.start()
		
	return 'Done'


def split_csv(file_name, func, tmp_dir, n):
	os.mkdir(tmp_dir)	

	dict_reader = csv.DictReader(open(file_name, 'r'))
	n_rows = len(list(csv.reader(open(file_name)))) - 1
	
	head = dict_reader.fieldnames
	
	n_rows_splitted = int(float(n_rows)/float(n))

	print n_rows_splitted

	count_segm = 0
	count_row = 0
	
	thread_list = []
	segment = []
	#files = []
	
	for row in dict_reader:
		if count_row == 0:
			count_segm += 1
			#curr_file = file_name.replace('.csv', '_'+str(count_segm)+'.csv')
			curr_file = tmp_dir+str(count_segm)+'.csv'
			segment.append(curr_file)
			b = open(curr_file, 'wr')
			dict_writer = csv.DictWriter(b, head)
			dict_writer.writerow(dict((fn,fn) for fn in head)) #Scrive gli header
			print "Segment ",count_segm
		
		dict_writer.writerow(row)
		count_row += 1
		
		if count_row == n_rows_splitted:
			if count_segm < n:
				b.close()
				count_row = 0
				
		
		
	for s in segment:
		o = s.replace('.csv', '_out.csv') # Sostituire nome
		#files.append(o)
		print o
		t = threading.Thread(target=func, args=('academia', s, o)) # Chiamata alla funzione (sostituire chiamata)
		thread_list.append(t)
		t.start()
		
	for s in segment:
		os.remove(s)

	#m(files)
	
	return 'Done'

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
					r['Corpus'] = unicode(corpus).encode('ascii', 'ingore')
				except Exception:
					r['Corpus'] = smart_str(corpus)

			
		except Exception:
			dict_writer.writerow(r)
			continue
		dict_writer.writerow(r)
	print 'Post processed: ', count
	return 'Done'

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

# Costruisce un csv con PostId, NumberOfUsersComments, TextOfUsersComments
def userscommentsonquestions_dataset(database, output_file):
	
	# Inizializza il csv da scrivere
	fieldnames = ['PostId' , 'NumberOfUsersComments', 'TextOfUsersComments']
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=fieldnames) # DELIMITER
	dict_writer.writerow(dict((fn,fn) for fn in fieldnames)) #Scrive gli header

	# Query per ottenere tutte le domande con la relativa data di accettazione della risposta qual'ora ci fosse
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
			#print row[0], ' Accepted'
			comments = execute_param_query(database, getUsersCommentsBeforeAccDate(str(row[0]), str(row[2])))
		else:
			#print row[0], ' Not Accepted'
			comments = execute_param_query(database, getUsersComments(str(row[0])))

		
		w_row['NumberOfUsersComments'] = str(comments.rowcount)
		w_row['TextOfUsersComments'] = str()
		for comm in comments:
			# comm[0] = c_Id
			# comm[1] = c_text
			w_row['TextOfUsersComments'] += ' ' + comm[1]
			#w_row['TextOfUsersComments'] += ' ' + unicode(comm[1], errors='ignore')
		
		dict_writer.writerow(w_row)


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
						body = unicode(c, errors='ignore')#smart_str(corpus)

				body_cleaned = clean_body(body) #smart_str(c))
				blen = text_length(body_cleaned)

				row_to_write = row_to_write + [body_cleaned]
				count += 1

			elif i == title_field:
				tlen = text_length(c)
				row_to_write = row_to_write + [c] # smart_str(c)
			else:
				row_to_write = row_to_write + [str(c)] # smart_str(c)
			i += 1
		row_to_write = row_to_write + [str(tlen)]
		row_to_write = row_to_write + [str(blen)]
		writer.writerow(row_to_write)
	

	print "Total post",total
	print "Post processed ",count
	return 'Done'


questions_query = "SELECT q_postID AS PostId, q_title AS Title, q_body AS Body, q_tags AS Tags, q_postDate AS PostCreationDate, q_ownerID AS UserId, q_acceptedAnswerId AS PostAcceptedAnswerId, q_answerCount AS AnswerCount FROM questions_mv"

questions_query_id_body_title_tags = "SELECT q_postID AS PostId, q_title AS Title, q_body AS Body, q_tags AS Tags FROM questions_mv"

#if __name__ == 'main':
#conv_senti_weekday_time('output/academia_fase5_cl.csv', 'output/academia_final.csv')

#split('output/academia_questions.csv', 'output/tmp/', 4)

#save_csv(execute_param_query('academia', questions_query), 'academia_questions.csv')
#save_csv_code_snip(execute_param_query('academia', questions_query), 'output/academia_questions.csv')

