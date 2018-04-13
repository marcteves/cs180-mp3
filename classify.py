#! /usr/bin/python3
# This script scans the extracted text of an email and returns the
# corresponding feature vector.
import email
import argparse
import csv
import os
import sys
import traceback
import logging
import numpy as np
import scipy.sparse as ss
import plotly.offline as plt
import plotly.graph_objs as go
from sklearn.naive_bayes import BernoulliNB 
from sklearn.naive_bayes import MultinomialNB 

def read_tags (filename):
    with open(filename,'r') as tag_file:
        tag_lines = tag_file.read().splitlines()
        tag_lines = [ int(x) for x in tag_lines ]
        return tag_lines

parser = argparse.ArgumentParser(description="""Takes four files as input,
        returns a vector classifying the test set""")
parser.add_argument("train_set")
parser.add_argument("train_tags")

parser.add_argument("test_set")
parser.add_argument("test_tags")

args = parser.parse_args()

train_vector = ss.load_npz(args.train_set)
train_tags = read_tags(args.train_tags)
test_vector = ss.load_npz(args.test_set)
test_tags = read_tags(args.test_tags)


classifier_b = BernoulliNB()
classifier_b.fit(train_vector, train_tags)

predicted_tags = classifier_b.predict(test_vector)

accuracy_b = sum(1 for x,y in zip(test_tags, predicted_tags) if x == y)
accuracy_b = accuracy_b / len(test_tags)

print("Bernoulli accuracy:")
print(accuracy_b)

classifier_m = MultinomialNB()
classifier_m.fit(train_vector, train_tags)

predicted_tags = classifier_m.predict(test_vector)

accuracy_m = sum(1 for x,y in zip(test_tags, predicted_tags) if x == y)
accuracy_m = accuracy_m / len(test_tags)

print("Multinomial accuracy:")
print(accuracy_m)
alphas = [0.01, 0.1, 0.2, 0.5, 1]
accuracies = []
for alpha in alphas:
    classifier_m = MultinomialNB(alpha=alpha)
    classifier_m.fit(train_vector, train_tags)

    predicted_tags = classifier_m.predict(test_vector)

    accuracy_m = sum(1 for x,y in zip(test_tags, predicted_tags) if x == y)
    accuracy_m = accuracy_m / len(test_tags)
    print("Multinomial accuracy with lambda %f:" % (alpha))
    accuracies.append(accuracy_m)
    print(accuracy_m)

# plot alpha vs. accuracy
trace_data = go.Scatter(
        x = alphas,
        y = accuracies,
        mode = 'lines + markers',
        name = 'data',
        )

layout1 = go.Layout(
        title = 'plot using' + args.train_set,
        xaxis = dict(
            title = 'lambda values',
            ),
        yaxis = dict(
            title = 'accuracy',
            ),
        )

figure_1 = go.Figure(data = [trace_data], layout = layout1)

plt.plot(figure_1, filename=args.train_set)
