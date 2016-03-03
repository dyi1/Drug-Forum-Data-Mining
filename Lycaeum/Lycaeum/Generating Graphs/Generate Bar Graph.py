import json
from pprint import pprint

with open('k-mean-clusters-names.json') as data_file:    
    data = json.load(data_file)
with open('Drug_Classification.json') as data_file:    
    effects = json.load(data_file)

g1 = data["1"]
g1Totaleffects = []
for drug in g1:
    for item in effects[drug]:
        g1Totaleffects.append(item)
diff_effects1 = list(set(g1Totaleffects))
effectCounter1 = {x : g1Totaleffects.count(x) for x in diff_effects1}

topEffects1 = []

inverse1 = [(value, key) for key, value in effectCounter1.items()]
for i in range(6):
    topEffects1.append((max(inverse1)[1],max(inverse1)[0]))
    inverse1.remove(max(inverse1))

print topEffects1


g0 = data["0"]
g0Totaleffects = []
for drug in g0:
    for item in effects[drug]:
        g0Totaleffects.append(item)
diff_effects0 = list(set(g0Totaleffects))
effectCounter0 = {x : g0Totaleffects.count(x) for x in diff_effects0}

topEffects0 = []

inverse0 = [(value, key) for key, value in effectCounter0.items()]
for i in range(6):
    topEffects0.append((max(inverse0)[1],max(inverse0)[0]))
    inverse0.remove(max(inverse0))
print topEffects0

effects0 = []
mentions0 = []
for item in topEffects0:
    effects0.append(item[0])
    mentions0.append(item[1])

effects1 = []
mentions1 = []
for item in topEffects1:
    effects1.append(item[0])
    mentions1.append(item[1])


import matplotlib.pyplot as plt
import numpy as np

N = 6

ind = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars

fig, ax = plt.subplots()
rects0 = ax.bar(ind, mentions0, width, color='r')

# add some text for labels, title and axes ticks
ax.set_ylabel('Number of Drugs with Associated Effect')
ax.set_title('Highest Effects Associated with Non-Medical Drugs')
ax.set_xticks(ind + width)
ax.set_xticklabels(effects0)



def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')

autolabel(rects0)
plt.savefig("Effects Associated with Non-Medical Drugs.png")
plt.show()


fig, ax = plt.subplots()
rects1 = ax.bar(ind, mentions1, width, color='r')

# add some text for labels, title and axes ticks
ax.set_ylabel('Number of Drugs with Associated Effect')
ax.set_title('Highest Effects Associated with Medical Drugs')
ax.set_xticks(ind + width)
ax.set_xticklabels(effects1)

autolabel(rects1)
plt.savefig("Effects Associated with Medical Drugs.png")
plt.show()





