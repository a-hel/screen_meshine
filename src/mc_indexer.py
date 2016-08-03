"""
Scan text files for occurences of relevant terms

Andreas Helfenstein 2016
"""
#from collections import defaultdict
import re
import xml.etree.cElementTree as ET

import mc_tree



def _walkthrough(index, post, sep="|"):
	words = re.compile("\w+").findall(post)
	word_nodes = [mc_tree.walk(index, word) for word in words]
	idx = [word_node.endvalue for word_node in word_nodes if word_node]
	clean_idx = list(set([elem for elem in idx if elem]))
	return clean_idx



def _find_concepts(sourcefile):
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
	basenode = mc_tree.Node("basenode")
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
	indexed_list = [_walkthrough(index, post) for post in posts]
	return indexed_list


if __name__ == '__main__':
	pass
	