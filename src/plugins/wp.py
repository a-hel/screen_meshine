
import requests
import json
from bs4 import BeautifulSoup

def _remove_html(html):
    """Return MeSH terms from url"""

    naked_body = BeautifulSoup(html, 'html.parser').get_text()
    naked_body_encoded =  naked_body.encode('utf-8')
    return naked_body_encoded

def _get_compact_ascii(plain_text):
	"""Remove non-ascii characters and double newlines"""
	no_ascii = plain_text.decode('utf-8').encode('ascii', errors='ignore')
	#Replacement with withespace in case of four consecutive newlines
	no_nl = no_ascii.replace('\n', ' ')
	return no_nl


def _clean_post(post):

	no_html = _remove_html(post)
	compact = _get_compact_ascii(no_html)
	return compact

def get_post_content(tag, number, page=1):

	base_url = 'https://public-api.wordpress.com/rest/v1.1/read/tags/%s/posts?number=%s&page=%s' % (tag, number, page)
	response = requests.get(base_url)
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
	chunk_size = min(size, 40)
	cycles = int(size/chunk_size)#+1
	ppp = size % chunk_size
	for tag in tags:
		for i in xrange(cycles):
			print("Tag: %s, cycle %s of %s" % (tag, i+1, cycles))
			for post in get_post_content(tag, ppp, page=i+1):
				plain_text = _clean_post(post)
				yield plain_text

def main(tags, size=1):

	for plain_text in _dispatch(tags, size):
		yield plain_text

