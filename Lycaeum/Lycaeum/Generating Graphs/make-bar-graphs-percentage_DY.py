import json, itertools
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import Graphics as artist
from matplotlib import rcParams

rcParams['text.usetex'] = True

rcParams['text.latex.unicode'] = True
'''
#-- create data frame

	        Classification            Cluster
	      Stimulant Depressant       Not  Psychotherapeutics
    Drug 

'''
READ = 'rb'

clusters = json.load(open('k-mean-clusters-names.json',READ)) 
classification = json.load(open('Drug_Classification.json',READ)) 

#-- get unique labels
classification_labels = list(set(list(itertools.chain.from_iterable([classification[key] 
									for key in classification.iterkeys()]))))


#-- Construct data frame 
LABELS = ['psychoactive','stimulant','sedative','hallucinogen','antidepressant']
data = np.zeros((len(classification),len(LABELS)))
all_drugs = clusters['0'] + clusters['1']
data = {drug:{'classification': classification[drug][0], 
		"cluster": "Psychotherapeutic" if drug in clusters['1'] else "Not Psychotherapeutic" } 
		for drug in all_drugs if drug in classification and classification[drug][0] in classification_labels}

'''
#-- Now flattern dictionary from 
	
	drug : {classification,cluster}
   
        -to-

	classification : cluster

'''
data_by_classification = {classification:{cluster:len([drug for drug in data 
									if data[drug]['cluster']==cluster 
								and data[drug]['classification'] == classification]) 
						for cluster in ['Psychotherapeutic','Not Psychotherapeutic']} for classification in LABELS}

Total_Psych = 0
Total_NonPsych = 0         

json.dump(data_by_classification,open('tests.json','w'))

for classificiation, cluster in data_by_classification.iteritems():
    for key, value in cluster.iteritems():
        if (key == 'Psychotherapeutic'):
            Total_Psych += float(value)
        else: 
            Total_NonPsych += float(value)

print Total_Psych
for classificiation, cluster in data_by_classification.iteritems():
    for key, value in cluster.iteritems():
        if (key == 'Psychotherapeutic'):
            data_by_classification[classificiation][key] = value/Total_Psych * 100
        else: 
            data_by_classification[classificiation][key] = value/Total_NonPsych * 100     


cluster_1_data = [data_by_classification[label]['Psychotherapeutic'] for label in LABELS]
for item in cluster_1_data:
    print item
cluster_0_data = [data_by_classification[label]['Not Psychotherapeutic'] for label in LABELS]
for item in cluster_0_data:
    print item
fig = plt.figure(figsize=(10,6))
ax = fig.add_subplot(111)
idx = np.arange(len(data_by_classification))
width = 0.35

cluster_0 = ax.bar(idx,cluster_0_data,width,color='k',
		label=artist.format('Not Psychotherapeutic'))
cluster_1 = ax.bar(idx+width,cluster_1_data,width,color='w',
		label=artist.format('Psychotherapeutic'))

artist.adjust_spines(ax)
ax.set_ylabel(artist.format('Percentage of Drug Types'))
ax.set_xticks(idx+width)
ax.set_xticklabels(map(artist.format,LABELS))
plt.legend(frameon=False, loc="upper left")
plt.savefig('prevalence-of-drug-classes-by-cluster.png')