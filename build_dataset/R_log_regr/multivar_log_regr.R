# Carica il file csv che contiene il dataset.
# Converte i campi boolean come CodeSnippet e Successful da 'yes', 'no' a TRUE, FALSE.
# Avvia la regressione logistica.

library(glmnet) #per ora non la usa
library(aod)
source('orcip_so.R')
#source('timaProbabilita.R') #DECOMMENTARE per calcolare la probabilità stimata

stackoverflow_dataset <- read.csv('/mnt/vdb1/tesi_pavone/database/datasets/filtered_questions_metrics.csv',sep=';')
stackoverflow_dataset$CodeSnippet <- sapply(as.character(stackoverflow_dataset$CodeSnippet),switch,'yes'=as.logical(TRUE),'no'=as.logical(FALSE))
stackoverflow_dataset$Successful <- sapply(as.character(stackoverflow_dataset$Successful),switch,'yes'=as.logical(TRUE),'no'=as.logical(FALSE))
stackoverflow_dataset$IsTheSameTopicBTitle <- sapply(as.character(stackoverflow_dataset$IsTheSameTopicBTitle),switch,'yes'=as.logical(TRUE),'no'=as.logical(FALSE))
stackoverflow_dataset$Gratitude <- sapply(as.character(stackoverflow_dataset$Gratitude),switch,'yes'=as.logical(TRUE),'no'=as.logical(FALSE))

cat("Dati caricati correttamente ")
cat("Inizio regressione..")
stackoverflow_logit <- glm(formula=Successful ~ CodeSnippet +
                       I(Weekday=='Weekend') + I(GMTHour=='Afternoon') + I(GMTHour=='Evening') +
                       I(GMTHour=='Night') + BodyLength + TitleLength + SentimentPositiveScore + SentimentNegativeScore +
					   CommentSentimentPositiveScore + CommentSentimentNegativeScore + Gratitude + NTag +
					   URL +IsTheSameTopicBTitle,
                       data=stackoverflow_dataset, family=multinomial())

cat("Regressione eseguita con successo..")
capture.output(summary(stackoverflow_logit), file="/mnt/vdb1/emotions-online-qa/regressione12ott2015.txt")

#plot.CodeSnippet_prob_pertopic(stackoverflow_dataset, stackoverflow_logit_new_DEF)
#DECOMMENTARE la riga soprastante per calcolare la probabilità stimata

cat("Calcolo odds in corso.")
orcipwald.glm(stackoverflow_logit)
