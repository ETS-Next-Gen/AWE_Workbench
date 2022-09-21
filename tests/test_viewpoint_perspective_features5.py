#!/usr/bin/env python3.10
# Copyright 2022, Educational Testing Service

import holmes_extractor.manager as holmes
import unittest
from awe_components.components.utility_functions import print_parse_tree
from awe_workbench.pipeline import pipeline_def

holmes_manager = holmes.Manager(
    'en_core_web_lg', perform_coreference_resolution=False, number_of_workers=2, extra_components=pipeline_def)

# GRE Sample from https://www.ets.org/gre/revised_general/prepare/analytical_writing/issue/sample_responses
holmes_manager.parse_and_register_document(
            document_text="In recent centuries, humans have developed the technology very rapidly, and you may accept some merit of it, and you may see a distortion in society occured by it. To be lazy for human in some meaning is one of the fashion issues in thesedays. There are many symptoms and resons of it. However, I can not agree with the statement that the technology make humans to be reluctant to thinkng thoroughly.\n\nOf course, you can see the phenomena of human laziness along with developed technology in some place. However, they would happen in specific condition, not general. What makes human to be laze of thinking is not merely technology, but the the tendency of human that they treat them as a magic stick and a black box. Not understanding the aims and theory of them couses the disapproval problems.\n\nThe most important thing to use the thechnology, regardless the new or old, is to comprehend the fundamental idea of them, and to adapt suit tech to tasks in need. Even if you recognize a method as a all-mighty and it is extremely over-spec to your needs, you can not see the result you want. In this procedure, humans have to consider as long as possible to acquire adequate functions. Therefore, humans can not escape from using their brain.\n\nIn addition, the technology as it is do not vain automatically, the is created by humans. Thus, the more developed tech and the more you want a convenient life, the more you think and emmit your creativity to breakthrough some banal method sarcastically.\n\nConsequently, if you are not passive to the new tech, but offensive to it, you would not lose your ability to think deeply. Furthermore, you may improve the ability by adopting it.", label='GRE_Sample_Essay')


class ViewpointPerspectiveFeatureTest(unittest.TestCase):

    def test_vwp_perspective(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        perspective_spans = {'implicit': {'6': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], '29': [29, 30, 31], '34': [33, 34, 35, 36, 37, 38, 39, 40], '41': [41, 42, 43, 44, 45, 46, 47, 48, 49], '51': [50, 51, 53, 54, 55, 56, 57, 58], '52': [52], '104': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111], '113': [112, 113, 114, 115, 116, 117, 118, 119], '120': [120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143], '152': [144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156], '173': [157, 158, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191], '160': [159, 160], '245': [240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250], '262': [251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263], '267': [264, 265, 266, 267, 268, 269, 270]}, 'explicit_1': [59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 79], 'explicit_2': [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 32, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 280, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339], 'explicit_3': {72: [72, 73, 74, 75, 76, 77, 78], 227: [223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239], 276: [271, 272, 273, 274, 275, 276, 277, 278, 279, 281, 282, 283, 284]}}
        self.assertEqual(doc._.vwp_perspective_spans,
                         perspective_spans)

    def test_vwp_stance_markers(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        stance_markers = {'implicit': {'41': [46], '52': [52], '104': [100, 103], '152': [147, 149, 155], '160': [160], '173': [178], '245': [240, 243, 247], '262': [252]}, 'explicit_1': [62], 'explicit_2': [14, 15, 23, 81, 82, 84, 85, 192, 193, 194, 211, 214, 215, 220, 288, 293, 299, 302, 304, 308, 314, 320, 326, 327, 329, 332], 'explicit_3': {72: [75, 78], 227: [234, 237], 276: [283]}}
        self.assertEqual(doc._.vwp_stance_markers,
                         stance_markers)

    def test_propn_egocentric(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.propn_egocentric,
                         0.36764705882352944)

    def test_propn_allocentric(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.propn_allocentric,
                         0.11176470588235295)

    def test_propositional_attitudes(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        propositional_attitudes = {'implicit': [[[59, 79], 61, 64], [[80, 99], 84, 86], [[100, 111], 102, 104], [[112, 143], 113, 120], [[144, 156], 145, 152], [[192, 222], 214, 217], [[240, 250], 242, 245], [[301, 328], 319, 322], [[329, 339], 331, 333]], 'implicit_3': [[[33, 49], 34, 42], [[59, 79], None, 67]], 'explicit_1': [], 'explicit_2': [[[157, 191], None, 173], [[271, 300], 288, 289]], 'explicit_3': {}}
        self.assertEqual(doc._.vwp_propositional_attitudes,
                         propositional_attitudes)

    def test_emotional_states(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        emotion_states = {'explicit_1': [], 'explicit_2': [15, 212, 221], 'explicit_3': {'Humans': [75], 'Human and Humans': [133], 'Tech': [190, 281]}}
        self.assertEqual(doc._.vwp_emotion_states,
                         emotion_states)

    def test_character_traits(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        # No character traits detected in this essay.
        # We may need another test with a different text.
        character_traits = {'explicit_1': [], 'explicit_2': [293, 299, 308], 'explicit_3': {}}
        self.assertEqual(doc._.vwp_character_traits,
                         character_traits)

    def test_subjectivity_ratings(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        subjectivity_ratings = [0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.3, 0.0, 0.0, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.125, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.43333333333333335, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.45454545454545453, 0.0, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.9, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.0, 1.0, 0.0, 0.0, 0.3333333333333333, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.3, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.45454545454545453, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.assertEqual(doc._.subjectivity_ratings,
                         subjectivity_ratings)

    def test_mean_subjectivity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_subjectivity,
                         0.0971136989732031)

    def test_med_subjectivity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.median_subjectivity, 0.0)

    def test_max_subjectivity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.max_subjectivity, 1.0)

    def test_min_subjectivity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.min_subjectivity, 0.0)

    def test_std_subjectivity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdev_subjectivity,
                         0.23942774650308649)

    def test_polarity_ratings(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        polarity_ratings = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.05000000000000002, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, -0.16666666666666666, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.13636363636363635, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.0, 0.0, 0.0, -0.125, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.05, 0.0, 0.0, 0.0, 0.0, 0.3333333333333333, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.1, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.13636363636363635, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.assertEqual(doc._.polarity_ratings,
                         polarity_ratings)

    def test_mean_polarity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_polarity,
                         0.007970197846230905)

    def test_med_polarity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.median_polarity, 0.0)

    def test_max_polarity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.max_polarity, 0.5)

    def test_min_polarity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.min_polarity, -0.5)

    def test_stdev_polarity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdev_polarity,
                         0.10006321173117026)

    def test_sentiment_ratings(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        sentiment_ratings = [0, 0.1, 0, 0, 0, 0.21, 0.26, 0, 0.13, 0.19, 0, 0, 0, 0, 0.13, 0.34, 0.06, 0.48, 0, 0, 0, 0, 0, 0.13, 0.31, 0.04, -0.37, 0, 0.06, 0, -0.1, 0, 0, 0, 0.29, -0.48, 0, 0.36, 0, 0.06, 0.36, 0, 0.27, 0, 0, 0.06, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -0.08, 0, 0.19, -0.35000000000000003, 0.38, -0.54, 0, 0, -0.21, 0, 0, 0.13, 0.27, 0, 0, 0.29, -0.31, 0, 0, 0.27, 0, 0, 0, -0.06, 0, 0, 0.35000000000000003, 0.31, 0, 0, 0, 0.36, -0.27, 0, 0, 0.26, 0.13, 0, 0.06, 0.21, 0, -0.08, 0, 0, 0, -0.12, 0, -0.12, 0.17, 0, 0.38, -0.08, 0, 0, 0, 0.36, 0, 0.29, 0, 0, 0.15, 0, 0.38, 0, -0.13, 0, 0, 0, 0, 0.03, 0, -0.36, 0, 0, 0.46, 0, -0.07, 0.04, 0.54, 0.06, 0, 0.04, 0.1, 0.08, 0, 0.38, -0.53, 0, 0, 0, -0.16, 0, 0, 0, 0, -0.4, 0, 0, 0, 0, 0, 0.45, 0.13, 0, 0.04, 0, 0, 0, -0.28, 0, 0.67, 0, -0.45, 0, 0, 0, 0.39, 0, -0.01, 0.51, 0, 0, 0, 0, 0, 0.21, 0.22, 0.19, 0, 0, 0, 0.11, 0, 0.08, 0, 0, 0.28, 0.04, 0.05, -0.07, 0.04, 0.21, 0, 0.36, 0, 0, 0, 0.30000000000000004, 0.17, 0, -0.12, 0, 0, 0.15, 0, 0, -0.35000000000000003, 0.38, -0.31, 0, -0.27, 0, 0.25, 0, 0, 0, -0.18, 0, 0, 0.21, 0, 0.39, -0.07, -0.05, -0.07, 0.53, 0, 0.12, -0.07, 0, 0, 0, 0, 0, -0.35000000000000003, 0.38, -0.12, 0, 0, 0, -0.30000000000000004, 0, 0, 0, 0, 0, 0, -0.13, -0.07, 0, 0, -0.1, 0.38, 0.44, -0.26, 0, 0, 0, 0, -0.1, 0, 0, 0, 0, 0, 0, 0.26, 0.19, 0, 0, 0, 0, 0.25, 0.04, 0.53, 0.42, 0, 0, 0, 0, 0.42, 0, 0, 0, 0.68, 0, 0.33, 0.06, -0.28, 0.05, -0.19, 0, 0, 0, 0, 0, 0, 0, 0.38, 0.04, 0, 0, -0.67, -0.19, 0, 0, 0.30000000000000004, 0, 0, 0, 0, 0, 0.38, 0.35000000000000003, 0, -0.5, 0, -0.42, 0, 0, 0, 0, 0, 0.13, 0.28, 0, 0.5, -0.1, 0, 0, 0]
        self.assertEqual(doc._.sentiment_ratings,
                         sentiment_ratings)

    def test_mean_sentiment(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_sentiment, 0.059669421487603305)

    def test_med_sentiment(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.median_sentiment, 0.0)

    def test_max_sentiment(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.max_sentiment, 0.68)

    def test_min_sentiment(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.min_sentiment, -0.67)

    def test_stdev_sentiment(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdev_sentiment,
                         0.2683496906535001)

    def test_tone_ratings(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        tone_ratings = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.19, 0.0, 0.0, 0.0, 0.0, 0.065, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.065, 0.0, 0.0, -0.37, 0.0, 0.0, 0.0, -0.1, 0.0, 0.0, 0.0, 0.0, -0.48, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.19, 0.17500000000000002, -0.38, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.31, 0.0, 0.0, 0.135, 0.0, 0.0, 0.0, -0.06, 0.0, 0.0, 0.17500000000000002, 0.0, 0.0, 0.0, 0.0, 0.0, -0.27, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.17, 0.0, -0.38, 0.05000000000000002, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.38, -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, -0.03, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.07, 0.0, 0.5, 0.0, 0.0, 0.0, -0.16666666666666666, 0.0, 0.0, -0.38, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.4, 0.0, 0.0, 0.0, 0.0, 0, 0.45, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.28, 0.0, 0.13636363636363635, 0.0, -0.45, 0.0, 0.0, 0.0, 0.0, 0.0, -0.01, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.04, 0.0, 0.0, 0.0, 0.0, 0.0, -0.07, 0.0, 0.0, 0.0, 0.36, 0.0, 0.0, 0.0, -0.125, 0.0, 0.0, -0.12, 0.0, 0.0, 0.0, 0.0, 0.0, 0.17500000000000002, -0.38, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.18, 0.0, 0.0, 0.0, 0.0, 0.0, -0.07, -0.05, -0.07, 0.265, 0.0, 0.0, -0.07, 0.0, 0.0, 0.0, 0.0, 0.0, 0.17500000000000002, -0.38, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.07, 0.0, 0.0, 0.0, -0.38, -0.44, 0.0, 0.0, 0.0, 0.0, 0.0, -0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.1, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.265, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.34, 0.0, 0.0, 0.0, -0.3, 0.0, -0.19, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.38, -0.04, 0.0, 0.0, 0.13636363636363635, 0.0, 0.0, 0.0, -0.30000000000000004, 0.0, 0.0, 0.0, 0.0, 0.0, -0.38, -0.35000000000000003, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.065, 0.0, 0.0, 0.0, -0.1, 0.0, 0.0, 0.0]
        self.assertEqual(doc._.tone_ratings,
                         tone_ratings)

    def test_mean_tone(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_tone,
                         -0.02251189581768094)

    def test_med_tone(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.median_tone, 0.0)

    def test_max_tone(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.max_tone, 0.5)

    def test_min_tone(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.min_tone, -0.5)

    def test_stdev_tone(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdev_tone,
                         0.15157085308452187)

    def test_vwp_arguments(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        vwp_arguments = [5, 6, 13, 14, 15, 16, 22, 23, 24, 59, 61, 62, 63, 64, 65, 66, 67, 68, 71, 73, 74, 81, 82, 84, 85, 86, 92, 93, 94, 100, 103, 104, 125, 144, 145, 146, 147, 149, 150, 152, 153, 155, 175, 176, 178, 179, 192, 193, 194, 195, 196, 197, 198, 205, 214, 215, 216, 217, 218, 219, 220, 221, 228, 229, 230, 240, 243, 244, 246, 247, 252, 253, 271, 280, 281, 287, 288, 289, 302, 304, 306, 314, 319, 320, 321, 322, 323, 324, 325, 326, 327, 329, 331, 332, 333, 334, 335, 336]
        self.assertEqual(doc._.vwp_arguments,
                         vwp_arguments)

    def test_propn_argument_words(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.propn_argument_words,
                         0.28823529411764703)

    def test_vwp_interactives(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        vwp_interactives = [9, 13, 22, 50, 61, 78, 84, 161, 169, 192, 194, 202, 206, 211, 214, 220, 224, 234, 274, 279, 280, 287, 288, 292, 305, 311, 319, 323, 331]
        self.assertEqual(doc._.vwp_interactives,
                         vwp_interactives)

    def test_propn_interactive(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.propn_interactive,
                         0.08529411764705883)

    # This text contains no quoted or direct speech. We need
    # another test article to do proper regression on these features.
    def test_vwp_quoted(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        vwp_quoted = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.assertEqual(doc._.vwp_quoted,
                         vwp_quoted)

    def test_vwp_direct_speech_spans(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.vwp_direct_speech_spans,
                         [[[288], [280], [[271, 300]]]])

    def test_propn_direct_speech(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.propn_direct_speech,
                         0.08529411764705883)

    def test_governing_subjects(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        governing_subjects = [8, 8, 8, None, None, None, 4, None, None, 4, 4, None, None, None, None, 13, None, None, None, None, None, None, None, None, 22, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 34, 34, 34, None, None, None, 34, 34, None, None, None, None, None, None, None, None, None, None, 61, None, None, None, None, 61, 61, None, None, None, None, None, 70, None, None, 72, 72, None, 72, 72, None, None, 84, 84, None, None, None, 84, None, None, None, None, None, 88, 88, None, None, 88, None, None, None, 102, None, None, None, 102, 102, 102, 102, None, None, 102, None, None, 112, None, None, 114, 114, 114, None, 113, None, 113, 113, None, None, None, None, None, None, None, None, None, 132, None, 134, None, 134, 134, None, None, 142, None, None, None, None, None, None, None, None, None, None, 145, None, None, None, None, None, None, 160, None, None, None, None, None, None, None, 169, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 186, None, 186, 186, None, 194, None, None, 194, None, None, None, None, 202, None, None, None, None, 204, 204, None, None, 204, 204, None, 211, None, None, None, None, 214, None, None, None, 220, None, 227, None, None, None, None, 227, None, 227, 227, 227, 227, 227, None, 227, None, None, None, 242, None, None, None, None, 242, 242, 242, None, 248, None, None, 256, None, None, None, None, None, None, 258, None, None, 256, 256, None, None, None, 265, None, None, None, 276, None, None, 275, None, None, None, None, None, None, 276, None, None, None, None, None, 288, None, 288, None, 288, None, 292, None, 288, None, None, None, 288, None, None, 319, None, None, None, 305, None, 305, 305, None, 305, 305, None, None, 305, 305, None, None, None, None, None, 319, None, 323, None, 323, 323, None, 331, None, None, None, 331, None, None, 335, 335, None, None]
        self.assertEqual(doc._.governing_subjects,
                         governing_subjects)

    def test_content_segments(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        content_segments = [[33, 59], [100, 192], [192, 223], [271, 300]]
        self.assertEqual(doc._.content_segments,
                         content_segments)

    def test_prompt_related(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        prompt_related = [[23, 5.423728813559322, ['thesedays', 'reson', 'thinkng', 'emmit'], [48, 55, 77, 291]], [11, 2.024701356549909, ['human', 'brain'], [4, 37, 72, 90, 114, 130, 227, 242, 249, 269]], [9, 1.619433198380567, ['technology', 'tech'], [8, 70, 95, 123, 186, 256, 276, 312]]]
        self.assertEqual(doc._.prompt_related,
                         prompt_related)

    def test_prompt_language(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        prompt_language = ['human', 'humans', 'technology', 'however', 'agree', 'of', 'course', 'problem', 'problems', 'regard', 'regardless', 'even', 'result', 'therefore', 'add', 'addition', 'thus', 'consequent', 'consequently', 'furthermore']
        self.assertEqual(doc._.prompt_language,
                         prompt_language)

    def test_core_sentences(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        core_sentences = [[0, 33], [59, 80], [80, 100], [251, 271]]
        self.assertEqual(doc._.core_sentences,
                         core_sentences)

    def test_extended_core_sentences(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        extended_core_sentences = [[223, 240], [240, 251], [301, 329], [329, 340]]
        self.assertEqual(doc._.extended_core_sentences,
                         extended_core_sentences)
