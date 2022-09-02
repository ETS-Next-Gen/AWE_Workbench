#!/usr/bin/env python3
import math
import names
import openpyxl
import pandas as pd
import random
import threading
import os
from awe_workbench.web.websocketClient import websocketClient
from awe_workbench.languagetool.languagetoolClient import languagetoolClient

def set_extensions(empathLexicon):
    """
    Add the metrics we want to capture to the spacy Token and Document objects
    """

    # Document level measure: vector of Empath (like LIWC) content category vectors
    # The 200 off the shelf vectors are pretty random so we probably won't
    # want to call it like this. More likely we'll use Empath to generate new clusters
    # based upon seed words from text samples, such as a source text.
    empathVec = lambda tokens: empathLexicon.analyze(tokens.text, normalize=True)
    Doc.set_extension("empathVector", getter=empathVec, force=True)

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

    ##############################
    # Initialize major variables #
    ##############################

    # define set of samples we can use
    dataset_filebases = [
        'temp',     
        'CBAL_HENRY_OrganicFarming_T2_6_edit',
        'CBAL_HENRY_OrganicFarming_T2_7_edit',
        'FLspMAspBLT_DES30023_020420',
        'FLspMAspBLT_DES30024_020420',
        'FLspMAspBLT_DES30025_020420',
        'HENRY_CBAL BANADs T17_edit',
        'HENRY_CBAL BANADS_T16_edit',
        'HENRY_CBAL_W_CashForGrades_FL11_T1_6_edit',
        'HENRY_CBAL_W_CashforGrades_FL11_T1_7_edit',
        'HENRY_CBAL_W_SocialNet_FL10_T1_6_edit',
        'HENRY_CBAL_W_SocialNet_FL10_T1_7_edit',
        'HENRY_Dolphin_T2_17_edit',
        'LSS_CG30032_020320',
        'RA_IMM30001_120219_nohalfpoint',
        'RAyr1_LH30004_111419',
        'spBLT_OF30020_020320',
        'spBLT_OF30021_020320',
        'banAds_FL10_CBAL_W_BanAds_FL10_T4_1'
]

    # Load a small sample set of documents for testing
    FILEBASE = 'banAds_FL10_CBAL_W_BanAds_FL10_T4_1' #st.selectbox('Choose a dataset',dataset_filebases)

    # Open the source document
    #source = open(os.path.expanduser("~/code/data/datasets/CBAL/{base}.source".format(base=FILEBASE))).read()
    #source = open(os.path.expanduser("~/code/data/datasets/CBAL/{base}.exemplar".format(base=FILEBASE))).read()

    #if st.checkbox("Use source text"):
    #    useSource = True
    #else:
    useSource = False

    # Load the selected data
    o_responses =  [str(a.value) for a in list(openpyxl.load_workbook(os.path.expanduser("~/code/data/datasets/CBAL/{base}.xlsx".format(base=FILEBASE))).active.columns)[1]]

    o_scores =  [str(a.value) for a in list(openpyxl.load_workbook(os.path.expanduser("~/code/data/datasets/CBAL/{base}.xlsx".format(base=FILEBASE))).active.columns)[4]]
    responses = []
    for i in range(len(o_responses)):
        response = o_responses[i]
        score = o_scores[i]
        responses.append([response, score])

    ########################################################
    # Set up the document set to analyse in this round     #
    ########################################################

    # Remove blank responses, and subsample 30 documents
    #docset = list(filter(None, responses))
    docset = random.sample(responses,30)

    ###############################################
    # Set up for demo where we need student names #
    ###############################################

    # Give random student names
    studentsBase = []
    while len(studentsBase)<len(docset):
        name = names.get_first_name()
        if name not in studentsBase:
            studentsBase.append(name)

    # Uncomment to show score data with student name
    #for i in range(len(studentsBase)):
    #    studentsBase[i] = studentsBase[i] #+ '_' + docset[i][1]
           
    # Initialize student and document variables
    if useSource:
        students=['Source Text']
        documents = [source]
    else:
        students=[]
        documents=[]
    
    for name in studentsBase:
        students.append(name)
    for document in docset:
        documents.append(document[0])

    df1 = lt.summarizeMultipleTexts(students, documents)
   
    texts = cs.send(documents)
    for text in texts:
        print(text)
        print('\n--------------\n')

    ok = parser.send(['CLEARPARSED'])
    print('parser cleared',ok)
    for i in range(0, len(texts)):
        # Register the document with Holmes
        print('loading ',students[i])
        ok = parser.send(['PARSEONE', students[i], texts[i]])

    labels = parser.send(['LABELS'])   
    for label in labels:
        tokens = parser.send(['DOCTOKENS', label])
        print(label, tokens)
        heads = parser.send(['DOCHEADS', label])
        print(label, heads)
        deps = parser.send(['DOCDEPENDENCIES', label])
        print(label, deps)
        ents = parser.send(['DOCENTITIES', label])
        print(label, ents)

    for label in labels:
        ok = parser.send(['REMOVE',label])
        print('removed label', label, ok)
        tokens = parser.send(['DOCTOKENS', label])
        print(label, tokens)

    for label in labels:
        ok = parser.send(['PARSESET',[labels,texts]])

    for label in labels:
        tokens = parser.send(['DOCTOKENS', label])
        print(label, tokens)
        heads = parser.send(['DOCHEADS', label])
        print(label, heads)
        deps = parser.send(['DOCDEPENDENCIES', label])
        print(label, deps)
        ents = parser.send(['DOCENTITIES', label])
        print(label, ents)
        serialized = parser.sendraw(['SERIALIZED', label])
        print(label, serialized)

    for label in labels:
        ok = parser.send(['REMOVE',label])
        print('removed label', label, ok)
        tokens = parser.send(['DOCTOKENS', label])
        print(label, tokens)

    for i in range(0, len(texts)):
        # Register the document with Holmes
        print('loading ',students[i])
        ok = parser.send(['PARSEONE', students[i], texts[i]])

    ok = parser.send(['PARSEONE', 'test', 'A dog barked at a cat'])
    print('test',ok)

    parser.send(['NEWSEARCHPHRASE','dogs bark', 'db'])

    matches = parser.send(['MATCH_DOCUMENTS'])
    for match in matches:
        print('matches', match)

    matches = parser.send(['TOPIC_MATCHES','The U.S. government should ban ads aimed at children under 12.'])
    for match in matches:
        print('topic matches', match)

    for label in labels:
        lemmas = parser.send(['LEMMAS',label])
        print('lemmas', label, lemmas)

    for label in labels:
        wordtypes = parser.send(['WORDTYPES',label])
        print('word types', label, wordtypes)

    for label in labels:
        roots = parser.send(['ROOTS',label])
        print('roots', label, roots)

    for label in labels:
        syls = parser.send(['SYLLABLES', label])
        print('syllables', label, syls)

    for label in labels:
        wlens = parser.send(['WORDLENGTH', label])
        print('WORDLENGTH', label, wlens)

    for label in labels:
        lats = parser.send(['LATINATES', label])
        print('latinates', label, lats)

    for label in labels:
        lats = parser.send(['ACADEMICS', label])
        print('academics', label, lats)

    for label in labels:
        fms = parser.send(['FAMILYSIZES', label])
        print('word family sizes', label, fms)

    for label in labels:
        fms = parser.send(['SENSENUMS', label])
        print('numbers of senses by word', label, fms)

    for label in labels:
        lfms = parser.send(['LOGSENSENUMS', label])
        print('log numbers of senses by word', label, lfms)

    for label in labels:
        mlx = parser.send(['MORPHOLEX', label])
        print('numbers of morphemes by word', label, mlx)

    for label in labels:
        mms = parser.send(['MORPHNUMS', label])
        print('numbers of morphemes by word', label, mms)

    for label in labels:
        hrf = parser.send(['HALROOTFREQS', label])
        print('morpholex root frequencies (from HAL corpus) by word', label, hrf)

    for label in labels:
        rfsz = parser.send(['ROOTFAMSIZES', label])
        print('morpholex family size of first root', label, rfsz)

    for label in labels:
        rpfmfs = parser.send(['ROOTPFMFS', label])
        print('percentage of family more frequent by word', label, rpfmfs)

    for label in labels:
        mms = parser.send(['TOKFREQS', label])
        print('token frequencies', label, mms)

    for label in labels:
        mms = parser.send(['LEMMAFREQS', label])
        print('lemma frequencies', label, mms)

    for label in labels:
        mms = parser.send(['ROOTFREQS', label])
        print('root frequencies', label, mms)

    for label in labels:
        mms = parser.send(['MAXFREQS', label])
        print('max frequencies across word, token, root', label, mms)

    for label in labels:
        mms = parser.send(['CONCRETES', label])
        print('token concreteness estimates', label, mms)

    for label in labels:
        mms = parser.send(['ANIMATES', label])
        print('token animate status', label, mms)

    for label in labels:
        mms = parser.send(['ABSTRACTTRAITS', label])
        print('token abstract trait status', label, mms)

    for label in labels:
        mms = parser.send(['DEICTICS', label])
        print('token deictic status', label, mms)

    for label in labels:
        mms = parser.send(['PARAGRAPHS', label])
        print('paragraph boundary locations', label, mms)

    for label in labels:
        mms = parser.send(['PARAGRAPHLENS', label])
        print('paragraph lengths', label, mms)

    for label in labels:
        mms = parser.send(['TRANSITIONPROFILE', label])
        print('transition frequency', label, mms[0])
        for item in mms[1]:
            print('transition category frequencies', item, mms[1][item])
        for item in mms[2]:
            print('transition word frequencies', item, mms[2][item])
        print('details on transitions', mms[3])

    for label in labels:
        mms = parser.send(['TRANSITIONDISTANCES', label])
        print('transition distances', label, mms)

    for label in labels:
        mms = parser.send(['SENTENCECOHESIONS', label])
        print('sentence cohesion', label, mms)

    for label in labels:
        mms = parser.send(['SLIDERCOHESIONS', label])
        print('coref chains', label, mms)

    for label in labels:
        mms = parser.send(['RHEMEDEPTHS', label])
        print('rheme depths', label, mms)

    for label in labels:
        mms = parser.send(['THEMEDEPTHS', label])
        print('theme depths', label, mms)

    for label in labels:
        mms = parser.send(['WEIGHTEDDEPTHS', label])
        print('weighted depths', label, mms)

    for label in labels:
        mms = parser.send(['WEIGHTEDBREADTHS', label])
        print('weighted breadths', label, mms)

    for label in labels:
        mms = parser.send(['SYNTACTICPROFILE', label])
        print('syntactic profile', label)
        for item in mms:
            print(item, mms[item])

    for label in labels:
        mms = parser.send(['NORMEDSYNTACTICPROFILE', label])
        print('normed syntactic profile', label)
        for item in mms:
            print(item, mms[item])

    for label in labels:
        mms = parser.send(['DIRECTSPEECHSPANS', label])
        print('Direct speech spans', label)
        print(mms)

    for label in labels:
        mms = parser.send(['INTERACTIVELANGUAGE', label])
        print('Interactive language', label)
        print(mms)

    for label in labels:
        mms = parser.send(['ARGUMENTLANGUAGE', label])
        print('Explicit argument language', label)
        print(mms)

    for label in labels:
        mms = parser.send(['SUBJECTIVITYRATINGS', label])
        print('TextBlob subjectivity ratings', label)
        print(mms)

    for label in labels:
        mms = parser.send(['POLARITYRATINGS', label])
        print('TextBlob polarity ratings', label)
        print(mms)

    for label in labels:
        mms = parser.send(['ASSESSMENTS', label])
        print('SpacyTextBlob stance markers', label)
        for item in mms:
            print(item)

    for label in labels:
        mms = parser.send(['SENTIMENTRATINGS', label])
        print('SentiWord sentiment polarity ratings', label)
        print(mms)

    for label in labels:
        mms = parser.send(['PERSPECTIVESPANS', label])
        print('Perspective spans', label)
        for key in mms:
            if key=='explicit_3':
                dictPer = mms[key]
                for thirdp in dictPer:
                    print(thirdp, dictPer[thirdp])
            else:
                print(key,mms[key])
                
    for label in labels:
        mms = parser.send(['STANCEMARKERS', label])
        print('Stance markers by perspective span', label)
        for key in mms:
            if key=='explicit_3':
                dictPer = mms[key]
                for thirdp in dictPer:
                    print(thirdp, dictPer[thirdp])
            else:
                print(key,mms[key])

    for label in labels:
        mms = parser.send(['EMOTIONALSTATES', label])
        print('Emotional state predicates by perspective span', label)
        for key in mms:
            if key=='explicit_3':
                dictPer = mms[key]
                for thirdp in dictPer:
                    print(thirdp, dictPer[thirdp])
            else:
                print(key,mms[key])

    for label in labels:
        mms = parser.send(['CHARACTERTRAITS', label])
        print('Character trait predicates by perspective span', label)
        for key in mms:
            if key=='explicit_3':
                dictPer = mms[key]
                for thirdp in dictPer:
                    print(thirdp, dictPer[thirdp])
            else:
                print(key,mms[key])

    for label in labels:
        mms = parser.send(['PROPOSITIONALATTITUDES', label])
        print('Propositional attitudes by perspective span', label)
        for key in mms:
            if key=='explicit_3':
                dictPer = mms[key]
                for thirdp in dictPer:
                    print(thirdp, dictPer[thirdp])
            else:
                print(key,mms[key])

    for label in labels:
        mms = parser.send(['GOVERNINGSUBJECTS', label])
        print('governing subjects for each token', label, mms)

    for label in labels:
        mms = parser.send(['DEVWORDS', label])
        print('content words not in the 4 largest/most import word clusters found in the document', label, mms)

    for label in labels:
        mms = parser.send(['CLUSTERINFO', label])
        print('cluster information for each doc', label, mms)

    featnames = ['ID']+ parser.send(['DOCSUMMARYLABELS'])
    data = []
    for i in range(0, len(texts)):
        label = students[i]
        values = [label]
        newvals = parser.send(['DOCSUMMARYFEATS', label])
        if newvals is not None:
            data.append(values+newvals)
    print(featnames)
    print('data',data)
                    
    df2 = pd.DataFrame(data,columns=featnames)
    df = pd.merge(df1, df2, on="ID")
    print(df.head)
    df.to_csv("output.csv")

    for label in labels:
        pts = parser.send(['PASTTENSESCOPE', label])
        print('list of flags for whether tokens are in past tense clauses', label, pts)

#    for label in labels:
#        tokvecs = parser.send(['TOKVECS',label])
#        print('token vectors', label, tokvecs)
