import numpy as np
import math 
from matplotlib import pyplot as plt
#import plotly.plotly as py
#from plotly.graph_objs import *
#import plotly.tools as tls

#py.sign_in('user', 'api_key') ##replace with user and api key

data = np.load('interaction_matrix-2015-11-28-w-deduped-curated-drug-names.npy')
standarize_matrix = data[:,:] 

largest = 0
minimum = 0

for i in xrange(968):
    for j in xrange(968):
        if data[i,j] > largest:
            largest = data[i,j]

for i in xrange(968):
    for j in xrange(968):
        standarize_matrix[i,j] = (data[i,j]/largest)         
        ##standarize_matrix[i,j] = math.log(data[i,j])
        #fails because there are zeros and log(0) undefined.

#Assume that standarize_matrix is covariance already

#get eigenvectors/values
eig_vals, eig_vecs = np.linalg.eig(standarize_matrix)

# Make a list of (eigenvalue, eigenvector) tuples
eig_pairs = [(np.abs(eig_vals[i]), eig_vecs[:,i]) for i in range(len(eig_vals))]

# Sort the (eigenvalue, eigenvector) tuples from high to low
#print eig_pairs[:][1]
eig_pairs.sort(key=lambda x: x[0])
eig_pairs.reverse()

'''
# Visually confirm that the list is correctly sorted by decreasing eigenvalues
print('Eigenvalues in descending order:')
for i in eig_pairs:
    print(i[0]) <-- Good, this is called a scree plot. (FYI.)


## Graph the effects of the eigenvalues. See which cause the most variance
tot = sum(eig_vals)
var_exp = [(i / tot)*100 for i in sorted(eig_vals, reverse=True)]
cum_var_exp = np.cumsum(var_exp)
trace1 = Bar(
        x=['PC %s' %i for i in range(1,200)],
        y=var_exp,
        showlegend=False)
trace2 = Scatter(
        x=['PC %s' %i for i in range(1,200)], 
        y=cum_var_exp,
        name='cumulative explained variance')
swag = Data([trace1, trace2])
layout=Layout(
        yaxis=YAxis(title='Explained variance in percent'),
        title='Explained variance by different principal components')
fig = Figure(data=swag, layout=layout)
py.iplot(fig)
'''
# look at first 2 eigenvectors. Explains roughly 13 percent variance
matrix_w = np.hstack((eig_pairs[0][1].reshape(968,1), 
                      eig_pairs[1][1].reshape(968,1)))

print('Matrix W:\n', matrix_w)

transformed = matrix_w.T.dot(standarize_matrix)
plt.plot(transformed[0,0:968], transformed[1,0:968],
         'o', markersize=7, color='red', alpha=0.2)
plt.xlim([-0.5,0.5])
plt.ylim([-0.1,0.1])
plt.xlabel('x_values')
plt.ylabel('y_values')
plt.legend()
plt.title('Praying I did this properly')
plt.show()
