import csv, re
from HTMLParser import HTMLParser
import string
import jpype
import os

LIWC = {}
classes = []

body1 = "The worldwide diffusion of social media has profoundly changed the way we communicate and access information. Increasingly, people try to solve domain-specific problems through interaction on social online Question and Answer (Q&A) sites. The enormous success of Stack Overflow, a community of 2.9 million programmers asking and providing answers about code development, attests this increasing trend. One of the biggest drawbacks of communication through social media is to appropriately convey sentiment through text. While display rules for emotions exist and are widely accepted for traditional face-to-face interaction, people might not be prepared for effectively dealing with the barriers of social media to non-verbal communication. Though, emotions matter, especially in the context of online Q&A communities where social reputation is a key factor for successful knowledge sharing. As a consequence, the design of systems and mechanisms for fostering emotional awareness in computer-mediated communication is becoming an important technical and social challenge for research in computer-supported collaborative work and social computing."

# JVM utilities
def start_JVM(path_libjvm='/usr/lib/jvm/java-7-openjdk-amd64/jre/lib/amd64/server/libjvm.so'):
	jpype.startJVM(path_libjvm, "-ea", "-Djava.class.path="+os.path.abspath("."))

def stop_JVM():
	jpype.shutdownJVM()
###############

# Carica il vettore globale classes con le classi LIWC.
# Il vettore sara':
#	classes = ['POSEMO', 'NEGEMO', 'TENTAT', ...]
def load_classes():
	f = open('LIWC.all.txt', 'r')
	reader = csv.reader(f)

	d = {}

	for row in reader:
		word = row[0]
		aff_class = row[1]
		if aff_class not in classes:
			classes.append(aff_class)

# Carica il dizionario globale LIWC dove le chiavi sono le parole
# ed i valori, corrispondenti alle chiavi, sono dei vettori che hanno: 
#	- alla prima posizione un valore booleano che indica se la parola 
#		corrispondente e' una radice (True) o e' una parola completa (False)
#	- nelle restanti posizioni le classi LIWC in cui ricade la parola (chiave
#		del dizionario)
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

# Calcola le classi LIWC in cui ricade una certa parola.
#
# parametri:
#	word: parola di cui si vogliono conoscere le classi LIWC in cui ricade
#
# output:
#	restituisce un vettore che alla prima posizione ha un valore boolenao 
#	che indica se la parola e' una radice (True) o se e' una parola completa
#	(False) e nelle restanti posizioni le classi LIWC in cui ricade la parola
def get_aff_classes_word(word):
	aff_classes = []
	if LIWC.has_key(word):
		aff_classes = LIWC[word]
	#print word, " > ", aff_classes
	return aff_classes

# Calcola le frequenze delle classi LIWC dato un testo in input.
# Le frequenze sono calcolate come il numero di volte che le parole del testo
# ricadono all'interno di una classe LIWC diviso il numero di parole del testo.
# Una parola viene cercata all'interno del dizionario LIWC secondo il seguente
# criterio:
#	- se la parola e' contenuta nel dizionario calcola le frequenze
#	- altrimenti fai lo stemming della parola e calcola le frequenze
#
# parametri:
#	corpus: testo da analizzare
#
# output:
#	dizionario dove le chiavi sono le classi LIWC e i valori sono le frequenze.
def get_aff_classes_corpus(corpus):
	
	S = jpype.JClass("Snowball")
	stemmer = S()
	
	freq = {}
	for c in classes:
		freq[c] = 0
	
	words = re.findall(r"[\w']+", corpus)
		
	n_word = len(words)
	#print "Number of words ",n_word
	for word in words:
		word = word.lower()
		if LIWC.has_key(word): #cerca parola completa...
			list_classes = get_aff_classes_word(word)
			
			for l in list_classes:
				if freq.has_key(l):
					freq[l] += 1
				
		else: # ...altrimenti fai lo stemming
			stem = stemmer.extract_stem(word)
			
			if LIWC.has_key(stem):
				list_classes = get_aff_classes_word(stem)
				
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

# Calcola il numero di volte che le parole del testo ricadono all'interno di una classe LIWC.
# Una parola viene cercata all'interno del dizionario LIWC secondo il seguente
# criterio:
#	- se la parola e' contenuta nel dizionario calcola le frequenze
#	- altrimenti fai lo stemming della parola e calcola le frequenze
#
# parametri:
#	corpus: testo da analizzare
#
# output:
#	dizionario con due chiavi:
#		- 'freq', il valore contiene un dizionario dove le chiavi sono le classi LIWC e i valori 
#			il numero di volte che le parole ricadono nella classe corrispondente
#		- 'n_words', il valore contiene il numero di parole nel parametro corpus
def get_aff_classes_corpus_count(corpus):
	
	S = jpype.JClass("Snowball")
	stemmer = S()
	
	freq = {}
	for c in classes:
		freq[c] = 0
	
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

# Calcola il numero di volte che le parole di un insieme di testi ricadono
# nella classi LIWC:
#	- POSEMO
#	- NEGEMO
#	- TENTAT
#
# parametri:
#	file_name: nome del file csv da cui leggere i testi da analizzare, deve
#		contenere almeno il campo 
#			- 'PostId'
#	output_file: nome del file su cui scrivere i risultati, conterra':
#			- 'PostId'
#			- 'POSEMO' che contiene il numero di volte che le parole ricadono
#				nella classe LIWC POSEMO, calcolato come nella funzione get_aff_classes_corpus_count
#			- 'NEGEMO' che contiene il numero di volte che le parole ricadono
#				nella classe LIWC NEGEMO, calcolato come nella funzione get_aff_classes_corpus_count
#			- 'TENTAT' che contiene il numero di volte che le parole ricadono
#				nella classe LIWC TENTAT, calcolato come nella funzione get_aff_classes_corpus_count
#	text_field: nome del campo che contiene il testo che si vuole analizzare
def affective_classes_POSEMO_NEGEMO_TENTAT_count(file_name, output_file, text_field='Corpus'):
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';')
	
	head = dict_reader.fieldnames
	f = ['PostId', 'POSEMO', 'NEGEMO', 'TENTAT']
	classes_list = ['POSEMO', 'NEGEMO', 'TENTAT']
	#for c in classes:
	#	f.append(c)

	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=f)
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header

	total = 0
	count = 0
	skipped = 0
	for row in dict_reader:
		total += 1
		
		corpus = row[text_field]
		r = {}
		r['PostId'] = row['PostId']
		try:
		
			try:
				corpus = corpus.decode('unicode_escape').encode('ascii','ignore')
			except UnicodeDecodeError:
				try:
					corpus = unicode(corpus).encode('ascii', 'ignore')
				except Exception:
					corpus = unicode(corpus, errors='ignore')

			freq_words = get_aff_classes_corpus_count(corpus)
			classes_res = freq_words['freq']
				
			for key in classes_res.keys():
				if key in classes_list:
					r[key] = classes_res[key]

			count += 1
		except Exception:
			#print r['PostId']
			r['POSEMO'] = str(0)
			r['NEGEMO'] = str(0)
			r['TENTAT'] = str(0)
			dict_writer.writerow(r)
			skipped += 1
			continue
		dict_writer.writerow(r)

	#stop_JVM()

	print "Initial posts ", total
	print "Post processed ", count
	print "Skipped: ", skipped
	return 'Done'

# Calcola le frequenze delle classi LIWC di un insieme di testi.
#
# parametri:
#	file_name: nome del file csv da cui leggere i testi da analizzare, deve
#		contenere almeno il campo 
#			- 'PostId'
#	output_file: nome del file su cui scrivere i risultati, conterra':
#			- 'PostId'
#			- un campo per ogni classe LIWC con le frequenze come calcolate 
#				nella funzione get_aff_classes_corpus
#	text_field: nome del campo che contiene il testo che si vuole analizzare
def affective_classes(file_name, output_file, text_field='Corpus'):
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
		corpus = row[text_field]
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
			for c in classes:
				r[c] = str(0)
			dict_writer.writerow(r)
			skipped += 1
			continue
		dict_writer.writerow(r)

	#stop_JVM()

	print "Initial posts ", total
	print "Post processed ", count
	print "Skipped: ", skipped
	return 'Done'

# Scrive le classi LIWC in un file di testo con nome 'LIWC_classes.txt'
def write_classes():
	out_classes = open('LIWC_classes.txt','w')
	for c in classes:
		out_classes.write(c+'\n')
	out_classes.close()

# Costruisce, dati due file csv, un file csv che contiene tutti i campi del primo
# ed il campo 'Accepted' del secondo. La fusione viene fatta sulla base del confronto 
# sul campo 'PostId'.
#
# parametri:
#	file_corpus: nome del file csv al quale aggiungere il campo 'Accepted'
#	file_acc: nome del file csv dal quale prendere il campo 'Accepted', deve contenere
#		almeno i campi:
#			- 'PostId'
#			- 'Accepted'
#	output_file: nome del file csv su cui scrivere, conterra' i campi:
#			- tutti i campi dal csv file_corpus
#			- 'Accepted' dal csv file_acc
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

# Calcola coverage per le domande con risposta accettata e senza risposta accettata. E dominance
# per le domande con risposta accettata.
#
# parametri:
#	file_name: nome del file csv che contiene i testi da analizzare, deve
#		contenere almeno i campi:
#			- testo da analizzare
#			- 'Accepted' con valore 'yes' se la domanda ha ricevuto una risposta
#				accettata, 'no' altrimenti
#	output_file: nome del file csv su cui scrivere i risultati
def coverage_dominance(file_name, output_file, text_field='Corpus'):
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
		
		corpus = row[text_field]
		
		try:
		
			try:
				corpus = corpus.decode('unicode_escape').encode('ascii','ignore')
				freq_words = get_aff_classes_corpus_count(corpus)
			except UnicodeDecodeError, e:
				try:
					corpus = unicode(corpus).encode('ascii', 'ignore')
					freq_words = get_aff_classes_corpus_count(corpus)
				except Exception, e:
					corpus = unicode(corpus, errors='ignore')#smart_str(corpus)
					freq_words = get_aff_classes_corpus_count(corpus)

			
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

	#stop_JVM() # Ferma la JVM

	print "Initial posts ", total
	print "Post processed ", count
	print "Skipped: ", skipped
	return 'Done'

#dict_writer = csv.DictWriter(open(output_file, 'w'), head)

s = 'I couldn\'t stand this tension, it was too much for me. I thought I\'d better go home e rest, I felt terribly stressed out'

load_liwc()		# Inizializza il dizionario globale LIWC
load_classes()	# Inizializza il vettore globale classes


# Avvia la JVM nel momento in cui viene importato il file come libreria, si puo' commentare tale riga e avviarla solo quando necessario
start_JVM() 

#affective_classes('stackoverflow_questions.csv', 'so_liwc.csv')
#affective_classes('academia_questions.csv', 'ac_liwc.csv')
#get_aff_classes_corpus(s)
#jpype.shutdownJVM()
#print LIWC['tension']



#corpus_plus_acc('../build-academia/output/dataset_liwcsenti.csv', '../build-academia/output/academia_fase1.csv', 'academia_input_coverage.csv')
#coverage_dominance('academia_input_coverage.csv', 'academia_coverage.csv')
