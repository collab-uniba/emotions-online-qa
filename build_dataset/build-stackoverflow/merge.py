import csv

def merge(file_name_input, file_name_metric, output_file):
	dict_reader_1 = csv.DictReader(open(file_name_input, 'r'), delimiter=';') # DELIMITER
	dict_reader_2 = csv.DictReader(open(file_name_metric, 'r'), delimiter=';') # DELIMITER
	
	head = dict_reader_1.fieldnames
	head_2 = dict_reader_2.fieldnames
	for h in head_2:
		if h != 'PostId':
			head.append(h)

	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=head) # DELIMITER
	dict_writer.writerow(dict((fn,fn) for fn in head)) #Scrive gli header
	
	for row_1 in dict_reader_1:
		for row_2 in dict_reader_2:
			if row_2['PostId'] == row_1['PostId']:
				for h in head_2:
					if h != 'PostId':
						row_1[h] = row_2[h]
				break		
		
		dict_writer.writerow(row_1)

	return 'Done'

#merge('academia_questions.csv', 'ac_questions_acc.csv', 'temp/academia_merge_1.csv')
#merge('temp/academia_merge_1.csv', 'ac_questions_answacc.csv', 'temp/academia_merge_2.csv')
#merge('temp/academia_merge_2.csv', 'ac_questions_questacc.csv', 'temp/academia_merge_3.csv')
#merge('temp/academia_merge_3.csv', 'ac_questions_answscore.csv', 'temp/academia_merge_4.csv')
#merge('temp/academia_merge_4.csv', 'ac_questions_questscore.csv', 'temp/academia_merge_5.csv')
#merge('temp/academia_merge_5.csv', 'ac_questions_badg.csv', 'temp/academia_merge_6.csv')
#merge('temp/academia_merge_6.csv', 'ac_questions_week.csv', 'temp/academia_merge_7.csv')
#merge('temp/academia_merge_7.csv', 'ac_questions_len.csv', 'temp/academia_merge_8.csv')
#merge('temp/academia_merge_8.csv', 'ac_sentiment.csv', 'temp/academia_merge_9.csv')
#merge('temp/academia_merge_9.csv', 'ac_liwc.csv', 'academia_final.csv')


