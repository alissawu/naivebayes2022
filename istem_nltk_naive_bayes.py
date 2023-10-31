# -*- coding: utf-8 -*-
"""iSTEM_nltk_Naive Bayes.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aSJW-V32xHMgfBA-UEoLOh5jtjNN66_7

# Importing nltk & other libraries for preprocessing text
"""

from dataclasses import dataclass
import nltk
nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download('stopwords')
import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')

# Read in sentence data from CSV
data = pd.read_csv("all-data 2.csv")
print(data)
# Lowercase
data["Sentence"] = data["Sentence"].str.lower()

# Remove punctuation
data["Sentence"] = data["Sentence"].str.replace("[^a-zA-Z]", " ")

# Tokenize sentences
data["Sentence"] = data["Sentence"].apply(word_tokenize)

# Remove stopwords
stop_words = set(stopwords.words('english'))
data["Sentence"] = data["Sentence"].apply(lambda x: [item for item in x if item not in stop_words])

# Stem words w/ Snowball stemmer
stemmer = SnowballStemmer('english')
data["Sentence"] = data["Sentence"].apply(lambda x: [stemmer.stem(y) for y in x])

print(data)

# TRAIN-TEST SPLIT
from sklearn.model_selection import train_test_split
X = data['Sentence']
y = data['Sentiment']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)  # 0.8:0.2 split

# VECTORIZATION
from sklearn.feature_extraction.text import CountVectorizer

# Concatenate the lists of words into a single string
X_train = X_train.apply(lambda x: ' '.join(x))
X_test = X_test.apply(lambda x: ' '.join(x))

# Create the vocabulary
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

from sklearn.naive_bayes import MultinomialNB

num_models = 5  # Number of Naive Bayes models to train
predictions = []  # List to store predictions from all models

alpha = 1  # Laplace smoothing factor, highest accuracy at a=1 from 1-10

for i in range(num_models):
    # Train the Naive Bayes classifier with Laplace smoothing
    classifier = MultinomialNB(alpha=alpha)
    classifier.fit(X_train, y_train)

    # Predict the sentiment for the test data using the trained model
    y_pred = classifier.predict(X_test)
    predictions.append(y_pred)

# Combine predictions using majority voting
label_mapping = {'negative': 0, 'neutral': 1, 'positive': 2} #must be pos values
converted_predictions = np.vstack([[label_mapping[p] for p in pred] for pred in predictions])
combined_predictions = np.mean(converted_predictions, axis=0).astype(int)

# Evaluate the performance of the combined model on the testing set
from sklearn.metrics import accuracy_score, classification_report

# Convert string labels to numeric labels in y_test
y_test_numeric = np.array([label_mapping[label] for label in y_test])

# Evaluate the performance of the combined model on the testing set
print("Accuracy:", accuracy_score(y_test_numeric, combined_predictions))
print("Classification Report:")
print(classification_report(y_test_numeric, combined_predictions, target_names=label_mapping.keys()))