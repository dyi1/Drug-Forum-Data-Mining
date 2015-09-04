# -*- coding: utf-8 -*-
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora, models, similarities
swag = ["archive/2c-b/Accidental Overdose Panic.txt",
"archive/2c-b/Breathtaking with Some Physical Discomfort.txt"]

documents = []
for item in swag:
    with open (item, "r") as fid:
        #documents.append(fid.read().replace('\n', ''))
        jack = fid.read().replace('\n', '')
        documents.append(jack)
#some issues in that ' becomes \xe2\x80\x99

stoplist = set('for a of the and to in'.split())

texts = [[word for word in document.lower().split() if word not in stoplist]
for document in documents]
    


dictionary = corpora.Dictionary(texts)

corpus = [dictionary.doc2bow(text) for text in texts]

lda = models.LdaModel(corpus, id2word=dictionary, num_topics=100)
corpus_lda = lda[corpus]
for doc in corpus_lda:
    print(doc)
