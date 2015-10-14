# Script per creare il csv della domande editate 
# Di ogni database dei siti di Stack Exchange

use bitcoin;
select distinct postId from questionsHistory_mv where postHistoryTypeId ='5' or postHistoryTypeId ='4' or postHistoryTypeId ='6' INTO OUTFILE 'editedq_bitcoin.csv' FIELDS TERMINATED BY ';' LINES TERMINATED BY '\n' ;

use crossValidated;
select distinct postId from questionsHistory_mv where postHistoryTypeId ='5' or postHistoryTypeId ='4' or postHistoryTypeId ='6' INTO OUTFILE 'editedq_crossValidated.csv' FIELDS TERMINATED BY ';' LINES TERMINATED BY '\n' ;

use englishLL;
select distinct postId from questionsHistory_mv where postHistoryTypeId ='5' or postHistoryTypeId ='4' or postHistoryTypeId ='6' INTO OUTFILE 'editedq_englishLL.csv' FIELDS TERMINATED BY ';' LINES TERMINATED BY '\n' ;

use englishLU;
select distinct postId from questionsHistory_mv where postHistoryTypeId ='5' or postHistoryTypeId ='4' or postHistoryTypeId ='6' INTO OUTFILE 'editedq_englishLU.csv' FIELDS TERMINATED BY ';' LINES TERMINATED BY '\n' ;

use freelancing;
select distinct postId from questionsHistory_mv where postHistoryTypeId ='5' or postHistoryTypeId ='4' or postHistoryTypeId ='6' INTO OUTFILE 'editedq_freelancing.csv' FIELDS TERMINATED BY ';' LINES TERMINATED BY '\n' ;
use graphicdesign;
select distinct postId from questionsHistory_mv where postHistoryTypeId ='5' or postHistoryTypeId ='4' or postHistoryTypeId ='6' INTO OUTFILE 'editedq_graphicdesign.csv' FIELDS TERMINATED BY ';' LINES TERMINATED BY '\n' ;

use homeImp;
select distinct postId from questionsHistory_mv where postHistoryTypeId ='5' or postHistoryTypeId ='4' or postHistoryTypeId ='6' INTO OUTFILE 'editedq_homeImp.csv' FIELDS TERMINATED BY ';' LINES TERMINATED BY '\n' ;

use mathematics;
select distinct postId from questionsHistory_mv where postHistoryTypeId ='5' or postHistoryTypeId ='4' or postHistoryTypeId ='6' INTO OUTFILE 'editedq_mathematics.csv' FIELDS TERMINATED BY ';' LINES TERMINATED BY '\n' ;

use mathoverflow;
select distinct postId from questionsHistory_mv where postHistoryTypeId ='5' or postHistoryTypeId ='4' or postHistoryTypeId ='6' INTO OUTFILE 'editedq_mathoverflow.csv' FIELDS TERMINATED BY ';' LINES TERMINATED BY '\n' ;

use miYodeya;
select distinct postId from questionsHistory_mv where postHistoryTypeId ='5' or postHistoryTypeId ='4' or postHistoryTypeId ='6' INTO OUTFILE 'editedq_miYodeya.csv' FIELDS TERMINATED BY ';' LINES TERMINATED BY '\n' ;

use patents;
select distinct postId from questionsHistory_mv where postHistoryTypeId ='5' or postHistoryTypeId ='4' or postHistoryTypeId ='6' INTO OUTFILE 'editedq_patents.csv' FIELDS TERMINATED BY ';' LINES TERMINATED BY '\n' ;

use physics;
select distinct postId from questionsHistory_mv where postHistoryTypeId ='5' or postHistoryTypeId ='4' or postHistoryTypeId ='6' INTO OUTFILE 'editedq_physics.csv' FIELDS TERMINATED BY ';' LINES TERMINATED BY '\n' ;

use projManagement;
select distinct postId from questionsHistory_mv where postHistoryTypeId ='5' or postHistoryTypeId ='4' or postHistoryTypeId ='6' INTO OUTFILE 'editedq_projManagement.csv' FIELDS TERMINATED BY ';' LINES TERMINATED BY '\n' ;

use quantFin;
select distinct postId from questionsHistory_mv where postHistoryTypeId ='5' or postHistoryTypeId ='4' or postHistoryTypeId ='6' INTO OUTFILE 'editedq_quantFin.csv' FIELDS TERMINATED BY ';' LINES TERMINATED BY '\n' ;

use scifi;
select distinct postId from questionsHistory_mv where postHistoryTypeId ='5' or postHistoryTypeId ='4' or postHistoryTypeId ='6' INTO OUTFILE 'editedq_scifi.csv' FIELDS TERMINATED BY ';' LINES TERMINATED BY '\n' ;

use serverfault;
select distinct postId from questionsHistory_mv where postHistoryTypeId ='5' or postHistoryTypeId ='4' or postHistoryTypeId ='6' INTO OUTFILE 'editedq_serverfault.csv' FIELDS TERMINATED BY ';' LINES TERMINATED BY '\n' ;

use superuser;
select distinct postId from questionsHistory_mv where postHistoryTypeId ='5' or postHistoryTypeId ='4' or postHistoryTypeId ='6' INTO OUTFILE 'editedq_superuser.csv' FIELDS TERMINATED BY ';' LINES TERMINATED BY '\n' ;

use workplace;
select distinct postId from questionsHistory_mv where postHistoryTypeId ='5' or postHistoryTypeId ='4' or postHistoryTypeId ='6' INTO OUTFILE 'editedq_workplace.csv' FIELDS TERMINATED BY ';' LINES TERMINATED BY '\n' ;
