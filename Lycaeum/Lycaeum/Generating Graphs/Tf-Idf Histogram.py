# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 16:16:56 2016

@author: David
"""
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

print substance_numbers
print len(substance_numbers) #Should equal 968

tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path


for doc in corpus_tfidf:
     for item in doc:
         if item[0] in substance_numbers:
             tfidf_values.append(item[1])
             
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
plt.savefig('Distribution of Tf-Idf values.png')
plt.show()



