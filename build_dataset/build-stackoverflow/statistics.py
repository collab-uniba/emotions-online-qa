import csv

# Calcola la media del sentiment score (positivo e negativo) per ogni topic
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
	for topic in sorted(topic_numb):
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
