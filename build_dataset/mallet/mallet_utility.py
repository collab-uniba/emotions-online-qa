import csv
import random
import time, sys

topic_name = {'Topic0':'Name0',
	'Topic1':'Name1',
	'Topic2':'Name2',
	'Topic3':'Name3',
	'Topic4':'Name4',
	'Topic5':'Name5',
	'Topic6':'Name6',
	'Topic7':'Name7',
	'Topic8':'Name8',
	'Topic9':'Name9',
	'Topic10':'Name10',
	'Topic11':'Name11',
	'Topic12':'Name12',
	'Topic13':'Name13',
	'Topic14':'Name14',
	'Topic15':'Name15',
	'Topic16':'Name16',
	'Topic17':'Name17',
	'Topic18':'Name18',
	'Topic19':'Name19',
	'Topic20':'Name20',
	'Topic21':'Name21',
	'Topic22':'Name22',
	'Topic23':'Name23',
	'Topic24':'Name24',
	'Topic25':'Name25',
	'Topic26':'Name26',
	'Topic27':'Name27',
	'Topic28':'Name28',
	'Topic29':'Name29',
	'Topic30':'Name30',
	'Topic31':'Name31',
	'Topic32':'Name32',
	'Topic33':'Name33',
	'Topic34':'Name34',
	'Topic35':'Name35',
	'Topic36':'Name36',
	'Topic37':'Name37',
	'Topic38':'Name38',
	'Topic39':'Name39',
	}

# Dato il file che contiene, per ogni post, i topic con lo score corrispondente (file csv
# in output da Mallet) seleziona quali topic superano una certa soglia.
#
# parametri:
#	input_file: nome del file csv da cui leggere, il file deve contenere i campi:
#			- 'PostId'
#			- 'Topic0' che contiene lo score per il topic 0
#			- 'Topic1' che contiene lo score per il topic 1
#			- ...
#			- 'TopicN' che contiene lo score per il topic N
#	output_file: nome del file csv su cui scrivere i risultati, conterra' i campi:
#			- 'PostId'
#			- 'Name0' che ha valore 'yes' se lo score di 'Topic0' su input_file 
#				e' maggiore del parametro threshold, 'no' altrimenti
#			- 'Name1' che ha valore 'yes' se lo score di 'Topic1' su input_file 
#				e' maggiore del parametro threshold, 'no' altrimenti
#			- ...
#			- 'NameN' che ha valore 'yes' se lo score di 'TopicN' su input_file 
#				e' maggiore del parametro threshold, 'no' altrimenti
#	threshold: soglia con la quale vengono confrontati gli score dei topic
#
# I campi 'Name0', 'Name1', .., 'NameN' vengono presi dal dizionario globale topic_name.
# NB: TALE FUNZIONE NON e' MAI STATA UTILIZZATA
def convert_mallet(input_file, output_file, threshold):
	dict_reader = csv.DictReader(open(input_file, 'r'), delimiter=';') # DELIMITER
	
	#f = dict_reader.fieldnames
	f = ['PostId']
	for k in topic_name: #Add the topic's list names as output_file headers
		f.append(topic_name[k])
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=f) # DELIMITER
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header
	
	max_topics = 0
	no_topic_count = 0	

	for row in dict_reader:
		no_topic = True
		c_topics = 0 #Counter: topics membership

		r = {}
		r['PostId'] = row['PostId']
		for field in row:
			if field != 'PostId':
				if float(row[field]) > threshold:
					r[topic_name[field]] = 'yes'
					c_topics += 1
					no_topic = False
				else:
					r[topic_name[field]] = 'no'

		if no_topic == True:
			no_topic_count += 1

		if c_topics > max_topics:
			max_topics = c_topics

		dict_writer.writerow(r)

	print 'No. of topics without an associated topic: ', no_topic_count
	print 'Max topics membership: ', max_topics

# Extract n_posts (random) with the first most relevant n_topics
#	input_file: the csv output from mallet  

# Dato il file che contiene, per ogni post, i topic con lo score corrispondente (file csv
# in output da Mallet) seleziona n post random con i rispettivi m topic con score piu' alto.
#
# parametri:
#	input_file: nome del file csv da cui leggere, il file deve contenere i campi:
#			- 'PostId'
#			- 'Topic0' che contiene lo score per il topic 0
#			- 'Topic1' che contiene lo score per il topic 1
#			- ...
#			- 'TopicN' che contiene lo score per il topic N
#	output_file: nome del file csv su cui scrivere i risultati, conterra'  n_posts istanze
#		random ed i campi:
#			- 'PostId'
#			- '1 topic' che contiene lo score, tra i topic, piu' alto per il post corrispondente
#			- '2 topic' che contiene il secondo score, tra i topic, piu' alto per il post corrispondente
#			- ...
#			- 'n_topics topic' che contiene n_topics-esimo score, tra i topic, piu' alto per il post corrispondente
#	n_topics: numero dei topic piu' alti che si vogliono selezionare
#	n_posts: numero di post random che si vogliono selezionare
def relevant_topics(input_file, output_file, n_topics, n_posts):
	dict_reader = csv.DictReader(open(input_file, 'r'), delimiter=';') # DELIMITER
	
	f = ['PostId']
	for c in range(1, n_topics+1): #Add the topic's list names as output_file headers
		f.append(str(c)+' topic')
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=f) # DELIMITER
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header

	n_rows = len(list(csv.reader(open(input_file)))) - 1
	posts_line = []	
	for c in range(0, n_posts):
		posts_line.append(random.randint(0, n_rows))
	posts_line = sorted(posts_line)
	
	c = 0
	for row in dict_reader:
		
		if c in posts_line:
			topics = []
			r = {}
			r['PostId'] = row['PostId']
			for field in row:
				if field != 'PostId':
					topics.append(float(row[field]))
		
			topics = sorted(topics, reverse=True)

			for c in range(1, n_topics+1):
				r[str(c)+' topic'] = topics[c-1]

			dict_writer.writerow(r)
		c += 1

# Dato il file che contiene, per ogni post, i topic con lo score corrispondente (file csv
# in output da Mallet) seleziona il topic con score piu' alto.
#
# parametri:
#	input_file: nome del file csv da cui leggere, il file deve contenere i campi:
#			- 'PostId'
#			- 'Topic0' che contiene lo score per il topic 0
#			- 'Topic1' che contiene lo score per il topic 1
#			- ...
#			- 'TopicN' che contiene lo score per il topic N
#	output_file: nome del file csv su cui scrivere i risultati, conterra' i campi:
#			- 'PostId'
#			- 'Topic' che contiene l'id del topic (0,1,...,N) con score piu' alto
#				per il post corrispondente
def add_topic(input_file, output_file):
	dict_reader = csv.DictReader(open(input_file, 'r'), delimiter=';') # DELIMITER
	
	f = ['PostId', 'Topic']
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=f) # DELIMITER
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header

	
	c = 0
	for row in dict_reader:
		
		topics = []
		curr_topic = ''
		curr_prob = 0
		r = {}
		r['PostId'] = row['PostId']
		for field in row:
			if field != 'PostId':
				if curr_prob < float(row[field]):
					curr_prob = float(row[field])
					curr_topic = field
				#topics.append(float(row[field]))
		r['Topic'] = curr_topic.replace('Topic', '')
		#topics = sorted(topics, reverse=True)

		#for c in range(1, n_topics+1):
		#	r[str(c)+' topic'] = topics[c-1]

		dict_writer.writerow(r)
		c += 1
		
# Seleziona n post random che hanno ricevuto una risposta accettata.
#
# parametri:
#	input_file: nome del file csv da cui leggere, deve contenere almeno i campi:
#			- 'PostId'
#			- 'Accepted' che ha valori 'yes' se il post ha una risposta accettata, 
#				'no' altrimenti
#			- 'Topic' id del topic associato al post
#	output_file: nome del file csv su cui scrivere i risultati, conterra' n_posts istanze
#		(dove il campo 'Accepted' vale 'yes') ed i campi:
#			- 'PostId'
#			- 'Topic' id del topic associato al post
#	n_posts: numero di post che si desiderano selezionare
def rand_id_topic_acc(input_file, output_file, n_posts):
	dict_reader = csv.DictReader(open(input_file, 'r'), delimiter=';') # DELIMITER
	
	f = ['PostId', 'Topic']
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=f) # DELIMITER
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header

	posts_acc = []
	for row in dict_reader:
		if row['Accepted'] == 'yes':
			posts_acc.append([row['PostId'], row['Topic']])
	
	n_rows = len(posts_acc)
	
	posts_line = []
	posts_line = random.sample(range(0, n_rows - 1), n_posts)

	print posts_line
	print 'Number of posts with accepted answer: ', n_rows
	print 'Number of selected posts: ', len(posts_line)	

	c = 0
	i = 0
	for row in posts_acc:	
		if c in posts_line:
			dict_writer.writerow({'PostId':row[0], 'Topic':row[1]})
			posts_line.remove(c)
			i += 1
			#print c
		c += 1
	#print c
	print 'No. of output posts: ', i
	print posts_line

# Seleziona n post random che non hanno ricevuto una risposta accettata ma
# che hanno ricevuto almeno una risposta
#
# parametri:
#	input_file: nome del file csv da cui leggere, deve contenere almeno i campi:
#			- 'PostId'
#			- 'Accepted' che ha valori 'yes' se il post ha una risposta accettata, 
#				'no' altrimenti
#			- 'HasAnswer' che ha valori 'yes' se il post ha almeno una risposta, 
#				'no' altrimenti
#			- 'Topic' id del topic associato al post
#	output_file: nome del file csv su cui scrivere i risultati, conterra' n_posts istanze
#		(dove il campo 'Accepted' vale 'no' ed il campo 'HasAnswer' vale 'yes') ed i campi:
#			- 'PostId'
#			- 'Topic' id del topic associato al post
#	n_posts: numero di post che si desiderano selezionare
def rand_id_topic_hasansw_noacc(input_file, output_file, n_posts):
	dict_reader = csv.DictReader(open(input_file, 'r'), delimiter=';') # DELIMITER
	
	f = ['PostId', 'Topic']
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=f) # DELIMITER
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header

	posts_acc = []
	for row in dict_reader:
		if row['Accepted'] == 'no' and row['HasAnswer'] == 'yes':
			posts_acc.append([row['PostId'], row['Topic']])
	
	n_rows = len(posts_acc)
	
	posts_line = []
	posts_line = random.sample(range(0, n_rows - 1), n_posts)

	print posts_line
	print 'Number of posts with accepted answer: ', n_rows
	print 'Number of selected posts: ', len(posts_line)	

	c = 0
	i = 0
	for row in posts_acc:	
		if c in posts_line:
			dict_writer.writerow({'PostId':row[0], 'Topic':row[1]})
			posts_line.remove(c)
			i += 1
			#print c
		c += 1
	#print c
	print 'No. of output posts: ', i
	print posts_line

# Seleziona n post random che non hanno ricevuto una risposta accettata ma
# che hanno ricevuto almeno una risposta
#
# parametri:
#	input_file: nome del file csv da cui leggere, deve contenere almeno i campi:
#			- 'PostId'
#			- 'NoAnswer' che ha valori 'yes' se il post non ha alcuna risposta, 
#				'no' altrimenti
#			- 'Topic' id del topic associato al post
#	output_file: nome del file csv su cui scrivere i risultati, conterra' n_posts istanze
#		(dove il campo 'NoAnswer' vale 'yes') ed i campi:
#			- 'PostId'
#			- 'Topic' id del topic associato al post
#	n_posts: numero di post che si desiderano selezionare
def rand_id_topic_noansw(input_file, output_file, n_posts):
	dict_reader = csv.DictReader(open(input_file, 'r'), delimiter=';') # DELIMITER
	
	f = ['PostId', 'Topic']
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=f) # DELIMITER
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header

	posts_acc = []
	for row in dict_reader:
		if row['NoAnswer'] == 'yes':
			posts_acc.append([row['PostId'], row['Topic']])
	
	n_rows = len(posts_acc)
	
	posts_line = []
	posts_line = random.sample(range(0, n_rows - 1), n_posts)

	print posts_line
	print 'Number of posts with accepted answer: ', n_rows
	print 'Number of selected posts: ', len(posts_line)	

	c = 0
	i = 0
	for row in posts_acc:	
		if c in posts_line:
			dict_writer.writerow({'PostId':row[0], 'Topic':row[1]})
			posts_line.remove(c)
			i += 1
			#print c
		c += 1
	#print c
	print 'No. of output posts: ', i
	print posts_line
