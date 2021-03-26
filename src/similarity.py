# -*- coding: utf-8 -*-
import numpy as np
import networkx as nx
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


def simi(u, v):
    x = np.empty([1,128], dtype = float) 
    y = np.empty([1,128], dtype = float) 
    x[0]=emb[u]
    y[0]=emb[v]
    # 余弦相似度
    simi = cosine_similarity(x, y)
    # print('cosine similarity:', simi)
    # 余弦距离 = 1 - 余弦相似度
    # dist = paired_distances(x, y, metric='cosine')
    # print('cosine distance:', dist)
    return simi

def get_graph(graph_t):
    #读取图
    fh = open(graph_t)
    graph = []
    for line in fh.readlines():
        line = line.replace('\n','')  #去除每一行最后的换行符号
        line = line.split(' ')
        for i in range (0,len(line)):
            line[i] = int(line[i])
        graph.append(line)
    fh.close() 
    G = np.array(graph)
    #G[第几行][0：上位结点 1：下位结点 2：权重]
    return G

def get_dict():
    #读取mapping_dic
    fp=open("thesis/mapping_dic/mapping_test.txt")
    dic = {}
    for line in fp.readlines():
        line = line.replace('\n','')  #去除每一行最后的换行符号
        line = line.replace(' ','')
        line = line.split(':')
        line[1] = int(line[1])
        dic[line[0]] = line[1]
        fp.close() 
    return dic

def avg_s(depth):
    total = 0
    avg = 0
    for i in range(0,len(G)):
        if G[i][2] == depth:
            for j in range(i+1,len(G)):
                if G[j][2] == depth:
                    if G[i][0] == G[j][0]:
                        # print G[i],G[j]
                        total += 1
                        avg += simi(G[i][1],G[j][1]) 
    
    avg = avg/total
    print depth
    print avg

emb = get_embedding("thesis/emb/o2v_0.5.txt")
G = get_graph("thesis/graph/wordnet_entity.edgelist")

for i in range(1,19):
    avg_s(i)




