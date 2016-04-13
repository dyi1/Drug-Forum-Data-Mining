# -*- coding: utf-8 -*-

import os
import nltk
import string
import json
     
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
            sentence = filter(lambda x: x in printable, sentence) # had a ASCII error           
            text = nltk.word_tokenize(sentence)
            result = nltk.pos_tag(text)
            adjectives = [i for i in result if i[1].lower() == 'jj']
            for drug in drug_names:
                if drug in sentence:
                    drug_adjectives[drug].append(adj for adj in adjectives)
                    print drug
            


print drug_adjectives

json.dump(drug_adjectives,open('associated_adjectives_with_drugs.json','w'))            

