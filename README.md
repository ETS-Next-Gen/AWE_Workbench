# AWE Workbench

This project serves as a workbench for open-source natural language processing pipeline designed to support automated writing evaluation (AWE) – automated scoring and feedback of student essays and other educational materials.

## AWE Project Dependencies

This project installs 4 other dependencies (more info on their individual repositories below):

* [AWE_Components](https://github.com/ArgLab/AWE_Components)
* [AWE_Lexica](https://github.com/ArgLab/AWE_Lexica)
* [AWE_LanguageTool](https://github.com/ArgLab/AWE_LanguageTool)
* [AWE_SpellCorrect](https://github.com/ArgLab/AWE_SpellCorrect)

## Installation

Before installing, make sure you have a python (3.11) virtual environment (venv, conda, etc).

Once you have set up your environment, ensure you are in the root directory of this project, then run:

```bash
# Install Workbench from root directory
pip install -e .

# Develop flag is to be used if in development mode
python -m awe_workbench.setup.data --[install/develop]
```

## Running Workbench & Tests

Before running any tests, ensure that you run the main and WordSeqProbability servers:

```bash
# Main Server
python -m awe_workbench.web.startServers

# wordSeqProbabilityServer
python -m awe_components.wordprobs.wordseqProbabilityServer
```

After this, you can run the main suite of tests:

```bash
pytest tests/test_awe_nlp.py
```

## Package Structure

There are 4 services provided by Workbench:

1. A LanguageTool wrapper. LanguageTool identifies grammar, usage, mechanics, and style errors, and provides feedback text that can be displayed to the user. Our LanguageTool wrapper provides an additional layer of classification that makes it easier to identify errors that address the same specific construct, such as subject/verb agreement within grammar, or likely types within spelling.

2. A spelling correction module that incorporates PySymSpell and Neuspell. This module is specifically designed to be used to standardize the spelling of student texts written on a common topic, so that they can be subjected to further NLP analysis. It works best when applied to a corpus of student texts that reflects a range of spelling abilities, so that it can infer the correct spellings of words commonly used to address a specific assignment. When this information is not available, or is not sufficient, it falls back on the spell-correction facilities provided by Neuspell, a state-of-the-art transformer-based spell-corrector.

3. A wrapper for the BERT transformer that allows the user to extract the probability of words in context. BERT can, of course, be used independently to build a variety of classifiers, though currently the AWE Workbench uses it only in a few, relatively limited contexts.

4. A natural language processing (NLP) pipeline built around the Spacy parser. In addition to the Coreferee and Holmes Extractor modules, this pipeline includes custom components.

### Custom Components to NLP pipeline

* A lexical feature component, which calculates a variety of word-based features, including token, lemma and root counts and frequencies, size of word families, syllable counts, word length, latinate and academic vocabulary status, number of word senses, and measures of animacy, abstractness/concreteness, sentiment and subjectivity.

* A lexical cluster component, which provides an agglomerative clustering of the words that appear within a document using Spacy word vectors. These clusters are used to support a number of other statistics, such as measures of the distribution of the largest clusters (which are likely to reflect the primary topic of the document) and of the difficulty of the vocabulary that appears in other, smaller clusters (which are likely to reflect development of secondary topics).

* A syntax and discourse feature component, which provides measures of the number and length of sentences and paragraphs, the number and types of transition words used to mark discourse segments, and the number and length of pronominal coreference chains; measures of syntactic complexity and variety such as depth of embedding and the number of tags and types of grammatical dependencies deployed in a text, and measures of textual coherence, such as the cosine similarity of content words in adjacent sentences or across paragraph boundaries and other discourse transitions.

* A viewpoint feature component, which identifies viewpoint predicates, such as emotion, cognition, and perception words, stance markers, which indicate the subjective perspective of the writer, and markers of direct and indirect speech. The viewpoint feature component uses this information to determine what parts of a text are to be evaluated as reflecting a specific viewpoint. The resulting features are used to support various genre-specific analyses, such as identification of the parts of a text that contain argumentation, or which contain references to the actions and mental states of story characters.

* A content segmentation component, which identifies major content blocks marked by chains of repeated or related words, and which determines whether individual sentences have significant content that address the main ideas of an essay and/or overlap with specified prompt language.

These modules are by design rule-based, rather than statistical in nature, and intended to capture features of the text that can be explicitly identified and labeled using linguistic knowledge. They capture dimensions that have been established as relevant to essay quality and structure in the research literature, which can be an important consideration when building educational applications. These criteria led to the exclusion of some forms of text analysis, such as rhetorical-structure parsing, which depend critically on a statistical model. However, the linguistic features supported by the AWE workbench include most of the surface cues that such models exploit. The outputs created by the AWE Workbench can easily be used as inputs to more sophisticated, statistical classifiers, but if used without modification, they are intended to provide a strong baseline for analyzing student texts.

It is important to note that while the features deployed in the AWE Workbench may bear a family resemblance to features deployed in commercial AWE systems, they were for the most part selected because they capture what patent law would recognize as prior art – well-known, long-established methods for analyzing student texts using natural language processing techniques. Places where the AWE Workbench contains novel contributions are identified below. Such contributions may be subject to patent applications filed by the authors, but are nonetheless released for use under the terms of the Gnu Affero public license.

Also note that we include a simple server API, to support use cases where the AWE Workbench needs to run in a distributed environment.

## Contributions

While largely based on prior art, the AWE Workbench does contain several significant innovations, which are outlined below.

Open-Source Concreteness Estimates. The largest, most reliable databases of lexical concreteness estimates for English are not available under the GNU Affero license. The AWE Workbench applies an algorithm that generalizes the freely-available Glasgow concreteness norms to other English words, using the WordNet ontology. This algorithm was developed by the authors as part of IES grant R205A210297. We are currently validating these estimates. However, they appear to be accurate enough to support their use as an approximation to larger datasets of human concreteness ratings, such as those provided by Brysbaert, Warriner, & Kuperman, 2013.

The ETS Viewpoint Lexicon. The AWE Workbench defines an approach to subjectivity and stance-taking that depends on a fine-grained lexical classification of cognition, perception, emotion, and communication predicates, developed by the authors as part of IES grant R205A210297. Using this classification, the AWE Workbench uses syntactic dependencies identified by the Spacy parser to locate noun phrases and clauses that define the viewpoints attributed to these predicates and the propositions to which those viewpoints apply. This makes it possible to identify explicit argument language, important features of narrative, and other aspects of text structure that depend upon stance and viewpoint. As such, it covers similar ground to such widely-used resources as the MPQA argument lexicon, but in greater depth, and follows a design philosophy similar to that defended by St. Dizier (2020). We are currently validating the use of this lexicon. However, its results appear to be accurate enough to use to identify potential argument or narrative language in a text.

## Applications

Like most state-of-the-art AWE systems, the AWE Workbench can be used to extract summary features that can be used to predict human scores or classify student responses into meaningful categories. We are currently validating these uses with publicly available datasets. However, since equivalent features to those deployed by the AWE Workbench have already been validated elsewhere, the user can proceed with similar applications in advance of our completion of this effort. We will include a script for extracting summary features with the distribution we are preparing for public release.

# AWE Language Features

## AWE Info Types

|infoType|Description/Notes                                                                                                                                       |
|--------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
|Doc     |Document-level feature; very similar to Token infoType, but utilizes a createSpanInfo() function which references a variable called "docspan_extensions"|
|Token   |Token-level feature; makes use of getattr(); applies filters to document tokens                                                                         |

## AWE Indicators

|Indicator|Description/Notes                                                                                                                                       |Doc/Token?|parserServer associated command(s)|
|---------|--------------------------------------------------------------------------------------------------------------------------------------------------------|----------|----------------------------------|
|text     |the text of a spacy token extracted by the system, less whitespace                                                                                      |Token     |DOCTOKENS                         |
|text_with_ws|the text of a spacy token extracted by the system, including adjacent whitespace (useful to get exact original text of a document from spacy tokens)    |Token     |DOCTOKENS_WITH_WS                 |
|lemma_   |the lemma (base word form) of a spacy token                                                                                                             |Token     |LEMMAS                            |
|is_stop  |whether a spacy token is in its standard stop list                                                                                                      |Token     |STOPWORDS                         |
|lower_   |the text of a spacy token, lowercased, less adjacent whitespace                                                                                         |Token     |WORDTYPES                         |
|root     |the root word (less any derivational suffixes like -ness) for a given word                                                                              |Token     |ROOTS                             |
|nSyll    |the number of syllables in a word                                                                                                                       |Token     |SYLLABLES                         |
|is_latinate|whether a word is classified as latinate vocabulary                                                                                                     |Token     |LATINATES                         |
|is_academic|whether a word is classified as academic vocabulary                                                                                                     |Token     |ACADEMICS                         |
|nSenses  |number of senses associated with a token's lemma in WordNet                                                                                             |Token     |SENSENUMS, LOGSENSENUMS           |
|morphology|an object summarizing morphological features associated with the token's lemma                                                                          |Token     |MORPHOLOGY                        |
|nMorph   |the number of morphemes in this token's lemma                                                                                                           |Token     |MORPHNUMS                         |
|min_root_freq|A word frequency statistic -- the frequency of the rarest word with the same root as this word                                                          |Token     |HALROOTFREQS, HALLOGROOTFREQS     |
|root_famSize|Root Word family size -- the number of words associated with this token's root word                                                                     |Token     |ROOTFAMSIZES                      |
|root_pfmf|A different word frequency statistic for the root (not the same frequency database as min_root_freq)                                                    |Token     |ROOTPFMFS                         |
|family_size|Word family size - the family size for this token's base word. May be different than for the root because word families are not based on the same analysis as root and morphology.|Token     |FAMILYSIZES                       |
|token_freq|Frequency of this exact word token (using the wordfreq library)                                                                                         |Token     |TOKFREQS                          |
|lemma_freq|Frequency of this token's base form (less inflections like plurals, using the wordfreq library)                                                         |Token     |LEMMAFREQS                        |
|root_Freq|Frequency of the root (using wordfreq library)                                                                                                          |Token     |ROOTFREQS                         |
|max_freq |Maximum frequency of all inflectional forms of a word (using wordfreq library)                                                                          |Token     |MAXFREQS                          |
|concreteness|Measure of abstract vs.concrete status of a word                                                                                                        |Token     |CONCRETES                         |
|abstract_trait|Classifier (yes/no) whether word names an abstract trait                                                                                                |Token     |ABSTRACTTRAITS                    |
|animate  |Classifier (yes/no) whether word names an animate entity                                                                                                |Token     |ANIMATES                          |
|location |Classifier (yes/no) whether word names a location                                                                                                       |Token     |LOCATIONS                         |
|deictic  |Classifier (yes/no) whether word is a deictic pronoun or anaphor like this, that, here, there                                                           |Token     |DEICTICS                          |
|delimiter_n|Number of delimiters (paragraph breaks etc.?) in document                                                                                               |Doc       |PARAGRAPHS                        |
|sents    |List of sentences in the document                                                                                                                       |Doc, Doc  |SENTENCES, PARAGRAPHLENS          |
|transitions|List of transition words in the document                                                                                                                |Doc       |TRANSITIONS                       |
|transition_distances|List of distances between transition words in the document                                                                                              |Doc       |TRANSITIONDISTANCES               |
|intersentence_cohesions|Cosine similarity between adjacent sentences using summed word embeddings for the words in either sentences                                             |Doc       |SENTENCECOHESIONS                 |
|sliding_window_cohesions|Cosine similarity calculated by taking cosine similarity between adjacent blocks of words within a document and sliding the window that defines those blocks over the whole document |Doc       |SLIDERCOHESIONS                   |
|syntacticDepthsOfRhemes|the syntactic depth (avg. number of head words dominating a given word) in the rheme, or predicate part of a sentence                                   |Doc, Token|RHEMEDEPTHS, THEMEDEPTHS          |
|weightedSyntacticDepths|the syntactic depth (avg. number of head words) in a text, weighted to reflect the fact that certain positions, like subject position, are costlier to put complex information in|Token     |WEIGHTEDDEPTHS                    |
|weightedSyntacticBreadths|the syntactic breadth (a measure similar to syntactic depth but which ignores embedded clauses) of the words in a document                              |Token     |WEIGHTEDBREADTHS                  |
|sentence_types|An object that contains summary information about the types of sentence patterns that appear in a document                                              |Doc       |SENTENCETYPES                     |
|vwp_quoted|Whether a word is part of a sequence of words between quotation marks                                                                                   |Token     |QUOTEDTEXT                        |
|vwp_direct_speech|What parts of a document is to be considered direct speech, often marked by verbs of saying and quotation marks                                         |Doc       |DIRECTSPEECHSPANS                 |
|vwp_in_direct_speech|Whether a token is part of a direct speech segment                                                                                                      |Token     |IN_DIRECT_SPEECH                  |
|vwp_perspective|A flag that identifies whether a word is a marker of perspective. check -- does this contain the ID of the token whose perspective is being taken? I think it may.|Token     |PERSPECTIVES                      |
|vwp_attribution|A flag that identifies whether a token is part of an attribution, like "according to Max"                                                               |Token     |ATTRIBUTIONS                      |
|vwp_source|A flag that identifies whether a token is to be interpreted as the source of a statement, like Max in "Max claims ..."                                  |Token     |SOURCES                           |
|vwp_cite |A flag that indicates whether a token is to be interpreted as part of a citation, i.e., like (Johnson, 2003)                                            |Token     |CITES                             |
|vwp_statements_of_fact|An object identifying sentences in a document to be interpreted as statements of fact                                                                   |Doc       |STATEMENTSOFFACT                  |
|vwp_statements_of_opinion|an object identifying sentences in a document to be interpreted as statements of opinions                                                               |Doc       |STATEMENTSOFOPINION               |
|vwp_perspective_spans|An object indicating what spans in a document are from what perspective                                                                                 |Doc       |PERSPECTIVESPANS                  |
|vwp_stance_markers|An object indicating what tokens ina document are to be interpreted as subjective elements indicating a stance or opinion                               |Doc       |STANCEMARKERS                     |
|vwp_claim|A flag indicating that a token is to be interpreted as part of a claim made by the author                                                               |Token     |CLAIMTEXTS                        |
|vwp_discussion|A flag indicating that a token is to be interpreted as part of text elaborating on some point, providing discussion of it                               |Token     |DISCUSSIONTEXTS                   |
|vwp_emotionword|A flag indicating that a token is to be interpreted as a word denoting an emotion                                                                       |Token     |EMOTIONWORDS                      |
|vwp_character_traits|A flag indicating that a token is to be interpreted as a word denoting a human character trait                                                          |Token     |CHARACTERWORDS                    |
|vwp_emotion_states|An object mapping emotional states to the tokens that identify the individual experiencing them                                                         |Doc       |EMOTIONALSTATES                   |
|vwp_propositional_attitudes|An object mapping clauses expressing propositions to phrases that express what individual has what attitude toward that proposition                     |Doc       |PROPOSITIONALATTITUDES            |
|vwp_social_awareness|An object that identifies specific words that indicate mutual social awareness between multiple individuals                                             |Doc       |SOCIAL_AWARENESS                  |
|concrete_detail|A flag indicating that a word names a concrete detail of some kind                                                                                      |Token     |CONCRETEDETAILS                   |
|vwp_interactive|A flag indicating that a word is typically used in a conversational context                                                                             |Token     |INTERACTIVELANGUAGE               |
|vwp_argumentword|A flag indicating that a word has some connection to argument                                                                                           |Token     |ARGUMENTWORDS                     |
|vwp_argumentation|A flag indicating that a word is part of a clause that makes some kind of argument                                                                      |Token     |ARGUMENTLANGUAGE                  |
|vwp_explicit_argument|A flag indicating that a word clearly implies an argument even taking out of context                                                                    |Token     |EXPLICITARGUMENTWORDS             |
|subjectivity|A value indicating how subjective vs. objective a token should be interpreted as being                                                                  |Token     |SUBJECTIVITYRATINGS               |
|vwp_sentiment|A value indicating a degree of positive or negative sentiment for any given word                                                                        |Token     |SENTIMENTRATINGS                  |
|vwp_tone |A value indicating some combination of sentiment and polarity (as these are closely related concepts, it's often better to combine them)                |Token     |TONERATINGS                       |
|polarity |A value indicating a degree of positive or negative sentiment for any given word                                                                        |Token     |POLARITYRATINGS                   |
|in_past_tense_scope|Whether a token is part of a past tense clause                                                                                                          |Token     |PASTTENSESCOPE                    |
|governing_subject|The word interpreted as being the logical subject of a predicate                                                                                        |Token     |GOVERNINGSUBJECTS                 |
|clusterID|An ID distinguishing different clusters of content words identified in a document                                                                       |Token     |CLUSTERS                          |
|main_ideas|An object indicating what spans in a document are likely to express the main idea of the document (works best in argumentative texts)                   |Doc       |MAINIDEAS                         |
|supporting_ideas|An object indicating what spans in a document are likely to express supporting arguments in a document                                                  |Doc       |SUPPORTINGIDEAS                   |
|supporting_details|An object indicating what spans in a document are likely to provide details, rather than abstract arguments and supporting points                       |Doc       |SUPPORTINGDETAILS                 |
|devword  |A flag indicating a word is probably being used to develop details in a longer text                                                                     |Token     |DEVWORDS                          |

## AWE Filters

|Filter|Description/Notes                                                                                                                                       |
|------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
|('is_alpha', ['True'])|Alphabetic words. Excludes punctuation, numerals, etc.                                                                                                  |
|('devword', ['True'])|Filters to just devwords.                                                                                                                               |
|('==', ['positive'])|appear as filters for "transitions" indicator                                                                                                           |
|('==', ['conditional'])|appear as filters for "transitions" indicator                                                                                                           |
|('==', ['consequential'])|appear as filters for "transitions" indicator                                                                                                           |
|('==', ['contrastive'])|appear as filters for "transitions" indicator                                                                                                           |
|('==', ['counterpoint'])|appear as filters for "transitions" indicator                                                                                                           |
|('==', ['comparative'])|appear as filters for "transitions" indicator                                                                                                           |
|('==', ['crossreferential'])|appear as filters for "transitions" indicator                                                                                                           |
|('==', ['illustrative'])|appear as filters for "transitions" indicator                                                                                                           |
|('==', ['negative'])|appear as filters for "transitions" indicator                                                                                                           |
|('==', ['emphatic'])|appear as filters for "transitions" indicator                                                                                                           |
|('==', ['evidentiary'])|appear as filters for "transitions" indicator                                                                                                           |
|('==', ['general'])|appear as filters for "transitions" indicator                                                                                                           |
|('==', ['ordinal'])|appear as filters for "transitions" indicator                                                                                                           |
|('==', ['purposive'])|appear as filters for "transitions" indicator                                                                                                           |
|('==', ['periphrastic'])|appear as filters for "transitions" indicator                                                                                                           |
|('==', ['hypothetical'])|appear as filters for "transitions" indicator                                                                                                           |
|('==', ['summative'])|appear as filters for "transitions" indicator                                                                                                           |
|('==', ['introductory'])|appear as filters for "transitions" indicator                                                                                                           |
|('==', ['ADJ'])|appear as filters for "pos_" indicator                                                                                                                  |
|('==', ['ADV'])|appear as filters for "pos_" indicator                                                                                                                  |
|('==', ['NOUN'])|appear as filters for "pos_" indicator                                                                                                                  |
|('==', ['PROPN'])|appear as filters for "pos_" indicator                                                                                                                  |
|('==', ['VERB'])|appear as filters for "pos_" indicator                                                                                                                  |
|('==', ['NUM'])|appear as filters for "pos_" indicator                                                                                                                  |
|('==', ['ADP'])|appear as filters for "pos_" indicator                                                                                                                  |
|('==', ['CCONJ'])|appear as filters for "pos_" indicator                                                                                                                  |
|('==', ['SCONJ'])|appear as filters for "pos_" indicator                                                                                                                  |
|('==', ['AUX'])|appear as filters for "pos_" indicator                                                                                                                  |
|('==', ['PRON'])|appear as filters for "pos_" indicator                                                                                                                  |
|('==', ['Simple'])|appear as filters for "sentence_types" indicator                                                                                                        |
|('==', ['SimpleComplexPred'])|appear as filters for "sentence_types" indicator                                                                                                        |
|('==', ['SimpleCompoundPred'])|appear as filters for "sentence_types" indicator                                                                                                        |
|('==', ['SimpleCompoundComplexPred'])|appear as filters for "sentence_types" indicator                                                                                                        |
|('==', ['Compound'])|appear as filters for "sentence_types" indicator                                                                                                        |
|('==', ['Complex'])|appear as filters for "sentence_types" indicator                                                                                                        |
|('==', ['CompoundComplex'])|appear as filters for "sentence_types" indicator                                                                                                        |
|('>', [.4])|appear as filters for "vwp_tone" indicator                                                                                                              |
|('<', [-.4])|appear as filters for "vwp_tone", "max_freq" indicators                                                                                                 |
|('>', [3])|appear as filters for "nSyll" indicator                                                                                                                 |

## AWE Transformations

|Transformation|Description/Notes                                                                                                                                       |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
|len           |Length of a list, if the indicator contains a list of items                                                                                             |
|sqrt          |Square root of a numeric value                                                                                                                          |
|log           |Log of a numeric value                                                                                                                                  |
|tokenlen      |Length in characters of the word token being summarized                                                                                                 |
|text          |The text value of a span or token                                                                                                                       |

## AWE Summary Types

|SummaryType|Description/Notes                                                                                                                                       |
|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
|mean       |the mean of the values of an indicator, if those are numeric                                                                                            |
|median     |the median of the values of an indicator, if those are numeric                                                                                          |
|max        |the maximum of the values of an indicator, if those are numeric                                                                                         |
|min        |the minimum of the values of an indicator, if those are numeric                                                                                         |
|stdev      |the standard deviation of the values of an indicator, if those are numeric                                                                              |
|proportion |the proportion of values that are positively flagged for an indicator                                                                                   |
|total      |the sum of the values of an indicator                                                                                                                   |
|counts     |the number of items in an indicator, if it's a list                                                                                                     |
|uniq       |a list of unique values extracted from the full list of values returned by an indicator                                                                 |

