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


def flattenViewpointList(vlist, tokens):
    outlist = []
    for key in vlist:
        if key == 'explicit_1' \
           or key == 'explicit_2':
            for item in vlist[key]:
                outlist.append(item)
        else:
            for subkey in vlist[key]:
                for item in vlist[key][subkey]:
                    outlist.append(item)
    flagged = []
    for i, token in enumerate(tokens):
        if i in outlist:
            flagged.append(True)
        else:
            flagged.append(False)
    return flagged


def fixMessage(message):
    message = message.replace('’', '&rsquo;')
    message = message.replace('‘', '&lsquo;')
    return message


def prepareRangeMarking(tokens, ranges):
    loc = 0
    output = ''
    for item in ranges:
        start = item[0]
        if '\n' in tokens[start]:
            start += 1
        end = item[1]
        output += ' '.join(tokens[loc:start])
        output += ' <span style="background-color: yellow"> '
        output += ' '.join(tokens[start:end])
        output += ' </span> '
        loc = end
    if loc<len(tokens):
        output += ' '.join(tokens[loc:len(tokens)])
    normalized = normalize(output.replace('  ', ' '))
    return normalized


def prepareCharacterDisplay(characterList, tokenList):

    third_person_pronouns = ['he',
                             'him',
                             'his',
                             'she',
                             'her',
                             'hers',
                             'it',
                             'its',
                             'they',
                             'them',
                             'their',
                             'theirs']
    outhtml = '<!DOCTYPE html><html><head></head><body>'
    tokstr = ''
    toklist = tokenList.copy()
    charNum = 0
    charset = {}
    for character in sorted(characterList.keys()):
        if character.lower() in third_person_pronouns:
            continue
        if len(characterList[character]) > 2:
            charset[character] = characterList[character]
    for character in charset:
        colorList = ['blue',
                     'green',
                     'brown',
                     'orange',
                     'red',
                     'purple',
                     'cyan',
                     'grey',
                     'yellow',
                     'mauve',
                     'teal']
        if len(characterList[character]) > 2:
            for ref in characterList[character]:
                if charNum < len(colorList):
                    toklist = toklist[:ref] \
                              + ['<u><font color="'
                                 + colorList[charNum]
                                 + '">' + toklist[ref]
                                 + '</font></u>'] \
                              + toklist[ref + 1:]
        charNum += 1
        tokstr = normalize(' '.join(toklist))
    headstr = '<ul>'
    charNum = 0
    for character in charset:
        headstr += '<li><font color="' \
                   + colorList[charNum] \
                   + '">' \
                   + character \
                   + '</font></li>'
        charNum += 1
    outhtml += headstr + '</ul><hr>' + tokstr + '</body></html>'
    return outhtml


def prepareConcreteDetailDisplay(tokens, details):
    loc = 0
    output = ''
    for item in details:
        detailLoc = item
        output += ' '.join(tokens[loc:detailLoc])
        output += ' <span style="background-color: yellow">' \
                  + tokens[detailLoc] + '</span> '
        loc = detailLoc + 1
    output += ' '.join(tokens[loc:len(tokens)])
    return normalize(output)


def prepareSceneDisplay(text,
                        tokens,
                        transitions,
                        in_direct_speech,
                        in_past_tense_scope,
                        locations):

    displayText = '<!DOCTYPE html><html><head></head><body>'
    headstr = '<ul><li><span style="background-color: #90ee90">' \
              + 'Times</span></li><li><span style=' \
              + '"background-color: yellow">Places</span></li>' \
              + '<li><span style="background-color: #c39bd3">Comments</span></li></ul>'
    displayText += headstr
    numComments = 0
    numPresent = 0
    lastCommentIndex = -2
    for index in tokens:
        if index in in_past_tense_scope \
           and not in_past_tense_scope[index]['value']:
            numPresent += 1
    for index in tokens:
        tenseInfo = False
        if index in in_past_tense_scope:
            tenseInfo = in_past_tense_scope[index]['value']
        directSpeech = False
        if index in in_direct_speech:
            directSpeech = in_direct_speech[index]['value']
        location = False
        if index in locations:
            location = locations[index]['value']
        temporal = False
        if index in transitions:
            value = transitions[index]['value']
            if value is not None and value == 'temporal':
                temporal = True
        if location:
            displayText += \
                '<span style="background-color: yellow">' \
                + tokens[index]['text'] \
                + '</span>'
        elif temporal:
            displayText += \
                '<span style="background-color: #90ee90">' \
                + tokens[index]['text'] \
                + '</span>'
        elif not tenseInfo and 1.0*numPresent/len(tokens)<.25:
            if lastCommentIndex + 1 < int(index):
                numComments+=1
            lastCommentIndex = int(index)
            displayText += \
                '<span style="background-color: #c39bd3">' \
                + tokens[index]['text'] \
                + '</span>'
        else:
            displayText += \
                tokens[index]['text']
    displayText += '</body></html>'
    return displayText, numComments


def displaySingleList(tokList, valueList):

    # reformat for convenience
    values = [False] * len(tokens)
    for entry in valueList:
        for loc in range(valueList[entry]['startToken'],
                         valueList[entry]['endToken']+1):
            values[loc] = True

    tokens2 = []
    outhtml = '<!DOCTYPE html><html><head></head><body>'
    for index in tokList:
       token = tokList[index]['text']
       highlight = False
       if values[int(index)]:
           highlight = True
       if highlight:
           outhtml += \
               '<span style="background-color: yellow">' \
               + token + '</span>'
       else:
           outhtml += token
    outhtml += '</body></html>'
    return outhtml
    

def displayDialogue(tokList, quotedTextList, dsList):

    # reformat for convenience
    tokens = [entry['value'] for entry in tokList.values()]
    quoted = [entry['value'] for entry in quotedTextList.values()]
    directspeech = [False] * len(tokens)
    for entry in dsList:
        for loc in range(dsList[entry]['startToken'],
                         dsList[entry]['endToken']+1):
            directspeech[loc] = True

    tokens2 = []
    outhtml = '<!DOCTYPE html><html><head></head><body>'
    for index in tokList:
       token = tokList[index]['value']
       quoted = False
       if index in quotedTextList:
           quoted = quotedTextList[index]['value']
       if quoted:
           outhtml += \
               '<span style="background-color: #90ee90">' \
               + token + '</span>'
       elif directspeech[int(index)]:
           outhtml += \
               '<span style="background-color: #87cefa">' \
               + token + '</span>'
       else:
           outhtml += token
    outhtml += '</body></html>'
    return outhtml


def prepareCompoundComplexDisplay(ccd,
                                  posinfo,
                                  sents,
                                  tokens,
                                  opt1,
                                  opt2,
                                  opt3,
                                  opt4,
                                  opt5,
                                  opt6,
                                  opt7):

    outhtml = '<!DOCTYPE html><html><head></head><body>'
    for i, sent in enumerate(sents):
        if ccd[i] == 'Simple':
            if opt1:
                outhtml += '<span style="font-style: bold;' \
                           + ' background-color: #AFEEEE">' \
                           + normalize(' '.join(tokens[sent[0]:sent[1]])) \
                           + '</span> '
            else:
                outhtml += normalize(' '.join(tokens[sent[0]:sent[1]])) + ' '
        elif ccd[i] == 'SimpleComplexPred':
            if opt2:
                outhtml += '<span style="font-style: bold;' \
                         + ' background-color: #AFEEEE">' \
                         + normalize(' '.join(tokens[sent[0]:sent[1]]))	 \
                         + '</span> '
            else:
                outhtml += normalize(' '.join(tokens[sent[0]:sent[1]])) + ' '
        elif ccd[i] == 'SimpleCompoundPred':
            if opt3:
                outhtml += '<span style="font-style: bold;' \
                           + ' background-color: #AFEEEE">' \
                           + normalize(' '.join(tokens[sent[0]:sent[1]])) \
                           + '</span> '
            else:
                outhtml += normalize(' '.join(tokens[sent[0]:sent[1]])) + ' '
        elif ccd[i] == 'SimpleCompoundComplexPred':
            if opt4:
                outhtml += '<span style="font-style: bold;' \
                           + ' background-color: #AFEEEE">' \
                           + normalize(' '.join(tokens[sent[0]:sent[1]])) \
                           + '</span> '
            else:
                outhtml += normalize(' '.join(tokens[sent[0]:sent[1]])) + ' '
        elif ccd[i] == 'Compound':
            if opt5:
                outhtml += '<span style="font-style: bold;' \
                           + ' background-color: #AFEEEE">' \
                           + normalize(' '.join(tokens[sent[0]:sent[1]])) \
                           + '</span> '
            else:
                outhtml += normalize(' '.join(tokens[sent[0]:sent[1]]))

        elif ccd[i] == 'Complex':
            if opt6:
                outhtml += '<span style="font-style: bold;' \
                           + ' background-color: #AFEEEE">' \
                           + normalize(' '.join(tokens[sent[0]:sent[1]])) \
                           + '</span> '
            else:
                outhtml += normalize(' '.join(tokens[sent[0]:sent[1]])) + ' '
        elif ccd[i] == 'CompoundComplex':
            if opt7:
                outhtml += '<span style="font-style: bold;' \
                           + ' background-color: #AFEEEE">' \
                           + normalize(' '.join(tokens[sent[0]:sent[1]])) \
                           + '</span> '
            else:
                outhtml += normalize(' '.join(tokens[sent[0]:sent[1]])) + ' '
        else:
            outhtml += normalize(' '.join(tokens[sent[0]:sent[1]])) \
                          + ' '
    outhtml += '</body></html>'
    outhtml = outhtml.replace('\n', '<br />')
    outhtml = outhtml.replace('</span> <span style="font-style: bold;'
                              + ' background-color: #AFEEEE">', ' ')
    outhtml = normalize(outhtml)
    return outhtml


def prepareToneDisplay(tone,
                       posinfo,
                       tokens,
                       threshold1,
                       threshold2,
                       threshold3,
                       threshold4,
                       threshold5):
    outhtml = '<!DOCTYPE html><html><head></head><body>'
    countB1 = 0
    countB2 = 0
    countB3 = 0
    countB4 = 0
    countB5 = 0
    for i, token in enumerate(tokens):
        if posinfo[i] in ['PUNCT', 'SPACE', 'SYM'] \
           or '\'' in tokens[i]:
            outhtml += tokens[i] + ' '
        elif tone[i] > 0.4:
            if threshold1:
                outhtml += '<span style="font-style: bold;' \
                           + ' background-color: #AFEEEE">' \
                           + tokens[i] + '</span> '
            else:
                outhtml += tokens[i] + ' '
            countB1 += 1
        elif tone[i] <= .4 and tone[i] > .15:
            if threshold2:
                outhtml += '<span style="font-style: bold;' \
                           + ' background-color: #AFEEEE">' \
                           + tokens[i] + '</span> '
            else:
                outhtml += tokens[i] + ' '
            countB2 += 1
        elif tone[i] >= -.2 and tone[i] <= .15:
            if threshold3:
                outhtml += '<span style="font-style: bold;' \
                           + ' background-color: #AFEEEE">' \
                           + tokens[i] + '</span> '
            else:
                outhtml += tokens[i] + ' '
            countB3 += 1
        elif tone[i] < -.2 and tone[i] > -.4:
            if threshold4:
                outhtml += '<span style="font-style: bold;' \
                           + ' background-color: #AFEEEE">' \
                           + tokens[i] \
                           + '</span> '
            else:
                outhtml += tokens[i] + ' '
            countB4 += 1
        elif tone[i] <= -.4:
            if threshold5:
                outhtml += '<span style="font-style: bold;' \
                           + ' background-color: #AFEEEE">' \
                           + tokens[i] \
                           + '</span> '
            else:
                outhtml += tokens[i] + ' '
            countB5 += 1
        else:
            outhtml += tokens[i] + ' '
            countB6 += 1
    outhtml += '</body></html>'
    outhtml = outhtml.replace('\n', '<br />')
    outhtml = outhtml.replace('</span> <span style="font-style: bold;'
                              + ' background-color: #AFEEEE">', ' ')
    outhtml = normalize(outhtml)
    return outhtml, countB1, countB2, countB3, countB4, countB5


def prepareSyllableDisplay(syl,
                           posinfo,
                           tokens,
                           threshold1,
                           threshold2,
                           threshold3,
                           threshold4):

    outhtml = '<!DOCTYPE html><html><head></head><body>'
    countB1 = 0
    countB2 = 0
    countB3 = 0
    countB4 = 0
    for i, token in enumerate(tokens):
        if posinfo[i] in ['PUNCT', 'SPACE', 'SYM'] \
           or '\'' in tokens[i] \
           or syl[i] is None:
            outhtml += tokens[i] + ' '
        elif syl[i] > 3:
            if threshold1:
                outhtml += '<span style="font-style: bold;' \
                           + ' background-color: #AFEEEE">' \
                           + tokens[i] + '</span> '
            else:
                outhtml += tokens[i] + ' '
            countB1 += 1
        elif syl[i] == 3:
            if threshold2:
                outhtml += '<span style="font-style: bold;' \
                           + ' background-color: #AFEEEE">' \
                           + tokens[i] + '</span> '
            else:
                outhtml += tokens[i] + ' '
            countB2 += 1
        elif syl[i] == 2:
            if threshold3:
                outhtml += '<span style="font-style: bold;' \
                           + ' background-color: #AFEEEE">' \
                           + tokens[i] + '</span> '
            else:
                outhtml += tokens[i] + ' '
            countB3 += 1
        elif syl[i] == 1:
            if threshold4:
                outhtml += '<span style="font-style: bold;' \
                           + ' background-color: #AFEEEE">' \
                           + tokens[i] + '</span> '
            else:
                outhtml += tokens[i] + ' '
            countB3 += 1
        else:
            outhtml += tokens[i] + ' '
            countB4 += 1
    outhtml += '</body></html>'
    outhtml = outhtml.replace('\n', '<br />')
    outhtml = outhtml.replace('</span> <span style="font-style: bold;'
                              + ' background-color: #AFEEEE">', ' ')
    outhtml = normalize(outhtml)
    return outhtml, countB1, countB2, countB3, countB4


def prepareFrequencyDisplay(fr,
                            posinfo,
                            tokens,
                            threshold1,
                            threshold2,
                            threshold3,
                            threshold4,
                            threshold5,
                            threshold6,
                            threshold7):

    outhtml = '<!DOCTYPE html><html><head></head><body>'
    countB1 = 0
    countB2 = 0
    countB3 = 0
    countB4 = 0
    countB5 = 0
    countB6 = 0
    countB7 = 0
    for i, token in enumerate(tokens):
        if posinfo[i] in ['PUNCT', 'SPACE', 'SYM'] \
           or '\'' in tokens[i]:
            outhtml += tokens[i] + ' '
        elif fr[i] > 7:
            if threshold1:
                outhtml += '<span style="font-style: bold;' \
                           + ' background-color: #AFEEEE">' \
                           + tokens[i] + '</span> '
            else:
                outhtml += tokens[i] + ' '
            countB1 += 1
        elif fr[i] <= 7 and fr[i] > 6:
            if threshold2:
                outhtml += '<span style="font-style: bold;' \
                           + ' background-color: #AFEEEE">' \
                           + tokens[i] + '</span> '
            else:
                outhtml += tokens[i] + ' '
            countB2 += 1
        elif fr[i] <= 6 and fr[i] > 5:
            if threshold3:
                outhtml += '<span style="font-style: bold;' \
                           + ' background-color: #AFEEEE">' \
                           + tokens[i] + '</span> '
            else:
                outhtml += tokens[i] + ' '
            countB3 += 1
        elif fr[i] <= 5 and fr[i] > 4:
            if threshold4:
                outhtml += '<span style="font-style: bold;' \
                           + ' background-color: #AFEEEE">' \
                           + tokens[i] + '</span> '
            else:
                outhtml += tokens[i] + ' '
            countB4 += 1
        elif fr[i] <= 4 and fr[i] > 3:
            if threshold5:
                outhtml += '<span style="font-style: bold;' \
                           + ' background-color: #AFEEEE">' \
                           + tokens[i] + '</span> '
            else:
                outhtml += tokens[i] + ' '
            countB5 += 1
        elif fr[i] <= 3 and fr[i] > 4:
            if threshold6:
                outhtml += '<span style="font-style: bold;' \
                           + ' background-color: #AFEEEE">' \
                           + tokens[i] + '</span> '
            else:
                outhtml += tokens[i] + ' '
            countB6 += 1
        elif fr[i] <= 2:
            if threshold7:
                outhtml += '<span style="font-style: bold;' \
                           + ' background-color: #AFEEEE">' \
                           + tokens[i] + '</span> '
            else:
                outhtml += tokens[i] + ' '
            countB7 += 1
        else:
            outhtml += tokens[i] + ' '
    outhtml += '</body></html>'
    outhtml = outhtml.replace('\n', '<br />')
    outhtml = outhtml.replace('</span> <span style="font-style: bold;'
                              + ' background-color: #AFEEEE">', ' ')
    outhtml = normalize(outhtml)
    return outhtml, countB1, countB2, countB3, countB4, \
        countB5, countB6, countB7


def prepareEmotionDisplay(em, tokens):
    outhtml = '<!DOCTYPE html><html><head></head><body>'
    for i, token in enumerate(tokens):
        if em[i]:
            outhtml += '<span style="font-style: bold;' \
                       + ' background-color: #AFEEEE">' \
                       + tokens[i] + '</span> '
        else:
            outhtml += tokens[i] + ' '
    outhtml += '</body></html>'
    outhtml = outhtml.replace('\n', '<br />')
    outhtml = outhtml.replace('</span> <span style="font-style: bold;'
                              + ' background-color: #AFEEEE">', ' ')
    outhtml = normalize(outhtml)
    return outhtml


def prepareSimpleDisplay(il, tokens):
    outhtml = '<!DOCTYPE html><html><head></head><body>'
    for i, token in enumerate(tokens):
        if i in il:
            outhtml += '<span style="font-style: bold;' \
                       + ' background-color: #AFEEEE">' \
                       + tokens[i] + '</span> '
        else:
            outhtml += tokens[i] + ' '
    outhtml += '</body></html>'
    outhtml = outhtml.replace('\n', '<br />')
    outhtml = outhtml.replace('</span> <span style="font-style: bold;'
                              + ' background-color: #AFEEEE">', ' ')
    outhtml = normalize(outhtml)
    return outhtml


def preparePOSDisplay(pos, choice, tokens):
    outhtml = '<!DOCTYPE html><html><head></head><body>'
    for i, item in enumerate(pos):
        if item == choice:
            outhtml += '<span style="font-style: bold;' \
                       + ' background-color: #AFEEEE">' \
                       + tokens[i] + '</span> '
        else:
            outhtml += tokens[i] + ' '
    outhtml += '</body></html>'
    outhtml = outhtml.replace('\n', '<br />')
    return outhtml


def prepareSupportingIdeas(ec):
    lastoffset = 0
    lastlength = 0
    outhtml = '<!DOCTYPE html><html><head></head><body>'
    for item in ec:
        outhtml += normalize(' '.join(tokens[lastoffset:item[0]]))
        outhtml += '<span style="font-style: bold;' \
                   + ' background-color: #AFEEEE">' \
                   + normalize(' '.join(tokens[item[0]:item[1]])) \
                   + '</span>'
        lastoffset = item[1]
    outhtml += normalize(' '.join(tokens[lastoffset:]))
    outhtml += '</body></html>'
    outhtml = outhtml.replace('\n', '<br />')
    return outhtml


def prepareQuoteCite(quotedtext, attributions, sources, citedtext):
    lastlength = 0
    outhtml = '<!DOCTYPE html><html><head></head><body>'
    inCite = False
    inQuote = False
    inAttrib = False
    for i, item in enumerate(quotedtext):
        if ((inCite
             or inQuote
             or inAttrib)
            and (item
                 or citedtext[i]
                 or sources[i]
                 or attributions[i])):
            outhtml += tokens[i] + ' '
        elif (inCite or inQuote or inAttrib):
            outhtml += tokens[i] + ' </span>'
            inCite = False
            inQuote = False
            inAttrib = False
        elif item:
            outhtml += '<span style="font-style: bold;' \
                       + ' background-color: #afeeee">' \
                       + tokens[i] + ' '
            inQuote = True
        elif citedtext[i]:
            outhtml += '<span style="font-style: bold;' \
                       + ' background-color: #ffff00">' \
                       + tokens[i] + ' '
            inCite = True
        elif sources[i] or attributions[i]:
            outhtml += '<span style="font-style: bold;' \
                       + ' background-color: #90ee90">' \
                       + tokens[i] + ' '
            inAttrib = True
        else:
            outhtml += tokens[i] + ' '
        lastoffset = i
    outhtml += '</body></html>'
    outhtml = normalize(outhtml.replace('\n', '<br />'))
    return outhtml


def prepareCorrections(result, text):
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

        if item['label'] + '/' + item['detail'] in detailcounts:
            detailcounts[item['label']
                         + '/'
                         + item['detail']] += 1
        else:
            detailcounts[item['label']
                         + '/'
                         + item['detail']] = 1
        outhtml += text[lastoffset:item['offset']]
        outhtml += '<span style=\"background-color: #ffeb2a\" type=\"' \
                   + item['label'] \
                   + '\" subtype=\"' \
                   + item['detail'] \
                   + '\" title="' \
                   + fixMessage(html.unescape(item['message'])) \
                   + '\">'
        outhtml += text[item['offset']:item['offset']+item['length']]
        outhtml += '</span> '
        lastoffset = item['offset'] + item['length']
        lastlength = item['length']
    outhtml += text[lastoffset:]
    outhtml += '</body></html>'
    outhtml = outhtml.replace('\n', '<br />')
    total = 0
    return outhtml


def prepareAcademicWordInfo(academics, latinates, tokens):
    academic_words = []
    for i, token in enumerate(tokens):
        if academics[i] is not None and academics[i] \
           or latinates[i] is not None and latinates[i]:
            if token.lower() not in academic_words:
                academic_words.append(token.lower())
    academic_words = sorted(academic_words)
    outhtml = '<!DOCTYPE html><html><head></head><body><p><b>'
    outhtml += ', '.join(academic_words) + '</b></p>'
    for i, token in enumerate(tokens):
        if academics[i] is not None and academics[i] \
           or latinates[i] is not None and latinates[i]:
            outhtml += '<span style="background-color: #ffff00 ">' \
                        + token \
                        + '</span> '
        else:
            outhtml += token + ' '
    outhtml += '</body></html>'
    outhtml = outhtml.replace('\n', '<br />')
    return academic_words, outhtml


def prepareTransitionMarking(tokens,
                             transitions,
                             content_segments):
    loc = 0
    lastStart = -1
    output = ''
    categories = {}
    prefix = '<div>'
    colorList = ["#FAED27",
                 "#7ddaff",
                 "#fcc9e3",
                 "#cee5ce",
                 "#ddd3ee",
                 "#f7bc81",
                 "#7979ED",
                 '#C4A484',
                 'cyan',
                 'mauve',
                 'purple']

    current_segment = 0
    temp = []
    openDiv = False
    temp = tokens

    loc = 0
    for i, item in enumerate(transitions[1]):
        if item != 'PARAGRAPH':
            categories[item] = i
            if item == 'temporal':
                prefix += ' <li style="display: inline">' \
                          + '<span title="Time"' \
                          + ' style="background-color: ' \
                          + colorList[i] + '">Time</span></li>'
            elif item == 'contrastive':
                prefix += ' <li style="display: inline">' \
                          + '<span title="Difference"' \
                          + ' style="background-color: ' \
                          + colorList[i] + '">Difference</span></li>'
            elif item == 'comparative':
                prefix += ' <li style="display: inline">' \
                          + '<span title="Similarity"' \
                          + ' style="background-color: ' \
                          + colorList[i] + '">Similarity</span></li>'
            elif item == 'illustrative':
                prefix += ' <li style="display: inline">' \
                          + '<span title="Illustration"' \
                          + ' style="background-color: ' \
                          + colorList[i] + '">Illustration</span></li>'
            elif item == 'emphatic':
                prefix += ' <li style="display: inline">' \
                          + '<span title="Emphasis"' \
                          + ' style="background-color: ' \
                          + colorList[i] + '">Emphasis</span></li>'
            elif item == 'ordinal':
                prefix += ' <li style="display: inline">' \
                          + '<span title="List" style="background-color: ' \
                          + colorList[i] + '">List</span></li>'
            elif item == 'evidentiary':
                prefix += ' <li style="display: inline">' \
                          + '<span title="List" style="background-color: ' \
                          + colorList[i] + '">Evidence</span></li>'
            elif item == 'conditional':
                prefix += ' <li style="display: inline">' \
                          + '<span title="Condition"' \
                          + ' style="background-color: ' \
                          + colorList[i] + '">Condition</span></li>'
            elif item == 'counterpoint':
                prefix += ' <li style="display: inline">' \
                          + '<span title="Counterpoint"' \
                          + ' style="background-color: ' \
                          + colorList[i] \
                          + '">Counterpoint</span></li>'
            elif item == 'consequential':
                prefix += ' <li style="display: inline">' \
                          + '<span title="Consequences"' \
                          + ' style="background-color: ' \
                          + colorList[i] \
                          + '">Consequences</span></li>'
    prefix += '</div><hr>'
    covered = []
    for item in transitions[3]:
        sentenceStart = item[1]
        start = item[2]
        end = item[3]
        if item[3] not in covered:
            output += ' '.join(temp[loc:start]) + ' '

        if item[4] != 'PARAGRAPH' and item[3] not in covered:
            if '>' in temp[start]:
                left = temp[start][0:temp[start].index('>') + 1]
                right = temp[start][temp[start].index('>') + 1:]
                if '\n' not in temp[start]:
                    output += left
                    temp[start] = right
                else:
                    temp[start] = right + left
            colorchoice = categories[item[4]]
            if item[4] == 'temporal':
                output += ' <span title="Time"' \
                          + ' style="background-color: ' \
                          + colorList[colorchoice] + '">'
            elif item[4] == 'contrastive':
                output += ' <span title="Difference"' \
                          + ' style="background-color: ' \
                          + colorList[colorchoice] + '">'
            elif item[4] == 'comparative':
                output += ' <span title="Similarity"' \
                          + ' style="background-color: ' \
                          + colorList[colorchoice] + '">'
            elif item[4] == 'illustrative':
                output += ' <span title="Illustration"' \
                          + ' style="background-color: ' \
                          + colorList[colorchoice] + '">'
            elif item[4] == 'emphatic':
                output += ' <span title="Emphasis"' \
                          + ' style="background-color: ' \
                          + colorList[colorchoice] + '">'
            elif item[4] == 'ordinal':
                output += ' <span title="List"' \
                          + ' style="background-color: ' \
                          + colorList[colorchoice] + '">'
            elif item[4] == 'evidentiary':
                output += ' <span title="Evidence"' \
                          + ' style="background-color: ' \
                          + colorList[colorchoice] + '">'
            elif item[4] == 'conditional':
                output += ' <span title="Condition"' \
                          + ' style="background-color: ' \
                          + colorList[colorchoice] + '">'
            elif item[4] == 'counterpoint':
                output += ' <span title="Counterpoint"' \
                          + ' style="background-color: ' \
                          + colorList[colorchoice] + '">'
            elif item[4] == 'consequential':
                output += ' <span title="Consequences"' \
                          + 'style="background-color: ' \
                          + colorList[colorchoice] + '">'
            else:
                output += ' <span title="' \
                          + item[4] + \
                         '" style="background-color: grey"> '
        if item[3] not in covered:
            output += ' '.join(temp[start:end+1]) + ' '
        if item[0] != 'NEWLINE' and item[3] not in covered:
            output += '</span> '
        loc = end + 1
        lastStart = sentenceStart
        if item[3] not in covered:
            covered.append(item[3])
    output += ' '.join(temp[loc:len(tokens)])
    return prefix + normalize(output)


def prepareArgumentWordMarking(tokens,
                               lemmas,
                               argumentwords,
                               explicitargwords,
                               promptlanguage,
                               promptrelated,
                               contentwords,
                               core):

    coreloc = 0
    start = 0
    end = 0
    temp = []
    openDiv = False
    inPromptSentences = []
    for i, item in enumerate(tokens):
        if core is not None and coreloc < len(core):
            start = core[coreloc][0]
            end = core[coreloc][1]
            if i >= start and i <= end:
                inPromptSentences.append(i)
            if i == start:
                openDiv = True
                if '\n' in tokens[i]:
                    temp.append(tokens[i]
                                + '<br /><div style="border:1px solid black;'
                                + ' margin: 5px; padding: 5px;'
                                + ' background-color: #E0FFFF">')
                else:
                    temp.append('<div style="border:1px solid black;'
                                + ' margin: 5px; padding: 5px;'
                                + ' background-color: #E0FFFF">'
                                + tokens[i])
                    openDiv = True
            elif i == end:
                if coreloc + 1 < len(core) \
                   and core[coreloc + 1][0] == end:
                    temp[i-1] += ' '
                else:
                    if '\n' in temp[i-1]:
                        temp[i - 1] = '</div>' + temp[i - 1]
                        openDiv = False
                    else:
                        temp[i-1] += '</div>'
                        openDiv = False
                if '\n' in tokens[i]:
                    if coreloc + 1 < len(core) \
                       and core[coreloc + 1][0] == end:
                        temp.append('</div>'
                                    + tokens[i]
                                    + '<br />'
                                    + '<div style="border:1px solid black;'
                                    + ' margin: 5px; padding: 5px;'
                                    + ' background-color: #E0FFFF">')
                        openDiv = False
                    else:
                        temp.append(tokens[i] + '<br />')
                else:
                    temp.append(tokens[i])
                coreloc += 1
            else:
                if '\n' in tokens[i]:
                    temp.append(tokens[i] + '<br />')
                else:
                    temp.append(tokens[i])
        else:
            temp.append(tokens[i])
    if openDiv:
        temp[len(temp)-1] += '</div>'

    essaystructure = temp
    temp = tokens

    loc = 0
    prefix2 = '<div style="width: 100%; display:flex;' \
              + ' flex-direction: row; justify-content: center;' \
              + ' align-items: center"><ul><li style="display: inline;' \
              + ' float: left; border:1px solid black; margin: auto;' \
              + ' padding: 5px; background-color: #AFEEEE">' \
              + 'Words Related to the Prompt' \
              + '</li><li style="display: inline; float: left;' \
              + ' border:none; margin: auto; padding: 5px">' \
              + '&nbsp;</li><li style="display: inline;' \
              + ' border:1px solid black; margin: auto;' \
              + ' padding: 5px; text-decoration: underline;' \
              + ' float: left; background-color: #FAED27">' \
              + 'Explicit Argument Words' \
              + '</li><li style="display: inline; float: left;' \
              + ' border:none; margin: auto; padding: 5px">' \
              + '&nbsp;</li><li style="display: inline;' \
              + ' border:1px solid black; margin: auto;' \
              + ' padding: 5px; text-decoration: underline;' \
              + ' float: left; background-color: #e4e4e4">' \
              + 'Supporting Academic Language' \
              + '</li></ul></div><hr style="width: 100%">'
    output = ''
    promptvoc = []
    if promptlanguage is not None and len(promptlanguage) > 0:
        for item in promptlanguage:
            promptvoc.append(item)
    if promptrelated is not None and len(promptrelated) > 0:
        for item in promptrelated:
            for word in item[2]:
                if word not in promptvoc \
                   and item in inPromptSentences:
                    promptvoc.append(word)
    temp = []
    for i, token in enumerate(tokens):
        if lemmas[i] in promptvoc \
           and (i not in contentwords
                or lemmas[i].lower() in promptlanguage) \
           and (i not in argumentwords
                or i in explicitargwords
                or (lemmas[i] is not None
                    and lemmas[i].lower() in promptlanguage)):
            temp.append(' <span style="text-decoration: underline;'
                        + ' background-color: #AFEEEE">' + token + '</span> ')
        else:
            temp.append(token)
    inSpan = False
    for item in argumentwords:
        output += ' '.join(temp[loc:item]) + ' '
        if item in ['\'s', '\'d', '\'ll', '\'ve', '\'m', 'n\'t']:
            output += item
        elif (item in explicitargwords
              and lemmas[item] is not None
              and lemmas[item].lower() not in promptvoc):
            output += ' <span style="text-decoration: underline;' \
                      + ' background-color: #FAED27"> '
            inSpan = True
        elif (lemmas[item] is not None
              and lemmas[item].lower() not in promptvoc):
            output += ' <span style="text-decoration: underline;' \
                      + ' background-color: #e4e4e4"> '
            inSpan = True
        output += temp[item]
        if item not in ['\'s', '\'d', '\'ll', '\'ve', '\'m', 'n\'t'] \
           and inSpan \
           and lemmas[item] is not None \
           and lemmas[item].lower() not in promptvoc:
            output += ' </span> '
            inSpan = False
        loc = item+1
    output += ' '.join(temp[loc:len(temp)])
    output = output.replace('</div></span>', '</span></div>')
    output = output.replace('</div> </span>', '</span></div>')
    output = output.replace('<span style="text-decoration: underline">'
                            + ' <div style="border:1px solid black;'
                            + ' margin: 5px; padding: 5px;'
                            + ' background-color: #E0FFFF">',
                            '<div style="border:1px solid black;'
                            + ' margin: 5px; padding: 5px;'
                            + ' background-color: #E0FFFF">'
                            + ' <span style="text-decoration: underline;'
                            + ' background-color: #AFEEEE">')
    output = output.replace(' <span style="text-decoration: underline;'
                            + ' background-color: #AFEEEE"><br />'
                            + '<div style="border:1px solid black;'
                            + ' margin: 5px; padding: 5px;'
                            + ' background-color: #E0FFFF">',
                            '<br /><div style="border:1px solid black;'
                            + ' margin: 5px; padding: 5px;'
                            + ' background-color: #E0FFFF">'
                            + ' <span style="text-decoration:'
                            + ' underline; background-color: #AFEEEE">')
    return normalize(' '.join(essaystructure)), prefix2 + normalize(output)


def preparePOSDisplayPage(pos, option3, tokens):
    if option3 == 'Noun':
        page = preparePOSDisplay(pos, 'NOUN', tokens)
    elif option3 == 'Proper Noun':
        page = preparePOSDisplay(pos, 'PROPN', tokens)
    elif option3 == 'Verb':
        page = preparePOSDisplay(pos, 'VERB', tokens)
    elif option3 == 'Adjective':
        page = preparePOSDisplay(pos, 'ADJ', tokens)
    elif option3 == 'Adverb':
        page = preparePOSDisplay(pos, 'ADV', tokens)
    elif option3 == 'Number':
        page = preparePOSDisplay(pos, 'NUM', tokens)
    elif option3 == 'Preposition':
        page = preparePOSDisplay(pos, 'ADP', tokens)
    elif option3 == 'Coordinating Conjunction':
        page = preparePOSDisplay(pos, 'CCONJ', tokens)
    elif option3 == 'Subordinating Conjunction':
        page = preparePOSDisplay(pos, 'SCONJ', tokens)
    elif option3 == 'Auxiliary Verb':
        page = preparePOSDisplay(pos, 'AUX', tokens)
    elif option3 == 'Pronoun':
        page = preparePOSDisplay(pos, 'PRON', tokens)
    else:
        page = ''
    return page


def prepareSubjectivityDisplay(tokens, ps, sm, option2, option3):
    perspectives = tokens.copy()
    for i, token in enumerate(tokens):
        perspectives[i] = None

    print(sm)
    stancemarkers = [False] * len(tokens)
    for entry in sm:
        print(entry)
    stancelocs = [sm[entry]['startToken'] for entry in sm]
    for i, token in enumerate(tokens):
        if i in stancelocs:
            stancemarkers[i] = True

    print(ps)
    perspectives = ['WRITER'] * len(tokens)
    for entry in ps:
        index = int(ps[entry]['startToken'])
        value = ps[entry]['value']
        if type(value) == str:
            perspectives[index] = value
        elif type(value) == int:
            perspectives[index] = 'THIRDPERSON'

    output = []
    for i, token in enumerate(tokens):
        if option2 == 'Details' \
           and perspectives[i] == 'OTHER':

            output.append('<span style="font-style: bold;'
                          + ' background-color: #AFEEEE"> '
                          + tokens[i] + ' </span>')

        elif '\n' in tokens[i]:
            output.append(tokens[i])
        elif (perspectives[i] in ['WRITER', 'SELF']
              and not stancemarkers[i]
              and option3 == 'Author\'s Perspective'):

            output.append('<span style="font-style: italic;'
                          + ' background-color: #ffffa1"> '
                          + tokens[i] + ' </span>')

        elif (perspectives[i] in ['WRITER', 'SELF']
              and option3 == 'Author\'s Perspective'):

            output.append('<span style="font-style: italic;'
                          + ' background-color: #ffffa1"><u> '
                          + tokens[i] + ' </u></span>')

        elif (perspectives[i] == 'AUDIENCE'
              and stancemarkers[i]
              and option3 == 'Audience Perspective'):

            output.append('<u><span title="Second Person"'
                          + ' style="font-style: italic;'
                          + ' background-color: #7ddaff"> '
                          + tokens[i] + ' </span></u>')

        elif (perspectives[i] == 'AUDIENCE'
              and option3 == 'Audience Perspective'):

            if not stancemarkers[i]:
                output.append('<span title="Second Person"'
                              + ' style="background-color: #7ddaff"> '
                              + tokens[i] + ' </span>')
            else:
                output.append('<span title="Second Person"'
                              + ' style="background-color: #7ddaff">'
                              + '<u> ' + tokens[i] + ' </u></span>')
        elif (option3 == 'Other Perspective'
              and perspectives[i] == 'THIRDPERSON'):

            if not stancemarkers[i]:
                output.append('<span title="Third Person"'
                              + ' style="background-color: #f7bc81"> '
                              + tokens[i] + ' </span>')
            else:
                output.append('<span title="Third Person"'
                              + ' style="background-color: #f7bc81">'
                              + '<u> ' + tokens[i] + ' </u></span>')
        else:
            output.append(tokens[i])

    return ' '.join(output), perspectives, stancemarkers


def prepareClaimDiscussionTextDisplay(tokens,
                                      ct,
                                      dt,
                                      core,
                                      perspectives,
                                      stancemarkers):

    temp1 = []
    temp2 = []

    cv = [False]*len(tokens)
    for item in core:
        for offset in range(item[0], item[1]):
            cv[offset] = True

    for i, token in enumerate(tokens):
        if dt[i] and not cv[i] and perspectives[i] != 'OTHER':
            temp1.append('<span style="font-style: italic;'
                         + ' background-color: #CEE5CE"> '
                         + token + ' </span>')
            temp2.append('<span style="font-style: italic;'
                         + ' background-color: #DDD3EE"> '
                         + token + ' </span>')
        elif ct[i] and not cv[i] and perspectives[i] != 'OTHER':
            temp1.append('<span style="font-style: italic;'
                         + ' background-color: #CEE5CE"> '
                         + token + ' </span>')
            temp2.append(' ' + token)
        else:
            temp1.append(' ' + token)
            temp2.append(' ' + token)
    return normalize(''.join(temp1)), normalize(''.join(temp2))


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


option0 = st.selectbox('',
                       ('GRE Essays',
                        'Censorship Essays',
                        'Narratives'))


# specify where to get the files we want to load
examplepath = os.path.dirname(__file__)
locs = []

if option0 == 'GRE Essays':
    for i in range(2, 7):
        tname = 'essays/gre' + str(i) + '.txt'
        locs.append(os.path.join(examplepath, tname))
elif option0 == 'Censorship Essays':
    for i in range(1, 26):
        tname = 'essays/censorship' + str(i) + '.txt'
        locs.append(os.path.join(examplepath, tname))
else:
    locs.append(os.path.join(examplepath, 'essays/leprechaun.txt'))
    locs.append(os.path.join(examplepath, 'essays/lion.txt'))

documents = []
for i, fname in enumerate(locs):
    with open(fname) as f:
        contents = f.read()
        documents.append(contents)

# Set up document labels
document_labels = []
if option0 == 'GRE Essays':
    for i in range(2, 7):
        document_labels.append('GRE_Essay ' + str(i))
elif option0 == 'Censorship Essays':
    for i in range(1, 26):
        document_labels.append('Censorship_Essay ' + str(i))
else:
    for i in range(1, 3):
        document_labels.append('Story ' + str(i))

# Set up UI elements for Streamlit

option = st.selectbox('',
                      tuple(document_labels))

option2 = st.selectbox('',
                       ('Conventions',
                        'Parts of Speech',
                        'Informal Language',
                        'Academic Language',
                        'Word Frequency',
                        'Number of Syllables',
                        'Sentence Variety',
                        'Transitions',
                        'Quotations, Citations, Attributions',
                        'Main Ideas',
                        'Supporting Ideas',
                        'Details',
                        'Statements of Fact',
                        'Statements of Opinion',
                        'Argument Words',
                        'Propositional Attitudes',
                        'Own vs. Other Perspectives',
                        'Characters',
                        'Emotion Words',
                        'Character Traits',
                        'Dialogue',
                        'Scene and Setting',
                        'Social Awareness',
                        'Concrete Details',
                        'Tone'))

option3 = ''
if option2 == 'Own vs. Other Perspectives':
    option3 = st.selectbox('',
                           ('Author\'s Perspective',
                            'Audience Perspective',
                            'Other Perspective'))
elif option2 == 'Parts of Speech':
    option3 = st.selectbox('',
                           ('Noun',
                            'Proper Noun',
                            'Verb',
                            'Adjective',
                            'Adverb',
                            'Number',
                            'Preposition',
                            'Coordinating Conjunction',
                            'Subordinating Conjunction',
                            'Auxiliary Verb',
                            'Pronoun'))
elif option2 == 'Word Frequency':
    option4 = st.checkbox('Very High Frequency Words')  # >7
    option5 = st.checkbox('High Frequency Words')  # 6-7
    option6 = st.checkbox('Medium High Frequency Words')  # 5-6
    option7 = st.checkbox('Medium Low Frequency Words')  # 4-5
    option8 = st.checkbox('Low Frequency Words')  # 3-4
    option9 = st.checkbox('Very Low Frequency Words')  # 2-3
    option10 = st.checkbox('Extremely Rare Words')  # <2
elif option2 == 'Number of Syllables':
    option4 = st.checkbox('Four or More Syllables')
    option5 = st.checkbox('Three Syllables')
    option6 = st.checkbox('Two Syllables')
    option7 = st.checkbox('One Syllable')
elif option2 == 'Sentence Variety':
    option4 = st.checkbox('Simple (Kernel) Sentences')
    option5 = st.checkbox('Simple Sentences with Complex Predicates')
    option6 = st.checkbox('Simple Sentences with Compound Predicates')
    option7 = st.checkbox('Simple Sentences with Compound/Complex Predicates')
    option8 = st.checkbox('Compound Sentences')
    option9 = st.checkbox('Complex Sentences')
    option10 = st.checkbox('Compound/Complex Sentences')
elif option2 == 'Tone':
    option4 = st.checkbox('Highly Positive Tone')
    option5 = st.checkbox('Positive Tone')
    option6 = st.checkbox('Neutral Tone')
    option7 = st.checkbox('Negative Tone')
    option8 = st.checkbox('Highly Negative Tone')

header, count = option.split()
if option0 == 'GRE Essays':
    document_text = documents[int(count)-2]
    document_label = document_labels[int(count)-2]
else:
    document_text = documents[int(count)-1]
    document_label = document_labels[int(count)-1]


# Open clients to communicate with the servers
parser, lt = initialize()
spellcorrect = websocketClient()
labels = parser.send(['LABELS'])


# Run spell correction
for i, dl in enumerate(document_labels):
    if dl not in labels and i < len(documents):
        [text] = spellcorrect.send([documents[i]])
        ok = parser.send(['PARSEONE', dl, text])

[ctext] = spellcorrect.send([document_text])

record = {}
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


# Send spell corrected text to the parser
tokList = parser.send(['AWE_INFO', document_label, 'text', 'Token'])
tok_with_wsList = parser.send(['AWE_INFO', document_label, 'text_with_ws', 'Token'])
tokens = [entry['value'] for entry in tokList.values()]

if tokens is None or len(tokens)==0:
    raise Exception("No tokens recognized")


# Display text outputs in the console and if running under
# streamlit, the formatted pages.

numWords = parser.send(['AWE_INFO',
                        document_label,
                        'text', 'Token', 'total'])
numLemmas = parser.send(['AWE_INFO',
                         document_label,
                        'lemma_', 'Token', 'totaluniq'])
numSentences = parser.send(['AWE_INFO',
                           document_label,
                           'sents', 'Doc', 'total'])
numParas = parser.send(['AWE_INFO',
                        document_label,
                        'delimiter_\n',
                        'Doc',
                        'total'])

print('\nBasic info')
print(numWords, ' words')
print(numLemmas, ' distinct words')
print(numSentences, ' Sentences')
print(numParas, ' paragraphs')


cliList = parser.send(["AWE_INFO",
                       document_label,
                       "all_cluster_info",
                       "Doc"])

if cliList is None:
    raise Exception("No information on word clusters retrieved")
clDict = {}
for entry in cliList.values():
    clDict[entry['text']] = entry['value']
clusters = pd.DataFrame.from_dict(clDict, orient='index')
clusters.index.name = 'Cluster'
clusters.columns = ['Count', 'Importance']
print(clusters)


rootList = parser.send(['AWE_INFO',
                          document_label,
                         'root',
                         'Token',
                         'counts',
                         json.dumps([('is_space', ['False']),
                                     ('is_punct', ['False']),
                                     ('is_stop', ['False'])])])

roots = pd.DataFrame.from_dict(rootList, orient='index')
roots.index.name = 'Root'
roots.columns = ['Frequency']
print(roots)

def proofreadOptions():
    result = lt.processText(record, document_text)
    if result is None:
        raise Exception("No correction information received")

    errorcounts = {}
    detailcounts = {}
    for item in result:

        if item['label'] in errorcounts:
            errorcounts[item['label']] += 1
        else:
            errorcounts[item['label']] = 1

        if item['label'] + '/' + item['detail'] in detailcounts:
            detailcounts[item['label'] + '/' + item['detail']] += 1
        else:
            detailcounts[item['label'] + '/' + item['detail']] = 1

    total = 0
    for key in sorted(errorcounts.keys()):
        total += errorcounts[key]
    print('\nTotal grammar, usage, mechanics, style errors:', total)

    print('\n-------Major error categories--------------------')
    for key in sorted(errorcounts.keys()):
        print(key, ':', errorcounts[key])

    print('\n-------Minor error categories--------------------')
    for key in sorted(detailcounts.keys()):
        print(key, ':', detailcounts[key])

    proofread = prepareCorrections(result, document_text)
    return proofread

def POSOptions():

    print('\nPart of Speech Information')

    posinfoList = parser.send(['AWE_INFO',
                               document_label,
                              'pos_',
                              'Token',
                              'counts'])

    if posinfoList is None:
        raise Exception(
            "No part of speech information retrieved")

    for item in posinfoList:
            print(item, posinfoList[item])

    posinfoList2 = parser.send(['AWE_INFO',
                                document_label,
                                'pos_', 'Token'])

    posinfo = [entry['value'] \
        for entry in posinfoList2.values()]

    POSDisplay = preparePOSDisplayPage(
        posinfo, option3, tokens)
    return POSDisplay

def informalOptions():
    ilList = posinfoList2 = parser.send(['AWE_INFO',
                                        document_label,
                                        'vwp_interactive', 'Token'])

    if ilList is None:
        raise Exception("No information on interactive language retrieved")
    il = []
    for entry in ilList.values():
        if entry['value']:
            il.append(entry['tokenIdx'])

    interactiveDisplay = prepareSimpleDisplay(il, tokens)

    pctIL = posinfoList2 = parser.send(['AWE_INFO',
                                       document_label,
                                       'vwp_interactive', 'Token', 'percent'])

    print('Percent Words Suggesting Informal Style: ', pctIL)
    return interactiveDisplay

def academicOptions():

    academicList = parser.send(['AWE_INFO',
                               document_label,
                              'is_academic', 'Token'])
    if academicList is None:
        raise Exception("No academic language information retrieved")

    academics = [entry['value'] for entry in academicList.values()]

    academic_words = parser.send(['AWE_INFO',
                                 document_label,
                                 'is_academic', 'Token', 'uniq'])

    latinateList = parser.send(['AWE_INFO',
                               document_label,
                               'is_latinate', 'Token'])

    if latinateList is None:
        raise Exception("No information on latinate words retrieved")
    latinates = [False]*len(tokens)
    for entry in latinateList.values():
        if entry['value']:
            latinates[entry['tokenIdx']] = True

    countAcad = 0
    for i, token in enumerate(tokens):
        if academics[i] or latinates[i]:
            countAcad += 1
    academic_words, academicPage = \
        prepareAcademicWordInfo(academics, latinates, tokens)

    print('\nPercent Words Suggesting Academic Style: ',
          round(countAcad * 1.0 / len(tokens) * 100))

    print(len(academic_words),
          ' distinct academic words used:',
          academic_words)
    return academicPage

def frequencyOptions():

    tf = parser.send(['AWE_INFO',
                      document_label,
                      'token_freq', 'Token', 'mean'])
    print('Mean token freq:', tf)

    posinfoList2 = parser.send(['AWE_INFO',
                                document_label,
                                'pos_', 'Token'])

    posinfo = [entry['value'] \
        for entry in posinfoList2.values()]

    mfList = parser.send(['AWE_INFO',
                         document_label,
                         'max_freq', 'Token'])

    if mfList is None:
        raise Exception("No information on maximum word frequencies")
    mf = [entry['value'] for entry in mfList.values()]

    freqDisplay, \
        countB1, \
        countB2, \
        countB3, \
        countB4, \
        countB5, \
        countB6, \
        countB7 = \
        prepareFrequencyDisplay(mf,
                                posinfo,
                                tokens,
                                option4,
                                option5,
                                option6,
                                option7,
                                option8,
                                option9,
                                option10)

    percentRare = round(countB7 / len(tokens) * 100)

    percentVeryLowFrequency = \
        round((countB6 + countB7) / len(tokens) * 100)

    percentLowFrequency = round((countB5
                                + countB6
                                + countB7) / len(tokens) * 100)

    percentMediumOrLowFrequency = \
        round((countB4
              + countB6
              + countB7) / len(tokens) * 100)

    percentMediumHighFrequencyOrBelow = \
        round((countB3
               + countB4
               + countB5
               + countB6
               + countB7) / len(tokens) * 100)

    percentHighFrequencyOrBelow = \
        round((countB2
               + countB3
               + countB4
               + countB5
               + countB6
               + countB7) / len(tokens) * 100)

    print('\nWord Frequencies')

    print('Percent high frequency or below:',
          percentHighFrequencyOrBelow)

    print('Percent medium high frequency or below:',
          percentMediumHighFrequencyOrBelow)

    print('Percent medium or low frequency:',
          percentMediumOrLowFrequency)

    print('Percent low frequency:',
          percentLowFrequency)

    print('Percent very low frequency:',
          percentVeryLowFrequency)

    print('Percent extremely rare words:',
          percentRare)
    return freqDisplay

def syllableOptions():

    posinfoList2 = parser.send(['AWE_INFO',
                                document_label,
                                'pos_', 'Token'])

    posinfo = [entry['value'] \
        for entry in posinfoList2.values()]

    sylList = parser.send(['AWE_INFO',
                           document_label,
                           'nSyll', 'Token'])

    if sylList is None:
        raise Exception("No information on maximum word family frequencies")
    syl = [entry['value'] for entry in sylList.values()]

    syllablePage = prepareSyllableDisplay(syl,
                                      posinfo,
                                      tokens,
                                      False,
                                      False,
                                      False,
                                      False)

    syllablePage, \
        countB1, \
        countB2, \
        countB3, \
        countB4 = \
        prepareSyllableDisplay(syl,
                               posinfo,
                               tokens,
                               option4,
                               option5,
                               option6,
                               option7)
    percentFourPlusSyls = \
        round(countB1 * 1.0 / len(tokens) * 100)
    percentThreePlusSyls = \
        round((countB1 + countB2) * 1.0 / len(tokens) * 100)
    percentTwoPlusSyls = \
        round((countB1 + countB2 + countB3) * 1.0 / len(tokens) * 100)

    print('\nNumber of Syllables')
    print(percentFourPlusSyls, ' percent words with four or more syllables')
    print(percentThreePlusSyls, ' percent words with three or more syllables')
    print(percentTwoPlusSyls, ' percent words with two or more syllables')
    return syllablePage

def sentenceTypeOptions():

    sents = parser.send(["AWE_INFO",
                         document_label,
                         "sents",
                         "Doc"])

    sentences = [[sents[idx]['startToken'], sents[idx]['endToken']] for idx in sents]

    posinfoList2 = parser.send(['AWE_INFO',
                                document_label,
                                'pos_', 'Token'])

    posinfo = [entry['value'] \
        for entry in posinfoList2.values()]

    stypeList = parser.send(['AWE_INFO',
                            document_label,
                            'sentence_types', 'Doc'])
    stypes = [entry['value'] for entry in stypeList.values()]

    ccdPage = \
        prepareCompoundComplexDisplay(stypes,
                                      posinfo,
                                      sentences,
                                      tokens,
                                      option4,
                                      option5,
                                      option6,
                                      option7,
                                      option8,
                                      option9,
                                      option10)

    print('\nSentence Variety:')

    stypeCount = parser.send(['AWE_INFO',
                              document_label,
                              'sentence_types', 'Doc', 'counts'])

    for key in stypeCount.keys():
        if key == 'Simple':
            print('Number of simple (kernel) sentences: ',
                  stypeCount[key])

        if key == 'SimpleComplexPred':
            print('Number of simple sentences with complex predicates: ',
                  stypeCount[key])

        if key == 'SimpleCompoundPred':
            print('Number of simple sentences with compound predicates: ',
                  stypeCount[key])

        if key == 'SimpleCompoundComplexPred':
            print('Number of simple sentences with compound/completx sentences: ',
                  stypeCount[key])

        if key == 'Complex':
            print('Number of complex sentences: ',
                  stypeCount[key])

        if key == 'Compound':
            print('Number of compound sentences: ',
                  stypeCount[key])

        if key == 'CompoundComplex':
            print('Number of compound/complex sentences',
                  stypeCount[key])

    return ccdPage

def quoteCiteOptions():
    print('\nQuotations:')

    quotedtextList = parser.send(["AWE_INFO",
                                  document_label,
                                  "vwp_quoted"])
    if quotedtextList is None:
        raise Exception("No quoted text information received")
    quotedtext = [entry['value'] for entry in quotedtextList.values()]

    numQuotes = 0
    quotedLast = False
    for i, val in enumerate(quotedtext):
        if val and not quotedLast:
            numQuotes += 1
            quotedLast = True
        elif not val:
            quotedLast = False

    numQuotedWords = parser.send(['AWE_INFO',
                                  document_label,
                                  'vwp_quoted',
                                  'Token',
                                  'total',
                                  json.dumps([('vwp_quoted',['True'])])])

    print('\n', numQuotes, ' quotation(s)')
    print(numQuotedWords, ' quoted words')

    percentQuotedWords = \
        round(1.0 * numQuotedWords / len(tokens) * 100)

    print(percentQuotedWords,
      ' percent quoted words')

    attributionList = parser.send(["AWE_INFO",
                                   document_label,
                                   "vwp_attribution"])

    if attributionList is None:
        raise Exception("No attribution information received")
    attributions = [entry['value'] for entry in attributionList.values()]

    numAttributionWords = parser.send(['AWE_INFO',
                                   document_label,
                                   'vwp_attribution',
                                   'Token',
                                   'total',
                                   json.dumps([('vwp_attribution',['True'])])])

    attributedLast = False
    numAttributions = 0
    for i, val in enumerate(attributions):
        if val and not attributedLast:
            numAttributions += 1
            attributedLast = True
        elif not val:
            attributedLast = False
    print('\n', numAttributions, ' attributions')
    print(numAttributionWords, ' attribution word(s)')

    sourceList = parser.send(["AWE_INFO",
                              document_label,
                              "vwp_source"])
    if sourceList is None:
        raise Exception("No source information received")
    sources = [entry['value'] for entry in sourceList.values()]
    sourceLast = False
    numSources = 0
    for i, val in enumerate(sources):
        if val and not sourceLast:
            numSources += 1
            sourceLast = True
        elif not val:
            sourceLast = False

    numSourceWords = parser.send(["AWE_INFO",
                                  document_label,
                                  "vwp_source",
                                  "Token",
                                  "total",
                                  json.dumps([('vwp_source',['True'])])])

    print('\n', numSources, ' source(s)')
    print(numSourceWords, ' source word(s)')

    citedtextList = parser.send(["AWE_INFO",
                                 document_label,
                                 "vwp_cite"])

    citedtext = [entry['value'] for entry in citedtextList.values()]

    citedLast = False
    numCites = 0
    for i, val in enumerate(citedtext):
        if val and not citedLast:
            numCites += 1
            citedLast = True
        elif not val:
            citedLast = False

    if citedtext is None:
        raise Exception("No citation information received")

    numCitedWords = parser.send(["AWE_INFO",
                                 document_label,
                                 "vwp_cite",
                                 "Token",
                                 "total",
                                 json.dumps([('vwp_cite',['True'])])])

    print('\n', numCites, ' citation(s)')
    print(numCitedWords, ' cited words(s)')

    quoteCite = prepareQuoteCite(quotedtext,
                                 attributions,
                                 sources,
                                 citedtext)
    return quoteCite

def statements_of_opinionOptions():
    ofList = parser.send(['AWE_INFO',
                          document_label,
                          'vwp_statements_of_opinion',
                          'Doc'])

    of = [[entry['startToken'], entry['endToken']+1] for entry in ofList.values()]

    opinionStatements = prepareRangeMarking(tokens, of)
    return opinionStatements

def statements_of_factOptions():
    sfList = parser.send(['AWE_INFO',
                          document_label,
                          'vwp_statements_of_fact',
                          'Doc'])
    sf = [[entry['startToken'], entry['endToken']+1] for entry in sfList.values()]

    factualStatements = prepareRangeMarking(tokens, sf)
    return factualStatements

def dialogueOptions():
    tok_with_wsList = parser.send(['AWE_INFO',
                                   document_label,
                                   'text_with_ws',
                                   'Token'])

    dsList = parser.send(["AWE_INFO",
                         document_label,
                         "vwp_direct_speech_spans",
                         "Doc"])
    quotedtextList = parser.send(["AWE_INFO",
                                  document_label,
                                  "vwp_quoted"])
    if quotedtextList is None:
        raise Exception("No quoted text information received")
    quotedtext = [entry['value'] for entry in quotedtextList.values()]

    dialogueDisplay = \
        displayDialogue(tok_with_wsList,
                        quotedtextList,
                        dsList)

    print('\nQuotations:')

    numQuotes = 0
    quotedLast = False
    for i, val in enumerate(quotedtext):
        if val and not quotedLast:
            numQuotes += 1
            quotedLast = True
        elif not val:
            quotedLast = False

    numQuotedWords = parser.send(['AWE_INFO',
                                  document_label,
                                  'vwp_quoted',
                                  'Token',
                                  'total',
                                  json.dumps([('vwp_quoted',['True'])])])

    print('\n', numQuotes, ' quotation(s)')
    print(numQuotedWords, ' quoted words')

    percentQuotedWords = \
        round(1.0 * numQuotedWords / len(tokens) * 100)

    print(percentQuotedWords,
      ' percent quoted words')

    return dialogueDisplay

def sceneSettingOptions():
    transitionList = parser.send(['AWE_INFO',
                                  document_label,
                                  'transitions', 'Doc'])

    tlist = []
    for entry in transitionList.values():
        category = entry['value']
        sentStart = entry['startToken']
        startToken = entry['startToken']
        endToken = entry['endToken']
        transition = entry['text']
        tlist.append([transition, sentStart, startToken, endToken, category])
    
    numTransitions = parser.send(['AWE_INFO',
                             document_label,
                             'transitions', 'Doc', 'total'])

    transitionTypeProfile = parser.send(['AWE_INFO',
                                   document_label,
                                   'transitions', 'Doc', 'counts'])
    print('\nType Frequency')
    for item in transitionTypeProfile:
       print(item, transitionTypeProfile[item])

    print('Number of transition words and phrases:', numTransitions)

    transitionProfile = parser.send(["AWE_INFO",
                                    document_label,
                                    "transitions",
                                    "Doc",
                                    "counts",
                                    json.dumps([]),
                                    json.dumps(["text"])])

    if transitionProfile is None:
        raise Exception("No information on transition words retrieved")

    print('\nTransition Words and Phrases:')
    tp = [numTransitions, transitionTypeProfile, transitionProfile, tlist]

    transition_categoriesList = parser.send(['AWE_INFO',
                                 document_label,
                                 'transition_category', 'Token'])

    in_direct_speechList = parser.send(['AWE_INFO',
                                        document_label,
                                        'vwp_in_direct_speech', 'Token'])

    in_past_tense_scopeList = parser.send(['AWE_INFO',
                                           document_label,
                                           'in_past_tense_scope', 'Token'])

    locList = parser.send(['AWE_INFO',
                      document_label,
                     'location', 'Token'])

    sceneSetting, numComments = \
        prepareSceneDisplay(ctext,
                            tok_with_wsList,
                            transition_categoriesList,
                            in_direct_speechList,
                            in_past_tense_scopeList,
                            locList)

    temporalCount = 0
    for item in tp[3]:
        if item[4] == 'temporal':
            temporalCount += 1

    locCount = 0
    for i, val in enumerate(locs):
        if val:
            locCount += 1

    sceneWordPercent = \
        round((temporalCount + locCount) * 1.0 / len(tokens) * 100)

    print(sceneWordPercent,
          ' percent words suggesting scene description')

    print(numComments,
          ' number of shifts into present tense suggesting a comment')
    return sceneSetting

def transitionOptions():

    print('Transition word and phrase information')

    transitionList = parser.send(['AWE_INFO',
                                 document_label,
                                 'transitions', 'Doc'])

    tlist = []
    for entry in transitionList.values():
        category = entry['value']
        sentStart = entry['startToken']
        startToken = entry['startToken']
        endToken = entry['endToken']
        transition = entry['text']
        tlist.append([transition, sentStart, startToken, endToken, category])

    numTransitions = parser.send(['AWE_INFO',
                                 document_label,
                                 'transitions', 'Doc', 'total'])

    transitionTypeProfile = parser.send(['AWE_INFO',
                                       document_label,
                                       'transitions', 'Doc', 'counts'])
    print('\nTransition Category Frequency')
    for item in transitionTypeProfile:
        print(item, transitionTypeProfile[item])

    print('Number of transition words and phrases:', numTransitions)

    transitionProfile = parser.send(["AWE_INFO",
                                    document_label,
                                    "transitions",
                                    "Doc",
                                    "counts",
                                    json.dumps([]),
                                    json.dumps(["text"])])
    print('\nType Frequency')
    for item in transitionProfile:
        print(item.replace('\n','PARA'), transitionProfile[item])

    tp = [numTransitions, transitionTypeProfile, transitionProfile, tlist]

    if tp is None:
        raise Exception("No information on transition words retrieved")
    prepcs = None
    transitionDisplay = prepareTransitionMarking(tokens, tp, prepcs)
    return transitionDisplay

def toneOptions():

    polarityList = parser.send(["AWE_INFO",
                                document_label,
                                "polarity"])
    pl = [entry['text'] for entry \
        in polarityList.values() if entry['value']>0]
    print('polarity words:', pl)

    toneList = parser.send(["AWE_INFO",
                            document_label,
                            "vwp_tone"])

    tone = [entry['value'] for entry in toneList.values()]

    stopwords = parser.send(["AWE_INFO",
                            document_label,
                            "is_stop"])

    posinfoList = parser.send(['AWE_INFO',
                               document_label,
                              'pos_',
                              'Token'])
    posinfo = [entry['value'] \
        for entry in posinfoList.values()]

    filteredtone = []
    for i, value in enumerate(tone):
        if str(i) not in stopwords:
            filteredtone.append(value)
        else:
            if not stopwords[str(i)]['value']:
                filteredtone.append(value)
            else:
                filteredtone.append(0.0)

    tonePage, \
        countStrongPositive, \
        countWeakPositive, \
        countNeutral, \
        countWeakNegative, \
        countStrongNegative = \
        prepareToneDisplay(filteredtone,
                           posinfo,
                           tokens,
                           option4,
                           option5,
                           option6,
                           option7,
                           option8)

    percentStrongPositive = \
        round(1.0 * countStrongPositive / len(tokens) * 100)

    percentWeakPositive = \
        round(1.0 * countWeakPositive/len(tokens) * 100)

    percentNeutral = \
        round(1.0 * countNeutral / len(tokens) * 100)

    percentWeakNegative = \
        round(1.0 * countWeakNegative / len(tokens) * 100)

    percentStrongNegative = \
        round(1.0 * countStrongNegative / len(tokens) * 100)

    print('\nTone:')
    print(percentStrongPositive, ' percent with strong positive connotations')
    print(percentWeakPositive, ' percent with weak positive connotations')
    print(percentNeutral, ' percent with neutral connotations')
    print(percentWeakNegative, ' percent with weak negative connotations')
    print(percentStrongNegative, ' percent with strong negative connotations')

    return tonePage

def socialAwarenessOptions():

    social_awarenessList = parser.send(["AWE_INFO",
                                        document_label,
                                        "vwp_social_awareness",
                                        "Doc"])

    social_awareness = [[entry['startToken'], entry['endToken']]
                       for entry in social_awarenessList.values()]

    tokList = parser.send(['AWE_INFO', document_label, 'text', 'Token'])
    tokens = [entry['value'] for entry in tokList.values()]
    socialAwarenessPage = \
        prepareRangeMarking(tokens, social_awareness)

    numTheoryOfMindSentences = len(social_awareness)

    numTOMWords = 0

    for item in social_awareness:
        numTOMWords = item[1] - item[0]

    percentTheoryOfMindText = \
        round(numTOMWords * 1.0 / len(tokens) * 100)

    print(numTheoryOfMindSentences,
          ' sentences expressing social awareness of'
          + ' other people\'s points of view')

    print(percentTheoryOfMindText,
          ' percent words expressing social awareness'
          + ' of other people\'s points of view')
    return socialAwarenessPage

def concreteDetailOptions():
    tokList = parser.send(['AWE_INFO', document_label, 'text', 'Token'])
    tokens = [entry['value'] for entry in tokList.values()]

    concretedetailsList = parser.send(["AWE_INFO",
                        document_label,
                        "concrete_detail"])
    concretedetails = [entry['tokenIdx'] \
                       for entry \
                       in concretedetailsList.values()
                       if entry['value']]

    concreteDetailPage = \
        prepareConcreteDetailDisplay(tokens, concretedetails)

    percentConcreteDetail = \
        round(1.0 * len(concretedetails) / len(tokens) * 100)

    print(percentConcreteDetail,
          ' percent concrete detail words')

    return concreteDetailPage

def emotionOptions():
    emotions = parser.send(["AWE_INFO",
                            document_label,
                            "vwp_emotion_states",
                            "Doc"])
    em = [False]*len(tokens)
    for entry in emotions.values():
        em[entry['startToken']] = True
    emotionDisplay = prepareEmotionDisplay(em, tokens)
    percentEmotion = \
        round(1.0 * len([item for item in em
                         if item is True]) / len(tokens) * 100)

    print('Percent emotion words: ', percentEmotion)


    return emotionDisplay

def characterOptions():
    [characters,
     otherRefs] = parser.send(['NOMINALREFERENCES',
                               document_label])

    print(characters)

    characterPage = prepareCharacterDisplay(characters, tokens)
    firstPersonRefs = 0
    numCharsMultiRef = 0
    references = []
    for key in characters:
        if key == 'SELF':
            firstPersonRefs += 1
        elif len(characters[key]) > 1:
            numCharsMultiRef += 1
            references.append(key)

    print(numCharsMultiRef,
          ' characters referenced more than once '
          + '(repeated references to the same name or descriptive noun)')

    print('List of references to people or characters:',
          sorted(references))
    return characterPage

def traitOptions():
    traitList = parser.send(["AWE_INFO",
                             document_label,
                            "vwp_character_traits",
                            "Doc"])
    traits = [False]*len(tokens)
    for entry in traitList.values():
        traits[entry['startToken']] = True
    traitDisplay = prepareEmotionDisplay(traits, tokens)
    return traitDisplay

def subjectivityOptions(option2, option3):
    ps = parser.send(['PERSPECTIVESPANS', document_label])
    if ps is None:
        raise Exception("No information on perspective spans retrieved")

    sm = parser.send(['STANCEMARKERS', document_label])

    if sm is None:
        raise Exception("No information on stance markers retrieved")

    subjectivities, \
        perspectives, \
        stancemarkers = \
        prepareSubjectivityDisplay(tokens,
                                   ps, sm, option2, option3)

    percentAllocentric = \
        round(len([item for item in perspectives
                   if item == 'OTHER']) * 1.0 / len(tokens) * 100)

    print(percentAllocentric,
          ' percent of words in sentences expressing'
          + ' a third party\'s point of view')

    percentEgocentric = \
        round(len([item for item in perspectives
                   if item == 'SELF']) * 1.0 / len(tokens) * 100)
    print(percentEgocentric,
          ' percent of words in sentences expressing'
          + 'the writer\'s point of view')

    return subjectivities

def argumentWordOptions():
    print('\nArgument Language:')


    lemmaList = parser.send(['AWE_INFO',
                             document_label,
                             'lemma_', 'Token'])
    lemmas = [entry['text'] for entry in lemmaList.values()]
    argew = parser.send(["AWE_INFO",
                         document_label,
                         "vwp_explicit_argument"])

    if argew is None:
        raise Exception("No information on explicit argument words retrieved")
    eaw = [entry['tokenIdx'] for entry in argew.values() if entry['value']]

    print('explicit argument words', [entry['text'] for entry in argew.values() if entry['value']])

    argw = parser.send(["AWE_INFO",
                        document_label,
                        "vwp_argumentword"])

    print('argument words', [entry['text'] for entry in argw.values() if entry['value']])

    awList = parser.send(["AWE_INFO",
                          document_label,
                          "vwp_argumentation"])
    if awList is None:
        raise Exception("No information on argument words retrieved")
    aw = [entry['tokenIdx'] for entry in awList.values() if entry['value']]

    percentArgumentLanguage = \
        parser.send(["AWE_INFO",
                     document_label,
                     "vwp_argumentation",
                     "Token",
                     "percent",
                     json.dumps([('vwp_argumentation',['True'])])])

    print(percentArgumentLanguage, ' percent argument language in text')

    csList = parser.send(["AWE_INFO",
                           document_label,
                           "supporting_ideas",
                           "Doc"])

    if csList is None:
        raise Exception("No information on supporting detail segments retrieved")
    cs = [[entry['startToken'], entry['endToken']+1] for entry in csList.values()]

    pl = parser.send(['PROMPTLANGUAGE', document_label])
    if pl is None:
        raise Exception("No information on main idea words retrieved")

    pr = parser.send(['PROMPTRELATED', document_label])
    if pr is None:
       raise Exception("No information on related main idea words retrieved")

    coreList = parser.send(["AWE_INFO",
                            document_label,
                            "main_ideas",
                            "Doc"])
    if coreList is None:
        raise Exception("No information on main ideas retrieved")
    core = [[entry['startToken'], entry['endToken']+1] for entry in coreList.values()]

    cw = []
    essaystructure, argumentwords = \
        prepareArgumentWordMarking(tokens,
                                   lemmas,
                                   aw, eaw, pl, pr, cw, core)
    return argumentwords

def mainIdeaOptions():
    coreList = parser.send(["AWE_INFO",
                            document_label,
                            "main_ideas",
                            "Doc"])
    if coreList is None:
        raise Exception("No information on main ideas retrieved")
    core = [[entry['startToken'], entry['endToken']+1] for entry in coreList.values()]

    sents = parser.send(["AWE_INFO",
                         document_label,
                         "sents",
                         "Doc"])

    percentCore = round(len(core) * 1.0 / len(sents) * 100)
    print(percentCore,
          ' percent of sentences seem to express the thesis'
          + ' and main points of an essay')

    essaystructure = prepareSupportingIdeas(core)
    return essaystructure

def supportingIdeaOptions():
    csList = parser.send(["AWE_INFO",
                          document_label,
                          "supporting_ideas",
                          "Doc"])

    if csList is None:
        raise Exception("No information on supporting detail segments retrieved")
    cs = [[entry['startToken'], entry['endToken']+1] for entry in csList.values()]

    sents = parser.send(["AWE_INFO",
                         document_label,
                         "sents",
                         "Doc"])

    percentSupporting = \
        round(len(cs) * 1.0 / len(sents) * 100)

    print(percentSupporting,
          ' percent of sentences seem to express supporting points')

    percentDetail = round(len(cs) * 1.0 / len(sents) * 100)

    supportingideas = prepareSupportingIdeas(cs)
    return supportingideas

def prepareDetailOptions():
    csList = parser.send(["AWE_INFO",
                          document_label,
                          "supporting_details",
                          "Doc"])
    if csList is None:
        raise Exception("No information on supporting detail segments retrieved")
    cs = [[entry['startToken'], entry['endToken']+1] for entry in csList.values()]

    sents = parser.send(["AWE_INFO",
                         document_label,
                         "sents",
                         "Doc"])

    percentDetail = round(len(cs) * 1.0 / len(sents) * 100)

    print(percentDetail,
          ' percent of sentences seem to provide details'
          + ' elaborating on the main points')

    details = prepareSupportingIdeas(cs)
    return details

def propositionalAttitudeOptions():
    pa = parser.send(["AWE_INFO",
                      document_label,
                      "vwp_propositional_attitudes",
                      "Doc"])

    if pa is None:
        raise Exception("No information on propositional"
                        + " attitudes retrieved")

    pa_display = displaySingleList(tokList, pa)
    return pa_display

if option2 == 'Conventions':
    proofread = proofreadOptions()
    st.write(proofread, unsafe_allow_html=True)
elif option2 == 'Parts of Speech':
    POSDisplay = POSOptions()
    st.write(POSDisplay, unsafe_allow_html=True)
elif option2 == 'Informal Language':
    interactiveDisplay = informalOptions()
    st.write(interactiveDisplay, unsafe_allow_html=True)
elif option2 == 'Academic Language':
    academicPage = academicOptions()
    st.write(academicPage, unsafe_allow_html=True)
elif option2 == 'Word Frequency':
    freqDisplay = frequencyOptions()
    st.write(freqDisplay, unsafe_allow_html=True)
elif option2 == 'Number of Syllables':
    syllablePage = syllableOptions()
    st.write(syllablePage, unsafe_allow_html=True)
elif option2 == 'Sentence Variety':
    ccdPage = sentenceTypeOptions()
    st.write(ccdPage, unsafe_allow_html=True)
elif option2 == 'Main Ideas':
    essaystructure = mainIdeaOptions()
    st.write(essaystructure, unsafe_allow_html=True)
elif option2 == 'Supporting Ideas':
    supportingideas = supportingIdeaOptions()
    st.write(supportingideas, unsafe_allow_html=True)
elif option2 == 'Details':
    details = prepareDetailOptions()
    st.write(details, unsafe_allow_html=True)
elif option2 == 'Statements of Opinion':
    opinionStatements = statements_of_opinionOptions()
    st.write(opinionStatements, unsafe_allow_html=True)
elif option2 == 'Statements of Fact':
    factualStatements = statements_of_factOptions()
    st.write(factualStatements, unsafe_allow_html=True)
elif option2 == 'Transitions':
    transitionDisplay = transitionOptions()
    st.write(transitionDisplay, unsafe_allow_html=True)
elif option2 == 'Quotations, Citations, Attributions':
    quoteCite = quoteCiteOptions()
    st.write(quoteCite, unsafe_allow_html=True)
elif option2 == 'Argument Words':
    argumentWords =  argumentWordOptions()
    st.write(argumentWords, unsafe_allow_html=True)
elif option2 == 'Propositional Attitudes':
    pa_display = propositionalAttitudeOptions()
    st.write(pa_display, unsafe_allow_html=True)
elif option2 == 'Own vs. Other Perspectives':
    subjectivities = subjectivityOptions(option2, option3)
    st.write(subjectivities, unsafe_allow_html=True)
elif option2 == 'Characters':
    characterPage = characterOptions()
    st.write(characterPage, unsafe_allow_html=True)
elif option2 == 'Emotion Words':
    emotionDisplay = emotionOptions()
    st.write(emotionDisplay, unsafe_allow_html=True)
elif option2 == 'Character Traits':
    traitDisplay = traitOptions()
    st.write(traitDisplay, unsafe_allow_html=True)
elif option2 == 'Dialogue':
    dialogueDisplay = dialogueOptions()
    st.write(dialogueDisplay, unsafe_allow_html=True)
elif option2 == 'Scene and Setting':
    sceneSetting = sceneSettingOptions()
    st.write(sceneSetting, unsafe_allow_html=True)
elif option2 == 'Social Awareness':
    socialAwarenessPage = socialAwarenessOptions()
    st.write(socialAwarenessPage, unsafe_allow_html=True)
elif option2 == 'Concrete Details':
    concreteDetailPage = concreteDetailOptions()
    st.write(concreteDetailPage, unsafe_allow_html=True)
elif option2 == 'Tone':
    tonePage = toneOptions()
    st.write(tonePage, unsafe_allow_html=True)
