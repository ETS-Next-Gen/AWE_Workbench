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
