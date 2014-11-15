import csv

# Fonde, in un unico file csv, le colonne di due file csv. I due file vengono fusi sulla
# base di un confronto sul campo 'PostId'.
#
# Esempio: i due file che vogliono fondere hanno, uno i campi PostId e Body e l'altro i
# campi PostId, SentimentNegativeScore e SentimentPositiveScore. Il file risultante 
# conterra' PostId, Body, SentimentNegativeScore e SentimentPositiveScore. Inoltre ogni
# istanza, del primo e del secondo file, saranno allineate sulla base del confronto 
# su PostId. In particolare, due istanze, provenienti dai due file, verranno allineate
# se i due PostId sono uguali.
#
# parametri:
#	file_name_input: nome del file che si vuole fondere, deve contenere almeno il campo:
#				- 'PostId'
#	file_name_metric: nome del file che si vuole fondere, deve contenere almeno il campo:
#				- 'PostId'
#	output_file: nome del file su cui scrivere, conterra' i campi:
#				- 'PostId'
#				- tutti i campi di file_name_input
#				- tutti i campi di file_name_metric
def substitute(file_name_input, file_name_metric, delim=';', output_file, subst_fields=[]):
	dict_reader_1 = csv.DictReader(open(file_name_input, 'r'), delimiter=';') # DELIMITER
	dict_reader_2 = csv.DictReader(open(file_name_metric, 'r'), delimiter=delim) # DELIMITER
	
	head = dict_reader_1.fieldnames
	if subst_fields == []:
		head_2 = dict_reader_2.fieldnames
		for h in head_2:
			subst_fields.append(h)
	#for h in head_2:
	#	if h != 'PostId':
	#		head.append(h)

	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=head) # DELIMITER
	dict_writer.writerow(dict((fn,fn) for fn in head)) #Scrive gli header
	
	for row_1 in dict_reader_1:
		for row_2 in dict_reader_2:
			if row_2['PostId'] == row_1['PostId']:
				for h in subst_fields:
					row_1[h] = row_2[h]
				break		
		
		dict_writer.writerow(row_1)

	return 'Done'
