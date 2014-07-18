import csv, re
from HTMLParser import HTMLParser
import string
import jpype
import os

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
	return re.sub('\<code>(.*?)\</code>', '', html)

def clean_body(html):
	return del_tags(del_code(html))

def del_punctuation(text):
	return text.translate(string.maketrans ("" , ""), string.punctuation)

def load_classes():
	f = open('LIWC[1].all.txt', 'r')
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
	return aff_classes

def get_aff_classes_corpus(corpus):
	
	
	S = jpype.JClass("Snowball")
	stemmer = S()
	#print a.sayHi()
	
	
	freq = {}
	for c in classes:
		freq[c] = 0
	#print freq

	corpus_cleaned = del_punctuation(clean_body(corpus))

	words = re.findall(r"[\w']+", corpus_cleaned)
		
	n_word = len(words)

	for word in words:
		word = word.lower()
		if LIWC.has_key(word):
			list_classes = get_aff_classes_word(word)
			if list_classes[0] == False:
				first = True
				for l in list_classes:
					if first == False:
						freq[l] += 1
					else:
						first = False
		else:
			#stemming
			stem = stemmer.extract_stem(word)
			#print stem
			if LIWC.has_key(stem):
				list_classes = get_aff_classes_word(stem)
				if list_classes[0] == True:
					first = True
					for l in list_classes:
						if first == False:
							freq[l] += 1
						else:
							first = False

	for key in freq.keys():
		freq[key] = float(freq[key])/float(n_word)
	
	return freq

def affective_classes(file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'))
	
	head = dict_reader.fieldnames
	head.append('Corpus')
	for c in classes:
		head.append(c)

	dict_writer = csv.DictWriter(open(output_file, 'w'), head)
	dict_writer.writerow(dict((fn,fn) for fn in head)) #Scrive gli header

	for row in dict_reader:
		body = row['Body']
		title = row['Title']
		try:
			body_cleaned = clean_body(body)
			corpus = title + " " + body_cleaned
			
			row['Corpus'] = corpus

			classes_res = get_aff_classes_corpus(corpus)
				#print classes_res
			for key in classes_res.keys():
				row[key] = classes_res[key]
		except Exception:
			continue
		dict_writer.writerow(row)

	return 'Done'
			
	
#dict_writer = csv.DictWriter(open(output_file, 'w'), head)

load_liwc()
load_classes()
#print classes
print "Number of affective classes: ", len(classes)
#print get_aff_classes_corpus(body1)
#jpype.startJVM("/usr/lib/jvm/java-7-openjdk-amd64/jre/lib/amd64/server/libjvm.so", "-ea", "-Djava.class.path="+os.path.abspath("."))
#affective_classes('ac_input.csv', 'ac_aff.csv')
#jpype.shutdownJVM()
