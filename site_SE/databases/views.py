from django.shortcuts import render
from django.http import HttpResponse
from django.utils.encoding import smart_str
import os
import sqlite3
import csv

from django.shortcuts import render_to_response, HttpResponse
from django.template import RequestContext



# Nomi database
db_directory = 'databases/db/'

# Query
posts_tags_query = "SELECT Id, Tags FROM Posts"
answers_query = "SELECT Id, Body, CreationDate FROM Posts WHERE PostTypeId = 2 AND creationDate BETWEEN '2014-01-01' AND '2014-01-07'"
questions_query = "SELECT Id, Body, CreationDate FROM Posts WHERE PostTypeId = 1 AND creationDate BETWEEN '2014-01-01' AND '2014-01-07'"
simple_query = "SELECT Id, Body, CreationDate FROM Posts WHERE Id = 4"

all_queries = [answers_query, questions_query, simple_query, posts_tags_query]


# Create your views here.

def databases(request):
	curr_dir = os.getcwd()
	dbs = os.listdir(curr_dir + '/' + db_directory)
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
