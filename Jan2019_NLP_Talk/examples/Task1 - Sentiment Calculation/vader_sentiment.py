"""
"""
from nltk.tokenize import word_tokenize, sent_tokenize
from vader_lexicon import loadLexicon

def get_features(review):
    lexicon = loadLexicon()

    features = []
    for sentence in sent_tokenize(review):
        sentFeatures = []
        for word in word_tokenize(sentence):
            if word in lexicon:
                sentFeatures.append((word,lexicon[word]))
        #Do some maths to calculate score. See functions below.
        # print(sentFeatures)
        features.append(sentFeatures)

    return features


def feat_to_score_1(features):
    """
    Average the sentiment for sentences, then average for all sentences.
    """
    scores = []
    for sent in features:
        sentScores = [item[1] for item in sent]
        avgSentScore = sum(sentScores) / len(sentScores)
        scores.append(avgSentScore)
    sentiment = sum(scores) / len(scores)
    return sentiment

def feat_to_score_2(features):
    """
    Simple average of all features in text.
    """
    scores = []
    for sent in features:
        scores.extend([item[1] for item in sent])
    sentiment = sum(scores) / len(scores)
    return sentiment


if __name__ == "__main__":
    review = "Always Sunny is off to a strong start now that it's proven that it can still pull off twists after more than a decade on the air."
    review2 = "what a great game, it's inspiring how much they crammed into this gem! I can't wait to enjoy the sequel."

    features = get_features(review2)
    print("Method 1: {}".format(feat_to_score_1(features)))
    print("Method 2: {}".format(feat_to_score_2(features)))
