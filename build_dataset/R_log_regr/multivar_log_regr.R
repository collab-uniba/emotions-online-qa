library(biglm)

stackoverflow_dataset <- read.csv('stackoverflow_t10_final.csv',sep=';')

stackoverflow_dataset$CodeSnippet <- sapply(as.character(stackoverflow_dataset$CodeSnippet),switch,'yes'=as.logical(TRUE),'no'=as.logical(FALSE))
stackoverflow_dataset$Successful <- sapply(as.character(stackoverflow_dataset$Successful),switch,'yes'=as.logical(TRUE),'no'=as.logical(FALSE))
stackoverflow_dataset$Topic <- factor(stackoverflow_dataset$Topic)

stackoverflow_logit <- bigglm(formula=Successful ~ CodeSnippet + GMTHour + Weekday + BodyLength + TitleLength + QuestionScore + AnswerScore + UsersAnswersAccepted + UsersQuestionsAccepted + NumberOfBadges + SentimentPositiveScore + SentimentNegativeScore + Topic + AFFECT + POSEMO + POSFEEL + OPTIM + NEGEMO + ANX + ANGER + SAD + COGMECH + INSIGHT + DISCREP + INHIB + TENTAT + CERTAIN + FEEL + SOCIAL + COMM, data=stackoverflow_dataset, family=binomial())

capture.output(summary(stackoverflow_logit), file="R_logit_regr/stackoverflow_multivar_logit_regr.txt")
