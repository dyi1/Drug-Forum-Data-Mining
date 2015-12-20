import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora, models
import codecs

dictionary = corpora.Dictionary(line.lower().split() for line in codecs.open('deduplicated-curated-drug-names', encoding = 'utf-8', mode= "r" ))

print dictionary
    
class MyCorpus(object):   
    def __iter__(self):
        for line in codecs.open('Master_File_Forums.txt', encoding = 'utf-8', mode= "r"):
            yield dictionary.doc2bow(line.lower().split())
            
corpus = MyCorpus()
print corpus 
'''
for vector in corpus: # load one vector into memory at a time
     print(vector)
'''
tfidf = models.TfidfModel(corpus)
#tfidf.save('/tmp/model.tfidf')
corpus_tfidf = tfidf[corpus]

for doc in corpus_tfidf:
    if doc != []:
        print(doc) #ALL OF THEM ARE BLANK??
    
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)
#lsi.save('/tmp/model.lsi') Trying to save but gives an IOError: [Errno 2] No such file or directory: '/tmp/model.tfidf' 
lsi_corpus = lsi[corpus_tfidf]

for doc in lsi_corpus:
    if doc != []:
        print doc
        