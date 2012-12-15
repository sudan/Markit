"""
	Author : Sumanth Prabhu <sumanthprabhu.104@gmail.com> 
"""

from nltk import word_tokenize,pos_tag,FreqDist,NaiveBayesClassifier
from nltk.corpus import stopwords

import os
import pickle
import time

def SaveClassifier(classifier,name):
  fModel = open(name + '.pkl',"wb")
  pickle.dump(classifier, fModel,1)
  fModel.close()


def features_extractor(word_features,line):
	""" Extract features for training set"""
	training_set = []

	#access features from each sentence
	token_list = word_tokenize(line)
	
	feature = {}
	for word in word_features:
		feature['contains(%s)' % word] = (word in token_list)
	
	return feature


def get_word_features(lines):
	""" Create a reference word feature"""
	wordlist = []
	for line in lines:
		wordlist += word_tokenize(line)

	#remove stopwords
	wordlist = [w for w in wordlist if w not in stopwords.words('english')]
	
	#remove proper nouns
	taglist = pos_tag(wordlist)
	wordlist = [w for (w,tag) in taglist if tag != "NP" ]
	
	wordlist = FreqDist(wordlist)
	word_features = wordlist.keys()
	return word_features


def read_data(directory,filename):
	"""read data from file"""
	with open(os.path.join(directory,filename)) as f:
		lines = f.readlines()
	return lines


def get_features(directory,file1,file2,all = False):
	"""Extract data and features"""
	lines1 = read_data(directory,file1)

	lines2 = read_data(directory,file2)

	lines = lines1[:1000] + lines2[:1000]

	#create a reference word feature
	word_features = get_word_features(lines)

	if all: #require all 3 lists ( training)
		return (word_features,lines1,lines2)

	#Classification
	return word_features


def trainer():

	print "Building the training set for Level1 classifier.."
	t1 = time.time()
	word_features,lines_subj,lines_obj = get_features("subobj","subjective_data.txt","objective_data.txt",all=True)
	training_set = []

	for line in lines_subj[:1000]:
		feature = features_extractor(word_features,line)
		feature_tuple = [(feature,"subjective")]
		training_set += feature_tuple

	for line in lines_obj[:1000]:
		feature = features_extractor(word_features,line)
		feature_tuple = [(feature,"objective")]
		training_set += feature_tuple

	t2 = time.time()
	print "Training set built (Time taken = " + str(t2 - t1) + "s)"

	#train the sub_obj classifier
	print "Training the Level1 classifier"
	t1 = time.time()
	sub_obj_classifier = NaiveBayesClassifier.train(training_set)


	#store sub_obj
	SaveClassifier(sub_obj_classifier,"sub_obj_classifier")
	t2 = time.time()
	print "Level1 classifier trained and saved (Time taken = " + str(t2 - t1) + "s)"

	print "Building the training set for Level2 classifier"
	t1 = time.time()
	word_features,lines_pos,lines_neg = get_features("polarity","pos.txt","neg.txt",all=True)
	training_set = []

	for line in lines_pos[:1000]:
		feature = features_extractor(word_features,line)
		feature_tuple = [(feature,"positive")]
		training_set += feature_tuple

	for line in lines_neg[:1000]:
		feature = features_extractor(word_features,line)
		feature_tuple = [(feature,"negative")]
		training_set += feature_tuple

	t2 = time.time()
	print "Training set built (Time taken = " + str(t2 - t1) + "s)"

	#train the senti classifier
	print "Training the Level2 classifier"
	t1 = time.time()
	polarity_classifier = NaiveBayesClassifier.train(training_set)

	#Store polarity
	SaveClassifier(polarity_classifier,"polarity_classifier")
	t2 = time.time()
	print "Level2 classifier trained and saved (Time taken = " + str(t2 - t1) + "s)"

def main():
	trainer()

if __name__ == "__main__":
	main()