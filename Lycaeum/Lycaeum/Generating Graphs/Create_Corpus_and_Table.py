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

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

drug_names = open('deduplicated-curated-drug-names','r').read().splitlines()

wordslist = dictionary.token2id.keys()

for drug in drug_names:
    if drug in wordslist:
        substance_numbers.append(dictionary.token2id[drug])
    else:
        substance_numbers.append(-1)

SubNum_Dict = {x: 0 for x in substance_numbers}
for doc in corpus:
    for item in doc:
        if item[0] in SubNum_Dict.keys():
            SubNum_Dict[item[0]] += item[1]
inverse = [(value, key) for key, value in SubNum_Dict.items()]

fid = open('Most_Mentioned_Substances.txt','w')
for i in xrange(20):
    for word in wordslist:
        if max(inverse)[1] == dictionary.token2id[word]:
            fid.write(str(word) + '   ' + str(max(inverse)[0]) + '\n')
    inverse.remove(max(inverse))

fid.close()


corpora.MmCorpus.serialize('Lycaeum_Forums.mm', corpus)
dictionary.save('Lycaeum_Forums.dict')
