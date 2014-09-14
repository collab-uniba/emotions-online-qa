import csv, re
from HTMLParser import HTMLParser
import string
import jpype
import os
from django.utils.encoding import smart_str

body1 = "The worldwide diffusion of social media has profoundly changed the way we communicate and access information. Increasingly, people try to solve domain-specific problems through interaction on social online Question and Answer (Q&A) sites. The enormous success of Stack Overflow, a community of 2.9 million programmers asking and providing answers about code development, attests this increasing trend. One of the biggest drawbacks of communication through social media is to appropriately convey sentiment through text. While display rules for emotions exist and are widely accepted for traditional face-to-face interaction, people might not be prepared for effectively dealing with the barriers of social media to non-verbal communication. Though, emotions matter, especially in the context of online Q&A communities where social reputation is a key factor for successful knowledge sharing. As a consequence, the design of systems and mechanisms for fostering emotional awareness in computer-mediated communication is becoming an important technical and social challenge for research in computer-supported collaborative work and social computing."

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
	return re.sub('<code>[\s\S.]+</code>', '', html)

def clean_body(html):
	return del_tags(del_code(html))

def del_punctuation(text):
	return text.translate(string.maketrans ("" , ""), string.punctuation)

def get_senti_score(corpus):
	#S = jpype.JClass('Sentiment')
	#sentiment = S()

	senti_score = sentiment_o.SentiStrengthgetScore(corpus)
	
	return senti_score

def sentiment(file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';')
	
	head = dict_reader.fieldnames
	#head.append('Corpus')
	f = ['PostId', 'SentimentPositiveScore', 'SentimentNegativeScore']
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
		corpus = row['Corpus']
		r = {}
		r['PostId'] = row['PostId']
		r['SentimentPositiveScore'] = 0
		r['SentimentNegativeScore'] = 0
		try:
			
			#body_cleaned = body.decode('unicode_escape').encode('ascii','ignore')
			#body_cleaned = smart_str(body)
			#body_cleaned = re.escape(body)

			
			#corpus = title + " " + body
			
			try:
				corpus = corpus.decode('unicode_escape').encode('ascii','ignore')
			except UnicodeDecodeError:
				#print r['PostId']
				try:
					corpus = unicode(corpus).encode('ascii', 'ingore')
				except Exception:
					corpus = unicode(corpus, errors='ignore') #smart_str(corpus)

			#score = get_senti_score(corpus.decode('unicode_escape').encode('ascii','ignore'))
			score = get_senti_score(corpus)
			
			s = score.split(" ")
			r['SentimentPositiveScore'] = s[0]
			r['SentimentNegativeScore'] = s[1]
			count += 1
		except Exception, e:
			print e
			print "Exception", row['PostId']
			dict_writer.writerow(r)
			skipped += 1
			continue
		dict_writer.writerow(r)

	jpype.shutdownJVM()
	print "Initial posts ", total
	print "Post processed ", count
	print "Skipped: ", skipped
	return 'Done'


jpype.startJVM("/usr/lib/jvm/java-7-openjdk-amd64/jre/lib/amd64/server/libjvm.so", "-ea", "-Djava.class.path="+os.path.abspath("."))
S = jpype.JClass('Sentiment')
sentiment_o = S()
#sentiment('academia_questions.csv', 'ac_sentiment.csv')
#sentiment('stackoverflow_questions.csv', 'so_sentiment.csv')
#sentiment('dataset_liwcsenti.csv', 'ac_sentiment.csv')

