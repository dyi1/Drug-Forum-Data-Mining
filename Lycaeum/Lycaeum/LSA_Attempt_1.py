import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora, models
import codecs

dictionary = corpora.Dictionary(line.lower().split() for line in codecs.open('deduplicated-curated-drug-names', encoding = 'utf-8', mode= "r" ))

print dictionary
    
class MyCorpus(object):   
    def __iter__(self):
        for line in codecs.open('Master_File_Forums.txt', encoding = 'utf-8', mode= "r"):
            drug_phrases = []
            for word in line:
                if word in dictionary:
                    drug_phrases.append(word)
            yield dictionary.doc2bow(drug_phrases)
            
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
    print(doc)
    
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)
#lsi.save('/tmp/model.lsi')
lsi_corpus = lsi[corpus_tfidf]

for doc in lsi_corpus:
    print doc