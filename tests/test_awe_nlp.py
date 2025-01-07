"""
--- [ Test: test_awe_nlp.py ] -----------------------------------------------------------

Set of corresponding tests for document features found in awe_nlp.py of writingobserver.

Author: Caleb Scott (cwscott3@ncsu.edu)

-----------------------------------------------------------------------------------------
"""

# --- [ IMPORTS ] -----------------------------------------------------------------------

import unittest
import json
import spacy
import coreferee
import spacytextblob.spacytextblob

import awe_components.components.lexicalFeatures
import awe_components.components.syntaxDiscourseFeats
import awe_components.components.viewpointFeatures
import awe_components.components.lexicalClusters
import awe_components.components.contentSegmentation

from awe_workbench.pipeline import pipeline_def
from examples.essays.essays import get_essay

# --- [ CONSTS/VARS ] -------------------------------------------------------------------

SPACY_MODEL = 'en_core_web_lg'

COMPONENTS = [el['component'] for el in pipeline_def]

TEST_TEXT = "gre6.txt"

# --- [ CLASSES ] -----------------------------------------------------------------------

class AWENLPTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        This is the basic initializer for all test classes.

        Sets up the spacy pipeline.
        """
        # Initialize the pipeline
        try:
            cls.nlp = spacy.load(SPACY_MODEL)
            for comp in COMPONENTS:
                cls.nlp.add_pipe(comp)
        except OSError as e:
            print("There was an error loading 'en_core_web_lg' from spacy.")
            raise OSError() from e
        
        # Now get the text
        cls.doc = cls.nlp(get_essay(TEST_TEXT))

    def test_is_academic(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(indicator='is_academic',summaryType='percent'), 22)

    def test_vwp_interactive_percent(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(indicator='vwp_interactive',summaryType='percent'), 4)

    def test_is_latinate(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(indicator='is_latinate',summaryType='percent'), 13)

    def test_vwp_evaluation_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(indicator='vwp_evaluation',summaryType='total'), 704)

    def test_vwp_emotionword_percent(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(indicator='vwp_emotionword',summaryType='percent'), 2)

    def test_vwp_argumentword_percent(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(indicator='vwp_argumentword',summaryType='percent'), 100)

    def test_vwp_explicit_argument_percent(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(indicator='vwp_explicit_argument',summaryType='percent'), 15)

    def test_vwp_statements_of_opinion_percent(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='vwp_statements_of_opinion',summaryType='percent'), 78)

    def test_vwp_statements_of_fact_percent(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='vwp_statements_of_fact',summaryType='percent'), 22)

    def test_transitions_counts(self):
        counts_dict = json.loads(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='transitions',summaryType='counts'))
        self.assertEqual(sum(list(counts_dict.values())), 25)

    def test_transitions_positive_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['positive'])],summaryType='total'), 0)

    def test_transitions_conditional_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['conditional'])],summaryType='total'), 0)

    def test_transitions_consequential_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['consequential'])],summaryType='total'), 0)

    def test_transitions_contrastive_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['contrastive'])],summaryType='total'), 5)

    def test_transitions_counterpoint_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['counterpoint'])],summaryType='total'), 0)

    def test_transitions_comparative_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['comparative'])],summaryType='total'), 1)

    def test_transitions_crossreferential_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['crossreferential'])],summaryType='total'), 0)

    def test_transitions_illustrative_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['illustrative'])],summaryType='total'), 6)

    def test_transitions_negative_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['negative'])],summaryType='total'), 0)

    def test_transitions_emphatic_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['emphatic'])],summaryType='total'), 2)

    def test_transitions_evidentiary_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['evidentiary'])],summaryType='total'), 0)

    def test_transitions_general_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['general'])],summaryType='total'), 0)

    def test_transitions_ordinal_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['ordinal'])],summaryType='total'), 0)

    def test_transitions_purposive_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['purposive'])],summaryType='total'), 0)

    def test_transitions_periphrastic_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['periphrastic'])],summaryType='total'), 0)

    def test_transitions_hypothetical_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['hypothetical'])],summaryType='total'), 0)

    def test_transitions_summative_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['summative'])],summaryType='total'), 0)

    def test_transitions_introductory_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['introductory'])],summaryType='total'), 5)

    def test_pos_adj_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(indicator='pos_',filters=[('==', ['ADJ'])],summaryType='total'), 62)

    def test_pos_adv_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(indicator='pos_',filters=[('==', ['ADV'])],summaryType='total'), 23)

    def test_pos_noun_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(indicator='pos_',filters=[('==', ['NOUN'])],summaryType='total'), 189)

    def test_pos_propn_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(indicator='pos_',filters=[('==', ['PROPN'])],summaryType='total'), 13)

    def test_pos_verb_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(indicator='pos_',filters=[('==', ['VERB'])],summaryType='total'), 78)

    def test_pos_num_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(indicator='pos_',filters=[('==', ['NUM'])],summaryType='total'), 2)

    def test_pos_adp_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(indicator='pos_',filters=[('==', ['ADP'])],summaryType='total'), 81)

    def test_pos_cconj_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(indicator='pos_',filters=[('==', ['CCONJ'])],summaryType='total'), 14)

    def test_pos_sconj_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(indicator='pos_',filters=[('==', ['SCONJ'])],summaryType='total'), 17)

    def test_pos_aux_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(indicator='pos_',filters=[('==', ['AUX'])],summaryType='total'), 36)

    def test_pos_pron_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(indicator='pos_',filters=[('==', ['PRON'])],summaryType='total'), 22)

    def test_sentence_types_counts(self):
        types_dict = json.loads(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='sentence_types',summaryType='counts'))
        self.assertEqual(sum(list(types_dict.values())), 35)

    def test_sentence_types_simple_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='sentence_types',filters=[('==', ['Simple'])],summaryType='total'), 13)

    def test_sentence_types_simple_complex_pred_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='sentence_types',filters=[('==', ['SimpleComplexPred'])],summaryType='total'), 3)

    def test_sentence_types_simple_compound_pred_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='sentence_types',filters=[('==', ['SimpleCompoundPred'])],summaryType='total'), 0)

    def test_sentence_types_simple_compound_complex_pred_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='sentence_types',filters=[('==', ['SimpleCompoundComplexPred'])],summaryType='total'), 0)

    def test_sentence_types_compound_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='sentence_types',filters=[('==', ['Compound'])],summaryType='total'), 2)

    def test_sentence_types_complex_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='sentence_types',filters=[('==', ['Complex'])],summaryType='total'), 16)

    def test_sentence_types_compound_complex_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='sentence_types',filters=[('==', ['CompoundComplex'])],summaryType='total'), 1)

    def test_vwp_source_percent(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(indicator='vwp_source',summaryType='percent'), 0)

    def test_vwp_attribution_percent(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(indicator='vwp_attribution',summaryType='percent'), 0)

    def test_vwp_cite_percent(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(indicator='vwp_cite',summaryType='percent'), 0)

    def test_vwp_quoted_percent(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(indicator='vwp_quoted',summaryType='percent'), 0)

    def test_vwp_direct_speech_percent(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='vwp_direct_speech',summaryType='percent'), 0)

    def test_vwp_in_direct_speech_percent(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(indicator='vwp_in_direct_speech',summaryType='percent'), 0)

    def test_vwp_tone_greater_percent(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(indicator='vwp_tone',filters=[('>', [0.4])],summaryType='percent'), 1)

    def test_vwp_tone_lesser_percent(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(indicator='vwp_tone',filters=[('<', [-0.4])],summaryType='percent'), 2)

    def test_concrete_details_percent(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(indicator='concrete_details',summaryType='percent'), 2)

    def test_main_ideas_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='main_ideas',summaryType='total'), 9)

    def test_supporting_ideas_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='supporting_ideas',summaryType='total'), 11)

    def test_supporting_details_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='supporting_details',summaryType='total'), 6)

    def test_nSyll_percent(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(indicator='nSyll',filters=[('>', [3])],summaryType='percent'), 10)

    def test_max_freq_lesser_percent(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(indicator='max_freq',filters=[('<', [4])],summaryType='percent'), 9)

    def test_sents_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='sents',summaryType='total'), 35)

    def test_delimiter_n_total(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='delimiter_n',summaryType='total'), 223)

    def test_vwp_character_percent(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(indicator='vwp_character',summaryType='percent'), 2)

    def test_in_past_tense_scope_percent(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(indicator='in_past_tense_scope',summaryType='percent'), 33)

    def test_vwp_propositional_attitudes_percent(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='vwp_propositional_attitudes',summaryType='percent'), 53)

    def test_vwp_social_awareness_percent(self):
        self.assertEqual(self.__class__.doc._.AWE_Info(infoType='Doc',indicator='vwp_social_awareness',summaryType='percent'), 3)

# --- [ END ] ---------------------------------------------------------------------------
