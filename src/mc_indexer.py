"""
Scan text files for occurences of relevant terms

Andreas Helfenstein 2016
"""
from collections import defaultdict

def _get_thesaurus():
	"""Return location of thesaurus file
	"""

	return "../MRCONSO.RRF"

def _get_term_source():
	"""Return location of term lookup file
	"""

	#return "../MRXNS_ENG.RRF"
	return "../dummy.txt"

def get_lookup_table(sep=","):
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
	lookup = defaultdict(lambda: "undef", lookup)
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
	term_list = [[lookup[cui] for cui in post] for post in cui_list]
	return term_list

def find_terms(search_term, posts):
	"""Find a term in a list of blog posts
	Arguments:
	search_term (str): The term to look for
	posts (list of str): The blog posts to crawl
	Returns:
	List of the indices of the posts that contain search_term.
	"""

	ret_val = []
	for e, post in enumerate(posts):
		if search_term in post:
			ret_val.append(e)
	return ret_val

def walkthrough(thesaurus, posts, sep="|", pos=14, max_steps="*"):
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
	term_list = [[] for _ in range(len(posts))]
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
			occurences = find_terms(search_term, posts)
			for occurence in occurences:
				term_list[occurence].append(cui)
	cui_list = [list(set(sublist)) for sublist in term_list]
	return cui_list

def main(posts):
	"""Scan posts for occurences of relevant terms.
	Arguments:
	posts (list of str): Posts or pieces of text to analyse, as
		pure ascii
	Returns:
	List of list with the terms found in each post.
	"""

	cui_list = walkthrough(_get_thesaurus(), posts, max_steps="*")
	terms = cui_to_terms(cui_list)
	return terms

if __name__ == '__main__':
	pass
	