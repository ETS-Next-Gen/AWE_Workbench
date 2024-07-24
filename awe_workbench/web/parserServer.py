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
from awe_components.components.utility_functions import content_pos

class parserServer:

    # Initialize
    parser = None

    def __init__(self, pipeline_def=[]):

        # set up and initializing Holmes
        # Start the Holmes manager with the English model
        # You can try setting overall_similarity_threshold
        # to 0.85 and/or perform_coreference_resolution to False
        self.parser = holmes_extractor.manager.Manager(
            model='en_core_web_lg',
            perform_coreference_resolution=True,
            extra_components=pipeline_def)

        asyncio.get_event_loop().run_until_complete(
            websockets.serve(self.run_parser, 'localhost', 8766, max_size=2 ** 24))
        print('parser running')
        asyncio.get_event_loop().run_forever()
        print('died')

    async def kill(self, websocket):
        self.parser.close()
        await websocket.close()
        exit()

    summaryLabels = [
        'mean_nSyll',
        'med_nSyll',
        'max_nSyll',
        'min_nSyll',
        'std_nSyll',
        'mean_sqnChars',
        'med_sqnChars',
        'max_sqnChars',
        'min_sqnChars',
        'std_sqnChars',
        'propn_latinate',
        'propn_academic',
        'mean_family_size',
        'med_family_size',
        'max_family_size',
        'min_family_size',
        'std_family_size',
        'mean_concreteness',
        'med_concreteness',
        'max_concreteness',
        'min_concreteness',
        'std_concreteness',
        'mean_logNSenses',
        'med_logNSenses',
        'max_logNSenses',
        'min_logNSenses',
        'std_logNSenses',
        'mean_nMorph',
        'med_nMorph',
        'max_nMorph',
        'min_nMorph',
        'std_nMorph',
        'mean_logfreq_HAL',
        'med_logfreq_HAL',
        'max_logfreq_HAL',
        'min_logfreq_HAL',
        'std_logfreq_HAL',
        'mean_root_fam_size',
        'med_root_fam_size',
        'max_root_fam_size',
        'min_root_fam_size',
        'std_root_fam_size',
        'mean_root_pfmf',
        'med_root_pfmf',
        'max_root_pfmf',
        'min_root_pfmf',
        'std_root_pfmf',
        'mean_token_frequency',
        'median_token_frequency',
        'max_token_frequency',
        'min_token_frequency',
        'std_token_frequency',
        'mean_lemma_frequency',
        'median_lemma_frequency',
        'max_lemma_frequency',
        'min_lemma_frequency',
        'std_lemma_frequency',
        'mean_max_frequency',
        'median_max_frequency',
        'max_max_frequency',
        'min_max_frequency',
        'std_max_frequency',
        'propn_abstract_traits',
        'propn_animates',
        'propn_deictics',
        'wf_type_count',
        'lemma_type_count',
        'type_count',
        'token_count',
        'paragraph_count',
        'mean_paragraph_length',
        'median_paragraph_length',
        'max_paragraph_length',
        'min_paragraph_length',
        'stdev_paragraph_length',
        'propn_transition_words',
        'transition_category_count',
        'transition_word_type_count',
        'mean_transition_distance',
        'median_transition_distance',
        'max_transition_distance',
        'min_transition_distance',
        'stdev_transition_distance',
        'mean_sent_cohesion',
        'median_sent_cohesion',
        'max_sent_cohesion',
        'min_sent_cohesion',
        'stdev_sent_cohesion',
        'mean_slider_cohesion',
        'median_slider_cohesion',
        'max_slider_cohesion',
        'min_slider_cohesion',
        'stdev_slider_cohesion',
        'num_corefs',
        'mean_coref_chain_len',
        'median_coref_chain_len',
        'max_coref_chain_len',
        'min_coref_chain_len',
        'stdev_coref_chain_len',
        'sentence_count',
        'mean_sentence_len',
        'median_sentence_len',
        'max_sentence_len',
        'min_sentence_len',
        'std_sentence_len',
        'mean_words_to_sentence_root',
        'median_words_to_sentence_root',
        'max_words_to_sentence_root',
        'min_words_to_sentence_root',
        'stdev_words_to_sentence_root',
        'meanRhemeDepth',
        'medianRhemeDepth',
        'maxRhemeDepth',
        'minRhemeDepth',
        'stdevRhemeDepth',
        'meanThemeDepth',
        'medianThemeDepth',
        'maxThemeDepth',
        'minThemeDepth',
        'stdevThemeDepth',
        'meanWeightedDepth',
        'medianWeightedDepth',
        'maxWeightedDepth',
        'minWeightedDepth',
        'stdevWeightedDepth',
        'meanWeightedBreadth',
        'medianWeightedBreadth',
        'maxWeightedBreadth',
        'minWeightedBreadth',
        'stdevWeightedBreadth',
        'syntacticVariety',
        'propn_past',
        'propn_argument_words',
        'propn_direct_speech',
        'propn_egocentric',
        'propn_allocentric',
        'mean_subjectivity',
        'median_subjectivity',
        'min_subjectivity',
        'max_subjectivity',
        'stdev_subjectivity',
        'mean_polarity',
        'median_polarity',
        'min_polarity',
        'max_polarity',
        'stdev_polarity',
        'mean_sentiment',
        'median_sentiment',
        'min_sentiment',
        'max_sentiment',
        'stdev_sentiment',
        'mean_main_cluster_span',
        'median_main_cluster_span',
        'min_main_cluster_span',
        'max_main_cluster_span',
        'stdev_main_cluster_span',
        'propn_devwords',
        'mean_devword_nsyll',
        'median_devword_nsyll',
        'min_devword_nsyll',
        'max_devword_nsyll',
        'stdev_devword_nsyll',
        'mean_devword_nmorph',
        'median_devword_nmorph',
        'min_devword_nmorph',
        'max_devword_nmorph',
        'stdev_devword_nmorph',
        'mean_devword_nsenses',
        'median_devword_nsenses',
        'min_devword_nsenses',
        'max_devword_nsenses',
        'stdev_devword_nsenses',
        'mean_devword_token_freq',
        'median_devword_token_freq',
        'min_devword_token_freq',
        'max_devword_token_freq',
        'stdev_devword_token_freq',
        'mean_devword_concreteness',
        'median_devword_concreteness',
        'min_devword_concreteness',
        'max_devword_concreteness',
        'stdev_devword_concreteness'
    ]

    async def run_parser(self, websocket, path):
        current_doc = ''
        async for message in websocket:

            messagelist = json.loads(message)
            print(messagelist)
            command = ''
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
                text = current_doc + messagelist[2]
                current_doc = ''
                if label in self.parser.list_document_labels():
                    self.parser.remove_document(label)
                self.parser.parse_and_register_document(text, label)
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(True))
            elif messagelist[0] == 'PARTIALTEXT':
                current_document += messagelist[2]
            elif messagelist[0] == 'PARSESET':
                command = 'PARSESET'
                results = []
                [labels, texts] = messagelist[1]
                for i, text in enumerate(texts):
                    text = texts[i]
                    print('parsed document', str(i+1), 'of', len(texts))
                    if text is not None and len(text) > 0:
                        if labels[i] in self.parser.list_document_labels():
                            self.parser.remove_document(labels[i])
                        self.parser.parse_and_register_document(
                            text, labels[i])
                await websocket.send(json.dumps(True))
            elif messagelist[0] == 'LABELS':
                command = 'LABELS'
                labels = self.parser.list_document_labels()
                await websocket.send(json.dumps(labels))
            elif messagelist[0] == 'SERIALIZED':
                command = 'SERIALIZED'
                label = messagelist[1]
                serialized = base64.b64encode(
                    self.parser.serialize_document(label))
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
                # This search takes a long list of keyword parameters,
                # all of them with preset default thresholds. TBD:
                # expose all of these parameters in more complex topic
                # match functionality. Holmes extractor documentation
                # describes what each of these parameters involves.
                matches = self.parser.topic_match_documents_against(
                    text_to_match,
                    word_embedding_match_threshold=.42,
                    relation_score=20,
                    reverse_only_relation_score=15,
                    single_word_score=10,
                    single_word_any_tag_score=5,
                    different_match_cutoff_score=10,
                    relation_matching_frequency_threshold=0.0,
                    embedding_matching_frequency_threshold=0.0,
                    use_frequency_factor=True)
                await websocket.send(json.dumps(matches))
            # Holmes Extractor also has supervised topic model
            # building facilities using the functions
            # get_supervised_topic_training_basis(),
            # and deserialize_supervised_topic_classifier().
            # TBD: Add support for Holmes supervised topic model
            #      building.
            elif messagelist[0] == 'AWE_INFO':
                label = messagelist[1]
                doc = self.parser.get_document(label)
                indic = None
                itype = None
                summ = None
                filt = None
                if len(messagelist) == 3:
                    indic = messagelist[2]
                    await websocket.send(
                        doc._.AWE_Info(indicator=indic))
                elif len(messagelist) == 4:
                    indic = messagelist[2]
                    itype = messagelist[3]
                    await websocket.send(
                        doc._.AWE_Info(indicator=indic,infoType=itype))
                elif len(messagelist) == 5:
                    indic = messagelist[2]
                    itype = messagelist[3]
                    summ = messagelist[4]
                    result = \
                        doc._.AWE_Info(indicator=indic,infoType=itype,summaryType=summ)
                    if type(result) in [int, float, bool]:
                        await websocket.send(str(result))
                    else:
                        await websocket.send(result)
                                      
                elif len(messagelist) == 6:
                    indic = messagelist[2]
                    itype = messagelist[3]
                    summ = messagelist[4]
                    filt = json.loads(messagelist[5])
                    result = \
                        doc._.AWE_Info(indicator=indic,infoType=itype,summaryType=summ,filters=filt)
                    if type(result) in [int, float]:
                        await websocket.send(str(result))
                    else:
                        await websocket.send(result)
                elif len(messagelist) == 7:
                    indic = messagelist[2]
                    itype = messagelist[3]
                    summ = messagelist[4]
                    filt = json.loads(messagelist[5])
                    trans = json.loads(messagelist[6])
                    result = \
                        doc._.AWE_Info(indicator=indic,infoType=itype,summaryType=summ,filters=filt,transformations=trans)
                    if type(result) in [int, float]:
                        await websocket.send(str(result))
                    else:
                        await websocket.send(result)
                                      
                else:
                    await websocket.send(json.dumps([]))
            elif messagelist[0] == 'DOCTOKENS':
                label = messagelist[1]
                doc = self.parser.get_document(label)
                if doc is not None:
                    await websocket.send(
                        doc._.AWE_Info(indicator='text'))
                else:
                    await websocket.send(json.dumps([]))
            elif messagelist[0] == 'DOCTOKENS_WITH_WS':
                label = messagelist[1]
                doc = self.parser.get_document(label)
                if doc is not None:
                    await websocket.send(
                        doc._.AWE_Info(indicator='text_with_ws'))
                else:
                    await websocket.send(json.dumps([]))
            elif messagelist[0] == 'DOCHEADS':
                command = 'DOCHEADS'
                # Position in the list returned equals position
                # in the document
                label = messagelist[1]
                doc = self.parser.get_document(label)
                heads = [token.head.i for token in doc]
                await websocket.send(json.dumps(heads))
            elif messagelist[0] == 'POS':
                command = 'POS'
                # Position in the list returned equals position
                # in the document
                label = messagelist[1]
                doc = self.parser.get_document(label)
                heads = [token.pos_ for token in doc]
                await websocket.send(json.dumps(heads))
            elif messagelist[0] == 'DOCDEPENDENCIES':
                command = 'DOCDEPENDENCIES'
                # Position in the list returned equals position
                # in the document
                label = messagelist[1]
                doc = self.parser.get_document(label)
                deps = [token.dep_ for token in doc]
                await websocket.send(json.dumps(deps))
            elif messagelist[0] == 'DOCENTITIES':
                command = 'DOCENTITIES'
                # Position in the list returned equals position
                # in the document
                label = messagelist[1]
                doc = self.parser.get_document(label)
                ents = [[ent.text,
                         ent.start_char,
                         ent.end_char,
                         ent.label_] for ent in doc.ents]
                await websocket.send(json.dumps(ents))
            elif messagelist[0] == 'TOKVECS':
                command = 'TOKVECS'
                # List returned contains lists pairing token
                # offset with token vectors cast as strings
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.token_vectors))
            elif messagelist[0] == 'LEMMAS':
                command = 'LEMMAS'
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(
                    doc._.AWE_Info(indicator='lemma_')
                )
            elif messagelist[0] == 'STOPWORDS':
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(
                    doc._.AWE_Info(indicator='is_stop')
                )
            elif messagelist[0] == 'WORDTYPES':
                command = 'WORDTYPES'
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='lower_',filters=[('is_alpha', ['True']),('is_stop', ['False'])],summaryType = 'uniq')
                ))
            elif messagelist[0] == 'ROOTS':
                command = 'ROOTS'
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='root')
                ))
            elif messagelist[0] == 'SYLLABLES':
                command = 'SYLLABLES'
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='nSyll')))
            elif messagelist[0] == 'WORDLENGTH':
                command = 'WORDLENGTH'
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='text', filters=[('is_alpha', ['True'])], transformations=['len', 'sqrt'])
                ))
            elif messagelist[0] == 'LATINATES':
                command = 'LATINATES'
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='is_latinate',filters=[('is_alpha', ['True'])])
                ))
            elif messagelist[0] == 'ACADEMICS':
                command = 'ACADEMICS'
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='is_academic',filters=[('is_alpha', ['True'])])
                ))
            elif messagelist[0] == 'SENSENUMS':
                command = 'SENSENUMS'
                # Position in the list returned equals position
                # in the document
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='nSenses',filters=[('is_alpha', ['True'])])
                ))
            elif messagelist[0] == 'LOGSENSENUMS':
                command = 'LOGSENSENUMS'
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='nSenses',filters=[('is_alpha', ['True'])],transformations=['log'])
                ))
            elif messagelist[0] == 'MORPHOLOGY':
                command = 'MORPHOLOGY'
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='morphology')
                ))
            elif messagelist[0] == 'MORPHNUMS':
                command = 'MORPHNUMS'
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='nMorph',filters=[('is_alpha', ['True'])])
                ))
            elif messagelist[0] == 'HALROOTFREQS':
                command = 'HALROOTFREQS'
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='min_root_freq',filters=[('is_alpha', ['True'])])
                ))
            elif messagelist[0] == 'HALLOGROOTFREQS':
                command = 'HALLOGROOTFREQS'
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='min_root_freq',filters=[('is_alpha', ['True'])],transformations=['log'])
                ))
            elif messagelist[0] == 'ROOTFAMSIZES':
                command = 'ROOTFAMSIZES'
                # Position in the list returned equals position
                # in the document
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='root_famSize',filters=[('is_alpha', ['True'])])
                ))
            elif messagelist[0] == 'ROOTPFMFS':
                command = 'ROOTPFMFS'
                # Position in the list returned equals position
                # in the document
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='root_pfmf',filters=[('is_alpha', ['True'])])
                ))
            elif messagelist[0] == 'FAMILYSIZES':
                command = 'FAMILYSIZES'
                # Position in the list returned equals position
                # in the document
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='family_size',filters=[('is_alpha', ['True'])])
                ))
            elif messagelist[0] == 'TOKFREQS':
                command = 'TOKFREQS'
                # Position in the list returned equals position
                # in the document
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='token_freq',filters=[('is_alpha', ['True'])])
                ))
            elif messagelist[0] == 'LEMMAFREQS':
                command = 'LEMMAfREQS'
                # Position in the list returned equals position
                # in the document
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='lemma_freq')))
            elif messagelist[0] == 'ROOTFREQS':
                command = 'ROOTFREQS'
                # Position in the list returned equals position
                # in the document
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='root_Freq')))
            elif messagelist[0] == 'MAXFREQS':
                command = 'MAXFREQS'
                # Position in the list returned equals position
                # in the document
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='max_freq')))
            elif messagelist[0] == 'CONCRETES':
                command = 'CONCRETES'
                # Position in the list returned equals position
                # in the document
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='concreteness')))
            elif messagelist[0] == 'ABSTRACTTRAITS':
                command = 'ABSTRACTTRAITS'
                # Position in the list returned equals position
                # in the document. Flag 1 if the word names an
                # abstract trait, 0 otherwise
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='abstract_trait')))
            elif messagelist[0] == 'ANIMATES':
                command = 'ANIMATES'
                # Position in the list returned equals position
                # in the document. Flag 1 if the word names an animate
                # entity, 0 otherwise
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='animate')))
            elif messagelist[0] == 'LOCATIONS':
                command = 'LOCATIONS'
                # Position in the list returned equals position
                # in the document. Flag 1 if the word names an
                # animate entity, 0 otherwise
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='location')))
            elif messagelist[0] == 'DEICTICS':
                command = 'DEICTICS'
                # Position in the list returned equals position in
                # the document. Flag 1 if the word names a deictic
                # element, 0 otherwise
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='deictic')))
            elif messagelist[0] == 'PARAGRAPHS':
                command = 'PARAGRAPHS'
                # Items in the list indicate word offsets in the document
                # at which paragraph breaks appear
                label = messagelist[1]
                doc = self.parser.get_document(label)
                                    
                await websocket.send(json.dumps(
                    doc._.AWE_Info(infoType="Doc",indicator='delimiter_n')
                ))
                    # doc._.paragraph_breaks))
            elif messagelist[0] == 'SENTENCES':
                command = 'SENTENCES'
                # Items in the list indicate word offsets in the document
                # at which paragraph breaks appear
                label = messagelist[1]
                doc = self.parser.get_document(label)
                
                await websocket.send(json.dumps(
                    doc._.AWE_Info(infoType="Doc",indicator='sents')
                ))
                #await websocket.send(json.dumps(
                #    [(sent.start, sent.end) for sent in doc.sents]))
            elif messagelist[0] == 'PARAGRAPHLENS':
                command = 'PARAGRAPHLENS'
                # Items in the list indicate lengths of paragraphs listed
                # by offset in GETPARAGRAPHS
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(infoType="Doc",indicator='sents',transformations=['tokenlen'])
                ))
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
                await websocket.send(json.dumps(
                    doc._.transition_word_profile))
            elif messagelist[0] == 'TRANSITIONS':
                command = 'TRANSITIONS'
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(infoType='Doc',indicator='transitions')
                ))
            elif messagelist[0] == 'TRANSITIONDISTANCES':
                command = 'TRANSITIONDISTANCES'
                # List of cosine distances between ten-word windows
                # before and after a transition
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(infoType='Doc',indicator='transition_distances')
                ))
            elif messagelist[0] == 'SENTENCECOHESIONS':
                command = 'SENTENCECOHESIONS'
                # List of cosine distances between ten-word windows
                # before and after a sentence boundary
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(infoType='Doc',indicator='intersentence_cohesions')
                ))
            elif messagelist[0] == 'SLIDERCOHESIONS':
                command = 'SLIDERCOHESIONS'
                # List of cosine distances between ten-word windows
                # before and after a sliding window through the text
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(infoType='Doc',indicator='sliding_window_cohesions')
                ))
            elif messagelist[0] == 'COREFCHAINS':
                command = 'COREFCHAINS'
                # List of coreference chains found in document
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.coref_chains))
            elif messagelist[0] == 'RHEMEDEPTHS':
                command = 'RHEMEDEPTHS'
                # Syntactic depth of the sentence rheme -- part of
                # sentence after the main verb where new information
                # is usually placed
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(infoType='Doc',indicator='syntacticDepthsOfRhemes')
                ))
            elif messagelist[0] == 'THEMEDEPTHS':
                command = 'THEMEDEPTHS'
                # Syntactic depth of the sentence theme -- part
                # of sentence before the main verb where given
                # information is usually placed
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='syntacticDepthsOfThemes')
                ))
            elif messagelist[0] == 'WEIGHTEDDEPTHS':
                command = 'WEIGHTEDDEPTHS'
                # Syntactic depth weighted to penalize
                # left-embedded structures
                # that tend to be harder to process
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='weightedSyntacticDepths')
                ))
            elif messagelist[0] == 'WEIGHTEDBREADTHS':
                command = 'WEIGHTEDBREADTHS'
                # Syntactic breadth -- measure of extent to which sentence
                # structure is additive, consisting of coordinated
                # structures and loosely appended modifiers typical of
                # spoken, often unplanned sentence production
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='weightedSyntacticBreadths')
                ))
            elif messagelist[0] == 'SENTENCETYPES':
                # tuple giving number and location of sentence types
                # format:
                # (1,1,1,1,[1,2,3,4]) would be the record for a text that
                # had four sentences -- simple sentence, compound sentence,
                # complex sentence, and compound/complex sentence, in
                # that order.
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(infoType='Doc',indicator='sentence_types')
                ))
            elif messagelist[0] == 'SYNTACTICPROFILE':
                command = 'SYNTACTICPROFILE'
                # Returns a dictionary containing frequency information
                # about the syntactic relations and categories in the text.
                # This includes information about the frequency of parts
                # of speech, morphological categories, and syntactic
                # dependencies between specific parts of speech.
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.syntacticProfile))
            elif messagelist[0] == 'NORMEDSYNTACTICPROFILE':
                command = 'NORMEDSYNTACTICPROFILE'
                # Returns a dictionary containing normalized
                # frequency information (proportionas) for the
                # syntactic relations and categories in the text.
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.syntacticProfileNormed))
            elif messagelist[0] == 'QUOTEDTEXT':
                command = 'QUOTEDTEXT'
                # 1 for tokens within quotation marks, 0 for other text
                # Position in the list corresponds to offset of token
                # in the document
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='vwp_quoted')
                ))
            elif messagelist[0] == 'DIRECTSPEECHSPANS':
                command = 'DIRECTSPEECHSPANS'
                # Data about subset of quoted text -- specifically,
                # quoted text that is attributed to a specific
                # speaker.
                #
                # Returns a list of lists with three top level
                # elements:
                #
                # 1. Speaker: a list of offsets to tokens
                #    referring to the speaker(s)
                # 2. Addressee: a list of offsets to tokens
                #    referring to the person(s) spoken to.
                # 3. Span start offset
                # 4. Span end offset.
                #
                # Note that first and second person pronouns
                # inside direct speech may reference a person
                # explicitly identified in the direct speech
                # framing text. Coreferee reference resolution
                # may apply, so that the speaker and addressee
                # references may be to a proper noun at the head
                # of a pronominal reference chain that includes
                # the direct speech frame.
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(infoType="Doc",indicator='vwp_direct_speech')
                ))
            elif messagelist[0] == 'IN_DIRECT_SPEECH':
                # 1 for tokens within quoted stretches of direct speech,
                # 0 for other text. Position in the list corresponds to
                # offset of token in the document
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='vwp_in_direct_speech')
                ))
            elif messagelist[0] == 'TENSECHANGES':
                # list of positions where tense changed in the main
                # document flow (not in direct speech/quotations,
                # with flag to indicate whether shift was to past
                # tense or to present tense.
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.vwp_tense_changes))
            elif messagelist[0] == 'PERSPECTIVES':
                # list of positions where perspective is indicated
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='vwp_perspective')
                ))
            elif messagelist[0] == 'ATTRIBUTIONS':
                # list of positions where attribution is indicated
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='vwp_attribution')
                ))
            elif messagelist[0] == 'SOURCES':
                # list of positions where source is indicated
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='vwp_source')
                ))
            elif messagelist[0] == 'CITES':
                # list of positions where source is indicated
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='vwp_cite')
                ))
            elif messagelist[0] == 'STATEMENTSOFFACT':
                # list of positions where source is indicated
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(infoType="Doc",indicator='vwp_statements_of_fact')
                ))
            elif messagelist[0] == 'STATEMENTSOFOPINION':
                # list of positions where source is indicated
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(infoType="Doc",indicator='vwp_statements_of_opinion')
                ))
            elif messagelist[0] == 'PERSPECTIVESPANS':
                command = 'PERSPECTIVESPANS'
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.vwp_perspective_spans))
                await websocket.send(
                    doc._.AWE_Info(infoType="Doc",indicator='vwp_perspective_spans')
                )
            elif messagelist[0] == 'STANCEMARKERS':
                command = 'STANCEMARKERS'
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(doc._.vwp_stance_markers))
                await websocket.send(
                    doc._.AWE_Info(infoType="Doc",indicator='vwp_stance_markers')
                )

            elif messagelist[0] == 'CLAIMTEXTS':
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='vwp_claim')
                ))

            elif messagelist[0] == 'DISCUSSIONTEXTS':
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='vwp_discussion')
                ))

            elif messagelist[0] == 'EMOTIONWORDS':
                command = 'EMOTIONWORDS'
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='vwp_emotionword')
                ))

            elif messagelist[0] == 'CHARACTERWORDS':
                command = 'CHARACTERWORDS'
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='vwp_character_traits')
                ))

            elif messagelist[0] == 'EMOTIONALSTATES':
                command = 'EMOTIONALSTATES'
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(
                    doc._.AWE_Info(infoType="Doc",indicator='vwp_emotion_states')
                )
            elif messagelist[0] == 'CHARACTERTRAITS':
                command = 'CHARACTERTRAITS'
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.vwp_character_traits))
            elif messagelist[0] == 'PROPOSITIONALATTITUDES':
                command = 'PROPOSITIONALATTITUDES'
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(infoType="Doc",indicator='vwp_propositional_attitudes')
                ))
            elif messagelist[0] == 'SOCIAL_AWARENESS':
                command = 'SOCIAL_AWARENESS'
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(infoType="Doc",indicator='vwp_social_awareness')
                ))
            elif messagelist[0] == 'CONCRETEDETAILS':
                command = 'CONCRETEDETAILS'
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(
                    doc._.AWE_Info(indicator='concrete_detail')
                )
            elif messagelist[0] == 'INTERACTIVELANGUAGE':
                command = 'INTERACTIVELANGUAGE'
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='vwp_interactive')
                ))
            elif messagelist[0] == 'ARGUMENTWORDS':
                command = 'ARGUMENTWORDS'
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='vwp_argumentword')
                ))
            elif messagelist[0] == 'ARGUMENTLANGUAGE':
                command = 'ARGUMENTLANGUAGE'
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='vwp_argumentation')
                ))
            elif messagelist[0] == 'EXPLICITARGUMENTWORDS':
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='vwp_explicit_argument')
                ))
            elif messagelist[0] == 'SUBJECTIVITYRATINGS':
                command = 'SUBJECTIVITYRATINGS'
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(                    
                    doc._.AWE_Info(indicator='subjectivity')
                ))
            elif messagelist[0] == 'SENTIMENTRATINGS':
                command = 'SENTIMENTRATINGS'
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(                    
                    doc._.AWE_Info(indicator='vwp_sentiment')
                ))
            elif messagelist[0] == 'TONERATINGS':
                command = 'TONERATINGS2'
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(                    
                    doc._.AWE_Info(indicator='vwp_tone')
                ))
            elif messagelist[0] == 'POLARITYRATINGS':
                command = 'POLARITYRATINGS'
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(                    
                    doc._.AWE_Info(indicator='polarity')
                ))
            elif messagelist[0] == 'ASSESSMENTS':
                command = 'ASSESSMENTS'
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(doc._.assessments))
            elif messagelist[0] == 'PASTTENSESCOPE':
                command = 'PASTTENSESCOPE'
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='in_past_tense_scope')
                ))
            elif messagelist[0] == 'GOVERNINGSUBJECTS':
                command = 'GOVERNINGSUBJECTS'
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='governing_subject')
                ))
            elif messagelist[0] == 'CLUSTERS':
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='clusterID')
                ))
            elif messagelist[0] == 'PROMPTLANGUAGE':
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(doc._.prompt_language))
            elif messagelist[0] == 'PROMPTRELATED':
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(doc._.prompt_related))
            elif messagelist[0] == 'MAINIDEAS':
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(
                    doc._.AWE_Info(infoType="Doc",indicator='main_ideas')
                )
            elif messagelist[0] == 'SUPPORTINGIDEAS':
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(
                    doc._.AWE_Info(infoType="Doc",indicator='supporting_ideas')
                )
            elif messagelist[0] == 'SUPPORTINGDETAILS':
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(
                    doc._.AWE_Info(infoType="Doc",indicator='supporting_details')
                )
            elif messagelist[0] == 'CLUSTERINFO':
                command = 'CLUSTERINFO'
                # Get the local word clusters our algorithm has
                # clustered the words of the student document into
                #
                # The data is a list of records in this format:
                # 1.  The clusterID.
                # 2.  The cluster rating, which is roughly a measure
                #     of how important the cluster seems to be in the
                #     docyument as measured by the number of words in it
                #     and their relative infrequency
                # 3.  A list of the actual word strings in each cluster
                # 4.  The offsets of the words assigned to each cluster
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(doc._.clusterInfo))
            elif messagelist[0] == 'DEVWORDS':
                command = 'DEVWORDS'
                # offset of the logical subject that governs
                # the domain this token belongs to
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(
                    doc._.AWE_Info(indicator='devword')
                ))
            elif messagelist[0] == 'NOMINALREFERENCES':
                command = 'NOMINALREFERENCES'
                # offset of the logical subject that governs
                # the domain this token belongs to
                label = messagelist[1]
                doc = self.parser.get_document(label)
                await websocket.send(json.dumps(doc._.nominalReferences))
            elif messagelist[0] == 'DOCSUMMARYLABELS':
                command = 'DOCSUMMARYLABELS'
                await websocket.send(json.dumps(self.summaryLabels))
            elif messagelist[0] == 'DOCSUMMARYFEATS':
                command = 'DOCSUMMARYFEATS'
                label = messagelist[1]
                doc = self.parser.get_document(label)
                summaryFeats = [
                    doc._.AWE_Info(indicator='nSyll',summaryType="mean"),
                    doc._.AWE_Info(indicator='nSyll',summaryType="median"),
                    doc._.AWE_Info(indicator='nSyll',summaryType="max"),
                    doc._.AWE_Info(indicator='nSyll',summaryType="min"),
                    doc._.AWE_Info(indicator='nSyll',summaryType="stdev"),
                    doc._.AWE_Info(indicator='text', filters=[('is_alpha', ['True'])], transformations=['len', 'sqrt'], summaryType='mean'),
                    doc._.AWE_Info(indicator='text', filters=[('is_alpha', ['True'])], transformations=['len', 'sqrt'], summaryType='median'),
                    doc._.AWE_Info(indicator='text', filters=[('is_alpha', ['True'])], transformations=['len', 'sqrt'], summaryType='max'),
                    doc._.AWE_Info(indicator='text', filters=[('is_alpha', ['True'])], transformations=['len', 'sqrt'], summaryType='min'),
                    doc._.AWE_Info(indicator='text', filters=[('is_alpha', ['True'])], transformations=['len', 'sqrt'], summaryType='stdev'),
                    doc._.AWE_Info(indicator='is_latinate',filters=[('is_alpha', ['True'])], summaryType="proportion"),
                    doc._.AWE_Info(indicator='is_academic',filters=[('is_alpha', ['True'])], summaryType="proportion"),
                    doc._.AWE_Info(indicator='family_size', filters=[('is_alpha', ['True'])], summaryType='mean'),
                    doc._.AWE_Info(indicator='family_size', filters=[('is_alpha', ['True'])], summaryType='median'),
                    doc._.AWE_Info(indicator='family_size', filters=[('is_alpha', ['True'])], summaryType='max'),
                    doc._.AWE_Info(indicator='family_size', filters=[('is_alpha', ['True'])], summaryType='min'),
                    doc._.AWE_Info(indicator='family_size', filters=[('is_alpha', ['True'])], summaryType='stdev'),
                    doc._.AWE_Info(indicator='concreteness', filters=[('is_alpha', ['True'])], summaryType='mean'),
                    doc._.AWE_Info(indicator='concreteness', filters=[('is_alpha', ['True'])], summaryType='median'),
                    doc._.AWE_Info(indicator='concreteness', filters=[('is_alpha', ['True'])], summaryType='max'),
                    doc._.AWE_Info(indicator='concreteness', filters=[('is_alpha', ['True'])], summaryType='min'),
                    doc._.AWE_Info(indicator='concreteness', filters=[('is_alpha', ['True'])], summaryType='stdev'),
                    doc._.AWE_Info(indicator='nSenses', filters=[('is_alpha', ['True'])], transformations=['log'], summaryType='mean'),
                    doc._.AWE_Info(indicator='nSenses', filters=[('is_alpha', ['True'])], transformations=['log'], summaryType='median'),
                    doc._.AWE_Info(indicator='nSenses', filters=[('is_alpha', ['True'])], transformations=['log'], summaryType='max'),
                    doc._.AWE_Info(indicator='nSenses', filters=[('is_alpha', ['True'])], transformations=['log'], summaryType='min'),
                    doc._.AWE_Info(indicator='nSenses', filters=[('is_alpha', ['True'])], transformations=['log'], summaryType='stdev'),
                    doc._.AWE_Info(indicator='nMorph', filters=[('is_alpha', ['True'])], summaryType='mean'),
                    doc._.AWE_Info(indicator='nMorph', filters=[('is_alpha', ['True'])], summaryType='median'),
                    doc._.AWE_Info(indicator='nMorph', filters=[('is_alpha', ['True'])], summaryType='max'),
                    doc._.AWE_Info(indicator='nMorph', filters=[('is_alpha', ['True'])], summaryType='min'),
                    doc._.AWE_Info(indicator='nMorph', filters=[('is_alpha', ['True'])], summaryType='stdev'),
                    doc._.AWE_Info(indicator='min_root_freq',filters=[('is_alpha', ['True'])],transformations=['log'],summaryType='mean'),
                    doc._.AWE_Info(indicator='min_root_freq',filters=[('is_alpha', ['True'])],transformations=['log'],summaryType='median'),
                    doc._.AWE_Info(indicator='min_root_freq',filters=[('is_alpha', ['True'])],transformations=['log'],summaryType='max'),
                    doc._.AWE_Info(indicator='min_root_freq',filters=[('is_alpha', ['True'])],transformations=['log'],summaryType='min'),
                    doc._.AWE_Info(indicator='min_root_freq',filters=[('is_alpha', ['True'])],transformations=['log'],summaryType='stdev'),
                    doc._.AWE_Info(indicator='root_famSize',filters=[('is_alpha', ['True'])],summaryType='mean'),
                    doc._.AWE_Info(indicator='root_famSize',filters=[('is_alpha', ['True'])],summaryType='median'),
                    doc._.AWE_Info(indicator='root_famSize',filters=[('is_alpha', ['True'])],summaryType='max'),
                    doc._.AWE_Info(indicator='root_famSize',filters=[('is_alpha', ['True'])],summaryType='min'),
                    doc._.AWE_Info(indicator='root_famSize',filters=[('is_alpha', ['True'])],summaryType='stdev'),
                    doc._.AWE_Info(indicator='root_pfmf',filters=[('is_alpha', ['True'])],summaryType='mean'),
                    doc._.AWE_Info(indicator='root_pfmf',filters=[('is_alpha', ['True'])],summaryType='median'),
                    doc._.AWE_Info(indicator='root_pfmf',filters=[('is_alpha', ['True'])],summaryType='max'),
                    doc._.AWE_Info(indicator='root_pfmf',filters=[('is_alpha', ['True'])],summaryType='min'),
                    doc._.AWE_Info(indicator='root_pfmf',filters=[('is_alpha', ['True'])],summaryType='stdev'),
                    doc._.AWE_Info(indicator='token_freq',filters=[('is_alpha', ['True'])],summaryType='mean'),
                    doc._.AWE_Info(indicator='token_freq',filters=[('is_alpha', ['True'])],summaryType='median'),
                    doc._.AWE_Info(indicator='token_freq',filters=[('is_alpha', ['True'])],summaryType='max'),
                    doc._.AWE_Info(indicator='token_freq',filters=[('is_alpha', ['True'])],summaryType='min'),
                    doc._.AWE_Info(indicator='token_freq',filters=[('is_alpha', ['True'])],summaryType='stdev'),
                    doc._.AWE_Info(indicator='lemma_freq',filters=[('is_alpha', ['True'])],summaryType='mean'),
                    doc._.AWE_Info(indicator='lemma_freq',filters=[('is_alpha', ['True'])],summaryType='median'),
                    doc._.AWE_Info(indicator='lemma_freq',filters=[('is_alpha', ['True'])],summaryType='max'),
                    doc._.AWE_Info(indicator='lemma_freq',filters=[('is_alpha', ['True'])],summaryType='min'),
                    doc._.AWE_Info(indicator='lemma_freq',filters=[('is_alpha', ['True'])],summaryType='stdev'),
                    doc._.AWE_Info(indicator='max_freq',summaryType='mean'),
                    doc._.AWE_Info(indicator='max_freq',summaryType='median'),
                    doc._.AWE_Info(indicator='max_freq',summaryType='max'),
                    doc._.AWE_Info(indicator='max_freq',summaryType='min'),
                    doc._.AWE_Info(indicator='max_freq',summaryType='stdev'),
                    doc._.AWE_Info(indicator='abstract_trait',filters=[('is_alpha', ['True'])], summaryType="proportion"),
                    doc._.AWE_Info(indicator='animate',filters=[('is_alpha', ['True'])], summaryType="proportion"),
                    doc._.AWE_Info(indicator='deictic',filters=[('is_alpha', ['True'])], summaryType="proportion"),
                    doc._.AWE_Info(indicator='root', filters=[('is_alpha', ['True']),('is_stop', ['False']),('pos_', content_pos)], summaryType = 'total'),
                    doc._.AWE_Info(indicator='lemma_', filters=[('is_alpha', ['True']),('is_stop', ['False']),('pos_', content_pos)], summaryType = 'total'),
                    doc._.AWE_Info(indicator='lower_', filters=[('is_alpha', ['True']),('is_stop', ['False']),('pos_', content_pos)], summaryType = 'total'),
                    doc._.AWE_Info(indicator='text', filters=[('is_alpha', ['True']),('is_stop', ['False']),('pos_', content_pos)], summaryType = 'total'),
                    doc._.AWE_Info(infoType="Doc",indicator='delimiter_n',summaryType='total'),
                    doc._.AWE_Info(infoType="Doc",indicator='sents',transformations=['tokenlen'],summaryType='mean'),
                    doc._.AWE_Info(infoType="Doc",indicator='sents',transformations=['tokenlen'],summaryType='median'),
                    doc._.AWE_Info(infoType="Doc",indicator='sents',transformations=['tokenlen'],summaryType='max'),
                    doc._.AWE_Info(infoType="Doc",indicator='sents',transformations=['tokenlen'],summaryType='min'),
                    doc._.AWE_Info(infoType="Doc",indicator='sents',transformations=['tokenlen'],summaryType='stdev'),
                    doc._.AWE_Info(infoType="Doc",indicator='transitions',summaryType='proportion'),
                    doc._.AWE_Info(infoType="Doc",indicator='transitions',summaryType='total'),
                    doc._.AWE_Info(infoType="Doc",indicator='transitions',transformations=['text'],summaryType='counts'),
                    doc._.AWE_Info(infoType="Doc",indicator='transition_distances',summaryType='mean'),
                    doc._.AWE_Info(infoType="Doc",indicator='transition_distances',summaryType='median'),
                    doc._.AWE_Info(infoType="Doc",indicator='transition_distances',summaryType='max'),
                    doc._.AWE_Info(infoType="Doc",indicator='transition_distances',summaryType='min'),
                    doc._.AWE_Info(infoType="Doc",indicator='transition_distances',summaryType='stdev'),
                    doc._.AWE_Info(infoType="Doc",indicator='intersentence_cohesions',summaryType='mean'),
                    doc._.AWE_Info(infoType="Doc",indicator='intersentence_cohesions',summaryType='median'),
                    doc._.AWE_Info(infoType="Doc",indicator='intersentence_cohesions',summaryType='max'),
                    doc._.AWE_Info(infoType="Doc",indicator='intersentence_cohesions',summaryType='min'),
                    doc._.AWE_Info(infoType="Doc",indicator='intersentence_cohesions',summaryType='stdev'),
                    doc._.AWE_Info(infoType="Doc",indicator='sliding_window_cohesions',summaryType='mean'),
                    doc._.AWE_Info(infoType="Doc",indicator='sliding_window_cohesions',summaryType='median'),
                    doc._.AWE_Info(infoType="Doc",indicator='sliding_window_cohesions',summaryType='max'),
                    doc._.AWE_Info(infoType="Doc",indicator='sliding_window_cohesions',summaryType='min'),
                    doc._.AWE_Info(infoType="Doc",indicator='sliding_window_cohesions',summaryType='stdev'),
                    doc._.AWE_Info(infoType="Doc",indicator='corefChainInfo',summaryType='counts'),
                    doc._.AWE_Info(infoType="Doc",indicator='corefChainInfo',transformations=['len'],summaryType='mean'),
                    doc._.AWE_Info(infoType="Doc",indicator='corefChainInfo',transformations=['len'],summaryType='median'),
                    doc._.AWE_Info(infoType="Doc",indicator='corefChainInfo',transformations=['len'],summaryType='max'),
                    doc._.AWE_Info(infoType="Doc",indicator='corefChainInfo',transformations=['len'],summaryType='min'),
                    doc._.AWE_Info(infoType="Doc",indicator='corefChainInfo',transformations=['len'],summaryType='stdev'),
                    doc._.AWE_Info(infoType="Doc",indicator='sents',summaryType='counts'),
                    doc._.AWE_Info(infoType="Doc",indicator='sents',transformations=['len'],summaryType='mean'),
                    doc._.AWE_Info(infoType="Doc",indicator='sents',transformations=['len'],summaryType='median'),
                    doc._.AWE_Info(infoType="Doc",indicator='sents',transformations=['len'],summaryType='max'),
                    doc._.AWE_Info(infoType="Doc",indicator='sents',transformations=['len'],summaryType='min'),
                    doc._.AWE_Info(infoType="Doc",indicator='sents',transformations=['len'],summaryType='stdev'),
                    doc._.AWE_Info(infoType="Doc",indicator='sentenceThemes',transformations=['tokenlen'],summaryType='mean'),
                    doc._.AWE_Info(infoType="Doc",indicator='sentenceThemes',transformations=['tokenlen'],summaryType='median'),
                    doc._.AWE_Info(infoType="Doc",indicator='sentenceThemes',transformations=['tokenlen'],summaryType='max'),
                    doc._.AWE_Info(infoType="Doc",indicator='sentenceThemes',transformations=['tokenlen'],summaryType='min'),
                    doc._.AWE_Info(infoType="Doc",indicator='sentenceThemes',transformations=['tokenlen'],summaryType='stdev'),
                    doc._.AWE_Info(infoType="Doc",indicator='syntacticDepthsOfRhemes',summaryType='mean'),
                    doc._.AWE_Info(infoType="Doc",indicator='syntacticDepthsOfRhemes',summaryType='median'),
                    doc._.AWE_Info(infoType="Doc",indicator='syntacticDepthsOfRhemes',summaryType='max'),
                    doc._.AWE_Info(infoType="Doc",indicator='syntacticDepthsOfRhemes',summaryType='min'),
                    doc._.AWE_Info(infoType="Doc",indicator='syntacticDepthsOfRhemes',summaryType='stdev'),
                    doc._.AWE_Info(infoType="Doc",indicator='syntacticDepthsOfThemes',summaryType='mean'),
                    doc._.AWE_Info(infoType="Doc",indicator='syntacticDepthsOfThemes',summaryType='median'),
                    doc._.AWE_Info(infoType="Doc",indicator='syntacticDepthsOfThemes',summaryType='max'),
                    doc._.AWE_Info(infoType="Doc",indicator='syntacticDepthsOfThemes',summaryType='min'),
                    doc._.AWE_Info(infoType="Doc",indicator='syntacticDepthsOfThemes',summaryType='stdev'),
                    doc._.AWE_Info(indicator='weightedSyntacticDepth',summaryType='mean'),
                    doc._.AWE_Info(indicator='weightedSyntacticDepth',summaryType='median'),
                    doc._.AWE_Info(indicator='weightedSyntacticDepth',summaryType='max'),
                    doc._.AWE_Info(indicator='weightedSyntacticDepth',summaryType='min'),
                    doc._.AWE_Info(indicator='weightedSyntacticDepth',summaryType='stdev'),
                    doc._.AWE_Info(indicator='weightedSyntacticBreadth',summaryType='mean'),
                    doc._.AWE_Info(indicator='weightedSyntacticBreadth',summaryType='median'),
                    doc._.AWE_Info(indicator='weightedSyntacticBreadth',summaryType='max'),
                    doc._.AWE_Info(indicator='weightedSyntacticBreadth',summaryType='min'),
                    doc._.AWE_Info(indicator='weightedSyntacticBreadth',summaryType='stdev'),
                    doc._.syntacticVariety,
                    doc._.AWE_Info(indicator='in_past_tense_scope',summaryType='proportion'),
                    doc._.AWE_Info(indicator='vwp_argumentation',summaryType='proportion'),
                    doc._.AWE_Info(infoType="Doc",indicator='vwp_direct_speech',summaryType='proportion'),
                    doc._.AWE_Info(indicator='vwp_egocentric',summaryType='proportion'),
                    doc._.AWE_Info(indicator='vwp_allocentric',summaryType='proportion'),
                    doc._.AWE_Info(indicator='subjectivity',summaryType='mean'),
                    doc._.AWE_Info(indicator='subjectivity',summaryType='median'),
                    doc._.AWE_Info(indicator='subjectivity',summaryType='min'),
                    doc._.AWE_Info(indicator='subjectivity',summaryType='max'),
                    doc._.AWE_Info(indicator='subjectivity',summaryType='stdev'),
                    doc._.AWE_Info(indicator='polarity',summaryType='mean'),
                    doc._.AWE_Info(indicator='polarity',summaryType='median'),
                    doc._.AWE_Info(indicator='polarity',summaryType='min'),
                    doc._.AWE_Info(indicator='polarity',summaryType='max'),
                    doc._.AWE_Info(indicator='polarity',summaryType='stdev'),
                    doc._.AWE_Info(indicator='vwp_sentiment',summaryType='mean'),
                    doc._.AWE_Info(indicator='vwp_sentiment',summaryType='median'),
                    doc._.AWE_Info(indicator='vwp_sentiment',summaryType='min'),
                    doc._.AWE_Info(indicator='vwp_sentiment',summaryType='max'),
                    doc._.AWE_Info(indicator='vwp_sentiment',summaryType='stdev'),
                    doc._.AWE_Info(infoType="Doc",indicator='main_cluster_spans',transformations=['len'],summaryType='mean'),
                    doc._.AWE_Info(infoType="Doc",indicator='main_cluster_spans',transformations=['len'],summaryType='median'),
                    doc._.AWE_Info(infoType="Doc",indicator='main_cluster_spans',transformations=['len'],summaryType='min'),
                    doc._.AWE_Info(infoType="Doc",indicator='main_cluster_spans',transformations=['len'],summaryType='max'),
                    doc._.AWE_Info(infoType="Doc",indicator='main_cluster_spans',transformations=['len'],summaryType='stdev'),
                    doc._.AWE_Info(indicator='devword', summaryType='proportion'),
                    doc._.AWE_Info(indicator='nSyll', filters=[('is_alpha', ['True']),('devword', ['True'])], summaryType='mean'),
                    doc._.AWE_Info(indicator='nSyll', filters=[('is_alpha', ['True']),('devword', ['True'])], summaryType='median'),
                    doc._.AWE_Info(indicator='nSyll', filters=[('is_alpha', ['True']),('devword', ['True'])], summaryType='min'),
                    doc._.AWE_Info(indicator='nSyll', filters=[('is_alpha', ['True']),('devword', ['True'])], summaryType='max'),
                    doc._.AWE_Info(indicator='nSyll', filters=[('is_alpha', ['True']),('devword', ['True'])], summaryType='stdev'),
                    doc._.AWE_Info(indicator='nMorph', filters=[('is_alpha', ['True']),('devword', ['True'])], summaryType='mean'),
                    doc._.AWE_Info(indicator='nMorph', filters=[('is_alpha', ['True']),('devword', ['True'])], summaryType='median'),
                    doc._.AWE_Info(indicator='nMorph', filters=[('is_alpha', ['True']),('devword', ['True'])], summaryType='min'),
                    doc._.AWE_Info(indicator='nMorph', filters=[('is_alpha', ['True']),('devword', ['True'])], summaryType='max'),
                    doc._.AWE_Info(indicator='nMorph', filters=[('is_alpha', ['True']),('devword', ['True'])], summaryType='stdev'),
                    doc._.AWE_Info(indicator='nSenses', filters=[('is_alpha', ['True']),('devword', ['True'])], summaryType='mean'),
                    doc._.AWE_Info(indicator='nSenses', filters=[('is_alpha', ['True']),('devword', ['True'])], summaryType='median'),
                    doc._.AWE_Info(indicator='nSenses', filters=[('is_alpha', ['True']),('devword', ['True'])], summaryType='min'),
                    doc._.AWE_Info(indicator='nSenses', filters=[('is_alpha', ['True']),('devword', ['True'])], summaryType='max'),
                    doc._.AWE_Info(indicator='nSenses', filters=[('is_alpha', ['True']),('devword', ['True'])], summaryType='stdev'),
                    doc._.AWE_Info(indicator='token_freq', filters=[('is_alpha', ['True']),('devword', ['True'])], summaryType='mean'),
                    doc._.AWE_Info(indicator='token_freq', filters=[('is_alpha', ['True']),('devword', ['True'])], summaryType='median'),
                    doc._.AWE_Info(indicator='token_freq', filters=[('is_alpha', ['True']),('devword', ['True'])], summaryType='min'),
                    doc._.AWE_Info(indicator='token_freq', filters=[('is_alpha', ['True']),('devword', ['True'])], summaryType='max'),
                    doc._.AWE_Info(indicator='token_freq', filters=[('is_alpha', ['True']),('devword', ['True'])], summaryType='stdev'),
                    doc._.AWE_Info(indicator='concreteness', filters=[('is_alpha', ['True']),('devword', ['True'])], summaryType='mean'),
                    doc._.AWE_Info(indicator='concreteness', filters=[('is_alpha', ['True']),('devword', ['True'])], summaryType='median'),
                    doc._.AWE_Info(indicator='concreteness', filters=[('is_alpha', ['True']),('devword', ['True'])], summaryType='min'),
                    doc._.AWE_Info(indicator='concreteness', filters=[('is_alpha', ['True']),('devword', ['True'])], summaryType='max'),
                    doc._.AWE_Info(indicator='concreteness', filters=[('is_alpha', ['True']),('devword', ['True'])], summaryType='stdev')
                ]
                await websocket.send(json.dumps(summaryFeats))
            else:
                await websocket.send(False)

if __name__ == '__main__':
    print('parser server loading')
    wsc = parserServer()
