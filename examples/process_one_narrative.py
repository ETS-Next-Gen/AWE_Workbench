#!/usr/bin/env python3.10
# Copyright 2022, Educational Testing Service

import argparse
import csv
import json
import math
import operator
import os
import random
import re
import sys
import threading

import names
import openpyxl
import pandas as pd
from awe_workbench.web.websocketClient import websocketClient
from awe_languagetool.languagetoolClient import languagetoolClient
import nltk
from nltk.corpus import stopwords

from example_lib import initialize, normalize, extract_features, \
    render_corrections, render_text, dt, h1, h2, hr, \
    render_summary_statistics, index_to_words, render_index_list, \
    render_histogram_from_dictionary, render_transitions

nltk.download('stopwords')

stopWords = set(stopwords.words('english'))

batch_size = 1

parser = argparse.ArgumentParser(description="Analyze a student text file")
parser.add_argument(
    '--filename',
    default="essays/leprechaun.txt",
    help='Which file to parse'
)
parser.add_argument(
    '--json',
    help="Output JSON feature dump to a file"
)

features_available = [
    "corrections",
    "transitions",
    "summary_stats"
]
parser.add_argument(
    '--features',
    help="Comma-seperated list of which features to print",
    default=",".join(features_available)
)

if __name__ == '__main__':
    args = parser.parse_args()
    text = open(args.filename).read()
    features = args.features.split(",")
    for feature in features:
        if feature not in features_available:
            print("Invalid feature: ", feature)
            print("Available: ", ",".join(features_available))

    spellchecker, parser, languagetool = initialize()
    record = {}

    # This will give a list of grammar and style errors.
    result = languagetool.processText(record, text)
    if "corrections" in features:
        render_corrections(text, result)

    [corrected] = spellchecker.send([text])
    # render_text(corrected, "Spell corrected")

    label = 'sample'
    features = extract_features(parser, corrected, label)

    if "summary_stats" in features:
        render_summary_statistics(features)
    hr()
    render_transitions(features)
    hr()
    acadlist = []
    countacad = 0
    for i, token in enumerate(features['doctokens']):
        if features['academics'][i] or features['latinates'][i]:
            countacad += 1
            if token.lower() not in acadlist:
                acadlist += [token.lower()]
    dt('Total number of academic and latinate words', countacad)
    dt('Total number of distinct academic and latinate words', len(acadlist))
    dt('Distinct academic words used', ' '.join(sorted(acadlist)))
    hr()
    numquoted = 0
    lastquoted = -1
    qs = ''
    qlist = []
    for i, offset in enumerate(features['quotedtext']):
        if features['quotedtext'][i]:
            numquoted += 1
            if i - 1 == lastquoted:
                qs += ' ' + features['doctokens'][i]
            elif len(qs) > 0:
                qlist += [qs.strip()]
                qs = ''
            lastquoted = i

    print('\nNumber of quoted words:', numquoted)
    print('Quotes:')
    hr()
    print(qlist)

    print('\nSources mentioned in attributions:', len(features['sources']))
    print(
        'Note: not all dialogue shows here, only third person, since'
        ' attributions in an argument are always third person. The'
        ' direct speech function handles true dialogue.'
    )
    hr()
    print("Sources:",
          index_to_words(features['doctokens'],
                         features['sources']))
    render_index_list(features, 'attributions')
    render_index_list(features, 'argumentwords')

    cts = []
    qs = ''
    countValid = 0
    hr()
    print('Number of sentences in core content:',
          len(features['coresentences']), '\n')
    h1('Core Content')
    for sentence in features['coresentences']:
        if len(normalize(' '.join(
               features['doctokens'][sentence[0]:sentence[1]]
               )).replace('\n', '')) > 0:
            print(normalize(' '.join(
                  features['doctokens'][sentence[0]:sentence[1]]
                  )).replace('\n', ''))

    print('Narratives don\'t have the patterns of repeated \
          words that gives us the core context/elaboration \
          distinction in an argument essay. So we don\'t see \
          much here or in the extended core context category.')

    h1('Extended Core Content')
    print('Number of sentences in extended core content:',
          len(features['extendedcoresentences']), '\n')
    for sentence in features['extendedcoresentences']:
        if len(normalize(' '.join(
               features['doctokens'][sentence[0]:sentence[1]]
               )).replace('\n', '')) > 0:
            print(normalize(' '.join(
                  features['doctokens'][sentence[0]:sentence[1]]
                  )).replace('\n', ''))

    print('\nNumber of sentences in supporting detail:',
          len(features['contentsegments']), '\n')
    h1('Supporting Details')
    for segment in features['contentsegments']:
        if len(normalize(' '.join(
               features['doctokens'][segment[0]:segment[1]])
               ).replace('\n', '')) > 0:
            print(normalize(' '.join(
                  features['doctokens'][segment[0]:segment[1]]
                  )).replace('\n', ''))
    hr()

    print('\nCore topic language:', features['promptlanguage'])
    print('Notice that what shows up as core vocabulary are fiction \
          verbs like walk, look, happen. This feature also is really \
          appropriate more for argument essays than narratives')
    print('\nCore topic clusters:', features['promptrelated'])
    h1("Dialogue")

    for (speakers, addressees, locs) in features['directspeechspans']:
        spk = []
        for item in speakers:
            spk.append(features['doctokens'][item])
        print('\n\nSpeaker(s):', spk)
        adr = []
        for item in addressees:
            adr.append(features['doctokens'][item])
        print('Addressee(s):', adr)
        txt = []
        for item in locs:
            txt.append(normalize(' '.join(
                       features['doctokens'][item[0]:item[1]])))
        print('Content:', txt)

    render_index_list(features, 'emotionwords')
    render_index_list(features, 'characterwords')

    h1("Social Awareness")
    print('Sentences indicating social awareness \
          (theory of mind) are important indicators \
          of sophistication in narrative.\n')
    for item in features['social_awareness']:
        print(normalize(' '.join(
              features['doctokens'][
                       item[0]:item[1]])).replace('\n',
                                                  '').strip())

    h1("Concrete Details")

    h1("Locations")
    last_i = -1
    locations = []
    txt = []
    last_i = -1
    for i, valid in enumerate(features['locations']):
        if valid:
            if i-last_i == 1:
                txt.append(features['doctokens'][i])
            else:
                txt = [features['doctokens'][i]]
        else:
            if len(txt) > 0:
                locations.append(normalize(' '.join(txt)).strip())
            txt = []
        last_i = i
    for location in locations:
        print(location)

    h1("Present Tense Comments")
    loc = 0
    present_segments = []
    temp = []
    for change in features['tensechanges']:
        present = False
        newloc = change['loc']
        if not change['past']:
            if not present:
                newloc = change['loc']
                present = True
                loc = newloc
            else:
                newloc = change['loc']
                if present:
                    temp += features['doctokens'][loc:newloc]
                present = True
                loc = newloc
        else:
            newloc = change['loc']
            temp += features['doctokens'][loc:newloc]
            if present:
                temp.append(features['doctokens'][newloc])
            if not features['quotedtext'][loc+1] and len(temp) > 1:
                present_segments.append(normalize(
                                        ' '.join(temp)
                                        ).strip().replace('\n', ''))
            temp = []
            present = False
            loc = newloc+1
    temp += features['doctokens'][loc:len(features['doctokens'])-1]
    if not features['quotedtext'][loc-1] and len(temp) > 1:
        present_segments.append(normalize(
                                ' '.join(temp)
                                ).strip().replace('\n', ''))

    for segment in present_segments:
        print(segment)

    [characters, otherRefs] = features['nominalreferences']
    h1("Characters Mentioned")

    sorted_chars = dict(
        sorted(characters.items(), key=operator.itemgetter(1), reverse=True)
    )
    for character in sorted_chars:
        print(character, len(characters[character]))

    if args.json is not None:
        json_dump = json.dumps(features, indent=3)
        if args.json == "-":
            print(json_dump)
        elif not args.json.endswith(".json"):
            print("JSON dump should end with .json")
            sys.exit(-1)
        elif os.path.exists(args.json):
            print("JSON file already exists. I'm not overwriting.")
            sys.exit(-1)
        else:
            with open(args.json, "w") as fp:
                fp.write(json_dump)

    # TODO: Add back citations.
    #
    # We don't have any in our test case, so we omit for now.

    # numcited = 0
    # lastcited = -1
    # qs = ''
    # qlist = []
    # for i, offset in enumerate(features['cites']):
    #      if offset:
    #           if i-1==lastcited:
    #               qs += ' ' + features['doctokens'][i]
    #           lastcited = i
    #      else:
    #           if len(qs)>0:
    #               qlist += [qs.strip()]
    #               numcited +=1
    #           qs = ''

    # print('\nNumber of citations:',numcited)
    # print('Citations:')
    # print(qlist)
