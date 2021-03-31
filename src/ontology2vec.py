# -*- coding: utf-8 -*-
import random
import numpy as np
import networkx as nx
from gensim.models import Word2Vec
from nltk.corpus import wordnet as wn

class Graph():
	def __init__(self, nx_G):
		self.G = nx_G

	def random_walk(self, walk_length, start_node):
		G = self.G
		#读取之前产生的采样表
		alias_nodes = self.alias_nodes
		# 产生一条序列walk
		walk = [start_node]

		while len(walk) < walk_length:
			cur = walk[-1]
			cur_nbrs = sorted(G.neighbors(cur))

			# alias method选择一个相邻结点
			i = alias_draw(alias_nodes[cur][0], alias_nodes[cur][1])
			walk.append(cur_nbrs[i])

		return walk

	def simulate_walks(self, num_walks, walk_length):
		G = self.G
		walks = []
		nodes = list(G.nodes())

		print 'Walk iteration:'
		for walk_iter in range(num_walks):
			print str(walk_iter+1), '/', str(num_walks)
			random.shuffle(nodes)
			for node in nodes:
				walk = self.random_walk(walk_length=walk_length, start_node=node)
				walks.append(walk)

		return walks

	def transition_probs(self, p):
		G = self.G
		alias_nodes = {}

		for node in G.nodes():
			neighbor = sorted(G.neighbors(node))

			w_bigger = G[node][neighbor[0]]['weight']
			w_smaller = G[node][neighbor[0]]['weight']
			for nbr in sorted(G.neighbors(node)):
				w = G[node][nbr]['weight']
				if w > w_bigger:
					w_bigger = w
				if w < w_smaller:
					w_smaller = w

			# 转移到各结点的概率
			unnormalized_probs = []
			for nbr in sorted(G.neighbors(node)):
				w = G[node][nbr]['weight']	#权重
				if w == w_bigger:
					unnormalized_probs.append(w*p)
				else:
					unnormalized_probs.append(w)

			# 标准化
			norm_const = sum(unnormalized_probs)
			normalized_probs =  [float(u_prob)/norm_const for u_prob in unnormalized_probs]

			# 创建每个结点的alias表
			alias_nodes[node] = alias_table(normalized_probs)

		self.alias_nodes = alias_nodes

		return


def alias_table(probs):
	# 构造alias采样表
	K = len(probs)
	accept = np.zeros(K)
	alias = np.zeros(K, dtype=np.int)

	smaller = []	# 小于1的
	larger = []	#大于1的
	for i, prob in enumerate(probs):
		accept[i] = K*prob
		if accept[i] < 1.0:
			smaller.append(i)
		else:
			larger.append(i)

	while len(smaller) > 0 and len(larger) > 0:
		small = smaller.pop()
		large = larger.pop()

		alias[small] = large
		accept[large] = accept[large] + accept[small] - 1.0
		 
		if accept[large] < 1.0:
			smaller.append(large)
		else:
			larger.append(large)

	return accept, alias

def alias_draw(accept, alias):
	K = len(accept)

	# 随机选取第i列
	i = int(np.floor(np.random.rand()*K))
	# 产生一个随机数，若小于此列中accept的值，返回列号i，否则返回相补的alias
	if np.random.rand() < accept[i]:
	    return i
	else:
	    return alias[i]
