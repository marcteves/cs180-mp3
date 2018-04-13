#! /usr/bin/python3
# This script builds the dictionary by taking the 35 000 most common words
# from the training set
# the input of this is a concatenated result of all the extracted text
# generate by strip_mail.py
# https://stackoverflow.com/questions/40559008/sorting-and-counting-words-from-a-text-file?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
# > 2018
# > still using stackoverflow
# > ISHYGDDT
import argparse
import re
import sys
import traceback
import logging
from stemming.porter2 import stem

parser = argparse.ArgumentParser(description="""Given a text file, make three 
        dictionaries with the X most common words in that file, one for each
        special case.
        A word is a string of alphabetical characters delimited by 
        spaces.""")
parser.add_argument("input")
parser.add_argument("output")
parser.add_argument("words", default="35000")

args = parser.parse_args()

stop_words = [ "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", "further", "had", "has", "have", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "it", "it's", "its", "itself", "let's", "me", "more", "most", "my", "myself", "nor", "of", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "she'd", "she'll", "she's", "should", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "we", "we'd", "we'll", "we're", "we've", "were", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "would", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves" ]

with open(args.input, 'r', errors='replace') as textfile, \
        open(args.output, 'w') as dictionary, \
        open(args.output + '_nostop', 'w') as dictionary_nostop:

    # clean the text file first
    text = textfile.read()
    word_dict = {}

    words = text.split()

    for word in words:
        word_dict[word] = word_dict.get(word, 0) + 1

    word_count = 0
    for word in sorted(word_dict, key=word_dict.get, reverse=True):
        dictionary.write(word + "\n")
        # stop words are checked here
        if word not in stop_words and len(word) > 2:
            dictionary_nostop.write(word + '\n')
        word_count += 1
        if (word_count >= int(args.words)):
            break

# now build stem dictionary
with open(args.output + '_nostop', 'r') as dictionary, \
        open(args.output + '_stem', 'w') as dictionary_stem:

    text = dictionary.read().splitlines()
    stem_list = []
    for word in text:
        stemmed_word = stem(word)
        if stemmed_word not in stem_list:
            stem_list.append(stemmed_word)
            dictionary_stem.write(stemmed_word + '\n')
