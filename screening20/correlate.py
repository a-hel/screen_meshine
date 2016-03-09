#!usr/bin/python

import numpy as np
import scipy
from collections import defaultdict
import itertools
import networkx as nx
import matplotlib.pyplot as plt

corr_map = defaultdict(dict)
categories = defaultdict()
cat_file = "categories.csv"

def color_by_cat(mappings, all_terms):
    colors = {'A': 'red',
        'B': 'blue',
        'C': 'green',
        'D': 'orange',
        'E': 'yellow',
        'F': 'black',
        'G': 'white'}

def generate_edges(col, graph):
    start = col.name
    print start
    for end, weight in col.iteritems():
        if weight:
            graph.add_edge(start, end, attr_dict={'weight':weight})
    return col

def _is_in_cat(cat, all_cats):
    if not all_cats:
        return True
    for single_cat in all_cats:
        if cat.startswith(single_cat):
            return True
    return False

def _filter_terms(res_file, cat_file, categories):
    """return results from res_file that fall into categories."""

    with open(cat_file, 'r') as cf:
        cf_pairs = [line.split(',') for line in cf if line != '\n']
        cat_table = {term.strip(): code.strip() for term, code in cf_pairs}

    with open(res_file, 'r') as rf:
        rf_pairs = [line.split(',') for line in rf if line != '\n']
        filtered_res = [[term.strip() for term in terms if
            _is_in_cat(cat_table[term.strip()], categories)] for terms in rf_pairs]

    return filtered_res, cat_table

def build_matrix(res_file, cat_file, categories=[]):
    """Build sparse x*x matrix for correlation"""

    active_terms, cat_table = _filter_terms(res_file, cat_file, categories)
    active_terms_flat = itertools.chain.from_iterable(active_terms) 
    active_set = list(set(active_terms_flat))
    dim = len(active_set)
    lookup = {term: idx for idx, term in enumerate(active_set)}
    rev_lookup = {idx: term for idx, term in enumerate(active_set)}
    corr_map = scipy.sparse.dok_matrix((dim, dim), dtype=np.int)

    for active_terms_line in active_terms:
        combs = itertools.combinations(active_terms_line, 2)
        for x,y in combs:
            corr_map[lookup[x], lookup[y]] += 1
    mappings = {'lookup': lookup, 'rev_lookup': rev_lookup, 'cat_table': cat_table}
    corr_map = corr_map + corr_map.transpose()
    return corr_map, mappings

def create_plot(corr_map, mappings, minweight=1):

    node_scale = 1
    node_sums = corr_map.sum(axis=0).tolist()[0]


    all_terms = mappings['lookup'].values()

    edgewidth = []
    nodeprops = []
    #G=nx.random_geometric_graph(200,0.125)
    G = nx.MultiGraph()

    corr_map_coo = corr_map.tocoo()
    max_correlations = corr_map_coo.max(axis=0).toarray()[0]
    node_sums = corr_map_coo.sum(axis=0).tolist()[0]

    for i, max_ in enumerate(max_correlations):
        if max_ >= minweight:
            G.add_node(i)
            n_color = 'green'
            n_size =  node_sums[i]*node_scale
            n_label = mappings['rev_lookup'][i]
            nodeprops.append([n_color, n_size, n_label, i])
            #nodelabels.append(mappings['rev_lookup'][i])
    nodecolor, nodesize, nodelabels, idx = zip(*nodeprops)

    for item in corr_map.items():
        start, end = item[0]
        weight = item[1]
        if weight >= minweight:
            print "Drawing edge: %s -> %s (Weight: %s)" % (mappings['rev_lookup'][start],
                    mappings['rev_lookup'][end], weight)
            edgewidth.append(weight)
            G.add_edge(start, end)

    edgewidth = np.array(edgewidth, dtype='uint8')
    edgewidth = np.around(np.log(edgewidth))

    nodesize = np.array(nodesize, dtype='uint8')*4
    nodelabels_dict = {idx[i]: lbl for i, lbl in enumerate(nodelabels)}

    # position is stored as node attribute data for random_geometric_graph
    #pos=nx.get_node_attributes(G,'pos')


    plt.figure(figsize=(50,50))
    #pos = nx.spring_layout(G)
    pos = nx.circular_layout(G)

    nx.draw_networkx_labels(G, pos, labels=nodelabels_dict, fontsize=12)
    nx.draw_networkx_edges(G,pos, alpha=0.6, width=edgewidth, edge_color='grey')
    nx.draw_networkx_nodes(G,pos, node_size=nodesize, node_color=nodecolor, alpha=0.6)

    #plt.xlim(-0.05,1.05)
    #plt.ylim(-0.05,1.05)
    plt.axis('off')
    return plt

if __name__ == '__main__':
    categories = ('A', # Anatomy
        'C', # Diseases
        'B', # Organsims
        'R', # Pharmacological actions
        'J') # Technology, food, beverages
    corr_map, mappings = build_matrix('../results.txt_clean.txt',
        '../categories.csv', categories=categories)
    plt = create_plot(corr_map, mappings, minweight=20)
    plt.show()
#    print corr_map.todense()

def blah():
    plt.savefig('graph.png')
    plt.show()