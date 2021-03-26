# -*- coding: utf-8 -*-
from nltk.corpus import wordnet as wn
import networkx as nx
import matplotlib.pyplot as plt

def o2graph(root):
    G = nx.Graph()
    G.depth = {}
    traverse(G, root, root)
    G = count_graph(G)
    # nx.write_edgelist(G,'ontology2vec/test/test.edgelist',data=['weight'])
    return G

def dir_o2graph(root):
    G = nx.DiGraph()
    G.depth = {}
    traverse(G, root, root)
    # G = count_graph(G)
    return G

def traverse(graph, root, node):
    graph.depth[node] = node.shortest_path_distance(root)
    for child in node.hyponyms():
        graph.add_edge(node,child,weight=graph.depth[node]+1)
        traverse(graph, root, child)

#绘图
def graph_draw(graph):
    nx.draw_spring(graph,
        node_size = 100,
        #  [100 * graph.degree(n) for n in graph],
        node_color = [graph.depth[n] for n in graph],
        with_labels = True
        )
    plt.show()

def count_graph(graph):
    list1 = list(graph.nodes) #结点
    nodes_nums = len(list1)

    list2 = []  #数字结点
    for i in range (0,nodes_nums):
        list2.append(i)

    mapping = dict(zip(list1, list2)) #将图的结点映射为数字
    G = nx.relabel_nodes(graph, mapping)
    #将对应关系保存为文件
    s = str(mapping).replace(",", "\n")
    f = open('ontology2vec/test/test_mapping_dict.txt','w')
    f.writelines(s)
    f.close()    

    return G

# root = wn.synset('entity.n.01')
# graph = o2graph(root)

# print graph.edges
# graph_draw(graph)

#生成边列表或邻接表
# nx.write_edgelist(graph,'str_entity.edgelist',data=['weight'])
# nx.write_edgelist(G1,'test.edgelist',data=['color'])
# nx.write_edgelist(G1,'test.edgelist',data=['color','weight'])
# nx.write_edgelist(G1,"wordnet_test.edgelist")
# nx.write_adjlist(graph,"str_entiy.adjlist")









