# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import nltk
import string
import json
import re, collections

def words(text):
    return re.findall('[a-z]+', text.lower())

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

corpus = open('big.txt','r')

NWORDS = train(words(corpus.read()))
alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
    s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [a + b[1:] for a, b in s if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b)>1]
    replaces   = [a + c + b[1:] for a, b in s for c in alphabet if b]
    inserts    = [a + c + b     for a, b in s for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words):
    return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or  known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)

printable = set(string.printable) # not all of the forum is ascii friendly




drug_names = open('deduplicated-curated-drug-names','r').read().splitlines()

drug_adjectives = {x: [] for x in drug_names}


text = ''
for root, dirs, files in os.walk("forums"):
    path = root.split('/')
    file_experience = ""
    for file in files:            
        file_name = "forums/" + os.path.basename(root) + "/" + file
        with open(file_name,"r") as fid:
            #print file_experience
            file_experience = fid.read()
        for sentence in file_experience.split('.'):
            unresolved_Neg = 0

            sentence = filter(lambda x: x in printable, sentence) # had a ASCII error           
            new_sentence = ""
            for word in sentence.split():
                new_sentence += (correct(word) + " ")

            text = nltk.word_tokenize(sentence)
            text2 = nltk.word_tokenize(new_sentence)
            result = nltk.pos_tag(text)
            result2 = nltk.pos_tag(text2)
            
            #print result
            #print result2
            for i in range(len(result2)):
                result2[i] = (result2[i][0] + "(spellcheck)",result2[i][1])             

            for i in range(len(result)):    
                if (result[i][0].lower() == 'not'):
                    unresolved_Neg += 1
                elif (unresolved_Neg > 0 and result[i][1].lower() == 'jj'):
                    result[i] = ("not_"+result[i][0],result[i][1])
                    unresolved_Neg -= 1
                    
            for i in range(len(result2)):    
                if (result2[i][0].lower() == 'not'):
                    unresolved_Neg += 1
                elif (unresolved_Neg > 0 and result2[i][1].lower() == 'jj'):
                    result2[i] = ("not_"+result[i][0],result2[i][1])
                    unresolved_Neg -= 1

            adjectives = [i for i in result if i[1].lower() == 'jj']
            adjectives2 = [i for i in result2 if i[1].lower() == 'jj']
            
            for drug in drug_names:
                if drug in sentence:
                    for adj in adjectives:
                        drug_adjectives[drug].append(adj[0])
                    for checked_adj in adjectives2:
                        drug_adjectives[drug].append(checked_adj[0])


print drug_adjectives

json.dump(drug_adjectives,open('adj_with_drugs_with_neg_and_spellcheck.json','w'))            

