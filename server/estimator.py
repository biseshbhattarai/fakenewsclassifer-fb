from nltk.stem import *
from nepali_stemmer.stemmer import NepStemmer
from nltk.corpus import stopwords
import pandas as pd
from nltk.tokenize import word_tokenize
from gensim import models
from gensim.similarities import WmdSimilarity
from Nepali_nl.Nepali_nlp.Nepali_tokenizer import Tokenizer 

def preprocesstext(sentence):
	NEPALI_SW = stopwords.words("nepali")
	tokens = Tokenizer().word_tokenize(sentence)
	return [NepStemmer().stem(x) for x in tokens if x not in NEPALI_SW]



def estimator(all_title):
	print('fdfd')
	
	nepali_stemmer = NepStemmer()
	
	# modellite = models.KeyedVectors.load("modellite")
	# news = open('online_khabar.txt', 'r')
	# title = news.read()Tokenizer
	newscorpus = [preprocesstext(news) for news in  all_title]
	print(newscorpus)
	# index = WmdSimilarity(newscorpus, modellite, num_best = 5)



