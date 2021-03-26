from nltk.corpus import wordnet as wn

# print wn.synsets('dog')
# print wn.synset('dog.n.01').definition()
# print wn.synset('dog.n.03').definition()
# print wn.synset('pawl.n.01').definition()

# print wn.synset('cat.n.01').hypernym_paths()



print wn.synset('dog.n.01').path_similarity(wn.synset('opera.n.01'))
print wn.synset('wildcat.n.03').hyponyms()
# print wn.synset('domestic_cat.n.01').member_holonyms()

# print wn.synset('dog.n.01').lemma_names()
# print wn.synsets('cat')[0]
# print wn.synset('object.n.01').lemmas()
# print wn.lemma('entity.n.01').name()
# print wn.synset('dog.n.03').examples()