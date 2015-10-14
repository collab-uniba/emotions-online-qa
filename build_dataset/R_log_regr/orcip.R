# Funzione che preso in input un modello di regressione logistica, 
# di tipo glm, calcola per ogni variabile dipendente:
#	- l'esponente del coefficente
#	- l'esponente dell'intervallo di confidenza
#
# parametri:
#	logit_model: modello di regressione logistica di tipo glm


orcipwald.glm <- function(logit_model){


	library(aod)

	orci <- exp(cbind(OR = coef(logit_model), confint(logit_model)))
	pwald <- NA
	chiwald <- NA
	fileConn<-file("output_noal_stackoverflow.txt")
	write.table(orci, fileConn, sep=";", row.names=TRUE, col.names=TRUE)
	
	return(orci)
}

