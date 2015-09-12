# -*- coding: utf-8 -*-
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora, models, similarities

documents = []
with open ("Master_File_for_Docs.txt", "r") as fid:
   for line in fid:
       documents.append(line)


stoplist = set('for a of the and to in'.split())
#Removes Stopwords
texts = [[word for word in document.lower().split() if word not in stoplist]
for document in documents]
    


dictionary = corpora.Dictionary(texts)

corpus = [dictionary.doc2bow(text) for text in texts]

lda = models.LdaModel(corpus, id2word=dictionary, num_topics=100)
corpus_lda = lda[corpus]
for doc in corpus_lda:
    print(doc)
