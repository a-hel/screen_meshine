
import requests
import json
from bs4 import BeautifulSoup



def get_post_content(tag, number, page=1):
	base_url = 'https://public-api.wordpress.com/rest/v1.1/read/tags/%s/posts?number=%s&page=%s' % (tag, number, page)
	try:
		response = requests.get(base_url)
	except requests.ConnectionError, e:
		print("Could not connect to server.\n[ %s ]" % e)
		return False
	json_response = json.loads(response.text)
	for post in json_response['posts']:
		html = post['content']
		yield html

def _get_html(request_url):
	response = requests.get(request_url)
	json_response = json.loads(response.text)
	for post in json_response['posts']:
		html = post['content']
		yield html

def _dispatch(tags, size):
	print tags
	chunk_size = min(size, 40)
	cycles = int((size-1)/chunk_size)+1
	#ppp = size % chunk_size
	ppp = chunk_size
	for tag in tags:
		print tag
		for i in xrange(cycles):
			print("WP plugin loading posts for '%s', cycle %s of %s" % (tag, i+1, cycles))
			for post in get_post_content(tag, ppp, page=i+1):
				#plain_text = _clean_post(post)
				#yield plain_text
				yield post

def main(tags, size=1):
	print tags
	for plain_text in _dispatch(tags, size):
		yield plain_text

