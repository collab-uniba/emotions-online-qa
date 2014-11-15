# Preso il dataset calcola la percentuale di successo per ogni topic.
# La percentuale di successo per un determinato topic viene calcolata
# come il numero di post, che appartengono a quel topic, che ricadono 
# nella classe Successful TRUE diviso il numero totale di post che
# appartengono al topic considerato.
# Le percentuali di successo calcolate per ongi topic vengono scritte
# nel file output_file.
#
# parametri:
#	dataset: data frame con le metriche
#	output_file: nome del file sul quale scrivere le percentuali di successo
#		per ogni topic

sr.topic <- function(dataset, output_file='sr_topic.txt'){

	topics <- unique(dataset$Topic) # get distinct value of topic

	cat('Topic', '\t', 'Success Rate', '\n', file=output_file)
	
	for(curr_topic in topics){
		curr_sr <- (length(dataset$Topic[dataset$Topic == curr_topic & dataset$Successful == 'TRUE']) / length(dataset$Topic[dataset$Topic == curr_topic])) * 100
		
		cat(curr_topic, '\t\t', curr_sr, ' %', '\n', file=output_file, append=TRUE)
	}
}

