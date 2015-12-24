import json 
import numpy as np
import Graphics as artist
import matplotlib.pyplot as plt

from mpl_toolkits.axes_grid1 import make_axes_locatable
from sklearn import decomposition, cluster, metrics

'''
   This module answers the question of whether the combinations of two drugs are correlated.
   We assume that if two drugs are correlated, they will lie parallel to the same principal component
'''

plt.xkcd()
data = np.load('interaction_matrix-2015-11-28-w-deduped-curated-drug-names.npy')
data[np.diag_indices_from(data)] /= 2. #Forgot to tell you this- MC
data = np.log(1.+data) #log because decreasing marginal importance
data = np.nan_to_num((data-data.min(axis=1))/(data.max(axis=1)-data.min(axis=1)))
pca = decomposition.PCA(n_components=10)
pca.fit(data)
print pca.explained_variance_ratio_
X = pca.transform(data)

 
#This code indicated there were two clusters 
#find optimal cluster
for nclus in xrange(2,10):
	kmeans = cluster.KMeans(n_clusters=nclus, n_init=20)
	kmeans.fit(X[:,1:])
	labels = kmeans.predict(X[:,1:])
	#print labels
	#print metrics.silhouette_score(X,labels)


kmeans = cluster.KMeans(n_clusters=2, n_init=20)
kmeans.fit(X[:,1:])
labels = kmeans.predict(X[:,1:])

print np.unique(labels)

cluster_labels = {str(label):list(np.where(labels==label)[0]) for label in labels}
json.dump(cluster_labels,open('k-mean-clusters.json','wb'))

drugs = open('deduplicated-curated-drug-names','r').read().splitlines()
cluster_contents = {str(label):[drugs[idx] for idx in cluster_labels[str(label)]] for label in labels}
json.dump(cluster_contents,open('k-mean-clusters-names.json','wb'))

'''
fig,(ax1,ax2) = plt.subplots(nrows=1,ncols=2,sharex=True,sharey=True)
ax1.scatter(X[:,0],X[:,1],c=X[:,2],cmap=plt.cm.bwr)
artist.adjust_spines(ax1)
ax1.set_xlabel('Principal Component 1')
ax1.set_ylabel('Principal Component 2')

for x,y,s,c in zip(X[:,0],X[:,1],
				['o' if label == 1 else 's' for label in labels],
				['k' if label == 1 else 'w' for label in labels]):
	ax2.scatter(x,y,marker=s,c=c)
artist.adjust_spines(ax2)
ax2.set_xlabel('Principal Component 1')
ax2.set_ylabel('Principal Component 2')

plt.tight_layout()

plt.savefig('pc-scatter.png')
'''
