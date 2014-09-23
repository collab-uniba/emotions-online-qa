import csv

# Calcola la media del sentiment score (positivo e negativo) per ogni topic
# SPECIFICA PER IL RAGGRUPPAMENTO PER TOPIC
def mean_sentiscore_per_topic(file_name, output_file):
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';')
	
	topic_posscore_mean = {} # Media positive sentiment score per ogni topic
	topic_negscore_mean = {} # Media negative sentiment score per ogni topic
	topic_numb = {} # Conta il numero di post per ogni topic (utilizzato per calcolare la media)
	
	for row in dict_reader:
		topic = row['Topic']
		
		if topic_numb.has_key(topic):
			topic_numb[topic] += 1
			topic_posscore_mean[topic] += int(row['SentimentPositiveScore'])
			topic_negscore_mean[topic] += int(row['SentimentNegativeScore'])
		else:
			topic_numb[topic] = 1
			topic_posscore_mean[topic] = int(row['SentimentPositiveScore'])
			topic_negscore_mean[topic] = int(row['SentimentNegativeScore'])

	out = open(output_file, 'w')
	for topic in sorted(topic_numb, key=int):
		topic_posscore_mean[topic] = float(topic_posscore_mean[topic]) / float(topic_numb[topic])
		topic_negscore_mean[topic] = float(topic_negscore_mean[topic]) / float(topic_numb[topic])
		
		out.write("Topic -> " + topic)
		out.write("\nNumber of posts -> " + str(topic_numb[topic]))
		out.write("\n\tMean sentiment positive score -> " + str(topic_posscore_mean[topic]))
		out.write("\n\tMean sentiment negative score -> " + str(topic_negscore_mean[topic]))
		out.write("\n\n")
		
		print "Topic -> " + topic
		print "\n\tMean sentiment positive score -> ", "|" * int(topic_posscore_mean[topic] / 0.1)
		print "\n\tMean sentiment negative score -> ", "|" * int((topic_negscore_mean[topic] / 0.1) * -1)
		print "\n"

# Calcola la media del sentiment score (positivo e negativo) per ogni valore del campo group_by 
# es. group_by = "Topic"
def mean_sentiscore(file_name, output_file, group_by):
	dict_reader = csv.DictReader(open(file_name, 'r'), delimiter=';')
	
	topic_posscore_mean = {} # Media positive sentiment score per ogni topic
	topic_negscore_mean = {} # Media negative sentiment score per ogni topic
	topic_numb = {} # Conta il numero di post per ogni topic (utilizzato per calcolare la media)
	
	for row in dict_reader:
		group_val = row[group_by]
		
		if topic_numb.has_key(group_val):
			topic_numb[group_val] += 1
			topic_posscore_mean[group_val] += int(row['SentimentPositiveScore'])
			topic_negscore_mean[group_val] += int(row['SentimentNegativeScore'])
		else:
			topic_numb[group_val] = 1
			topic_posscore_mean[group_val] = int(row['SentimentPositiveScore'])
			topic_negscore_mean[group_val] = int(row['SentimentNegativeScore'])

	out = open(output_file, 'w')
	for group_val in sorted(topic_numb):
		topic_posscore_mean[group_val] = float(topic_posscore_mean[group_val]) / float(topic_numb[group_val])
		topic_negscore_mean[group_val] = float(topic_negscore_mean[group_val]) / float(topic_numb[group_val])
		
		out.write(group_by + " -> " + group_val)
		out.write("\nNumber of posts -> " + str(topic_numb[group_val]))
		out.write("\n\tMean sentiment positive score -> " + str(topic_posscore_mean[group_val]))
		out.write("\n\tMean sentiment negative score -> " + str(topic_negscore_mean[group_val]))
		out.write("\n\n")
		
		print group_by, " -> " + group_val
		print "\n\tMean sentiment positive score -> ", "|" * int(topic_posscore_mean[group_val] / 0.1)
		print "\n\tMean sentiment negative score -> ", "|" * int((topic_negscore_mean[group_val] / 0.1) * -1)
		print "\n"
