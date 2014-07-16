from django.shortcuts import render
from django.http import HttpResponse
from django.utils.encoding import smart_str
import os
import sqlite3
import csv

from django.shortcuts import render_to_response, HttpResponse
from django.template import RequestContext



# Nomi database
stackoverflow = 'stackoverflow.db'
italian = 'italian.stackexchange.dump.db'
academia = 'academia.dump.db'
db_directory = '/mnt/workingdir/emotions-online-qa/site_SE/databases/db/'

# Query
posts_tags_query = "SELECT Id, Tags, PostTypeId FROM Posts"
answers_query = "SELECT Id AS PostId, Title, Body, Tags, CreationDate AS PostCreationDate, OwnerUserId AS UserId, AcceptedAnswerId AS PostAcceptedAnswerId FROM Posts WHERE Posts.PostTypeId = 2"
questions_query = "SELECT Id AS PostId, Title, Body, Tags, CreationDate AS PostCreationDate, OwnerUserId AS UserId, AcceptedAnswerId AS PostAcceptedAnswerId FROM Posts WHERE Posts.PostTypeId = 1 AND Posts.OwnerUserId IS NOT NULL"
simple_query = "SELECT Id, Body, CreationDate FROM Posts WHERE Id = 4"
most_recent_post_date = "SELECT MAX(CreationDate) FROM Posts ORDER BY CreationDate DESC"
first_post_date = "SELECT MIN(CreationDate) FROM Posts ORDER BY CreationDate DESC"
number_of_users = "SELECT COUNT(Id) from Users"
quest_accepted = "SELECT COUNT(Id) FROM Posts WHERE PostTypeId = 1 AND AcceptedAnswerId IS NOT NULL"
quest_resp_no_accepted = "SELECT COUNT(Id) FROM Posts WHERE PostTypeId = 1 AND AnswerCount > 0 AND AcceptedAnswerId IS NULL"
quest_no_answ = "SELECT COUNT(Id) FROM Posts WHERE PostTypeId = 1 AND AnswerCount = 0"
#users_answ_acc = "SELECT Posts.OwnerUserId AS UserId, count(Post.Id) AS UsersAnswersAccepted FROM Posts INNER JOIN Votes ON Posts.Id = Votes.PostId WHERE Posts.PostTypeId = 2 AND Posts.OwnerUserId = @User AND Votes.CreationDate < @Date AND Votes.VoteTypeId = 1"


all_queries = [{'id':'1','title':"List of all answers with id, body and creation date", 'quer':answers_query}, 
		{'id':'2','title':"List of all questions with id, body and creation date", 'quer':questions_query}, 
		{'id':'3','title':"Post with id 4 with body and creation date", 'quer':simple_query}, 
		{'id':'4','title':"List of all posts with id, tags and the type", 'quer':posts_tags_query}, 
		{'id':'5','title':"Date of the most recent post", 'quer':most_recent_post_date}, 
		{'id':'6','title':"Date of the first post", 'quer':first_post_date}, 
		{'id':'7','title':"Number of all users", 'quer':number_of_users}, 
		{'id':'8','title':"Number of questions with an 'accepted' answer", 'quer':quest_accepted}, 
		{'id':'9','title':"Number of questions with at least one answer but with no 'accepted' answer", 'quer':quest_resp_no_accepted}, 
		{'id':'10','title':"Number of questions with no answer", 'quer':quest_no_answ}]
		#{'id':'11','title':"", 'quer':users_answ_acc}]


dbs = [{'title':"Stackoverflow",'dir':stackoverflow},
	{'title':"Italian",'dir':italian},
	{'title':"Academia",'dir':academia}]


# Create your views here.

def databases(request):
	#curr_dir = os.getcwd()
	#dbs = os.listdir(curr_dir + '/' + db_directory)
	#dbs = os.listdir(db_directory)
	page_title = "Choose a database"
	return render(request, 'index.html', {'page_title': page_title, 'dbs': dbs})

def queries(request, db_title):
	page_title = "Query List"
	return render(request, 'queries.html', {'page_title': page_title, 'all_queries': all_queries, 'db_title': db_title})

def get_query(query_id):
	for q_elem in all_queries:
		if q_elem['id'] == query_id:
			query = q_elem['quer']
	return query

def get_db_dir(db_title):
	for db_elem in dbs:
		if db_elem['title'] == db_title:
			db = db_elem['dir']
	return db

def process_csv(request, db_title, query_id):
	query = get_query(query_id)
	db = get_db_dir(db_title)
	result_set = execute_query(db, query)
	resp_csv = download_csv(request, result_set)
	return resp_csv

def process_vis(request, db_title, query_id):
	query = get_query(query_id)
	db = get_db_dir(db_title)
	page_title = "Result set"
	result_set = execute_query(db, query)
	desc = result_set.description
	fields = []
	for d in desc:
		fields = fields + [d[0]]

	return render(request, 'results.html', {'page_title': page_title, 'result_set': result_set, 'fields': fields, 'db_title': db_title})

def execute_query(db, query):
	#path_to_db = db_directory + db
	path_to_db = os.getcwd() + '/databases/db/' + db
	conn = sqlite3.connect(path_to_db)
	c = conn.cursor()
	result_set = c.execute(query)
	
	return result_set

def download_csv(request, result_set):
	resp = HttpResponse(content_type='text/csv')
	resp['Content-Disposition'] = 'attachment; filename="result-set.csv"'
	
	writer = csv.writer(resp)
	
	desc = result_set.description # Prende i campi della tabella
	fields = []
	for d in desc:
		fields = fields + [d[0]]

	writer.writerow(fields)

	for row in result_set: # Prende i record della tabella
		row_to_write = []
		for c in row:
			row_to_write = row_to_write + [smart_str(c)]
		writer.writerow(row_to_write)

	return resp
