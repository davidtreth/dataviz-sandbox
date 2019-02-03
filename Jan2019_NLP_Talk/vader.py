import nltk
import pickle
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
lexicon = sia.lexicon

# rescale
lexicon1 = {l:lexicon[l]/4 for l in lexicon}

for l in lexicon1:
	print(l, lexicon1[l])

with open('lexicon.pickle', 'wb') as f:
	pickle.dump(lexicon1, f)

lexkeyvaltup = [(k,v) for (k,v) in lexicon1.items()]
lexicon2 = sorted(lexkeyvaltup,key=lambda kvtup:kvtup[1])

for l in lexicon2:
	print(l)
	
