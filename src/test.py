# -*- coding: utf-8 -*-
import ontology2graph
import networkx as nx
from nltk.corpus import wordnet as wn
import matplotlib.pyplot as plt

#绘图
def graph_draw(graph):
    nx.draw_spring(graph,
        node_size = 100,
        #  [100 * graph.degree(n) for n in graph],
        # node_color = [graph.depth[n] for n in graph],
        with_labels = True
        )
    plt.show()

fh = open("cat.adjlist")
G = nx.read_adjlist(fh)

graph_draw(G)
