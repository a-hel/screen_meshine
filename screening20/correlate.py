#!usr/bin/python

import pandas
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

with open(cat_file, 'r') as f:
    lines = f.readlines()
for line in lines:
    term, cat = line.rstrip('\n').split(',')
    categories[term] = cat
    
with open('resfile_n.txt', 'r') as f:
    lines = f.readlines()
for line in lines:
    line = line.rstrip('\n')
    term_list = line.split(',')
    combs = itertools.combinations(term_list, 2)
    for x,y in combs:
        try:
            corr_map[x][y] += 1
        except KeyError:
            corr_map[x][y] = 1
df = pandas.DataFrame.from_dict(corr_map)
df.fillna(0, inplace=True)


all_terms = df.index
#http://eutils.ncbi.nlm.nih.gov/entrez/eutils/
#G=nx.random_geometric_graph(200,0.125)
G = nx.MultiGraph()
for i in all_terms:
    G.add_node(i)
colorscheme = [color_by_cat[categories[t][0:1]] for t in all_terms]
print colorscheme
df.apply(generate_edges, axis=0, args =(G,))

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
node_labels = {i: i for i in all_terms}
pos = nx.spring_layout(G)
nx.draw_networkx_labels(G, pos, labels=node_labels)
#nx.draw(G, pos)

nx.draw_networkx_edges(G,pos,alpha=0.4)
nx.draw_networkx_nodes(G,pos,
                       node_size=80,
                       node_color=colorscheme,
                       cmap=plt.cm.Reds_r)

#plt.xlim(-0.05,1.05)
#plt.ylim(-0.05,1.05)
plt.axis('off')
plt.savefig('graph.png')
plt.show()