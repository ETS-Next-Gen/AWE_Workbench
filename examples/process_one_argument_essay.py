#!/usr/bin/env python3.10
# Copyright 2022, Educational Testing Service

import csv
import re
import os
import math
import names
import openpyxl
import pandas as pd
import random
import threading
from awe_workbench.web.websocketClient import websocketClient
from awe_languagetool.languagetoolClient import languagetoolClient
import nltk
from nltk.corpus import stopwords
import argparse

nltk.download('stopwords')
stopWords = set(stopwords.words('english'))

batch_size = 1


def initialize():
    """
    Initialize our CorpusSpellcheck and parser objects
    (for spell-correction and parsing with spacy + coreferee
    and other extensions using a modified version of the
    holmes extractor library. While doing so, we initialize
    a series of lexical databases that support some of the
    metrics we want to capture.
    """
    # Initialize the spellchecker
    cs = websocketClient()
    lt = languagetoolClient()

    # Initialize the parser
    parser = websocketClient()
    parser.set_uri("ws://localhost:8766")

    # return spellchecker and parser objects
    return cs, parser, lt


def normalize(text):
    text = text.replace('&nbsp;', ' ')
    text = text.replace('  ', ' ')
    text = text.replace(' .', '.')
    text = text.replace(' ,', ',')
    text = text.replace(' ;', ';')
    text = text.replace(' :', ':')
    text = text.replace(' !', '!')
    text = text.replace(' ?', '?')
    text = text.replace(' \'s', '\'s')
    text = text.replace(' \'d', '\'d')
    text = text.replace(' \'ve', '\'ve')
    text = text.replace(' \'ll', '\'ll')
    text = text.replace(' n\'t', 'n\'t')
    text = text.replace(' n''t', 'n\'t')
    text = text.replace(' ’s', '\'s')
    text = text.replace(' ’d', '\'d')
    text = text.replace(' ’ve', '\'ve')
    text = text.replace(' ’ll', '\'ll')
    text = text.replace(' n’t', 'n\'t')
    text = text.replace(' - ', '-')
    text = text.replace('"', '" ')
    text = text.replace(' ”', '”')
    text = text.replace('“ ', '“')
    text = text.replace(' "', '"')
    text = text.replace('  ', ' ')
    text = re.sub(r'" (.*?)" ', r' "\1" ', text)

    return text


if __name__ == '__main__':

    cs, parser, lt = initialize()

    argparser = argparse.ArgumentParser(description="Parse a student text file")
    argparser.add_argument(
        '--filename',
        default="essays/gre6.txt",
        help='Which file to parse'
    )

    args = argparser.parse_args()
    doc = open(args.filename).read()

    text = None
    with open('essays/gre6.txt') as f:
        text = f.read()
    record = {}
    result = lt.processText(record, text)
    if result is None:
        raise Exception("No correction information received")

    print(result)
    lastoffset = 0
    lastlength = 0
    outhtml = '<!DOCTYPE html><html><head></head><body>'
    errorcounts = {}
    detailcounts = {}
    for item in result:

        if item['label'] in errorcounts:
            errorcounts[item['label']] += 1
        else:
            errorcounts[item['label']] = 1

        if item['label'] + '/' + item['detail'] \
           in detailcounts:
            detailcounts[item['label']
                         + '/'
                         + item['detail']] += 1
        else:
            detailcounts[item['label']
                         + '/'
                         + item['detail']] = 1
        outhtml += text[lastoffset: item['offset']]
        outhtml += \
            '<error class="highlight", type=\"' \
            + item['label'] \
            + '" subtype="' \
            + item['detail'] \
            + '" title="' \
            + item['message'] \
            + '">'
        outhtml += \
            text[item['offset']: item['offset'] + item['length']]
        outhtml += '</error>'
        lastoffset = item['offset'] + item['length']
        lastlength = item['length']
    outhtml += text[lastoffset+lastlength:]
    outhtml += '</body></html>'
    print(outhtml)
    total = 0
    for key in sorted(errorcounts.keys()):
        total += errorcounts[key]
    print('\nTotal grammar, usage, mechanics, style errors:',
          total)
    print('\n-------Major error categories--------------------')
    for key in sorted(errorcounts.keys()):
        print(key, ':', errorcounts[key])
    print('\n-------Minor error categories--------------------')
    for key in sorted(detailcounts.keys()):
        print(key, ':', detailcounts[key])

    [corrected] = cs.send([text])
    print(corrected)

    ok = parser.send(['PARSEONE', 'sample', corrected])
    if ok is None:
        raise Exception("Parse Failed")

    tokens = parser.send(['DOCTOKENS', 'sample'])
    if tokens is None:
        raise Exception("No tokens retrieved")

    sentences = parser.send(['SENTENCES', 'sample'])
    if sentences is None:
        raise Exception("No sentences recognized")
    paragraphs = parser.send(['PARAGRAPHS', 'sample'])
    if paragraphs is None:
        raise Exception("No paragraphs recognized")
    pos = parser.send(['POS', 'sample'])
    if pos is None:
        raise Exception("No part of speech information retrieved")

    academics = parser.send(['ACADEMICS', 'sample'])
    if academics is None:
        raise Exception("No academic language information retrieved")
    latinates = parser.send(['LATINATES', 'sample'])
    if latinates is None:
        raise Exception("No information on latinate words retrieved")

    frequencies = parser.send(['FREQUENCIES', 'sample'])
    if frequencies is None:
        raise Exception("No frequency information retrieved")

    halrootfreqs = parser.send(['HALROOTFREQS', 'sample'])
    if halrootfreqs is None:
        raise Exception("No root word frequency information retrieved")

    transitionprofile = parser.send(['TRANSITIONPROFILE', 'sample'])
    if transitionprofile is None:
        raise Exception("No transition profile information received")

    quotedtext = parser.send(['QUOTEDTEXT', 'sample'])
    if quotedtext is None:
        raise Exception("No quoted text information received")

    perspectives = parser.send(['PERSPECTIVES', 'sample'])
    if perspectives is None:
        raise Exception("No perspective/viewpoint information received")

    attributions = parser.send(['ATTRIBUTIONS', 'sample'])
    if attributions is None:
        raise Exception("No attribution information received")

    sources = parser.send(['SOURCES', 'sample'])
    if sources is None:
        raise Exception("No source information received")

    citedtext = parser.send(['CITES', 'sample'])
    if citedtext is None:
        raise Exception("No citation information received")

    argwords = parser.send(['ARGUMENTWORDS', 'sample'])
    if argwords is None:
        raise Exception("No argument word information received")

    coresentences = parser.send(['CORESENTENCES',
                                'sample'])
    if coresentences is None:
        raise Exception("No core sentence information received")

    extendedcoresentences = parser.send(['EXTENDEDCORESENTENCES',
                                        'sample'])
    if extendedcoresentences is None:
        raise Exception("No extended core sentence information received")

    content_segments = parser.send(['CONTENTSEGMENTS',
                                   'sample'])
    if content_segments is None:
        raise Exception("No content segment information received")

    promptlanguage = parser.send(['PROMPTLANGUAGE',
                                 'sample'])
    if promptlanguage is None:
        raise Exception("No prompt language information received")

    promptrelated = parser.send(['PROMPTRELATED', 'sample'])
    if promptrelated is None:
        raise Exception("No prompt related cluster word information received")

    print('No paragraphs: ', len(paragraphs))
    print('No sentences: ', len(sentences))
    print('No words: ', len(tokens))
    print('\nNo of transition words:',
          transitionprofile[0])
    print('Types of transitions: ')
    for item in transitionprofile[1]:
        print('\t', item, ': ',
              transitionprofile[1][item])
    print('Specific transitions used:')
    for item in transitionprofile[2]:
        print('\t', item, ': ',
              transitionprofile[2][item])

    laststart = 0
    lastend = 0
    tokensfixed = []
    for item in transitionprofile[3]:
        if item[0] == 'NEWLINE':
            continue
        print(item)
        tokensfixed += tokens[lastend: item[1]]
        tokensfixed += ['<transition type="'
                        + item[4] + '" >']
        tokensfixed += tokens[item[2]: item[3] + 1]
        tokensfixed += ['</transition>']
        laststart = item[2]
        lastend = item[3] + 1
    tokensfixed += tokens[lastend:]
    print(normalize(' '.join(
          tokensfixed)).replace('= "', '="'
                                ).replace('\n',
                                          '<br>\n'))
    acadlist = []
    countacad = 0
    for i, token in enumerate(tokens):
        if academics[i] or latinates[i]:
            countacad += 1
            if token.lower() not in acadlist:
                acadlist += [token.lower()]
    print('\nTotal number of academic and latinate words: ',
          countacad)
    print('\nTotal number of distinct academic and latinate words: ',
          len(acadlist))
    print('\nDistinct academic words used: ',
          ' '.join(sorted(acadlist)), '\n')
    numquoted = 0
    lastquoted = -1
    qs = ''
    qlist = []
    for i, offset in enumerate(quotedtext):
        if quotedtext[i]:
            numquoted += 1
            if i - 1 == lastquoted:
                qs += ' ' + tokens[i]
            elif len(qs) > 0:
                qlist += [qs.strip()]
                qs = ''
            lastquoted = i

    print('\nNumber of quoted words:', numquoted)
    print('Quotes:')
    print(qlist)
    numSources = 0
    for i, token in enumerate(tokens):
        if sources[i]:
            numSources += 1
    print('\nSources mentioned in attributions:',
          numSources)
    for i, token in enumerate(tokens):
        if sources[i]:
            print(token)
    print('\nAttribution, Source:')
    for i, token in enumerate(tokens):
        if attributions[i]:
            print(token, tokens[perspectives[i][0]])

    numcited = 0
    lastcited = -1
    qs = ''
    qlist = []
    for i, offset in enumerate(citedtext):
        if offset:
            if i - 1 == lastcited:
                qs += ' ' + tokens[i]
            lastcited = i
        else:
            if len(qs) > 0:
                qlist += [qs.strip()]
                numcited += 1
            qs = ''
    print('\nNumber of citations:', numcited)
    print('Citations:')
    print(qlist)
    arglist = []
    for item in argwords:
        arglist += [tokens[item]]
    print('Explicit argumentation words:',
          arglist)
    cts = []
    qs = ''
    countValid = 0
    print('Number of sentences in core content:',
          len(coresentences), '\n')
    print('-----Core Content -------------------')
    for sentence in coresentences:
        if len(normalize(' '.join(
               tokens[sentence[0]:sentence[1]]
               )).replace('\n', '')) > 0:
            print(normalize(' '.join(
                  tokens[sentence[0]:sentence[1]]
                  )).replace('\n', ''), '\n')

    print('\n-----Extended Core Content -------------------')
    print('Number of sentences in extended core content:',
          len(extendedcoresentences), '\n')
    for sentence in extendedcoresentences:
        if len(normalize(' '.join(
           tokens[sentence[0]:sentence[1]]
           )).replace('\n', '')) > 0:
            print(normalize(' '.join(
                  tokens[sentence[0]:sentence[1]]
                  )).replace('\n', ''), '\n')

    print('\nNumber of sentences in supporting detail:',
          len(content_segments), '\n')
    print('-----Supporting Details---------------')
    for segment in content_segments:
        if len(normalize(' '.join(
               tokens[segment[0]:segment[1]]
               )).replace('\n', '')) > 0:
            print(normalize(' '.join(
                  tokens[segment[0]:segment[1]]
                  )).replace('\n', ''), '\n')

    print('\nCore topic language:', promptlanguage)
    print('\nCore topic clusters:', promptrelated)
    ok = parser.send(['REMOVE', 'sample'])
