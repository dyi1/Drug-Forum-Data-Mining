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
import numpy as np


read_File = open('Multi_drug_references_with_no_stops','r')
from gensim import corpora, models, similarities

texts = []
for line in read_File:
    texts.append(line.split())

substance_numbers = []
tfidf_values = []
#print texts[0]
print len(texts)
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
'''
#Make tf-idf Matrix
tfidf_matrix = np.array(np.zeros((len(texts),len(substance_numbers))))
#Tf-Idf value is zero if unmentioned in doc. 
for i, value in enumerate(substance_numbers):
    for k, doc in enumerate(corpus_tfidf):
        for item in doc:
            if item[0] == value:
                tfidf_matrix[k][i] = item[1]
                
np.save('Lycaeum_TfIdf_Matrix',tfidf_matrix)
'''
for doc in corpus_tfidf:
     for item in doc:
         if item[0] in substance_numbers:
             tfidf_values.append(item[1])

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path



fig, ax = plt.subplots()

# histogram our data with numpy
n, bins = np.histogram(tfidf_values, 50)

# get the corners of the rectangles for the histogram
left = np.array(bins[:-1])
right = np.array(bins[1:])
bottom = np.zeros(len(left))
top = bottom + n

# we need a (numrects x numsides x 2) numpy array for the path helper
# function to build a compound path
XY = np.array([[left, left, right, right], [bottom, top, top, bottom]]).T

# get the Path object
barpath = path.Path.make_compound_path_from_polys(XY)
# make a patch out of it
patch = patches.PathPatch(
    barpath, facecolor='blue', edgecolor='gray', alpha=0.8)
ax.add_patch(patch)

# update the view limits
ax.set_xlim(left[0], right[-1])
ax.set_ylim(bottom.min(), top.max())

plt.xlabel('Tf-Idf Score')
plt.ylabel('Number of Comments with Score')
plt.title('Distribution of Tf-Idf values')

plt.show()
plt.savefig('Distribution of Tf-Idf values.png')
