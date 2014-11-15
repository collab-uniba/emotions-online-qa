# Funzione che presi in input due modelli di regressione logistica, 
# di tipo bigglm, calcola il likelihood ratio test come nel codice 
# della funzione lrtest nel package epicalc.
#
# parametri:
#	null_model: modello di regressione logistica di tipo bigglm
#	model: modello di regressione logistica di tipo bigglm

likelihood_ratio.bigglm <- function(null_model, model){

	# Code from epicalc::lrtest
	# also http://nlp.stanford.edu/manning/courses/ling289/logistic.pdf (pag.3)
	#
	# lrt1 <- 2 * (as.numeric(logLik(model2) - logLik(model1)))		#in epicalc::lrtest
	# lrt2 <- as.numeric(abs(deviance(model) - deviance(null_model)))	#in http://nlp.stanford.edu/manning/courses/ling289/logistic.pdf
	# lrt1 == lrt2 -> TRUE

	residual_deviance_diff <- as.numeric((deviance(model) - deviance(null_model)))
	residual_df_diff <- as.numeric((model$df.resid - null_model$df.resid))

	if (residual_deviance_diff < 0) {
		residual_deviance_diff <- -residual_deviance_diff
		residual_df_diff <- -residual_df_diff
        }
        if (residual_deviance_diff * residual_df_diff < 0) {
		cat("Likelihood gets worse with more variables.\n")
        }
	#else {
		p.value <- pchisq(residual_deviance_diff, residual_df_diff, lower.tail=FALSE)
		cat("Chi-squared ", residual_df_diff, "d.f. = ", residual_deviance_diff, "\nP value = ", sprintf("%.5f",p.value), "\n")
		output <- list(model1 = null_model$call, model2 = model$call, 
				model.class = class(null_model), Chisquared = residual_deviance_diff, df = residual_df_diff, 
				p.value = pchisq(residual_deviance_diff, residual_df_diff, lower.tail=FALSE))
		return(output)
		
	#}
}

# For model evaluation (against the null model)
#	model_eval_lr_test <- likelihood_ratio.bigglm(null_model=stackoverflow_logit_null, model=stackoverflow_logit_new)
#
# For statistical test of individual predictor (as P(LR-test) in epicalc::logistic.display)
#	Topic_lr_test <- likelihood_ratio.bigglm(null_model=stackoverflow_logit_new_withoutTopic, model=stackoverflow_logit_new)
