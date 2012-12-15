"""
	Author : Sumanth Prabhu <sumanthprabhu.104@gmail.com> 
"""

from __future__ import print_function
from base import features_extractor
from base import get_features
import pickle
import os
import sys
import time

def validity(argv):
	""" Check for valid input """
	if len(argv) != 2:
		return [False,"Missing arguments"]
	try:
   		with open(sys.argv[1]) as f: 
   			pass
	except IOError as e:
   		return [False, str(e)]
   	else:
		return [True]


def LoadClassifier(name):
	""" Load the stored classifier """

	# os.system("gunzip " + name + ".pkl.gz")
  	fModel = open(name + '.pkl',"rb")
  	classifier = pickle.load(fModel)
  	fModel.close()
  	# os.system("gzip" + name + ".pkl")
  	return classifier


def classification(lines):
	""" classify the given input """
	print("Loading classifier...")
	classifier1 = LoadClassifier("sub_obj_classifier")
	classifier2 = LoadClassifier("polarity_classifier")

	print("Loading feature extractor..",end="")
	t1 = time.time()
	word_features1 = get_features("subobj","subjective_data.txt","objective_data.txt")
	word_features2 = get_features("polarity","pos.txt","neg.txt")
	t2 = time.time()

	print("(Time taken = " + str(t2-t1) + "s)")
	print("Classifying..")
	count = 1

	for line in lines:
		features1 = features_extractor(word_features1,line)
		if classifier1.classify(features1) == "subjective":
			features2 = features_extractor(word_features2,line)
			result = classifier2.classify(features2)
			print("Line" + str(count) + " :", result)	
			count += 1		
		else:
			print("Line" + str(count) + " :", "neutral")
			count += 1

def main():
	resp = validity(sys.argv)
	if resp[0]:
		with open(sys.argv[1]) as f:
			lines = f.readlines()
		
		classification(lines)
	else:
		print("Error :" + resp[1])


if __name__ == "__main__":
	main()