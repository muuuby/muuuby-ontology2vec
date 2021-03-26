# -*- coding: utf-8 -*-
import numpy as np
import networkx as nx
import ontology2vec
import ontology2graph
from gensim.models import Word2Vec
from nltk.corpus import wordnet as wn

def learn_embeddings(walks):
	walks = [map(str, walk) for walk in walks]

	print "Training..."
	model = Word2Vec(walks, size= 128, window= 10, min_count= 0, sg=1, workers = 8, iter= 1)
	model.wv.save_word2vec_format("ontology2vec/test/test_embedding.vector")
	
	return


root = wn.synsets('cat')[0]
nx_G = ontology2graph.o2graph(root) 
nx.write_edgelist(nx_G ,'ontology2vec/test/test_edge.edgelist',data=['weight'])

p = 1 #scale
num_walks = 10
walk_length = 80
G = ontology2vec.Graph(nx_G)
G.transition_probs(p)
walks = G.simulate_walks(num_walks, walk_length)
learn_embeddings(walks)


