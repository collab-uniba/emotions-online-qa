# Script per creare le viste materializzate


use stackoverflow_march;

#vista materializzata all Questions
DROP TABLE questions_mv;
CREATE TABLE questions_mv (
    q_postID INTEGER  NOT NULL PRIMARY KEY
  , q_title TEXT
  , q_body TEXT
  , q_tags TEXT
  , q_postDate   DATETIME           NOT NULL
  , q_ownerID INTEGER NOT NULL
  , q_acceptedAnswerId    INTEGER
  ,	q_answerCount INTEGER
  , UNIQUE INDEX pID (q_postID)
  , INDEX pDate (q_postDate)
  , INDEX pOwner (q_ownerID)
  , INDEX pAcceptedAnsw (q_acceptedAnswerId)
);


INSERT INTO questions_mv
SELECT Id, Title, Body, Tags, CreationDate, OwnerUserId, AcceptedAnswerId, AnswerCount 
FROM Posts WHERE Posts.PostTypeId = 1 AND Posts.OwnerUserId <> 0
;


#Question Score
DROP TABLE questiondownvotes_mv;
CREATE TABLE questiondownvotes_mv (
    d_postID INTEGER  NOT NULL 
  , d_ownerID INTEGER NOT NULL
  , d_postDate   DATETIME           NOT NULL
  , d_voteDate    DATETIME         NOT NULL
  , dts_voteDate DATE NOT NULL  
  , d_voteID INTEGER NOT NULL PRIMARY KEY
  , INDEX pID (d_postID)
  , INDEX oID (d_ownerID)
  , INDEX pDate (d_postDate)
  , INDEX vDate (d_voteDate)
  , INDEX v_ts_Date (dts_voteDate)
  , UNIQUE INDEX vID (d_voteID)
 , INDEX user_datavoto (d_ownerID, dts_voteDate)
);


INSERT INTO questiondownvotes_mv
SELECT Posts.Id, Posts.OwnerUserId, Posts.CreationDate, Votes.CreationDate, date(Votes.CreationDate), Votes.Id 
FROM Posts INNER JOIN Votes ON Posts.Id = Votes.PostId 
WHERE Posts.PostTypeId = 1 AND Votes.VoteTypeId = 3
;


#Materialized View for Question Upvotes
DROP TABLE questionupvotes_mv;
CREATE TABLE questionupvotes_mv (
    u_postID INTEGER  NOT NULL 
  , u_ownerID INTEGER NOT NULL
  , u_postDate   DATETIME           NOT NULL
  , u_voteDate    DATETIME         NOT NULL
  , uts_voteDate DATE NOT NULL  
  , u_voteID INTEGER NOT NULL PRIMARY KEY
  , INDEX pID (u_postID)
  , INDEX oID (u_ownerID)
  , INDEX pDate (u_postDate)
  , INDEX vDate (u_voteDate)
  , INDEX v_ts_Date (uts_voteDate)
  , UNIQUE INDEX vID (u_voteID)
 , INDEX user_datavoto (u_ownerID, uts_voteDate)
);


INSERT INTO questionupvotes_mv
SELECT Posts.Id, Posts.OwnerUserId, Posts.CreationDate, Votes.CreationDate, date(Votes.CreationDate), Votes.Id 
FROM Posts INNER JOIN Votes ON Posts.Id = Votes.PostId 
WHERE Posts.PostTypeId = 1 AND Votes.VoteTypeId = 2
;

#Materialized View for Answer Downvotes
DROP TABLE answerdownvotes_mv;
CREATE TABLE answerdownvotes_mv (
    d_postID INTEGER  NOT NULL 
  , d_ownerID INTEGER NOT NULL
  , d_postDate   DATETIME           NOT NULL
  , d_voteDate    DATETIME         NOT NULL
  , dts_voteDate DATE NOT NULL  
  , d_voteID INTEGER NOT NULL PRIMARY KEY
  , INDEX pID (d_postID)
  , INDEX oID (d_ownerID)
  , INDEX pDate (d_postDate)
  , INDEX vDate (d_voteDate)
  , INDEX v_ts_Date (dts_voteDate)
  , UNIQUE INDEX vID (d_voteID)
 , INDEX user_datavoto (d_ownerID, dts_voteDate)
);


INSERT INTO answerdownvotes_mv
SELECT Posts.Id, Posts.OwnerUserId, Posts.CreationDate, Votes.CreationDate, date(Votes.CreationDate), Votes.Id 
FROM Posts INNER JOIN Votes ON Posts.Id = Votes.PostId 
WHERE Posts.PostTypeId = 2 AND Votes.VoteTypeId = 3
;


#Materialized View for Answer Upvotes
DROP TABLE answerupvotes_mv;
CREATE TABLE answerupvotes_mv (
    u_postID INTEGER  NOT NULL 
  , u_ownerID INTEGER NOT NULL
  , u_postDate   DATETIME           NOT NULL
  , u_voteDate    DATETIME         NOT NULL
  , uts_voteDate DATE NOT NULL  
  , u_voteID INTEGER NOT NULL PRIMARY KEY
  , INDEX pID (u_postID)
  , INDEX oID (u_ownerID)
  , INDEX pDate (u_postDate)
  , INDEX vDate (u_voteDate)
  , INDEX v_ts_Date (uts_voteDate)
  , UNIQUE INDEX vID (u_voteID)
 , INDEX user_datavoto (u_ownerID, uts_voteDate)
);


INSERT INTO answerupvotes_mv
SELECT Posts.Id, Posts.OwnerUserId, Posts.CreationDate, Votes.CreationDate, date(Votes.CreationDate), Votes.Id 
FROM Posts INNER JOIN Votes ON Posts.Id = Votes.PostId 
WHERE Posts.PostTypeId = 2 AND Votes.VoteTypeId = 2
;


#risposte dell'utente accettate da altri

DROP TABLE acceptedanswer_mv;
CREATE TABLE acceptedanswer_mv (
    postID INTEGER  NOT NULL PRIMARY KEY
  , ownerID INTEGER NOT NULL
  , postDate   DATETIME           NOT NULL
  , voteDate    DATETIME         NOT NULL
  , ts_voteDate    DATE      NOT NULL
  , voteID INTEGER NOT NULL
  , UNIQUE INDEX pID (postID)
  , INDEX oID (ownerID)
  , INDEX pDate (postDate)
  , INDEX vDate (voteDate)
  , UNIQUE INDEX vID (voteID)
 , INDEX user_dataVoto (ownerID, ts_voteDate)
);


INSERT INTO acceptedanswer_mv
SELECT Posts.Id, Posts.OwnerUserId, Posts.CreationDate, Votes.CreationDate, date(Votes.CreationDate), Votes.Id
FROM Posts INNER JOIN Votes ON Posts.Id = Votes.PostId 
WHERE Posts.PostTypeId = 2 AND Votes.VoteTypeId = 1
;

#risposte accettate dall'utente alle sue domande
DROP TABLE questwithacceptedanswer_mv;
CREATE TABLE questwithacceptedanswer_mv (
    postID INTEGER  NOT NULL PRIMARY KEY
  , ownerID INTEGER NOT NULL
  , postDate   DATETIME           NOT NULL
  , voteDate    DATETIME         NOT NULL
  , ts_voteDate    DATE       NOT NULL
  , voteID INTEGER NOT NULL 
  , UNIQUE INDEX pID (postID)
  , INDEX pDate (postDate)
  , INDEX vDate (voteDate)
  , INDEX vID (voteID)
 , INDEX user_dataVoto (ownerID, ts_voteDate)
);


INSERT INTO questwithacceptedanswer_mv
SELECT q_postID, q_ownerID, q_postDate, Votes.CreationDate, date(Votes.CreationDate), Votes.Id
FROM questions_mv INNER JOIN Votes ON questions_mv.q_acceptedAnswerId = Votes.PostId
WHERE questions_mv.q_acceptedAnswerId IS NOT NULL AND Votes.VoteTypeId = 1
;

# userscommentquestions_mv
# Vista materializzata: Contiene tutti i commenti che un utente di una domanda ha scritto alla sua domanda

DROP TABLE userscommentsquestions_mv;
CREATE TABLE  userscommentsquestions_mv (
	c_Id INTEGER NOT NULL PRIMARY KEY
  ,	q_Id INTEGER NOT NULL
  ,	userId INTEGER NOT NULL
  ,	c_text TEXT
  ,	c_ts_creationDate DATE NOT NULL
  ,	INDEX idx_c_Id (c_Id)
  ,	INDEX idx_q_Id (q_Id)
  ,	INDEX idx_userId (userId)
  ,	INDEX idx_c_ts_creationDate (c_ts_creationDate)
  ,	INDEX idx_quest_dataVoto(q_Id, c_ts_creationDate)
);

INSERT INTO userscommentsquestions_mv
SELECT Comments.Id as c_Id, questions_mv.q_postID as q_Id, questions_mv.q_ownerID as userId, Comments.Text as c_text, date(Comments.CreationDate) as c_date
FROM questions_mv INNER JOIN Comments ON questions_mv.q_postId = Comments.PostId AND questions_mv.q_ownerId = Comments.UserId;

# Script per creare la tabella questionHistory_mv
# crea una tabella che contiene  le domande con PostHistory non nullo
# Utile per estrarre le domande modificate e rimosse 

use stackoverflow;
DROP TABLE questionsHistory_mv;
CREATE TABLE questionsHistory_mv (
	Id INTEGER NOT NULL PRIMARY KEY 
  , postID INTEGER  
  , postHistoryTypeId SMALLINT
  , creationDate datetime
  , INDEX pID (postID)
  , INDEX pDate (creationDate)
);


INSERT INTO questionsHistory_mv SELECT PostHistory.Id, PostHistory.postId, PostHistory.PostHistoryTypeId, PostHistory.CreationDate FROM questions_mv1 INNER JOIN PostHistory ON questions_mv1.q_postID = PostHistory.PostId  WHERE PostHistoryTypeId IS NOT NULL;

SELECT postId, creationDate, PostHistoryTypeId FROM    qutionsHistory_mv  WHERE questionsHistory_mv.creationDate IN (select MAX(creationDate) from questionsHistory_mv a where questionsHistory_mv.postID = a.postId Group by a.postId )AND PostHistoryTypeId ='10' OR PostHistoryTypeId='12';

