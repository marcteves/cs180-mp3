#! /usr/bin/python3
# This script scans a given email, extracts the text parts, and saves it to
# a file
# it is too difficult to write a program that would process all the emails
# in a satisfying manner, so we do our best by just removing the HTML tags
# when they are encountered
import email
import argparse
import os
import numpy as np
import sys
from html.parser import HTMLParser

class HTMLStripper(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = []
    def handle_data(self, data):
        self.data.append(data)
    def get_result(self):
        return u''.join(self.data)

parser = argparse.ArgumentParser(description="""Given a list of email files,
strip the text parts """)
parser.add_argument("filename", nargs="+")

args = parser.parse_args()

for filename in args.filename:
    with open(filename, 'r') as file_obj, \
    open('text/' + os.path.basename(filename), 'w') as write_obj:
        mail_file = file_obj.read()
        mail = email.message_from_string(mail_file)
        for part in mail.walk():
            if (part.get_content_maintype() == 'text'):
                if (part.get_content_subtype() == 'html'):
                    html_parser = HTMLStripper()
                    html_parser.feed(part.get_payload())
                    print(html_parser.get_result())
                    write_obj.write(html_parser.get_result())
                else:
                    print(part.get_payload())
                    write_obj.write(part.get_payload())
