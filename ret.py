#!/usr/bin/python
import os.path
import httplib, urllib, urllib2, cookielib
import requests
 
def get_tgt(server, username, password):
	params ={
		"username": username,
		"password": password
		}
	response = requests.post(server, data=params)
	location = response.headers['location']
	tgt = location[location.rfind('/') + 1:]
	#requests.delete(server)
	return tgt

def get_st(server, tgt, service):
	params = {
		"service": service
		}
	response = requests.post(server + '/' + tgt, data=params)
	return response.text, response.cookies

def get_document(service, ticket):
	response = requests.get(service + "?ticket=" + ticket)
	return response.text

def get_ticket(server, username, password, service):
	if not all([server, username, password, service]):
		5/0
	return get_st(server, get_tgt(server, username, password), service)

def main(username='ahelfens', password='Geni1291'):
	server = "https://utslogin.nlm.nih.gov/cas/v1/tickets";
	service = "http://wsd.nlm.nih.gov/Restricted/Non-Reviewed_Results/index.shtml"
	ticket = get_ticket(server, username, password, service)
	document = get_document(service, ticket)
	return document

def handle_submission():
	server = "https://utslogin.nlm.nih.gov/cas/v1/tickets" #casAuthServer = ""
	username = 'ahelfens'
	password = 'Geni1291'
	service = "http://skr.nlm.nih.gov/cgi-bin/SKR/Restricted_CAS/API_batchValidationII.pl"#this.privService
	serviceTicket, cookie = get_ticket(server, username, password, service)
	response = requests.get("http://utslogin.nlm.nih.gov/cas/serviceValidate?ticket=" + serviceTicket)#, "service": "http://umlsks.nlm.nih.gov"})
	print response
	print cookie
	5/0
	ticketTimeStamp = 0
	params = {
		#'service': service,
		#'username': 'ahelfens',
		#'password': 'Geni1291',
		'RUN_PROG': 'MTI',
		'SKR_API': "true",
		'Batch_Command': 'MTI -opt1L_DCMS -E',
		'Email_Address': 'andreas.helfenstein@helsinki.fi',
		'Batch_Env': '',
		'BatchNotes': 'SKR Web API test',
		'SilentEmail': "false",
		'REMOTE_USER': "ahelfens",
		'RPriority': '0',
		#'Filtering': 'Special_Output',
		'UpLoad_File': open('sample.txt', 'rb')
		}
	#files = {'UpLoad_File': open('res_1.txt', 'r'),
	#	'Email_Address': (None,'andreas.helfenstein@helsinki.fi')} #formMap
	files = {'UpLoad_File': ('sample.txt', open('sample.txt', 'rb'), 'text/plain', {'Expires': '0'})}
	print(service + "?ticket=" + serviceTicket)
	response = requests.post(service + "?ticket=" + serviceTicket,
		#files=files,
		params=params, 
		cookies=cookie)
	print response.status
	return response


if __name__ == "__main__":
  	response = handle_submission()
  	print response.text
  	print response.headers
