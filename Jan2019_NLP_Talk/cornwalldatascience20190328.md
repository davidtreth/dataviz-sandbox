% Sentiment Analysis – Lightning talk – Data Science Cornwall 
% David Trethewey
% 28/03/2019

Using NLTK in Python and visualisation in matplotlib
====================================================

As a 5 minute lightning talk, following up to the [previous talk on 31st January 2019 talk by Peter Conway to the Data Science Cornwall Group](https://www.meetup.com/datasciencecornwall/events/254352933/) I focused on generating some basic statistics on the game reviews, and plotting some figures using `matplotlib`.

Sentiment of the words
----------------------
The sentiment of a number of words is given in a lexicon in [nltk.sentiment.vader.SentimentIntensityAnalyzer](http://www.nltk.org/_modules/nltk/sentiment/vader.html)

[Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for
Sentiment Analysis of Social Media Text. Eighth International Conference on
Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.](http://comp.social.gatech.edu/papers/icwsm14.vader.hutto.pdf)

The main code used are in the files [vader.py](vader.py), where the lexicon is read in, and saved to a `pickle` file, and the [gamereviews.py](gamereviews.py) file where the main code that reads in the game reviews, calculates basic statistics, and a few figures.

The Jupyter notebook  [Example_pos_neg_reviews_sentimentscores.ipynb](Example_pos_neg_reviews_sentimentscores.ipynb) takes a random example of a positive and a negative review, and shows what is happening when it is split into sentences, checked for negation, and scored for sentiment.

Checking the methodology
------------------------

Is a naive equivalance of more positive words = positive review accurate?

Does it look different when you move from a global view to a per review view?

![All lexicon words in positive reviews](positivegames_alllexiconwords.png)

![All lexicon words in negative reviews](negativegames_alllexiconwords.png)

![Histogram of sentiment score for lexicon words in positive reviews. There are more positive than negative words in positive reviews, but a fairly substantial minority of words are negative](positivegames_histogram.png)

![Histogram of sentiment score for lexicon words in negative reviews. There are a larger proportion of negative words in negative reviews than in positive reviews. Note there are still quite a lot of positive words in negative reviews, but few very positive words with sentiment > 0.6 or so.](negativegames_histogram.png)

Instead of looking at a histogram of the sentiment every word, we can measure the median of each review's sentiment. This could help avoid the effect of outliers, but some positive reviews have a median sentiment score that is negative.

![The median sentiment score in every positive review](positivegames_median.png)

![The median sentiment score in every negative review](negativegames_median.png)


Some negative reviews have a *minimum* sentiment score well into positive territory:

![The minimum sentiment score in every positive review](positivegames_min.png)
![The minimum sentiment score in every negative review](negativegames_min.png)

However, very few positive reviews have only negative words:

![The maximum sentiment score in every positive review](positivegames_max.png)
![The maximum sentiment score in every negative review](negativegames_max.png)


Testing a hypothesis
--------------------

* Does the length of a review have a correlation with sentiment?

![Positive reviews: median scaled word sentiment score vs. number of tokens in lexicon. Positive reviews made up of negative words tends to decline with the length of the review.](positivegames1.png)

![Negative reviews: median scaled word sentiment score vs. number of tokens in lexicon. Negative reviews seem to have a bimodal distribution which tends to be more the case for longer reviews, perhaps reviewers tend to either use negative words, or negated positive words consistently, and more so for longer than shorter reviews.
](negativegames1.png)

Rather than long rants full of negativity, the most negative reviews are short.

Naive negation
--------------

If a word is negated, e.g. not good, its sentiment may be inverted compared to what it would be in a positive sentence.
The [nltk.sentiment.vader.SentimentIntensityAnalyzer](http://www.nltk.org/_modules/nltk/sentiment/vader.html) tools provide a function to decide whether a sentence is negated. 
This is a fairly naive method, since all it is doing is checking for a list of keywords that may imply negation.
In the code in gamereviews.py I use NLTKs sentence tokenization method and multiply the sentiments in any negated sentence by -1 (the `negation` variable).

~~~~~~~~~
import pickle
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize
import matplotlib.pyplot as plt
from nltk.sentiment.vader import negated

negation = -1

# using sentence tokenization
# if a sentence contains negation, flip the sentiment values.
self.sentences = [s for s in sent_tokenize(reviewtext)]
self.sentnegated = np.zeros(len(self.sentences))
self.sentlextok_kvtup_2 = []
self.lextok_kvtup_2 = []
    for i,s in enumerate(self.sentences):
        sentencetokens = [t.lower() for t in word_tokenize(s)]
        sentntokens = len(sentencetokens)
        sentlextokens = [t for t in sentencetokens if t in lexicon]
        if negated(sentencetokens):                        
            sentlextok_kvtup = [("NEG:"+t,negation*lexicon[t]) for t in sentlextokens]
            self.sentnegated[i] = 1
        else:
            sentlextok_kvtup = [(t,lexicon[t]) for t in sentlextokens]    
            self.lextok_kvtup_2.extend(sentlextok_kvtup)
            self.sentlextok_kvtup_2.append(sentlextok_kvtup)
~~~~~~~~~

Results taking account of negation
----------------------------------
![All lexicon words in positive reviews, with negation](withneg_positivegames_alllexiconwords.png)

![All lexicon words in negative reviews, with negation](withneg_negativegames_alllexiconwords.png)

![Histogram of sentiment score, with negation, for lexicon words in positive reviews. This now has a lot more negative words.](withneg_positivegames_histogram.png)

![Histogram of sentiment score, with negation, for lexicon words in negative reviews. Accounting for negation has increased the number of negative words, but there remain a large proportion of positive words.](withneg_negativegames_histogram.png)

![The median sentiment score in every positive review, with negation.](withneg_positivegames_median.png)

![The median sentiment score in every negative review, with negation.](withneg_negativegames_median.png)

![The minimum sentiment score in every positive review, with negation.](withneg_positivegames_min.png)

![The minimum sentiment score in every negative review, with negation.](withneg_negativegames_min.png)

![The maximum sentiment score in every positive review, with negation.](withneg_positivegames_max.png)

![The maximum sentiment score in every negative review, with negation.](withneg_negativegames_max.png)

Possible problems
-----------------

As an example:

~~~~~~
for n,s, kv in zip(posrev_ex.sentnegated, posrev_ex.sentences, posrev_ex.sentlextok_kvtup_2):
    if n==1:
        print("Negated sentence:", end=" ")    
    print(s)
    print(kv)
    print("\n")

Zombies is really fun, much more light-hearted tone than Treyarch's versions and IW have done quite a good job distancing themselves from it.
[('fun', 0.575), ('good', 0.475)]


The 80s aesthetic, the hoff and the soundtrack are all really great.
[('great', 0.775)]


The inclusion of some weapons from the past is also pretty neat too.
[('weapons', -0.475), ('pretty', 0.55), ('neat', 0.5)]


Overall, really fun.
[('fun', 0.575)]


Negated sentence: The themepark has tonnes of great minigames that you can sort of relax on for a bit, taking a break from the zombie killing and all.Multiplayer isn't nearly as great.
[('NEG:great', -0.775), ('NEG:relax', -0.475), ('NEG:killing', 0.85), ('NEG:great', -0.775)]


IW have tried to implement all these abilities that make you go fast but the gameplay itself just feels dreadfully slow.
[('abilities', 0.25), ('dreadfully', -0.675)]


Negated sentence: Titanfall 2 does this sort of movement system much more better and I would suggest that if you're looking for fast jet-packing action that you just go play that instead.I haven't got around to Campaign yet but I would recommend this purchase on zombies alone (especially with friends)
[('NEG:better', -0.475), ('NEG:play', -0.35), ('NEG:recommend', -0.375), ('NEG:alone', 0.25), ('NEG:friends', -0.525)]


~~~~~~

The sentence tokenization sometimes doesn't work because spaces after full-stops are often missing in the reviews. Either with this problem, or a long sentence with subordinate clauses etc., words may be overclassified as being in negative sentences.

Also, some words, such as "weapons", or "killing" might generally have negative connotations, but not necessarily in the context of a shoot-'em up computer game.

Conclusions
-----------
* Using this method doesn't allow us to make conclusions about the overall sentiment of individual reviews.
* It is important to understand the data issues that may cause problems with how something is being processed, e.g. reviews that are formatted in a non-standard way confusing sentence tokenization.
* To improve the results, it could be necessary to have a more fine-grained approach to working out what words are governed by negation, rather than simply applying it to a whole sentence