
#import requests
import json
import re
import sys
import os
import grequests
import requests
import itertools as itt

from bs4 import BeautifulSoup


def _decompile_terms(response):
    """Find mesh terms from raw html using regexp"""
    
    exp = '(?<=term=)[\w ]*(?=" target)'
    res = re.findall(exp, response)
    term_list = list(set(res))
    return term_list

def _get_mesh_terms_s(raw_text):
    """extract mesh terms from raw_text"""
    print(raw_text)
    mesh_url = r"http://ii.nlm.nih.gov/cgi-bin/II/Interactive/MeSHonDemand.pl"
    rs = requests.post(mesh_url, data=raw_text[0])
    
    print(rs.text)
    with open('blah.html', 'w') as f:
    	f.write(rs.text)
    terms = [_decompile_terms(r) for r in response_encoded]
    print(terms)
    return terms

def _get_categories(queries, idx=0):
    db = "mesh"
    stem_url = r"http://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    mesh_db = stem_url + "esearch.fcgi?db=%s&term=%s&retmode=json"
    record_db = stem_url + "esummary.fcgi?db=%s&id=%s&retmode=json"
    #filter out bad queries
    rs = [grequests.get(mesh_db % (db, query)) for query in queries]
    records = grequests.map(rs)
    records_json = [r.json() for r in records]#.text.encode('utf-8')
    mesh_ids = [r['esearchresult']['idlist'][idx] for r in records_json
    	if not r['esearchresult'].has_key('ERROR')]
    rs2 = [grequests.get(record_db % (db, mesh_id)) for mesh_id in mesh_ids]
    records2 = grequests.map(rs2)
    records2_json = [r.json() for r in records2]
    treenums = [r['result'][mesh_id]['ds_idxlinks'][idx]['treenum'] for
    	(r, mesh_id) in zip(records2_json, mesh_ids)]
    meshterms = [r['result'][mesh_id]['ds_meshterms'][idx] for 
    	(r, mesh_id) in zip(records2_json, mesh_ids)]
    return (meshterms, treenums)

def clean(sourcefile, include_categories=[]):
	delim = ','
	max_requests = 10
	targetfile = sourcefile[0:sourcefile.rfind('.')] + '_clean.txt'
	with open(sourcefile, 'r') as sf:
		sourceterms = [line.split(delim) for line in sf if not line.startswith('#')]
	sourcelist = [elem.strip() for elem in itt.chain(*sourceterms)]
	sourceset = list(set(sourcelist))
	#sourceset = sourceset[0:20]
	cycles = int(len(sourceset)/max_requests)
	terms = []
	cats = []
	for i in range(cycles):
		start_idx = i * max_requests
		end_idx = start_idx + max_requests
		print("Retrieving %2.d %% " % (i/float(cycles)*100))
		_terms, _cats = _get_categories(sourceset[start_idx:end_idx])
		terms.extend(_terms)
		cats.extend(_cats)


	with open(targetfile, 'a', buffering=100) as tf:
		for pair in zip(terms,cats):
			#insert category check
			tf.write("; ".join(pair))
			tf.write("\n")
	return targetfile

def _get_mesh_terms(raw_text):
    """extract mesh terms from raw_text"""
    text_rq = [{'InputText': raw} for raw in raw_text]
    mesh_url = r"http://ii.nlm.nih.gov/cgi-bin/II/Interactive/MeSHonDemand.pl"
    rs = [grequests.post(mesh_url, data=tr) for tr in text_rq]
    responses = grequests.map(rs)
    response_encoded = [r.text.encode('utf-8') for r in responses]
    print(response_encoded)
    with open('blah.html', 'w') as f:
    	f.write(response_encoded[1])
    terms = [_decompile_terms(r) for r in response_encoded]
    print(terms)
    return terms




def save_mesh(mesh_terms, fname, buf=1):
	with open(fname, 'a+', buffering=buf) as f:
		f.write("# Automated saving after cycle %s \n" % i)
		for line in mesh_terms:
			f.write(", ".join(line))
			f.write("\n")
	return True

def _import_plugins(names=False, pluginpath='./plugins/'):

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

	

def main(tags, n_posts, plugins=('wp'), target="new_project", buf=100,
	chunk_size=2):
	engines = _import_plugins(plugins)
	indic_len = 10000
	l_counter = 0
	f_counter = 1
	f_list = []
	text_list = []

	for engine in engines:
		# Plug-ins recieve the number of posts to return and 
		# yield chuncks of posts
		
		#text_chunk = [[]] * chunk_size

		for e, txt in enumerate(engine.main(tags, n_posts)):
			l_counter += len(txt)
			text_list.append(txt)
			if l_counter >= indic_len:
				fname = "res_%s.txt" % f_counter
				with open(target + os.sep + fname, "w") as f:
					f.write("\n".join(text_list))
					f_list.append(fname)
				l_counter = 0
				f_counter += 1
				text_list = []
	return f_list
			



if __name__ == "__main__":
	i = 1
	n = len(sys.argv)
	size = 0
	tags = []
	to = './'
	fname = 'results'
	plugins = []
	helptext = "This is the help"
	while i < n:
		arg = sys.argv[i]
		if arg.startswith('-'):
			if arg in ('-h', '--help'):
				print(helptext)
				break
			if arg in ('-to', '--to'):
				i += 1
				to = sys.argv[i]
			if arg in ('-f', '--filename'):
				i += 1
				fname = sys.argv[i]
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
	#cleaned = clean('results.txt')

	#main(['medicine', 'nature', 'cure', 'plants',
	#	'herbal+remedy', 'traditional+remedy',], 1000, fname="results_2.txt")

	#main(['bacteria', 'virus', 'infection', 'antibiotic',
	#	'natural+remedy', 'medicinal+plants', 'home+remedy', ], 10000,
	#	fname="result-big.txt")
