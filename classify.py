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

def compute_accuracy(classifier, test_vector, train_vector, test_tags, train_tags):

    predicted_tags = classifier.predict(test_vector)
    train_predicted = classifier.predict(train_vector)

    accuracy = sum(1 for x,y in zip(test_tags, predicted_tags) if x == y)
    accuracy += sum(1 for x,y in zip(train_tags, train_predicted) if x == y)
    accuracy = accuracy / (len(test_tags) + len(train_tags))
    return accuracy


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

print("Bernoulli accuracy:")
accuracy = compute_accuracy(classifier_b, test_vector, train_vector, test_tags, train_tags)
print(accuracy)

classifier_m = MultinomialNB()
classifier_m.fit(train_vector, train_tags)

print("Multinomial accuracy:")
accuracy = compute_accuracy(classifier_m, test_vector, train_vector, test_tags, train_tags)
print(accuracy)
alphas = [0.01, 0.1, 0.2, 0.5, 1]
accuracies = []
for alpha in alphas:
    classifier_m = MultinomialNB(alpha=alpha)
    classifier_m.fit(train_vector, train_tags)

    print("Multinomial accuracy with lambda %f:" % (alpha))
    accuracy = compute_accuracy(classifier_m, test_vector, train_vector, test_tags, train_tags)
    accuracies.append(accuracy)
    print(accuracy)

# plot alpha vs. accuracy
trace_data = go.Scatter(
        x = alphas,
        y = accuracies,
        mode = 'lines + markers',
        name = 'data',
        )

layout1 = go.Layout(
        title = 'plot using ' + args.train_set,
        xaxis = dict(
            title = 'lambda values',
            ),
        yaxis = dict(
            title = 'accuracy',
            ),
        )

figure_1 = go.Figure(data = [trace_data], layout = layout1)

plt.plot(figure_1, filename=args.train_set)
