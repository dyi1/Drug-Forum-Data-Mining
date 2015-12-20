import json
from gensim import corpora, models, similarities

texts = [item['text'] for item in json.load(open('lycaeum-forum-processed-has-drug-names.json','r')).itervalues()]

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
lsi = models.lsimodel.LsiModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=400)
corpus_lsi = lsi[corpus_tfidf]

num_topics = 100
with open('topics','w') as outfile:
	for i in xrange(num_topics):
		print>>outfile,lsi.print_topic(i)