# Carica il file csv che contiene il dataset.
# Converte i campi CodeSnippet e Successful da 'yes', 'no' a TRUE, FALSE.
# Fattorizza il campo Topic (altrimenti R lo prende come numerico).
# Avvia la regressione logistica.

library(biglm)

stackoverflow_dataset <- read.csv('../mallet/build_input_mallet/t_15/stackoverflow_final.csv',sep=';')

stackoverflow_dataset$CodeSnippet <- sapply(as.character(stackoverflow_dataset$CodeSnippet),switch,'yes'=as.logical(TRUE),'no'=as.logical(FALSE))
stackoverflow_dataset$Successful <- sapply(as.character(stackoverflow_dataset$Successful),switch,'yes'=as.logical(TRUE),'no'=as.logical(FALSE))
stackoverflow_dataset$Topic <- factor(stackoverflow_dataset$Topic)

stackoverflow_logit_new.woLIWC <- bigglm(formula=Successful ~ CodeSnippet +   
                                I(Weekday=='Weekend') +
                               I(GMTHour=='Afternoon') + I(GMTHour=='Evening') + I(GMTHour=='Night') +
                               BodyLength + TitleLength + QuestionScore + AnswerScore + UsersAnswersAccepted +
                               UsersQuestionsAccepted + NumberOfBadges + SentimentPositiveScore + SentimentNegativeScore +
                               NumberOfUsersComments + CommentSentimentPositiveScore + CommentSentimentNegativeScore +
                               I(Topic=='0') + I(Topic=='1') + I(Topic=='2') + I(Topic=='3') + I(Topic=='5') + I(Topic=='6') +
                               I(Topic=='7') + I(Topic=='8') + I(Topic=='9') + I(Topic=='10') + I(Topic=='11') + I(Topic=='12') +
                               I(Topic=='13') + I(Topic=='14'),
                               data=stackoverflow_dataset, family=binomial())

#capture.output(summary(stackoverflow_logit), file="R_logit_regr/stackoverflow_multivar_logit_regr.txt")
