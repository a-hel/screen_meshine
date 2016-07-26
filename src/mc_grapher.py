#!usr/bin/python
"""
MedCrawler

Analyze occurrences of terms and plot them in network graph

Andreas Helfenstein 2016
"""

import sys
import os
import numpy as np
import scipy
from collections import defaultdict, Counter
import itertools
import networkx as nx
import matplotlib.pyplot as plt


def _get_colors(cats, col_scheme="default"):
    """Return a list of color codes for given categories, based on the color
    scheme.

    Arguments:

    cats (iterable): The category codes of the terms to be plotted
    col_scheme (str, default="default"): Name of the color scheme.

    Returns:

    List of strings of the same length as cats
    """

    default = {'A': 'red',
        'B': 'blue',
        'C': 'green',
        'D': 'orange',
        'E': 'yellow',
        'F': 'black',
        'G': 'white'}
    default = defaultdict(lambda: 'grey', default)
    all_schemes = {"default": default}
    cur_scheme = all_schemes[col_scheme]
    colors = [cur_scheme[cat[0]] for cat in cats]
    return colors

def _is_in_cat(cat, all_cats):
    """Return True if cat is in all_cats, else False.

    Arguments:

    cat (str): Category code to query
    all_cats (iterable): List of all categories to include. If empty,
        all categories are included.

    Returns:

    bool
    """

    if all_cats == []:
        return True
    for single_cat in all_cats:
        if cat.startswith(single_cat):
            return True
    return False


def _load_dataset(res_file, categories, exclude=[]):
    """Read the extracted MeSH terms into dict.

    Arguments:

    res_file (str): File name and path to load
    categories (list): List of category codes to include in the analysis
    exclde (list, default=[]): List of MeSH terms to exclude from the analysis.

    Returns:

    Dict with post number as keys and a list of tuples (MeSH term, category)
        as values
    """

    posts = []
    with open(res_file, "r") as f:
        for line in f:
            if line.isspace():
                continue
            elif line.startswith('#'):
                continue
            else:
                terms = [term.strip() for term in line.split("|") if not term in exclude]
                posts.append(terms)
    return posts

def _flatten(dataset):
    """Return lists of MeSH terms, category codes, color codes for unique
    MeSH terms.
    Arugments:
    dataset (list of lists): A dataset as output by _load_dataset()
    Returns:
    List of unique terms
    """

    arr = reduce(list.__add__,[elem for elem in dataset])
    uniques = list(set(arr))
    if uniques == []:
        return False
    return uniques

def build_matrix(res_file, categories=[], highlight=False, exclude=[],
    color_scheme="default"):
    """Build sparse x*x matrix to count correlations.

    Arguments:

    res_file (str): File name and path to load
    categories (list, default=[]): List of categories to include
    highlight (str, default=False): MeSH term to highlight
    exclude (list, default=[]): List of MeSH terms to exclude
    color_scheme (str, default="default"): Color scheme for the plot

    Returns:

    Correlation matrix, metadata

    """

    dataset = _load_dataset(res_file, categories, exclude)
    uniques = _flatten(dataset)
    if len(uniques) <= 0:
        msg = "\nWARNING:\n"
        msg += "Your category settings dont yield any results.\n"
        msg += "Try different category settings."
        print(msg)
        sys.exit(0)
    dim = len(uniques)
    lookup = {term: idx for idx, term in enumerate(uniques)}
    corr_map = scipy.sparse.dok_matrix((dim, dim), dtype=np.int)

    for posts in dataset:
        #try:
        #    termline = zip(*dataset[keys])[0]
        #except IndexError:
        #    continue
        if not highlight:
            combs = itertools.combinations(posts, 2)
        else:
            if highlight not in posts:
                continue
            else:
                combs = ((highlight, term) for term in posts 
                        if term != highlight)
        for x,y in combs:
            corr_map[lookup[x], lookup[y]] += 1
    corr_map = corr_map + corr_map.transpose()
    return corr_map, uniques

def create_plot(corr_map, terms, minweight=1, dpi=300):
    """Draw plot and metadata.

    Arguments:

    corr_map (scipy.sparse.dok_matrix): Correlation matrix as returned from
        build_matrix()
    mappings (dict): Correlation metadata as returned from build_matrix()
    minweight (int, default=1): Minimum number of co-occurrences to draw.

    Returns:

    Matplotlib plot, edge metadata
    """

    node_scale = 4
    edge_scale = 1
    node_sums = corr_map.sum(axis=0).tolist()[0]
    edgewidth = []
    nodeprops = []
    lit_edges = []
    G = nx.MultiGraph()
    corr_map_coo = corr_map.tocoo()
    max_correlations = corr_map_coo.max(axis=0).toarray()[0]
    if max(max_correlations) < minweight:
        ctr = Counter(max_correlations)
        msg = "\nWARNING:\n"
        msg += "Your minweight setting (%s) is larger than your " % minweight  +\
            "strongest connection (%s)\n\n" % max(max_correlations)
        msg += "Weight distribution:\n"
        msg += " W \t  n \n"
        msg += "--- \t --- \n"
        for pair in ctr.items():
            msg += "%s \t %s \n" % pair
        print(msg)
        sys.exit(0)
    node_sums = corr_map_coo.sum(axis=0).tolist()[0]
    for i, max_ in enumerate(max_correlations):
        if max_ >= minweight:
            G.add_node(i)
            #n_color = mappings['colors'][i]
            n_color = 'Green'
            n_size =  node_sums[i]*node_scale
            n_label = terms[i]
            nodeprops.append([n_color, n_size, n_label, i])
    if len(nodeprops) == 0:
        msg = "\nERROR:\n"
        msg += "Your current settings do not produce any connections.\n"
        msg += "Try different settings."
        print(msg)
        sys.exit(0)
    nodecolor, nodesize, nodelabels, idx = zip(*nodeprops)
    for item in corr_map.items():
        start, end = item[0]
        weight = item[1]
        if weight >= minweight:
            lit_edges.append((terms[start], terms[end], str(weight)))
            edgewidth.append(weight)
            G.add_edge(start, end)
    edgewidth = np.array(edgewidth, dtype='uint8')
    edgewidth = np.around(np.log(edgewidth))*edge_scale
    nodesize = np.array(nodesize, dtype='uint8')*node_scale
    nodelabels_dict = {idx[i]: lbl for i, lbl in enumerate(nodelabels)}
    plt.figure(figsize=(20,20), facecolor="white", dpi=dpi)
    pre_pos = nx.circular_layout(G)
    pos = nx.spring_layout(G, k=None, pos=pre_pos, iterations=100, scale=1)
    offset = np.array([0, 0.5])
    textpos = {keys: pos[keys] + offset for keys in pos}
    #pos = nx.circular_layout(G)
    nx.draw_networkx_labels(G, textpos, labels=nodelabels_dict, fontsize=12)
    nx.draw_networkx_edges(G, pos, width=edgewidth, edge_color='grey', alpha=0.6)
    nx.draw_networkx_nodes(G, pos, node_size=nodesize, node_color=nodecolor, alpha=0.6)
    #plt.xlim(-0.05,1.05)
    #plt.ylim(-0.05,1.05)
    plt.axis('off')
    return plt, lit_edges

def usage():
    """Print help text"""
    help_text = "Usage:\n"
    help_text += "python correlate.py <cat1> <cat2> -p project !<exclude>\n"
    help_text += "Options:\n"
    help_text += "-mw \t Minimum weight of edges\n"
    help_text += "-hl \t Highlight term\n"
    help_text += "-h \t Help\n"
    help_text += "Example:\n"
    help_text += "correlate.py B01 B02 C -p NewProject -mw 10 !Humans !Cats"
    return help_text

def main(project, categories=[], minweight=1, highlight=False, exclude=[],
    color_scheme="default", source="terms.txt"):
    """Build and show the graph.

    Arguments:
    project (str): The project name
    categories (list, default=[]): The MeSH categories to include. If
        the list is empty, all categories will be included.
    minweight (int, default=1): Minimum weight necessary for connections
        to be displayed.
    highlight (str, default=False): A specific term to highlight. If
        false, no term will be highlighted
    exclude (list, default=[]): List of terms to exclude from the analysis.
    color_scheme (str, default="default"): Not yet implemented.
    """

    project_path = "../projects/"
    gid = 1
    graph_name = lambda: '/graph_%s.png' % gid
    while os.path.isfile(graph_name()):
        gid += 1

    if not os.path.isdir(project_path):
        os.mkdir(project_path)
    if not os.path.isdir(project_path + project):
        raise NameError, "The project '%s' does not exist." % project
    if not os.path.exists(project_path + project + "/" + source):
        raise NameError, "File '%s' from project '%s' is missing" % (source,
            project)
    if not type(minweight) == int:
        raise TypeError, "Minweight needs to be an Integer >= 1"
    if minweight < 1:
        raise ValueError, "Minweight needs to be larger than or equal to 1."
    corr_map , terms= build_matrix(project_path + project + "/" + source,
        categories=categories, highlight=highlight,  exclude=exclude,
        color_scheme=color_scheme)
    plt, edges = create_plot(corr_map, terms, minweight=minweight)
    with open(project_path + project +'/info_%s.txt' % gid, 'w') as f:
        f.write('# Information for Graph %s\n' % gid)
        f.write('# Project: %s\n' % project)
        f.write('# Command: %s\n' % " ".join(sys.argv))
        f.write('# Edges (start, end, weight):\n')
        for edge in edges:
            f.write(", ".join(edge))
            f.write("\n")
    #plt.savefig(project_path + project + graph_name())
    plt.show()
    return True


if __name__ == '__main__':
    main('dummy')
    
