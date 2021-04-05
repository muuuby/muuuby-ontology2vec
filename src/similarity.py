# -*- coding: utf-8 -*-
import numpy as np
import networkx as nx
import ontology2graph
from nltk.corpus import wordnet as wn
from sklearn.metrics.pairwise import cosine_similarity, paired_distances

def get_embedding(emb_t):
    #读取向量
    fp=open(emb_t)
    arrays = []
    for line in fp.readlines():
        line = line.replace('\n','')  #去除每一行最后的换行符号
        line = line.split('\t')[1:]
        for i in range (0,len(line)):
            line[i] = float(line[i])
        arrays.append(line)
    fp.close() 
    emb = np.array(arrays)

    return emb

def select_node(depth):
    # 获取深度为depth的所有结点
    nodelist = get_key(node_depth, depth)

    print depth
    for i in range(0, len(nodelist)):
        childlist = nodelist[i].hyponyms()
        if(len(childlist)>5):
            s = avg(nodelist[i])
            if(s > 0.95):
                print s,len(childlist),nodelist[i]

def avg(node):
    s = 0
    childlist = node.hyponyms()

    c1 = dic.get(str(childlist[0]))

    for j in range(1, len(childlist)):
        c2 = dic.get(str(childlist[j]))
        s += simi(c1, c2)

    s = s/(len(childlist)-1)
    return s
    
def brother_simi(node):
    print "\n"
    childlist = node.hyponyms()
    print childlist[0]
    c1 = dic.get(str(childlist[0]))

    for j in range(1, len(childlist)):
        c2 = dic.get(str(childlist[j]))
        s = simi(c1, c2)

        print childlist[j],s[0][0]

def simi(u,v):
    x = np.empty([1,128], dtype = float) 
    y = np.empty([1,128], dtype = float) 
    x[0]=emb[u]
    y[0]=emb[v]
    # 余弦相似度
    simi = cosine_similarity(x, y)
    # print('cosine similarity:', simi)
    # 余弦距离 = 1 - 余弦相似度
    dist = paired_distances(x, y, metric='cosine')
    # print('cosine distance:', dist)
    return simi

def get_graph(root):
    #读取图
    root = wn.synsets(root)[0]
    G = ontology2graph.o2graph(root, node_depth) 

    return G

def get_dict(d):
    #读取mapping_dic
    fp=open(d)
    for line in fp.readlines():
        line = line.replace('\n','')  #去除每一行最后的换行符号
        line = line.replace(' ','')
        line = line.split(':')
        dic[line[0]] = int(line[1])
        fp.close() 
    return dic

def get_key (dict, value):
    return [k for k, v in dict.items() if v == value]

def avg_s(depth):
    total = 0
    avg = 0
    # 获取深度为depth的所有结点
    nodelist = get_key(node_depth, depth)

    # 对于每个深度为depth的结点，计算它的子节点之间的平均距离
    for i in range(0, len(nodelist)):
        childlist = nodelist[i].hyponyms()
        for j in range(0, len(childlist)):
            for k in range(j+1, len(childlist)):
                c1 = dic.get(str(childlist[j]))
                c2 = dic.get(str(childlist[k]))
 
                total += 1
                avg += simi(c1, c2)
    
    avg = avg/total
    print depth+1,avg[0][0]

node_depth = {} # 各结点的深度
dic = {}    # 结点对应的数值

emb = get_embedding("thesis/t/dw_10_10_10.txt")
G = get_graph('entity')
get_dict("thesis/mapping_dic/mapping_dict.txt")

for i in range(1,19):
    avg_s(i)






