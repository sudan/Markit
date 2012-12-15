About Sentimental

Sentimental is a sentiment analyzer that analyzes the polarity of a set of statements and classifies the statement as "positive", "negative" or "neutral" using the naive bayes classifier. It uses but a very basic approach to identify keywords in a statement which reflect its polarity.

It makes use of two classifiers for the purpose:
1) subjective-objective classifier a.k.a Level1 classifier
   - Identifies whether the given statement is a subjective statement or an objective statement
   - Trained with 1000 subjective and 1000 objective statements picked from movie reviews
   - Takes 62 seconds to build the training set and 57 seconds to train the classifier

2) Polarity classifier a.k.a Level2 classifier
   - Classifies the given statement as positive or negative
   - Trained with 1000 positive and 1000 negative statements picked from movie reviews
   - Takes 51 seconds to build the training set and 52 seconds to train the classifier

Accuracy 
	Sentimental has an accuracy of 70.1%

Dependencies
nltk

How to run ?
Run base.py to train the classifier. Or you can directly run classifier.py with the already trained classifier available in the same directory.
python base.py
python classifier.py <test_file>