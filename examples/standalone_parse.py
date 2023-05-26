#!/usr/bin/env python3.10
# Copyright 2022, Educational Testing Service

import awe_workbench
import holmes_extractor
import holmes_extractor.manager
import holmes_extractor.ontology
from holmes_extractor.manager import Manager
from holmes_extractor.ontology import Ontology
from awe_components.components.utility_functions \
    import print_parse_tree
from awe_workbench.pipeline import pipeline_def
import argparse

parser = argparse.ArgumentParser(description="Parse a student text file")
parser.add_argument(
    '--filename',
    default="essays/leprechaun.txt",
    help='Which file to parse'
)

args = parser.parse_args()
doc = open(args.filename).read()


# Manager here makes use of the holmes extractor manager object which
# provides the ability to load and archive working documents in memory.
# Documents can be registered/deregistered for use.

manager = holmes_extractor.manager.Manager(
            model='en_core_web_lg',
            perform_coreference_resolution=True,
            extra_components=pipeline_def
       )

manager.parse_and_register_document(doc, 'temp')
out = manager.get_document('temp')
print_parse_tree(out)
doc = out
print(doc._.AWE_Info(infoType='Token', indicator='vwp_argumentation', filters=[('vwp_argumentation',['True'])], summaryType='percent')) 

'''
content_pos = ['NOUN', 'PROPN', 'VERB', 'ADJ', 'ADV', 'CD']
summaryFeats = [
    doc._.AWE_Info(indicator='nSyll',
                   summaryType="mean"),
    doc._.AWE_Info(indicator='nSyll',
                   summaryType="median"),
    doc._.AWE_Info(indicator='nSyll',
                   summaryType="max"),
    doc._.AWE_Info(indicator='nSyll',
                   summaryType="min"),
    doc._.AWE_Info(indicator='nSyll',
                   summaryType="stdev"),
    doc._.AWE_Info(indicator='text', \
                   filters=[('is_alpha', ['True'])], \
                            transformations=['len', 'sqrt'], \
                            summaryType='mean'),
    doc._.AWE_Info(indicator='text', \
                   filters=[('is_alpha', ['True'])], \
                   transformations=['len', 'sqrt'], \
                   summaryType='median'),
    doc._.AWE_Info(indicator='text', \
                   filters=[('is_alpha', ['True'])], \
                   transformations=['len', 'sqrt'], \
                   summaryType='max'),
    doc._.AWE_Info(indicator='text', \
                   filters=[('is_alpha', ['True'])], \
                            transformations=['len', 'sqrt'], \
                            summaryType='min'),
    doc._.AWE_Info(indicator='text', \
                   filters=[('is_alpha', ['True'])], \
                   transformations=['len', 'sqrt'], \
                   summaryType='stdev'),
    doc._.AWE_Info(indicator='is_latinate',
                   filters=[('is_alpha', ['True'])], \
                   summaryType="proportion"),
    doc._.AWE_Info(indicator='is_academic',
                   filters=[('is_alpha', ['True'])], \
                   summaryType="proportion"),
    doc._.AWE_Info(indicator='family_size', \
                   filters=[('is_alpha', ['True'])], \
                   summaryType='mean'),
    doc._.AWE_Info(indicator='family_size', \
                   filters=[('is_alpha', ['True'])], \
                   summaryType='median'),
    doc._.AWE_Info(indicator='family_size', \
                   filters=[('is_alpha', ['True'])], \
                   summaryType='max'),
    doc._.AWE_Info(indicator='family_size', \
                   filters=[('is_alpha', ['True'])], \
                   summaryType='min'),
    doc._.AWE_Info(indicator='family_size', \
                   filters=[('is_alpha', ['True'])], \
                   summaryType='stdev'),
    doc._.AWE_Info(indicator='concreteness', \
                   filters=[('is_alpha', ['True'])], \
                   summaryType='mean'),
    doc._.AWE_Info(indicator='concreteness', \
                   filters=[('is_alpha', ['True'])], \
                   summaryType='median'),
    doc._.AWE_Info(indicator='concreteness', \
                   filters=[('is_alpha', ['True'])], \
                   summaryType='max'),
    doc._.AWE_Info(indicator='concreteness', \
                   filters=[('is_alpha', ['True'])], \
                   summaryType='min'),
    doc._.AWE_Info(indicator='concreteness', \
                   filters=[('is_alpha', ['True'])], \
                   summaryType='stdev'),
    doc._.AWE_Info(indicator='nSenses', \
                   filters=[('is_alpha', ['True'])], \
                   transformations=['log'], \
                   summaryType='mean'),
    doc._.AWE_Info(indicator='nSenses', \
                   filters=[('is_alpha', ['True'])], \
                   transformations=['log'], \
                   summaryType='median'),
    doc._.AWE_Info(indicator='nSenses', \
                   filters=[('is_alpha', ['True'])], \
                   transformations=['log'], \
                   summaryType='max'),
    doc._.AWE_Info(indicator='nSenses', \
                   filters=[('is_alpha', ['True'])], \
                   transformations=['log'], \
                   summaryType='min'),
    doc._.AWE_Info(indicator='nSenses', \
                   filters=[('is_alpha', ['True'])], \
                   transformations=['log'], \
                   summaryType='stdev'),
    doc._.AWE_Info(indicator='nMorph', \
                   filters=[('is_alpha', ['True'])], \
                   summaryType='mean'),
    doc._.AWE_Info(indicator='nMorph', \
                   filters=[('is_alpha', ['True'])], \
                   summaryType='median'),
    doc._.AWE_Info(indicator='nMorph', \
                   filters=[('is_alpha', ['True'])], \
                   summaryType='max'),
    doc._.AWE_Info(indicator='nMorph', \
                   filters=[('is_alpha', ['True'])], \
                   summaryType='min'),
    doc._.AWE_Info(indicator='nMorph', \
                   filters=[('is_alpha', ['True'])], \
                   summaryType='stdev'),
    doc._.AWE_Info(indicator='min_root_freq',
                   filters=[('is_alpha', ['True'])],
                   transformations=['log'],
                   summaryType='mean'),
    doc._.AWE_Info(indicator='min_root_freq',
                   filters=[('is_alpha', ['True'])],
                   transformations=['log'],
                   summaryType='median'),
    doc._.AWE_Info(indicator='min_root_freq',
                   filters=[('is_alpha', ['True'])],
                   transformations=['log'],
                   summaryType='max'),
    doc._.AWE_Info(indicator='min_root_freq',
                   filters=[('is_alpha', ['True'])],
                   transformations=['log'],
                   summaryType='min'),
    doc._.AWE_Info(indicator='min_root_freq',
                   filters=[('is_alpha', ['True'])],
                   transformations=['log'],
                   summaryType='stdev'),
    doc._.AWE_Info(indicator='root_famSize',
                   filters=[('is_alpha', ['True'])],
                   summaryType='mean'),
    doc._.AWE_Info(indicator='root_famSize',
                   filters=[('is_alpha', ['True'])],
                   summaryType='median'),
    doc._.AWE_Info(indicator='root_famSize',
                   filters=[('is_alpha', ['True'])],
                   summaryType='max'),
    doc._.AWE_Info(indicator='root_famSize',
                   filters=[('is_alpha', ['True'])],
                   summaryType='min'),
    doc._.AWE_Info(indicator='root_famSize',
                   filters=[('is_alpha', ['True'])],
                   summaryType='stdev'),
    doc._.AWE_Info(indicator='root_pfmf',
                   filters=[('is_alpha', ['True'])],
                   summaryType='mean'),
    doc._.AWE_Info(indicator='root_pfmf',
                   filters=[('is_alpha', ['True'])],
                   summaryType='median'),
    doc._.AWE_Info(indicator='root_pfmf',
                   filters=[('is_alpha', ['True'])],
                   summaryType='max'),
    doc._.AWE_Info(indicator='root_pfmf',
                   filters=[('is_alpha', ['True'])],
                   summaryType='min'),
    doc._.AWE_Info(indicator='root_pfmf',
                   filters=[('is_alpha', ['True'])],
                   summaryType='stdev'),
    doc._.AWE_Info(indicator='token_freq',
                   filters=[('is_alpha', ['True'])],
                   summaryType='mean'),
    doc._.AWE_Info(indicator='token_freq',
                   filters=[('is_alpha', ['True'])],
                   summaryType='median'),
    doc._.AWE_Info(indicator='token_freq',
                   filters=[('is_alpha', ['True'])],
                   summaryType='max'),
    doc._.AWE_Info(indicator='token_freq',
                   filters=[('is_alpha', ['True'])],
                   summaryType='min'),
    doc._.AWE_Info(indicator='token_freq',
                   filters=[('is_alpha', ['True'])],
                   summaryType='stdev'),
    doc._.AWE_Info(indicator='lemma_freq',
                   filters=[('is_alpha', ['True'])],
                   summaryType='mean'),
    doc._.AWE_Info(indicator='lemma_freq',
                   filters=[('is_alpha', ['True'])],
                   summaryType='median'),
    doc._.AWE_Info(indicator='lemma_freq',
                   filters=[('is_alpha', ['True'])],
                   summaryType='max'),
    doc._.AWE_Info(indicator='lemma_freq',
                   filters=[('is_alpha', ['True'])],
                   summaryType='min'),
    doc._.AWE_Info(indicator='lemma_freq',
                   filters=[('is_alpha', ['True'])],
                   summaryType='stdev'),
    doc._.AWE_Info(indicator='max_freq',
                   summaryType='mean'),
    doc._.AWE_Info(indicator='max_freq',
                   summaryType='median'),
    doc._.AWE_Info(indicator='max_freq',
                   summaryType='max'),
    doc._.AWE_Info(indicator='max_freq',
                   summaryType='min'),
    doc._.AWE_Info(indicator='max_freq',
                   summaryType='stdev'),
    doc._.AWE_Info(indicator='abstract_trait',
                   filters=[('is_alpha', ['True'])], \
                   summaryType="proportion"),
    doc._.AWE_Info(indicator='animate',
                   filters=[('is_alpha', ['True'])], \
                   summaryType="proportion"),
    doc._.AWE_Info(indicator='deictic',
                   filters=[('is_alpha', ['True'])], \
                   summaryType="proportion"),
    doc._.AWE_Info(indicator='root', \
                   filters=[('is_alpha', ['True']),
                            ('is_stop', ['False']),
                            ('pos_', content_pos)], \
                   summaryType = 'counts'),
    doc._.AWE_Info(indicator='lemma_', \
                   filters=[('is_alpha', ['True']),
                            ('is_stop', ['False']),
                            ('pos_', content_pos)], \
                   summaryType = 'counts'),
    doc._.AWE_Info(indicator='lower_', \
                   filters=[('is_alpha', ['True']),
                            ('is_stop', ['False']),
                            ('pos_', content_pos)], \
                   summaryType = 'counts'),
    doc._.AWE_Info(indicator='text', \
                   filters=[('is_alpha', ['True']),
                            ('is_stop', ['False']),
                            ('pos_', content_pos)], \
                   summaryType = 'counts'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='delimiter_\n',
                   summaryType='counts')[0],
    doc._.AWE_Info(infoType="Doc",
                   indicator='sents',
                   transformations=['tokenlen'],
                   summaryType='mean'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='sents',
                   transformations=['tokenlen'],
                   summaryType='median'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='sents',
                   transformations=['tokenlen'],
                   summaryType='max'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='sents',
                   transformations=['tokenlen'],
                   summaryType='min'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='sents',
                   transformations=['tokenlen'],
                   summaryType='stdev'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='transitions',
                   summaryType='total'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='transitions',
                   summaryType='counts'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='transitions',
                   transformations=['text'],
                   summaryType='counts'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='transition_distances',
                   summaryType='mean'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='transition_distances',
                   summaryType='median'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='transition_distances',
                   summaryType='max'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='transition_distances',
                   summaryType='min'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='transition_distances',
                   summaryType='stdev'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='intersentence_cohesions',
                   summaryType='mean'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='intersentence_cohesions',
                   summaryType='median'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='intersentence_cohesions',
                   summaryType='max'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='intersentence_cohesions',
                   summaryType='min'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='intersentence_cohesions',
                   summaryType='stdev'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='sliding_window_cohesions',
                   summaryType='mean'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='sliding_window_cohesions',
                   summaryType='median'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='sliding_window_cohesions',
                   summaryType='max'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='sliding_window_cohesions',
                   summaryType='min'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='sliding_window_cohesions',
                   summaryType='stdev'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='corefChainInfo',
                   summaryType='counts'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='corefChainInfo',
                   transformations=['len'],
                   summaryType='mean'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='corefChainInfo',
                   transformations=['len'],
                   summaryType='median'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='corefChainInfo',
                   transformations=['len'],
                   summaryType='max'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='corefChainInfo',
                   transformations=['len'],
                   summaryType='min'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='corefChainInfo',
                   transformations=['len'],
                   summaryType='stdev'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='sents',
                   summaryType='counts'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='sents',
                   transformations=['len'],
                   summaryType='mean'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='sents',
                   transformations=['len'],
                   summaryType='median'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='sents',
                   transformations=['len'],
                   summaryType='max'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='sents',
                   transformations=['len'],
                   summaryType='min'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='sents',
                   transformations=['len'],
                   summaryType='stdev'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='sentenceThemes',
                   transformations=['tokenlen'],
                   summaryType='mean'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='sentenceThemes',
                   transformations=['tokenlen'],
                   summaryType='median'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='sentenceThemes',
                   transformations=['tokenlen'],
                   summaryType='max'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='sentenceThemes',
                   transformations=['tokenlen'],
                   summaryType='min'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='sentenceThemes',
                   transformations=['tokenlen'],
                   summaryType='stdev'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='syntacticDepthsOfRhemes',
                   summaryType='mean'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='syntacticDepthsOfRhemes',
                   summaryType='median'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='syntacticDepthsOfRhemes',
                   summaryType='max'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='syntacticDepthsOfRhemes',
                   summaryType='min'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='syntacticDepthsOfRhemes',
                   summaryType='stdev'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='syntacticDepthsOfThemes',
                   summaryType='mean'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='syntacticDepthsOfThemes',
                   summaryType='median'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='syntacticDepthsOfThemes',
                   summaryType='max'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='syntacticDepthsOfThemes',
                   summaryType='min'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='syntacticDepthsOfThemes',
                   summaryType='stdev'),
    doc._.AWE_Info(indicator='weightedSyntacticDepth',
                   summaryType='mean'),
    doc._.AWE_Info(indicator='weightedSyntacticDepth',
                   summaryType='median'),
    doc._.AWE_Info(indicator='weightedSyntacticDepth',
                   summaryType='max'),
    doc._.AWE_Info(indicator='weightedSyntacticDepth',
                   summaryType='min'),
    doc._.AWE_Info(indicator='weightedSyntacticDepth',
                   summaryType='stdev'),
    doc._.AWE_Info(indicator='weightedSyntacticBreadth',
                   summaryType='mean'),
    doc._.AWE_Info(indicator='weightedSyntacticBreadth',
                   summaryType='median'),
    doc._.AWE_Info(indicator='weightedSyntacticBreadth',
                   summaryType='max'),
    doc._.AWE_Info(indicator='weightedSyntacticBreadth',
                   summaryType='min'),
    doc._.AWE_Info(indicator='weightedSyntacticBreadth',
                   summaryType='stdev'),
    doc._.syntacticVariety,
    doc._.AWE_Info(indicator='in_past_tense_scope',
                   summaryType='proportion'),
    doc._.AWE_Info(indicator='vwp_argumentation',
                   summaryType='proportion'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='direct_speech_spans',
                   summaryType='proportion'),
    doc._.AWE_Info(indicator='vwp_egocentric',
                   summaryType='proportion'),
    doc._.AWE_Info(indicator='vwp_allocentric',
                   summaryType='proportion'),
    doc._.AWE_Info(indicator='subjectivity',
                   summaryType='mean'),
    doc._.AWE_Info(indicator='subjectivity',
                   summaryType='median'),
    doc._.AWE_Info(indicator='subjectivity',
                   summaryType='min'),
    doc._.AWE_Info(indicator='subjectivity',
                   summaryType='max'),
    doc._.AWE_Info(indicator='subjectivity',
                   summaryType='stdev'),
    doc._.AWE_Info(indicator='polarity',
                   summaryType='mean'),
    doc._.AWE_Info(indicator='polarity',
                   summaryType='median'),
    doc._.AWE_Info(indicator='polarity',
                   summaryType='min'),
    doc._.AWE_Info(indicator='polarity',
                   summaryType='max'),
    doc._.AWE_Info(indicator='polarity',
                   summaryType='stdev'),
    doc._.AWE_Info(indicator='vwp_sentiment',
                   summaryType='mean'),
    doc._.AWE_Info(indicator='vwp_sentiment',
                   summaryType='median'),
    doc._.AWE_Info(indicator='vwp_sentiment',
                   summaryType='min'),
    doc._.AWE_Info(indicator='vwp_sentiment',
                   summaryType='max'),
    doc._.AWE_Info(indicator='vwp_sentiment',
                   summaryType='stdev'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='main_cluster_spans',
                   transformations=['len'],
                   summaryType='mean'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='main_cluster_spans',
                   transformations=['len'],
                   summaryType='median'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='main_cluster_spans',
                   transformations=['len'],
                   summaryType='min'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='main_cluster_spans',
                   transformations=['len'],
                   summaryType='max'),
    doc._.AWE_Info(infoType="Doc",
                   indicator='main_cluster_spans',
                   transformations=['len'],
                   summaryType='stdev'),
    doc._.AWE_Info(indicator='devword', \
                   summaryType='proportion'),
    doc._.AWE_Info(indicator='nSyll', \
                   filters=[('is_alpha', ['True']),
                            ('devword', ['True'])], \
                   summaryType='mean'),
    doc._.AWE_Info(indicator='nSyll', \
                   filters=[('is_alpha', ['True']),
                            ('devword', ['True'])], \
                   summaryType='median'),
    doc._.AWE_Info(indicator='nSyll', \
                   filters=[('is_alpha', ['True']),
                            ('devword', ['True'])], \
                   summaryType='min'),
    doc._.AWE_Info(indicator='nSyll', \
                   filters=[('is_alpha', ['True']),
                            ('devword', ['True'])], \
                   summaryType='max'),
    doc._.AWE_Info(indicator='nSyll', \
                   filters=[('is_alpha', ['True']),
                            ('devword', ['True'])], \
                   summaryType='stdev'),
    doc._.AWE_Info(indicator='nMorph', \
                   filters=[('is_alpha', ['True']),
                            ('devword', ['True'])], \
                   summaryType='mean'),
    doc._.AWE_Info(indicator='nMorph', \
                   filters=[('is_alpha', ['True']),
                            ('devword', ['True'])], \
                   summaryType='median'),
    doc._.AWE_Info(indicator='nMorph', \
                   filters=[('is_alpha', ['True']),
                            ('devword', ['True'])], \
                   summaryType='min'),
    doc._.AWE_Info(indicator='nMorph', \
                   filters=[('is_alpha', ['True']),
                            ('devword', ['True'])], \
                   summaryType='max'),
    doc._.AWE_Info(indicator='nMorph', \
                   filters=[('is_alpha', ['True']),
                            ('devword', ['True'])], \
                   summaryType='stdev'),
    doc._.AWE_Info(indicator='nSenses', \
                   filters=[('is_alpha', ['True']),
                            ('devword', ['True'])], \
                   summaryType='mean'),
    doc._.AWE_Info(indicator='nSenses', \
                   filters=[('is_alpha', ['True']),
                            ('devword', ['True'])], \
                   summaryType='median'),
    doc._.AWE_Info(indicator='nSenses', \
                   filters=[('is_alpha', ['True']),
                            ('devword', ['True'])], \
                   summaryType='min'),
    doc._.AWE_Info(indicator='nSenses', \
                   filters=[('is_alpha', ['True']),
                            ('devword', ['True'])], \
                   summaryType='max'),
    doc._.AWE_Info(indicator='nSenses', \
                   filters=[('is_alpha', ['True']),
                            ('devword', ['True'])], \
                   summaryType='stdev'),
    doc._.AWE_Info(indicator='token_freq', \
                   filters=[('is_alpha', ['True']),
                            ('devword', ['True'])], \
                   summaryType='mean'),
    doc._.AWE_Info(indicator='token_freq', \
                   filters=[('is_alpha', ['True']),
                            ('devword', ['True'])], \
                   summaryType='median'),
    doc._.AWE_Info(indicator='token_freq', \
                   filters=[('is_alpha', ['True']),
                            ('devword', ['True'])], \
                   summaryType='min'),
    doc._.AWE_Info(indicator='token_freq', \
                   filters=[('is_alpha', ['True']),
                            ('devword', ['True'])], \
                   summaryType='max'),
    doc._.AWE_Info(indicator='token_freq', \
                   filters=[('is_alpha', ['True']),
                            ('devword', ['True'])], \
                   summaryType='stdev'),
    doc._.AWE_Info(indicator='concreteness', \
                   filters=[('is_alpha', ['True']),
                            ('devword', ['True'])], \
                   summaryType='mean'),
    doc._.AWE_Info(indicator='concreteness', \
                   filters=[('is_alpha', ['True']),
                            ('devword', ['True'])], \
                   summaryType='median'),
    doc._.AWE_Info(indicator='concreteness', \
                   filters=[('is_alpha', ['True']),
                            ('devword', ['True'])], \
                   summaryType='min'),
    doc._.AWE_Info(indicator='concreteness', \
                   filters=[('is_alpha', ['True']),
                            ('devword', ['True'])], \
                   summaryType='max'),
    doc._.AWE_Info(indicator='concreteness', \
                   filters=[('is_alpha', ['True']),
                            ('devword', ['True'])], \
                   summaryType='stdev')]
print(summaryFeats)
'''

