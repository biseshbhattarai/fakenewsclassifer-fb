#Script that classifies the news . 
#Here initially two dataset is taken , one containing real news and the other containing fake news . After tokenizing the words and sentences . Word tagging is done , which classifies the type of word like (naam , sarbanam) . After tagging and classifing it then shuffle both the real and fake news and train it using various classifiers . After training using various classifier at the end it summarizes the result it received from all the classifiers and then use mode upon it and gives where it is fake news or real news . 
import nltk
import random
from nltk.tag import tnt 
from nltk.corpus import indian 
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize
from Nepali_nl.Nepali_nlp.Nepali_tokenizer import Tokenizer 

#Intializing class here 

class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf
#Dataset for both real news and fake news .     
short_pos = open("dataset/1405194780.txt","r").read()
short_neg = open("dataset/1449293640.txt","r").read()

all_words = []

documents = []
#Tagging the words and categoring its type 
trains = indian.tagged_sents('nepali.pos')
tnt_pos_tagger = tnt.TnT()
tnt_pos_tagger.train(trains) 

for p in short_pos.rsplit('\n'):
    #Tokeninzing and tagging the words for positive text 
	documents.append( (p, "real"))
	words = word_tokenize(p)
    #returns a tuple here 
	pos = tnt_pos_tagger.tag(words)
	for w in pos:
		all_words.append(w[0])

    
for p in short_neg.rsplit('\n'):
    #Tokeninzing and tagging the words for negative text 
    documents.append( (p, "fake") )
    words = word_tokenize(p)
    pos = tnt_pos_tagger.tag(words)
    for w in pos:
    	all_words.append(w[0].lower())


#pickling the documents so we don't have to use run it multiple times . 
save_documents = open("pickled_algos/documents.pickle","wb")
pickle.dump(documents, save_documents)
save_documents.close()

#gather all the words that are most frequently used .
all_words = nltk.FreqDist(all_words)


word_features = list(all_words.keys())[:5000]


save_word_features = open("pickled_algos/word_features5k.pickle","wb")
pickle.dump(word_features, save_word_features)
save_word_features.close()

#returns a dictionary , here it looks for the word in the news and its match in the dataset to find features .
def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

featuresets = [(find_features(rev), category) for (rev, category) in documents]
random.shuffle(featuresets)

testing_set = featuresets[0:]
training_set = featuresets[:355]


classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set))*100)


save_classifier = open("pickled_algos/originalnaivebayes5k.pickle","wb")
pickle.dump(classifier, save_classifier)
save_classifier.close()

MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set))*100)

save_classifier = open("pickled_algos/MNB_classifier5k.pickle","wb")
pickle.dump(MNB_classifier, save_classifier)
save_classifier.close()

BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(training_set)
print("BernoulliNB_classifier accuracy percent:", (nltk.classify.accuracy(BernoulliNB_classifier, testing_set))*100)

save_classifier = open("pickled_algos/BernoulliNB_classifier5k.pickle","wb")
pickle.dump(BernoulliNB_classifier, save_classifier)
save_classifier.close()

LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print("LogisticRegression_classifier accuracy percent:", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)

save_classifier = open("pickled_algos/LogisticRegression_classifier5k.pickle","wb")
pickle.dump(LogisticRegression_classifier, save_classifier)
save_classifier.close()


LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)

save_classifier = open("pickled_algos/LinearSVC_classifier5k.pickle","wb")
pickle.dump(LinearSVC_classifier, save_classifier)
save_classifier.close()



SGDC_classifier = SklearnClassifier(SGDClassifier())
SGDC_classifier.train(training_set)
print("SGDClassifier accuracy percent:",nltk.classify.accuracy(SGDC_classifier, testing_set)*100)

