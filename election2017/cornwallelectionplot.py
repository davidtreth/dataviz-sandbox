import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv

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
    dframe = pd.DataFrame(list(csv.DictReader(spamreader)))

# get a set of the constituency names    
consts = set(dframe['Constituency'])
print(consts)

fig = plt.figure()
# use suptitle to stop overwriting the axes titles
plt.suptitle("Distribution of Votes in Cornwall\nGeneral Election 8th June 2017")
plt.axis('equal')
plt.xticks([])
plt.yticks([])
for p, c in enumerate(consts):
    # print("Constituency of {}".format(c))
    surnames = dframe.loc[dframe.Constituency == c, ['Surname']].values
    forenames = dframe.loc[dframe.Constituency == c, ['Forenames']].values
    # 'Description' details which party the candidate stood for
    # use d[0] so that the elements are strings not a list containing a string
    descs = [d[0] for d in dframe.loc[dframe.Constituency == c, ['Description']].values]
    plotcolours = [chooseColour(d) for d in descs]
    # combine the forename and surname
    forenames = [f for f in forenames]
    forename = [f[0].split()[0] for f in forenames]
    names = [f+" "+s for f,s in zip(forename, surnames)]
    names = [n[0] for n in names]
    votes = dframe.loc[dframe.Constituency == c, ['Votes']].values
    votes1 = [v[0] for v in votes]
    # create a label with name, party and number of votes
    namedescsvotes = [n+"\n"+d+"\n"+v for n,d,v in zip(names, descs, votes1)]

    totalvotes = np.sum(votes, dtype=np.int)
    # print(totalvotes)
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
    descs = dframe.loc[dframe.Constituency == c, ['Description']].values
    descs = descs[0]
    plotcolours = [chooseColour(d) for d in descs]
    print(descs)
    ax = fig2.add_subplot(2, 3, p+1)
    ax.axis('equal')
    ax.set_title(c)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.pie([1], labels=descs, colors=plotcolours)

plt.show()
