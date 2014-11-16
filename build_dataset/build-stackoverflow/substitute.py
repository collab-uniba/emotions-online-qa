import csv

# Sostituisce i campi di un file csv ad i campi di un altro file csv e scrive tutto su
# un nuovo file csv. I due file vengono fusi sulla base di un confronto sul campo 'PostId'.
#
# parametri:
#	file_name_input: nome del file a cui si vogliono sostituire i campi, deve contenere almeno il campo:
#				- 'PostId'
#	file_name_metric: nome del file da cui prendere i campi da sostituire, deve contenere almeno il campo:
#				- 'PostId'
#	output_file: nome del file su cui scrivere, conterra' i campi:
#				- 'PostId'
#				- tutti i campi di file_name_input aggiornati
#	delim: delimitatore da utilizzare per aprire file_name_metric
#	subst_fields: vettore che contiene i nomi dei campi che si vogliono sostituire, tali campi devono
#		essere presenti sia in file_name_input sia in file_name_metric; se tale vettore e' vuoto
#		vengono considerati tutti i campi di file_name_metric
def substitute(file_name_input, file_name_metric, output_file, delim=';', subst_fields=[]):
	dict_reader_1 = csv.DictReader(open(file_name_input, 'r'), delimiter=';') # DELIMITER
	dict_reader_2 = csv.DictReader(open(file_name_metric, 'r'), delimiter=delim) # DELIMITER
	
	head = dict_reader_1.fieldnames
	if subst_fields == []:
		head_2 = dict_reader_2.fieldnames
		for h in head_2:
			if h != 'PostId':
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
