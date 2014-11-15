# Funzione che preso in input un modello di regressione logistica, 
# di tipo bigglm, calcola per ogni variabile dipendente:
#	- l'esponente del coefficente
#	- l'esponente dell'intervallo di confidenza
#	- il Chi2 ed il p-value per il Wald test
#
# parametri:
#	logit_model: modello di regressione logistica di tipo bigglm

orcipwald.bigglm <- function(logit_model){

	library(biglm)
	library(aod)

	orci <- exp(cbind(OR = coef(logit_model), confint(logit_model)))
	pwald <- NA
	chiwald <- NA
	for(i in 1:length(coef(logit_model))){
		curr_test <- (wald.test(b = coef(logit_model), Sigma = vcov(logit_model), Terms = i))$result$chi2
		# curr_test[1] : chi2
		# curr_test[2] : df
		# curr_test[3] : p
		pwald[i] <- curr_test[3]
		chiwald[i] <- curr_test[1]
	}
	orcip <- cbind(orci, "p(Wald)" = pwald, "Wald Chi2" = chiwald)
	#orcip <- cbind(orci, "Wald Chi2" = chiwald)
	
	return(orcip)
}

