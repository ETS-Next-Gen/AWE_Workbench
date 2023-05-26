import spacy
import coreferee
import spacytextblob.spacytextblob
import awe_components.components.lexicalFeatures
import awe_components.components.syntaxDiscourseFeats
import awe_components.components.viewpointFeatures
import awe_components.components.lexicalClusters
import awe_components.components.contentSegmentation
import json

# Initialize the spacy pipeline
nlp = spacy.load("en_core_web_lg")

# Adding all of the components, since
# each of them turns out to be implicated in
# the demo list. I note below which ones can
# be loaded separately to support specific indicators.
nlp.add_pipe('coreferee')
nlp.add_pipe('spacytextblob')
nlp.add_pipe('lexicalfeatures')
nlp.add_pipe('syntaxdiscoursefeatures')
nlp.add_pipe('viewpointfeatures')
nlp.add_pipe('lexicalclusters')
nlp.add_pipe('contentsegmentation')

def outputIndicator(indicatorName, itype, stype=None, text=None, added_filter=None):
    '''
       A function to output three types of information: summary metrics,
       lists of textual information selected by the indicator, and
       the offset information for each word or span selected by the indicator
    '''

    indicator = {}

    if added_filter is None:
        theFilter = [(indicatorName,[True]),('is_alpha',[True])]
    else:
        theFilter = added_filter
        theFilter.append(('is_alpha',[True]))

    indicator['metric'] =\
        doc2._.AWE_Info(infoType=itype,
                        indicator=indicatorName,
                        filters=theFilter,
                        summaryType=stype)  
    
    data = json.loads(
        doc2._.AWE_Info(infoType=itype,
                        indicator=indicatorName,
                        filters=theFilter)).values()

    indicator['offsets'] = \
        [[entry['offset'],entry['length']] \
         for entry \
         in data]

    if itype == 'Token':
        indicator['text'] = \
            json.loads(doc2._.AWE_Info(infoType=itype,
                   indicator=indicatorName, 
                   filters=theFilter,
                   transformations=['lemma'],
                   summaryType='uniq'))
    else:
        indicator['text'] = []

        for span in indicator['offsets']:
            indicator['text'].append(text[int(span[0]):int(span[0])+int(span[1])])

    return indicator

# Two documents slightly modified for purpose of making sure all the indicators show
text = "I do not believe that censorship should be an option for people that find a book, magazine, or movie offensive. I believe that if a person decides to take a book off the shelf because he/she is offended, they are obviously paranoid. If a few cuss words are found in a book and a person doesn't want their children to read that book, then don't allow them to get it. Don't make all of the other people suffer. Censorship is an unnecessary solution to something that isn't even a problem. You know what they say, 'If it ain't broken, don't fix it.'\n\n     First of all, people have a variety of opinions. Some people think that violence is ok and some people don't think it's ok. If one person decides to put a book off the shelf because they find it offensive, what will the next person think? They may find violence perfectly acceptable and they might allow their kids to read the book. Then it would create a big conflict.\n\n     Lastly, parents need to allow their kids to grow up and mature. They also need their kids to know the difference between right and wrong. If they don't read books or movies with violence or cuss words when they're young, what will they do when they discover it when they're older? As a child, it is a time to learn life lessons and begin to form clear distinctions between right and wrong. Shielding your children from it will only hinder their progress in figuring things out and learning to think for themselves as adults (Paterson, 2009).\n\n     According to some critics, censorship is the same thing that Hitler did to prevent people to think for themselves and discover that his tactics were a great evil to society (Paterson, 2009). In other words, censorship is part of fascism and should not even be considered in American society. The citizens of the U.S. have the responsibility of exposing the truth and teaching our children the differences between right and wrong. It's one of the ideals that help make this country great"

text2 = "She took me by the hand and walked me into the lobby like a five-year old child. Didn’t she know I was pushing 15? This was the third home Nancy was placing me in - in a span of eight months. I guess she felt a little sorry for me. The bright fluorescent lights threatened to burn my skin as I walked towards a bouncy-looking lady with curly hair and a sweetly-smiling man. They called themselves Allie and Alex. Cute, I thought.\n\nAfter they exchanged the usual reams of paperwork, it was off in their Chevy Suburban to get situated into another new home. This time, there were no other foster children and no other biological children. Anything could happen.\n\nOver the next few weeks, Allie, Alex, and I fell into quite a nice routine. She’d make pancakes for breakfast, or he’d fry up some sausage and eggs. They sang a lot, even danced as they cooked. They must have just bought the house because, most weekends, we were painting a living room butter yellow or staining a coffee table mocha brown.\n\nI kept waiting for the other shoe to drop. When would they start threatening a loss of pancakes if I didn’t mow the lawn? When would the sausage and eggs be replaced with unidentifiable slosh because he didn’t feel like cooking in the morning? But, it never happened. They kept cooking, singing, and dancing like a couple of happy fools.\n\nIt was a Saturday afternoon when Allie decided it was time to paint the brick fireplace white. As we crawled closer to the dirty old firepit, we pulled out the petrified wood and noticed a teeny, tiny treasure box. We looked at each other in wonder and excitement. She actually said, “I wonder if the leprechauns left it!” While judging her for being such a silly woman, I couldn’t help but laugh and lean into her a little.\n\nTogether, we reached for the box and pulled it out. Inside was a shimmering solitaire ring. Folded underneath was a short piece of paper that read:\n\n“My darling, my heart. Only 80 days have passed since I first held your hand. I simply cannot imagine my next 80 years without you in them. Will you take this ring, take my heart, and build a life with me? This tiny little solitaire is my offering to you. Will you be my bride?”\n\nAs I stared up at Allie, she asked me a question. “Do you know what today is?” I shook my head. “It’s May 20th. That’s 80 days since Nancy passed your hand into mine and we took you home.”\n\nIt turns out, love comes in all shapes and sizes, even a teeny, tiny treasure box from a wonderfully silly lady who believes in leprechauns."


# Process the text
doc = nlp(text)  

# Serialize the data
data = doc.to_bytes()

# Load a different doc in theat variable
doc = nlp(text2)
print('------------------------')
print(doc)
print('------------------------')
# Create a new variable and load the serialized doc
doc2 = nlp('')
doc2.from_bytes(data)
print(doc2)
print('------------------------')

# Define a set of indicators with the kind of filtering/summariation we want
#
# Academic Language, Latinate Words, Low Frequency Words, Adjectives, Adverbs,
#    Sentences, Paragraphs -- 
#    just need to have lexicalfeatures in the pipeline to run.
#
# Transition Words, Ordinal Transition Words --
#    -- shouldonly need syntaxdiscoursefeats in the pipeline to run
#
# Information Sources, Attributions, Citations, Quoted Words, Informal Language
# Argument Words, Opinion Words, Emotion Words, Character Trait Words, Concrete Details,
# Positive and Negative Tone --
#     Need lexicalfeatures + syntaxdiscoursefeats + viewpointfeatures to run
#
# Main idea sentences, supporting idea sentences, supporting detail sentences --
#     Need the full pipeline to run, though the main dependencies are on
#     lexicalclusters and contentsegmentation
#
# Format for this list: Label, type of indicator (Token or Doc), indicator name,
# filter (if needed), summary function to use
spanIndicators = [('Academic Language', 'Token', 'is_academic', None, 'percent'),
                  ('Latinate Words', 'Token', 'is_latinate', None, 'percent'),
                  ('Polysyllabic Words', 'Token', 'nSyll', [('>',[3])], 'percent'),
                  ('Low Frequency Words', 'Token', 'max_freq', [('<',[4])], 'percent'),
                  ('Transition Words', 'Doc', 'transitions', None, 'counts'),
                  ('Ordinal Transition Words', 'Doc', 'transitions',[('==',['ordinal'])], 'total'),
                  ('Adjectives', 'Token', 'pos_', [('==',['ADJ'])], 'percent'),
                  ('Adverbs', 'Token', 'pos_', [('==',['ADV'])], 'percent'),
                  ('Sentence Types', 'Doc', 'sentence_types', None, 'counts'),
                  ('Simple Sentences', 'Doc', 'sentence_types',[('==',['Simple'])], 'total'),
                  ('Sentences', 'Doc', 'sents', None, 'total'),
                  ('Paragraphs', 'Doc', 'delimiter_\n', None, 'total'),
                  ('Information Sources', 'Token', 'vwp_source', None, 'percent'),
                  ('Attributions', 'Token', 'vwp_attribution', None, 'percent'),
                  ('Citations', 'Token', 'vwp_cite', None, 'percent'),
                  ('Quoted Words', 'Token', 'vwp_quoted', None, 'percent'),
                  ('Informal Language', 'Token', 'vwp_interactive', None, 'percent'),
                  ('Argument Words', 'Token', 'vwp_argumentword', None, 'percent'),
                  ('Opinion Words', 'Token', 'vwp_evaluation', None, 'total'),
                  ('Emotion Words', 'Token', 'vwp_emotionword', None, 'percent'),
                  ('Positive Tone', 'Token', 'vwp_tone', [('>',[.4])], 'percent'),
                  ('Negative Tone', 'Token', 'vwp_tone', [('<',[-.4])], 'percent'),
                  ('Character Trait Words', 'Token', 'vwp_character', None, 'percent'),
                  ('Concrete Details', 'Token', 'concrete_details', None, 'percent'),
                  ('Main Idea Sentences', 'Doc', 'main_ideas', None, 'total'),
                  ('Supporting Idea Sentences', 'Doc', 'supporting_ideas', None, 'total'),
                  ('Supporting Detail Sentences', 'Doc', 'supporting_details', None, 'total')
                  ]


# Loop through the indicators and print out the data we got
for indicator in spanIndicators:
    (label, infoType, select, filterInfo, summaryType) = indicator
    data = outputIndicator(select, infoType, stype=summaryType, text=text, added_filter=filterInfo)
    print('----------------------')
    print(label + ':', data)
    print('----------------------')
