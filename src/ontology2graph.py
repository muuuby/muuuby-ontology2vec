# -*- coding: utf-8 -*-
from nltk.corpus import wordnet as wn
import networkx as nx
import matplotlib.pyplot as plt

mapping = {}

def o2graph(root, node_depth):
    G = nx.Graph()
    depth = 1
    traverse(G, root, depth, node_depth)
    G = mapping_graph(G)
    nx.write_edgelist(G,'thesis/test/test.edgelist',data=['weight'])
    return G

def traverse(graph, node, depth, node_depth):
    node_depth[node] = depth
    depth += 1
    for child in node.hyponyms():
        graph.add_edge(node, child, weight=depth)
        traverse(graph, child, depth, node_depth)

#绘图
def graph_draw(graph):
    nx.draw_spring(graph,
        node_size = 100,
        #  [100 * graph.degree(n) for n in graph],
        node_color = [graph.depth[n] for n in graph],
        with_labels = True
        )
    plt.show()

def mapping_graph(graph):
    list1 = list(graph.nodes) #结点
    nodes_nums = len(list1)

    list2 = []  #数字结点
    for i in range (0,nodes_nums):
        list2.append(i)

    mapping = dict(zip(list1, list2)) #将图的结点映射为数字
    G = nx.relabel_nodes(graph, mapping)
    #将对应关系保存为文件
    s = str(mapping).replace(",", "\n")
    f = open('thesis/test/mapping_dic.txt','w')
    f.writelines(s)
    f.close()    

    return G










