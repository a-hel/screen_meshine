"""
Scan text files for occurences of relevant terms

Andreas Helfenstein 2016
"""
#from collections import defaultdict
import re
import xml.etree.cElementTree as ET

import mc_tree



def _walkthrough(index, post, sep="|"):
	""" Return words in post that are in index """

	words = re.compile("\w+").findall(post)
	word_nodes = [mc_tree.walk(index, word) for word in words]
	idx = [word_node.endvalue for word_node in word_nodes if word_node]
	clean_idx = list(set([elem for elem in idx if elem]))
	return clean_idx



def _find_concepts(sourcefile):
	""" Extract MeSH terms, synonyms and treenode from MeSH xml descriptor """

	e = ET.parse(sourcefile).getroot()
	for descriptor in e.iter("DescriptorRecord"):
		name = descriptor.find("DescriptorName").find("String").text
		try:
			leaf = descriptor.find("TreeNumberList").find("TreeNumber").text
		except AttributeError:
			print("No tree number found for '%s'" % name)
			continue
		synelem = descriptor.find("ConceptList").find("Concept").find("TermList")
		synterms = synelem.findall("Term")
		synonyms = [syn.find("String").text for syn in synterms]
		yield (name, leaf, synonyms)

def build_index(sourcefile):
	""" Build index based on sourcefile.

	Argument:

	sourcefile (str): Path and file name of the MeSH database (e.g. 
		desc2016.xml)
	basenode = mc_tree.Node("basenode")

	Returns:

	mc_tree.Node
	"""

	i = 0
	for name, leaf, synonyms in _find_concepts(sourcefile):
		rightmosts = [mc_tree.build(basenode, synonym) for synonym in synonyms]
		for rightmost in rightmosts:
			rightmost.endvalue = (name, leaf)
		if i%1000 == 0:
			print("%s \t %s" % (i, name))
		i += 1
	print("Index built")
	return basenode

def traverse(index, posts):
	""" Find indexed words from posts

	Arguments:

	index (mc_tree.Node): The tree node from where to start the search
	posts (list of str): List of all the posts in pure ASCII

	Returns:

	List of tuples (found terms, tree number)
	"""
	
	indexed_list = [_walkthrough(index, post) for post in posts]
	return indexed_list


if __name__ == '__main__':
	pass
	