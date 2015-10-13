# Copyright (c) 2013 Georgios Gousios
# MIT-licensed

# ERRORE RISCONTRATO: quando si esegue in mysql 'source dump.sql'
# ERROR 13 (HY000): Can't get stat of '/mnt/workingdir/stackoverflow_dump/Badges.xml' (Errcode: 13)
#
# SOLUZIONE
# sudo chown mysql:mysql /mnt/workingdir/stackoverflow_dump/ -R

drop database stackoverflow; 
create database stackoverflow DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
 
use stackoverflow;
 
create table Badges (
Id INT NOT NULL PRIMARY KEY,
UserId INT,
Name VARCHAR(50),
Date DATETIME
);
 
CREATE TABLE Comments (
Id INT NOT NULL PRIMARY KEY,
PostId INT NOT NULL,
Score INT NOT NULL DEFAULT 0,
Text TEXT,
CreationDate DATETIME,
UserId INT NOT NULL,
UserDisplayName TEXT
);
 
CREATE TABLE PostHistory (
Id INT NOT NULL PRIMARY KEY,
PostHistoryTypeId SMALLINT NOT NULL,
PostId INT NOT NULL,
RevisionGUID VARCHAR(36),
CreationDate DATETIME,
UserId INT NOT NULL,
CommentT TEXT,
Text TEXT,
CloseReasonId TEXT
);
 
CREATE TABLE Posts (
Id INT NOT NULL PRIMARY KEY,
PostTypeId SMALLINT,
AcceptedAnswerId INT,
ParentId INT,
Score INT,
ViewCount INT,
Body TEXT,
OwnerUserId INT NOT NULL,
OwnerDisplayName TEXT,
LastEditorUserId INT,
LastEditorDisplayName TEXT,
LastEditDate DATETIME,
LastActivityDate DATETIME,
CommunityOwnedDate DATETIME,
Title TEXT,
Tags TEXT,
AnswerCount INT,
CommentCount INT,
FavoriteCount INT,
CreationDate DATETIME,
ClosedDate DATETIME
);
 
CREATE TABLE Users (
Id INT NOT NULL PRIMARY KEY,
Reputation INT,
CreationDate DATETIME,
DisplayName VARCHAR(50),
LastAccessDate DATETIME,
Views INT DEFAULT 0,
WebsiteUrl VARCHAR(256),
Location VARCHAR(256),
AboutMe TEXT,
Age INT,
UpVotes INT,
DownVotes INT,
EmailHash VARCHAR(32),
AccountId INT,
ProfileImageUrl TEXT
);
 
CREATE TABLE Votes (
Id INT NOT NULL PRIMARY KEY,
PostId INT NOT NULL,
VoteTypeId SMALLINT,
CreationDate DATETIME,
UserId INT NOT NULL,
BountyAmount INT DEFAULT 0
);

CREATE TABLE PostLinks(
Id INT NOT NULL PRIMARY KEY,
CreationDate DATETIME,
PostId INT,
RelatedPostId INT,
LinkTypeId INT
);
 
load xml infile '/mnt/workingdir/stackoverflow_dump/Badges.xml'
into table Badges
rows identified by '<row>';
 
load xml infile '/mnt/workingdir/stackoverflow_dump/Comments.xml'
into table Comments
rows identified by '<row>';
 
load xml infile '/mnt/workingdir/stackoverflow_dump/PostHistory.xml'
into table PostHistory
rows identified by '<row>';
 
load xml infile '/mnt/workingdir/stackoverflow_dump/Posts.xml'
into table Posts
rows identified by '<row>';
 
load xml infile '/mnt/workingdir/stackoverflow_dump/Users.xml'
into table Users
rows identified by '<row>';

load xml infile '/mnt/workingdir/stackoverflow_dump/Votes.xml'
into table Votes
rows identified by '<row>';

load xml infile '/mnt/workingdir/stackoverflow_dump/PostLinks.xml'
into table PostLinks
rows identified by '<row>';
 
create index badges_idx_1 on Badges(UserId);
create index badges_idx_2 on Badges(Date);
create index badges_idx_3 on Badges(Id);
 
create index comments_idx_1 on Comments(PostId);
create index comments_idx_2 on Comments(UserId);
 
create index post_history_idx_1 on PostHistory(PostId);
create index post_history_idx_2 on PostHistory(UserId);
 
create index posts_idx_1 on Posts(AcceptedAnswerId);
create index posts_idx_2 on Posts(ParentId);
create index posts_idx_3 on Posts(OwnerUserId);
create index posts_idx_4 on Posts(LastEditorUserId);
create index posts_idx_5 on Posts(PostTypeId);
create index posts_idx_6 on Posts(Id);
 
create index votes_idx_1 on Votes(PostId);
create index votes_idx_2 on Votes(VoteTypeId);
create index votes_idx_3 on Votes(Id);
create index votes_idx_4 on Votes(CreationDate);
