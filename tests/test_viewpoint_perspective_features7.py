#!/usr/bin/env python3.10
# Copyright 2022, Educational Testing Service

import holmes_extractor.manager as holmes
import unittest
from awe_components.components.utility_functions import print_parse_tree
from awe_workbench.pipeline import pipeline_def

holmes_manager = holmes.Manager(
    'en_core_web_lg', perform_coreference_resolution=False, number_of_workers=2, extra_components=pipeline_def)

document_text = "She took me by the hand and walked me into the lobby like a five-year old child. Didn’t she know I was pushing 15? This was the third home Nancy was placing me in - in a span of eight months. I guess she felt a little sorry for me. The bright fluorescent lights threatened to burn my skin as I walked towards a bouncy-looking lady with curly hair and a sweetly-smiling man. They called themselves Allie and Alex. Cute, I thought.\n\nAfter they exchanged the usual reams of paperwork, it was off in their Chevy Suburban to get situated into another new home. This time, there were no other foster children and no other biological children. Anything could happen.\n\nOver the next few weeks, Allie, Alex, and I fell into quite a nice routine. She’d make pancakes for breakfast, or he’d fry up some sausage and eggs. They sang a lot, even danced as they cooked. They must have just bought the house because, most weekends, we were painting a living room butter yellow or staining a coffee table mocha brown.\n\nI kept waiting for the other shoe to drop. When would they start threatening a loss of pancakes if I didn’t mow the lawn? When would the sausage and eggs be replaced with unidentifiable slosh because he didn’t feel like cooking in the morning? But, it never happened. They kept cooking, singing, and dancing like a couple of happy fools.\n\nIt was a Saturday afternoon when Allie decided it was time to paint the brick fireplace white. As we crawled closer to the dirty old firepit, we pulled out the petrified wood and noticed a teeny, tiny treasure box. We looked at each other in wonder and excitement. She actually said, “I wonder if the leprechauns left it!” While judging her for being such a silly woman, I couldn’t help but laugh and lean into her a little.\n\nTogether, we reached for the box and pulled it out. Inside was a shimmering solitaire ring. Folded underneath was a short piece of paper that read:\n\n“My darling, my heart. Only 80 days have passed since I first held your hand. I simply cannot imagine my next 80 years without you in them. Will you take this ring, take my heart, and build a life with me? This tiny little solitaire is my offering to you. Will you be my bride?”\n\nAs I stared up at Allie, she asked me a question. “Do you know what today is?” I shook my head. “It’s May 20th. That’s 80 days since Nancy passed your hand into mine and we took you home.”\n\nIt turns out, love comes in all shapes and sizes, even a teeny, tiny treasure box from a wonderfully silly lady who believes in leprechauns."

holmes_manager.parse_and_register_document(document_text, label='Personal Narrative')


class ViewpointPerspectiveFeatureTest2(unittest.TestCase):

    def test_vwp_perspective(self):
        doc = holmes_manager.get_document('Personal Narrative')
        perspective_spans = {'implicit': {'30': [29, 30, 31, 32, 33, 46], '36': [34, 35, 36, 38, 39, 40, 41, 42, 43, 44, 45], '61': [57, 58, 59, 60, 61, 62, 63, 65, 84], '73': [71, 72, 73], '86': [85, 86, 87, 88, 89, 90, 91], '108': [97, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121], '100': [98, 99, 100, 101, 103, 104, 105], '102': [102], '126': [122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136], '139': [137, 138, 139, 140], '163': [161, 162, 163, 164, 165, 166, 167, 168], '171': [169, 170, 171, 172, 173, 174, 175, 176, 177], '179': [178, 179, 180, 181, 182, 183, 184, 188], '187': [185, 186, 187], '193': [189, 190, 191, 192, 193, 194, 195, 216], '198': [198], '231': [228, 229, 230, 231, 232, 233, 234, 235, 236, 244], '271': [267, 268, 269, 270, 271, 272], '274': [273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287], '393': [392, 393, 394, 395, 396, 397, 398], '401': [399, 400, 401, 402, 403, 404, 405, 406, 409, 410, 411, 413, 414, 416, 417], '408': [407, 408], '422': [418, 419, 420, 421, 422, 429], '465': [461, 462, 463, 464, 465, 467, 468, 470], '508': [506, 507, 508, 509, 510, 511], '513': [512, 513, 514, 515, 523], '518': [516, 517, 518, 520, 521], '532': [530, 531, 532, 533], '536': [534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 554, 559], '553': [552, 553], '556': [555, 556, 557, 558]}, 'explicit_1': [2, 8, 24, 37, 47, 48, 55, 56, 64, 66, 67, 68, 69, 70, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 92, 93, 94, 95, 96, 153, 196, 197, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 237, 238, 239, 240, 241, 242, 243, 295, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 347, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 412, 415, 423, 424, 425, 426, 427, 428, 430, 435, 466, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 501, 502, 503, 504, 505, 522, 524, 525, 526, 527, 528, 529], 'explicit_2': [440, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 469, 471, 472, 473, 474, 475, 476, 477, 494, 519], 'explicit_3': {0: [0, 1, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 25, 26, 27, 28], 34: [34, 49, 50, 51, 52, 53, 54], 150: [141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 154, 155, 156, 157, 158, 159, 160, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266], 295: [288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 342, 343, 344, 345, 346, 354, 355], 347: [348, 349, 350, 351, 352, 353], 430: [431, 432, 433, 434, 436, 437, 438, 439, 441, 442, 443], 494: [492, 493, 495, 496, 497, 498, 499, 500]}}
        self.assertEqual(doc._.vwp_perspective_spans,
                         perspective_spans)

    def test_vwp_stance_markers(self):
        doc = holmes_manager.get_document('Personal Narrative')
        stance_markers = {'implicit': {'61': [61], '73': [73], '102': [102], '139': [138], '163': [168], '179': [183], '193': [190, 192], '198': [198], '231': [229, 232, 244], '271': [270], '408': [408], '422': [418], '536': [543], '553': [552, 553], '556': [556]}, 'explicit_1': [2, 8, 24, 55, 153, 237, 333, 347, 363, 367, 430, 435], 'explicit_2': [460, 476], 'explicit_3': {0: [28], 150: [145, 158, 246, 266], 295: [343, 354], 347: [349], 430: [431, 432], 494: [499]}}
        self.assertEqual(doc._.vwp_stance_markers,
                         stance_markers)

    def test_propn_egocentric(self):
        doc = holmes_manager.get_document('Personal Narrative')
        self.assertEqual(doc._.propn_egocentric, 0.2642857142857143)

    def test_propn_allocentric(self):
        doc = holmes_manager.get_document('Personal Narrative')
        self.assertEqual(doc._.propn_allocentric, 0.18571428571428572)

    def test_propositional_attitudes(self):
        doc = holmes_manager.get_document('Personal Narrative')
        propositional_attitudes = {'implicit': [[[20, 28], 22, 23], [[122, 136], None, 126], [[122, 136], None, 130], [[137, 140], 137, 139], [[189, 216], 189, 193], [[228, 244], 230, 231], [[245, 266], 248, 252], [[267, 272], 269, 271], [[342, 355], 342, 344], [[356, 378], 366, 369], [[430, 443], 430, 434]], 'implicit_3': [], 'explicit_1': [[[47, 56], 47, 48]], 'explicit_2': [], 'explicit_3': {0: [[[0, 19], 0, 23]], 295: [[[288, 306], 295, 344]]}}
        self.assertEqual(doc._.vwp_propositional_attitudes,
                         propositional_attitudes)

    def test_emotion_states(self):
        doc = holmes_manager.get_document('Personal Narrative')
        emotion_states = {'explicit_1': [338, 340, 371], 'explicit_2': [], 'explicit_3': {'Nancy': [50, 53], 'Lady': [71], 'Alex and Allie': [179, 184, 277, 280, 285], 'Alex': [260]}}
        self.assertEqual(doc._.vwp_emotion_states,
                         emotion_states)

    def test_character_traits(self):
        doc = holmes_manager.get_document('Personal Narrative')
        character_traits = {'explicit_1': [],
                            'explicit_2': [],
                            'explicit_3': {'Alex and Allie': [286],
                                           'Lady': [553]}}
        self.assertEqual(doc._.vwp_character_traits,
                         character_traits)

    def test_subjectivity_ratings(self):
        doc = holmes_manager.get_document('Personal Narrative')
        subjectivity_ratings = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 1.0, 0.0, 0.0, 0.0, 0.0, 0.7999999999999999, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.65, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.45454545454545453, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.375, 0.0, 0.0, 0.0, 0.0, 0.375, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.375, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.8, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.375, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3333333333333333, 0.0, 0.0, 0.0, 0.0, 0.0, 0.35714285714285715, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 1.0, 0.875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.assertEqual(doc._.subjectivity_ratings, subjectivity_ratings)

    def test_mean_subjectivity(self):
        doc = holmes_manager.get_document('Personal Narrative')
        self.assertEqual(doc._.mean_subjectivity, 0.06680634636299661)

    def test_med_subjectivity(self):
        doc = holmes_manager.get_document('Personal Narrative')
        self.assertEqual(doc._.median_subjectivity, 0.0)

    def test_max_subjectivity(self):
        doc = holmes_manager.get_document('Personal Narrative')
        self.assertEqual(doc._.max_subjectivity, 1.0)

    def test_min_subjectivity(self):
        doc = holmes_manager.get_document('Personal Narrative')
        self.assertEqual(doc._.min_subjectivity, 0.0)

    def test_std_subjectivity(self):
        doc = holmes_manager.get_document('Personal Narrative')
        self.assertEqual(doc._.stdev_subjectivity, 0.20841701513602512)

    def test_polarity_ratings(self):
        doc = holmes_manager.get_document('Personal Narrative')
        polarity_ratings = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.1875, -0.5, 0.0, 0.0, 0.0, 0.0, 0.7000000000000001, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.35, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.13636363636363635, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.125, 0.0, 0.0, 0.0, 0.0, -0.125, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.125, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.6, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.125, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0, -0.1875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.1875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.assertEqual(doc._.polarity_ratings, polarity_ratings)

    def test_mean_polarity(self):
        doc = holmes_manager.get_document('Personal Narrative')
        self.assertEqual(doc._.mean_polarity, 0.00824563367666816)

    def test_med_polarity(self):
        doc = holmes_manager.get_document('Personal Narrative')
        self.assertEqual(doc._.median_polarity, 0.0)

    def test_max_polarity(self):
        doc = holmes_manager.get_document('Personal Narrative')
        self.assertEqual(doc._.max_polarity, 1.0)

    def test_min_polarity(self):
        doc = holmes_manager.get_document('Personal Narrative')
        self.assertEqual(doc._.min_polarity, -0.6)

    def test_stdev_polarity(self):
        doc = holmes_manager.get_document('Personal Narrative')
        self.assertEqual(doc._.stdev_polarity, 0.14514011197364973)

    def test_sentiment_ratings(self):
        doc = holmes_manager.get_document('Personal Narrative')
        sentiment_ratings = [0, 0, 0, -0.1, 0, 0.22, 0, 0, 0, 0, 0, -0.06, 0.61, 0.04, 0.1, 0, 0.18, -0.45, 0.55, 0, 0, 0, 0, -0.45, -0.19, 0, 0, 0, 0, 0, 0, 0, 6.000000000000001e-05, 0.62, 0, 0, 0, 0, 0, 0, 0, 0.04, 0.18, 0, 0.09, 0, 0, -0.19, 0.04, 0, 0, 0.04, 0.22, -0.04, 0, 0, 0, 0, 0.46, 0.04, 0, -0.6000000000000001, 0, -0.31, 0, 0.19, -0.07, -0.19, 0, 0, 0.04, 0.41000000000000003, 0, 0.1, 0.47000000000000003, 0, 0, 0.29, 0, 0.04, 0.6900000000000001, 0, 0.72, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0.64, 0, -0.19, 0.44, 0, 0, 0, 0, 0.34, 0, 0.12, 0, 0, -0.18, 0, 0, 0, -0.04, 0, 0, -0.07, 0.21, 0, 0.27, 0, 0, -0.07, 0.67, 0.62, 0, 0, 0.15, 0, 0, 0, -0.08, 0.1, 0.18, 0, 0, -0.08, 0.1, 0.39, 0, 0, 0, 0, 0.12, 0, 0, 0.17, 0, 0.00519, 0, 0, 0, 0, 0, 0, 0, 0, -0.19, -0.38, 0, 0.03, 0.04, 0.48, -0.01, 0, 0, 0, 0.27, 0, 0, 0.59, 0, 0, 0, 0, 0.23, 0.34, 0.06, 0.33, 0, 0, 0, 0, 0, 0.04, 0.03, 0, 0.08, 0, -0.07, 0, 0, 0, 0, 0.11, 0.21, 0.39, 0, 0, 0.54, 0, 0, 0, 0, 0, 0, 0, 0.47000000000000003, 0.04, 0.2, 0.13, 0.34, 0.27, 0, 0, 0.04, 0.5, 0.12, 0.38, 0.13, 0, 0, -0.19, -0.34, 0.15, 0, 0, 0.1, 0.19, 0, -0.19, 0, 0, 0, 0, 0.35000000000000003, -0.30000000000000004, 0.04, -0.52, 0, 0, 0, 0.19, 0, 0, 0.01, 0, -0.26, 0, 0, 0, 0, 0.33, 0, 0, 0.29, 0, 0, -0.34, -0.02, 0, 0, 0, 0, -0.31, -0.61, -0.44, 0, 0, -0.35000000000000003, 0, 0, 0, 0, 0.39, 0, 0, 0, -0.34, 0.44, 0, 0, 0, 0, 0, 0.61, 0.04, 0.52, 0, 0.86, 0, 0, 0, 0, 0, 0.04, 0, 0.42, 0, 0, 0.21, 0, 0, 0.15, 0, 0.18, 0, -0.08, 0.23, 0.29, 0, -0.07, 0, 0, 0, 0, 0, -0.45, -0.45, 0, 0, 0, 0, -0.30000000000000004, 0, 0, 0.2, 0, 0.23, 0.04, 0.15, 0, 0.02, 0.66, 0.08, 0, 0, 0, 0, 0, 0.1, 0, 0.42, 0, 0.65, 0, 0, 0.16, 0, 0, 0, -0.19, 0.42, 0, 0, 0, -0.01, 0, 0, 0, 0, 0, 0, 0, 0, 0.07, -0.04, -0.43, -0.52, 0, 0.19, 0, 0, -0.48, 0, -0.64, 0, -0.33, 0, 0, -0.04, -0.22, 0, 0, 0.17, 0, 0, 0, 0, 0, 0.08, 0, 0, 0, -0.30000000000000004, 0, 0.02, 0, 0.04, 0, 0.15, 0.52, 0, 0, 0, 0, 0.04, 0.16, 0.05, 0, 0.1, 0, 0.43, 0, 0, 0, 0, 0.58, 0, 0, 0.48, 0, 0.07, 0, 0, 0.21, 0, 0, -0.19, 0.58, 0, 0, 0.22, 0, 0.19, -0.30000000000000004, -0.35000000000000003, 0.38, -0.55, 0, -0.00519, 0, 0, 0, 0, 0, 0, 0, 0.08, 0, -0.04, 0, 0.52, 0, -0.04, 0, 0.48, 0, 0, 0.33, 0.04, 0.42, 0, 0, 0, 0, 0.02, 0.22, 0.15, 0, 0, 0.12, 0, 0, 0, 0.08, 0, 0.29, 0, 0.45, 0, 0, 0, -0.07, -0.19, 0, 0.34, 0, 0, 0, 0, 0, 0, 0.04, 0.34, 0, 0, 0.1, 0, 0.45, 0, 0.15, 0, 0, 0, -0.19, 0, 0, 0.21, 0, 0, 0, 0, 0.13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.22, 0, -0.02, 0, 0, 0, 0, 0.62, 0, 0, 0, 0, 0, -0.30000000000000004, 0, 0.75, 0, 0, 0.21, 0, 0, 0, 0, 0.08, 0.04, 0.15, 0, 0.02, 0.66, 0.08, 0, 0.04, 0.6000000000000001, 0.43, 0.47000000000000003, 0, 0, 0, 0, 0]
        self.assertEqual(doc._.sentiment_ratings, sentiment_ratings)

    def test_mean_sentiment(self):
        doc = holmes_manager.get_document('Personal Narrative')
        self.assertEqual(doc._.mean_sentiment, 0.1034975369458128)

    def test_med_sentiment(self):
        doc = holmes_manager.get_document('Personal Narrative')
        self.assertEqual(doc._.median_sentiment, 0.0)

    def test_max_sentiment(self):
        doc = holmes_manager.get_document('Personal Narrative')
        self.assertEqual(doc._.max_sentiment, 0.86)

    def test_min_sentiment(self):
        doc = holmes_manager.get_document('Personal Narrative')
        self.assertEqual(doc._.min_sentiment, -0.64)

    def test_stdev_sentiment(self):
        doc = holmes_manager.get_document('Personal Narrative')
        self.assertEqual(doc._.stdev_sentiment, 0.28297934666238045)

    def test_tone_ratings(self):
        doc = holmes_manager.get_document('Personal Narrative')
        tone_ratings = [0.0, 0.0, 0.0, -0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.06, 0.0, 0.0, 0.0, 0.0, 0.0, -0.45, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.19, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.19, 0.0, 0.0, 0.0, 0.0, -0.1875, -0.5, 0.0, 0.0, 0.0, 0.0, 0.46, 0.0, 0.0, -0.6000000000000001, 0.0, -0.31, 0.0, 0.0, -0.07, -0.19, 0.0, 0.0, 0.0, 0.0, 0.0, 0.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.35, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, -0.19, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.25, 0.0, 0.0, -0.18, 0.0, 0.0, 0.0, -0.04, 0.0, 0.0, -0.07, 0.0, 0.0, 0.0, 0.0, 0.0, -0.07, 0.13636363636363635, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.08, -0.125, 0.0, 0.0, 0.0, -0.08, -0.125, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.19, -0.38, 0.0, 0.0, 0.0, 0.6, -0.01, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.04, 0.0, -0.07, 0.0, 0.0, 0.0, 0.0, 0.055, 0.0, 0.195, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.19, -0.34, 0.0, 0.0, 0.0, -0.125, 0.0, 0.0, -0.19, 0.0, 0.0, 0.0, 0.0, 0.0, -0.30000000000000004, 0.0, -0.52, 0.0, 0.0, 0.0, -0.19, 0.0, 0.0, -0.01, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.34, -0.02, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.39, 0.0, 0.0, 0.0, -0.34, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.08, 0.0, 0.0, 0.0, -0.07, 0.0, 0.0, 0.0, 0.0, 0.0, -0.6, -0.45, 0.0, 0.0, 0.0, 0.0, -0.30000000000000004, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.125, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.08, 0.0, 0.0, 0.0, -0.19, 0.0, 0.0, 0.0, 0.0, -0.01, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.07, 0.0, -0.5, 0.0, 0.0, -0.19, 0.0, 0.0, 0.0, 0.0, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0, -0.1875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.30000000000000004, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.035, 0.0, 0.0, 0.0, 0.0, 0.0, -0.19, 0.25, 0.0, 0.0, 0.0, 0.0, -0.19, 0.15000000000000002, 0.17500000000000002, -0.38, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.04, 0.0, 0.0, 0.0, -0.04, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.1875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.07, -0.19, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.19, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.02, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.30000000000000004, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.04, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.assertEqual(doc._.tone_ratings, tone_ratings)

    def test_mean_tone(self):
        doc = holmes_manager.get_document('Personal Narrative')
        self.assertEqual(doc._.mean_tone, -0.01549820868786386)

    def test_med_tone(self):
        doc = holmes_manager.get_document('Personal Narrative')
        self.assertEqual(doc._.median_tone, 0.0)

    def test_max_tone(self):
        doc = holmes_manager.get_document('Personal Narrative')
        self.assertEqual(doc._.max_tone, 1.0)

    def test_min_tone(self):
        doc = holmes_manager.get_document('Personal Narrative')
        self.assertEqual(doc._.min_tone, -0.6000000000000001)

    def test_stdev_tone(self):
        doc = holmes_manager.get_document('Personal Narrative')
        self.assertEqual(doc._.stdev_tone, 0.16871829461446927)

    def test_vwp_arguments(self):
        doc = holmes_manager.get_document('Personal Narrative')
        vwp_arguments = [12, 20, 21, 23, 28, 47, 48, 50, 61, 62, 86, 163, 168, 190, 191, 192, 193, 196, 198, 209, 228, 229, 232, 237, 245, 246, 253, 256, 258, 259, 260, 261, 262, 263, 267, 332, 333, 343, 344, 349, 354, 356, 357, 359, 360, 366, 367, 368, 369, 370, 405, 406, 407, 408, 423, 424, 425, 430, 431, 432, 433, 434, 487, 488, 489, 490, 493, 494, 495, 496, 498, 499]
        self.assertEqual(doc._.vwp_arguments, vwp_arguments)

    def test_propn_argument_words(self):
        doc = holmes_manager.get_document('Personal Narrative')
        self.assertEqual(doc._.propn_argument_words, 0.12857142857142856)

    def test_vwp_interactives(self):
        doc = holmes_manager.get_document('Personal Narrative')
        vwp_interactives = [2, 8, 20, 24, 29, 37, 47, 55, 64, 67, 92, 94, 119, 122, 125, 137, 153, 156, 158, 183, 192, 196, 201, 218, 238, 239, 256, 258, 285, 308, 317, 332, 336, 342, 343, 347, 361, 366, 367, 382, 412, 415, 424, 427, 430, 435, 440, 445, 447, 451, 459, 461, 466, 469, 472, 474, 480, 486, 488, 494, 501, 503, 512, 519, 522, 524, 526, 543]
        self.assertEqual(doc._.vwp_interactives, vwp_interactives)

    def test_propn_interactive(self):
        doc = holmes_manager.get_document('Personal Narrative')
        self.assertEqual(doc._.propn_interactive, 0.12142857142857143)

    def test_vwp_quoted(self):
        doc = holmes_manager.get_document('Personal Narrative')
        vwp_quoted = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.assertEqual(doc._.vwp_quoted, vwp_quoted)

    def test_vwp_direct_speech_spans(self):
        doc = holmes_manager.get_document('Personal Narrative')
        self.assertEqual(doc._.vwp_direct_speech_spans, [[[94], [], [[92, 96]]], [[295, 342, 347], [], [[342, 355]]], [[404, 412, 415, 424, 430, 435, 451, 459, 466, 474], [427, 440, 445, 469, 472], [[402, 416], [411, 416], [418, 429], [430, 443], [444, 460], [461, 470], [471, 477]]], [[484, 522, 524], [488, 494, 519, 526], [[478, 491], [492, 500], [506, 511], [512, 529]]]])

    def test_propn_direct_speech(self):
        doc = holmes_manager.get_document('Personal Narrative')
        self.assertEqual(doc._.propn_direct_speech, 0.19285714285714287)

    def test_governing_subjects(self):
        doc = holmes_manager.get_document('Personal Narrative')
        governing_subjects = [None, 0, None, 2, None, None, None, 0, None, 8, None, None, 8, None, None, None, 8, 8, 8, None, None, None, None, 22, None, None, 24, None, None, None, 29, None, 29, 29, None, None, 34, None, 37, None, 37, None, 37, 37, None, 37, None, None, 47, None, 49, None, None, 49, 49, None, None, None, 60, None, None, 60, None, 60, None, 64, None, None, 67, 67, None, 74, None, 74, None, None, 77, None, None, None, None, None, None, None, None, None, 85, None, 87, None, 87, None, None, None, None, 94, None, None, None, None, 99, None, None, None, None, None, None, None, 107, 107, 107, None, None, 111, None, None, 107, 107, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 135, 135, None, None, None, None, 137, None, None, 148, None, 148, 148, 148, None, None, None, None, None, None, None, 148, 148, None, None, None, None, None, None, None, 161, None, 164, None, None, None, None, None, 169, None, None, None, None, None, None, None, 178, None, None, None, 178, 178, None, None, 186, None, None, None, None, 189, 189, None, None, None, None, None, None, None, None, None, 201, None, None, None, None, None, None, 201, None, None, None, None, None, None, None, None, 218, 218, None, None, 224, None, None, 224, None, None, None, None, 230, 230, None, None, None, None, None, None, None, None, 238, None, None, None, None, None, None, None, None, None, None, 248, 248, None, None, None, None, None, None, 257, 257, 257, 257, None, 257, None, None, None, None, 269, 269, None, None, 273, 273, None, 273, None, None, 273, 273, None, 273, 273, 273, 273, None, None, None, 289, None, None, 289, None, None, 295, None, 297, 297, None, None, None, None, None, 304, None, None, None, 308, 308, 308, None, 315, 315, None, None, None, 317, None, None, None, None, None, 317, None, 330, None, 330, None, None, None, None, 332, 332, None, 332, 332, 332, None, 332, None, None, 342, 342, None, None, None, 347, None, None, None, 351, None, None, None, None, 366, None, 358, None, None, None, None, None, None, None, None, None, 366, None, 366, None, 366, 366, None, None, None, None, None, 382, None, None, 382, 382, None, None, None, 382, None, None, None, None, None, None, None, None, None, None, None, None, 399, None, 399, 399, 399, 399, None, 404, None, None, None, None, 412, None, None, 415, None, None, None, None, None, 420, None, None, 424, 424, None, 427, None, None, 430, None, None, 430, None, 435, None, 435, 435, None, 438, None, None, None, None, 445, None, None, None, 445, None, 451, None, None, 445, None, None, 457, None, None, None, 464, 464, None, 464, None, 466, 466, None, None, None, None, 472, None, 474, None, None, None, None, None, 480, None, 480, None, None, None, 486, None, None, None, None, None, None, None, 494, 497, None, 497, None, None, None, 501, None, 503, None, None, None, 507, None, 507, None, None, 512, None, 512, None, None, 517, None, 519, 520, None, None, None, 524, None, 524, None, None, None, None, 531, None, None, None, 535, None, None, None, None, None, None, None, None, 549, None, 549, None, None, None, None, 553, 554, None, None, 554, 554, None, None]
        self.assertEqual(doc._.governing_subjects, governing_subjects)

    def test_content_segments(self):
        doc = holmes_manager.get_document('Personal Narrative')
        content_segments = [[0, 20], [20, 29], [29, 47], [47, 57], [57, 85], [85, 92], [92, 97], [97, 122], [122, 137], [137, 141], [141, 287], [288, 392], [392, 399], [399, 418], [418, 430], [430, 444], [444, 461], [461, 471], [471, 478], [478, 492], [492, 560]]
        self.assertEqual(doc._.content_segments, content_segments)

    def test_prompt_related(self):
        doc = holmes_manager.get_document('Personal Narrative')
        prompt_related = [[4, 3.0605871330418486, ['walk', 'keep', 'crawl', 'pull', 'notice', 'look', 'reach', 'pass', 'stare', 'shake'], [7, 68, 219, 274, 309, 318, 324, 333, 383, 388, 422, 481, 502, 518]], [22, 2.127659574468085, ['Nancy', 'Allie', 'Alex'], [34, 88, 90, 148, 150, 295, 484, 517]], [19, 1.5341264871634313, ['sorry', 'happy', 'fool', 'silly', 'laugh', 'darling'], [53, 285, 286, 363, 371, 413, 553]]]
        self.assertEqual(doc._.prompt_related, prompt_related)

    def test_prompt_language(self):
        doc = holmes_manager.get_document('Personal Narrative')
        prompt_language = ['walk', 'walked', 'keep', 'kept', 'pull', 'pulled', 'look', 'looked', 'actual', 'actually', 'pass', 'passed', 'first']
        self.assertEqual(doc._.prompt_language, prompt_language)

    def test_core_sentences(self):
        doc = holmes_manager.get_document('Personal Narrative')
        core_sentences = []
        self.assertEqual(doc._.core_sentences, core_sentences)
