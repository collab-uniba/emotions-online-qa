library(biglm)

print("Processing codesnip")
stackoverflow_codesnip <- bigglm(formula=Successful ~ CodeSnippet, data=stackoverflow_dataset, family=binomial())
capture.output(summary(stackoverflow_codesnip), file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=FALSE)
cat("\n\n", file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)

print("Processing gmthour")
stackoverflow_gmthour <- bigglm(formula=Successful ~ GMTHour, data=stackoverflow_dataset, family=binomial())
capture.output(summary(stackoverflow_gmthour), file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)
cat("\n\n", file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)

print("Processing weekday")
stackoverflow_weekday <- bigglm(formula=Successful ~ Weekday, data=stackoverflow_dataset, family=binomial())
capture.output(summary(stackoverflow_weekday), file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)
cat("\n\n", file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)

print("Processing bodylen")
stackoverflow_bodylen <- bigglm(formula=Successful ~ BodyLength, data=stackoverflow_dataset, family=binomial())
capture.output(summary(stackoverflow_bodylen), file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)
cat("\n\n", file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)

print("Processing titlelen")
stackoverflow_titlelen <- bigglm(formula=Successful ~ TitleLength, data=stackoverflow_dataset, family=binomial())
capture.output(summary(stackoverflow_titlelen), file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)
cat("\n\n", file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)

print("Processing questionscore")
stackoverflow_questionscore <- bigglm(formula=Successful ~ QuestionScore, data=stackoverflow_dataset, family=binomial())
capture.output(summary(stackoverflow_questionscore), file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)
cat("\n\n", file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)

print("Processing answerscore")
stackoverflow_answerscore <- bigglm(formula=Successful ~ AnswerScore, data=stackoverflow_dataset, family=binomial())
capture.output(summary(stackoverflow_answerscore), file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)
cat("\n\n", file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)

print("Processing usersanswacc")
stackoverflow_usersanswacc <- bigglm(formula=Successful ~ UsersAnswersAccepted, data=stackoverflow_dataset, family=binomial())
capture.output(summary(stackoverflow_usersanswacc), file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)
cat("\n\n", file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)

print("Processing usersquestacc")
stackoverflow_usersquestacc <- bigglm(formula=Successful ~ UsersQuestionsAccepted, data=stackoverflow_dataset, family=binomial())
capture.output(summary(stackoverflow_usersquestacc), file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)
cat("\n\n", file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)

print("Processing numberbadges")
stackoverflow_numberbadges <- bigglm(formula=Successful ~ NumberOfBadges, data=stackoverflow_dataset, family=binomial())
capture.output(summary(stackoverflow_numberbadges), file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)
cat("\n\n", file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)

print("Processing sentipos")
stackoverflow_sentipos <- bigglm(formula=Successful ~ SentimentPositiveScore, data=stackoverflow_dataset, family=binomial())
capture.output(summary(stackoverflow_sentipos), file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)
cat("\n\n", file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)

print("Processing sentineg")
stackoverflow_sentineg <- bigglm(formula=Successful ~ SentimentNegativeScore, data=stackoverflow_dataset, family=binomial())
capture.output(summary(stackoverflow_sentineg), file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)
cat("\n\n", file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)

print("Processing topic")
stackoverflow_topic <- bigglm(formula=Successful ~ Topic, data=stackoverflow_dataset, family=binomial())
capture.output(summary(stackoverflow_topic), file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)
cat("\n\n", file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)

print("Processing AFFECT")
stackoverflow_AFFECT <- bigglm(formula=Successful ~ AFFECT, data=stackoverflow_dataset, family=binomial())
capture.output(summary(stackoverflow_AFFECT), file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)
cat("\n\n", file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)

print("Processing POSEMO")
stackoverflow_POSEMO <- bigglm(formula=Successful ~ POSEMO, data=stackoverflow_dataset, family=binomial())
capture.output(summary(stackoverflow_POSEMO), file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)
cat("\n\n", file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)

print("Processing POSFEEL")
stackoverflow_POSFEEL <- bigglm(formula=Successful ~ POSFEEL, data=stackoverflow_dataset, family=binomial())
capture.output(summary(stackoverflow_POSFEEL), file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)
cat("\n\n", file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)

print("Processing OPTIM")
stackoverflow_OPTIM <- bigglm(formula=Successful ~ OPTIM, data=stackoverflow_dataset, family=binomial())
capture.output(summary(stackoverflow_OPTIM), file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)
cat("\n\n", file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)

print("Processing NEGEMO")
stackoverflow_NEGEMO <- bigglm(formula=Successful ~ NEGEMO, data=stackoverflow_dataset, family=binomial())
capture.output(summary(stackoverflow_NEGEMO), file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)
cat("\n\n", file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)

print("Processing ANX")
stackoverflow_ANX <- bigglm(formula=Successful ~ ANX, data=stackoverflow_dataset, family=binomial())
capture.output(summary(stackoverflow_ANX), file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)
cat("\n\n", file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)

print("Processing ANGER")
stackoverflow_ANGER <- bigglm(formula=Successful ~ ANGER, data=stackoverflow_dataset, family=binomial())
capture.output(summary(stackoverflow_ANGER), file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)
cat("\n\n", file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)

print("Processing SAD")
stackoverflow_SAD <- bigglm(formula=Successful ~ SAD, data=stackoverflow_dataset, family=binomial())
capture.output(summary(stackoverflow_SAD), file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)
cat("\n\n", file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)

print("Processing COGMECH")
stackoverflow_COGMECH <- bigglm(formula=Successful ~ COGMECH, data=stackoverflow_dataset, family=binomial())
capture.output(summary(stackoverflow_COGMECH), file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)
cat("\n\n", file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)

print("Processing INSIGHT")
stackoverflow_INSIGHT <- bigglm(formula=Successful ~ INSIGHT, data=stackoverflow_dataset, family=binomial())
capture.output(summary(stackoverflow_INSIGHT), file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)
cat("\n\n", file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)

print("Processing DISCREP")
stackoverflow_DISCREP <- bigglm(formula=Successful ~ DISCREP, data=stackoverflow_dataset, family=binomial())
capture.output(summary(stackoverflow_DISCREP), file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)
cat("\n\n", file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)

print("Processing INHIB")
stackoverflow_INHIB <- bigglm(formula=Successful ~ INHIB, data=stackoverflow_dataset, family=binomial())
capture.output(summary(stackoverflow_INHIB), file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)
cat("\n\n", file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)

print("Processing TENTAT")
stackoverflow_TENTAT <- bigglm(formula=Successful ~ TENTAT, data=stackoverflow_dataset, family=binomial())
capture.output(summary(stackoverflow_TENTAT), file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)
cat("\n\n", file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)

print("Processing CERTAIN")
stackoverflow_CERTAIN <- bigglm(formula=Successful ~ CERTAIN, data=stackoverflow_dataset, family=binomial())
capture.output(summary(stackoverflow_CERTAIN), file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)
cat("\n\n", file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)

print("Processing FEEL")
stackoverflow_FEEL <- bigglm(formula=Successful ~ FEEL, data=stackoverflow_dataset, family=binomial())
capture.output(summary(stackoverflow_FEEL), file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)
cat("\n\n", file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)

print("Processing SOCIAL")
stackoverflow_SOCIAL <- bigglm(formula=Successful ~ SOCIAL, data=stackoverflow_dataset, family=binomial())
capture.output(summary(stackoverflow_SOCIAL), file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)
cat("\n\n", file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)

print("Processing COMM")
stackoverflow_COMM <- bigglm(formula=Successful ~ COMM, data=stackoverflow_dataset, family=binomial())
capture.output(summary(stackoverflow_COMM), file="R_logit_regr/stackoverflow_univar_log_regr.txt",append=TRUE)
