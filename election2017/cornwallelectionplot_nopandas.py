import matplotlib.pyplot as plt
import numpy as np
import csv
from collections import defaultdict

def chooseColour(desc):
    if desc == "Labour Party":
        return "red"
    elif "Liberal" in desc:
        return "yellow"
    elif "Green" in desc:
        return "green"
    elif "Conservative" in desc:
        return "blue"
    else:
        return "magenta"

   
with open('cornwallelectionresults2017.csv', 'r') as spamreader:
    # read the header
    data = csv.reader(spamreader)
    header = data.next()

consts = []

with open('cornwallelectionresults2017.csv', 'r') as spamreader:
    # read the constitutencies
    data = csv.DictReader(spamreader)
    datadict = {}
    for row in data:
        consts.append(row['Constituency'])
        
consts = list(set(consts))
for c in consts:
    datadict[c] = defaultdict(list)

with open('cornwallelectionresults2017.csv', 'r') as spamreader:
    # read the data itself
    data = csv.DictReader(spamreader)
    for row in data:
        for h in row:
            if h != 'Constituency':
                datadict[row['Constituency']][h].append(row[h])

fig = plt.figure()
# use suptitle to stop overwriting the axes titles
plt.suptitle("Distribution of Votes in Cornwall\nGeneral Election 8th June 2017")
plt.axis('equal')
plt.xticks([])
plt.yticks([])
for p, c in enumerate(consts):
    print("Constituency of {}".format(c))
    surnames = datadict[c]['Surname']
    forenames = datadict[c]['Forenames']
    descs = datadict[c]['Description']
    votes = datadict[c]['Votes']
    
    forename1 = [f.split()[0] for f in forenames]
    names = [f+" "+s for f,s in zip(forename1, surnames)]    
    namedescsvotes = [n+"\n"+d+"\n"+v for n,d,v in zip(names, descs, votes)]
    votes = [int(v) for v in votes]
    totalvotes = np.sum(votes, dtype=np.int)
    plotcolours = [chooseColour(d) for d in descs]
    
    ax = fig.add_subplot(2, 3, p+1)
    ax.axis('equal')
    ax.set_title("{C}: {t} votes cast".format(C=c, t=totalvotes))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.pie(votes, radius = np.sqrt(totalvotes/50000.0), labels=namedescsvotes, colors=plotcolours, autopct='%1.1f%%')

fig2 = plt.figure()
plt.suptitle("Representation of Cornwall in the House of Commons")
plt.axis('equal')
plt.xticks([])
plt.yticks([])

for p, c in enumerate(consts):
    descs = datadict[c]['Description']
    descs = descs[:1]
    surnames = datadict[c]['Surname']
    forenames = datadict[c]['Forenames']
    forename1 = [f.split()[0] for f in forenames]
    names = [f+" "+s for f,s in zip(forename1, surnames)]
    names = names[:1]
    label = [n+"\n"+d for n,d in zip(names, descs)]
    
    plotcolours = [chooseColour(d) for d in descs]
    ax = fig2.add_subplot(2, 3, p+1)
    ax.axis('equal')
    ax.set_title(c)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.pie([1], labels=label, colors=plotcolours)
    
plt.show()
                          
    
    
