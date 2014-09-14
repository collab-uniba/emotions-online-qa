import csv, re
from HTMLParser import HTMLParser
import string
import jpype
import os
from django.utils.encoding import smart_str

LIWC = {}
classes = []

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
	f = del_code(html)
	return del_tags(f)

def del_punctuation(text):
	return text.translate(string.maketrans ("" , ""), string.punctuation)

def load_classes():
	f = open('LIWC.all.txt', 'r')
	reader = csv.reader(f)

	d = {}

	for row in reader:
		word = row[0]
		aff_class = row[1]
		if aff_class not in classes:
			classes.append(aff_class)


	

def load_liwc():
	f = open('LIWC.all.txt', 'r')
	reader = csv.reader(f)

	for row in reader:
		word = row[0]
		aff_class = row[1]

		if "* " in row[0]:
			#stem
			key = word.replace("* ", "")
			if LIWC.has_key(key):
				LIWC.setdefault(key, []).append(aff_class)
			else:
				LIWC.setdefault(key, []).append(True)
				LIWC.setdefault(key, []).append(aff_class)
		else:
			key = word.replace(" ", "")
			if LIWC.has_key(key):
				LIWC.setdefault(key, []).append(aff_class)
			else:
				LIWC.setdefault(key, []).append(False)
				LIWC.setdefault(key, []).append(aff_class)

def get_aff_classes_word(word):
	aff_classes = []
	if LIWC.has_key(word):
		aff_classes = LIWC[word]
	#print word, " > ", aff_classes
	return aff_classes

def get_aff_classes_corpus(corpus):
	
	
	S = jpype.JClass("Snowball")
	stemmer = S()
	#print a.sayHi()
	
	
	freq = {}
	for c in classes:
		freq[c] = 0
	#print freq

	#corpus_cleaned = del_punctuation(clean_body(corpus))
	#corpus_cleaned = corpus.decode('unicode_escape').encode('ascii','ignore')

	words = re.findall(r"[\w']+", corpus)
		
	n_word = len(words)
	#print "Number of words ",n_word
	for word in words:
		word = word.lower()
		if LIWC.has_key(word):
			list_classes = get_aff_classes_word(word)
			#if list_classes[0] == False:
			#print list_classes
			for l in list_classes:
				if freq.has_key(l):
					freq[l] += 1
				
		else:
			#stemming
			stem = stemmer.extract_stem(word)
			#print stem
			if LIWC.has_key(stem):
				list_classes = get_aff_classes_word(stem)
				#print stem, list_classes[0]
				#if list_classes[0] == True:
				#print list_classes
				for l in list_classes:
					if freq.has_key(l):
						freq[l] += 1
					
	
	#print " "
	#for key in freq.keys():
	#	print key," > ",freq[key]
	#print " "
	
	for key in freq.keys():
		freq[key] = float(freq[key])/float(n_word)
	#for key in freq.keys():
	#	print key," > ",freq[key]
	return freq

def get_aff_classes_corpus_freq(corpus):
	
	S = jpype.JClass("Snowball")
	stemmer = S()
	#print a.sayHi()
	
	freq = {}
	for c in classes:
		freq[c] = 0
	#print freq

	#corpus_cleaned = del_punctuation(clean_body(corpus))
	#corpus_cleaned = corpus.decode('unicode_escape').encode('ascii','ignore')

	words = re.findall(r"[\w']+", corpus)
		
	n_word = len(words)
	#print "Number of words ",n_word
	for word in words:
		word = word.lower()
		if LIWC.has_key(word):
			list_classes = get_aff_classes_word(word)
			
			for l in list_classes:
				if freq.has_key(l):
					freq[l] += 1
				
		else:
			#stemming
			stem = stemmer.extract_stem(word)
			print stem
			if LIWC.has_key(stem):
				list_classes = get_aff_classes_word(stem)
				
				for l in list_classes:
					if freq.has_key(l):
						freq[l] += 1
		
	return {'freq':freq, 'n_words':n_word}

def affective_classes(file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';')
	
	head = dict_reader.fieldnames
	f = ['PostId']
	#head.append('Corpus')
	for c in classes:
		f.append(c)

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
		try:
			#body_cleaned = clean_body(body)
			#corpus = title + " " + body_cleaned
		
			#corpus = title + " " + body
		
			try:
				corpus = corpus.decode('unicode_escape').encode('ascii','ignore')
			except UnicodeDecodeError:
				#print r['PostId']
				try:
					corpus = unicode(corpus).encode('ascii', 'ignore')
				except Exception:
					corpus = unicode(corpus, errors='ignore')#smart_str(corpus)

			classes_res = get_aff_classes_corpus(corpus)
				#print classes_res
			for key in classes_res.keys():
				r[key] = classes_res[key]
			count += 1
		except Exception:
			#print r['PostId']
			dict_writer.writerow(r)
			skipped += 1
			continue
		dict_writer.writerow(r)

	jpype.shutdownJVM()

	print "Initial posts ", total
	print "Post processed ", count
	print "Skipped: ", skipped
	return 'Done'

def write_classes():
	out_classes = open('LIWC_classes.txt','w')
	for c in classes:
		out_classes.write(c+'\n')
	out_classes.close()
			
def corpus_plus_acc(file_corpus, file_acc, output_file):
	dict_reader_1 = csv.DictReader(open(file_corpus, 'r'), delimiter=';') # DELIMITER
	dict_reader_2 = csv.DictReader(open(file_acc, 'r'), delimiter=',') # DELIMITER
	
	head = dict_reader_1.fieldnames
	head.append('Accepted')

	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=head) # DELIMITER
	dict_writer.writerow(dict((fn,fn) for fn in head)) #Scrive gli header
	
	for row_1 in dict_reader_1:
		for row_2 in dict_reader_2:
			if row_2['PostId'] == row_1['PostId']:
				print row_2['Accepted']
				row_1['Accepted'] = row_2['Accepted']
				break		
		
		dict_writer.writerow(row_1)

	return 'Done'

def coverage_dominance(file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';')
	
	f = ['Metric']
	for c in classes:
		f.append(c)

	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=f)
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header

	total = 0
	count = 0
	skipped = 0
	
	acc_words = 0 # Total words of posts with an accepted answer
	notacc_words = 0 # Total words of posts without an accepted answer

	coverage_acc = {}
	for c in classes:
		coverage_acc[c] = 0

	coverage_notacc = {}
	for c in classes:
		coverage_notacc[c] = 0
	
	dominance_acc = {}
	for c in classes:
		dominance_acc[c] = 0


	for row in dict_reader:
		total += 1
		
		corpus = row['Corpus']
		
		try:
		
			try:
				corpus = corpus.decode('unicode_escape').encode('ascii','ignore')
				freq_words = get_aff_classes_corpus_freq(corpus)
			except UnicodeDecodeError, e:
				try:
					corpus = unicode(corpus).encode('ascii', 'ignore')
					freq_words = get_aff_classes_corpus_freq(corpus)
				except Exception, e:
					corpus = unicode(corpus, errors='ignore')#smart_str(corpus)
					freq_words = get_aff_classes_corpus_freq(corpus)

			
			if "yes" in row['Accepted']:
				acc_words += freq_words['n_words']
				classes_res = freq_words['freq']
				for key in classes_res.keys():
					coverage_acc[key] += classes_res[key]
			else:
				notacc_words += freq_words['n_words']
				classes_res = freq_words['freq']
				for key in classes_res.keys():
					coverage_notacc[key] += classes_res[key]
			
			count += 1
		except Exception, e:
			skipped += 1
			print 'Exception: ', e.message
			continue

	
	print "Coverage for accepted: "
	print "Frequency: ", coverage_acc
	print "Number of words: ", acc_words, "\n"

	print "Coverage for not accepted: "
	print "Frequency: ", coverage_notacc
	print "Number of words: ", notacc_words, "\n"

	for key in coverage_acc.keys():
		coverage_acc[key] = float(coverage_acc[key])/float(acc_words)

	for key in coverage_notacc.keys():
		coverage_notacc[key] = float(coverage_notacc[key])/float(notacc_words)

	for key in dominance_acc.keys():
		dominance_acc[key] = float(coverage_acc[key])/float(coverage_notacc[key])

	print "Coverage for accepted: "
	print "Frequency: ", coverage_acc
	print "Number of words: ", acc_words, "\n"

	print "Coverage for not accepted: "
	print "Frequency: ", coverage_notacc
	print "Number of words: ", notacc_words, "\n"

	print "Dominance: ", dominance_acc, "\n"

	coverage_acc['Metric'] = "Coverage Accepted"
	coverage_notacc['Metric'] = "Coverage Not Accepted"
	dominance_acc['Metric'] = "Dominance Accepted"

	dict_writer.writerow(coverage_acc)
	dict_writer.writerow(coverage_notacc)
	dict_writer.writerow(dominance_acc)

	jpype.shutdownJVM()

	print "Initial posts ", total
	print "Post processed ", count
	print "Skipped: ", skipped
	return 'Done'

#dict_writer = csv.DictWriter(open(output_file, 'w'), head)

s = 'I couldn\'t stand this tension, it was too much for me. I thought I\'d better go home e rest, I felt terribly stressed out'

load_liwc()
load_classes()

#print classes
#print "Number of affective classes: ", len(classes)

jpype.startJVM("/usr/lib/jvm/java-7-openjdk-amd64/jre/lib/amd64/server/libjvm.so", "-ea", "-Djava.class.path="+os.path.abspath("."))
#affective_classes('stackoverflow_questions.csv', 'so_liwc.csv')
#affective_classes('academia_questions.csv', 'ac_liwc.csv')
#get_aff_classes_corpus(s)
#jpype.shutdownJVM()
#print LIWC['tension']



#corpus_plus_acc('../build-academia/output/dataset_liwcsenti.csv', '../build-academia/output/academia_fase1.csv', 'academia_input_coverage.csv')
coverage_dominance('academia_input_coverage.csv', 'academia_coverage.csv')
