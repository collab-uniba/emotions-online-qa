from django.shortcuts import render
from django.http import HttpResponse
from django.utils.encoding import smart_str
import os
import sqlite3
import csv

from django.shortcuts import render_to_response, HttpResponse
from django.template import RequestContext



# Nomi database
db_directory = '/mnt/workingdir/emotions-online-qa/site_SE/databases/db/'

# Query
posts_tags_query = "SELECT Id, Tags, PostTypeId FROM Posts"
answers_query = "SELECT Id, Body, CreationDate FROM Posts WHERE PostTypeId = 2 AND creationDate BETWEEN '2014-01-01' AND '2014-01-07'"
questions_query = "SELECT Id, Body, CreationDate FROM Posts WHERE PostTypeId = 1 AND creationDate BETWEEN '2014-01-01' AND '2014-01-07'"
simple_query = "SELECT Id, Body, CreationDate FROM Posts WHERE Id = 4"
most_recent_post_date = "SELECT MAX(CreationDate) FROM Posts ORDER BY CreationDate DESC"
first_post_date = "SELECT MAX(CreationDate) FROM Posts ORDER BY CreationDate DESC"
number_of_users = "SELECT COUNT(Id) from Users"
quest_accepted = "SELECT COUNT(Id) FROM Posts WHERE PostTypeId = 1 AND AcceptedAnswerId IS NOT NULL"
quest_resp_no_accepted = "SELECT COUNT(Id) FROM Posts WHERE PostTypeId = 1 AND AnswerCount > 0 AND AcceptedAnswerId IS NULL"
quest_no_accepted = "SELECT COUNT(Id) FROM Posts WHERE PostTypeId = 1 AND AnswerCount = 0"


all_queries = [{'title':"List of all questions with id, body and creation date", 'quer':answers_query}, 
		{'title':"List of all questions with id, body and creation date", 'quer':questions_query}, 
		{'title':"Post with id 4 with body and creation date", 'quer':simple_query}, 
		{'title':"List of all posts with id, tags and the type", 'quer':posts_tags_query}, 
		{'title':"Date of the most recent post", 'quer':most_recent_post_date}, 
		{'title':"Date of the first post", 'quer':first_post_date}, 
		{'title':"Number of all users", 'quer':number_of_users}, 
		{'title':"Number of questions with an 'accepted' answer", 'quer':quest_accepted}, 
		{'title':"Number of questions with at least one answer but with no 'accepted' answer", 'quer':quest_resp_no_accepted}, 
		{'title':"Number of questions with no 'accepted' answer", 'quer':quest_no_accepted}]

#all_queries = [answers_query, questions_query, simple_query, posts_tags_query, most_recent_post_date, first_post_date, number_of_users, quest_accepted, quest_resp_no_accepted, quest_no_accepted]


# Create your views here.

def databases(request):
	#curr_dir = os.getcwd()
	#dbs = os.listdir(curr_dir + '/' + db_directory)
	dbs = os.listdir(db_directory)
	page_title = "Databases"
	return render(request, 'index.html', {'page_title': page_title, 'dbs': dbs})

def queries(request, db):
	page_title = "Query List"
	return render(request, 'queries.html', {'page_title': page_title, 'all_queries': all_queries, 'db': db})


def process_req(request, db, query):
	result_set = execute_query(db, query)
	resp_csv = download_csv(request, result_set)
	return resp_csv
	
def execute_query(db, query):
	path_to_db = db_directory + db
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



#Alec Larsen - University of the Witwatersrand, South Africa, 2012 import shlex, subprocess

def RateSentiment(sentiString):
    #open a subprocess using shlex to get the command line string into the correct args list format
    p = subprocess.Popen(shlex.split("java -jar SentiStrength.jar stdin sentidata C:/SentStrength_Data/"),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    #communicate via stdin the string to be rated. Note that all spaces are replaced with +
    stdout_text, stderr_text = p.communicate(sentiString.replace(" ","+"))
    #remove the tab spacing between the positive and negative ratings. e.g. 1    -5 -> 1-5
    stdout_text = stdout_text.rstrip().replace("\t","")
    return stdout_text
