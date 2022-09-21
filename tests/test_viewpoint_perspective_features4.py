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
            document_text="There is no current proof that advancing technology will deteriorate the ability of humans to think. On the contrary, advancements in technology had advanced our vast knowledge in many fields, opening opportunities for further understanding and achievement. For example, the problem of dibilitating illnesses and diseases such as alzheimer's disease is slowing being solved by the technological advancements in stem cell research. The future ability of growing new brain cells and the possibility to reverse the onset of alzheimer's is now becoming a reality. This shows our initiative as humans to better our health demonstrates greater ability of humans to think.\n\nOne aspect where the ability of humans may initially be seen as an example of deteriorating minds is the use of internet and cell phones. In the past humans had to seek out information in many different enviroments and aspects of life. Now humans can sit in a chair and type anything into a computer and get an answer. Our reliance on this type of technology can be detrimental if not regulated and regularily substituted for other information sources such as human interactions and hands on learning. I think if humans understand that we should not have such a reliance on computer technology, that we as a species will advance further by utilizing the opportunity of computer technology as well as the other sources of information outside of a computer. Supplementing our knowledge with internet access is surely a way for technology to solve problems while continually advancing the humaThere is no current proof that advancing technology will deteriorate the ability of humans to think. On the contrary, advancements in technology had advanced our vast knowledge in many fields, opening opportunities for further understanding and achievement. For example, the problem of dibilitating illnesses and diseases such as alzheimer's disease is slowing being solved by the technological advancements in stem cell research. The future ability of growing new brain cells and the possibility to reverse the onset of alzheimer's is now becoming a reality. This shows our initiative as humans to better our health demonstrates greater ability of humans to think.\n\nOne aspect where the ability of humans may initially be seen as an example of deteriorating minds is the use of internet and cell phones. In the past humans had to seek out information in many different enviroments and aspects of life. Now humans can sit in a chair and type anything into a computer and get an answer. Our reliance on this type of technology can be detrimental if not regulated and regularily substituted for other information sources such as human interactions and hands on learning. I think if humans understand that we should not have such a reliance on computer technology, that we as a species will advance further by utilizing the opportunity of computer technology as well as the other sources of information outside of a computer. Supplementing our knowledge with internet access is surely a way for technology to solve problems while continually advancing the human race.", label='GRE_Sample_Essay')


class ViewpointPerspectiveFeatureTest(unittest.TestCase):

    def test_vwp_perspective(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        perspective_spans = {'implicit': {'1': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], '25': [17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 29, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40], '30': [30], '57': [41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68], '51': [51], '89': [69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92], '94': [93, 94, 96, 97, 98, 99, 100, 110], '104': [104], '129': [111, 112, 113, 129, 130, 131, 132, 133, 134, 135, 136, 137], '122': [114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128], '142': [138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 149, 150, 151, 152, 153, 154, 155], '148': [148], '254': [248, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 283], '268': [268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282], '292': [284, 285, 286, 287, 288, 289, 290, 291, 292, 294, 295, 296, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307], '297': [297], '324': [308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335], '318': [318], '356': [336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359], '361': [360, 361, 363, 364, 365, 366, 367, 377], '371': [371], '396': [378, 379, 380, 396, 397, 398, 399, 400, 401, 402, 403, 404], '389': [381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395], '409': [405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 416, 417, 418, 419, 420, 421, 422], '415': [415], '521': [515, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536]}, 'explicit_1': [26, 95, 101, 102, 103, 105, 106, 107, 108, 109, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 221, 247, 249, 293, 362, 368, 369, 370, 372, 373, 374, 375, 376, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 488, 514, 516], 'explicit_2': [], 'explicit_3': {157: [156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173], 206: [205, 206, 207, 208, 219, 220, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246], 424: [423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440], 473: [472, 473, 474, 475, 486, 487, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513]}}

        self.assertEqual(doc._.vwp_perspective_spans,
                         perspective_spans)

    def test_vwp_stance_markers(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        stance_markers = {'implicit': {'1': [4, 15], '25': [17, 20, 28, 34], '30': [30], '57': [41, 45, 52], '89': [79], '94': [94, 96], '104': [104], '122': [119, 122, 123, 124, 125, 126], '148': [148], '254': [250, 255, 262], '268': [271, 282], '292': [284, 287, 295, 301], '297': [297], '324': [308, 312, 319], '356': [346], '361': [361, 363], '371': [371], '389': [386, 389, 390, 391, 392, 393], '415': [415], '521': [517, 522, 529]}, 'explicit_1': [103, 109, 181, 183, 184, 210, 221, 370, 376, 448, 450, 451, 477, 488], 'explicit_2': [], 'explicit_3': {157: [158], 206: [205, 236], 424: [425], 473: [472, 503]}}
        self.assertEqual(doc._.vwp_stance_markers,
                         stance_markers)

    def test_propn_egocentric(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.propn_egocentric,
                         0.515828677839851)

    def test_propn_allocentric(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.propn_allocentric,
                         0.186219739292365)

    def test_propositional_attitudes(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        propositional_attitudes = {'implicit': [[[0, 16], None, 1], [[0, 16], None, 4], [[156, 173], 157, 159], [[174, 202], 175, 182], [[248, 283], 248, 254], [[268, 282], None, 271], [[423, 440], 424, 426], [[441, 469], 442, 449], [[515, 536], 515, 521]], 'implicit_3': [[[17, 40], 21, 25], [[41, 68], 48, 57], [[69, 92], 76, 89], [[284, 307], 288, 292], [[308, 335], 315, 324], [[336, 359], 343, 356]], 'explicit_1': [[[203, 247], 203, 204], [[470, 514], 470, 471]], 'explicit_2': [], 'explicit_3': {206: [[[205, 218], 206, 207]], 473: [[[472, 485], 473, 474]]}}
        self.assertEqual(doc._.vwp_propositional_attitudes,
                         propositional_attitudes)

    def test_emotional_states(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        emotion_states = {'explicit_1': [], 'explicit_2': [], 'explicit_3': {}}
        self.assertEqual(doc._.vwp_emotion_states,
                         emotion_states)

    def test_character_traits(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        # No character traits detected in this essay.
        # We may need another test with a different text.
        character_traits = {'explicit_1': [], 'explicit_2': [], 'explicit_3': {}}
        self.assertEqual(doc._.vwp_character_traits,
                         character_traits)

    def test_subjectivity_ratings(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        subjectivity_ratings = [0.0, 0.0, 0.0, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6, 0.0, 1.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.125, 0.0, 0.0, 0.0, 0.45454545454545453, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.8500000000000001, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.375, 0.0, 0.0, 0.5, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.375, 0.0, 0.0, 0.0, 0.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.8888888888888888, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6, 0.0, 1.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.125, 0.0, 0.0, 0.0, 0.45454545454545453, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.8500000000000001, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.375, 0.0, 0.0, 0.5, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.375, 0.0, 0.0, 0.0, 0.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.8888888888888888, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0]
        self.assertEqual(doc._.subjectivity_ratings,
                         subjectivity_ratings)

    def test_mean_subjectivity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_subjectivity,
                         0.045381197870824425)

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
                         0.1638519638285082)

    def test_polarity_ratings(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        polarity_ratings = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.13636363636363635, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.45, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.125, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.125, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.13636363636363635, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.45, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.125, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.125, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.assertEqual(doc._.polarity_ratings,
                         polarity_ratings)

    def test_mean_polarity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_polarity,
                         0.014824594492644285)

    def test_med_polarity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.median_polarity, 0.0)

    def test_max_polarity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.max_polarity, 0.5)

    def test_min_polarity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.min_polarity, -0.25)

    def test_stdev_polarity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdev_polarity,
                         0.08965735351867955)

    def test_sentiment_ratings(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        sentiment_ratings = [0, 0, 0.08, -0.13, -0.34, 0, 0, 0.13, 0.08, -0.34, 0, 0.5, 0, 0, 0, 0.42, 0, 0.08, 0, -0.4, 0, 0, 0, 0.13, 0, 0.28, 0, 0.17, 0.5700000000000001, 0, 0, 0, 0, 0.23, 0, 0, 0.19, 0.53, 0, 0.5700000000000001, 0, 0, -0.02, 0, 0, -0.37, 0, 0, 0, 0, 0, -0.07, -0.07, 0, 0, -0.8300000000000001, 0, 0, 0, 0, -0.1, 0, 0.07, 0, 0, 0.02, -0.22, 0.37, 0, 0, 0.42, 0.5, 0, 0, 0.67, 0.30000000000000004, 0, 0, 0, 0.38, 0, -0.34, 0, -0.16, 0, 0, 0, 0, 0.06, 0.28, 0.04, 0.31, 0, 0, 0, 0, 0.42, -0.07, 0, 0, 0.44, 0, 0.46, 0, 0.62, 0.5, 0, 0, 0, 0.42, 0, 0, 0.27, -0.02, 0, 0, 0.5, 0, 0, 0.13, 0, 0.29, 0, -0.07, -0.07, -0.02, 0, 0, 0, 0, 0, 0.04, 0, 0.42, 0, -0.22, 0, 0, 0, 0, 0.02, 0, 0, 0, 0.31, -0.30000000000000004, 0.33, 0, 0, 0.22, 0, 0, 0, 0, 0.42, 0, 0.06, 0, 0.35000000000000003, 0.2, 0, 0.04, 0.22, 0, 0.26, 0, 0, 0.04, 0.46, 0, 0.27, -0.07, 0.27, 0, 0, 0.5700000000000001, 0.08, 0, 0.26, 0, 0.13, 0.35000000000000003, 0.29, -0.42, 0, 0.38, 0, 0, 0, 0, 0, -0.1, -0.33, 0, 0.07, 0.07, -0.36, 0, 0, 0, -0.08, -0.35000000000000003, 0, -0.19, 0.42, 0, 0, 0.42, 0, 0, 0, 0.38, -0.21, 0.07, -0.04, -0.5700000000000001, -0.08, -0.46, -0.13, 0, 0, 0, -0.07, 0.04, 0.06, 0.08, 0.27, 0.19, -0.1, 0, 0, 0.52, 0, 0.46, 0.13, -0.07, 0.65, -0.07, 0, 0.1, 0, 0, 0.33, 0.05, 0, 0.04, 0.46, 0, 0, 0, 0.5700000000000001, 0, 0.42, 0.42, 0, 0.41000000000000003, 0.04, 0.22, 0, 0.13, 0, 0.32, 0, 0, 0.12, 0, 0, 0, 0, 0.08, -0.13, -0.34, 0, 0, 0.13, 0.08, -0.34, 0, 0.5, 0, 0, 0, 0.42, 0, 0.08, 0, -0.4, 0, 0, 0, 0.13, 0, 0.28, 0, 0.17, 0.5700000000000001, 0, 0, 0, 0, 0.23, 0, 0, 0.19, 0.53, 0, 0.5700000000000001, 0, 0, -0.02, 0, 0, -0.37, 0, 0, 0, 0, 0, -0.07, -0.07, 0, 0, -0.8300000000000001, 0, 0, 0, 0, -0.1, 0, 0.07, 0, 0, 0.02, -0.22, 0.37, 0, 0, 0.42, 0.5, 0, 0, 0.67, 0.30000000000000004, 0, 0, 0, 0.38, 0, -0.34, 0, -0.16, 0, 0, 0, 0, 0.06, 0.28, 0.04, 0.31, 0, 0, 0, 0, 0.42, -0.07, 0, 0, 0.44, 0, 0.46, 0, 0.62, 0.5, 0, 0, 0, 0.42, 0, 0, 0.27, -0.02, 0, 0, 0.5, 0, 0, 0.13, 0, 0.29, 0, -0.07, -0.07, -0.02, 0, 0, 0, 0, 0, 0.04, 0, 0.42, 0, -0.22, 0, 0, 0, 0, 0.02, 0, 0, 0, 0.31, -0.30000000000000004, 0.33, 0, 0, 0.22, 0, 0, 0, 0, 0.42, 0, 0.06, 0, 0.35000000000000003, 0.2, 0, 0.04, 0.22, 0, 0.26, 0, 0, 0.04, 0.46, 0, 0.27, -0.07, 0.27, 0, 0, 0.5700000000000001, 0.08, 0, 0.26, 0, 0.13, 0.35000000000000003, 0.29, -0.42, 0, 0.38, 0, 0, 0, 0, 0, -0.1, -0.33, 0, 0.07, 0.07, -0.36, 0, 0, 0, -0.08, -0.35000000000000003, 0, -0.19, 0.42, 0, 0, 0.42, 0, 0, 0, 0.38, -0.21, 0.07, -0.04, -0.5700000000000001, -0.08, -0.46, -0.13, 0, 0, 0, -0.07, 0.04, 0.06, 0.08, 0.27, 0.19, -0.1, 0, 0, 0.52, 0, 0.46, 0.13, -0.07, 0.65, -0.07, 0, 0.1, 0, 0, 0.33, 0.05, 0, 0.04, 0.46, 0, 0, 0, 0.5700000000000001, 0, 0.42, 0.42, 0, 0.41000000000000003, 0.04, 0.22, 0, 0.13, 0, 0.32, 0, 0, 0.12, 0, 0, 0.36, 0.11, 0]
        self.assertEqual(doc._.sentiment_ratings,
                         sentiment_ratings)

    def test_mean_sentiment(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_sentiment, 0.11572614107883818)

    def test_med_sentiment(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.median_sentiment, 0.0)

    def test_max_sentiment(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.max_sentiment, 0.67)

    def test_min_sentiment(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.min_sentiment,
                         -0.8300000000000001)

    def test_stdev_sentiment(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdev_sentiment,
                         0.2783455430853229)

    def test_tone_ratings(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        tone_ratings = [0.0, 0.0, -0.08, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.34, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.28, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.02, 0.0, 0.0, -0.37, 0.0, 0.0, 0.0, 0.0, 0.0, -0.07, -0.07, 0.0, 0.0, -0.8300000000000001, 0.0, 0.0, 0.0, 0.0, -0.1, 0.0, 0.0, 0.0, 0.0, 0.0, -0.22, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.13636363636363635, 0.0, 0.0, 0.0, 0.0, 0.19, 0.0, -0.34, 0.0, -0.16, 0.0, 0.0, 0.0, 0.0, 0.0, 0.28, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.21, -0.07, 0.0, 0.0, 0.44, 0.0, 0.0, 0.0, 0.62, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.02, 0.0, 0.0, 0.0, 0.0, 0.0, 0.065, 0.0, 0.0, 0.0, -0.07, -0.07, -0.02, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.22, 0.0, 0.0, 0.0, 0.0, -0.25, 0.0, 0.0, 0.0, 0.0, -0.30000000000000004, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.17500000000000002, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.07, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.17500000000000002, 0.0, -0.42, 0.0, -0.38, 0.0, 0.0, 0.0, 0.0, 0.0, -0.125, 0.0, 0.0, -0.07, -0.07, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.19, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.38, 0.0, -0.07, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.07, 0.0, 0.0, 0.0, 0.0, 0.0, -0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.07, 0.325, -0.07, 0.0, -0.125, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.08, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.34, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.28, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.02, 0.0, 0.0, -0.37, 0.0, 0.0, 0.0, 0.0, 0.0, -0.07, -0.07, 0.0, 0.0, -0.8300000000000001, 0.0, 0.0, 0.0, 0.0, -0.1, 0.0, 0.0, 0.0, 0.0, 0.0, -0.22, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.13636363636363635, 0.0, 0.0, 0.0, 0.0, 0.19, 0.0, -0.34, 0.0, -0.16, 0.0, 0.0, 0.0, 0.0, 0.0, 0.28, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.21, -0.07, 0.0, 0.0, 0.44, 0.0, 0.0, 0.0, 0.62, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.02, 0.0, 0.0, 0.0, 0.0, 0.0, 0.065, 0.0, 0.0, 0.0, -0.07, -0.07, -0.02, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.22, 0.0, 0.0, 0.0, 0.0, -0.25, 0.0, 0.0, 0.0, 0.0, -0.30000000000000004, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.17500000000000002, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.07, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.17500000000000002, 0.0, -0.42, 0.0, -0.38, 0.0, 0.0, 0.0, 0.0, 0.0, -0.125, 0.0, 0.0, -0.07, -0.07, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.19, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.38, 0.0, -0.07, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.07, 0.0, 0.0, 0.0, 0.0, 0.0, -0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.07, 0.325, -0.07, 0.0, -0.125, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.assertEqual(doc._.tone_ratings,
                         tone_ratings)

    def test_mean_tone(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_tone, -0.01023764617125613)

    def test_med_tone(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.median_tone, 0.0)

    def test_max_tone(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.max_tone, 0.62)

    def test_min_tone(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.min_tone,
                         -0.8300000000000001)

    def test_stdev_tone(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdev_tone,
                         0.14640313944514674)

    def test_vwp_arguments(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        vwp_arguments = [0, 1, 2, 4, 5, 6, 11, 14, 15, 17, 18, 19, 20, 24, 25, 26, 28, 29, 41, 42, 44, 45, 46, 51, 52, 56, 57, 58, 59, 60, 71, 78, 79, 80, 94, 95, 96, 97, 103, 104, 105, 106, 108, 109, 114, 116, 119, 122, 123, 124, 125, 126, 174, 175, 181, 183, 184, 185, 193, 194, 195, 197, 200, 201, 203, 204, 205, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 220, 221, 222, 225, 226, 227, 228, 231, 236, 237, 250, 254, 255, 261, 262, 263, 269, 271, 272, 273, 278, 281, 282, 284, 285, 286, 287, 291, 292, 293, 295, 296, 308, 309, 311, 312, 313, 318, 319, 323, 324, 325, 326, 327, 338, 345, 346, 347, 361, 362, 363, 364, 370, 371, 372, 373, 375, 376, 381, 383, 386, 389, 390, 391, 392, 393, 441, 442, 448, 450, 451, 452, 460, 461, 462, 464, 467, 468, 470, 471, 472, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 487, 488, 489, 492, 493, 494, 495, 498, 503, 504, 517, 521, 522, 528, 529, 530]
        self.assertEqual(doc._.vwp_arguments,
                         vwp_arguments)

    def test_propn_argument_words(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.propn_argument_words,
                         0.3426443202979516)

    def test_vwp_interactives(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        vwp_interactives = [0, 26, 51, 54, 74, 86, 93, 95, 101, 140, 165, 174, 177, 194, 203, 209, 213, 221, 249, 293, 318, 321, 341, 353, 360, 362, 368, 407, 432, 441, 444, 461, 470, 476, 480, 488, 516]
        self.assertEqual(doc._.vwp_interactives,
                         vwp_interactives)

    def test_propn_interactive(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.propn_interactive,
                         0.06890130353817504)

    # This text contains no quoted or direct speech. We need another test article
    # to do proper regression on these features.
    def test_vwp_quoted(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        vwp_quoted = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.assertEqual(doc._.vwp_quoted, vwp_quoted)

    def test_vwp_direct_speech_spans(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.vwp_direct_speech_spans, [])

    def test_propn_direct_speech(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.propn_direct_speech, 0.0)

    def test_governing_subjects(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        governing_subjects = [None, None, None, None, None, None, None, None, None, 7, None, None, None, None, None, None, None, 28, None, None, None, None, None, None, None, 21, None, 26, 26, 26, 31, None, None, 21, None, None, None, None, None, None, None, 48, None, None, None, None, None, None, None, None, None, None, None, None, None, 53, None, 48, None, 48, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 76, 76, None, 76, None, None, 93, None, 95, None, None, None, 98, None, 101, 102, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 116, None, None, None, None, None, None, 113, None, 113, 113, None, None, None, None, None, 141, None, 141, None, 141, None, 141, None, None, 146, None, None, None, None, None, None, None, None, 157, None, None, 157, 157, None, None, None, 157, None, 165, None, None, None, 157, None, None, None, None, 174, 174, None, None, None, None, None, 175, 175, None, None, 175, None, 175, 175, 175, None, None, None, None, None, None, None, None, None, None, None, None, None, 203, None, None, 206, None, None, None, None, 209, None, None, None, None, None, None, None, None, None, None, None, None, None, 221, 221, 221, 221, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 249, 250, None, None, 248, None, None, None, None, None, None, 259, None, None, 259, 259, None, None, None, None, None, None, None, None, None, None, 274, None, None, None, None, None, None, None, 295, None, None, None, None, None, None, None, 288, None, 293, 293, 293, 298, None, None, 288, None, None, None, None, None, None, None, 315, None, None, None, None, None, None, None, None, None, None, None, None, None, 320, None, 315, None, 315, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 343, 343, None, 343, None, None, 360, None, 362, None, None, None, 365, None, 368, 369, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 383, None, None, None, None, None, None, 380, None, 380, 380, None, None, None, None, None, 408, None, 408, None, 408, None, 408, None, None, 413, None, None, None, None, None, None, None, None, 424, None, None, 424, 424, None, None, None, 424, None, 432, None, None, None, 424, None, None, None, None, 441, 441, None, None, None, None, None, 442, 442, None, None, 442, None, 442, 442, 442, None, None, None, None, None, None, None, None, None, None, None, None, None, 470, None, None, 473, None, None, None, None, 476, None, None, None, None, None, None, None, None, None, None, None, None, None, 488, 488, 488, 488, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 516, 517, None, None, 515, 515, None, 515, None, None, None, 526, None, None, 526, 526, None, None, None, None]
        self.assertEqual(doc._.governing_subjects,
                         governing_subjects)

    def test_content_segments(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        content_segments = [[41, 111], [138, 174], [308, 378], [405, 441]]
        self.assertEqual(doc._.content_segments,
                         content_segments)

    def test_prompt_related(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        prompt_related = [[23, 4.43795914259837, ['human', 'brain', 'mind'], [13, 75, 98, 107, 118, 128, 141, 157, 196, 206, 280, 342, 365, 374, 385, 395, 408, 424, 463, 473, 534]], [14, 3.966699314397649, ['technology', 'advancement', 'technological'], [7, 21, 23, 62, 63, 180, 218, 234, 259, 274, 288, 290, 329, 330, 447, 485, 501, 526]], [2, 3.8626609442060085, ['dibilitating', 'enviroment', 'detrimental'], [47, 150, 183, 314, 417, 450]]]
        self.assertEqual(doc._.prompt_related,
                         prompt_related)

    def test_prompt_language(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        prompt_language = ['proof', 'technology', 'human', 'humans', 'contrary', 'knowledge', 'problem', 'brain', 'show', 'shows', 'initiate', 'initiative', 'demonstrate', 'demonstrates', 'initial', 'initially', 'mind', 'minds', 'detriment', 'detrimental', 'think', 'further', 'far', 'sure', 'surely']
        self.assertEqual(doc._.prompt_language,
                         prompt_language)

    def test_core_sentences(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        core_sentences = [[0, 17], [111, 138], [174, 203], [203, 248], [248, 284], [378, 405], [441, 470], [470, 515], [515, 537]]
        self.assertEqual(doc._.core_sentences,
                         core_sentences)

    def test_extended_core_sentences(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        extended_core_sentences = [[17, 41], [284, 308]]
        self.assertEqual(doc._.extended_core_sentences,
                         extended_core_sentences)
