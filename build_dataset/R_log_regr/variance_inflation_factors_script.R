# variance inflation factors
# misura quanto la varianza di un coefficiente di regressione stimata è aumentatata a causa della collinearità.
# la formula è la stessa della regressione, ma viene passata in input all'operatore VIF(glm(formula= ... ))

VIF(glm(formula=CodeSnippet ~  I(Weekday=='Weekend') + I(GMTHour=='Afternoon') + I(GMTHour=='Evening') + I(GMTHour=='Night') + BodyLength + TitleLength + SentimentPositiveScore + SentimentNegativeScore + CommentSentimentPositiveScore + CommentSentimentNegativeScore + AvgUpperCharsPPost + Gratitude + NTag + URL +IsTheSameTopicBTitle, data=stackoverflow_dataset, family=binomial()))


VIF(glm(formula=Weekday ~  CodeSnippet + I(GMTHour=='Afternoon') + I(GMTHour=='Evening') + I(GMTHour=='Night') + BodyLength + TitleLength + SentimentPositiveScore + SentimentNegativeScore + CommentSentimentPositiveScore + CommentSentimentNegativeScore + AvgUpperCharsPPost + Gratitude + NTag + URL +IsTheSameTopicBTitle, data=stackoverflow_dataset, family=binomial()))


VIF(glm(formula=GMTHour ~  CodeSnippet + I(Weekday=='Weekend') + BodyLength + TitleLength + SentimentPositiveScore + SentimentNegativeScore + CommentSentimentPositiveScore + CommentSentimentNegativeScore + AvgUpperCharsPPost + Gratitude + NTag + URL +IsTheSameTopicBTitle, data=stackoverflow_dataset, family=binomial()))


VIF(glm(formula=BodyLength ~  I(Weekday=='Weekend') + I(GMTHour=='Afternoon') + I(GMTHour=='Evening') + I(GMTHour=='Night') + CodeSnippet + TitleLength + SentimentPositiveScore + SentimentNegativeScore + CommentSentimentPositiveScore + CommentSentimentNegativeScore + AvgUpperCharsPPost + Gratitude + NTag + URL +IsTheSameTopicBTitle, data=stackoverflow_dataset, family=binomial()))


VIF(glm(formula=TitleLength ~  I(Weekday=='Weekend') + I(GMTHour=='Afternoon') + I(GMTHour=='Evening') + I(GMTHour=='Night') + CodeSnippet + BodyLength + SentimentPositiveScore + SentimentNegativeScore + CommentSentimentPositiveScore + CommentSentimentNegativeScore + AvgUpperCharsPPost + Gratitude + NTag + URL +IsTheSameTopicBTitle, data=stackoverflow_dataset, family=binomial()))


VIF(glm(formula=SentimentPositiveScore ~  I(Weekday=='Weekend') + I(GMTHour=='Afternoon') + I(GMTHour=='Evening') + I(GMTHour=='Night') + CodeSnippet + TitleLength + BodyLength + SentimentNegativeScore + CommentSentimentPositiveScore + CommentSentimentNegativeScore + AvgUpperCharsPPost + Gratitude + NTag + URL +IsTheSameTopicBTitle, data=stackoverflow_dataset, family=binomial()))


VIF(glm(formula=SentimentNegativeScore ~  I(Weekday=='Weekend') + I(GMTHour=='Afternoon') + I(GMTHour=='Evening') + I(GMTHour=='Night') + CodeSnippet + BodyLength + SentimentPositiveScore + TitleLength + CommentSentimentPositiveScore + CommentSentimentNegativeScore + AvgUpperCharsPPost + Gratitude + NTag + URL +IsTheSameTopicBTitle, data=stackoverflow_dataset, family=binomial()))

VIF(glm(formula= CommentSentimentPositiveScore ~  I(Weekday=='Weekend') + I(GMTHour=='Afternoon') + I(GMTHour=='Evening') + I(GMTHour=='Night') + CodeSnippet + BodyLength + SentimentPositiveScore + TitleLength + SentimentNegativeScore + CommentSentimentNegativeScore + AvgUpperCharsPPost + Gratitude + NTag + URL +IsTheSameTopicBTitle, data=stackoverflow_dataset, family=binomial()))

VIF(glm(formula= CommentSentimentNegativeScore ~  I(Weekday=='Weekend') + I(GMTHour=='Afternoon') + I(GMTHour=='Evening') + I(GMTHour=='Night') + CodeSnippet + BodyLength + SentimentPositiveScore + TitleLength + SentimentNegativeScore +  CommentSentimentPositiveScore + AvgUpperCharsPPost + Gratitude + NTag + URL +IsTheSameTopicBTitle, data=stackoverflow_dataset, family=binomial()))

VIF(glm(formula= AvgUpperCharsPPost ~  I(Weekday=='Weekend') + I(GMTHour=='Afternoon') + I(GMTHour=='Evening') + I(GMTHour=='Night') + CodeSnippet + BodyLength + SentimentPositiveScore + TitleLength + SentimentNegativeScore +  CommentSentimentPositiveScore + CommentSentimentNegativeScore + Gratitude + NTag + URL +IsTheSameTopicBTitle, data=stackoverflow_dataset, family=binomial()))

VIF(glm(formula= Gratitude ~  I(Weekday=='Weekend') + I(GMTHour=='Afternoon') + I(GMTHour=='Evening') + I(GMTHour=='Night') + CodeSnippet + BodyLength + SentimentPositiveScore + TitleLength + SentimentNegativeScore +  CommentSentimentPositiveScore + CommentSentimentNegativeScore + AvgUpperCharsPPost + NTag + URL +IsTheSameTopicBTitle, data=stackoverflow_dataset, family=binomial()))

VIF(glm(formula=NTag ~  I(Weekday=='Weekend') + I(GMTHour=='Afternoon') + I(GMTHour=='Evening') + I(GMTHour=='Night') + CodeSnippet + BodyLength + SentimentPositiveScore + TitleLength + SentimentNegativeScore +  CommentSentimentPositiveScore + CommentSentimentNegativeScore + AvgUpperCharsPPost + Gratitude + URL +IsTheSameTopicBTitle, data=stackoverflow_dataset, family=binomial()))

VIF(glm(formula= URL ~  I(Weekday=='Weekend') + I(GMTHour=='Afternoon') + I(GMTHour=='Evening') + I(GMTHour=='Night') + CodeSnippet + BodyLength + SentimentPositiveScore + TitleLength + SentimentNegativeScore +  CommentSentimentPositiveScore + CommentSentimentNegativeScore + AvgUpperCharsPPost + Gratitude + NTag +IsTheSameTopicBTitle, data=stackoverflow_dataset, family=binomial()))

VIF(glm(formula= IsTheSameTopicBTitle ~  I(Weekday=='Weekend') + I(GMTHour=='Afternoon') + I(GMTHour=='Evening') + I(GMTHour=='Night') + CodeSnippet + BodyLength + SentimentPositiveScore + TitleLength + SentimentNegativeScore +  CommentSentimentPositiveScore + CommentSentimentNegativeScore + AvgUpperCharsPPost + Gratitude + NTag +URL, data=stackoverflow_dataset, family=binomial()))

VIF(glm(formula=CodeSnippet ~  I(Weekday=='Weekend') + I(GMTHour=='Afternoon') + I(GMTHour=='Evening') + I(GMTHour=='Night') + BodyLength + TitleLength + SentimentPositiveScore + SentimentNegativeScore + CommentSentimentPositiveScore + CommentSentimentNegativeScore + AvgUpperCharsPPost + Gratitude + NTag + URL +IsTheSameTopicBTitle, data=stackoverflow_dataset, family=binomial()))


VIF(glm(formula=Weekday ~  CodeSnippet + I(GMTHour=='Afternoon') + I(GMTHour=='Evening') + I(GMTHour=='Night') + BodyLength + TitleLength + SentimentPositiveScore + SentimentNegativeScore + CommentSentimentPositiveScore + CommentSentimentNegativeScore + AvgUpperCharsPPost + Gratitude + NTag + URL +IsTheSameTopicBTitle, data=stackoverflow_dataset, family=binomial()))


VIF(glm(formula=GMTHour ~  CodeSnippet + I(Weekday=='Weekend') + BodyLength + TitleLength + SentimentPositiveScore + SentimentNegativeScore + CommentSentimentPositiveScore + CommentSentimentNegativeScore + AvgUpperCharsPPost + Gratitude + NTag + URL +IsTheSameTopicBTitle, data=stackoverflow_dataset, family=binomial()))


VIF(glm(formula=BodyLength ~  I(Weekday=='Weekend') + I(GMTHour=='Afternoon') + I(GMTHour=='Evening') + I(GMTHour=='Night') + CodeSnippet + TitleLength + SentimentPositiveScore + SentimentNegativeScore + CommentSentimentPositiveScore + CommentSentimentNegativeScore + AvgUpperCharsPPost + Gratitude + NTag + URL +IsTheSameTopicBTitle, data=stackoverflow_dataset, family=binomial()))


VIF(glm(formula=TitleLength ~  I(Weekday=='Weekend') + I(GMTHour=='Afternoon') + I(GMTHour=='Evening') + I(GMTHour=='Night') + CodeSnippet + BodyLength + SentimentPositiveScore + SentimentNegativeScore + CommentSentimentPositiveScore + CommentSentimentNegativeScore + AvgUpperCharsPPost + Gratitude + NTag + URL +IsTheSameTopicBTitle, data=stackoverflow_dataset, family=binomial()))


VIF(glm(formula=SentimentPositiveScore ~  I(Weekday=='Weekend') + I(GMTHour=='Afternoon') + I(GMTHour=='Evening') + I(GMTHour=='Night') + CodeSnippet + TitleLength + BodyLength + SentimentNegativeScore + CommentSentimentPositiveScore + CommentSentimentNegativeScore + AvgUpperCharsPPost + Gratitude + NTag + URL +IsTheSameTopicBTitle, data=stackoverflow_dataset, family=binomial()))


VIF(glm(formula=SentimentNegativeScore ~  I(Weekday=='Weekend') + I(GMTHour=='Afternoon') + I(GMTHour=='Evening') + I(GMTHour=='Night') + CodeSnippet + BodyLength + SentimentPositiveScore + TitleLength + CommentSentimentPositiveScore + CommentSentimentNegativeScore + AvgUpperCharsPPost + Gratitude + NTag + URL +IsTheSameTopicBTitle, data=stackoverflow_dataset, family=binomial()))

VIF(glm(formula= CommentSentimentPositiveScore ~  I(Weekday=='Weekend') + I(GMTHour=='Afternoon') + I(GMTHour=='Evening') + I(GMTHour=='Night') + CodeSnippet + BodyLength + SentimentPositiveScore + TitleLength + SentimentNegativeScore + CommentSentimentNegativeScore + AvgUpperCharsPPost + Gratitude + NTag + URL +IsTheSameTopicBTitle, data=stackoverflow_dataset, family=binomial()))

VIF(glm(formula= CommentSentimentNegativeScore ~  I(Weekday=='Weekend') + I(GMTHour=='Afternoon') + I(GMTHour=='Evening') + I(GMTHour=='Night') + CodeSnippet + BodyLength + SentimentPositiveScore + TitleLength + SentimentNegativeScore +  CommentSentimentPositiveScore + AvgUpperCharsPPost + Gratitude + NTag + URL +IsTheSameTopicBTitle, data=stackoverflow_dataset, family=binomial()))

VIF(glm(formula= AvgUpperCharsPPost ~  I(Weekday=='Weekend') + I(GMTHour=='Afternoon') + I(GMTHour=='Evening') + I(GMTHour=='Night') + CodeSnippet + BodyLength + SentimentPositiveScore + TitleLength + SentimentNegativeScore +  CommentSentimentPositiveScore + CommentSentimentNegativeScore + Gratitude + NTag + URL +IsTheSameTopicBTitle, data=stackoverflow_dataset, family=binomial()))

VIF(glm(formula= Gratitude ~  I(Weekday=='Weekend') + I(GMTHour=='Afternoon') + I(GMTHour=='Evening') + I(GMTHour=='Night') + CodeSnippet + BodyLength + SentimentPositiveScore + TitleLength + SentimentNegativeScore +  CommentSentimentPositiveScore + CommentSentimentNegativeScore + AvgUpperCharsPPost + NTag + URL +IsTheSameTopicBTitle, data=stackoverflow_dataset, family=binomial()))

VIF(glm(formula=NTag ~  I(Weekday=='Weekend') + I(GMTHour=='Afternoon') + I(GMTHour=='Evening') + I(GMTHour=='Night') + CodeSnippet + BodyLength + SentimentPositiveScore + TitleLength + SentimentNegativeScore +  CommentSentimentPositiveScore + CommentSentimentNegativeScore + AvgUpperCharsPPost + Gratitude + URL +IsTheSameTopicBTitle, data=stackoverflow_dataset, family=binomial()))

VIF(glm(formula= URL ~  I(Weekday=='Weekend') + I(GMTHour=='Afternoon') + I(GMTHour=='Evening') + I(GMTHour=='Night') + CodeSnippet + BodyLength + SentimentPositiveScore + TitleLength + SentimentNegativeScore +  CommentSentimentPositiveScore + CommentSentimentNegativeScore + AvgUpperCharsPPost + Gratitude + NTag +IsTheSameTopicBTitle, data=stackoverflow_dataset, family=binomial()))

VIF(glm(formula= IsTheSameTopicBTitle ~  I(Weekday=='Weekend') + I(GMTHour=='Afternoon') + I(GMTHour=='Evening') + I(GMTHour=='Night') + CodeSnippet + BodyLength + SentimentPositiveScore + TitleLength + SentimentNegativeScore +  CommentSentimentPositiveScore + CommentSentimentNegativeScore + AvgUpperCharsPPost + Gratitude + NTag +URL, data=stackoverflow_dataset, family=binomial()))

