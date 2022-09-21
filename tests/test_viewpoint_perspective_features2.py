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
            document_text="Surely many of us have expressed the following sentiment, or some variation on it, during our daily commutes to work: \"People are getting so stupid these days!\" Surrounded as we are by striding and strident automatons with cell phones glued to their ears, PDA's gripped in their palms, and omniscient, omnipresent CNN gleaming in their eyeballs, it's tempting to believe that technology has isolated and infantilized us, essentally transforming us into dependent, conformist morons best equipped to sideswip one another in our SUV's.\n\nFurthermore, hanging around with the younger, pre-commute generation, whom tech-savviness seems to have rendered lethal, is even less reassuring. With \"Teen People\" style trends shooting through the air from tiger-striped PDA to zebra-striped PDA, and with the latest starlet gossip zipping from juicy Blackberry to teeny, turbo-charged cell phone, technology seems to support young people's worst tendencies to follow the crowd. Indeed, they have seemingly evolved into intergalactic conformity police. After all, today's tech-aided teens are, courtesy of authentic, hands-on video games, literally trained to kill; courtesy of chat and instant text messaging, they have their own language; they even have tiny cameras to efficiently photodocument your fashion blunders! Is this adolescence, or paparazzi terrorist training camp?\n\nWith all this evidence, it's easy to believe that tech trends and the incorporation of technological wizardry into our everyday lives have served mostly to enforce conformity, promote dependence, heighten comsumerism and materialism, and generally create a culture that values self-absorption and personal entitlement over cooperation and collaboration. However, I argue that we are merely in the inchoate stages of learning to live with technology while still loving one another. After all, even given the examples provided earlier in this essay, it seems clear that technology hasn't impaired our thinking and problem-solving capacities. Certainly it has incapacitated our behavior and manners; certainly our values have taken a severe blow. However, we are inarguably more efficient in our badness these days. We're effective worker bees of ineffectiveness!\n\nIf Technology has so increased our senses of self-efficacy that we can become veritable agents of the awful, virtual CEO's of selfishness, certainly it can be beneficial. Harnessed correctly, technology can improve our ability to think and act for ourselves. The first challenge is to figure out how to provide technology users with some direly-needed direction.", label='GRE_Sample_Essay')


class ViewpointPerspectiveFeatureTest(unittest.TestCase):

    def test_vwp_perspective(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        perspective_spans = {'implicit': {'26': [23, 24, 25, 26, 27, 28, 29, 30, 31, 32], '52': [33, 49, 50, 51, 52, 53, 54, 55, 56, 57, 59, 60, 61, 62, 63, 64, 65], '45': [45, 46, 47, 48], '58': [58], '68': [66, 67, 68, 69, 70, 71, 98], '75': [72, 73, 74, 75, 76, 77, 79, 80, 81, 83, 84, 85, 86, 87], '89': [88, 89, 90, 91, 92, 93, 94, 96, 97], '123': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 122, 123, 124, 125, 126, 127], '117': [113, 114, 115, 116, 117, 118, 119, 120, 121], '170': [128, 151, 152, 153, 154, 155, 168, 169, 170, 171, 172, 173, 174, 175, 177, 178, 179, 180, 181, 182], '135': [129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150], '156': [156, 157, 158, 159, 160, 161, 162, 166, 167], '165': [163, 164, 165], '176': [176], '188': [183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193], '236': [194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 243, 244, 245], '246': [246, 247, 248, 249, 250, 251, 252, 253, 254, 255], '263': [256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 312], '281': [267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299], '301': [300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311], '351': [337, 338, 339, 340, 341, 342, 343, 349, 350, 351, 352, 365], '344': [344, 345, 346, 347, 348], '357': [353, 354, 355, 356, 357, 359, 360, 361, 362, 363, 364], '369': [366, 367, 368, 369, 371, 372, 373], '436': [405, 432, 433, 434, 435, 436, 437, 438], '410': [406, 407, 408, 409, 410, 412, 413, 414, 415, 416], '425': [425], '444': [439, 440, 441, 442, 443, 444, 446, 447, 448, 449, 450, 451, 453], '457': [454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 471, 472], '470': [468, 469, 470]}, 'explicit_1': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 78, 82, 95, 277, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 358, 370, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 411, 417, 418, 419, 420, 421, 422, 423, 424, 426, 427, 428, 429, 430, 431, 445, 452], 'explicit_2': [242], 'explicit_3': {}}
        self.assertEqual(doc._.vwp_perspective_spans,
                         perspective_spans)

    def test_vwp_stance_markers(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        stance_markers = {'implicit': {'26': [28, 31], '58': [58], '68': [69, 71], '89': [88], '123': [100, 124, 126], '117': [117], '170': [170, 172], '176': [176], '188': [183, 187], '236': [194, 195, 205, 215, 220, 235, 240, 245], '246': [246, 255], '263': [264, 266], '281': [282, 296], '351': [337, 338, 340, 343, 351, 352], '357': [361], '369': [366], '410': [406, 409, 412], '425': [425], '436': [433, 435, 437], '444': [440, 443, 448], '457': [456, 459], '470': [468]}, 'explicit_1': [0, 1, 5, 40, 375, 377, 384, 388, 390, 399, 403, 404, 419, 421], 'explicit_2': [], 'explicit_3': {}}
        self.assertEqual(doc._.vwp_stance_markers,
                         stance_markers)

    def test_propn_egocentric(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.propn_egocentric,
                         0.7061310782241015)

    def test_propn_allocentric(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.propn_allocentric, 0.0)

    def test_propositional_attitudes(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        propositional_attitudes = {'implicit': [[[0, 32], 24, 26], [[33, 98], 67, 68], [[99, 127], None, 123], [[128, 182], 169, 170], [[183, 193], 185, 188], [[194, 245], 228, 229], [[337, 365], 350, 351], [[337, 365], 350, 351], [[366, 383], 377, 379], [[384, 396], 386, 387], [[405, 438], 434, 436], [[439, 453], 442, 444]], 'implicit_3': [[[454, 472], 456, 457]], 'explicit_1': [[[313, 336], 315, 316]], 'explicit_2': [], 'explicit_3': {}}
        self.assertEqual(doc._.vwp_propositional_attitudes,
                         propositional_attitudes)

    def test_emotional_states(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        emotion_states = {'explicit_1': [333], 'explicit_2': [], 'explicit_3': {'Culture': [301]}}
        self.assertEqual(doc._.vwp_emotion_states,
                         emotion_states)

    def test_character_traits(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        # No character traits detected in this essay. We may need another test
        # with a different text.
        character_traits = {'explicit_1': [40, 390], 'explicit_2': [], 'explicit_3': {'People': [28], 'Pda': [58], 'Teens': [205, 220, 240]}}
        self.assertEqual(doc._.vwp_character_traits,
                         character_traits)

    def test_subjectivity_ratings(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        subjectivity_ratings = [0.8888888888888888, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06666666666666667, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.9, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.75, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6666666666666666, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.8333333333333334, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.95, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3833333333333333, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5714285714285714, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5714285714285714, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5714285714285714, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3333333333333333, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.assertEqual(doc._.subjectivity_ratings,
                         subjectivity_ratings)

    def test_mean_subjectivity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_subjectivity,
                         0.07682315064390537)

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
                         0.22539452272167562)

    def test_polarity_ratings(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        polarity_ratings = [0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.7999999999999999, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.8, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.16666666666666666, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.43333333333333335, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.2, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.05000000000000002, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.13636363636363635, 0.0, 0.0, 0.0, 0.0, 0.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.10000000000000002, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.21428571428571427, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.21428571428571427, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, -0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.21428571428571427, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.assertEqual(doc._.polarity_ratings,
                         polarity_ratings)

    def test_mean_polarity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_polarity,
                         0.0026535571346892103)

    def test_med_polarity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.median_polarity, 0.0)

    def test_max_polarity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.max_polarity, 1.0)

    def test_min_polarity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.min_polarity, -1.0)

    def test_stdev_polarity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdev_polarity,
                         0.17544979638212832)

    def test_sentiment_ratings(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        sentiment_ratings = [0.41000000000000003, 0, 0, 0, 0.21, 0.17, 0, 0.08, 0.30000000000000004, 0, 0, 0.06, -0.29, 0.08, 0, 0, 0, 0, 0.18, 0, 0, 0.01, 0, 0, 0.17, 0, 0, 0, -0.54, 0, 0, 0, 0, 0, -0.07, 0, 0, -0.1, 0, 0, -0.17, 0, 0, -0.22, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.21, 0, 0, 0, 0.30000000000000004, 0, 0, 0, 0, 0, 0, 0.26, 0, 0.51, 0, 0.13, 0, -0.16, 0, 0, 0, 0, 0, 0, 0, 0, 0.56, 0, 0.24, 0, 0.36, 0.16, 0, 0, 0.27, -0.07, 0, 0, -0.06, 0, 0, 0, 0, 0, 0, 0.15, 0, 0, -0.28, 0, 0, 0, -0.21, 0.27, 0, 0, 0.19, 0, 0, 0, 0, 0.21, 0, -0.63, 0, 0, 0.08, 0.1, 0.21, 0, 0, 0, 0.02, 0.17, 0, 0.45, 0, 0, 0.13, 0, 0.42, 0, 0.25, 0, 0.06, 0, 0, 0.36, 0, 0.06, 0, 0, 0, 0, 0, -0.42, 0.31, -0.37, 0, 0, 0.51, 0.4, 0, 0.15, 0, 0, 0, 0.19, -0.22, 0.27, 0, 0.13, 0, 0, 0.47000000000000003, 0.32, 0.17, 0, 0.25, 0, 0, -0.04, 0, -0.13, 0, 0, 0, 0, 0.21, 0.15, 0, 0, 0.33, 0.24, -0.1, 0, 0, 0.21, 0, 0.15, 0, 0.19, 0, 0, 0.14, 0, 0, 0.44, 0, 0.47000000000000003, 0, 0, 0, 0.08, 0.41000000000000003, 0, 0, 0, 0, 0, -0.79, 0, 0.44, 0, 0.18, 0, 0.21, 0.37, 0, 0, 0, 0.21, 0, 0, 0.34, 0, 0, 0.08, 0.21, 0.02, 0, 0, 0.48, 0, 0, 0.06, 0, 0, 0, 0, 0.25, 0, 0, 0, -0.66, 0.04, 0.5, 0, 0, 0, 0.21, 0, -0.07, 0, 0, 0, 0.61, 0, 0.51, 0, 0.19, 0, 0, 0, 0.09, 0, 0.07, 0.38, 0, 0, 0.11, 0, 0.21, 0, 0, 0, 0.08, 0.24, 0, 0.38, -0.35000000000000003, 0, 0.34, 0, 0, -0.37, 0, 0, -0.42, 0.71, 0.04, 0.32, 0, 0, 0.46, 0, 0.21, 0, 0.27, 0, 0.17, 0.4, 0, 0.28, 0, 0.08, 0, -0.19, -0.46, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.35000000000000003, 0, 0.73, 0, 0.13, 0, -0.02, 0.36, 0.27, -0.07, 0, 0, 0.21, 0, 0.08, 0.17, 0, 0, 0, 0, 0, 0, -0.02, 0, 0, 0, 0.28, 0, -0.13, 0, 0, 0.21, 0, -0.15, 0, 0.37, 0, 0, 0, 0, 0.15, 0, 0, -0.34, 0, 0.07, 0, 0, 0, 0.15, 0, 0, 0.21, -0.12, 0.04, -0.44, 0.27, 0, 0.08, 0, 0, 0, 0, 0, 0.48, 0, 0, -0.36, 0, 0, 0, 0, 0, 0.48, 0.23, 0, 0, 0.48, 0, 0, 0, 0.13, 0, 0, 0, 0, 0, 0, 0.46, 0, 0.12, 0, 0, 0.35000000000000003, 0.33, 0.03, 0, 0, 0, -0.68, 0, 0.27, 0, 0, 0, -0.51, 0, 0.15, 0, 0.35000000000000003, 0.29, 0.4, 0, 0, -0.38, 0, 0.13, 0.35000000000000003, 0.28, 0, 0.5, 0, 0.42, 0, 0.16, 0, 0, 0, 0, 0.58, 0.23, 0, 0, 0.02, -0.30000000000000004, 0, 0, 0.41000000000000003, 0.13, 0, 0, 0.06, 0, 0, 0.12, 0.11, 0]
        print(doc._.sentiment_ratings)
        self.assertEqual(doc._.sentiment_ratings,
                         sentiment_ratings)

    def test_mean_sentiment(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_sentiment,
                         0.0925943396226415)

    def test_med_sentiment(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.median_sentiment, 0.025)

    def test_max_sentiment(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.max_sentiment, 0.73)

    def test_min_sentiment(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.min_sentiment, -0.79)

    def test_stdev_sentiment(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdev_sentiment,
                         0.2517283677948165)

    def test_tone_ratings(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        tone_ratings = [0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.29, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.7999999999999999, 0.0, 0.0, 0.0, 0.0, 0.0, -0.07, 0.0, 0.0, -0.1, 0.0, 0.0, -0.17, 0.0, 0.0, -0.22, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.13, 0.0, 0.0, 0.0, 0.0, 0.0, -0.16, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.8, 1.0, 0.0, 0.0, 0.0, 0.0, -0.07, 0.0, 0.0, -0.06, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.28, 0.0, 0.0, 0.0, -0.21, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.63, 0.0, 0.0, 0.04, -0.16666666666666666, 0.105, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.42, 0.0, -0.37, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.22, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, -1.0, 0.0, 0.0, -0.04, 0.0, -0.13, 0.0, 0.0, 0.0, 0.0, 0.0, 0.075, 0.0, 0.0, 0.0, 0.0, -0.1, 0.0, 0.0, 0.105, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.47000000000000003, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.79, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.04, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.66, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.07, 0.0, 0.0, 0.0, 0.61, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.2, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, -0.35000000000000003, 0.0, 0.0, 0.0, 0.0, -0.37, 0.0, 0.0, -0.42, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.19, -0.46, 0.0, 0.0, 0.0, -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.13636363636363635, 0.0, 0.0, 0.0, -0.02, 0.36, 0.0, -0.07, 0.0, 0.0, 0.105, 0.0, 0.04, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.02, 0.0, 0.0, 0.0, 0.28, 0.0, 0.0, 0.0, 0.0, -0.21, 0.0, 0.0, 0.0, -0.37, 0.0, 0.0, 0.0, 0.0, 0.21428571428571427, 0.0, 0.0, -0.34, 0.0, 0.0, 0.0, 0.0, 0.0, 0.21428571428571427, 0.0, 0.0, 0.0, -0.12, 0.0, -0.44, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.24, 0.0, 0.0, -0.36, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6, 0.0, 0.0, 0.0, 0.24, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.17500000000000002, 0.0, 0.015, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.51, 0.0, 0.21428571428571427, 0.0, 0.17500000000000002, 0.0, 0.2, 0.0, 0.0, -0.38, 0.0, 0.0, 0.17500000000000002, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, -0.30000000000000004, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        print(doc._.tone_ratings)
        self.assertEqual(doc._.tone_ratings,
                         tone_ratings)

    def test_mean_tone(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_tone,
                         -0.036631034060279344)

    def test_med_tone(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.median_tone, 0.0)

    def test_max_tone(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.max_tone, 1.0)

    def test_min_tone(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.min_tone, -1.0)

    def test_stdev_tone(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdev_tone,
                         0.2166434664720677)

    def test_vwp_arguments(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        vwp_arguments = [0, 1, 2, 3, 4, 5, 25, 26, 27, 28, 31, 69, 70, 71, 72, 100, 113, 117, 118, 119, 120, 124, 125, 126, 128, 151, 170, 171, 172, 176, 177, 178, 179, 183, 186, 187, 188, 189, 194, 195, 215, 229, 235, 236, 245, 250, 257, 258, 259, 260, 264, 265, 266, 267, 280, 281, 282, 283, 313, 315, 316, 317, 318, 319, 337, 338, 340, 341, 342, 343, 344, 345, 351, 352, 353, 356, 359, 366, 368, 369, 375, 376, 377, 378, 379, 384, 386, 388, 389, 390, 406, 408, 409, 410, 411, 412, 413, 417, 418, 419, 421, 425, 433, 435, 436, 437, 440, 443, 444, 445, 446, 447, 448, 454, 456, 457, 458, 459, 461, 462, 463, 466, 467, 468]
        print(doc._.vwp_arguments)
        self.assertEqual(doc._.vwp_arguments,
                         vwp_arguments)

    def test_propn_argument_words(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.propn_argument_words,
                         0.26215644820295986)

    def test_vwp_interactives(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        vwp_interactives = [3, 17, 27, 28, 29, 35, 51, 67, 68, 78, 82, 95, 97, 124, 175, 176, 198, 235, 242, 247, 258, 259, 262, 263, 277, 282, 315, 318, 332, 340, 347, 355, 356, 358, 370, 376, 386, 389, 392, 394, 397, 398, 409, 411, 418, 425, 429, 445, 452]
        self.assertEqual(doc._.vwp_interactives,
                         vwp_interactives)

    def test_propn_interactive(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.propn_interactive,
                         0.10359408033826638)

    # This text contains no quoted or direct speech.
    # We need another test article
    # to do proper regression on these features.
    def test_vwp_quoted(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        vwp_quoted = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.assertEqual(doc._.vwp_quoted,
                         vwp_quoted)

    def test_vwp_direct_speech_spans(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.vwp_direct_speech_spans,
                         [[[3, 17], [], [[0, 32]]]])

    def test_propn_direct_speech(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.propn_direct_speech, 0.0)

    def test_governing_subjects(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        governing_subjects = [3, None, None, None, None, 3, None, None, None, None, None, None, None, None, None, None, 3, None, 17, 17, None, 3, None, None, None, None, 24, 28, 24, None, None, None, None, 50, None, None, 35, 35, 35, None, 35, 35, 35, None, None, None, None, None, 47, None, None, None, 50, 50, None, 54, None, None, 50, None, 50, 50, None, None, None, 64, None, None, 67, 67, None, 67, None, None, None, 73, None, 73, None, None, 73, 73, None, 82, None, None, None, None, None, None, None, None, None, None, None, None, 95, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 116, None, None, 116, 113, None, None, 126, 126, None, None, None, None, None, None, None, None, None, 134, 134, None, None, None, None, None, 143, None, 134, None, None, 148, None, None, None, None, None, None, None, None, None, None, 159, None, None, None, None, None, None, 167, None, None, None, None, 169, None, 169, None, None, None, 174, 174, None, 174, None, None, None, 185, None, None, None, 185, 185, 185, 185, None, 185, None, 202, 202, None, None, None, None, None, 197, 197, 202, None, 202, 202, 213, None, None, None, None, None, None, None, 202, 202, None, 202, None, 202, 202, None, None, None, None, None, None, None, 228, None, 230, 230, None, None, 234, 234, 238, None, None, 234, 234, None, None, 242, None, 248, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 262, 262, None, 262, None, None, None, None, None, None, None, None, None, None, None, 277, 277, None, 269, 269, None, 269, None, None, 269, None, None, 269, None, None, None, None, None, 269, 269, None, None, None, 299, None, None, None, None, None, None, None, None, None, None, None, 315, None, None, 315, None, None, 318, 318, 318, None, 318, 318, 318, 318, None, 318, 318, None, None, 318, 318, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 350, None, None, None, None, None, 354, None, None, None, None, None, None, 358, None, 367, None, None, 367, None, 370, None, 370, None, 377, None, 376, None, 377, None, 382, None, None, 386, None, None, 386, 390, 390, 386, 386, None, 392, None, None, None, None, 397, 397, None, 397, 397, 397, None, None, None, None, None, 407, 407, None, 411, 411, None, None, 411, None, None, None, 418, 418, 418, 418, None, 428, None, 428, None, None, None, None, None, 434, None, None, 434, 434, None, 442, 442, None, None, None, 442, None, 445, None, 445, None, 445, 445, None, None, None, None, None, 456, None, 456, None, None, None, 456, None, None, 465, None, None, None, None, None, None]
        self.assertEqual(doc._.governing_subjects,
                         governing_subjects)

    def test_content_segments(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        content_segments = [[0, 33], [99, 128], [194, 255], [337, 384], [384, 397], [397, 405]]
        self.assertEqual(doc._.content_segments,
                         content_segments)

    def test_prompt_related(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        prompt_related = [[33, 2.9208434151399927, ['technology', 'tech', 'savviness', 'technological', 'wizardry', 'Technology'], [73, 114, 116, 169, 199, 268, 274, 275, 330, 354, 407, 442, 464]], [50, 1.9179541822056472, ['conformist', 'conformity', 'materialism', 'entitlement', 'selfishness'], [86, 191, 285, 293, 307, 431]], [41, 1.4803625377643503, ['surely', 'furthermore', 'generally', 'merely', 'certainly'], [0, 100, 296, 320, 366, 375, 433]]]
        self.assertEqual(doc._.prompt_related,
                         prompt_related)

    def test_prompt_language(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        prompt_language = ['so', 'stupid', 'tempt', 'tempting', 'technology', 'conform', 'conformist', 'furthermore', 'assure', 'reassuring', 'support', 'after', 'all', 'easy', 'general', 'generally', 'however', 'argue', 'still', 'clear', 'certain', 'certainly', 'value', 'values', 'efficient', 'self', 'selfishness', 'beneficial', 'challenge']
        self.assertEqual(doc._.prompt_language,
                         prompt_language)

    def test_core_sentences(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        core_sentences = [[33, 99], [128, 183], [256, 313], [313, 337], [405, 439], [454, 473]]
        self.assertEqual(doc._.core_sentences,
                         core_sentences)

    def test_extended_core_sentences(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        extended_core_sentences = [[183, 194], [439, 454]]
        self.assertEqual(doc._.extended_core_sentences,
                         extended_core_sentences)
