#! /usr/bin/python3
import email
import argparse
import os
import sys
import traceback
import logging
import re

parser = argparse.ArgumentParser(description="""Given a dictionary and a file
containing a list of text files, write the ham-spam vector of each text file""")
parser.add_argument("reference")
parser.add_argument("output")
parser.add_argument("input")

args = parser.parse_args()

with open(args.input, 'r') as input_file, \
        open(args.reference, 'r') as ref_file, \
        open(args.output, 'w') as out_file:
    input_list = input_file.read().splitlines()
    ref_list = ref_file.read().splitlines()

    for line in input_list:
        line_number = int(line.partition("inmail.")[-1]) - 1
        ham_or_spam = ref_list[line_number].split()[0]
        if (ham_or_spam == "spam"):
            out_file.write("1\n")
        else:
            out_file.write("0\n")
