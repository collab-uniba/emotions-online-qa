# Reference http://www.ats.ucla.edu/stat/r/dae/logit.htm
# Script per calcolare la probabilità di successo stimata 
# sulla base del modello definito in data.frame()
library(ggplot2)

	plot.CodeSnippet_prob_pertopic <- function(dataset, logit_model){
	SentimentNegativeScore <- fixall_varyCodeSnippettopic(dataset, logit_model)
	ggplot(SentimentNegativeScore, aes(x = SentimentNegativeScore, y = PredictedProb))

}


fixall_varyCodeSnippettopic <- function(dataset, logit_model){
	
	newdata2 <- with(dataset, 
	data.frame(SentimentNegativeScore = 	4,#median(SentimentNegativeScore),#rep(seq(from = 0, to = 4, length.out = 5), length(topics)), 
		SentimentPositiveScore = 	3,#median(SentimentPositiveScore),
		CodeSnippet = 			FALSE,#factor(rep(c(FALSE,TRUE), each = 1)),
		GMTHour = 			'Afternoon',#factor('Morning', levels=c('Morning', 'Afetrnoon', 'Evening', 'Nigth')),
		Weekday = 			'Weekday',#factor('Weekday', levels=c('Weekday', 'Weekend')),
		BodyLength = 			254,#median(BodyLength),
		IsTheSameTopicBTitle =		FALSE,	
		Gratitude = 			TRUE,
		TitleLength = 			3,#median(TitleLength),
#		NumberOfUsersComments = 	median(NumberOfUsersComments),
#		CommentSentimentPositiveScore = median(CommentSentimentPositiveScore),
#		CommentSentimentNegativeScore = median(CommentSentimentNegativeScore),
		URL = 				3,#median(URL),
		NImg = 				0,#median(NImg),
		NTag = 				3,#median(NTag),
		AvgUpperCharsPPost =		0.03498542274052478,#median(AvgUpperCharsPPost),
		Successful = FALSE
			)
		)

	newdata3 <- data.frame(newdata2, PredictedProb=predict(logit_model, newdata = newdata2, type = "response"))
	
	capture.output(summary(newdata3), file="probabilita_di_successo.txt")	
	return(newdata3)
}

