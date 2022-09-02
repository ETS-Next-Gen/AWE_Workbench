import streamlit as st
import re
from annotated_text import annotated_text
from awe_workbench.web.websocketClient import websocketClient
from pylt_classifier.languagetoolClient import languagetoolClient


def initialize():
    """
    Initialize our CorpusSpellcheck and parser objects
    (for spell-correction and parsing with spacy + coreferee
    and other extensions using a modified version of the holmes
    extractor library. While doing so, we initialize a walked
    series of lexical databases that support some of the metrics
    we want to capture.
    """

    # Initialize the parser
    parser = websocketClient()
    parser.set_uri("ws://localhost:8766")

    # return spellchecker and parser objects
    return parser


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
                          + colorList[i] + \
                          '">Time</span></li>'
            elif item == 'contrastive':
                prefix += ' <li style="display: inline">' \
                          + '<span title="Difference"' \
                          + ' style="background-color: ' \
                          + colorList[i] \
                          + '">Difference</span></li>'
            elif item == 'comparative':
                prefix += ' <li style="display: inline">' \
                          + '<span title="Similarity"' \
                          + ' style="background-color: ' \
                          + colorList[i] \
                          + '">Similarity</span></li>'
            elif item == 'illustrative':
                prefix += ' <li style="display: inline">' \
                          + '<span title="Illustration"' \
                          + ' style="background-color: ' \
                          + colorList[i] \
                          + '">Illustration</span></li>'
            elif item == 'emphatic':
                prefix += ' <li style="display: inline">' \
                          + '<span title="Emphasis"' \
                          + 'style="background-color: ' \
                          + colorList[i] \
                          + '">Emphasis</span></li>'
            elif item == 'ordinal':
                prefix += ' <li style="display: inline">' \
                          + '<span title="List"' \
                          + ' style="background-color: ' \
                          + colorList[i] \
                          + '">List</span></li>'
            elif item == 'evidentiary':
                prefix += ' <li style="display: inline">' \
                          + '<span title="List"' \
                          + ' style="background-color: ' \
                          + colorList[i] + \
                         '">Evidence</span></li>'
            elif item == 'conditional':
                prefix += ' <li style="display: inline">' \
                          + '<span title="Condition"' \
                          + ' style="background-color: ' \
                          + colorList[i] \
                          + '">Condition</span></li>'
            elif item == 'counterpoint':
                prefix += ' <li style="display: inline">' \
                          + '<span title="Counterpoint"' \
                          + ' style="background-color: ' \
                          + colorList[i] + \
                          '">Counterpoint</span></li>'
            elif item == 'consequential':
                prefix += ' <li style="display: inline">' \
                          + '<span title="Consequences"' \
                          + ' style="background-color: ' \
                          + colorList[i] + \
                          '">Consequences</span></li>'
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
                output += ' <span title="Time" style="background-color: ' \
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
                output += ' <span title="Emphasis" style="background-color: ' \
                          + colorList[colorchoice] + '">'
            elif item[4] == 'ordinal':
                output += ' <span title="List" style="background-color: ' \
                          + colorList[colorchoice] + '">'
            elif item[4] == 'evidentiary':
                output += ' <span title="Evidence" style="background-color: ' \
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
                          + ' style="background-color: ' \
                          + colorList[colorchoice] + '">'
            else:
                output += ' <span title="' \
                          + item[4] \
                          + '" style="background-color: grey"> '
        if item[3] not in covered:
            output += ' '.join(temp[start: end + 1]) + ' '
        if item[0] != 'NEWLINE' and item[3] not in covered:
            output += '</span> '
        loc = end + 1
        lastStart = sentenceStart
        if item[3] not in covered:
            covered.append(item[3])
    output += ' '.join(temp[loc: len(tokens)])
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
                   and core[coreloc+1][0] == end:
                    temp[i - 1] += ' '
                else:
                    if '\n' in temp[i - 1]:
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
        temp[len(temp) - 1] += '</div>'

    essaystructure = temp
    temp = tokens

    loc = 0
    prefix2 = '<div style="width: 100%; display:flex; flex-direction: row;' \
              + ' justify-content: center; align-items: center">' \
              + '<ul><li style="display: inline;' \
              + ' float: left; border:1px solid black;' \
              + ' margin: auto; padding: 5px;' \
              + ' background-color: #AFEEEE">' \
              + 'Words Related to the Prompt' \
              + '</li><li style="display: inline; float: left; border:none;' \
              + ' margin: auto; padding: 5px">&nbsp;</li>' \
              + '<li style="display: inline; border:1px solid black;' \
              + ' margin: auto; padding: 5px; text-decoration: underline;' \
              + ' float: left; background-color: #FAED27">' \
              + 'Explicit Argument Words' \
              + '</li><li style="display: inline; float: left; border:none;' \
              + ' margin: auto; padding: 5px">&nbsp;</li>' \
              + '<li style="display: inline; border:1px solid black;' \
              + ' margin: auto; padding: 5px; text-decoration: underline;' \
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
                or lemmas[i].lower() in promptlanguage):
            temp.append(' <span style="text-decoration: underline;'
                        + ' background-color: #AFEEEE">'
                        + token + '</span> ')
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
                            + ' <span style="text-decoration: underline;'
                            + ' background-color: #AFEEEE">')
    return normalize(' '.join(essaystructure)), prefix2 + normalize(output)


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
        if option2 == 'Details' and perspectives[i] == 'OTHER':
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
                          + ' background-color: #7ddaff"> ' +
                          + tokens[i] + ' </span></u>')
        elif (perspectives[i] == 'AUDIENCE'
              and option3 == 'Audience Perspective'):
            if not stancemarkers[i]:
                output.append('<span title="Second Person"'
                              + ' style="background-color: #7ddaff"> '
                              + tokens[i] + ' </span>')
            else:
                output.append('<span title="Second Person"'
                              + ' style="background-color: #7ddaff"><u> '
                              + tokens[i] + ' </u></span>')
        elif (option3 == 'Other Perspective'
              and perspectives[i] == 'THIRDPERSON'):
            if not stancemarkers[i]:
                output.append('<span title="Third Person"'
                              + ' style="background-color: #f7bc81"> '
                              + tokens[i] + ' </span>')
            else:
                output.append('<span title="Third Person"'
                              + ' style="background-color: #f7bc81"><u> '
                              + tokens[i] + ' </u></span>')
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
            temp1.append('<span style="font-style: italic; '
                         + 'background-color: #CEE5CE"> '
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


# if option == 'GRE Issue Essay':
#     st.write('<h1>GRE Issue Essay</h1>', unsafe_allow_html=True)

prompt = "As people rely more and more on technology to solve problems," \
         + " the ability of humans to think for themselves will surely" \
         + " deteriorate."

directions = 'Discuss the extent to which you agree or disagree with the' \
             + ' statement and explain your reasoning for the position you' \
             + ' take. In developing and supporting your position, you' \
             + ' should consider ways in which the statement might or' \
             + ' might not hold true and explain how these considerations' \
             + ' shape your position.'

st.write('<b>' + prompt + '</b>', unsafe_allow_html=True)
st.write('<i>' + directions + '</i>', unsafe_allow_html=True)

option = st.selectbox('',
                      ('Score 6 GRE Issue Essay',
                       'Score 5 GRE Issue Essay',
                       'Score 4 GRE Issue Essay',
                       'Score 3 GRE Issue Essay',
                       'Score 2 GRE Issue Essay'))

option2 = st.selectbox('',
                       ('Key Points',
                        'Supporting Points',
                        'Details',
                        'Transitions',
                        'Argument Words',
                        'Own vs. Other Perspectives'))
option3 = ''
if option2 == 'Own vs. Other Perspectives':
    option3 = st.selectbox('',
                           ('Author\'s Perspective',
                            'Audience Perspective',
                            'Other Perspective'))

document_text6 = None
with open('essays/gre6.txt') as f:
    document_text6 = f.read()
    f.close()

document_label6 = 'Score 6 GRE Issue Essay'

document_text5 = None
with open('essays/gre5.txt') as f:
    document_text5 = f.read()
    f.close()

document_label5 = 'Score 5 GRE Issue Essay'

document_text4 = None
with open('essays/gre4.txt') as f:
    document_text4 = f.read()
    f.close()

document_label4 = 'Score 4 GRE Issue Essay'

document_text3 = None
with open('essays/gre3.txt') as f:
    document_text3 = f.read()
    f.close()

document_label3 = 'Score 3 GRE Issue Essay'

document_text2 = None
with open('essays/gre2.txt') as f:
    document_text2 = f.read()
    f.close()

document_label2 = 'Score 2 GRE Issue Essay'

parser = initialize()
if option == 'Score 6 GRE Issue Essay':
    document_text = document_text6
    document_label = document_label6
elif option == 'Score 5 GRE Issue Essay':
    document_text = document_text5
    document_label = document_label5
elif option == 'Score 4 GRE Issue Essay':
    document_text = document_text4
    document_label = document_label4
elif option == 'Score 3 GRE Issue Essay':
    document_text = document_text3
    document_label = document_label3
elif option == 'Score 2 GRE Issue Essay':
    document_text = document_text2
    document_label = document_label2

cs = websocketClient()
[text] = cs.send([document_text])

# ok = parser.send(['PARSEONEWITHPROMPT',document_label, \
#                  text,prompt,'effect of technology on thinking'])
ok = parser.send(['PARSEONE', document_label, text])
tokens = parser.send(['DOCTOKENS', document_label])
lemmas = parser.send(['LEMMAS', document_label])

tp = parser.send(['TRANSITIONPROFILE', document_label])
aw = parser.send(['ARGUMENTLANGUAGE', document_label])
eaw = parser.send(['EXPLICITARGUMENTWORDS', document_label])
cli = parser.send(['CLUSTERINFO', document_label])
cs = parser.send(['CONTENTSEGMENTS', document_label])
pl = parser.send(['PROMPTLANGUAGE', document_label])
pr = parser.send(['PROMPTRELATED', document_label])
core = parser.send(['CORESENTENCES', document_label])
ec = parser.send(['EXTENDEDCORESENTENCES', document_label])
ps = parser.send(['PERSPECTIVESPANS', document_label])
sm = parser.send(['STANCEMARKERS', document_label])
pa = parser.send(['PROPOSITIONALATTITUDES', document_label])

print(pl, pr)

prepcs = []
cw = []
prepcs = None
# for chain in cs:
#     flat_list = sorted([item for sublist in chain[2] for item in sublist])
#     for item in flat_list:
#         cw.append(item)
#     prepcs.append([chain[0], chain[1], flat_list])

details, argumentwords = \
   prepareArgumentWordMarking(tokens, lemmas, aw, eaw, pl, pr, cw, cs)

lastoffset = 0
lastlength = 0
outhtml = '<!DOCTYPE html><html><head></head><body>'
for item in ec:
    outhtml += normalize(' '.join(tokens[lastoffset:item[0]]))
    outhtml += '<span style="font-style: bold; background-color: #AFEEEE">' \
        + normalize(' '.join(tokens[item[0]:item[1]])) + '</span>'
    lastoffset = item[1]
outhtml += normalize(' '.join(tokens[lastoffset:]))
outhtml += '</body></html>'
outhtml = outhtml.replace('\n', '<br />')

essaystructure, argumentwords = \
    prepareArgumentWordMarking(tokens, lemmas, aw, eaw, pl, pr, cw, core)

transitions = prepareTransitionMarking(tokens, tp, prepcs)
subjectivities, perspectives, stancemarkers = \
    prepareSubjectivityDisplay(tokens, ps, sm, option2, option3)
ok = parser.send(['CLEARPARSED'])
if option2 == 'Key Points':
    st.write(essaystructure, unsafe_allow_html=True)
elif option2 == 'Supporting Points':
    st.write(outhtml, unsafe_allow_html=True)
elif option2 == 'Details':
    st.write(details, unsafe_allow_html=True)
elif option2 == 'Content Words':
    st.write(contentDev, unsafe_allow_html=True)
elif option2 == 'Transitions':
    st.write(transitions, unsafe_allow_html=True)
elif option2 == 'Argument Words':
    st.write(argumentwords, unsafe_allow_html=True)
elif option2 == 'Own vs. Other Perspectives':
    st.write(subjectivities, unsafe_allow_html=True)
