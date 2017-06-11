import matplotlib.pyplot as plt
import matplotlib_venn as venn
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
    forenames = [f for f in forenames]
    forename = [f[0].split()[0] for f in forenames]
    names = [f+" "+s for f,s in zip(forename, surnames)]
    names = [n[0] for n in names]
    votes = dframe.loc[dframe.Constituency == c, ['Votes']].values
    votes1 = [v[0] for v in votes]
    turnout =  dframe.loc[dframe.Constituency == c, ['Turnout']].values
    turnout = float(np.max(turnout))
    # not actually used here
    # namedescsvotes = [n+"\n"+d+"\n"+v for n,d,v in zip(names, descs, votes1)]

    totalvotes = np.sum(votes, dtype=np.int)
    # calculate the number of people who are on the electoral register from
    # turnout and votes cast (should really get this directly from data due to
    # spoiled ballots etc.)
    electorate = np.int(totalvotes / (turnout/100.0))
    novote = electorate - totalvotes
    votewinner = int(votes1[0])
    voteothers = totalvotes - votewinner
    winnername = names[0]

    ax = fig.add_subplot(2, 3, p+1)
    ax.axis('equal')
    ax.set_title("{C}: {t} votes cast".format(C=c, t=totalvotes))
    ax.set_xticks([])
    ax.set_yticks([])
    
    # subsets = (Ab, aB, AB)
    # i.e. A and not(B), not(A) and B, A and B
    # in this example the second of these must be zero
    # since A is those who cast votes, and B is those voting for the winner
    v = venn.venn2(subsets=(voteothers, 0, votewinner), set_colors =('lightgray', 'navy'), set_labels=('Other candidates', winnername))
    

                          
fig2 = plt.figure()
plt.suptitle("Distribution of Votes in Cornwall\nGeneral Election 8th June 2017")
plt.axis('equal')
plt.xticks([])
plt.yticks([])
for p, c in enumerate(consts):
    surnames = dframe.loc[dframe.Constituency == c, ['Surname']].values
    forenames = dframe.loc[dframe.Constituency == c, ['Forenames']].values
    descs = dframe.loc[dframe.Constituency == c, ['Description']].values
    descs = descs[0]
    plotcolours = [chooseColour(d) for d in descs]
    forenames = [f for f in forenames]
    forename = [f[0].split()[0] for f in forenames]
    names = [f+" "+s for f,s in zip(forename, surnames)]
    names = [n[0] for n in names]
    votes = dframe.loc[dframe.Constituency == c, ['Votes']].values
    votes1 = [v[0] for v in votes]
    turnout =  dframe.loc[dframe.Constituency == c, ['Turnout']].values
    turnout = float(np.max(turnout))
    
    
    namedescsvotes = [n+"\n"+d+"\n"+v for n,d,v in zip(names, descs, votes1)]

    totalvotes = np.sum(votes, dtype=np.int)
    electorate = np.int(totalvotes / (turnout/100.0))    
    novote = electorate - totalvotes
    votewinner = int(votes1[0])
    voteothers = totalvotes - votewinner
    winnername = names[0]
    print(names)
    print(winnername)
    #print(descs)
    ax = fig2.add_subplot(2, 3, p+1)
    ax.axis('equal')
    ax.set_title(c+"\nturnout ={t}%".format(t=turnout))
    ax.set_xticks([])
    ax.set_yticks([])
    # subsets=(Abc, aBc, ABc, abC, AbC, aBC, ABC)
    # i.e. A and not(B) and not(C), not(A) and B and not(C) etc.
    # in this example several of these sets must be zero
    # since A is the electoral regisrer, and B is those voting for the winner
    # C those voting for other candidates
    v = venn.venn3(subsets=(novote, 0, votewinner, 0, voteothers, 0, 0), set_colors =('lightgray', 'blue', 'red'), set_labels=('electoral register', winnername,'Other candidates'))
    


plt.show()
