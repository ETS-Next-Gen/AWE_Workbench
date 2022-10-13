#!/usr/bin/env python3.10
# Copyright 2022, Educational Testing Service

import streamlit as st
import re
import asyncio
import html
import os
import json
import pandas as pd

from annotated_text import annotated_text
from awe_workbench.web.websocketClient import websocketClient
from awe_languagetool.languagetoolClient import languagetoolClient

# Define clients to access AWE Workbench servers
def initialize():
    """
    Initialize our CorpusSpellcheck and parser objects (for spell-
    correction and parsing with spacy + coreferee and other extensions
    using a modified version of the holmes extractor library. While
    doing so, we initialize a walkedseries of lexical databases that support
    some of the metrics we want to capture.
    """

    # Initialize the parser
    parser = websocketClient()
    parser.set_uri("ws://localhost:8766")

    lt = languagetoolClient()

    # return spellchecker and parser objects
    return parser, lt

def proofread(lt, document_text):
    '''
        Grab the LanguageTool feedback for a single document
    '''
    record = {}
    result = lt.processText(record, document_text)
    if result is None:
        raise Exception("No correction information received")
    return result

def summarize_proofreading(proof_results):
    '''
        Summarize LanguageTool results across a set of 
        documents using the data_dict format we use for
        indicators
    '''
    all_categories = []
    data_dict = {}

    # Go through the proof results and
    # put them in our standard indicator format
    for doc_id in proof_results:
        if doc_id not in data_dict.keys():
            data_dict[doc_id] = {}
        
        for result in proof_results[doc_id]:
        
            # Populate the info field with relevant
            # results for each indicator
            indicator = result['label'].title()
            if indicator not in all_categories:
                all_categories.append(indicator)
            if indicator not in data_dict[doc_id]:
                data_dict[doc_id][indicator] = {}
            if 'info' not in data_dict[doc_id][indicator]:
                data_dict[doc_id][indicator]['info'] = []
            data_dict[doc_id][indicator]['info'].append(result)

            # Populate the info field with relevant
            # results for each subindicator (category +
            # detail)
            subindicator = \
                result['label'].title() \
                    + '/' + result['detail'].title()
            if subindicator not in all_categories:
                all_categories.append(subindicator)
            if subindicator not in data_dict[doc_id]:
                data_dict[doc_id][subindicator] = {}
            if 'info' not in data_dict[doc_id][subindicator]:
                data_dict[doc_id][subindicator]['info'] = []
            data_dict[doc_id][subindicator]['info'].append(result)
            
        # Add the type, summary, and text fields
        for indicator in data_dict[doc_id]:
            # define the summary as being proofreading result
            # not parsing result
            data_dict[doc_id][indicator]['type'] = 'proofreading'
            
            # count of errors is length of the info field list
            data_dict[doc_id][indicator]['summary'] = \
                len(data_dict[doc_id][indicator]['info'])
                
            # use offset and length to get the text of the
            # error then grab context field to show where
            # the error is
            data_dict[doc_id][indicator]['text'] = \
                  ', '.join([dlookup[doc_id][proof['offset']:\
                             proof['offset']+proof['length']] \
                             + ' in "' \
                             + proof['context']['text'] \
                             + '"' \
                             for proof \
                             in data_dict[doc_id][indicator]['info']])        

        # Create blank records if an indicator isn't represented
        # in the proofing data
        for indicator in all_categories:
            if indicator not in data_dict[doc_id]:
                data_dict[doc_id][indicator] = {}
                data_dict[doc_id][indicator]['type'] = 'proofreading'
                data_dict[doc_id][indicator]['summary'] = 0
                data_dict[doc_id][indicator]['text'] = ''
                data_dict[doc_id][indicator]['info'] = []
    return data_dict

# Json record of indicators we will retrieve and summarize info for
indicators = [
    [{'name': 'Number of syllables',
      'type': 'parser',
      'summary':
        {"name": "nSyll",
         "infoType": "Token",
         "filters": [("is_alpha",[True])],
         "summaryInfo": "mean"
         },
     'text':
        {"name": "nSyll",
         "infoType": "Token",
         "summaryInfo": "uniq",
         "filters": [(">",[3]),("is_alpha",[True])],
         "transformations": ["lemma"]
        },
     'info':
        {"name": "nSyll",
         "infoType": "Token"
        }
    }],
    [{'name': 'Word Frequency',
      'type': 'parser',
      'summary':
        {"name": "max_freq",
         "infoType": "Token",
         "summaryInfo": "mean",
         "filters": [("is_alpha",[True])],
         "transformations": ["neg"]
        },
     'text':
        {"name": "max_freq",
         "infoType": "Token",
         "summaryInfo": "uniq",
         "filters": [("<",[4]),("is_alpha",[True])],
         "transformations": ["lemma"]
        },
     'info':
        {"name": "max_freq",
         "infoType": "Token"
        }
     }
    ],
    [{'name': 'Academic Words',
      'type': 'parser',
      'summary':
        {"name": "is_academic",
         "infoType": "Token",
         "summaryInfo": "percent",
         "filters": [("is_alpha",[True])]
        },
     'text':
        {"name": "is_academic",
         "infoType": "Token",
         "summaryInfo": "uniq",
         "filters": [("is_academic",[True]),("is_alpha",[True])],
         "transformations": ["lemma"]
        },
     'info':
        {"name": "is_academic",
         "infoType": "Token"
        }
     }
    ],
    [{'name': 'Latinate words',
      'type': 'parser',
      'summary':
        {"name": "is_latinate",
         "infoType": "Token",
         "summaryInfo": "percent",
         "filters": [("is_alpha",[True])]
        },
     'text':
        {"name": "is_latinate",
         "infoType": "Token",
         "summaryInfo": "uniq",
         "filters": [("is_latinate",[True]),("is_alpha",[True])],
         "transformations": ["lemma"]
        },
     'info':
        {"name": "is_latinate",
         "infoType": "Token"
         }
     }
    ],
    [{'name': 'Informal language',
      'type': 'parser',
      'summary':
        {"name": "vwp_interactive",
         "infoType": "Token",
         "summaryInfo": "percent",
         "filters": [("is_alpha",[True])]
        },
     'text':
        {"name": "vwp_interactive",
         "infoType": "Token",
         "summaryInfo": "uniq",
         "filters": [("vwp_interactive",[True]),("is_alpha",[True])],
         "transformations": ["lemma"]
        },
     'info':
        {"name": "vwp_interactive",
         "infoType": "Token"
        }
     }
    ],
    [{'name': 'Sentence Types', 
      'type': 'parser',
      'summary':
        {"name": "sentence_types",
         "infoType": "Doc",
         "summaryInfo": "total"
        },
     'text':
        {"name": "sentence_types",
         "infoType": "Doc",
         "summaryInfo": "counts"         
        },
     'info':
        {"name": "sentence_types",
         "infoType": "Doc"
        }
     }
    ],
    [{'name': 'Transitions', 
      'type': 'parser',
      'summary':
        {"name": "transitions",
         "infoType": "Doc",
         "summaryInfo": "total"
        },
     'text':
        {"name": "transitions",
         "infoType": "Doc",
         "summaryInfo": "uniq",
         "filters": [],
         "transformations": ["lower"]
        },
     'info':
        {"name": "transitions",
         "infoType": "Doc"
        }
     }
    ]
]

def parse_and_summarize(document_labels,
                        indicators,
                        data_dict):
    '''
        Function takes a set of document ids and indicators,
        parses them, and summarizes them into the data_dict
        format we use for indicators
    '''
    # Grab indicator info for each document
    for doc_id in document_labels:
        for entry in indicators:
            for subentry in entry:
                if subentry['type'] == 'parser':

                   indicator = subentry['name']
                    
                   # Construct a blank indicator data record
                   outinfo = {}
                   outinfo['name'] = indicator
                   outinfo['summary'] = None
                   outinfo['text'] = None
                   outinfo['info'] = None
                                 
                   for indicatorMode in subentry:
                       # For each entry in the indicator list,
                       # construct an appropriate query to send
                       # to the server
                       indicatorInfo = subentry[indicatorMode]
                       
                       # Seven parameter format
                       # Includes doc_id, the indicator
                       # name, infoType (list of token
                       # records [Token] or span records [Doc])
                       # plus specification of type of
                       # summarization to perform (if any),
                       # filters to filter records out with,
                       # and transformations to change what
                       # is summarized in the 'value' field
                       # of the record set returned by the
                       # AWE_Info function.
                       if 'summaryInfo' in indicatorInfo \
                          and 'filters' in indicatorInfo \
                          and 'transformations' in indicatorInfo:
                           value = parser.send(['AWE_INFO',
                               doc_id, indicatorInfo['name'],
                               indicatorInfo['infoType'],
                               indicatorInfo['summaryInfo'],
                               json.dumps(indicatorInfo[
                                   'filters']),
                               json.dumps(
                                   indicatorInfo[
                                       'transformations'])])

                       # five parameter format
                       elif 'summaryInfo' in indicatorInfo \
                          and 'filters' in indicatorInfo:
                           value = parser.send(['AWE_INFO',
                               doc_id, indicatorInfo['name'],
                               indicatorInfo['infoType'],
                               indicatorInfo['summaryInfo'],
                               json.dumps(
                                   indicatorInfo['filters'])])

                       # four parameter format
                       elif 'summaryInfo' in indicatorInfo:
                           value = parser.send(['AWE_INFO',
                               doc_id, indicatorInfo['name'],
                               indicatorInfo['infoType'],
                               indicatorInfo['summaryInfo']])

                       # three parameter format
                       elif 'infoType' in indicatorInfo:
                           value = parser.send(['AWE_INFO',
                               doc_id, indicatorInfo['name'],
                               indicatorInfo['infoType']])
 
                       # Construct and format the output data
                       # for the text field
                       if indicatorMode == 'text':
                           if 'summaryInfo' in indicatorInfo:
                               if indicatorInfo['summaryInfo'] == 'counts':
                                   for key in value.keys():
                                       outinfo['text'] = str(value)
                               else:
                                   outinfo['text'] = \
                                       ', '.join(sorted(value))
                           else:
                               outinfo['text'] = \
                                   ', '.join(sorted(value))

                       # Construct and format the output data for
                       # the summary field
                       elif 'summaryInfo' in indicatorInfo:
                           outinfo['summary'] = value

                       # Set the output data for the info field
                       elif 'infoType' in indicatorInfo:
                           outinfo['info'] = value

                   # Associate the formatted data with the 
                   # specified doc_id and indicator
                   if doc_id not in data_dict:
                       data_dict[doc_id] = {}
                   data_dict[doc_id][indicator] = outinfo
    return data_dict

if __name__ == '__main__':

    # specify where to get the files we want to load
    examplepath = os.path.dirname(__file__)
    locs = []
    for i in range(1, 26):
        tname = 'essays/censorship' + str(i) + '.txt'
        locs.append(os.path.join(examplepath, tname))

    documents = []
    for i, fname in enumerate(locs):
        with open(fname) as f:
            contents = f.read()
            documents.append(contents)

    # Set up document labels
    document_labels = []
    dlookup = {}
    for i in range(1, 26):
        label = 'Censorship_Essay ' + str(i)
        document_labels.append(label)
        dlookup[label] = documents[i-1]

    # Open clients to communicate with the servers
    parser, lt = initialize()
    spellcorrect = websocketClient()

    # Run proofreading and summarize the results
    proof_results = {}
    for i, label in enumerate(document_labels):
        detailcounts = proofread(lt, dlookup[label])
        proof_results[label] = detailcounts
    data_dict = summarize_proofreading(proof_results)

    # Run spell correction
    for i, dl in enumerate(document_labels):
        [text] = spellcorrect.send([dlookup[dl]])
        ok = parser.send(['PARSEONE', dl, text])

    # Parse documents and summarize indicators
    data_dict = parse_and_summarize(document_labels,
                                    indicators,
                                    data_dict)

    # Display all fields but info to show we did the work
    # (the info field has a lot of fields in it -- including
    # offset and length, for use in highlighting, and
    # tokenIdx (for Token records) or startToken and endToken
    # [for Doc records] to indicate the spacy tokens
    # that a parser indicator is associated with)
    for idx in data_dict:
        for item in data_dict[idx]:
            for i, block in enumerate(data_dict[idx][item]):
                if block == 'text':
                    print(idx, item, block, 
                        json.dumps(
                            data_dict[idx][item][block]))
                elif block != 'info' \
                   and data_dict[idx][item]['summary'] != 0:
                    print(idx, item, block,
                       data_dict[idx][item][block])
