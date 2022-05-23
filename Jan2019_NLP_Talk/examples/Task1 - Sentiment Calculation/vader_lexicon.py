import string
import pickle
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

punctuation = list(string.punctuation)
numbers = list(string.digits)

def saveLexicon(fileName='lexicon'):
    sia = SentimentIntensityAnalyzer()
    lexicon = sia.lexicon
    print("VADER lexicon's size: {}".format(len(lexicon.keys())))

    results = {}
    for word in lexicon.keys():
        #Remove 'words' containing punctuation (smileys):
        if any(ch in punctuation for ch in word):
            continue
        #Remove 'words' containing numbers:
        if any(ch in numbers for ch in word):
            continue
        results[word] = lexicon[word]/4 #normalize scores.
    print("Cleaned lexicon's size: {}".format(len(results.keys())))

    #Save 'results' to .pickle file:
    with open('{}.pickle'.format(fileName), 'wb') as wf:
        pickle.dump(results, wf)

def loadLexicon(fileName='lexicon'):
    with open('{}.pickle'.format(fileName), 'rb') as rf:
        lexicon = pickle.load(rf)
    return lexicon

if __name__ == "__main__":
    # saveLexicon()
    lexicon = loadLexicon()
    print(lexicon)
