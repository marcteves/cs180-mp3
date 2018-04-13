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

parser = argparse.ArgumentParser(description="""Given a text file, make a 
        dictionary with the X most common words in that file.
        A word is a string of alphabetical characters delimited by 
        spaces.""")
parser.add_argument("input")
parser.add_argument("output")
parser.add_argument("words", default="35000")

args = parser.parse_args()


with open(args.input, 'r', errors='replace') as textfile, \
        open(args.output, 'w') as dictionary:

    # clean the text file first
    text = textfile.read()
    word_dict = {}

    words = text.split()

    for word in words:
        word_dict[word] = word_dict.get(word, 0) + 1

    word_count = 0
    for word in sorted(word_dict, key=word_dict.get, reverse=True):
        dictionary.write(word + "\n")
        word_count += 1
        if (word_count >= int(args.words)):
            break
