import streamlit as st
import re
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


third_person_pronoun = ['he',
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

colorList = ["#d98880",
             "#c39bd3",
             "#7fb3d5",
             "#76d7c4",
             "#f7dc6f",
             "e67e22",
             "#b2babb"]

lion = None
with open('essays/lion.txt') as f:
    lion = f.read()

leprechaun = None
with open('essays/leprechaun.txt') as f:
    leprechaun = f.read()


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
                   and tokens[last-1] != '"'
                   and tokens[last-1] != "'"
                   and tokens[last-1] != "''"
                   and tokens[last-1] != '``'
                   and tokens[last-1] != '”'
                   and tokens[last-1] != '“'
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


def prepareCharacterDisplay(characterList, tokenList):
    tokstr = ''
    toklist = tokenList.copy()
    charNum = 0
    charset = {}
    for character in sorted(characterList.keys()):
        if character.lower() in third_person_pronoun:
            continue
        if len(characterList[character]) > 2:
            charset[character] = characterList[character]
    for character in charset:
        colorList = ["blue",
                     "green",
                     "brown",
                     "orange",
                     "red",
                     "purple",
                     "cyan"]
        if len(characterList[character]) > 2:
            for ref in characterList[character]:
                toklist = toklist[:ref]\
                    + ['<u><font color="'
                       + colorList[charNum]
                       + '">'
                       + toklist[ref]
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
            + '</li>'
        charNum += 1
    headstr += '</ul><hr>'
    return headstr, tokstr


def prepareEmotionDisplay(emotions,
                          characterList,
                          tokenList,
                          colorList):

    toklist = tokenList.copy()
    first = emotions['explicit_1']
    second = emotions['explicit_2']
    third = emotions['explicit_3']

    charset = []
    for charName in sorted(characterList.keys()):
        if charName.lower() in third_person_pronoun:
            continue
        if len(characterList[charName]) > 2:
            for item in characterList[charName]:
                charset.append(charName)
    emoset = {}
    for i, character in enumerate(third):
        emotionList = third[character]
        if character in charset:
            for item in emotionList:
                if character not in emoset:
                    emoset[character] = []
                emoset[character].append(item)

    for item in first:
        if 'SELF' not in emoset:
            emoset['SELF'] = []
        if item not in emoset['SELF']:
            emoset['SELF'].append(item)

    for item in second:
        if 'you' not in emoset:
            emoset['you'] = []
        if item not in emoset['you']:
            emoset['you'].append(item)

    headstr = '<ul><lh>for ... </lh>'
    for i, character in enumerate(emoset):
        headstr += '<li><span style="background-color:' \
            + colorList[i] + \
            '">' \
            + character \
            + '</span></li>'
    headstr += '</ul><hr>'
    for i, character in enumerate(emoset):
        emotionList = emoset[character]
        for offset in emotionList:
            toklist = toklist[:offset] \
                + ['<span style="background-color:'
                   + colorList[i]
                   + '">'
                   + toklist[offset]
                   + '</span>'] \
                + toklist[offset+1:]
    return headstr, normalize(' '.join(toklist))


def prepareTraitDisplay(traits, characterList, tokenList, colorList):
    toklist = tokenList.copy()
    first = traits['explicit_1']
    second = traits['explicit_2']
    third = traits['explicit_3']

    charset = {}
    for charName in sorted(characterList.keys()):
        if charName.lower() in third_person_pronoun:
            continue
    traitset = {}
    for i, character in enumerate(third):
        traitList = third[character]
        if character in characterList:
            for item in traitList:
                if character not in traitset:
                    traitset[character] = []
                traitset[character].append(item)

    for item in first:
        if 'SELF' not in traitset:
            traitset['SELF'] = []
        if item not in traitset['SELF']:
            traitset['SELF'].append(item)

    for item in second:
        if 'you' not in traitset:
            traitset['you'] = []
        if item not in traitset['you']:
            traitset['you'].append(item)
    headstr = '<ul><lh>for ... </lh>'
    for i, character in enumerate(traitset):
        headstr += '<li><span style="background-color:' \
            + colorList[i] \
            + '">' \
            + character \
            + '</span></li>'
    headstr += '</ul><hr>'
    for i, character in enumerate(traitset):
        traitList = traitset[character]
        for offset in traitList:
            toklist = toklist[:offset] \
                + ['<span style="background-color:'
                   + colorList[i] + '">'
                   + toklist[offset]
                   + '</span>'] \
                + toklist[offset + 1:]
    return headstr, normalize(' '.join(toklist))


def prepareSceneDisplay(tokens,
                        transitions,
                        in_direct_speech,
                        tense_changes,
                        locations):
    loc = 0
    temp = []
    for change in tense_changes:
        present = False
        newloc = change['loc']
        if not change['past']:
            if not present:
                newloc = change['loc']
                temp += tokens[loc:newloc - 1]
                temp.append(tokens[newloc - 1]
                            + '<strong style="background-color: #c39bd3">')
                present = True
                loc = newloc
            else:
                newloc = change['loc']
                temp += tokens[loc: newloc]
                present = True
                loc = newloc
        else:
            newloc = change['loc']
            temp += tokens[loc: newloc]
            if newloc > 0:
                temp.append('</strong>'+tokens[newloc])
            else:
                temp.append(tokens[newloc])
            present = False
            loc = newloc + 1
    temp += tokens[loc:len(tokens) - 1]
    if present:
        temp.append('</strong>' + tokens[len(tokens)-1])
    else:
        temp.append(tokens[len(tokens)-1])

    loc = 0
    temp2 = []
    inLoc = False
    for i, locFlag in enumerate(locations):
        if not inLoc and locFlag:
            temp2.append('<span style="background-color: yellow">'+temp[i])
            inLoc = True
        elif inLoc and not locFlag:
            temp2.append('</span>' + temp[i])
            inLoc = False
        else:
            temp2.append(temp[i])
    temp = temp2
    loc = 0
    output = ''
    for transition in transitions:
        breakloc = transition[1]
        start = transition[2]
        end = transition[3]
        if transition[4] != 'temporal' \
           or in_direct_speech[start]:
            output += ' '.join(temp[loc:end]) + ' '
            loc = end
        else:
            output += ' '.join(temp[loc:breakloc])
            output += ' '.join(temp[breakloc:start])
            output += ' <span style="background-color: #90ee90"> '
            output += ' '.join(temp[start:end+1])
            output += ' </span> '
            loc = end+1
    output += ' '.join(temp[loc:len(temp)])
    headstr = '<ul><li><span style="background-color: #90ee90">' \
        + 'Times</span></li><li>' \
        + '<span style="background-color: yellow">Places</span>'
    if len(tense_changes) > 1:
        headstr += \
            '<li><span style="background-color: #c39bd3">Comments</span></li>'
    headstr += '</ul><hr>'
    return headstr, normalize(output.replace('  ',
                              ' ').replace('\n',
                                           '<br />'))


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
    output += ' '.join(tokens[loc: len(tokens)])
    return normalize(output.replace('  ', ' '))


cs, parser, lt = initialize()


def prepareConcreteDetailDisplay(tokens, details):
    loc = 0
    output = ''
    for item in details:
        detailLoc = item
        output += ' '.join(tokens[loc:detailLoc])
        output += ' <span style="background-color: yellow">'\
                  + tokens[detailLoc] + '</span> '
        loc = detailLoc + 1
    output += ' '.join(tokens[loc:len(tokens)])
    return normalize(output)


document_text = lion
document_label = 'Aesop'

option2 = st.selectbox('', ('Fable', 'Personal Narrative'))

if option2 == 'Fable':
    st.write('<h1>Aesop\'s Fables: The Lion and the Mouse</h1>',
             unsafe_allow_html=True)

    document_text = lion
    document_label = 'Aesop'

elif option2 == 'Personal Narrative':
    st.write('<h1>Personal Narrative</h1>', unsafe_allow_html=True)

    document_text = leprechaun
    document_label = 'Personal Narrative'

ok = parser.send(['PARSEONE', document_label, document_text])
tokens = parser.send(['DOCTOKENS', document_label])
print(tokens)
quoted = parser.send(['QUOTEDTEXT', document_label])

animates = parser.send(['ANIMATES', document_label])
clusters = parser.send(['CLUSTERS', document_label])
[characters, otherRefs] = parser.send(['NOMINALREFERENCES',
                                      document_label])
print(document_label)
directspeech = parser.send(['DIRECTSPEECHSPANS', document_label])
print(directspeech)
emotions = parser.send(['EMOTIONALSTATES',
                       document_label])
traits = parser.send(['CHARACTERTRAITS',
                     document_label])
transitionprofile = parser.send(['TRANSITIONPROFILE',
                                document_label])
in_direct_speech = parser.send(['IN_DIRECT_SPEECH',
                               document_label])
tensechanges = parser.send(['TENSECHANGES',
                           document_label])
social_awareness = parser.send(['SOCIAL_AWARENESS',
                               document_label])
concretedetails = parser.send(['CONCRETEDETAILS',
                              document_label])
argumentlanguage = parser.send(['ARGUMENTLANGUAGE',
                               document_label])
locs = parser.send(['LOCATIONS', document_label])
ok = parser.send(['CLEARPARSED'])

tokens2 = displayDialogue(tokens, quoted, directspeech)
headstr3, tokens3 = \
    prepareCharacterDisplay(characters, tokens)

headstr4, tokens4 = prepareEmotionDisplay(emotions,
                                          characters,
                                          tokens,
                                          colorList)

headstr5, tokens5 = prepareTraitDisplay(traits,
                                        characters,
                                        tokens,
                                        colorList)

headstr6, tokens6 = prepareSceneDisplay(tokens,
                                        transitionprofile[3],
                                        in_direct_speech,
                                        tensechanges,
                                        locs)

tokens7 = prepareSocialAwarenessDisplay(tokens, social_awareness)
tokens8 = prepareConcreteDetailDisplay(tokens, concretedetails)
option = st.selectbox(
    '',
    ('Characters',
     'Dialogue',
     'Scene and Setting',
     'Concrete Details',
     'Emotions',
     'Character Traits',
     'Awareness of Others'))

if option == 'Characters':
    st.write(headstr3, unsafe_allow_html=True)
elif option == 'Emotions':
    st.write(headstr4, unsafe_allow_html=True)
elif option == 'Character Traits':
    st.write(headstr5, unsafe_allow_html=True)
elif option == 'Scene and Setting':
    st.write(headstr6, unsafe_allow_html=True)

if option == 'Characters':
    st.write(tokens3, unsafe_allow_html=True)
elif option == 'Dialogue':
    st.write(tokens2, unsafe_allow_html=True)
elif option == 'Emotions':
    st.write(tokens4, unsafe_allow_html=True)
elif option == 'Awareness of Others':
    st.write(tokens7, unsafe_allow_html=True)
elif option == 'Character Traits':
    st.write(tokens5, unsafe_allow_html=True)
elif option == 'Scene and Setting':
    st.write(tokens6, unsafe_allow_html=True)
elif option == 'Concrete Details':
    st.write(tokens8, unsafe_allow_html=True)
else:
    st.write(document_text)
    
print(quoted)
