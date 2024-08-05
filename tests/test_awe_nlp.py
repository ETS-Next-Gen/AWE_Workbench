"""
--- [ Test: test_awe_nlp.py ] -----------------------------------------------------------

Set of corresponding tests for document features found in awe_nlp.py of writingobserver.

Author: Caleb Scott (cwscott3@ncsu.edu)

-----------------------------------------------------------------------------------------
"""

# --- [ IMPORTS ] -----------------------------------------------------------------------

import holmes_extractor.manager as holmes
import unittest
import json
from awe_components.components.utility_functions import print_parse_tree
from awe_workbench.pipeline import pipeline_def

# --- [ CONSTS/VARS ] -------------------------------------------------------------------

holmes_manager = holmes.Manager(
    'en_core_web_lg', 
    perform_coreference_resolution=False, 
    number_of_workers=2, 
    extra_components=pipeline_def
)

# --- [ SETUP ] -------------------------------------------------------------------------

# GRE Sample from https://www.ets.org/gre/revised_general/prepare/analytical_writing/issue/sample_responses
# NOTE: in the examples directory, this sample is called gre6
holmes_manager.parse_and_register_document(
    document_text="The statement linking technology negatively with free thinking plays on recent human experience over the past century. Surely there has been no time in history where the lived lives of people have changed more dramatically. A quick reflection on a typical day reveals how technology has revolutionized the world. Most people commute to work in an automobile that runs on an internal combustion engine. During the workday, chances are high that the employee will interact with a computer that processes information on silicon bridges that are .09 microns wide. Upon leaving home, family members will be reached through wireless networks that utilize satellites orbiting the earth. Each of these common occurrences could have been inconceivable at the turn of the 19th century.\n\nThe statement attempts to bridge these dramatic changes to a reduction in the ability for humans to think for themselves. The assumption is that an increased reliance on technology negates the need for people to think creatively to solve previous quandaries. Looking back at the introduction, one could argue that without a car, computer, or mobile phone, the hypothetical worker would need to find alternate methods of transport, information processing and communication. Technology short circuits this thinking by making the problems obsolete.\n\nHowever, this reliance on technology does not necessarily preclude the creativity that marks the human species. The prior examples reveal that technology allows for convenience. The car, computer and phone all release additional time for people to live more efficiently. This efficiency does not preclude the need for humans to think for themselves. In fact, technology frees humanity to not only tackle new problems, but may itself create new issues that did not exist without technology. For example, the proliferation of automobiles has introduced a need for fuel conservation on a global scale. With increasing energy demands from emerging markets, global warming becomes a concern inconceivable to the horse-and-buggy generation. Likewise dependence on oil has created nation-states that are not dependent on taxation, allowing ruling parties to oppress minority groups such as women. Solutions to these complex problems require the unfettered imaginations of maverick scientists and politicians.\n\nIn contrast to the statement, we can even see how technology frees the human imagination. Consider how the digital revolution and the advent of the internet has allowed for an unprecedented exchange of ideas. WebMD, a popular internet portal for medical information, permits patients to self research symptoms for a more informed doctor visit. This exercise opens pathways of thinking that were previously closed off to the medical layman. With increased interdisciplinary interactions, inspiration can arrive from the most surprising corners. Jeffrey Sachs, one of the architects of the UN Millenium Development Goals, based his ideas on emergency care triage techniques. The unlikely marriage of economics and medicine has healed tense, hyperinflation environments from South America to Eastern Europe.\n\nThis last example provides the most hope in how technology actually provides hope to the future of humanity. By increasing our reliance on technology, impossible goals can now be achieved. Consider how the late 20th century witnessed the complete elimination of smallpox. This disease had ravaged the human race since prehistorical days, and yet with the technology of vaccines, free thinking humans dared to imagine a world free of smallpox. Using technology, battle plans were drawn out, and smallpox was systematically targeted and eradicated.\n\nTechnology will always mark the human experience, from the discovery of fire to the implementation of nanotechnology. Given the history of the human race, there will be no limit to the number of problems, both new and old, for us to tackle. There is no need to retreat to a Luddite attitude to new things, but rather embrace a hopeful posture to the possibilities that technology provides for new avenues of human imagination.", 
    label='GRE_Sample_Essay'
)

# --- [ CLASSES ] -----------------------------------------------------------------------

class AWENLPTest(unittest.TestCase):

    def test_is_academic(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(indicator='is_academic',summaryType='percent'), 22)

    def test_vwp_interactive_percent(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(indicator='vwp_interactive',summaryType='percent'), 4)

    def test_is_latinate(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(indicator='is_latinate',summaryType='percent'), 13)

    def test_vwp_evaluation_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(indicator='vwp_evaluation',summaryType='total'), 704)

    def test_vwp_emotionword_percent(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(indicator='vwp_emotionword',summaryType='percent'), 2)

    def test_vwp_argumentword_percent(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(indicator='vwp_argumentword',summaryType='percent'), 100)

    def test_vwp_explicit_argument_percent(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(indicator='vwp_explicit_argument',summaryType='percent'), 15)

    def test_vwp_statements_of_opinion_percent(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='vwp_statements_of_opinion',summaryType='percent'), 78)

    def test_vwp_statements_of_fact_percent(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='vwp_statements_of_fact',summaryType='percent'), 22)

    def test_transitions_counts(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        counts_dict = json.loads(doc._.AWE_Info(infoType='Doc',indicator='transitions',summaryType='counts'))
        self.assertEqual(sum(list(counts_dict.values())), 25)

    def test_transitions_positive_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['positive'])],summaryType='total'), 0)

    def test_transitions_conditional_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['conditional'])],summaryType='total'), 0)

    def test_transitions_consequential_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['consequential'])],summaryType='total'), 0)

    def test_transitions_contrastive_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['contrastive'])],summaryType='total'), 5)

    def test_transitions_counterpoint_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['counterpoint'])],summaryType='total'), 0)

    def test_transitions_comparative_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['comparative'])],summaryType='total'), 1)

    def test_transitions_crossreferential_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['crossreferential'])],summaryType='total'), 0)

    def test_transitions_illustrative_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['illustrative'])],summaryType='total'), 6)

    def test_transitions_negative_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['negative'])],summaryType='total'), 0)

    def test_transitions_emphatic_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['emphatic'])],summaryType='total'), 2)

    def test_transitions_evidentiary_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['evidentiary'])],summaryType='total'), 0)

    def test_transitions_general_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['general'])],summaryType='total'), 0)

    def test_transitions_ordinal_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['ordinal'])],summaryType='total'), 0)

    def test_transitions_purposive_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['purposive'])],summaryType='total'), 0)

    def test_transitions_periphrastic_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['periphrastic'])],summaryType='total'), 0)

    def test_transitions_hypothetical_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['hypothetical'])],summaryType='total'), 0)

    def test_transitions_summative_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['summative'])],summaryType='total'), 0)

    def test_transitions_introductory_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='transitions',filters=[('==', ['introductory'])],summaryType='total'), 5)

    def test_pos_adj_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(indicator='pos_',filters=[('==', ['ADJ'])],summaryType='total'), 62)

    def test_pos_adv_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(indicator='pos_',filters=[('==', ['ADV'])],summaryType='total'), 23)

    def test_pos_noun_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(indicator='pos_',filters=[('==', ['NOUN'])],summaryType='total'), 189)

    def test_pos_propn_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(indicator='pos_',filters=[('==', ['PROPN'])],summaryType='total'), 13)

    def test_pos_verb_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(indicator='pos_',filters=[('==', ['VERB'])],summaryType='total'), 78)

    def test_pos_num_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(indicator='pos_',filters=[('==', ['NUM'])],summaryType='total'), 2)

    def test_pos_adp_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(indicator='pos_',filters=[('==', ['ADP'])],summaryType='total'), 81)

    def test_pos_cconj_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(indicator='pos_',filters=[('==', ['CCONJ'])],summaryType='total'), 14)

    def test_pos_sconj_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(indicator='pos_',filters=[('==', ['SCONJ'])],summaryType='total'), 17)

    def test_pos_aux_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(indicator='pos_',filters=[('==', ['AUX'])],summaryType='total'), 36)

    def test_pos_pron_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(indicator='pos_',filters=[('==', ['PRON'])],summaryType='total'), 22)

    def test_sentence_types_counts(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        types_dict = json.loads(doc._.AWE_Info(infoType='Doc',indicator='sentence_types',summaryType='counts'))
        self.assertEqual(sum(list(types_dict.values())), 35)

    def test_sentence_types_simple_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='sentence_types',filters=[('==', ['Simple'])],summaryType='total'), 13)

    def test_sentence_types_simple_complex_pred_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='sentence_types',filters=[('==', ['SimpleComplexPred'])],summaryType='total'), 3)

    def test_sentence_types_simple_compound_pred_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='sentence_types',filters=[('==', ['SimpleCompoundPred'])],summaryType='total'), 0)

    def test_sentence_types_simple_compound_complex_pred_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='sentence_types',filters=[('==', ['SimpleCompoundComplexPred'])],summaryType='total'), 0)

    def test_sentence_types_compound_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='sentence_types',filters=[('==', ['Compound'])],summaryType='total'), 2)

    def test_sentence_types_complex_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='sentence_types',filters=[('==', ['Complex'])],summaryType='total'), 16)

    def test_sentence_types_compound_complex_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='sentence_types',filters=[('==', ['CompoundComplex'])],summaryType='total'), 1)

    def test_vwp_source_percent(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(indicator='vwp_source',summaryType='percent'), 0)

    def test_vwp_attribution_percent(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(indicator='vwp_attribution',summaryType='percent'), 0)

    def test_vwp_cite_percent(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(indicator='vwp_cite',summaryType='percent'), 0)

    def test_vwp_quoted_percent(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(indicator='vwp_quoted',summaryType='percent'), 0)

    def test_vwp_direct_speech_percent(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='vwp_direct_speech',summaryType='percent'), 0)

    def test_vwp_in_direct_speech_percent(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(indicator='vwp_in_direct_speech',summaryType='percent'), 0)

    def test_vwp_tone_greater_percent(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(indicator='vwp_tone',filters=[('>', [0.4])],summaryType='percent'), 1)

    def test_vwp_tone_lesser_percent(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(indicator='vwp_tone',filters=[('<', [-0.4])],summaryType='percent'), 2)

    def test_concrete_details_percent(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(indicator='concrete_details',summaryType='percent'), 2)

    def test_main_ideas_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='main_ideas',summaryType='total'), 9)

    def test_supporting_ideas_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='supporting_ideas',summaryType='total'), 11)

    def test_supporting_details_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='supporting_details',summaryType='total'), 6)

    def test_nSyll_percent(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(indicator='nSyll',filters=[('>', [3])],summaryType='percent'), 10)

    def test_max_freq_lesser_percent(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(indicator='max_freq',filters=[('<', [4])],summaryType='percent'), 9)

    def test_sents_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='sents',summaryType='total'), 35)

    def test_delimiter_n_total(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='delimiter_n',summaryType='total'), 223)

    def test_vwp_character_percent(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(indicator='vwp_character',summaryType='percent'), 2)

    def test_in_past_tense_scope_percent(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(indicator='in_past_tense_scope',summaryType='percent'), 33)

    def test_vwp_propositional_attitudes_percent(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='vwp_propositional_attitudes',summaryType='percent'), 53)

    def test_vwp_social_awareness_percent(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.AWE_Info(infoType='Doc',indicator='vwp_social_awareness',summaryType='percent'), 3)

# --- [ END ] ---------------------------------------------------------------------------
