# Script per eseguire il roc test
# Carica i dati di una predizione random e della predizione calcolata

require(utils)
library(pROC)
library(aod)

prediction   <- read.csv('/mnt/vdb1/emotions-online-qa/build_dataset/output_faffa/metric_all/rot_test/stackoverflow_all.csv',sep=',')
randomPred  <- read.csv('/mnt/vdb1/emotions-online-qa/build_dataset/output_faffa/metric_all/rot_test/stackoverflow_random.csv', sep=',')

 
#il file associato a rocPrediction contiene le colonne: gold e prediction
rocPrediction  <- roc(prediction$gold, porediction$prediction)
#il file associato a rocRandomPred contiene le colonne gold e random_prediction
rocRandomPred <- roc(prediction$gold, randomPred$random_prediction)


###### INIZIO TEST ########
comp_pred_randomPred <- roc.test(rocPrediction, rocRandomPred, method="bootstrap")
#scrittura risultati sul file
capture.output(comp_pred_randomPred, file="stackoverflow_all_random_pvalue.txt")

