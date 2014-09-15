import csv
import random
import time, sys
from progressbar import Percentage, ProgressBar, Bar, RotatingMarker, FileTransferSpeed, ETA

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

#DON'T YOU DARE!
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
	
	widgets = ['Something: ', Percentage(), ' ', Bar(marker=RotatingMarker()), ' ', ETA()] ## PROGRESS BAR
	#pbar = ProgressBar(widgets=widgets, maxval=n_rows).start() ## PROGRESS BAR
	
	c = 0
	for row in dict_reader:
		#pbar.update(c+1)
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
		
		update_progress(c, n_rows)

		#time.sleep(1)
	#pbar.finish()

def update_progress(i, total):
	point = total / 100
	increment = total / 100
	sys.stdout.write('\r')
	# the exact output you're looking for:
	#sys.stdout.write("[%-20s] %d%%" % ('='*i, 10*i))
	sys.stdout.write("[" + "=" * (i / increment) +  " " * ((total - i)/ increment) + "]")
	sys.stdout.flush()

# Create the csv file with PostId and the relative most relevant topic (only one)
#	input:  the csv output from mallet
def add_topic(input_file, output_file):
	dict_reader = csv.DictReader(open(input_file, 'r'), delimiter=';') # DELIMITER
	
	f = ['PostId', 'Topic']
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=f) # DELIMITER
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header

	
	c = 0
	for row in dict_reader:
		#pbar.update(c+1)
		
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
		
		#update_progress(c, n_rows)

		#time.sleep(1)
	#pbar.finish()

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


#rand_id_topic_acc('../build-academia/output/academia_fase5.csv', 'rand_acc.csv', 300)
#rand_id_topic_hasansw_noacc('../build-academia/output/academia_fase5.csv', 'rand_hasansw_noacc.csv', 160)
#rand_id_topic_noansw('../build-academia/output/academia_fase5.csv', 'rand_hasansw_noacc.csv', 60)

#relevant_topics('10_topics/academia_t10_longsw.csv', 'prova.csv', 3, 10)
