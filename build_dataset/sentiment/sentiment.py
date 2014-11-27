import csv
import string
import jpype
import os

body_test = "The worldwide diffusion of social media has profoundly changed the way we communicate and access information. Increasingly, people try to solve domain-specific problems through interaction on social online Question and Answer (Q&A) sites. The enormous success of Stack Overflow, a community of 2.9 million programmers asking and providing answers about code development, attests this increasing trend. One of the biggest drawbacks of communication through social media is to appropriately convey sentiment through text. While display rules for emotions exist and are widely accepted for traditional face-to-face interaction, people might not be prepared for effectively dealing with the barriers of social media to non-verbal communication. Though, emotions matter, especially in the context of online Q&A communities where social reputation is a key factor for successful knowledge sharing. As a consequence, the design of systems and mechanisms for fostering emotional awareness in computer-mediated communication is becoming an important technical and social challenge for research in computer-supported collaborative work and social computing."


# Calcola il sentiment score positivo e negativo per il testo che si vuole
# analizzare.
#
# parametri:
#	corpus: testo che si vuole analizzare
#
# output:
#	restituisce una stringa con il sentiment score positivo seguito dal 
#	sentiment score negativo separati da uno spazio.
def get_senti_score(corpus):
	senti_score = sentiment_o.SentiStrengthgetScore(corpus)
	
	return senti_score

# JVM utilities
def start_JVM(path_libjvm='/usr/lib/jvm/java-7-openjdk-amd64/jre/lib/amd64/server/libjvm.so'):
	jpype.startJVM(path_libjvm, "-ea", "-Djava.class.path="+os.path.abspath("."))

def stop_JVM():
	jpype.shutdownJVM()
###############


# Calcola il sentiment score positivo ed il sentiment score negativo per ogni testo contenuto 
# nel file di input.
#
# parametri:
#	file_name: nome del file csv contenente i testi da analizzare, deve contenere almeno:
#			- 'PostId'
#			- il campo con il testo da analizzare
#	output_file: nome del file csv su cui scrivere i risultati, conterra' i campi:
#			- 'PostId'
#			- 'SentimentPositiveScore' con valore nell'intervallo [1,5], conterra' valore
#				'None' se il calcolo non va a buon fine
#			- 'SentimentNegativeScore' con valore nell'intervallo [-1,-5], conterra' valore
#				'None' se il calcolo non va a buon fine
#	text_field: nome del campo che contiene il testo che si vuole analizzare
def sentiment(file_name, output_file, textfield='Corpus'):
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';')
	
	f = ['PostId', 'SentimentPositiveScore', 'SentimentNegativeScore']
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=f)
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header
	total = 0
	count = 0
	skipped = 0
	for row in dict_reader:
		total += 1
		corpus = row[textfield]
		r = {}
		r['PostId'] = row['PostId']
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
			print "Exception on id ", row['PostId']
			dict_writer.writerow(r)
			skipped += 1
			continue
		dict_writer.writerow(r)

	stop_JVM()
	print "Initial posts ", total
	print "Post processed ", count
	print "Skipped: ", skipped
	return 'Done'


# Calcola il sentiment score positivo ed il sentiment score negativo per ogni testo contenuto 
# nel file di input.
#
# parametri:
#	file_name: nome del file csv contenente i testi da analizzare, deve contenere almeno:
#			- 'PostId'
#			- 'TextOfUsersComments' contiene il testo da analizzare
#			- 'NumberOfUsersComments'
#	output_file: nome del file csv su cui scrivere i risultati, conterra' i campi:
#			- 'PostId'
#			- 'NumberOfUsersComments'
#			- 'CommentSentimentPositiveScore' con valore nell'intervallo [1,5] risultato del calcolo
#				sul campo 'TextOfUsersComments', conterra' valore 'None' se il calcolo non va a buon fine
#			- 'CommentSentimentNegativeScore' con valore nell'intervallo [-1,-5] risultato del calcolo
#				sul campo 'TextOfUsersComments', conterra' valore 'None' se il calcolo non va a buon fine
def sentiment_comments(file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';')
	
	head = dict_reader.fieldnames
	
	f = ['PostId', 'NumberOfUsersComments', 'CommentSentimentPositiveScore', 'CommentSentimentNegativeScore']
	
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
				try:
					corpus = unicode(corpus).encode('ascii', 'ignore')
				except Exception:
					corpus = unicode(corpus, errors='ignore')

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

# Avvia la JVM nel momento in cui viene importato il file come libreria, si puo' commentare tale riga e avviarla solo quando necessario
start_JVM()

# S = carica la classe Sentiment
S = jpype.JClass('Sentiment')

# sentiment_o = oggetto della classe Sentiment
sentiment_o = S()
