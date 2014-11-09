import csv, re
from HTMLParser import HTMLParser
import string
import jpype
import os
from django.utils.encoding import smart_str

body_test = "The worldwide diffusion of social media has profoundly changed the way we communicate and access information. Increasingly, people try to solve domain-specific problems through interaction on social online Question and Answer (Q&A) sites. The enormous success of Stack Overflow, a community of 2.9 million programmers asking and providing answers about code development, attests this increasing trend. One of the biggest drawbacks of communication through social media is to appropriately convey sentiment through text. While display rules for emotions exist and are widely accepted for traditional face-to-face interaction, people might not be prepared for effectively dealing with the barriers of social media to non-verbal communication. Though, emotions matter, especially in the context of online Q&A communities where social reputation is a key factor for successful knowledge sharing. As a consequence, the design of systems and mechanisms for fostering emotional awareness in computer-mediated communication is becoming an important technical and social challenge for research in computer-supported collaborative work and social computing."


def get_senti_score(corpus):
	senti_score = sentiment_o.SentiStrengthgetScore(corpus)
	
	return senti_score

# JVM utilities
def start_JVM(path_libjvm='/usr/lib/jvm/java-7-openjdk-amd64/jre/lib/amd64/server/libjvm.so'):
	jpype.startJVM(path_libjvm, "-ea", "-Djava.class.path="+os.path.abspath("."))

def stop_JVM():
	jpype.shutdownJVM()
###############


# From a CSV file calculate the positive/negative sentiment score and output the results in a CSV file
#	param:
#		file_name = input CSV file
#		output_name = output CSV file
#		postId = string containing the field, on the file_name, of the id
#		textfield = string of the field to analyze for sentiment
#
#	output CSV file format:
#		Id
#		SentimentPositiveScore = {1, 2, 3, 4, 5} (default 'None' if something goes wrong)
#		SentimentNegativeScore = {-1, -2, -3, -4, -5} (default 'None' if something goes wrong)

def sentiment(file_name, output_file, postId='PostId', textfield='Corpus'):
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';')
	
	f = [postId, 'SentimentPositiveScore', 'SentimentNegativeScore']
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=f)
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header
	total = 0
	count = 0
	skipped = 0
	for row in dict_reader:
		total += 1
		corpus = row[textfield]
		r = {}
		r[postId] = row[postId]
		r['SentimentPositiveScore'] = str('None')
		r['SentimentNegativeScore'] = str('None')
		try:
			
			try:
				corpus = corpus.decode('unicode_escape').encode('ascii','ignore')
			except UnicodeDecodeError:
				try:
					corpus = unicode(corpus).encode('ascii', 'ignore')
				except Exception:
					corpus = unicode(corpus, errors='ignore') #smart_str(corpus)

			score = get_senti_score(corpus)
			
			s = score.split(" ")
			r['SentimentPositiveScore'] = s[0]
			r['SentimentNegativeScore'] = s[1]
			count += 1
		except Exception, e:
			print e
			print "Exception on id ", row[postId]
			dict_writer.writerow(r)
			skipped += 1
			continue
		dict_writer.writerow(r)

	stop_JVM()
	print "Initial posts ", total
	print "Post processed ", count
	print "Skipped: ", skipped
	return 'Done'





# function sentiment specialized for the case of the comment
#
#	input CSV file format (the output file of the function userscommentsonquestions_dataset from the module builddataset):
#		PostId
#		NumberOfUsersComment
#		TextOfUsersComments
#
#	output CSV file format:
#		PostId
#		NumberOfUsersComment
#		CommentSentimentPositiveScore = {1, 2, 3, 4, 5} (default 'None' if something goes wrong)
#		CommentSentimentNegativeScore = {-1, -2, -3, -4, -5} (default 'None' if something goes wrong)

def sentiment_comments(file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';')
	
	head = dict_reader.fieldnames
	#head.append('Corpus')
	f = ['PostId', 'NumberOfUsersComments', 'CommentSentimentPositiveScore', 'CommentSentimentNegativeScore']
	#head.append('SentimentPositiveScore')
	#head.append('SentimentNegativeScore')

	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=f)
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header
	total = 0
	count = 0
	skipped = 0
	for row in dict_reader:
		total += 1
		#body = row['Body']
		#title = row['Title']
		corpus = row['TextOfUsersComments']
		r = {}
		r['PostId'] = row['PostId']
		r['NumberOfUsersComments'] = row['NumberOfUsersComments']
		r['CommentSentimentPositiveScore'] = 'None'
		r['CommentSentimentNegativeScore'] = 'None'
		try:
			
			try:
				corpus = corpus.decode('unicode_escape').encode('ascii','ignore')
			except UnicodeDecodeError:
				#print r['PostId']
				try:
					corpus = unicode(corpus).encode('ascii', 'ignore')
				except Exception:
					corpus = unicode(corpus, errors='ignore') #smart_str(corpus)

			score = get_senti_score(corpus)
			
			s = score.split(" ")
			r['CommentSentimentPositiveScore'] = s[0]
			r['CommentSentimentNegativeScore'] = s[1]
				
			count += 1
		except Exception, e:
			print e
			print "Exception", row['PostId']
			dict_writer.writerow(r)
			skipped += 1
			continue
		dict_writer.writerow(r)

	stop_JVM()
	print "Initial posts ", total
	print "Post processed ", count
	print "Skipped: ", skipped
	return 'Done'

# Automaticly start a JVM, you can comment the next line and start the JVM when you need it
start_JVM()

# S = class Sentiment
S = jpype.JClass('Sentiment')

# sentiment_o = object of the class Sentiment
sentiment_o = S()

#sentiment('academia_questions.csv', 'ac_sentiment.csv')
#sentiment('stackoverflow_questions.csv', 'so_sentiment.csv')
#sentiment('dataset_liwcsenti.csv', 'ac_sentiment.csv')

