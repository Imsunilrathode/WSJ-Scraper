"""
Readme
==========
Author: Sunil
Date: Jan 27 2018

Get title, sub_headline, epoch-publish-milliseconds ,article_section
and article_body 200 words of body content from article html path.

The program will generate json file for each day.
COMMAND LINE EXECUTION EXAMPLE:
===============================
C:\Users>python <FILE_NAME> <destination_path>

C:\Users\Sunil>python2 wsj_parser.py "D:\data" "D:\parsed-data" 2>errorlog.txt

"""

import os
from bs4 import BeautifulSoup
import codecs
import sys
import calendar
import datetime
import itertools
import re
import json
import sys

reload(sys)
sys.setdefaultencoding('utf8')
# source file path
path = sys.argv[1]
out_path = sys.argv[2]


# parse html files to json format
def html2json(file_path):
    record_dict = {}
    path1 = r'%s' % file_path
    page = codecs.open(path1, 'r')

    soup = BeautifulSoup(page, "lxml")

    timestamp = soup.find('meta',{'name':'article.published'})["content"]
    if timestamp:
        utc_time = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.000Z")
        pub_epoch_time = calendar.timegm(utc_time.timetuple()) + (utc_time.microsecond / 1000000.)
        record_dict[int(pub_epoch_time)] = {}
    else:
        return None
    try:
        article_section = soup.find('meta', {'name': 'article.section'})["content"]
    except:
        article_section = ""
    try:
        title = soup.find('meta', {'name': 'article.origheadline'})["content"].encode('utf-8')
    except:
        title = ""
    try:
        sub_head = soup.find('h2', {'class': 'sub-head'}).text.encode('utf-8')
    except:
        sub_head = ""
    try:
        author = soup.find('meta',{'name':'author'})["content"]
    except:
        author = ""
    try:
        article_body = soup.find('div',{'class':'wsj-snippet-body'}).find_all('p')
        article_body = ' '.join(each.getText().encode('utf-8') for each in article_body)
    except:
        article_body = ""


    record_dict[pub_epoch_time]["article_section"] = article_section
    record_dict[pub_epoch_time]["title"] = title
    record_dict[pub_epoch_time]["sub_head"] = sub_head
    record_dict[pub_epoch_time]["author"] = author
    record_dict[pub_epoch_time]["article-body"] = article_body

    return record_dict


# Read each folder inside file path
for folder in os.listdir(path):
    full_json = {}
    json_format = ''

    print >> sys.stdout,folder +"     processing"

    for each in os.listdir(path + "//" + folder):
        filename = path + "//" + folder + "//" + each
        # function call to html2json
        filedata = html2json(filename)

        # error logs
        if filedata:
            full_json.update(filedata)
        else:
            print >> sys.stderr, "    Error file with incomplete content   " + filename
            continue

    # print(full_json)
    # check json_format is empty or not.
    if not full_json:
        print >> sys.stderr, "Error folder with size 0    " + folder
        continue


    output_filepath = out_path + "\\" + folder + ".json"

    # write json
    with open(output_filepath, 'wb') as f:
        f.write(json.dumps(full_json, indent=2, sort_keys=True, ensure_ascii=False).encode('utf8'))
