import pickle
from nltk.tokenize import word_tokenize

#Import from `nb_classifier.py`:
from nb_classifier import word_feats


#Load our classifier from file:
with open('classifier.pickle', 'rb') as rf:
    classifier = pickle.load(rf)

#Check most informative features (sanity check):
classifier.show_most_informative_features(15)

#Test the classifier on some example reviews:
test_review = ""
features = word_feats(word_tokenize(test_review))
classification = classifier.classify(features)
print("{}\n={}\n".format(test_review, classification))
