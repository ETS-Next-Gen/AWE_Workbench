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
from awe_workbench.languagetool.languagetoolClient import languagetoolClient

batch_size = 1

def initialize():
    """
    Initialize our CorpusSpellcheck and parser objects (for spell-
    correction and parsing with spacy + coreferee and other extensions
    using a modified version of the holmes extractor library. While
    doing so, we initialize a series of lexical databases that support
    some of the metrics we want to capture.
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

    ids = []
    docs = []
    fileheaders = ['ID','case', 'model_id', 'model_group', 'prompt_specific', 'appointment_id', 'prompt_id', 'program', 'test_data', 'gd1','gd2','gd3']
    filedata = []
    with open(os.path.expanduser('~/code/data/sample_essays.csv'), 'r', newline='', encoding='utf-8', errors='ignore') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            fileinfo = []
            ID = row['essay_id']
            fileinfo.append(ID)
            text = row['essay_text']
            case = row['case']
            fileinfo.append(case)
            model_id = row['model_id']
            fileinfo.append(model_id)
            model_group = row['model_group']
            fileinfo.append(model_group)
            prompt_specific = row['prompt_specific']
            fileinfo.append(prompt_specific)
            appointment_id = row['appointment_id']
            fileinfo.append(appointment_id)
            prompt_id = row['prompt_id']
            fileinfo.append(prompt_id)
            program = row['program']
            fileinfo.append(program)
            test_date = row['test_date']
            fileinfo.append(test_date)
            gd1 = row['gd1']
            fileinfo.append(gd1)
            gd2 = row['gd2']
            fileinfo.append(gd2)
            gd3 = row['gd3']
            fileinfo.append(gd3)

            ids.append(ID)
            docs.append(text)
            filedata.append(fileinfo)

    df0 = pd.DataFrame(filedata,columns=fileheaders)
   
    head = docs[0:batch_size]
    tail = docs[batch_size:]
    
    headIds = ids[0:batch_size]
    tailIds = ids[batch_size:]
    texts = []
    syntactic_data = []
    dfFinal = None
    while len(head)>0:

        df1 = lt.summarizeMultipleTexts(headIds, head)
        texts = None
        texts = cs.send(head)
    
        if texts is None:
            print('error')
        else:
            for text in texts:
                print('len',len(text))
        print('parsing')
        ok = parser.send(['PARSESET',[headIds,texts]])


        featnames = ['ID']+ parser.send(['DOCSUMMARYLABELS'])
        data = []
        for i in range(0, len(texts)):
            label = headIds[i]
            values = [label]
            print('parsing', label, i)
            newvals = parser.send(['DOCSUMMARYFEATS', label])
            if newvals is not None:
                data.append(values+newvals)

            profile = parser.send(['NORMEDSYNTACTICPROFILE', label])
            profile['ID'] = label
            syntactic_data.append(profile)
        df2 = pd.DataFrame(data,columns=featnames)
        df3 = pd.merge(df0, df1, on="ID")
        df4 = pd.merge(df3, df2)
        if dfFinal is None:
            dfFinal = df4
        else:
            dfFinal = pd.concat([dfFinal,df4],axis=0, ignore_index=True)

        print(len(dfFinal))
        
        for i in range(0,len(texts)):
            label = headIds[i]
            print('removing', label)
            ok = parser.send(['REMOVE', label])

        head = tail[0:batch_size]
        tail = tail[batch_size:]
        headIds = tailIds[0:batch_size]
        tailIds = tailIds[batch_size:]

    syntactic_profile = pd.DataFrame.from_records(syntactic_data)
    syntactic_profile = syntactic_profile.fillna(0)
    syntactic_profile.set_index('ID', inplace=True)
    dfFinal.set_index('ID', inplace=True)
    
    dfFinal = pd.merge(dfFinal,syntactic_profile, on='ID')
            
    dfFinal.to_csv("output.csv")

