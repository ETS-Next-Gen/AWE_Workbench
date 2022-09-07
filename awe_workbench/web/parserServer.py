#!/usr/bin/env python3.10
# Copyright 2022, Educational Testing Service

import asyncio
import base64
import websockets
import json
import awe_workbench
import holmes_extractor
import holmes_extractor.manager
import holmes_extractor.ontology
from holmes_extractor.manager import Manager
from holmes_extractor.ontology import Ontology

class parserServer:

    # Initialize
    parser = None

    def __init__(self, pipeline_def=[]):

        ### set up and initializing Holmes
        # Start the Holmes manager with the English model
        # You can try setting overall_similarity_threshold to 0.85 and/or perform_coreference_resolution to False
        self.parser = holmes_extractor.manager.Manager(
            model='en_core_web_lg',
            perform_coreference_resolution=True,
            extra_components=pipeline_def)      

        asyncio.get_event_loop().run_until_complete(
            websockets.serve(self.run_parser, 'localhost', 8766))
        print('parser running')
        asyncio.get_event_loop().run_forever()
        print('died')

    async def kill(self, websocket):
        self.parser.close()
        await websocket.close()
        exit()

    async def run_parser(self, websocket, path):
        async for message in websocket:

            messagelist = json.loads(message)
            command = ''
            #print(messagelist)
            try:
                if messagelist[0] == 'KILL':
                    command = 'KILL'
                    await websocket.send(json.dumps(True))
                    await self.kill(websocket)
                elif messagelist[0] == 'CLEARPARSED':
                    command = 'CLEARPARSED'
                    self.parser.remove_all_documents()
                    await websocket.send(json.dumps(True))
                elif messagelist[0] == 'REMOVE':
                    command = 'REMOVE'
                    label = messagelist[1]
                    self.parser.remove_document(label)
                    await websocket.send(json.dumps(True))
                elif messagelist[0] == 'PARSEONE':
                    command = 'PARSEONE'
                    label = messagelist[1]
                    text = messagelist[2]
                    if label in self.parser.list_document_labels():
                        self.parser.remove_document(label)
                    self.parser.parse_and_register_document(text, label)
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(True))
                elif messagelist[0] == 'PARSESET':
                    command = 'PARSESET'
                    results = []
                    [labels, texts] = messagelist[1]
                    for i, text in enumerate(texts):
                        text = texts[i]
                        if text is not None and len(text)>0:
                            if labels[i] in self.parser.list_document_labels():
                                self.parser.remove_document(labels[i])
                            self.parser.parse_and_register_document(text,labels[i])
                    await websocket.send(json.dumps(True))
                elif messagelist[0] == 'LABELS':
                    command = 'LABELS'
                    labels = self.parser.list_document_labels()
                    await websocket.send(json.dumps(labels))
                elif messagelist[0] == 'SERIALIZED':
                    command = 'SERIALIZED'
                    label = messagelist[1]
                    serialized = base64.b64encode(self.parser.serialize_document(label))
                    await websocket.send(serialized)
                elif messagelist[0] == 'NEWSEARCHPHRASE':
                    command = 'NEWSEARCHPHRASE'
                    search_phrase_text = messagelist[1]
                    label = messagelist[2]
                    ok = self.parser.register_search_phrase(search_phrase_text)
                    await websocket.send(ok)
                elif messagelist[0] == 'REMOVELABELEDSEARCH':
                    command = 'REMOVELABELEDSEARCH'
                    label = messagelist[1]
                    self.parser.remove_all_search_phrases_with_label(label)
                    await websocket.send(json.dumps(True))
                elif messagelist[0] == 'CLEARSEARCHES':
                    command = 'CLEARSEARCHES'
                    self.parser.remove_all_search_phrases()
                    await websocket.send(json.dumps(True))
                elif messagelist[0] == 'SHOWSEARCHLABELS':
                    command = 'SHOWSEARCHLABELS'
                    labels = self.parser.list_search_phrase_labels()
                    await websocket.send(json.dumps(labels))
                elif messagelist[0] == 'MATCH_DOCUMENTS':
                    command = 'MATCH_DOCUMENTS'
                    matches = self.parser.match()
                    await websocket.send(json.dumps(matches))
                elif messagelist[0] == 'FREQUENCIES':
                    command = 'FREQUENCIES'
                    freqinfo = self.parser.get_corpus_frequency_information()
                    await websocket.send(json.dumps(freqinfo))
                elif messagelist[0] == 'TOPIC_MATCHES':
                    command = 'TOPIC_MATCHES'
                    text_to_match = messagelist[1]
                    # This search takes a long list of keyword parameters, all
                    # of them with preset default thresholds. TBD: expose
                    # all of these parameters in more complex topic match
                    # functionality. Holmes extractor documentation describes
                    # what each of these parameters involves.
                    matches = self.parser.topic_match_documents_against(text_to_match, \
                                                                        word_embedding_match_threshold=.42, \
                                                                        relation_score=20, \
                                                                        reverse_only_relation_score=15, \
                                                                        single_word_score=10, \
                                                                        single_word_any_tag_score=5, \
                                                                        different_match_cutoff_score=10, \
                                                                        relation_matching_frequency_threshold=0.0, \
                                                                        embedding_matching_frequency_threshold=0.0, \
                                                                        use_frequency_factor=True)
                    await websocket.send(json.dumps(matches))
                # Holmes Extractor also has supervised topic model building
                # facilities using the functions get_supervised_topic_training_basis(),
                # and deserialize_supervised_topic_classifier(). TBD: Add support
                # for Holmes supervised topic model building to the server, using
                # the example from the examples directory.
                elif messagelist[0] == 'DOCTOKENS':
                    command = 'DOCTOKENS'
                    # Position in the list returned equals position in the document
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    if doc is not None:
                        tokens = [token.text for token in doc if token.text is not None]
                        await websocket.send(json.dumps(tokens))
                    else:
                        await websocket.send(json.dumps([]))
                elif messagelist[0] == 'DOCHEADS':
                    command = 'DOCHEADS'
                    # Position in the list returned equals position in the document
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    heads = [token.head.i for token in doc]
                    await websocket.send(json.dumps(heads))
                elif messagelist[0] == 'POS':
                    command = 'POS'
                    # Position in the list returned equals position in the document
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    heads = [token.pos_ for token in doc]
                    await websocket.send(json.dumps(heads))
                elif messagelist[0] == 'DOCDEPENDENCIES':
                    command = 'DOCDEPENDENCIES'
                    # Position in the list returned equals position in the document
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    deps = [token.dep_ for token in doc]
                    await websocket.send(json.dumps(deps))
                elif messagelist[0] == 'DOCENTITIES':
                    command = 'DOCENTITIES'
                    # Position in the list returned equals position in the document
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    ents = [[ent.text, ent.start_char, ent.end_char, ent.label_] for ent in doc.ents]
                    await websocket.send(json.dumps(ents))
                elif messagelist[0] == 'TOKVECS':
                    command = 'TOKVECS'
                    #List returned contains lists pairing token offset with token vectors cast as strings
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.token_vectors))
                elif messagelist[0] == 'LEMMAS':
                    command = 'LEMMAS'
                    # Position in the list returned equals position in the document
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.lemmas))
                elif messagelist[0] == 'STOPWORDS':
                    # Position in the list returned equals position in the document
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.stopwords))
                elif messagelist[0] == 'WORDTYPES':
                    command = 'WORDTYPES'
                    # Note: this is just a list of the unique word types,
                    # so position in the list does not correspond to
                    # position in the text.
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.word_types))
                elif messagelist[0] == 'ROOTS':
                    command = 'ROOTS'
                    # Position in the list returned equals position in the document
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.morphroot))
                elif messagelist[0] == 'SYLLABLES':
                    command = 'SYLLABLES'
                    # Position in the list returned equals position in the document
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.nSyllables))
                elif messagelist[0] == 'WORDLENGTH':
                    command = 'WORDLENGTH'
                    # Position in the list returned equals position in the document
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.sqrtNChars))
                elif messagelist[0] == 'LATINATES':
                    command = 'LATINATES'
                    # Position in the list returned equals position in the document
                    # Flag 1 for latinate, 0 for not
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.latinates))
                elif messagelist[0] == 'ACADEMICS':
                    command = 'ACADEMICS'
                    # Position in the list returned equals position in the document
                    # Flag 1 for academic, 0 for not
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.academics))
                elif messagelist[0] == 'SENSENUMS':
                    command = 'SENSENUMS'
                    # Position in the list returned equals position in the document
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.sensenums))
                elif messagelist[0] == 'LOGSENSENUMS':
                    command = 'LOGSENSENUMS'
                    # Position in the list returned equals position in the document
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.logsensenums))
                elif messagelist[0] == 'MORPHOLEX':
                    command = 'MORPHOLEX'
                    # Position in the list returned equals position in the document
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.morpholex))
                elif messagelist[0] == 'MORPHNUMS':
                    command = 'MORPHNUMS'
                    # Position in the list returned equals position in the document
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.morphnums))
                elif messagelist[0] == 'HALROOTFREQS':
                    command = 'HALROOTFREQS'
                    # Position in the list returned equals position in the document
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.root_freqs_HAL))
                elif messagelist[0] == 'HALLOGROOTFREQS':
                    command = 'HALLOGROOTFREQS'
                    # Position in the list returned equals position in the document
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.log_root_freqs_HAL))
                elif messagelist[0] == 'ROOTFAMSIZES':
                    command = 'ROOTFAMSIZES'
                    # Position in the list returned equals position in the document
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.root_fam_sizes))
                elif messagelist[0] == 'ROOTPFMFS':
                    command = 'ROOTPFMFS'
                    # Position in the list returned equals position in the document
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.root_pfmfs))
                elif messagelist[0] == 'FAMILYSIZES':
                    command = 'FAMILYSIZES'
                    # Position in the list returned equals position in the document
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.family_sizes))
                elif messagelist[0] == 'TOKFREQS':
                    command = 'TOKFREQS'
                    # Position in the list returned equals position in the document
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps([str(num) for num in doc.vector]))
                elif messagelist[0] == 'LEMMAFREQS':
                    command = 'LEMMAfREQS'
                    # Position in the list returned equals position in the document
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.lemma_freqs))
                elif messagelist[0] == 'ROOTFREQS':
                    command = 'ROOTFREQS'
                    # Position in the list returned equals position in the document
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.root_freqs))
                elif messagelist[0] == 'MAXFREQS':
                    command = 'MAXFREQS'
                    # Position in the list returned equals position in the document
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.max_freqs))
                elif messagelist[0] == 'MORPHLEXVALS':
                    command = 'MORPHLEXVALS'
                    # Position in the list returned equals position in the document
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.morpholex))
                elif messagelist[0] == 'CONCRETES':
                    command = 'CONCRETES'
                    # Position in the list returned equals position in the document
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.concretes))
                elif messagelist[0] == 'ABSTRACTTRAITS':
                    command = 'ABSTRACTTRAITS'
                    # Position in the list returned equals position in the document
                    # Flag 1 if the word names an abstract trait, 0 otherwise
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.abstract_traits))
                elif messagelist[0] == 'ANIMATES':
                    command = 'ANIMATES'
                    # Position in the list returned equals position in the document
                    # Flag 1 if the word names an animate entity, 0 otherwise
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.animates))
                elif messagelist[0] == 'LOCATIONS':
                    command = 'LOCATIONS'
                    # Position in the list returned equals position in the document
                    # Flag 1 if the word names an animate entity, 0 otherwise
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.locations))
                elif messagelist[0] == 'DEICTICS':
                    command = 'DEICTICS'
                    # Position in the list returned equals position in the document
                    # Flag 1 if the word names a deictic element, 0 otherwise
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.animates))
                elif messagelist[0] == 'PARAGRAPHS':
                    command = 'PARAGRAPHS'
                    # Items in the list indicate word offsets in the document
                    # at which paragraph breaks appear
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.paragraph_breaks))
                elif messagelist[0] == 'SENTENCES':
                    command = 'SENTENCES'
                    # Items in the list indicate word offsets in the document
                    # at which paragraph breaks appear
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps([(sent.start,sent.end) for sent in doc.sents]))
                elif messagelist[0] == 'PARAGRAPHLENS':
                    command = 'PARAGRAPHLENS'
                    # Items in the list indicate lengths of paragraphs listed by offset
                    # in GETPARAGRAPHS
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.paragraph_lengths))
                elif messagelist[0] == 'TRANSITIONPROFILE':
                    command = 'TRANSITIONPROFILE'
                    # Returns a rich data structure in a list containing
                    # (1) total number of transition words in the document
                    # (2) a dictionary that lists the frequency of a predefined
                    #     set of transition word categories.
                    # (3) a dictionary that lists the frequency of individual
                    #     transition words
                    # (4) a list of lists that provides for each transition
                    #     word the word string, its start and stop offsets,
                    #     and its transition word category.
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.transition_word_profile))
                elif messagelist[0] == 'TRANSITIONDISTANCES':
                    command = 'TRANSITIONDISTANCES'
                    # List of cosine distances between ten-word windows before and after
                    # a transition
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.transition_distances))
                elif messagelist[0] == 'SENTENCECOHESIONS':
                    command = 'SENTENCECOHESIONS'
                    # List of cosine distances between ten-word windows before and after
                    # a sentence boundary
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.intersentence_cohesions))
                elif messagelist[0] == 'SLIDERCOHESIONS':
                    command = 'SLIDERCOHESIONS'
                    # List of cosine distances between ten-word windows before and after
                    # a sliding window through the text
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.sliding_window_cohesions))
                elif messagelist[0] == 'COREFCHAINS':
                    command = 'COREFCHAINS'
                    # List of coreference chains found in document
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.coref_chains))
                elif messagelist[0] == 'RHEMEDEPTHS':
                    command = 'RHEMEDEPTHS'
                    # Syntactic depth of the sentence rheme -- part of sentence
                    # before the main verb where given information is usually placed
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.syntacticRhemeDepths))
                elif messagelist[0] == 'THEMEDEPTHS':
                    command = 'THEMEDEPTHS'
                    # Syntactic depth of the sentence rheme -- part of sentence
                    # after the main verb where given information is usually placed
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.syntacticThemeDepths))
                elif messagelist[0] == 'WEIGHTEDDEPTHS':
                    command = 'WEIGHTEDDEPTHS'
                    # Syntactic depth weighted to penalize left-embedded structures
                    # that tend to be harder to process
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.weightedSyntacticDepths))
                elif messagelist[0] == 'WEIGHTEDBREADTHS':
                    command = 'WEIGHTEDBREADTHS'
                    # Syntactic breadth -- measure of extent to which sentence structure
                    # is additive, consisting of coordinated structures and loosely appended
                    # modifiers typical of spoken, often unplanned sentence production
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.weightedSyntacticBreadths))
                elif messagelist[0] == 'SENTENCETYPES':
                    # tuple giving number and location of sentence types
                    # format:
                    # (1,1,1,1,[1,2,3,4]) would be the record for a text that
                    # had four sentences -- simple sentence, compound sentence, complex
                    # sentence, and compound/complex sentence, in that order.
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.sentence_types))
                elif messagelist[0] == 'SYNTACTICPROFILE':
                    command = 'SYNTACTICPROFILE'
                    # Returns a dictionary containing frequency information about
                    # the syntactic relations and categories in the text. This includes
                    # information about the frequency of parts of speech, morphological
                    # categories, and syntactic dependencies between specific parts
                    # of speech.
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.syntacticProfile))
                elif messagelist[0] == 'NORMEDSYNTACTICPROFILE':
                    command = 'NORMEDSYNTACTICPROFILE'
                    # Returns a dictionary containing normalized frequency information
                    # (proportionas) for the syntactic relations and categories in the text.
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.syntacticProfileNormed))
                elif messagelist[0] == 'QUOTEDTEXT':
                    command = 'QUOTEDTEXT'
                    # 1 for tokens within quotation marks, 0 for other text
                    # Position in the list corresponds to offset of token in the document
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.vwp_quoted))
                elif messagelist[0] == 'DIRECTSPEECHSPANS':
                    command = 'DIRECTSPEECHSPANS'
                    # Data about subset of quoted text -- specifically, quoted text
                    # that is attributed to a specific speaker.
                    #
                    # Returns a list of lists with three top level elements:
                    # 1. Speaker: a list of offsets to tokens referring to the speaker(s)
                    # 2. Addressee: a list of offsets to tokens referring to the person(s) spoken to.
                    # 3. Span start offset
                    # 4. Span end offset.
                    #
                    # Note that first and second person pronouns inside direct speech may reference
                    # a person explicitly identified in the direct speech framing text. Coreferee
                    # reference resolution may apply, so that the speaker and addressee references
                    # may be to a proper noun at the head of a pronominal reference chain that includes
                    # the direct speech frame.
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.vwp_direct_speech_spans))
                elif messagelist[0] == 'IN_DIRECT_SPEECH':
                    # 1 for tokens within quoted stretches of direct speech, 0 for other text
                    # Position in the list corresponds to offset of token in the document
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.vwp_in_direct_speech))
                elif messagelist[0] == 'TENSECHANGES':
                    # list of positions where tense changed in the main document flow (not in direct speech/
                    # quotations, with flag to indicate whether shift was to past tense or to present tense.
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.vwp_tense_changes))
                elif messagelist[0] == 'PERSPECTIVES':
                    # list of positions where perspective is indicated
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.vwp_perspectives))
                elif messagelist[0] == 'ATTRIBUTIONS':
                    # list of positions where attribution is indicated
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.vwp_attributions))
                elif messagelist[0] == 'SOURCES':
                    # list of positions where source is indicated
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.vwp_sources))
                elif messagelist[0] == 'CITES':
                    # list of positions where source is indicated
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.vwp_cites))
                elif messagelist[0] == 'PERSPECTIVESPANS':
                    command = 'PERSPECTIVESPANS'
                    # Returns a dictionary with four top level keys:
                    # 1.Implicit: Spans whose perspective is implicitly that of the
                    #   speaker/author
                    # 2. First person: Spans whose perspective is explicitly that of
                    #    the speaker/author, indicated by first person pronouns
                    # 3. Second person: Spans whose perspective is explicitly that of
                    #    the audience, indicated by second person pronouns
                    # 4. Third person: Spans whose perspective is that of some other
                    #    agent. This key has subkeys corresponding to the offsets of
                    #    the noun/proper noun referring to the viewpoint entity.
                    #
                    # Each of these keys is associated with a list of offsets, which
                    # corresponds to the words in the spans to which these perspectives
                    # apply.
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.vwp_perspective_spans))
                elif messagelist[0] == 'STANCEMARKERS':
                    command = 'STANCEMARKERS'
                    # Stance marker tokens identified by our perspective lexicon/code
                    # Returns a dictionary with four top level keys:
                    # 1.Implicit: Spans whose perspective is implicitly that of the
                    #   speaker/author
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.vwp_stance_markers))
                elif messagelist[0] == 'PERSPECTIVESPANS':
                    command = 'PERSPECTIVESPANS'
                    # Returns a dictionary with
                    # 2. First person: Spans whose perspective is explicitly that of
                    #    the speaker/author, indicated by first person pronouns
                    # 3. Second person: Spans whose perspective is explicitly that of
                    #    the audience, indicated by second person pronouns
                    # 4. Third person: Spans whose perspective is that of some other
                    #    agent. This key has subkeys corresponding to the offsets of
                    #    the noun/proper noun referring to the viewpoint entity.
                    #
                    # Each of these keys is associated with a list of offsets, which
                    # corresponds to the stance markers in the spans to which these perspectives
                    # apply.
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.vwp_stance_markers))

                elif messagelist[0] == 'CLAIMTEXTS':
                    # Returns a sequence of true/false flags corresponding to token offsets
                    # in the document that are part of a claim sentence
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.vwp_claims))

                elif messagelist[0] == 'DISCUSSIONTEXTS':
                    # Returns a sequence of true/false flags corresponding to token offsets
                    # in the document that are part of a claim sentence
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.vwp_discussions))

                elif messagelist[0] == 'EMOTIONWORDS':
                    command = 'EMOTIONWORDS'
                    # Returns a sequence of true/false flags corresponding to token offsets
                    # in the document that are emotion words
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.vwp_emotionwords))

                elif messagelist[0] == 'CHARACTERWORDS':
                    command = 'CHARACTERWORDS'
                    # Returns a sequence of true/false flags corresponding to token offsets
                    # in the document that are character words
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.vwp_characterwords))

                elif messagelist[0] == 'EMOTIONALSTATES':
                    command = 'EMOTIONALSTATES'
                    # Returns a dictionary with four top level keys:
                    # 1.Implicit: Spans whose perspective is implicitly that of the
                    #   speaker/author
                    # 2. First person: Spans whose perspective is explicitly that of
                    #    the speaker/author, indicated by first person pronouns
                    # 3. Second person: Spans whose perspective is explicitly that of
                    #    the audience, indicated by second person pronouns
                    # 4. Third person: Spans whose perspective is that of some other
                    #    agent. This key has subkeys corresponding to the offsets of
                    #    the noun/proper noun referring to the viewpoint entity.
                    #
                    # Each of these keys is associated with a list of offsets, which
                    # corresponds to emotion predicates that apply to these perspectives
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.vwp_emotion_states))
                elif messagelist[0] == 'CHARACTERTRAITS':
                    command = 'CHARACTERTRAITS'
                    # Returns a dictionary with four top level keys:
                    # 1.Implicit: Spans whose perspective is implicitly that of the
                    #   speaker/author
                    # 2. First person: Spans whose perspective is explicitly that of
                    #    the speaker/author, indicated by first person pronouns
                    # 3. Second person: Spans whose perspective is explicitly that of
                    #    the audience, indicated by second person pronouns
                    # 4. Third person: Spans whose perspective is that of some other
                    #    agent. This key has subkeys corresponding to the offsets of
                    #    the noun/proper noun referring to the viewpoint entity.
                    #
                    # Each of these keys is associated with a list of offsets, which
                    # corresponds to character trait predicates that apply to these perspectives
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.vwp_character_traits))
                elif messagelist[0] == 'PROPOSITIONALATTITUDES':
                    command = 'PROPOSITIONALATTITUDES'
                    # Returns a dictionary with four top level keys:
                    # 1.Implicit: Spans whose perspective is implicitly that of the
                    #   speaker/author
                    # 2. First person: Spans whose perspective is explicitly that of
                    #    the speaker/author, indicated by first person pronouns
                    # 3. Second person: Spans whose perspective is explicitly that of
                    #    the audience, indicated by second person pronouns
                    # 4. Third person: Spans whose perspective is that of some other
                    #    agent. This key has subkeys corresponding to the offsets of
                    #    the noun/proper noun referring to the viewpoint entity.
                    #
                    # Each of these keys is associated with a list of offsets, which
                    # corresponds to propositional attitude predicates like think, feel,
                    # or believe, that describe mental states of the entity referred to
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.vwp_propositional_attitudes))
                elif messagelist[0] == 'SOCIAL_AWARENESS':
                    command = 'SOCIAL_AWARENESS'
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.vwp_social_awareness))
                elif messagelist[0] == 'CONCRETEDETAILS':
                    command = 'CONCRETEDETAILS'
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.concrete_details))
                elif messagelist[0] == 'INTERACTIVELANGUAGE':
                    command = 'INTERACTIVELANGUAGE'
                    # 1 interactive cue words 0 other
                    # Returns a list of offsets to tokens that cue a more oral, interactive style
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.vwp_interactives))
                elif messagelist[0] == 'ARGUMENTWORDS':
                    command = 'ARGUMENTWORDS'
                    # 1 argument language 0 other
                    # Returns a list of offsets to tokens that cue a more oral, interactive style
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.vwp_argumentwords))
                elif messagelist[0] == 'ARGUMENTLANGUAGE':
                    command = 'ARGUMENTLANGUAGE'
                    # 1 argument language 0 other
                    # Returns a list of offsets to tokens that cue a more oral, interactive style
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.vwp_arguments))
                elif messagelist[0] == 'EXPLICITARGUMENTWORDS':
                    command = 'ARGUMENTWORDS'
                    # 1 argument language 0 other
                    # Returns a list of offsets to tokens that cue a more oral, interactive style
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.vwp_explicit_arguments))
                elif messagelist[0] == 'SUBJECTIVITYRATINGS':
                    command = 'SUBJECTIVITYRATINGS'
                    # Real number between 0 and 1: tokens that cue subjectivity of the text
                    # (stronger or weaker stance). Position in the list returned equals
                    # position in the document
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.subjectivity_ratings))
                elif messagelist[0] == 'SENTIMENTRATINGS':
                    command = 'SENTIMENTRATINGS'
                    # 1 or 0: tokens that cue positive or negative sentiment poarity
                    # Position in the list returned equals position in the document
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.sentiment_ratings))
                elif messagelist[0] == 'TONERATINGS':
                    command = 'TONERATINGS2'
                    # 1 or 0: tokens that cue positive or negative tone
                    # Position in the list returned equals position in the document
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.tone_ratings))
                elif messagelist[0] == 'POLARITYRATINGS':
                    command = 'POLARITYRATINGS'
                    # Real number betweeen -1 and 1: tokens that cue positive or
                    # negative TextBlob sentiment polarity. Position in the list returned
                    # equals position in the document
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.polarity_ratings))
                elif messagelist[0] == 'ASSESSMENTS':
                    command = 'ASSESSMENTS'
                    # 1 or 0: stance marker tokens identified by SpacyTextBlob
                    # List of word strings
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.assessments))
                elif messagelist[0] == 'PASTTENSESCOPE':
                    command = 'PASTTENSESCOPE'
                    # 1 or 0: whether words are part of past tense clauses
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.pastTenseScope))
                elif messagelist[0] == 'GOVERNINGSUBJECTS':
                    command = 'GOVERNINGSUBJECTS'
                    # offset of the logical subject that governs the domain this token belongs to
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.governing_subjects))
                elif messagelist[0] == 'CLUSTERS':
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps([tok._._tclust for tok in doc]))
                elif messagelist[0] == 'PROMPTLANGUAGE':
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.prompt_language))
                elif messagelist[0] == 'PROMPTRELATED':
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.prompt_related))
                elif messagelist[0] == 'CORESENTENCES':
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.core_sentences))
                elif messagelist[0] == 'EXTENDEDCORESENTENCES':
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.extended_core_sentences))
                elif messagelist[0] == 'CONTENTSEGMENTS':
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.content_segments))
                elif messagelist[0] == 'CLUSTERINFO':
                    command = 'CLUSTERINFO'
                    # Get the local word clusters our algorithm has clustered the words of the student document into
                    #
                    # The data is a list of records in this format:
                    # 1.  The clusterID.
                    # 2.  The cluster rating, which is roughly a measure of how important the cluster seems to be in the document
                    #     as measured by the number of words in it and their relative infrequency
                    # 3.  A list of the actual word strings in each cluster
                    # 4.  The offsets of the words assigned to each cluster
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.clusterInfo))
                elif messagelist[0] == 'DEVWORDS':
                    command = 'DEVWORDS'
                    # offset of the logical subject that governs the domain this token belongs to
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.devwords))
                elif messagelist[0] == 'NOMINALREFERENCES':
                    command = 'NOMINALREFERENCES'
                    # offset of the logical subject that governs the domain this token belongs to
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    await websocket.send(json.dumps(doc._.nominalReferences))
                elif messagelist[0] == 'DOCSUMMARYLABELS':
                    command = 'DOCSUMMARYLABELS'
                    summaryLabels = [\
                    'mean_nSyll',\
                    'med_nSyll',\
                    'max_nSyll',\
                    'min_nSyll',\
                    'std_nSyll',\
                    'mean_sqnChars',\
                    'med_sqnChars',\
                    'max_sqnChars',\
                    'min_sqnChars',\
                    'std_sqnChars',\
                    'propn_latinate',\
                    'propn_academic',\
                    'mean_family_size',\
                    'med_family_size',\
                    'max_family_size',\
                    'min_family_size',\
                    'std_family_size',\
                    'mean_concreteness',\
                    'med_concreteness',\
                    'max_concreteness',\
                    'min_concreteness',\
                    'std_concreteness',\
                    'mean_logNSenses',\
                    'med_logNSenses',\
                    'max_logNSenses',\
                    'min_logNSenses',\
                    'std_logNSenses',\
                    'mean_nMorph',\
                    'med_nMorph',\
                    'max_nMorph',\
                    'min_nMorph',\
                    'std_nMorph',\
                    'mean_logfreq_HAL',\
                    'med_logfreq_HAL',\
                    'max_logfreq_HAL',\
                    'min_logfreq_HAL',\
                    'std_logfreq_HAL',\
                    'mean_root_fam_size',\
                    'med_root_fam_size',\
                    'max_root_fam_size',\
                    'min_root_fam_size',\
                    'std_root_fam_size',\
                    'mean_root_pfmf',\
                    'med_root_pfmf',\
                    'max_root_pfmf',\
                    'min_root_pfmf',\
                    'std_root_pfmf',\
                    'mean_token_frequency',\
                    'median_token_frequency',\
                    'max_token_frequency',\
                    'min_token_frequency',\
                    'std_token_frequency',\
                    'mean_lemma_frequency',\
                    'median_lemma_frequency',\
                    'max_lemma_frequency',\
                    'min_lemma_frequency',\
                    'std_lemma_frequency',\
                    'mean_max_frequency',\
                    'median_max_frequency',\
                    'max_max_frequency',\
                    'min_max_frequency',\
                    'std_max_frequency',\
                    'propn_abstract_traits',\
                    'propn_animates',\
                    'propn_deictics',\
                    'wf_type_count',\
                    'lemma_type_count',\
                    'type_count',\
                    'token_count',\
                    'paragraph_count',\
                    'mean_paragraph_length',\
                    'median_paragraph_length',\
                    'max_paragraph_length',\
                    'min_paragraph_length',\
                    'stdev_paragraph_length',\
                    'total_transition_words',\
                    'transition_category_count',\
                    'transition_word_type_count',\
                    'mean_transition_distance',\
                    'median_transition_distance',\
                    'max_transition_distance',\
                    'min_transition_distance',\
                    'stdev_transition_distance',\
                    'mean_sent_cohesion',\
                    'median_sent_cohesion',\
                    'max_sent_cohesion',\
                    'min_sent_cohesion',\
                    'stdev_sent_cohesion',\
                    'mean_slider_cohesion',\
                    'median_slider_cohesion',\
                    'max_slider_cohesion',\
                    'min_slider_cohesion',\
                    'stdev_slider_cohesion',\
                    'num_corefs',\
                    'mean_coref_chain_len',\
                    'median_coref_chain_len',\
                    'max_coref_chain_len',\
                    'min_coref_chain_len',\
                    'stdev_coref_chain_len',\
                    'sentence_count',\
                    'mean_sentence_len',\
                    'median_sentence_len',\
                    'max_sentence_len',\
                    'min_sentence_len',\
                    'std_sentence_len',\
                    'mean_words_to_sentence_root',\
                    'median_words_to_sentence_root',\
                    'max_words_to_sentence_root',\
                    'min_words_to_sentence_root',\
                    'stdev_words_to_sentence_root',\
                    'meanRhemeDepth',\
                    'medianRhemeDepth',\
                    'maxRhemeDepth',\
                    'minRhemeDepth',\
                    'stdevRhemeDepth',\
                    'meanThemeDepth',\
                    'medianThemeDepth',\
                    'maxThemeDepth',\
                    'minThemeDepth',\
                    'stdevThemeDepth',\
                    'meanWeightedDepth',\
                    'medianWeightedDepth',\
                    'maxWeightedDepth',\
                    'minWeightedDepth',\
                    'stdevWeightedDepth',\
                    'meanWeightedBreadth',\
                    'medianWeightedBreadth',\
                    'maxWeightedBreadth',\
                    'minWeightedBreadth',\
                    'stdevWeightedBreadth',\
                    'syntacticVariety',\
                    'propn_past',\
                    'propn_argument_words',\
                    'propn_direct_speech',\
                    'propn_egocentric',\
                    'propn_allocentric',\
                    'mean_subjectivity',\
                    'median_subjectivity',\
                    'min_subjectivity',\
                    'max_subjectivity',\
                    'stdev_subjectivity',\
                    'mean_polarity',\
                    'median_polarity',\
                    'min_polarity',\
                    'max_polarity',\
                    'stdev_polarity',\
                    'mean_sentiment',\
                    'median_sentiment',\
                    'min_sentiment',\
                    'max_sentiment',\
                    'stdev_sentiment',\
                    'mean_main_cluster_span',\
                    'median_main_cluster_span',\
                    'min_main_cluster_span',\
                    'max_main_cluster_span',\
                    'stdev_main_cluster_span',\
                    'propn_devwords',\
                    'mean_devword_nsyll',\
                    'median_devword_nsyll',\
                    'min_devword_nsyll',\
                    'max_devword_nsyll',\
                    'stdev_devword_nsyll',\
                    'mean_devword_nmorph',\
                    'median_devword_nmorph',\
                    'min_devword_nmorph',\
                    'max_devword_nmorph',\
                    'stdev_devword_nmorph',\
                    'mean_devword_nsenses',\
                    'median_devword_nsenses',\
                    'min_devword_nsenses',\
                    'max_devword_nsenses',\
                    'stdev_devword_nsenses',\
                    'mean_devword_token_freq',\
                    'median_devword_token_freq',\
                    'min_devword_token_freq',\
                    'max_devword_token_freq',\
                    'stdev_devword_token_freq',\
                    'mean_devword_concreteness',\
                    'median_devword_concreteness',\
                    'min_devword_concreteness',\
                    'max_devword_concreteness',\
                    'stdev_devword_concreteness']
                    await websocket.send(json.dumps(summaryLabels))

                elif messagelist[0] == 'DOCSUMMARYFEATS':
                    command = 'DOCSUMMARYFEATS'
                    label = messagelist[1]
                    doc = self.parser.get_document(label)
                    summaryFeats = [\
                        doc._.mean_nSyll,\
                        doc._.med_nSyll,\
                        doc._.max_nSyll,\
                        doc._.min_nSyll,\
                        doc._.std_nSyll, \
                        doc._.mean_sqnChars,\
                        doc._.med_sqnChars,\
                        doc._.max_sqnChars,\
                        doc._.min_sqnChars,\
                        doc._.std_sqnChars,\
                        doc._.propn_latinate,\
                        doc._.propn_academic,\
                        doc._.mean_family_size,\
                        doc._.med_family_size,\
                        doc._.max_family_size,\
                        doc._.min_family_size,\
                        doc._.std_family_size,\
                        doc._.mean_concreteness,\
                        doc._.med_concreteness,\
                        doc._.max_concreteness,\
                        doc._.min_concreteness,\
                        doc._.std_concreteness,\
                        doc._.mean_logNSenses,\
                        doc._.med_logNSenses,\
                        doc._.max_logNSenses,\
                        doc._.min_logNSenses,\
                        doc._.std_logNSenses,\
                        doc._.mean_nMorph,\
                        doc._.med_nMorph,\
                        doc._.max_nMorph,\
                        doc._.min_nMorph,\
                        doc._.std_nMorph,\
                        doc._.mean_logfreq_HAL,\
                        doc._.med_logfreq_HAL,\
                        doc._.max_logfreq_HAL,\
                        doc._.min_logfreq_HAL,\
                        doc._.std_logfreq_HAL,\
                        doc._.mean_root_fam_size,\
                        doc._.med_root_fam_size,\
                        doc._.max_root_fam_size,\
                        doc._.min_root_fam_size,\
                        doc._.std_root_fam_size,\
                        doc._.mean_root_pfmf,\
                        doc._.med_root_pfmf,\
                        doc._.max_root_pfmf,\
                        doc._.min_root_pfmf,\
                        doc._.std_root_pfmf,\
                        doc._.mean_token_frequency,\
                        doc._.median_token_frequency,\
                        doc._.max_token_frequency,\
                        doc._.min_token_frequency,\
                        doc._.std_token_frequency,\
                        doc._.mean_lemma_frequency,\
                        doc._.median_lemma_frequency,\
                        doc._.max_lemma_frequency,\
                        doc._.min_lemma_frequency,\
                        doc._.std_lemma_frequency,\
                        doc._.mean_max_frequency,\
                        doc._.median_max_frequency,\
                        doc._.max_max_frequency,\
                        doc._.min_max_frequency,\
                        doc._.std_max_frequency,\
                        doc._.propn_abstract_traits,\
                        doc._.propn_animates,\
                        doc._.propn_deictics,\
                        doc._.wf_type_count,\
                        doc._.lemma_type_count,\
                        doc._.type_count,\
                        doc._.token_count,\
                        doc._.paragraph_count,\
                        doc._.mean_paragraph_length,\
                        doc._.median_paragraph_length,\
                        doc._.max_paragraph_length,\
                        doc._.min_paragraph_length,\
                        doc._.stdev_paragraph_length,\
                        doc._.total_transition_words,\
                        doc._.transition_category_count,\
                        doc._.transition_word_type_count,\
                        doc._.mean_transition_distance,\
                        doc._.median_transition_distance,\
                        doc._.max_transition_distance,\
                        doc._.min_transition_distance,\
                        doc._.stdev_transition_distance,\
                        doc._.mean_sent_cohesion,\
                        doc._.median_sent_cohesion,\
                        doc._.max_sent_cohesion,\
                        doc._.min_sent_cohesion,\
                        doc._.stdev_sent_cohesion,\
                        doc._.mean_slider_cohesion,\
                        doc._.median_slider_cohesion,\
                        doc._.max_slider_cohesion,\
                        doc._.min_slider_cohesion,\
                        doc._.stdev_slider_cohesion,\
                        doc._.num_corefs,\
                        doc._.mean_coref_chain_len,\
                        doc._.median_coref_chain_len,\
                        doc._.max_coref_chain_len,\
                        doc._.min_coref_chain_len,\
                        doc._.stdev_coref_chain_len,\
                        doc._.sentence_count,\
                        doc._.mean_sentence_len,\
                        doc._.median_sentence_len,\
                        doc._.max_sentence_len,\
                        doc._.min_sentence_len,\
                        doc._.std_sentence_len,\
                        doc._.mean_words_to_sentence_root,\
                        doc._.median_words_to_sentence_root,\
                        doc._.max_words_to_sentence_root,\
                        doc._.min_words_to_sentence_root,\
                        doc._.stdev_words_to_sentence_root,\
                        doc._.meanRhemeDepth,\
                        doc._.medianRhemeDepth,\
                        doc._.maxRhemeDepth,\
                        doc._.minRhemeDepth,\
                        doc._.stdevRhemeDepth,\
                        doc._.meanThemeDepth,\
                        doc._.medianThemeDepth,\
                        doc._.maxThemeDepth,\
                        doc._.minThemeDepth,\
                        doc._.stdevThemeDepth,\
                        doc._.meanWeightedDepth,\
                        doc._.medianWeightedDepth,\
                        doc._.maxWeightedDepth,\
                        doc._.minWeightedDepth,\
                        doc._.stdevWeightedDepth,\
                        doc._.meanWeightedBreadth,\
                        doc._.medianWeightedBreadth,\
                        doc._.maxWeightedBreadth,\
                        doc._.minWeightedBreadth,\
                        doc._.stdevWeightedBreadth,\
                        doc._.syntacticVariety,\
                        doc._.propn_past,\
                        doc._.propn_argument_words,\
                        doc._.propn_direct_speech,\
                        doc._.propn_egocentric,\
                        doc._.propn_allocentric,\
                        doc._.mean_subjectivity,\
                        doc._.median_subjectivity,\
                        doc._.min_subjectivity,\
                        doc._.max_subjectivity,\
                        doc._.stdev_subjectivity,\
                        doc._.mean_polarity,\
                        doc._.median_polarity,\
                        doc._.min_polarity,\
                        doc._.max_polarity,\
                        doc._.stdev_polarity,\
                        doc._.mean_sentiment,\
                        doc._.median_sentiment,\
                        doc._.min_sentiment,\
                        doc._.max_sentiment,\
                        doc._.stdev_sentiment,\
                        doc._.mean_main_cluster_span,\
                        doc._.median_main_cluster_span,\
                        doc._.min_main_cluster_span,\
                        doc._.max_main_cluster_span,\
                        doc._.stdev_main_cluster_span,\
                        doc._.propn_devwords,\
                        doc._.mean_devword_nsyll,\
                        doc._.median_devword_nsyll,\
                        doc._.min_devword_nsyll,\
                        doc._.max_devword_nsyll,\
                        doc._.stdev_devword_nsyll,\
                        doc._.mean_devword_nmorph,\
                        doc._.median_devword_nmorph,\
                        doc._.min_devword_nmorph,\
                        doc._.max_devword_nmorph,\
                        doc._.stdev_devword_nmorph,\
                        doc._.mean_devword_nsenses,\
                        doc._.median_devword_nsenses,\
                        doc._.min_devword_nsenses,\
                        doc._.max_devword_nsenses,\
                        doc._.stdev_devword_nsenses,\
                        doc._.mean_devword_token_freq,\
                        doc._.median_devword_token_freq,\
                        doc._.min_devword_token_freq,\
                        doc._.max_devword_token_freq,\
                        doc._.stdev_devword_token_freq,\
                        doc._.mean_devword_concreteness,\
                        doc._.median_devword_concreteness,\
                        doc._.min_devword_concreteness,\
                        doc._.max_devword_concreteness,\
                        doc._.stdev_devword_concreteness]
                    await websocket.send(json.dumps(summaryFeats))
                else:
                    await websocket.send(json.dumps(False))
                """
                ,\
                """
            except Exception as e:
                print('exception', e, command)
                await websocket.send(json.dumps(None))


if __name__ == '__main__':
    print('parser server loading')
    wsc = parserServer()
