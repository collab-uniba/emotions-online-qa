import csv

# Converte un file csv che utilizza come delimitatore il carattere ';'
# in un file csv che utilizza come delimitatore il carattere ','.
#
# parametri:
#	input_file: nome del file csv con delimitatore ';' da cui leggere
#	output_file: nome del file csv con delimitatore ',' su cui scrivere
def to_comma(input_file, output_file):
	dict_reader = csv.DictReader(open(input_file, 'r'), delimiter=';')
	dict_writer = csv.DictWriter(open(output_file, 'w'), delimiter=',', fieldnames=dict_reader.fieldnames)  # DELIMITER
	dict_writer.writerow(dict((fn,fn) for fn in dict_reader.fieldnames)) #Scrive gli header

	for row in dict_reader:
		dict_writer.writerow(row)
