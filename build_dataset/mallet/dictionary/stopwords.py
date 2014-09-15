import re, csv, string
from django.utils.encoding import smart_str

def del_punctuation(text):
	return text.translate(string.maketrans ("" , ""), string.punctuation)

def create_dictionary(file_name, output):
	print "Processing..."
	dict_reader = csv.DictReader(open(file_name, 'r'))

	dictionary = {}
	n_word = 0

	for row in dict_reader:
		body = row['Body']
		title = row['Title']
		
		try:
			body_cleaned = del_punctuation(smart_str(body))
			title_cleaned = del_punctuation(smart_str(title))
			
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

	w = csv.writer(open(output, "w"))
	for elem in sorted_dict:
		w.writerow([elem,dictionary[elem]])

	print "Done..."

	return sorted_dict


def create_stopwords_file(file_name, output, threshold):
	reader = csv.reader(open(file_name, 'r'))
	writer = open(output, 'w')

	for row in reader:
		if float(row[1]) > threshold:
			writer.write(row[0]+'\n')



#create_dictionary('academia_questions.csv', 'dict.csv')
create_stopwords_file('dict.csv', 'sw.txt', 0.000099994)
