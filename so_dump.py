# -*- coding: utf-8 -*-

import sqlite3
import os
import xml.etree.cElementTree as etree
import logging

ANATHOMY = {
 'Badges': {
  'Id':'INTEGER',
  'UserId':'INTEGER', # Id dell'utente che ha ricevuto il badge
  'Name':'TEXT',	  # Nome del badge http://meta.stackexchange.com/help/badges
  'Date':'DATETIME',  # Data di ricevimento del badge
 },
 'Comments': {
  'Id':'INTEGER',				# Id del commento
  'PostId':'INTEGER',			# Id del post commentato
  'Score':'INTEGER',			# Punteggio di utilità del commento
  'Text':'TEXT',				# Testo del commento
  'CreationDate':'DATETIME',	# Data di creazione del commento
  'UserId':'INTEGER',			# Id dell'utente che ha scritto il commento (presente solo se l'utente non è stato cancellato)
  'UserDisplayName':'TEXT'		# Nome dell'utente che ha scritto il commento (presente solo se l'utente è stato cancellato)
 },
 'Posts': {
  'Id':'INTEGER',					# Id del post
  'PostTypeId':'INTEGER', 			# Tipo del post: 
									# 	1 se è una domanda, 
									# 	2 se è una risposta
									# 	3 wiki
									# 	4 TagWikiExcerpt
									# 	5 TagWiki
									# 	6 ModeratorNomination
									# 	7 WikiPlaceholder
									# 	8 PrivilegeWiki
  'ParentID':'INTEGER', 			# Id della domanda a cui risponde il post, presente solo se PostTypeId è 2
  'AcceptedAnswerId':'INTEGER', 	# Id della risposta accettata, presente solo se PostTypeId è 1
  'CreationDate':'DATETIME',		# Data di creazione del post
  'Score':'INTEGER',				# Punteggio del post
  'ViewCount':'INTEGER',			# Numero di visualizzazioni nel caso in cui il post sia una domanda (PostTypeId è 1)
  'Body':'TEXT',					# Corpo del post
  'OwnerUserId':'INTEGER', 			# Id dell'utente proprietario del post (presente solo se l'utente non è stato cancellato) 
  'OwnerDisplayName':'TEXT',		# Nome dell'utente proprietario del post (presente solo se l'utente è stato cancellato)
  'LastEditorUserId':'INTEGER',		# Id dell'ultimo utente che ha editato il post http://meta.stackexchange.com/help/editing
  'LastEditorDisplayName':'TEXT', 	# Nome dell'ultimo utente che ha modificato il post
  'LastEditDate':'DATETIME', 		# Data dell'ultima modifica del post
  'LastActivityDate':'DATETIME',	# Data dell'ultima attività del post (può corrispondere con la data di creazione, dell'ultimo modifica)
  'CommunityOwnedDate':'DATETIME', #(present only if post is community wikied)
  'Title':'TEXT',					# Titolo del post
  'Tags':'TEXT',					# Lista dei tag associati al post (<tag1><tag2>..<tagN>)
  'AnswerCount':'INTEGER',			# Numero di risposte
  'CommentCount':'INTEGER',			# Numero di commenti
  'FavoriteCount':'INTEGER',		# Numero di utenti che hanno votato come preferito il post (presente solo se PostTypeId è 1)
  'ClosedDate':'DATETIME',			# Data di chiusura del post
 },
 'PostHistory': {
  'Id':'INTEGER',
  'PostHistoryTypeId':'INTEGER',	# Tipo dello storico
           #- 1: Initial Title - The first title a question is asked with.
           #- 2: Initial Body - The first raw body text a post is submitted with.
           #- 3: Initial Tags - The first tags a question is asked with.
           #- 4: Edit Title - A question's title has been changed.
           #- 5: Edit Body - A post's body has been changed, the raw text is stored here as markdown.
           #- 6: Edit Tags - A question's tags have been changed.
           #- 7: Rollback Title - A question's title has reverted to a previous version.
           #- 8: Rollback Body - A post's body has reverted to a previous version - the raw text is stored here.
           #- 9: Rollback Tags - A question's tags have reverted to a previous version.
           #- 10: Post Closed - A post was voted to be closed.
           #- 11: Post Reopened - A post was voted to be reopened.
           #- 12: Post Deleted - A post was voted to be removed.
           #- 13: Post Undeleted - A post was voted to be restored.
           #- 14: Post Locked - A post was locked by a moderator.
           #- 15: Post Unlocked - A post was unlocked by a moderator.
           #- 16: Community Owned - A post has become community owned.
           #- 17: Post Migrated - A post was migrated.
           #- 18: Question Merged - A question has had another, deleted question merged into itself.
           #- 19: Question Protected - A question was protected by a moderator
           #- 20: Question Unprotected - A question was unprotected by a moderator
           #- 21: Post Disassociated - An admin removes the OwnerUserId from a post.
           #- 22: Question Unmerged - A previously merged question has had its answers and votes restored.
           #- 24: Suggested Edit Applied
           #- 25: Post Tweeted
           #- 31: Discussion moved to chat
           #- 33: Post Notice Added
           #- 34: Post Notice Removed
           #- 35: Post Migrated Away
           #- 36: Post Migrated Here
           #- 37: Post Merge Source
           #- 38: Post Merge Destination
  'PostId':'INTEGER',			# Id del post
  'RevisionGUID':'',			# Stringa alfanumerica che identifica univocamente una revisione
  'CreationDate':'DATETIME',	# Data di creazione dello storico
  'UserId':'INTEGER',			# Id dell'utente che ha apportato la modifica, dipendentemente al valore di PostHistoryTypeId
  'UserDisplayName':'TEXT',		# Nome dell'utente, visualizzato se l'utente è stato rimosso quindi non è più referenziato dall'id
  'Comment':'TEXT',				# Commento sulla revisione
  'Text':'TEXT',
           #- If PostHistoryTypeId = 10, 11, 12, 13, 14, or 15  this column will contain a JSON encoded string with all users who have voted for the PostHistoryTypeId
           #- If PostHistoryTypeId = 17 this column will contain migration details of either "from <url>" or "to <url>"
  'CloseReasonId':'INTEGER',	# Motivo per il quale il post è stato chiuso
           #- 1: Exact Duplicate - This question covers exactly the same ground as earlier questions on this topic; its answers may be merged with another identical question.
           #- 2: off-topic
           #- 3: subjective
           #- 4: not a real question
           #- 7: too localized
           #- 10: general reference
           #- 20: noise of pointless
           #- 101: duplicate
           #- 102: off-topic
           #- 103: unclear what you're asking
           #- 104: too broad
           #- 105: primarly opinion-based
 },
 'PostLinks': {
  'Id':'INTEGER',
  'CreationDate':'DATETIME',	# Data di creazione del link
  'PostId':'INTEGER',			# Id del post
  'RelatedPostId':'INTEGER',	# Id del post linkato all'interno di PostId
  'LinkTypeId':'INTEGER',		# Tipo di link
           #- 1: Linked, all'interno di PostId è stato menzionato RelatedPostId
           #- 3: Duplicate, PostId è un duplicato di RelatedPostId
	# Se PostId viene chiuso allora si viene reindirizzati a RelatedPostId
 },
 'Votes': {
  'Id':'INTEGER',			
  'PostId':'INTEGER',			# Id del Post
  'UserId':'INTEGER',			# Id dell'utente
  'VoteTypeId':'INTEGER',		# Tipo di voto
           # -   1: AcceptedByOriginator
           # -   2: UpMod
           # -   3: DownMod
           # -   4: Offensive
           # -   5: Favorite
           # -   6: Close
           # -   7: Reopen
           # -   8: BountyStart
           # -   9: BountyClose
           # -  10: Deletion
           # -  11: Undeletion
           # -  12: Spam
           # -  13: InformModerator
  'CreationDate':'DATETIME',	# Data di creazione del voto
  'BountyAmount':'INTEGER'		# Taglia associata al post http://meta.stackexchange.com/help/bounty
 },
 'Users': {
  'Id':'INTEGER',				# Id dell'utente, identifica su un sito della rete StackExchange
  'Reputation':'INTEGER',		# Reputazione dell'utente
  'CreationDate':'DATETIME',	# Data di creazione dell'account
  'DisplayName':'TEXT',			# Nome dell'utente
  'LastAccessDate':'DATETIME',	# Data ultimo accesso
  'WebsiteUrl':'TEXT',			# URL ad un sito dell'utente
  'Location':'TEXT',			# Luogo 
  'Age':'INTEGER',				# Anni
  'AboutMe':'TEXT',				# Descrizione dell'utente
  'Views':'INTEGER',			# Numero di visualizzazioni del profilo
  'UpVotes':'INTEGER',			# Numero di upvote ricevuti
  'DownVotes':'INTEGER',		# Numero di downvote ricevuti
  'AccountId':'INTEGER',		# Id dell'account, identifica sulla rete StackExchange
  'ProfileImageUrl':'TEXT'		# URL all'immagine di profilo
  #'EmailHash':'TEXT'
  },
}

def dump_files(file_names, anathomy, 
    dump_path='.', 
    dump_database_name = 'so-dump.db',
    create_query='CREATE TABLE IF NOT EXISTS [{table}]({fields})',
    insert_query='INSERT INTO {table} ({columns}) VALUES ({values})',
    log_filename='so-parser.log'):

 logging.basicConfig(filename=os.path.join(dump_path, log_filename),level=logging.INFO)
 db = sqlite3.connect(os.path.join(dump_path, dump_database_name))

 for file in file_names:
  print "Opening {0}.xml".format(file)
  with open(os.path.join(dump_path, file + '.xml')) as xml_file:
   tree = etree.iterparse(xml_file)
   table_name = file

   sql_create = create_query.format(
        table=table_name, 
        fields=", ".join(['{0} {1}'.format(name, type) for name, type in anathomy[table_name].items()]))
   print('Creating table {0}'.format(table_name))

   try:
    logging.info(sql_create)
    db.execute(sql_create)
   except Exception, e:
    logging.warning(e)

   for events, row in tree:
    try:
     logging.debug(row.attrib.keys())

     #db.execute solleva eccezione nella creazione della tabella Users
     db.execute(insert_query.format(
        table=table_name, 
        columns=', '.join(row.attrib.keys()), 
        values=('?, ' * len(row.attrib.keys()))[:-2]),
        row.attrib.values())
     print ".",
    except Exception, e:
     logging.warning(e)
     print "x",
    finally:
     row.clear()
   print "\n"
   db.commit()
   del(tree)

if __name__ == '__main__':
   dump_files(ANATHOMY.keys(), ANATHOMY)
