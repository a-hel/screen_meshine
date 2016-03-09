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
color_by_cat = {'A': 'red',
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
        cf_pairs = [line.split(',') for line in cf]
        cat_table = {term.strip(): code.strip() for term, code in cf_pairs}

    with open(res_file, 'r') as rf:
        rf_pairs = [line.split(',') for line in rf]
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
    mappings = {'lookup': lookup, 'rev_lookup': rev_lookup, 'cat_table': cat_table}
    return corr_map, mappings

def create_plot(corr_map, mappings, minweight=1):

    all_terms = lookup.values()
    #G=nx.random_geometric_graph(200,0.125)
    G = nx.MultiGraph()
    for i in all_terms:
        G.add_node(i)
    for item in corr_map.items():
        start, end = item[0]
        weight = item[1]
        if weight >= minweight:
            G.add_edge(start, end, attr_dict={'weight':weight})
#    colorscheme = [color_by_cat[categories[t][0:1]] for t in all_terms]
#    print colorscheme


    # position is stored as node attribute data for random_geometric_graph
    #pos=nx.get_node_attributes(G,'pos')

    # find node near center (0.5,0.5)
    #dmin=1
    #ncenter=0
    #for n in pos:
    #    x,y=pos[n]
    #    d=(x-0.5)**2+(y-0.5)**2
    #    if d<dmin:
    #        ncenter=n
    #        dmin=d

    # color by path length from node near center
    #p=nx.single_source_shortest_path_length(G,ncenter)

    plt.figure(figsize=(8,8))
    node_labels = {i: mappings[rev_lookup][i] for i in all_terms}
    pos = nx.spring_layout(G)
    nx.draw_networkx_labels(G, pos, labels=node_labels)
    #nx.draw(G, pos)

    nx.draw_networkx_edges(G,pos,alpha=0.4)
    nx.draw_networkx_nodes(G,pos,
                           node_size=80,
                           #node_color=colorscheme,
                           cmap=plt.cm.Reds_r)

    #plt.xlim(-0.05,1.05)
    #plt.ylim(-0.05,1.05)
    plt.axis('off')
    return plt

if __name__ == '__main__':
    categories = ('A', 'B')
    corr_map, mappings = build_matrix('resfile_n.txt',
        'categories.csv', categories=categories)
    plt = create_plot(corr_map, mappings)
    plt.show()
#    print corr_map.todense()

def blah():
    plt.savefig('graph.png')
    plt.show()