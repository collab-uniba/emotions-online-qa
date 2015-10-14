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
		print row_1['PostId']
	return 'Done'




def merge2(file_name_input, file_name_metric, output_file):

        f1=open(file_name_input, 'r')
        f2=open(file_name_metric, 'r')
        dict_reader_1 = csv.DictReader(f1, delimiter=';')
        dict_reader_2 = csv.DictReader(f2, delimiter=';')

        head = dict_reader_1.fieldnames
        head_2 = dict_reader_2.fieldnames
        for h in head_2:
                if h != 'PostId':
                        head.append(h)
        f2.close()
        dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=head)
        dict_writer.writerow(dict((fn,fn) for fn in head))
        c=0
        for row_1 in dict_reader_1:
                f2= open(file_name_metric, 'r')
                dict_reader_2 = csv.DictReader(f2, delimiter=';')
                for row_2 in dict_reader_2:
                        if row_2['PostId'] == row_1['PostId']:
                                for h in head_2:
                                        if h != 'PostId':
                                                row_1[h] = row_2[h]
                                c+=1
                                dict_writer.writerow(row_1)
                                f2.close()
                                break
        print 'Post processed: ', c
        return 'Done'




def intersection(file_name, input_file, output_file): #input_file contiene  gli id delle domande da non tenere
        dict_reader1 = csv.DictReader(open(file_name, 'r'), delimiter = ';')
        dict_reader2 = csv.DictReader(open(input_file, 'r'), delimiter = ';')
        head = dict_reader1.fieldnames

        dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=head)
        dict_writer.writerow(dict((fn,fn) for fn in head)) #Scrive gli header
        count = 0
        a = []
        ida =0
        #getQuest30="SELECT PostId FROM only30"
        #result_set = execute_param_query(db, getQuest30)
        app = []
        for tup in dict_reader2:
                 ida= int(tup['PostId'])
                 app.append(ida)
                 #print 'inseriti in app', ida
        for row in dict_reader1:
                if int(row['PostId']) not in app:
                    dict_writer.writerow(row)
                    count += 1

        print 'Post scritti: ', count
        return 'Done'



