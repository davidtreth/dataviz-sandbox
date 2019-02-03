import os
dataPath = os.path.join(__file__,'..','..','..','data','steam_reviews')
posData = os.path.join(dataPath,'pos.txt')
negData = os.path.join(dataPath,'neg.txt')
import nltk
from nltk.tokenize import word_tokenize
import random
import pickle

#Create a list of stopwords:
from nltk.corpus import stopwords
import string
stopWords = list(set(stopwords.words('english')))
stopWords.extend(string.punctuation)


#Collect documents:
documents = []
#Load positive review data:
with open(posData, 'r', encoding='utf-8') as rf:
    posDocs = [(word_tokenize(review), 'pos') for review in rf.readlines()]
    random.shuffle(posDocs)
documents.extend(posDocs)
#Load negative review data:
with open(negData, 'r', encoding='utf-8') as rf:
    negDocs = [(word_tokenize(review), 'neg') for review in rf.readlines()]
    random.shuffle(negDocs)
documents.extend(negDocs)


def word_feats(words):
    """
    A function to convert a word tokenized list to the 'word feature'
    format expected by the classifier.
    """
    return dict([(word.lower(), True) for word in words if word not in stopWords])


#Construct our datasets for training and evaluation:
train_data = posDocs[50:1050] + negDocs[50:1050]
eval_data = posDocs[:50] + negDocs[:50]
train_set = [(word_feats(rev), category) for (rev, category) in train_data]
eval_set = [(word_feats(rev), category) for (rev, category) in eval_data]

#Train our classifier:
classifier = nltk.NaiveBayesClassifier.train(train_set)

#Perform some basic analysis:
print("Naive Bayes Algo accuracy: {}".format(
    nltk.classify.accuracy(classifier, eval_set)
))
classifier.show_most_informative_features(15)

#Test our model before deciding to .pickle it:
test_pos_review = "great game! i had a lot of fun with the multiplayer."
test_neg_review = "waste of money. you shouldn't buy this game in its current state."
feats = word_feats(word_tokenize(test_neg_review))
classification = classifier.classify(feats)
print(classification)

#.pickle (save) our model for the future:
with open('classifier.pickle', 'wb') as wf:
    pickle.dump(classifier, wf)
