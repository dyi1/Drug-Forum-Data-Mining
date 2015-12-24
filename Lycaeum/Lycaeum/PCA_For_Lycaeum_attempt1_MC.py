import numpy as np
import Graphics as artist
import matplotlib.pyplot as plt

from mpl_toolkits.axes_grid1 import make_axes_locatable


plt.xkcd()
data = np.load('interaction_matrix-2015-11-28-w-deduped-curated-drug-names.npy')
print data[:10,3]
data[np.diag_indices_from(data)] /= 2. #Forgot to tell you this- MC
data = np.log(1.+data) #log because decreasing marginal importance

data = (data-data.min(axis=1))/(data.max(axis=1)-data.min(axis=1))


cutoff = 10
eig_vals, eig_vecs = np.linalg.eigh(data) #Wrong function
idx = np.argsort(eig_vals) # sorting the eigenvalues
idx = idx[::-1]       # in ascending order

# sorting eigenvectors according to the sorted eigenvalues
eig_vecs = eig_vecs[:,idx]
eig_vecs = eig_vecs[:,range(cutoff)]
eig_vals = eig_vals[idx] # sorting eigenvalues
score = np.dot(eig_vecs.T,data) # projection of the data in the new space

eig_vals /= eig_vals.max()
print eig_vals[:10]
fig,axs = plt.subplots(nrows=1,ncols=3, figsize=(14,6.5))

#-- Raw data
im = axs[0].imshow(data,interpolation='nearest',aspect='equal',cmap = plt.cm.bone_r)
divider = make_axes_locatable(axs[0])
cax = divider.append_axes("right", size="15%", pad=0.05)
cbar = plt.colorbar(im, cax=cax)
artist.adjust_spines(axs[0])
axs[0].set_xlabel('No. of mentions')
axs[0].set_ylabel('No. of mentions')

# -- Eigenvectors
im = axs[1].imshow(eig_vecs*eig_vals[:,np.newaxis],interpolation='nearest',aspect='auto',cmap = plt.cm.bone_r)
divider = make_axes_locatable(axs[1])
cax = divider.append_axes("right", size="15%", pad=0.05)
cbar = plt.colorbar(im, cax=cax)
artist.adjust_spines(axs[1])
axs[1].set_xlabel('P.C., scaled by $\lambda$')
axs[1].set_ylabel('Weight')

# -- Projection
im = axs[2].imshow(score,interpolation='nearest',aspect='auto',cmap = plt.cm.bone_r)
divider = make_axes_locatable(axs[2])
cax = divider.append_axes("right", size="15%", pad=0.05)
cbar = plt.colorbar(im, cax=cax)
artist.adjust_spines(axs[2])
axs[2].set_xlabel('Principal component')
axs[2].set_ylabel('Weight')


plt.tight_layout()
plt.savefig('pca-xkcd-from-corr.png')

