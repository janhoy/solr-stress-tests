#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Convert stackexchange xml to solr input json
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))
import argparse
import json
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from time import strftime


def read_config():
    parser = argparse.ArgumentParser(description='Convert stackexchange xml to json')
    parser.add_argument('--fromFile', default='cooking.stackexchange.com/Posts.xml', help='From file')
    parser.add_argument('--toFile', default='cooking.json', help='To file')
    return parser.parse_args()


def main():
    conf = read_config()
    tree = ET.parse(conf.fromFile)
    root = tree.getroot()
    num_docs = 0
    with open(conf.toFile, 'w') as jsonOut:
        solr_docs = []
        for post in root:
            solr_doc = {'id': post.attrib['Id'],
                        'PostTypeId': post.attrib['PostTypeId'],
                        'CreationDate': post.attrib['CreationDate']+'Z',
                        'Score': post.attrib['Score'],
                        'Body': post.attrib['Body'],
                        'CommentCount': post.attrib['CommentCount'],
                        }

            if 'ParentId' in post.attrib.keys():
                solr_doc['ParentId'] = post.attrib['ParentId']
            if 'AnswerCount' in post.attrib.keys():
                solr_doc['AnswerCount'] = post.attrib['AnswerCount']
            if 'Tags' in post.attrib.keys():
                solr_doc['Tags'] = post.attrib['Tags']
            if 'Title' in post.attrib.keys():
                solr_doc['Title'] = post.attrib['Title']
            if 'LastEditDate' in post.attrib.keys():
                solr_doc['LastEditDate'] = post.attrib['LastEditDate'] + 'Z'
            if 'OwnerUserId' in post.attrib.keys():
                solr_doc['OwnerUserId'] = post.attrib['OwnerUserId']
            solr_docs.append(solr_doc)
            num_docs += 1

        json.dump(solr_docs, jsonOut, ensure_ascii=False, indent=2)
    print("Done, %d docs written" % num_docs)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nReceived Ctrl-C, exiting early')
