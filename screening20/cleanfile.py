#!usr/bin/python

import requests
from collections import defaultdict

include_categories = ['A', 'B', 'C', 'D', 'E']
include_depth = len(include_categories[0])
cat_file = "../categories.csv"
res_file = "../results.txt"
categories = defaultdict()
new_lines = []

def find_category(query, idx=0):
    db = "mesh"
    stem_url = r"http://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    mesh_db = stem_url + "esearch.fcgi?db=%s&term=%s&retmode=json"
    record_db = stem_url + "esummary.fcgi?db=%s&id=%s&retmode=json"
    record_list = requests.get(mesh_db % (db, query)).json()
    try:
        mesh_id = record_list['esearchresult']['idlist'][idx]
    except KeyError:
        print record_list
    record_data = requests.get(record_db % (db, mesh_id)).json()
    treenum = record_data['result'][mesh_id]['ds_idxlinks'][idx]['treenum']
    meshterm = record_data['result'][mesh_id]['ds_meshterms'][idx]
    return (meshterm, treenum)

#http://eutils.ncbi.nlm.nih.gov/entrez/eutils/

try:
    with open(cat_file, 'r') as f:
        for line in f:

    #    lines = f.readlines()
    #for line in lines:
            term, cat = line.rstrip('\n').split(',')
            categories[term] = cat
except IOError:
    pass
    
with open(res_file, 'r') as f:
#    lines = f.readlines()
#for line in lines:
    for line in f:
        if line.startswith('#'):
            continue
        if line == '\n':
            continue
        new_line = []
        term_list = line.rstrip('\n').split(',')
        for term in term_list:
            print term
            if term in categories.keys():
                cat = categories[term]
            else:
                try:
                    t, cat = find_category(term)
                except requests.ConnectionError:
                    cat = None
                categories[term] = cat
            if cat[0:include_depth] in include_categories:
                new_line.append(term)
        new_lines.append(new_line)
    
with open(res_file + '_clean.txt', 'w') as f:
    for l1 in new_lines:
        f.write(','.join(l1))
        f.write('\n')
        
with open(cat_file, 'a') as f:
    for key in categories:
        f.write('%s,%s\n' % (key, categories[key]))

            