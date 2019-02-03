#!/usr/bin/python3
# -*- coding: utf-8 -*-
# based on 31st January 2019 talk by Peter Conway to Data Science Cornwall Group
# https://www.meetup.com/datasciencecornwall/events/254352933/
# this was to work on the first task set in the slides
# to calculate a score to represent each review's sentiment
# My approach is to visualise the data using matplotlib


import os
import time
import pickle
import numpy as np
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt

class GameReview:
	def __init__(self, reviewtext):
		self.reviewtext = reviewtext
		self.tokens = [t.lower() for t in word_tokenize(reviewtext)]
		self.ntokens = len(self.tokens)
		# create a list of tokens including only those in the lexicon
		self.lexicontokens = [t for t in self.tokens if t in lexicon]
		# create a list of tuples of token, sentiment score
		self.lextok_kvtup = [(t,lexicon[t]) for t in self.lexicontokens]		
		# sort by value
		self.sorted_lextokens = sorted(self.lextok_kvtup,key=lambda kvtup:kvtup[1])		
		self.ntokens_lexicon = len(self.lexicontokens)
		self.sentiments = np.array([tv[1] for tv in self.sorted_lextokens])
		self.createStats()
			
	def createStats(self):
		if len(self.sentiments) > 0:
			self.minSentiment = np.min(self.sentiments)
			self.maxSentiment = np.max(self.sentiments)
			self.medianSentiment = np.median(self.sentiments)
			self.meanSentiment = np.mean(self.sentiments)
		else:
			self.minSentiment = 0
			self.maxSentiment = 0
			self.medianSentiment = 0
			self.meanSentiment = 0
			
	
	def printLexiconTokens(self):
		""" output the tokens that are in lexicon along 
		with their sentiment scores to terminal """
		for tv in self.lextok_kvtup:
			print("{t}: {s}".format(t=tv[0],s=tv[1]), end=" ")
		print("\n")
					
	def printSortedLexiconTokens(self):
		""" output the tokens that are in lexicon along 
		with their sentiment scores to terminal sorted by value """		
		for tv in self.sorted_lextokens:
			print("{t}: {s}".format(t=tv[0],s=tv[1]), end=" ")
		print("\n")
			
	def printStatsSentiment(self):
		""" output the basic stats for a review """
		print("N tokens in review = {n}".format(n=self.ntokens))
		if self.ntokens > 0:
			print("N tokens in review in lexicon = {n} ({p:.2%})".format(n=self.ntokens_lexicon,
			p = self.ntokens_lexicon/self.ntokens))
			if self.ntokens_lexicon > 0:
				print("lowest sentiment score = {s}".format(s=self.minSentiment))			
				print("median sentiment score = {s}".format(s=self.medianSentiment))
				print("mean sentiment score = {s:.3f}".format(s=self.meanSentiment))
				print("max sentiment score = {s}".format(s=self.maxSentiment))
				
def plotReviews(list_rev, titletext, Nfig=0):
	""" plot the minimum, maximum and median scores for each review """
	minscores = [r.minSentiment for r in list_rev]
	maxscores = [r.maxSentiment for r in list_rev]
	medianscores = [r.medianSentiment for r in list_rev]
	xvals = np.arange(len(list_rev)) + 1
	plt.figure(Nfig+1, [6,12])
	plt.xlabel("review")
	plt.xlabel("review")
	plt.ylabel("min sentiment score [-1,1]")
	plt.plot(xvals, minscores, 'b.')
	plt.title(titletext)
	plt.figure(Nfig+2, [6,12])
	plt.xlabel("review")
	plt.ylabel("max sentiment score [-1,1]")
	plt.plot(xvals, maxscores, 'r.')
	plt.title(titletext)
	plt.figure(Nfig+3, [6,12])
	plt.plot(xvals, medianscores, 'k.')
	plt.xlabel("review")
	plt.ylabel("median sentiment score [-1,1]")
	plt.title(titletext)
							
# load the lexicon from pickle
with open('lexicon.pickle', 'rb') as f:
   lexicon = pickle.load(f)

# get the reviews   
gamereviewdir = os.path.join("data","steam_reviews")
posfile = os.path.join(gamereviewdir, "pos.txt")
negfile = os.path.join(gamereviewdir, "neg.txt")

# open positive reviews
with open(posfile, 'r') as f:
	posreviews = f.readlines()
	
# open negative reviews
with open(negfile, 'r') as f:
	negreviews = f.readlines()

# generate the review objects for positive reviews
posreview_objs = []
for r in posreviews:
	print(r)
	revobj = GameReview(r)
	posreview_objs.append(revobj)
	revobj.printSortedLexiconTokens()
	revobj.printStatsSentiment()
	print("\n" + "-"*80)
	
print("total of {n} positive reviews".format(n=len(posreview_objs)))
posreviews_lextokens = [r for r in posreview_objs if r.ntokens_lexicon > 0]
print("total of {n} positive reviews with at least one token within lexicon".format(n=len(posreviews_lextokens)))

plotReviews(posreviews_lextokens, "Sentiment score for words in lexicon in positive reviews")

plt.tight_layout()

# generate the review objects for positive reviews
negreview_objs = []
for r in negreviews:
	print(r)
	revobj = GameReview(r)
	negreview_objs.append(revobj)
	revobj.printSortedLexiconTokens()
	revobj.printStatsSentiment()
	print("\n" + "-"*80)
	
print("total of {n} negative reviews".format(n=len(negreview_objs)))
negreviews_lextokens = [r for r in negreview_objs if r.ntokens_lexicon > 0]
print("total of {n} negative reviews with at least one token within lexicon".format(n=len(negreviews_lextokens)))
			
plotReviews(negreviews_lextokens, "Sentiment score for words in lexicon in negative reviews", 3)

plt.tight_layout()

plt.show()
