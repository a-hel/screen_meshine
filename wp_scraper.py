A
B
B
B
B
D
C
A
B

import requests
import json
import re

from bs4 import BeautifulSoup


def _decompile_terms(response):
    """Find mesh terms from raw html using regexp"""
    
    exp = '(?<=term=)[\w ]*(?=" target)'
    res = re.findall(exp, response)
    term_list = list(set(res))
    return term_list

def _get_mesh_terms(raw_text):
    """extract mesh terms from raw_text"""
    
    mesh_url = r"http://ii.nlm.nih.gov/cgi-bin/II/Interactive/MeSHonDemand.pl"
    response = requests.post(mesh_url, data=raw_text)
    response_encoded = response.text.encode('utf-8')
    terms = _decompile_terms(response_encoded)
    return terms


def _remove_html(html):
    """Return MeSH terms from url"""

    naked_body = BeautifulSoup(html, 'html.parser').get_text()
    naked_body_encoded =  naked_body.encode('utf-8')
    return naked_body_encoded


def get_post_content(tag, number, page=1):

	base_url = 'https://public-api.wordpress.com/rest/v1.1/read/tags/%s/posts?number=%s&page=%s' % (tag, number, page)
	response = requests.get(base_url)
	json_response = json.loads(response.text)
	for post in json_response['posts']:
		html = post['content']
		yield html

def save_mesh(mesh_terms, fname, i):
	with open(fname, 'a+') as f:
		f.write("# Automated saving after cycle %s \n" % i)
		for line in mesh_terms:
			f.write(", ".join(line))
			f.write("\n")

def main(tags, n_posts, fname="results.txt"):

	cycles = int(n_posts/40)+1
	ppp = n_posts%40
	for tag in tags:
		mesh_terms = []
		for i in xrange(cycles):
			print "Tag: %s, cycle %s of %s" % (tag, i+1, cycles)
			for post in get_post_content(tag, ppp, page=i+1):
				plain_text = _remove_html(post)
				raw_data = {"InputText": plain_text}
				mesh_terms.append(_get_mesh_terms(raw_data))
			ppp = 40
			if i%10 == 0:
				save_mesh(mesh_terms, fname, i)
				mesh_terms = []
		save_mesh(mesh_terms, fname, tag)



if __name__ == "__main__":
	main(['bacteria', 'virus', 'infection', 'antibiotic',
		'natural cure', 'medicinal plants', 'home remedy', ], 1000)
