"""
MedCrawler

Scraping engine to retrieve and handle posts and interface
to plugins.

Andreas Helfenstein 2016
"""

import sys
import os
import requests

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
	"""Convert html to ascii-only text"""

	no_html = _remove_html(post)
	compact = _get_compact_ascii(no_html)
	return compact

def _import_plugins(names=False, pluginpath='./plugins/'):
	"""Load plugins"""

	all_plugins = []
	sys.path.append(pluginpath)
	if not names:
		names = [d[0:-3] for d in os.listdir(pluginpath) if d.endswith('.py')]
	for name in names:
		try:
			plugin = __import__(name, fromlist=['main',])
			# add check for necessary functions
			all_plugins.append(plugin)
		except Exception, e:
			print('!! Could not load plugin %s:\n!! %s' % (name, e))
	return all_plugins

	

def main(tags, n_posts, plugins=('wp'), target="new_project"):
	"""Retrieve blog posts.
	Arguments:
	tags (list of str): Keywords to look for
	n_posts (int): Number of posts to retrieve per keyword and plugin
	plugins (list of str): Plugins to include. Plugins must be saved
		in the 'plugins' folder under <plugin_name>.py
	target (str): Project name
	Yields:
	Posts as pure ascii text
	"""

	engines = _import_plugins(plugins)
	f_counter = 0
	f_list = []
	text_list = []

	for engine in engines:
		# Plug-ins recieve the number of posts to return and 
		# yield chuncks of posts

		for txt in engine.main(tags, n_posts):
			cleantxt = _clean_post(txt)
			yield cleantxt
			

if __name__ == "__main__":
	i = 1
	n = len(sys.argv)
	size = 0
	tags = []
	to = './'
	plugins = []
	while i < n:
		arg = sys.argv[i]
		if arg.startswith('-'):
			if arg in ('-h', '--help'):
				print(helptext)
				break
			if arg in ('-pr', '--project'):
				i += 1
				to = sys.argv[i]
			if arg in ('-p', '--plugins'):
				i += 1
				plugins = sys.argv[i].split(',')
		elif arg.isdigit():
			size = int(arg)
		elif type(arg) == str:
			tags.append(arg)
		i += 1

	main(tags, size, plugins=plugins, 
		target=to)
	sys.exit(0)

