#!usr/bin/python

import sys
import numpy as np
import scipy
from collections import defaultdict
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

    posts = {}
    with open(res_file, "r") as f:
        for line in f:
            if line.isspace():
                continue
            elif line.startswith('#'):
                cur_key = line[line.rfind("_")+1:line.rfind(".")]
                posts[cur_key] = []
            else:
                data = line.split("|")
                mesh = data[1].lstrip("*")
                if mesh in exclude:
                    continue
                cat = data[2]
                if _is_in_cat(cat, categories):
                    posts[cur_key].append((mesh, cat))
    return posts

def _flatten(dataset):
    """Return lists of MeSH terms, category codes, color codes for unique
    MeSH terms.

    Arugments:

    dataset (dict): A dataset as output by _load_dataset()

    Returns:

    List of unique MeSH terms, list of their category, list of their color
    """

    arr = reduce(list.__add__,[dataset[key] for key in dataset.keys()])
    uniques = list(set(arr))
    terms, cats = zip(*uniques)
    colors = _get_colors(cats, col_scheme="default")
    return terms, cats, colors


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
    terms, cats, colors = _flatten(dataset)
    dim = len(terms)
    lookup = {term: idx for idx, term in enumerate(terms)}
    corr_map = scipy.sparse.dok_matrix((dim, dim), dtype=np.int)

    for keys in dataset:
        termline = zip(*dataset[keys])[0]
        if not highlight:
            combs = itertools.combinations(termline, 2)
        else:
            if highlight not in termline:
                continue
            else:
                combs = ((highlight, term) for term in termline 
                        if term != highlight)
        for x,y in combs:
            corr_map[lookup[x], lookup[y]] += 1
    mappings = {'lookup': lookup,
        'terms': terms, 
        'cats': cats, 
        'colors': colors}
    corr_map = corr_map + corr_map.transpose()
    return corr_map, mappings

def create_plot(corr_map, mappings, minweight=1):
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
    terms = mappings['terms']
    edgewidth = []
    nodeprops = []
    lit_edges = []
    G = nx.MultiGraph()
    corr_map_coo = corr_map.tocoo()
    max_correlations = corr_map_coo.max(axis=0).toarray()[0]
    node_sums = corr_map_coo.sum(axis=0).tolist()[0]
    for i, max_ in enumerate(max_correlations):
        if max_ >= minweight:
            G.add_node(i)
            n_color = mappings['colors'][i]
            #n_color = 'Green'
            n_size =  node_sums[i]*node_scale
            n_label = terms[i]
            nodeprops.append([n_color, n_size, n_label, i])
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
    plt.figure(figsize=(20,20))
    pre_pos = nx.circular_layout(G)
    pos = nx.spring_layout(G, k=None, pos=pre_pos, iterations=100, scale=1)
    #pos = nx.circular_layout(G)
    nx.draw_networkx_labels(G, pos, labels=nodelabels_dict, fontsize=12)
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


if __name__ == '__main__':
    categories = []
    minweight = 10
    exclude = []
    highlight = False
    color_scheme = "default"
    gid = 1
    if len(sys.argv) <= 1:
        print(usage())
        sys.exit(0)
    else:
        i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg.startswith('-'):
            if arg in ('-h', '--help'):
                print(usage())
                sys.exit(0)
            if arg in ('-mw', '--minweight'):
                i += 1
                minweight = int(sys.argv[i])
            if arg in ('-hl', '--highlight'):
                i += 1
                highlight = sys.argv[i]
            if arg in ('-c', '--colors'):
                i += 1
                color_scheme = sys.argv[i]
            if arg in ('-p', '--project'):
                i += 1
                project = sys.argv[i]
                    
        elif arg.startswith('/'):
            exclude.append(arg[1:])
        else:
            categories.append(arg)
        i += 1
    project_path = "../projects/"
    corr_map, mappings = build_matrix(project_path + project + "/out.txt",
        categories=categories, highlight=highlight,  exclude=exclude,
        color_scheme=color_scheme)
    plt, edges = create_plot(corr_map, mappings, minweight=minweight)
    with open(project_path + project +'/info_%s.txt' % gid, 'w') as f:
        f.write('# Information for Graph %s\n' % gid)
        f.write('# Project: %s\n' % project)
        f.write('# Command: %s\n' % " ".join(sys.argv))
        f.write('# Edges (start, end, weight):\n')
        for edge in edges:
            f.write(", ".join(edge))
            f.write("\n")
    plt.savefig(project_path + project +'/graph_%s.png' % gid)
    plt.show()
