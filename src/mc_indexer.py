"""
Scan text files for occurences of relevant terms

Andreas Helfenstein 2016
"""
from collections import defaultdict
import os
import multiprocessing
from functools import partial

import mc_scraper


def build_dict(path):
	source = _get_thesaurus()
	target = path
	sep = "|"
	cui_pos = 0
	term_pos = 14
	source_pos = 11

	with open(source, "r") as s, open(target, "w") as t:
		for line in s:
			l = line.split(sep)
			if not l[source_pos] in ["MSH", "SNOMEDCT"]:
				continue
			t.write(l[cui_pos] + sep + l[term_pos] + "\n")
	return True

def _get_thesaurus(thesaurus="../MRCONSO.RRF"):
	"""Return location of thesaurus file
	"""

	return thesaurus

def _get_term_source(dictionary="../DICT.txt"):
	"""Return location of term lookup file
	"""

	if not os.path.isfile(dictionary):
		build_dict(dictionary)
	return dictionary

def get_lookup_table(sep="|"):
	"""Read lookup file and return as dict.
	Aruguments:
	sep (str, default=","): Separator used in lookup file
	Returns:
	dict {code: term}
	"""

	f_source = _get_term_source()
	with open(f_source, "r") as f:
		pairs = [l.split(sep) for l in f]
	lookup = {cui.strip(): term.strip() for (cui, term) in pairs}
	#lookup = defaultdict(lambda: "undef", lookup)
	lookup = defaultdict(lambda: "nd", lookup)
	return lookup

def cui_to_terms(cui_list):
	"""Replace CUI with corresponding terms
	Arguments:
	cui_list (2-D iterable): List of list, where the outer list are the 
	blog posts and the inner the CUI's appearing in this post.
	Returns:
	List of list of the same dimensions as cui_list, with cui's replaced
	by the corresponding terms.

	"""

	lookup = get_lookup_table()
	term_list = [[lookup[cui] for cui in post if cui != "nd"] for post in cui_list]
	return term_list

def find_terms(thes_dict, post):
	"""Find a term in a list of blog posts
	Arguments:
	search_term (str): The term to look for
	posts (list of str): The blog posts to crawl
	Returns:
	List of the indices of the posts that contain search_term.
	"""

	ret_val = [thes_dict[keys] for keys in thes_dict if keys in post]	
	return ret_val

def load_thesaurus(thesaurus, sep="|", pos=14, max_steps="*"):
	thes_dict = {}
	with open(thesaurus, "r") as thes:
		for e, line in enumerate(thes):
			if e > max_steps:
				break
			splitted = line.split(sep)
			search_term = splitted[pos].strip()
			if len(search_term) <= 4:
				continue
				# check idea behind "weird" terms such as "m", "Dip", 2
				# Then make better workaround

			cui = splitted[0].strip()
			thes_dict[search_term] = cui
	print("Thesaurus loaded")
	return thes_dict

def cross_find(thes_dict, posts):
	p = multiprocessing.Pool()
	func = partial(find_terms, thes_dict)
	found_terms = p.imap(func, posts)
	p.close()
	p.join()
	return found_terms


def walkthrough(thes_dict, posts, sep="|", pos=14, max_steps="*"):
	"""Walk through thesaurus file and return CUI's found in posts
	Arguments:
	thesaurus (str): Location of thesaurus file
	posts (list of str): The posts to analyze
	sep (str, default="|"): Separator in thesaurus file
	pos (int, default=14): Index of term in thesaurus file
	max_steps (int or str, default="*"): Number of lines to read from
		thesaurus, if str, the whole file will be read (debugging only)
	Returns:
	List of lists, with the outer list being of same length as posts
		and the inner list contains the CUI's found in the respective
		post.
	"""

	
	n_posts = len(posts)
	print("Analysis of %s posts." % n_posts)
	term_list = cross_find(thes_dict, posts)
	cui_list = [list(set(sublist)) for sublist in term_list]
	return cui_list

def _retrieve(keywords, n_posts, plugins, chunk_size=4):
	"""Retrieve posts chunkwise"""

	params = {"tags": keywords, "n_posts": n_posts, "plugins": plugins}
	post_list = [[]] * chunk_size
	for i, post in enumerate(mc_scraper.main(**params)):
		print("Getting data: Chunk %s" % i)
		idx = i%chunk_size
		post_list[idx] = post
		if idx == chunk_size-1:
			yield post_list
	yield post_list[0:idx]

def main(tags, size, plugins):
	"""Scan posts for occurences of relevant terms.
	Arguments:
	posts (list of str): Posts or pieces of text to analyse, as
		pure ascii
	Returns:
	List of list with the terms found in each post.
	"""
	thes_dict = load_thesaurus(_get_thesaurus())
	for chunk in _retrieve(tags, size, plugins=plugins):
		cui_list = walkthrough(thes_dict, chunk, max_steps="*")
		terms = cui_to_terms(cui_list)
		#_save(project_dir, indexed_list)
	return terms

if __name__ == '__main__':
	pass
	