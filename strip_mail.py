#! /usr/bin/python3
# This script scans a given email, extracts the text parts, and saves it to
# a file
# it is too difficult to write a program that would process all the emails
# in a satisfying manner, so we do our best by just removing the HTML tags
# when they are encountered
# if the text part is encoded in something that isn't an english encoding, 
# the email is ignored.
import email
import argparse
import os
import numpy as np
import sys
import traceback
import logging
from html.parser import HTMLParser

class HTMLStripper(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = []
    def handle_data(self, data):
        self.data.append(data)
    def get_result(self):
        return u''.join(self.data)
    def data_clear(self):
        self.data = []

parser = argparse.ArgumentParser(description="""Given a list of email files,
strip the text parts """)
parser.add_argument("filename", nargs="+")

args = parser.parse_args()

# These are all the reasonable english encodings. If it fails here, then it's
# safe to just ignore the email.
encodings = ['utf-8','utf-7','latin_1']
# actually, it doesn't fail in latin_1, but it returns some useless gibberish 
# interspersed with real legit stuff
html_parser = HTMLStripper()
print("Mail strip started")

for filename in args.filename:
    success = False
    write_path = 'text/' + os.path.basename(filename)
    for e in encodings:
        try:
            with open(filename, 'r', encoding=e) as file_obj, \
            open(write_path, 'w') as write_obj:
                mail_file = file_obj.read()
                mail = email.message_from_string(mail_file)
                for part in mail.walk():
                    if (part.get_content_maintype() == 'text'):
                        try:
                            if (part.get_content_subtype() == 'html'):
                                html_parser.feed(part.get_payload())
                                write_obj.write(html_parser.get_result())
                                html_parser.reset()
                                html_parser.data_clear()
                            else:
                                write_obj.write(part.get_payload())
                        except Exception as e:
                            logging.error(traceback.format_exc())
            success = True
            print("Processing %s success!" % (filename))
            break
        except UnicodeDecodeError as e:
            print("Unicode error with file %s using %s" % (filename, e))
            logging.error(traceback.format_exc())
    if not success:
        print("Processing %s FAILURE!" % (filename))
        try:
            os.remove(write_path)
        except OSError:
            pass
