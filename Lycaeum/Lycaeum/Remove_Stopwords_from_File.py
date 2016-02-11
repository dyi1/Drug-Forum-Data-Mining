# -*- coding: utf-8 -*-
'''
File_With_Stopwords = open('Two_or_more_drug_references','r')

Removed_Stopwords = open('Multi_drug_references_with_no_stops','w')

stopwords = set(open('stopwords.txt','r').read().splitlines())

for line in File_With_Stopwords:
    words = [word for word in line.lower().split() if word not in stopwords]
    txt = ' '.join(words)
    Removed_Stopwords.write(txt + '\n')
    
File_With_Stopwords.close()
Removed_Stopwords.close()
'''

read_File = open('Multi_drug_references_with_no_stops','r')
from gensim import corpora, models, similarities

texts = []
for line in read_File:
    texts.append(line.split())

substance_numbers = []
tfidf_values = []
#print texts[0]

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
drug_names = open('deduplicated-curated-drug-names','r').read().splitlines()

wordslist = dictionary.token2id.keys()
for key in wordslist:
    for drug in drug_names:
        if key == drug:
             substance_numbers.append(dictionary.token2id[key])
substance_numbers.sort()
 

#print corpus[0]
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

print corpus_tfidf

for doc in corpus_tfidf:
     for item in doc:
         if item[0] in substance_numbers:
             tfidf_values.append(item[1])
         
print tfidf_values[0:10]
