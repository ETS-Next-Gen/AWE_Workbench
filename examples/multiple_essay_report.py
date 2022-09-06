import streamlit as st
import re
import asyncio
import html

from annotated_text import annotated_text
from awe_workbench.web.websocketClient import websocketClient
from pylt_classifier.languagetoolClient import languagetoolClient


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
        if key=='explicit_1' or key=='explicit_2':
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


def prepareSocialAwarenessDisplay(tokens, social_awareness):
    loc = 0
    output = ''
    for item in social_awareness:
        start = item[0]
        if '\n' in tokens[start]:
            start += 1
        end = item[1]
        output += ' '.join(tokens[loc:start])
        output += ' <span style="background-color: yellow"> '
        output += ' '.join(tokens[start:end])
        output += ' </span> '
        loc = end
    output += ' '.join(tokens[loc:len(tokens)])
    return normalize(output.replace('  ', ' '))


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


def prepareSceneDisplay(tokens, transitions, in_direct_speech, tense_changes,locations):
    loc = 0
    temp = []
    numComments = 0
    present = False
    startHighlight = 0
    numPastTokens = 0
    lastchange = None
    for change in tense_changes:
        if lastchange is not None \
           and (not change['past']
                or in_direct_speech[change['loc']]
                or tokens[lastchange['loc']] 
                in ['"', '"', "'", '“', '”', "''", '``']):
            numPastTokens += change['loc'] - lastchange['loc']
        present = False
        newloc = change['loc']
        if not change['past'] and not in_direct_speech[newloc]:
            startHighlight = newloc
            if not present:
                newloc = change['loc']
                temp += tokens[loc:newloc]
                temp.append('<strong style="background-color: #c39bd3">')
                present = True
                numComments += 1
                loc = newloc
            else:
                newloc = change['loc']
                temp += tokens[loc:newloc]
                present = True
                loc = newloc
        else:
            newloc = change['loc']
            temp += tokens[loc:newloc]
            if newloc>0:
                temp.append('</strong>'+tokens[newloc])
            else:
                temp.append(tokens[newloc])
            present = False         
            loc = newloc+1
        lastchange = change
    temp += tokens[loc:len(tokens)-1]
    if present:
        temp.append('</strong>' + tokens[len(tokens)-1])
    else:
        temp.append(tokens[len(tokens)-1])

    print('num past tokens: ', numPastTokens)
    if numPastTokens * 1.0 / len(tokens) < .6 or numComments <= 1:
        temp = tokens
       
    loc = 0
    temp2 = []
    inLoc = False
    lastLoc = 0
    for i, locFlag in enumerate(locations):    
        lastLoc = i
        if not inLoc and locFlag:
            temp2.append('<span style="background-color: yellow">'+temp[i])
            inLoc = True
        elif inLoc and not locFlag:
            temp2.append('</span>' + temp[i])
            inLoc = False
        else:
            temp2.append(temp[i])
    while lastLoc < len(temp):
        temp2.append(temp[lastLoc])
        lastLoc+=1
    temp = temp2

    loc = 0
    output = ''
    for transition in transitions:
        breakloc = transition[1]
        start = transition[2]
        end = transition[3]
        if transition[4] != 'temporal' or in_direct_speech[start]: 
            output += ' '.join(temp[loc:end]) + ' '
            loc = end
        else:
            output += ' '.join(temp[loc:breakloc])
            #output += '<hr>'
            output += ' '.join(temp[breakloc:start])
            output += ' <span style="background-color: #90ee90"> '
            output += ' '.join(temp[start:end+1])
            output += ' </span> '
            loc = end+1
    output += ' '.join(temp[loc:len(temp)])
    headstr = '<ul><li><span style="background-color: #90ee90">Times</span></li><li><span style="background-color: yellow">Places</span>'
    if numPastTokens * 1.0 / len(tokens) >= .6 and numComments > 1:
        headstr += '<li><span style="background-color: #c39bd3">Comments</span></li>'
    headstr += '</ul><hr>'
    outhtml = '<!DOCTYPE html><html><head></head><body>'
    outhtml += headstr
    outhtml += normalize(output.replace('  ',' ').replace('\n','<br />'))
    outhtml += '</body></html>'
    return outhtml, numComments


def displayDialogue(tokens, quoted, directspeech):
    tokens2 = []
    first = 0
    for (speakers, addressees, locs) in directspeech:
        for loc in locs:
            last = loc[0]
            tokens2.append(' '.join(tokens[first:last]))

            first = loc[0]
            x = first

            last = loc[1]+1
            y = last
            if first < len(tokens) \
               and re.match('\s+', tokens[first]):
                first += 1
            while (first < len(tokens)
                   and not quoted[first]
                   and not re.match('\s+', tokens[first])
                   and tokens[first] != '"'
                   and tokens[first] != "'"
                   and tokens[first] != "''"
                   and tokens[first] != '``'
                   and tokens[first] != '”'
                   and tokens[first] != '“'
                   and first <= last):
                first += 1

            while (not quoted[last - 1]
                   and tokens[last - 1] != '"'
                   and tokens[last - 1] != "'"
                   and tokens[last - 1] != "''"
                   and tokens[last - 1] != '``'
                   and tokens[last - 1] != '”'
                   and tokens[last - 1] != '“'
                   and last > 0
                   and first < last):
                last -= 1
            if x != first:
                while re.match('\s+', tokens[x]):
                    tokens2.append(' ' + tokens[x])
                    x += 1
                tokens2.append(' <span style="background-color: #90ee90">'
                               + ' '.join(tokens[x:first])
                               + '</span> ')
            while (first < len(tokens)
                   and re.match('\s+', tokens[first])):
                tokens2.append(' ' + tokens[first])
                first += 1
            tokens2.append(' <span style="background-color: #87cefa">'
                           + ' '.join(tokens[first:last])
                           + '</span> ')
            tokens2.append(' <span style="background-color: #90ee90">'
                           + ' '.join(tokens[last:y])
                           + '</span> ')
            last = first
            first = loc[1] + 1
    tokens2.append(' '.join(tokens[first:len(tokens) - 1]))
    tokens2 = normalize(''.join(tokens2)).replace('\n','<br />')
    return tokens2


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
        if ccd[i] == 1:
            if opt1:
                outhtml += '<span style="font-style: bold;' \
                           + ' background-color: #AFEEEE">' \
                           + normalize(' '.join(tokens[sent[0]:sent[1]])) \
                           + '</span> '
            else:
                outhtml += normalize(' '.join(tokens[sent[0]:sent[1]])) + ' '
        elif ccd[i] == 2:
            if opt2:
                outhtml += '<span style="font-style: bold;' \
                         + ' background-color: #AFEEEE">' \
                         + normalize(' '.join(tokens[sent[0]:sent[1]]))	 \
                         + '</span> '
            else:
                outhtml += normalize(' '.join(tokens[sent[0]:sent[1]])) + ' '
        elif ccd[i] == 3:
            if opt3:
                outhtml += '<span style="font-style: bold;' \
                           + ' background-color: #AFEEEE">' \
                           + normalize(' '.join(tokens[sent[0]:sent[1]])) \
                           + '</span> '
            else:
                outhtml += normalize(' '.join(tokens[sent[0]:sent[1]])) + ' '
        elif ccd[i] == 4:
            if opt4:
                outhtml += '<span style="font-style: bold;' \
                           + ' background-color: #AFEEEE">' \
                           + normalize(' '.join(tokens[sent[0]:sent[1]])) \
                           + '</span> '
            else:
                outhtml += normalize(' '.join(tokens[sent[0]:sent[1]])) + ' '
        elif ccd[i] == 5:
            if opt5:
                outhtml += '<span style="font-style: bold;' \
                           + ' background-color: #AFEEEE">' \
                           + normalize(' '.join(tokens[sent[0]:sent[1]])) \
                           + '</span> '
            else:
                outhtml += normalize(' '.join(tokens[sent[0]:sent[1]]))

        elif ccd[i] == 6:
            if opt6:
                outhtml += '<span style="font-style: bold;' \
                           + ' background-color: #AFEEEE">' \
                           + normalize(' '.join(tokens[sent[0]:sent[1]])) \
                           + '</span> '
            else:
                outhtml += normalize(' '.join(tokens[sent[0]:sent[1]])) + ' '
        elif ccd[i] == 7:
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
           or '\'' in tokens[i] \
           or syl[i] is None:
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

    stancemarkers = tokens.copy()
    for i, token in enumerate(tokens):
        stancemarkers[i] = False

    for domain in ps['implicit']:
        if domain in sm['implicit']:
            perspectives[int(domain)] = 'WRITER'
            if domain in sm['implicit']:
                for loc in sm['implicit'][domain]:
                    stancemarkers[loc] = True
            for loc in ps['implicit'][domain]:
                perspectives[loc] = 'WRITER'
        else:
            for loc in ps['implicit'][domain]:
                perspectives[loc] = 'OTHER'
    for sub in ps['explicit_1']:
        perspectives[sub] = 'WRITER'
    for sub in sm['explicit_1']:
        stancemarkers[sub] = True
        perspectives[sub] = 'WRITER'
    for sub in ps['explicit_2']:
        perspectives[sub] = 'AUDIENCE'
    for sub in sm['explicit_2']:
        stancemarkers[sub] = True
        perspectives[sub] = 'AUDIENCE'
    for domain in ps['explicit_3']:
        perspectives[int(domain)] = 'THIRDPERSON'
        for item in ps['explicit_3'][domain]:
            perspectives[item] = 'THIRDPERSON'
        if domain in sm['explicit_3']:
            for loc in sm['explicit_3'][domain]:
                stancemarkers[loc] = True
                perspectives[loc] = 'THIRDPERSON'

    output = []
    for i, token in enumerate(tokens):
        if option2 == 'Details' \
           and perspectives[i] == 'OTHER':

            output.append('<span style="font-style: bold;'
                          + ' background-color: #AFEEEE"> '
                          + tokens[i] + ' </span>')

        elif '\n' in tokens[i]:
            output.append(tokens[i])
        elif (perspectives[i] == 'WRITER'
              and not stancemarkers[i]
              and option3 == 'Author\'s Perspective'):

            output.append('<span style="font-style: italic;'
                          + ' background-color: #ffffa1"> '
                          + tokens[i] + ' </span>')

        elif (perspectives[i] == 'WRITER'
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


prompt = ""

directions = ""

st.write('<b>' + prompt + '</b>', unsafe_allow_html=True)
st.write('<i>' + directions + '</i>', unsafe_allow_html=True)

option = st.selectbox('',
                      ('Essay 1',
                       'Essay 2',
                       'Essay 3',
                       'Essay 4',
                       'Essay 5',
                       'Essay 6',
                       'Essay 7',
                       'Essay 8',
                       'Essay 9',
                       'Essay 10',
                       'Essay 11',
                       'Essay 12',
                       'Essay 13',
                       'Essay 14',
                       'Essay 15',
                       'Aesop',
                       'Personal Narrative'))

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
                        'Argument Words',
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


document_labels = ['Essay 1',
                   'Essay 2',
                   'Essay 3',
                   'Essay 4',
                   'Essay 5',
                   'Essay 6',
                   'Essay 7',
                   'Essay 8',
                   'Essay 9',
                   'Essay 10',
                   'Essay 11',
                   'Essay 12',
                   'Essay 13',
                   'Essay 14',
                   'Essay15',
                   'Aesop',
                   'Personal Narrative']

documents = ["I do not believe that censorship should be an option for people that find a book, magazine, or movie offensive. I believe that if a person decides to take a book off the shelf because he/she is offended, they are obviously paranoid. If a few cuss words are found in a book and a person doesn't want their children to read that book, then don't allow them to get it. Don't make all of the other people suffer. Censorship is an unnecessary solution to something that isn't even a problem. You know what they say, 'If it ain't broken, don't fix it.'\n      First of all, people have a variety of opinions. Some people think that violence is ok and some people don't think it's ok. If one person decides to put a book off the shelf because they find it offensive, what will the next person think? They may find violence perfectly acceptable and they might allow their kids to read the book. Then it would create a big conflict.\n     Lastly, parents need to allow their kids to grow up and mature. They also need their kids to know the difference between right and wrong. If they don't read books or movies with violence or cuss words when they're young, what will they do when they discover it when they're older? As a child, it is a time to learn life lessons and begin to form clear distinctions between right and wrong. Shielding your children from it will only hinder their progress in figuring things out and learning to think for themselves as adults (Paterson, 2009).\n     Censorship is the same thing that Hitler did to prevent people to think for themselves and discover that his tactics were a great evil to society. In other words, censorship is part of fascism and should not even be considered in American society. The citizens of the U.S. have the responsibility of exposing the truth and teaching our children the differences between right and wrong. It's one of the ideals that help make this country great", "Censorship. Sometimes it's needed, sometimes it's not. Children of today are exposed to many adult things, whether it is watching tv or a movie, or just witnessing things at home. I believe censorship is neccesary for young children, they shouldn't be exposed to bad launguage, or graphic scenes, or something that is strictly for adults. They will experience these things one day, and they need to be mature enough to understand them.\n Teenagers on the other hand is a whole different story. They want to hear the bad language and see graphic, gory scenes. It's all about action to the boys, drama for the girls, and everyone wants to hear those juicy details. Censorship won't stop them from moving on to the next movie or book on the shelf that has all these things in them. Even though all teens act like it's not important and that their old enough to see all this, somethimes their probably not. If you think that telling your teenage daughter or son that their not allowed to watch a movie or read a book because of something it says, they'll probably just go log onto the internet and see it anyway. Nothing is censored on the internet, so if your all about censorship, don't go onto to the internet.Adults do not need censorship. There adults, they can make their own decisions and they know what they want to watch or read.\nRemoving things from the shelves of libraries is sometimes needed. There should be sections, children, teens, and adults. There are ratings on movies, and books are written for a certain age limit so everything should be placed accordingly. Censorship is needed, but your parents or guardian are the ones who will most likely tell you whether or not your going to be able to read a book or a watch a movie.\n Some people find things more offensive than others. So censorship is really in the eye of the beholder. Personally I believe in censorship, but to others, its a waste of time. I wouldn't want my child watching a movie where someone gets brudally murdered and where there cussing every other word. Music can come uncensored and censored, it just depends what you want to hear. Censorship is either loved or hated, its all one big opinion.", " Each book in a library bears its own relation to each person that enters that library.  Whether the books relate well or poorly to each person is not something for a mass of people to decide.  Every person has a different outlook on what makes a story interesting.  There will not ever be a book that every human being agrees to be both appropriate and vivacious.  Designed with distinctly different minds, people want to read distinctly different books, written by distinctly different authors.  People should maintain a right to choose which books he or she may want to read.\n     Never, will one book bind the world.  Minds of human beings are too complexly separated.  For example; reading 'Moby Dick' by Melville in my English class last year was more than appropriate, though rather boring for the majority of the class.  Books of racism, religion, and sexual content intrigue a person's mind, or otherwise disgust one's.  Finding satisfactory books for everyone in a community to agree simply will not ever be done.  There will always be that one person who declines to agree.\n     It is a choice.  It is a choice for each person to read what he or she wants to read.  If you force something upon a society of readers, then what will they have left for their own minds' freedom?  Face it, forcing an atheist to read an emotionally comprehensive novel of the Christian faith will not be stood for by the reader.  Cursing, to some people, brings a book to a realistic point.  To others, however, it draws them further and further away from the story.  A choice should remain a person's right; especially to read a book written to be read.\n     Finding an appropriate book is not the problem.  That has yet to become the problem.  The only problem is finding appropriate books that are both compelling and enthralling.  I find 'The Catcher in the Rye' to be dangerously inappropriate.  However, it captivates my mind beyond other dimensions.  Others that I know choose not to read it because of the offensive content.  Do I find it offensive to some? No, but I understand where others could find it offensive.  There is no way to approve a book to not be offensive, because it is not offensive to every person who reads it.  To reiterate, the mind of human is a unique one, that identifies with no other.\n     To sum up the full idea of this position; every person should be given the choice to read what he or she desires.  Give each person the choice, and the rebellion will settle down.  Removing a book from a shelf just puts the craving in the hearts of certain people to read it; sometimes completely rebelliously.  Katherine Paterson is extremely correct by saying that taking a book from a shelf everytime someone wants one banned will not leave books for anyone.  As a person, I am well associated with my mind, and it desires the freedom of choice.  Every human mind desires the freedom to choose.  Give people the choice. Remove no books from a shelf, and let the outcome draw in whoever is interested in whatever they may be interested in.  Let readers have their freedom.", "In society today, people take things in very many different ways. So things that might help one person, may offend other.\n      In libraries, there are different kinds of books; fiction, non fiction..(etc). So if you dont like a particular book, maybe you should try looking in a different area. I do not think books should be removed from the shelf because the book has offened a few people.\n      We are blessed to live in America, where we have freedom of speech. So authors have freedom to write what they would like to. They work long hard hours getting a book ready to be published and then someone wants to take it off the shelf becasue it offened a few people? I do not think that is right.\n     'One man's junk is another man's treasure.' I think this quote goes along with this topic very well, because the book may not mean something to one person but it may mean the word to someone else.\n      You never know what people may need to hear. Maybe an alcoholic is at a point in his/her life and is ready to change, and someone has a book about a recovering alcoholic. Now, this kind of book may offend a few people, but it may save a family, a friendship or maybe even a life.\n      Take Alice Walker for intance, her journal is now a book. Now this may offend a few people that might have been thereor maybe don't like The Color Purple, but her story has the right to be told. Yes, there is violence in it, and i understand that maybe you don't want your 8 year old to hear about how they use to treat African-American women, but the story has the right to be told, and should be told.\n      I do not think that the librarian has the right to take a book off the shelf at the library, just because it has offened a few. There are lots of different kinds of books, if the books you are reading offend you, look for a different type of book", "I think alot of books are good to read cause some of them will tell you more wat u didnt know so thierfore u might pick up a book that u like and read it andyou may like it but doesnt have more meaning to  what your reading alot of books you read have some type of character in it that might talk about another thing thats opposite then what the other charcter is talking about magazines show you sometimes wat the persons life style is like some books that people read has no action or felling in it so \nthey can just pick up and read the book its always good to pick up a reasonable  book so someone can read books thats positive and would mean something to other people to read the same book you read i think the best book is one that tells you about life and what you need to know to suceed life you may run in to a book that is true and get into it so you can learn sometimes about what you read and write about it on a essay paper a magazine and movie book shows alot of action and wat its like what they do most people migh think its boring to read a unaction book so they get a book that they have action to so it might exsite them more than a regular book but most books have more pictures than words in it you should take a book off the shelf that has wat  you need to know about cause action books might not help you all the time the more action fun books you read are not as good as wat another book is taking place at in a store", "In our society today there is always going to be something that someone disagrees with or dislikes.  Items should not be removed from the shelves just because someone takes offense to it.  Everyone has a book or movie out there that they disagree with, but if it is removed just for that reason then there would be a very limited selection left.  Students would take advantage of this and they would have educational books removed.\n     Removing items from shelves removes history.  Our history books tell us stories of slavery and descrimination.  If someone takes offense to this and has it removed then we are losing a part of our history that needs to be heard and taught so that it does not occur again.  Items in the library are items that you can choose to check out or choose to not check out.  If you take offense to an item in the library then you do not have to read it.  Something that you may take as offensive may be something that inspires and encourages someone else.  Wether you like an item or dislike it is a matter of your own personal opinion and decisions should not be made based on someones opinion alone.\n    Think about it.  If you have a favorite book, movie, or song then would you want it to be gotten rid of based on someones opinion?  You have the right to be able to read,watch, or listen to whatever you want.  It should not be limited based on someone elses opinion.  It would cause much argument among people.  Some have different opinions then others on a certain item in the library which will lead to argument and possible violence.\n     There are so many wonderful and inspiring books and movies out there and there is always going to be someone who does not like at least one of them.  If items are removed based on someones opinion then there will be a very limited selection left.  People read for enjoyment and knowledge.  They deserve to have a wide selction to choose from.\n     In our society today there is always going to be something that someone disagrees with or dislikes.  Our opinions should not be based on a person's dislike of something.  If they take offense to it then they have the right to ignore it.  There are so many books and movies out there that teach us of life before our generation.  We need these books and movies so that there are not repeat events of all of the rough times our ancestors had to go through.  We need these books for future generations so that we are able to teach and guide them.  Items should not be removed from the shelves ba,sed on the fact that someone takes offense to it.", "Practice What You Preach\n     The U.S. is considered one of the greatest countries in the world because it is a free country. In the 1800's people migrated here to escape the control that their government had in their homeland. In America we practice freedom of speech. If we censor materials like books, music, movies, etc. it would defeat the entire purpose of America and it's Constitution.\n     Everyone has their own personality with likes and dislikes. Not everyone likes the same music or is interested in reading the same subject, thats why its wonderful that their is a variety of everything. If you start banning or censoring certain things then how will people learn? There is nothing wrong with learning about negative things because that teaches people lessons so they know What or What not to do if in that situation. When you censor 'bad things' it creates naive thinkers, which only leads to discrimination.\n      I agree that for children there should warnings for material that parents may find offensive. For example, movies have ratings for different age groups, and books could do the same. Of course its up to the parents if they want to follow the recommendations but banning something all together is not neccessary.\n     I personally learned a lot of things from Shows I've seen on television. Whats on television may be considered 'street smart' education but that is good. Today we live in a scary and violent society, so being 'street smart' is an advantage. If television was censored then people would not know what to do in a bad situation because they have never experienced or seen of it before.\n     If books, movies, magazines, music, etc. are removed from shelves then America is not practicing What it preaches to the many of people who come here in search of freedom.", "Censorhship should play a major part in which books should enter and leave the library. Thats why I think that if a book, movie, magazine, or cd should deffinitly should be removed from the shelf if it is found offensive to atleast ten children. Now it would be asking too much to have the libraian read through all the books to make sure there is no bad language or anything else that a parent might not want their child to read about. So therefore a library should have a certain section that if a libraian thinks that there might be some bad language or refrence to drugs or alcohol then that book should go into that part of the library. I have found some books that have some pretty graphic material in them that I dont think a little kid should be reading but there was nothing I could do about it except take it up to the libraian.\n      Movies would be a major thing that they would have to watch out for. Just because the movie has a title that dont seem that bad dont mean that there wont be any grapic images in that movie, or that there wont be any inappropriate language used at one point in the movie. Now since movies are alot easier to review and since they also have a rating then that should make it easier to tell if that movie should go on the shelves of a library or not. But there should deffinitly be a part in the library that if they did want to allow certain movies in there that would be inappropriate for little children then those movies should be put in that part of the library that has a door on it so the kids would know not to go in that room.\n      Music would be another thing you would deffinitly have to watch out for because with each song could change how the languge is in that cd. So I think that the librarian should have to sit down and persoanlly listen to that cd before they decide to put it out on the shelves for others to be able to listen to. But personally i think that there should be no music allowed in libraries just because with every new cd album that an artist makes he could easily change how his wording is in the songs. So you just never know what the artist of the song is going to do with his music. One album can be perfectly fine and not have one cuss word on it, but then the next album that he or she makes could just be loaded with cuss words.\n      Another possible way to prevent little kids from hearing or reading about inappropriate stuff is to have some of the books, magazines, cd's, or movies catagorized by age. As a child gets older he will be tought more about certain things. Then once he picks up that book and sees that its mentioned in the book it wont be that big of a shock to him or his parents. With the way things are today its almost impossible for a kid to pick something up and not read about drugs or violence. So if you were to go through and take everything off the shelf that mentioned drugs or violence then there would be nothing left on the shelfs for kids to listen to or read.\n      Your not going to be able to catch every single movie, book, magazine, or cd that has something to do with violence or alcohol use. But you can take some of the stuff that has alot of that kind of stuff in it off the shelf. By just taking some of the materials off the shelf that contain stuff that may seem inappropriate for children will deffinitly make a big difference and it could possibly protect your child from reading across it someday when he or she reads a book and sees that or listens to a cd and hears the artist metion something about that.\n      Game designers are now starting to make all their games around violene. So if you were to take all the games that have violence in them and take them off the shelf there would be no games left for kids to play. So there are just some things that contain violence that you just cant keep your child from seeing at one point in time. All the games have a rating on them so you should have an adult check that game rating before you let your child get that game. By doing that you will be able to somewhat controll what your child will see and it will also make it better because then you are not taking games that other kids might like off the shelf and making them no longer available.\n      So I have pretty much covered about how who ever is in charge of the games, books, movies and cds should look them over and possibly listen or look at them just to see what they are like before they put them out on the shelf. You dont have to censor everything but there are deffinitly some things out there that should not be put out on the shelfs for little kids to look at or listen to. And if a little kid wants to get a game a parent should have to look at the game and the rating of the game to determine if that child is mature enough to handle what goes on in that game. But overall I personally dont think that they should just go through and ban everything from going on the shelfs it should be up to the child to determine if they can handle what that movie or book contains", "Do I believe that some books should be taking off the shelves if they are found offensive ?\n     Well what do you think ? I think they should depending on cause or what degeree of the party being offended. I feel if there are books ,movies,or music that are saying or showing a form of insluts then it depends on who is being offended.\n      If you have a racist book against all races like blacks,asian,or mexican etc... other minorities may find out about those forms of insults and they raise an issue about it, then yes take it off the shelves.\n      If you have a confrontation about it then it could get violent . Also, if you dont then they could sue you for racism or make it public to everyone that you are a racist library and you would loose business.\n      So to avoid all of the fighting and  lawsuits and other humiliation against you and the other minorites. If they bring up a situation then just take it off the shelves so you can stay safe and them as well.\n           Plus , they only come here for an oppurtunity to start a new life cause usually they're coming from poverty srticken towns, homes countries. I myself, am not a racist person I think that we are equal just unique individuals we're all unique in our own ways  that is what makes us who we are today.", "Many people have many different thoughts and beliefs. Some people may believe that a movie or song needs to be removed, but others may disagree, and nobody wants the things they enjoy to be taken away.\n     If there was a book on a shelf in a bookstore that you didn't agree with and thought should be removed, and you removed it, then you are taking away from someone who may enjoy that book. If everyone removed things from life that they didn't enjoy, then there would be very little to enjoy.\n    For example, I personally love horror movies. I love the thrill you get from a horror movie and how they can make you jump even though it's just a movie screen. I'm sure there are people in this world who think horror movies are wrong. If those people were allowed to just remove them forever, I, and many other people, would be sadly dissapointed. I also love video games. Video games are a huge part of my life, and I know for a fact that there are people who highly disagree with some of the content of them. If people could take video games away because they didn't agree with them, i would be crushed.\n     I am also aware that people may just be worried about their children watching movies, listening to songs, or reading books that are not appropriate for them. I understand that the parents want their children to be supervised, but removing the books, movies and songs is not exactly the answer. Movies and books can easily be censored. Many movies and songs have language filters and some movie programs now have parental options that allow the parents to decide what movies they want to allow their children to watch. Parents can also supervise their children when they download music onto an ipod or phone, and depending on where they are bought, books and magazine's may require parental consent. Video games also require parental consent depending on the rating of the game.\n      We can't just go around removing everything we dont like, because it is not fair to those who may like it. We live in a world with many different ideas, thoughts and beliefs, and we all need equal right to share them", "Today in society there are many things people have different views on. They can be religion, race, or brought up in a different way. Today in libraries there are many books of all types. They can relate to all different kinds of people. If one book is discriminating against another indivual is this right? I think the libraries need to stay the way they are and leave things the way they have had them for different reasons.\n       First off, no one is the same, what might be bad to someone else can be good to another person. If someone simply doesn't like the context of a book, movie, or even music ect. They don't have to read,watch,or listen to it. Since no one is the same what someone might not find appealing can be amazing thing to another person.\n     Second, this can be there for purpose. The U.S. wasn't always a equal place. If there are books that talk about the discrimination on other races I think it's simply showing history. If we didn't have history to look back on we wouldn't be able to see how America has progressed. From slave states to all free states. I think it is important for material such as that to be left so it can looked on upon.\n     Third reason, is a library is suppose to consist of these different things such as books, movies, music ect. If we were to take everything out the libraries that comes off offensive it wouldn't be a place were you could find things that you wanted. It would probably be a boring place. If theres no variety in a library I don't see how it can be called a library. You can find whatever your looking for in a library whether its on how to do hair to the hitsory of the United States.\n     In conslusion, these reason make up why libraries should stay the way they are. One is because what might be offensive to a ivdivual might be different to someone else. Second, it would take a lot away from history. Thrid, it wouldn't make a library what it is today. These are ligetament resaons why it should be left alone", "In our public libraries we can find books that are related to slavery, drugs, gangs, prostitution and violence. Theses books all have history in them of our past. We cannot, as a society, forget our past because as many historains say, history repeats its self. If we start censoring our libraries then all that history will be forgoten, and/or lost.\n      Libraries can help us in many different ways. They help us with school projects, bussiness projects, and libraries better our knoweldge as a person. You cannot go censoring the libraries just because someone finds a book offesive. The stories of slavory are still taken offensively amoug people today, but if we start taking stories about people who have been enslaved and hide them from the poeple, we will slip back into that terrible past.\n      There are gang stories of terrifying people, such as Al Capone. He killed many people, destroyed many shops and probably even sold a lot of drugs. We need history to show our weakness as a nation and not hide because of this weakness but thrive on it to better our cities, better our police training, and most importantly, better the next generation of kids to be raised better.\n      There is more than just books at the public library, there are movies and documentaries of our nation and the World. Movies that talk about World War One and World War Two. These types of movies can show how horrifying War really is and how cruel people can get. During World War Two, there was the Holocaust where six million jews lost their lives because one person, Hitler, did not like them. People made movies like those to show the World how devestating man can be but people have made movies on amazing discoveries and amazing places. For example Einstein. One of the greatest findings amoug the World.\n      Music can also be a good way to better ones self. If you play an instrument and you need music to play to, why not go to the library to get some? You dont have to worry about payin for a dollar cd and you can use it until your done with it then return. Then with how advanced our technokwledge is, people can get cd's to burn on to a computer and put on their ipod or MP3 player. Plus the library is a good place to just go look for music you like.\n      So, should there be censorship in our libraries? NO! There should not and the key reason as to why is because it is history. History of our country, history of our World, and history of sad and hard times. Instead of censoring our youth of today from history we need to set age limits. Young people of a certain age can not read certain books unless they are with a parent or gaurdian. That is one simple way to keep our kids from readin to mature thing but still able to get the history he/she needs because as historains always say, history repeats its self and as a growing nation, we need to better ourselves in every way possible. The answer to that is through our history.", "I dont think books that would affend people should be on the shelf. some of the books that maybe on the shelf may hurt some ones feelings. But i also think people should beable to read what they want to read. many people wouldnt read a book that they think would affend them.\n      There are many kinds of books not all book will be bad or affend people. but books that are not apropriot for young kids or teens shouldnt even be in school librarys. In public librarys i think it should be ok to have every type of book. and have different books in different place's. like haveing the young adalt section and the adalt and children section.\n     I think screton books should be sold in book stores like i dont think they should have inapropeiout books in children book store's. They should have a different store for certain books. And parents should monitor what there children are reading and take part in the book by helping them understand what the book is saying.\n      There are lots of parents that dont really care about what there kids read, and to me that's there busness but my apenioun is that they shouldn't let there kids read what they want. Parents should be with the child when he/she is picking out a book. But if it is a teen 16 and older, i think they would be old enough to choise what they want to read. by the time they are that age they have matured enough to read and understand things much easer", "Hi im henry and I agree that if there are books in a school libray or a public libray that are offensive they should be removed. im a type of person who belives that offensive books shouldnt be in librays because i ahte seeing people upset or mad  because they read a book that effened them. That inclues magazines and movies and even music.\n       myself henry has read a few books that has effened my self or has made fun of black people and i have black friends. if I could have it my way i would have all books like that out of school librays and public librays. And i say that because little kids dont need to be reading that kind of stuff and neither do we. thats just like music now days you turn on a radio station and people are cussing and making fun of other colored people. Also you cant understand what there saying half the time. They need to put on music that u can understand that doesnt have cussing in it and that you can understand because some kids like to listen to music.\n     magazines, I look at alot of magazines my self but there all like coonhunting magazines or four-wheeler ones lookin for tires or somthing like that. but yes also the bad magazines need t go to that way little kids arent looking at them. also it mite help some crime to stop to. I say that because people look at magazines that have shooting in then and that have crime in them to. So people see that and there like i wanna try this somtime. so then they call there buddies and say lets try this and most of them do then there in trouble. so i think that it would be helpful to get all the bad magazines that were made and throw them away and things mite change. make some that have like cartoons in them and comics for the little kids. you could even try and make some good health ones that advertise good health for people and teens. To me things would possibly change if we get all the  naughty things out of book,magazines,music.\n     Movies, this is a big one just about all the movies are bad. There are some good ones out there if u look. but i dont know how we could change the movies by anycahnce at all.\n     That was my opion on things. i hope it all makes sense about how i feel and how i think about things.", "Why censore something that someone worked hard on? People put up money and countless amounts of time to write this and yet you want to censore it.See there is honestly no need to censore any thing in the library because there certain sections for certain people therefore this whole conversation shouldnt be going on in the first place.People just like to knit pick about what they can not handle for instense like the word nigger i dont like it at all but i can handle it and therfore i just shut my mouth and suck it up.So I just feel like all the critique and all the imature people just need not to read or dont go to the library but thats only me though.So stop acting like little children the authors want their stuff on shelves and not being banned and raved and ranted about alsoIn conclusion stop being imature and if you dont like it dont read it. Always think to yourself about what your doing before you decside", "A lion lay asleep in the forest, his great head resting on his paws. A timid little mouse came upon him unexpectedly, and in her fright and haste to get away, ran across the lion's nose. Roused from his nap, the lion laid his huge paw angrily on the tiny creature to kill her.\n\n\"Spare me!\" begged the poor mouse. \"Please let me go and some day I will surely repay you.\"\n\nThe lion was much amused to think that a mouse could ever help him. But he was generous and finally let the mouse go.\n\nSome days later, while stalking his prey in the forest, the lion was caught in the toils of a hunter's net. Unable to free himself, he filled the forest with his angry roaring. The mouse knew the voice and quickly found the lion struggling in the net. Running to one of the great ropes that bound him, she gnawed it until it parted, and soon the lion was free.\n\n\"You laughed when I said I would repay you,\" said the Mouse. \"Now you see that even a Mouse can help a Lion.\"", "She took me by the hand and walked me into the lobby like a five-year old child. Didn’t she know I was pushing 15? This was the third home Nancy was placing me in - in a span of eight months. I guess she felt a little sorry for me. The bright fluorescent lights threatened to burn my skin as I walked towards a bouncy-looking lady with curly hair and a sweetly-smiling man. They called themselves Allie and Alex. Cute, I thought.\n\nAfter they exchanged the usual reams of paperwork, it was off in their Chevy Suburban to get situated into another new home. This time, there were no other foster children and no other biological children. Anything could happen.\n\nOver the next few weeks, Allie, Alex, and I fell into quite a nice routine. She’d make pancakes for breakfast, or he’d fry up some sausage and eggs. They sang a lot, even danced as they cooked. They must have just bought the house because, most weekends, we were painting a living room butter yellow or staining a coffee table mocha brown.\n\nI kept waiting for the other shoe to drop. When would they start threatening a loss of pancakes if I didn’t mow the lawn? When would the sausage and eggs be replaced with unidentifiable slosh because he didn’t feel like cooking in the morning? But, it never happened. They kept cooking, singing, and dancing like a couple of happy fools.\n\nIt was a Saturday afternoon when Allie decided it was time to paint the brick fireplace white. As we crawled closer to the dirty old firepit, we pulled out the petrified wood and noticed a teeny, tiny treasure box. We looked at each other in wonder and excitement. She actually said, “I wonder if the leprechauns left it!” While judging her for being such a silly woman, I couldn’t help but laugh and lean into her a little.\n\nTogether, we reached for the box and pulled it out. Inside was a shimmering solitaire ring. Folded underneath was a short piece of paper that read:\n\n“My darling, my heart. Only 80 days have passed since I first held your hand. I simply cannot imagine my next 80 years without you in them. Will you take this ring, take my heart, and build a life with me? This tiny little solitaire is my offering to you. Will you be my bride?”\n\nAs I stared up at Allie, she asked me a question. “Do you know what today is?” I shook my head. “It’s May 20th. That’s 80 days since Nancy passed your hand into mine and we took you home.”\n\nIt turns out, love comes in all shapes and sizes, even a teeny, tiny treasure box from a wonderfully silly lady who believes in leprechauns."]

parser, lt = initialize()

if option == 'Essay 1':
    document_text = documents[0]
    document_label = document_labels[0]
elif option == 'Essay 2':
    document_text = documents[1]
    document_label = document_labels[1]
elif option == 'Essay 3':
    document_text = documents[2]
    document_label = document_labels[2]
elif option == 'Essay 4':
    document_text = documents[3]
    document_label = document_labels[3]
elif option == 'Essay 5':
    document_text = documents[4]
    document_label = document_labels[4]
elif option == 'Essay 6':
    document_text = documents[5]
    document_label = document_labels[5]
elif option == 'Essay 7':
    document_text = documents[6]
    document_label = document_labels[6]
elif option == 'Essay 8':
    document_text = documents[7]
    document_label = document_labels[7]
elif option == 'Essay 9':
    document_text = documents[8]
    document_label = document_labels[8]
elif option == 'Essay 10':
    document_text = documents[9]
    document_label = document_labels[9]
elif option == 'Essay 11':
    document_text = documents[10]
    document_label = document_labels[10]
elif option == 'Essay 12':
    document_text = documents[11]
    document_label = document_labels[11]
elif option == 'Essay 13':
    document_text = documents[12]
    document_label = document_labels[12]
elif option == 'Essay 14':
    document_text = documents[13]
    document_label = document_labels[13]
elif option == 'Essay 15':
    document_text = documents[14]
    document_label = document_labels[14]
elif option == 'Aesop':
    document_text = documents[15]
    document_label = document_labels[15]
elif option == 'Personal Narrative':
    document_text = documents[16]
    document_label = document_labels[16]

spellcorrect = websocketClient()
labels = parser.send(['LABELS'])
print('\n\n\n\n--------------------------')
print(labels, '\n\n', document_text)
print('current label: ', document_label)
print('--------------------------\n\n\n\n')

for i, dl in enumerate(document_labels):
    if dl not in labels:
        [text] = spellcorrect.send([documents[i]])
        ok = parser.send(['PARSEONE', dl, text])

[ctext] = spellcorrect.send([document_text])

record = {}
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

tokens = parser.send(['DOCTOKENS', document_label])
if tokens is None:
    raise Exception("No tokens recognized")

numWords = len(tokens)
print('\nBasic info')
print(numWords, ' words')

lemmas = parser.send(['LEMMAS', document_label])

numLemmas = len(set([lemma.lower()
                     for lemma in lemmas
                     if lemma is not None]))

print(numLemmas, ' distinct words')
if lemmas is None:
    raise Exception("No lemmas recognized")

sentences = parser.send(['SENTENCES', document_label])
if sentences is None:
    raise Exception("No sentences recognized")
numSentences = len(sentences)
print(numSentences, ' Sentences')

paragraphs = parser.send(['PARAGRAPHS', document_label])
if paragraphs is None:
    raise Exception("No paragraphs recognized")
numParas = len(paragraphs)
print(numParas, ' paragraphs')

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

print('\nPart of Speech Information')

posinfo = parser.send(['POS', document_label])
if posinfo is None:
    raise Exception("No part of speech information retrieved")

numVerbs = len([item for item in posinfo if item == 'VERB'])
print(numVerbs, ' verbs')

numNouns = len([item for item in posinfo if item == 'NOUN'])
print(numNouns, ' nouns')

numProperNouns = len([item for item in posinfo if item == 'PROPN'])
print(numProperNouns, ' proper nouns')

numAdjectives = len([item for item in posinfo if item == 'ADJ'])
print(numAdjectives, ' adjectives')

numAdverbs = len([item for item in posinfo if item == 'ADV'])
print(numAdverbs, ' adverbs')

numPreps = len([item for item in posinfo if item == 'ADP'])
print(numPreps, ' prepositions')

numCC = len([item for item in posinfo if item == 'CCONJ'])
print(numCC, ' coordinating conjunctions')

numSC = len([item for item in posinfo if item == 'SCONJ'])
print(numSC, ' subordinating conjunctions')

numAux = len([item for item in posinfo if item == 'AUX'])
print(numAux, ' auxiliary verbs')

numPron = len([item for item in posinfo if item == 'PRON'])
print(numPron, ' pronouns')

POSDisplay = preparePOSDisplayPage(posinfo, option3, tokens)

print('\nVocabulary Information')

il = parser.send(['INTERACTIVELANGUAGE', document_label])
if il is None:
    raise Exception("No information on propositional attitudes retrieved")

interactiveDisplay = prepareSimpleDisplay(il, tokens)
print('Percent Words Suggesting Informal Style: ',
      round(len(il) * 1.0 / len(tokens) * 100))

academics = parser.send(['ACADEMICS', document_label])
if academics is None:
    raise Exception("No academic language information retrieved")

latinates = parser.send(['LATINATES', document_label])
if latinates is None:
    raise Exception("No information on latinate words retrieved")

academic_words = []
if academics is None:
    raise Exception("No academic language information retrieved")

latinates = parser.send(['LATINATES', document_label])
if latinates is None:
    raise Exception("No information on latinate words retrieved")

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

mf = parser.send(['MAXFREQS', document_label])
if mf is None:
    raise Exception("No information on maximum word"
                    + " family frequencies")

freqDisplay, \
    countB1, \
    countB2, \
    countB3, \
    countB4, \
    countB5, \
    countB6, \
    countB7 = prepareFrequencyDisplay(mf,
                                      posinfo,
                                      tokens,
                                      False,
                                      False,
                                      False,
                                      False,
                                      False,
                                      False,
                                      False)

if option2 == 'Word Frequency':
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
      percentLowFrequency)

print('Percent very low frequency:',
      percentVeryLowFrequency)

print('Percent extremely rare words:',
      percentRare)

syl = parser.send(['SYLLABLES', document_label])
if syl is None:
    raise Exception("No information on maximum word family frequencies")

syllablePage = prepareSyllableDisplay(syl,
                                      posinfo,
                                      tokens,
                                      False,
                                      False,
                                      False,
                                      False)

if option2 == 'Number of Syllables':
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

stypes, \
    numSimple, \
    numSimpleComplexPred, \
    numSimpleCompoundPred, \
    numSimpleCompoundComplexPred, \
    numCompound, \
    numComplex, \
    numCompoundComplex = parser.send(['SENTENCETYPES',
                                     document_label])

ccdPage = \
    prepareCompoundComplexDisplay(stypes,
                                  posinfo,
                                  sentences,
                                  tokens,
                                  False,
                                  False,
                                  False,
                                  False,
                                  False,
                                  False,
                                  False)

if option2 == 'Sentence Variety':
    stypes, \
        numSimple,  \
        numSimpleComplexPred, \
        numSimpleCompoundPred, \
        numSimpleCompoundComplexPred, \
        numCompound, \
        numComplex, \
        numCompoundComplex = parser.send(['SENTENCETYPES',
                                         document_label])
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

print('\nSentence Variety')
print('Number of simple kernel sentences: ',
      numSimple)
print('Number of simple sentences with complex predicates: ',
      numSimpleComplexPred)
print('Number of simple sentences with compound predicates: ',
      numSimpleCompoundPred)
print('Number of simple sentences with compound/complex predicates: ',
      numSimpleCompoundComplexPred)
print('Number of compound sentences: ', numCompound)
print('Number of complex sentences: ', numComplex)
print('Number of compound/complex sentences', numCompoundComplex)

print('\nTransition Words and Phrases:')
tp = parser.send(['TRANSITIONPROFILE', document_label])
if tp is None:
    raise Exception("No information on transition words retrieved")

numTransitions = tp[0]
transitionTypeProfile = tp[1]
transitionLocs = tp[2]
print(tp[0], 'transition words or phrases used')

print('\nType\tFrequency')
for item in sorted(transitionTypeProfile):
    print(item, '\t', transitionTypeProfile[item])

tlist = []
print('\nTransition\tFrequency')
for item in sorted(transitionLocs):
    print(item, '\t', transitionLocs[item])

prepcs = None
transitions = prepareTransitionMarking(tokens, tp, prepcs)

print('\nQuotes, Citations, Attributions:')

quotedtext = parser.send(['QUOTEDTEXT', document_label])
numQuotes = 0
quotedLast = False
for i, val in enumerate(quotedtext):
    if val and not quotedLast:
        numQuotes += 1
        quotedLast = True
    elif not val:
        quotedLast = False
if quotedtext is None:
    raise Exception("No quoted text information received")
numQuotedWords = len([val for val in quotedtext if val])

print('\n', numQuotes, ' quotation(s)')
print(numQuotedWords, ' quoted words')

attributions = parser.send(['ATTRIBUTIONS', document_label])
if attributions is None:
    raise Exception("No attribution information received")

numAttributionWords = len([val for val in attributions if val])
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

sources = parser.send(['SOURCES', document_label])
if sources is None:
    raise Exception("No source information received")
numSourceWords = len([val for val in sources if val])
sourceLast = False
numSources = 0
for i, val in enumerate(sources):
    if val and not sourceLast:
        numSources += 1
        sourceLast = True
    elif not val:
        sourceLast = False

print('\n', numSources, ' source(s)')
print(numSourceWords, ' source word(s)')

citedtext = parser.send(['CITES', document_label])
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

numCitedWords = len([val for val in citedtext if val])
print('\n', numCites, ' citation(s)')
print(numCitedWords, ' cited words(s)')

quoteCite = prepareQuoteCite(quotedtext,
                             attributions,
                             sources,
                             citedtext)

print('\nArgument Language:')

aw = parser.send(['ARGUMENTLANGUAGE', document_label])
if aw is None:
    raise Exception("No information on argument words retrieved")

percentArgumentLanguage = round(len(aw) * 1.0 / len(tokens) * 100)
print(percentArgumentLanguage, ' percent argument language in text')

eaw = parser.send(['EXPLICITARGUMENTWORDS', document_label])
if eaw is None:
    raise Exception("No information on explicit argument words retrieved")

cli = parser.send(['CLUSTERINFO', document_label])
if cli is None:
    raise Exception("No information on word clusters retrieved")

cs = parser.send(['CONTENTSEGMENTS', document_label])
if cs is None:
    raise Exception("No information on content segments retrieved")

pl = parser.send(['PROMPTLANGUAGE', document_label])
if pl is None:
    raise Exception("No information on main idea words retrieved")

pr = parser.send(['PROMPTRELATED', document_label])
if tp is None:
    raise Exception("No information on related main idea words retrieved")

core = parser.send(['CORESENTENCES', document_label])
if core is None:
    raise Exception("No information on core sentences retrieved")

ec = parser.send(['EXTENDEDCORESENTENCES', document_label])
if ec is None:
    raise Exception("No information on extended core sentences retrieved")

ps = parser.send(['PERSPECTIVESPANS', document_label])
if ps is None:
    raise Exception("No information on perspective spans retrieved")

sm = parser.send(['STANCEMARKERS', document_label])

if sm is None:
    raise Exception("No information on stance markers retrieved")

pa = parser.send(['PROPOSITIONALATTITUDES', document_label])
if pa is None:
    raise Exception("No information on propositional"
                    + " attitudes retrieved")

cw = []

percentCore = round(len(core) * 1.0 / len(sentences) * 100)
print(percentCore,
      ' percent of sentences seem to express the thesis'
      + ' and main points of an essay')

percentSupporting = \
    round(len(ec) * 1.0 / len(sentences) * 100)

print(percentSupporting,
      ' percent of sentences seem to express supporting points')

percentDetail = round(len(cs) * 1.0 / len(sentences) * 100)

print(percentSupporting,
      ' percent of sentences seem to provide details'
      + ' elaborating on the main points')

details, argumentwords = \
    prepareArgumentWordMarking(tokens, lemmas, aw,
                               eaw, pl, pr, cw, cs)

supportingideas = prepareSupportingIdeas(ec)

essaystructure, argumentwords = \
    prepareArgumentWordMarking(tokens,
                               lemmas,
                               aw, eaw, pl, pr, cw, core)
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

print('\nNarrative Language:')

em = parser.send(['EMOTIONWORDS',
                 document_label])

if em is None:
    raise Exception("No information on emotion words retrieved")

emotionDisplay = prepareEmotionDisplay(em, tokens)

percentEmotion = \
    round(1.0 * len([item for item in em
                     if item is True]) / len(tokens) * 100)

print('Percent emotion words: ', percentEmotion)

ct = parser.send(['CHARACTERWORDS', document_label])

if ct is None:
    raise Exception("No information on character' \
                    + ' trait words retrieved")

traitDisplay = prepareEmotionDisplay(ct, tokens)

percentCharacter = \
    round(1.0 * len([item for item in ct
                     if item is True]) / len(tokens) * 100)

print('Percent character trait words: ',
      percentCharacter)

#emotions = parser.send(['EMOTIONALSTATES',
#                       document_label])
#em = flattenViewpointList(emotions, tokens)
#emotionDisplay = prepareEmotionDisplay(em, tokens)

#traits = parser.send(['CHARACTERTRAITS',
#                     document_label])
#ct = flattenViewpointList(traits, tokens)                       
#traitDisplay = prepareEmotionDisplay(ct, tokens)


directspeech = parser.send(['DIRECTSPEECHSPANS', document_label])

countDirect = 0
for item in directspeech:
    for offset in item:
        countDirect += 1

percentDialogueIndicator = \
    round(1.0 * countDirect / len(tokens) * 100)

print('Percent words suggesting dialogue: ',
      percentDialogueIndicator)

percentQuotedWords = \
    round(1.0 * numQuotedWords / len(tokens) * 100)

print(percentQuotedWords,
      ' percent quoted words')

dialogueDisplay = displayDialogue(tokens,
                                  quotedtext,
                                  directspeech)

in_direct_speech = parser.send(['IN_DIRECT_SPEECH',
                               document_label])

tensechanges = parser.send(['TENSECHANGES',
                           document_label])

locs = parser.send(['LOCATIONS',
                   document_label])

sceneSetting, numComments = \
    prepareSceneDisplay(tokens,
                        tp[3],
                        in_direct_speech,
                        tensechanges,
                        locs)

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

social_awareness = parser.send(['SOCIAL_AWARENESS',
                               document_label])

socialAwarenessPage = \
    prepareSocialAwarenessDisplay(tokens, social_awareness)

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

concretedetails = \
    parser.send(['CONCRETEDETAILS', document_label])

concreteDetailPage = \
    prepareConcreteDetailDisplay(tokens, concretedetails)

percentConcreteDetail = \
    round(1.0 * len(concretedetails) / len(tokens) * 100)

print(percentConcreteDetail,
      ' percent concrete detail words')

[characters,
 otherRefs] = parser.send(['NOMINALREFERENCES',
                          document_label])

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

print(firstPersonRefs, ' first person references')

print(numCharsMultiRef,
      ' characters referenced more than once '
      + '(repeated references to the same name or descriptive noun)')

print('List of references to people or characters:',
      sorted(references))

polarity = parser.send(['TONERATINGS', document_label])
stopwords = parser.send(['STOPWORDS', document_label])
filteredpolarity = []
for i, value in enumerate(polarity):
    if not stopwords[i]:
        filteredpolarity.append(value)
    else:
        filteredpolarity.append(0.0)

tonePage, \
    countStrongPositive, \
    countWeakPositive, \
    countNeutral, \
    countWeakNegative, \
    countStrongNegative = \
    prepareToneDisplay(filteredpolarity,
                       posinfo,
                       tokens,
                       False,
                       False,
                       False,
                       False,
                       False)

if option2 == 'Tone':
    tonePage, \
        countStrongPositive, \
        countWeakPositive, \
        countNeutral, \
        countWeakNegative, \
        countStrongNegative = \
        prepareToneDisplay(filteredpolarity,
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

if option2 == 'Conventions':
    st.write(proofread, unsafe_allow_html=True)
elif option2 == 'Parts of Speech':
    st.write(POSDisplay, unsafe_allow_html=True)
elif option2 == 'Informal Language':
    st.write(interactiveDisplay, unsafe_allow_html=True)
elif option2 == 'Academic Language':
    st.write(academicPage, unsafe_allow_html=True)
elif option2 == 'Word Frequency':
    st.write(freqDisplay, unsafe_allow_html=True)
elif option2 == 'Number of Syllables':
    st.write(syllablePage, unsafe_allow_html=True)
elif option2 == 'Sentence Variety':
    st.write(ccdPage, unsafe_allow_html=True)
elif option2 == 'Main Ideas':
    st.write(essaystructure, unsafe_allow_html=True)
elif option2 == 'Supporting Ideas':
    st.write(supportingideas, unsafe_allow_html=True)
elif option2 == 'Details':
    st.write(details, unsafe_allow_html=True)
elif option2 == 'Content Words':
    st.write(contentDev, unsafe_allow_html=True)
elif option2 == 'Transitions':
    st.write(transitions, unsafe_allow_html=True)
elif option2 == 'Quotations, Citations, Attributions':
    st.write(quoteCite, unsafe_allow_html=True)
elif option2 == 'Argument Words':
    st.write(argumentwords, unsafe_allow_html=True)
elif option2 == 'Own vs. Other Perspectives':
    st.write(subjectivities, unsafe_allow_html=True)
elif option2 == 'Characters':
    st.write(characterPage, unsafe_allow_html=True)
elif option2 == 'Emotion Words':
    st.write(emotionDisplay, unsafe_allow_html=True)
elif option2 == 'Character Traits':
    st.write(traitDisplay, unsafe_allow_html=True)
elif option2 == 'Dialogue':
    st.write(dialogueDisplay, unsafe_allow_html=True)
elif option2 == 'Scene and Setting':
    st.write(sceneSetting, unsafe_allow_html=True)
elif option2 == 'Social Awareness':
    st.write(socialAwarenessPage, unsafe_allow_html=True)
elif option2 == 'Concrete Details':
    st.write(concreteDetailPage, unsafe_allow_html=True)
elif option2 == 'Tone':
    st.write(tonePage, unsafe_allow_html=True)

