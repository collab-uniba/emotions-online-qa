import jpype
import csv
import os

def dataset_mallet(input_file, output_file):
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
		tags = row['Tags']
		try:
			#t = tags.replace('<',' ')
			tags_cleaned = tags.replace('<',' ').replace('>',' ')
			corpus = title + " " + body + " " + tags_cleaned
			
			try:
				r['Corpus'] = corpus.decode('unicode_escape').encode('ascii','ignore')
			except UnicodeDecodeError:
				print r['PostId']
				try:
					r['Corpus'] = unicode(corpus).encode('ascii', 'ignore')
				except Exception:
					print "Last Exception handled"
					#r['Corpus'] = smart_str(corpus)
					r['Corpus'] = unicode(corpus,errors='ignore')

			
		except Exception:
			dict_writer.writerow(r)
			continue
		dict_writer.writerow(r)
	print 'Post processed: ', count
	return 'Done'
	
def dataset_mallet_stem(input_file, output_file):
	jpype.startJVM("/usr/lib/jvm/java-7-openjdk-amd64/jre/lib/amd64/server/libjvm.so", "-ea", "-Djava.class.path="+os.path.abspath("."))
	
	Snowball = jpype.JClass("Snowball")
	
	stemmer = Snowball()

	#a = jpype.JString("I couldn\'t stand this tension, it c++ c# was too much for me. I thought I\'d better go home e rest, I felt terribly stressed out")
	#out =  s.extract_stem_corpus(a)
	#print out

	dict_reader = csv.DictReader(open(input_file, 'r'), delimiter=';') # DELIMITER
	
	head = dict_reader.fieldnames
	f = ['PostId', 'Corpus']
	
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=f) # DELIMITER
	dict_writer.writerow(dict((fn,fn) for fn in f)) #Scrive gli header
	
	count = 0
	total = 0
	skipped = 0
	for row in dict_reader:
		r = {}
		r['PostId'] = row['PostId']
		body = row['Body']
		title = row['Title']
		tags = row['Tags']
		try:
			#t = tags.replace('<',' ')
			tags_cleaned = tags.replace('<',' ').replace('>',' ')
			corpus = title + " " + body + " " + tags_cleaned
			
			try:
				corpus = corpus.decode('unicode_escape').encode('ascii','ignore')
				r['Corpus'] = stemmer.extract_stem_corpus(corpus)
				count += 1
			except UnicodeDecodeError:
				try:
					corpus = unicode(corpus).encode('ascii', 'ignore')
					r['Corpus'] = stemmer.extract_stem_corpus(corpus)
					count += 1
				except Exception:
					#r['Corpus'] = smart_str(corpus)
					corpus = unicode(corpus,errors='ignore')
					r['Corpus'] = stemmer.extract_stem_corpus(corpus)
					count += 1

			
		except Exception:
			dict_writer.writerow(r)
			print r['PostId'], ' Skipped'
			skipped += 1
			total += 1
			continue
		dict_writer.writerow(r)
		total += 1
	
	#jpype.shutdownJVM()
	print "Initial posts ", total
	print 'Post processed: ', count
	print 'Post skipped: ', skipped
	return 'Done'

dataset_mallet_stem('../../build-academia/output/academia_questions.csv', 'ac_input_mallet.csv')
