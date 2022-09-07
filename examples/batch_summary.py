#!/usr/bin/env python3
import csv
import os
import math
import names
import openpyxl
import pandas as pd
import random
import threading
from awe_workbench.web.websocketClient import websocketClient
from awe_languagetool.languagetoolClient import languagetoolClient

batch_size = 1

def initialize():
    """
    Initialize our CorpusSpellcheck and parser objects (for spell-
    correction and parsing with spacy + coreferee and other extensions
    using a modified version of the holmes extractor library. While
    doing so, we initialize a series of lexical databases that support
    some of the metrics we want to capture.
    
    This script assumes that we have already run these two commands
    in another window:
        python -m awe_workbench.web.startServers
        python -m awe_components.wordprobs.wordseqProbabilityServer

    """
    # Initialize the spellchecker
    cs = websocketClient()
    lt = languagetoolClient()

    # Initialize the parser
    parser = websocketClient()
    parser.set_uri("ws://localhost:8766")

    # return spellchecker and parser objects
    return cs, parser, lt

if __name__ == '__main__':

    cs, parser, lt = initialize()
    ids = ['GRE2','GRE3','GRE4','GRE5','GRE6']
    docs = ['essays/gre2.txt','essays/gre3.txt','essays/gre4.txt','essays/gre5.txt','essays/gre6.txt']
    data = []
    syntactic_data = []
    doc_contents = []
    for i, fname in enumerate(docs):
        with open(fname) as f:
            contents = f.read()
            doc_contents.append(contents)

    print('Running LanguageTool')
    df1 = lt.summarizeMultipleTexts(ids, doc_contents)
    texts = None
    print('Running spellcorrect')
    texts = cs.send(doc_contents)

    if texts is None:
        print('error')
    else:
        print('Running parser')
        # Note that this way of sending the essays to the parser
        # leaves all of the parsed essays sitting in memory
        # on the server -- great if you plan to query them again,
        # not so great for a single run if the number of texts
        # is large. For a more efficient run, loop through and
        # send the texts one by one using PARSEONE. Then merge
        # the fows of data in the script.
        ok = parser.send(['PARSESET',[ids, texts]])

    featnames = ['ID'] + parser.send(['DOCSUMMARYLABELS'])

    for i in range(0, len(texts)):
        newvals = parser.send(['DOCSUMMARYFEATS', ids[i]])
        label = ids[i]
        values = [label]
        if newvals is not None:
            data.append(values+newvals)
        dfFinal = None
        profile = parser.send(['NORMEDSYNTACTICPROFILE', label])
        profile['ID'] = label
        if profile is not None:
            syntactic_data.append(profile)

    df1 = pd.DataFrame(data,columns=featnames)
    df1.set_index('ID', inplace=True)
    syntactic_profile = pd.DataFrame.from_records(syntactic_data)
    syntactic_profile = syntactic_profile.fillna(0)
    syntactic_profile.set_index('ID', inplace=True)
    dfFinal = pd.merge(df1,syntactic_profile, on='ID')

    dfFinal.to_csv("output.csv")

