import numpy as np
import os
from gensim import corpora, models, similarities 

read_File = open('Multi_drug_references_with_no_stops','r')

corpus = corpora.MmCorpus('Lycaeum_Forums.mm')
docNum = 0
for doc in corpus:
    docNum += 1
#docNum represents total number of documents
dictionary = corpora.Dictionary.load('Lycaeum_Forums.dict')


substance_numbers = []
tfidf_values = []
drug_names = open('deduplicated-curated-drug-names','r').read().splitlines()

wordslist = dictionary.token2id.keys()

for drug in drug_names:
    if drug in wordslist:
        substance_numbers.append(dictionary.token2id[drug])
    else:
        substance_numbers.append(-1)
#Will be of the order as appears in file deduplicated-curated-drug-names

tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

tfidf_matrix = np.array(np.zeros((docNum,len(substance_numbers))))
#Tf-Idf value is zero if unmentioned in doc. 
#All -1 in substance numbers also will be 0.
for i, value in enumerate(substance_numbers):
    for k, doc in enumerate(corpus_tfidf):
        for item in doc:
            if item[0] == value:
                tfidf_matrix[k][i] = item[1]
                
np.save('Lycaeum_TfIdf_Matrix',tfidf_matrix)