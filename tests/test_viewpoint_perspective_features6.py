#!/usr/bin/env python3.10
# Copyright 2022, Educational Testing Service

import holmes_extractor.manager as holmes
import unittest
from awe_components.utility_functions import print_parse_tree

holmes_manager = holmes.Manager(
    'en_core_web_lg', perform_coreference_resolution=False, number_of_workers=2)

# Aesop's fable is a public domain document available at http://read.gov/aesop/007.html
document_text="A lion lay asleep in the forest, his great head resting on his paws. A timid little mouse came upon him unexpectedly, and in her fright and haste to get away, ran across the lion's nose. Roused from his nap, the lion laid his huge paw angrily on the tiny creature to kill her.\n\n\"Spare me!\" begged the poor mouse. \"Please let me go and some day I will surely repay you.\"\n\nThe lion was much amused to think that a mouse could ever help him. But he was generous and finally let the mouse go.\n\nSome days later, while stalking his prey in the forest, the lion was caught in the toils of a hunter's net. Unable to free himself, he filled the forest with his angry roaring. The mouse knew the voice and quickly found the lion struggling in the net. Running to one of the great ropes that bound him, she gnawed it until it parted, and soon the lion was free.\n\n\"You laughed when I said I would repay you,\" said the Mouse. \"Now you see that even a Mouse can help a Lion.\""

holmes_manager.parse_and_register_document(document_text, label='Aesop')

class ViewpointPerspectiveFeatureTest2(unittest.TestCase):

    def test_vwp_perspective(self):
        doc = holmes_manager.get_document('Aesop')
        perspective_spans = {'implicit': {'64': [62, 63, 64, 66, 67], '68': [68, 69, 71, 72], '70': [70], '75': [73, 74, 75, 77, 78, 79, 80, 82, 83, 84, 86, 87], '106': [104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114], '115': [115], '131': [116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140], '147': [141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154], '182': [170, 171, 172, 173, 174, 176, 180, 181, 182, 183, 187, 188], '175': [175], '178': [177, 178, 179], '186': [184, 185, 186], '192': [189, 190, 191, 192, 193, 194], '195': [195], '196': [196], '208': [206, 207, 208, 209, 210, 211]}, 'explicit_1': [65, 76, 81, 199, 200, 201, 202, 203, 204, 205], 'explicit_2': [85, 197, 198, 214], 'explicit_3': {1: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 19, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61], 19: [1, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], 90: [88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103], 156: [90, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169], 214: [210, 212, 213, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225]}}
        self.assertEqual(doc._.vwp_perspective_spans,perspective_spans)

    def test_vwp_stance_markers(self):
        doc = holmes_manager.get_document('Aesop')
        stance_markers = {'implicit': {'64': [66], '70': [70], '75': [83], '106': [107], '175': [175], '192': [193], '208': [208]}, 'explicit_1': [201, 203], 'explicit_2': [], 'explicit_3': {1: [9], 19: [17], 90: [99], 214: [217, 220]}}
        self.assertEqual(doc._.vwp_stance_markers,stance_markers)

    def test_propn_egocentric(self):
        doc = holmes_manager.get_document('Aesop')
        self.assertEqual(doc._.propn_egocentric,0.14601769911504425)

    def test_propn_allocentric(self):
        doc = holmes_manager.get_document('Aesop')
        self.assertEqual(doc._.propn_allocentric,0.41150442477876104)

    def test_propositional_attitudes(self):
        doc = holmes_manager.get_document('Aesop')
        propositional_attitudes = {'implicit': [[[42, 61], 48, 49], [[73, 87], None, 75], [[116, 140], 129, 131], [[212, 225], 214, 215]], 'implicit_3': [], 'explicit_1': [], 'explicit_2': [], 'explicit_3': {90: [[[88, 103], 90, 95]], 156: [[[155, 169], 156, 162]], 210: [[[197, 211], 210, 201]]}}
        self.assertEqual(doc._.vwp_propositional_attitudes,propositional_attitudes)  
        
    def test_emotion_states(self):
        doc = holmes_manager.get_document('Aesop')
        emotion_states = {'explicit_1': [], 'explicit_2': [], 'explicit_3': {'Mouse': [28], 'Lion': [53, 93, 152, 165]}}
        self.assertEqual(doc._.vwp_emotion_states,emotion_states)

    def test_character_traits(self):
        doc = holmes_manager.get_document('Aesop')
        character_traits = {'explicit_1': [], 'explicit_2': [], 'explicit_3': {'Mouse': [17], 'Lion': [107]}}
        self.assertEqual(doc._.vwp_character_traits,character_traits)
                
    def test_subjectivity_ratings(self):
        doc = holmes_manager.get_document('Aesop')
        subjectivity_ratings = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.75, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.9, 0.0, 1.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.8888888888888888, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.8, 0.0, 0.0, 0.0, 0.9, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.75, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.8, 0.0, 0.0, 0.0, 0.0, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.assertEqual(doc._.subjectivity_ratings,subjectivity_ratings)

    def test_mean_subjectivity(self):
        doc = holmes_manager.get_document('Aesop')
        self.assertEqual(doc._.mean_subjectivity,0.1446998722860792)

    def test_med_subjectivity(self):
        doc = holmes_manager.get_document('Aesop')
        self.assertEqual(doc._.median_subjectivity,0.0)

    def test_max_subjectivity(self):
        doc = holmes_manager.get_document('Aesop')
        self.assertEqual(doc._.max_subjectivity,1.0)

    def test_min_subjectivity(self):
        doc = holmes_manager.get_document('Aesop')
        self.assertEqual(doc._.min_subjectivity,0.0)

    def test_std_subjectivity(self):
        doc = holmes_manager.get_document('Aesop')
        self.assertEqual(doc._.stdev_subjectivity,0.3124083650270696)

    def test_polarity_ratings(self):
        doc = holmes_manager.get_document('Aesop')
        polarity_ratings = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.1875, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4000000000000001, 0.0, -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5, 0.0, 0.4, 0.0, 0.0, 0.0, 0.4, 0.0, 0.0, 0.0, 0.0, -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3333333333333333, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        self.assertEqual(doc._.polarity_ratings,polarity_ratings)

    def test_mean_polarity(self):
        doc = holmes_manager.get_document('Aesop')
        self.assertEqual(doc._.mean_polarity,0.03156130268199234)

    def test_med_polarity(self):
        doc = holmes_manager.get_document('Aesop')
        self.assertEqual(doc._.median_polarity,0.0)

    def test_max_polarity(self):
        doc = holmes_manager.get_document('Aesop')
        self.assertEqual(doc._.max_polarity,0.8)

    def test_min_polarity(self):
        doc = holmes_manager.get_document('Aesop')
        self.assertEqual(doc._.min_polarity,-0.5)

    def test_stdev_polarity(self):
        doc = holmes_manager.get_document('Aesop')
        self.assertEqual(doc._.stdev_polarity,0.2057206641937544)

    def test_sentiment_ratings (self):
        doc = holmes_manager.get_document('Aesop')
        sentiment_ratings = [0.04, 0.21, 0.29, 0.37, 0, 0, 0.42, 0, 0, 0.62, 0.21, 0, 0.08, 0, 0, 0, 0.04, -0.4, 0.22, -0.05, 0, 0, 0, 0.02, 0, 0, 0, 0, -0.43, 0, -0.22, 0, 0.27, -0.01, 0, 0, 0, 0, 0.21, 0, 0.12, 0, 0, 0, 0, 0.38, 0, 0, 0.21, 0, 0, 0.18, 0.1, -0.07, 0.08, 0, 0.02, 0.26, 0, -0.79, 0, 0, 0, 0, 0.14, 0, 0, 0, 0, 0, -0.33, -0.05, 0, 0, 0.25, 0.23, 0, 0.33, 0, 0.06, 0.34, -0.19, 0.08, 0.15, 0.04, 0, 0, 0, 0, 0, 0.21, 0, 0.19, 0.51, 0, 0.42, 0, 0.04, -0.05, 0, 0, 0.48, 0, 0, 0, 0, 0, 0.6000000000000001, 0, 0, 0.23, 0, -0.05, 0.33, 0, 0, 0.06, 0, 0, 0, 0, 0, 0, -0.31, 0, 0, 0.42, 0, 0, 0.21, 0, 0, 0, 0, 0, 0, 0.04, 0.0098, 0, 7.000000000000001e-05, 0, -0.51, 0, 0.81, 0, 0, 0, 0.12, 0, 0.42, 0, 0, -0.61, 0.21, 0, 0, -0.05, 0, 0, 0.37, 0, 0, 0, 0, 0.21, -0.19, 0, 0, 7.000000000000001e-05, 0, 0.38, 0, 0.27, 0, 0, 0.62, 0, 0, -0.23, 0, 0, 0, 0, 0, 0, 0, 0.12, 0, 0, -0.07, 0, 0.21, 0, 0.81, 0, 0, 0, 0, 0, 0, -0.19, 0, -0.19, 0, 0.04, 0, 0, 0, 0, 0, -0.05, 0, 0, 0.06, 0, 0.31, 0, 0.08, 0.04, -0.05, 0.35000000000000003, 0.48, 0.04, 0.21, 0, 0]
        self.assertEqual(doc._.sentiment_ratings,sentiment_ratings)
        
    def test_mean_sentiment(self):
        doc = holmes_manager.get_document('Aesop')
        self.assertEqual(doc._.mean_sentiment,0.09563149425287357)

    def test_med_sentiment(self):
        doc = holmes_manager.get_document('Aesop')
        self.assertEqual(doc._.median_sentiment,0.0098)

    def test_max_sentiment(self):
        doc = holmes_manager.get_document('Aesop')
        self.assertEqual(doc._.max_sentiment,0.81)

    def test_min_sentiment(self):
        doc = holmes_manager.get_document('Aesop')
        self.assertEqual(doc._.min_sentiment,-0.79)

    def test_stdev_sentiment(self):
        doc = holmes_manager.get_document('Aesop')
        self.assertEqual(doc._.stdev_sentiment,0.2770221163932531)

    def test_vwp_arguments(self):
        doc = holmes_manager.get_document('Aesop')
        vwp_arguments = [68, 70, 95, 96, 99, 104, 157, 162, 165, 201, 202, 203, 205, 208, 214, 215, 216, 217, 220, 221]
        self.assertEqual(doc._.vwp_arguments,vwp_arguments)

    def test_propn_argument_words(self):
        doc = holmes_manager.get_document('Aesop')
        self.assertEqual(doc._.propn_argument_words,0.08849557522123894)

    def test_vwp_interactives(self):
        doc = holmes_manager.get_document('Aesop')
        vwp_interactives = [9, 39, 51, 65, 74, 76, 81, 83, 85, 91, 95, 106, 130, 138, 175, 177, 197, 200, 202, 205, 210, 214]
        self.assertEqual(doc._.vwp_interactives,vwp_interactives)

    def test_propn_interactive(self):
        doc = holmes_manager.get_document('Aesop')
        self.assertEqual(doc._.propn_interactive,0.09734513274336283)

    def test_vwp_quoted(self):
        doc = holmes_manager.get_document('Aesop')
        vwp_quoted = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]

        self.assertEqual(doc._.vwp_quoted,vwp_quoted)

    def test_vwp_direct_speech_spans(self):
        doc = holmes_manager.get_document('Aesop')
        self.assertEqual(doc._.vwp_direct_speech_spans,[[[65, 71, 76, 81], [85], [[62, 67], [68, 72], [73, 87]]], [[200, 202, 210], [197, 205, 214], [[197, 211], [212, 225]]]])

    def test_propn_direct_speech(self):
        doc = holmes_manager.get_document('Aesop')
        self.assertEqual(doc._.propn_direct_speech,0.18141592920353983)
      
    def test_governing_subjects(self):
        doc = holmes_manager.get_document('Aesop')
        governing_subjects = [None, None, 1, 1, 1, None, 1, None, None, 10, 8, 10, 10, None, 13, None, None, 19, 19, None, 19, None, None, 19, None, None, 19, None, 27, None, 27, None, 19, 19, None, 19, 19, None, None, None, 38, None, 48, 48, None, 44, None, None, None, 48, None, 52, 50, 48, 52, None, 57, None, None, 48, None, None, None, None, None, None, None, None, None, None, 71, None, None, None, None, None, None, 76, None, None, None, None, None, 81, 81, None, None, None, None, None, None, 90, 93, 90, None, 90, None, None, None, None, 98, 98, None, None, None, None, 105, 105, None, 105, 105, None, None, 112, None, None, None, None, 129, None, None, 129, None, 122, 123, None, 123, None, None, None, None, 129, 129, None, None, None, None, None, None, 137, None, 146, None, 146, None, None, None, 146, None, None, 149, None, 151, 151, None, None, None, 156, None, None, None, 156, 156, None, None, 164, 164, None, None, None, 181, 181, 181, 181, None, 176, 181, None, 176, None, None, None, 181, None, None, None, 185, None, None, 191, None, None, 191, 191, None, None, None, None, 197, 200, None, 200, None, None, 202, None, None, None, 210, None, None, None, None, 214, None, 214, None, None, None, None, None, 219, None, None, None, None]
        self.assertEqual(doc._.governing_subjects,governing_subjects)


    def test_content_segments(self):
        doc = holmes_manager.get_document('Aesop')      
        content_segments = [[0, 62, [[1, 14, 38, 48, 52], [2], [3], [6], [10], [11], [17], [19], [20], [23], [28], [30], [33], [35], [40], [42], [45], [49], [51], [53], [56], [57], [59]]], [88, 115, [[98, 112], [90], [93], [107], [110]]], [141, 195, [[152, 159], [164, 191], [141], [143], [147], [149], [153], [156], [161], [168], [170], [176], [178], [182], [186], [189], [193]]], [197, 226, [[210, 219], [198], [204], [223]]]]
        self.assertEqual(doc._.content_segments,content_segments)
        
    def test_prompt_related(self):
        doc = holmes_manager.get_document('Aesop')      
        prompt_related = [[5, 2.444390124663897, ['lion', 'paw', 'Lion'], [1, 14, 38, 48, 52, 90, 129, 164, 191, 223]], [4, 1.6241299303944317, ['mouse', 'Mouse'], [19, 71, 98, 112, 156, 210, 219]], [9, 1.1996161228406907, ['angrily', 'amused', 'angry', 'voice', 'laugh'], [53, 93, 152, 159, 198]]]
        self.assertEqual(doc._.prompt_related,prompt_related)
        
    def test_prompt_language(self):
        doc = holmes_manager.get_document('Aesop')      
        prompt_language = ['lion', 'paw', 'paws', 'mouse', 'angry', 'angrily']
        self.assertEqual(doc._.prompt_language,prompt_language)

    def test_core_sentences(self):
        doc = holmes_manager.get_document('Aesop')      
        core_sentences = []
        self.assertEqual(doc._.core_sentences,core_sentences)


