import awe_workbench.parser.manager as holmes
from awe_workbench.parser.components.utility_functions import print_parse_tree

import unittest

holmes_manager = holmes.Manager(
    'en_core_web_lg', perform_coreference_resolution=False, number_of_workers=2)

# GRE Sample from https://www.ets.org/gre/revised_general/prepare/analytical_writing/issue/sample_responses
holmes_manager.parse_and_register_document(
            document_text="The statement linking technology negatively with free thinking plays on recent human experience over the past century. Surely there has been no time in history where the lived lives of people have changed more dramatically. A quick reflection on a typical day reveals how technology has revolutionized the world. Most people commute to work in an automobile that runs on an internal combustion engine. During the workday, chances are high that the employee will interact with a computer that processes information on silicon bridges that are .09 microns wide. Upon leaving home, family members will be reached through wireless networks that utilize satellites orbiting the earth. Each of these common occurrences could have been inconceivable at the turn of the 19th century.\n\nThe statement attempts to bridge these dramatic changes to a reduction in the ability for humans to think for themselves. The assumption is that an increased reliance on technology negates the need for people to think creatively to solve previous quandaries. Looking back at the introduction, one could argue that without a car, computer, or mobile phone, the hypothetical worker would need to find alternate methods of transport, information processing and communication. Technology short circuits this thinking by making the problems obsolete.\n\nHowever, this reliance on technology does not necessarily preclude the creativity that marks the human species. The prior examples reveal that technology allows for convenience. The car, computer and phone all release additional time for people to live more efficiently. This efficiency does not preclude the need for humans to think for themselves. In fact, technology frees humanity to not only tackle new problems, but may itself create new issues that did not exist without technology. For example, the proliferation of automobiles has introduced a need for fuel conservation on a global scale. With increasing energy demands from emerging markets, global warming becomes a concern inconceivable to the horse-and-buggy generation. Likewise dependence on oil has created nation-states that are not dependent on taxation, allowing ruling parties to oppress minority groups such as women. Solutions to these complex problems require the unfettered imaginations of maverick scientists and politicians.\n\nIn contrast to the statement, we can even see how technology frees the human imagination. Consider how the digital revolution and the advent of the internet has allowed for an unprecedented exchange of ideas. WebMD, a popular internet portal for medical information, permits patients to self research symptoms for a more informed doctor visit. This exercise opens pathways of thinking that were previously closed off to the medical layman. With increased interdisciplinary interactions, inspiration can arrive from the most surprising corners. Jeffrey Sachs, one of the architects of the UN Millenium Development Goals, based his ideas on emergency care triage techniques. The unlikely marriage of economics and medicine has healed tense, hyperinflation environments from South America to Eastern Europe.\n\nThis last example provides the most hope in how technology actually provides hope to the future of humanity. By increasing our reliance on technology, impossible goals can now be achieved. Consider how the late 20th century witnessed the complete elimination of smallpox. This disease had ravaged the human race since prehistorical days, and yet with the technology of vaccines, free thinking humans dared to imagine a world free of smallpox. Using technology, battle plans were drawn out, and smallpox was systematically targeted and eradicated.\n\nTechnology will always mark the human experience, from the discovery of fire to the implementation of nanotechnology. Given the history of the human race, there will be no limit to the number of problems, both new and old, for us to tackle. There is no need to retreat to a Luddite attitude to new things, but rather embrace a hopeful posture to the possibilities that technology provides for new avenues of human imagination.", label='GRE_Sample_Essay')


class ViewpointPerspectiveFeatureTest(unittest.TestCase):

    def test_vwp_perspective(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        perspective_spans = {'implicit': {'1': [0, 1, 17], '2': [2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], '6': [6], '21': [18, 19, 20, 21, 22, 23, 24, 25, 36], '33': [26, 27, 28, 29, 30, 31, 32, 33, 34, 35], '44': [37, 38, 39, 40, 41, 42, 43, 44, 51], '48': [45, 46, 47, 48, 49, 50], '54': [52, 53, 54, 55, 56, 57, 58, 59, 67], '61': [60, 61, 62, 63, 64, 65, 66], '73': [68, 69, 70, 71, 72, 73, 74, 94], '79': [75, 76, 77, 78, 79, 80, 81, 82], '84': [83, 84, 85, 86, 87, 88], '90': [89, 90, 91, 92, 93], '103': [95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 113], '108': [107, 108, 109], '110': [110, 111, 112], '121': [114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130], '131': [131], '134': [132, 133, 134, 135, 136, 137, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152], '138': [138], '155': [153, 154, 155, 174], '162': [156, 157, 158, 159, 160, 161, 162, 163, 164], '168': [165, 166, 167, 168, 169, 170, 171, 172, 173], '216': [212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222], '223': [223], '233': [224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 241], '237': [236, 237, 238, 239, 240], '245': [242, 243, 244, 245, 251], '248': [246, 247, 248, 249, 250], '259': [252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 268], '265': [262, 263, 264, 265, 266, 267], '273': [269, 270, 271, 272, 273, 274, 275, 282], '279': [276, 277, 278, 279, 280, 281], '287': [283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296], '299': [297, 298, 299, 300, 301, 308], '305': [302, 303, 304, 305, 306, 307], '317': [309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327], '338': [328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 350], '341': [341, 342, 343, 344, 345, 346, 347, 348, 349], '356': [351, 352, 353, 354, 355, 356, 357, 358, 359, 377], '361': [360, 361, 362, 363, 364, 365, 366, 367], '371': [368, 369, 370, 371, 372, 373, 374, 375, 376], '383': [378, 379, 380, 382, 383, 384, 386, 387, 389, 390, 391, 392], '381': [381], '385': [385], '388': [388], '393': [393], '411': [411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 427, 428, 429, 430], '426': [426], '441': [431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453], '456': [454, 455, 456, 457, 458, 459, 469], '463': [460, 461, 462, 463, 464, 465, 466, 467, 468], '477': [470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 482, 483], '481': [480, 481], '515': [507, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526], '508': [508], '527': [527], '531': [528, 529, 530, 531, 532, 534, 535, 546], '533': [533], '539': [536, 537, 538, 539, 540, 541, 542, 543, 544, 545], '559': [547, 548, 550, 551, 552, 553, 555, 556, 557, 558, 559, 560], '554': [554], '561': [561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573], '577': [574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591], '596': [592, 594, 595, 596, 597, 598, 599, 600, 604], '593': [593], '601': [601, 602, 603], '611': [605, 606, 607, 608, 609, 610, 611, 612, 613, 614], '618': [615, 616, 617, 618, 619, 620, 621], '622': [622], '626': [623, 624, 625, 626, 627, 628, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638, 639, 640, 641], '652': [642, 643, 644, 645, 646, 647, 648, 649, 650, 651, 652, 653, 654, 655, 656, 657, 658, 659, 660, 661, 662, 663, 664, 665, 670], '672': [671, 672, 673, 674, 675, 676, 677, 678, 679, 680, 681, 682, 683, 684, 685, 686, 687, 688, 690, 691, 692, 693, 703], '689': [689], '696': [694, 695, 696, 697, 698, 699, 700, 701, 702]}, 'explicit_1': [394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 549, 666, 667, 668, 669], 'explicit_2': [], 'explicit_3': {181: [175, 176, 177, 178, 179, 180, 181, 182, 183, 211], 197: [184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210], 485: [484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506]}}
        self.assertEqual(doc._.vwp_perspective_spans,perspective_spans)

    def test_vwp_stance_markers(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        stance_markers = {'implicit': {'1': [1], '2': [4, 7, 8], '6': [6], '21': [18], '33': [35], '44': [39, 44], '42': [42], '73': [72], '117': [117], '121': [119, 122], '134': [133, 134, 149], '138': [138], '155': [154], '162': [159], '168': [168, 169, 173], '216': [216, 220, 221], '233': [227, 232, 235], '245': [244, 245], '248': [250], '265': [267], '273': [270, 275], '279': [279], '287': [283, 284, 291, 294], '299': [297, 301], '317': [317, 319], '338': [331, 340], '341': [341], '381': [381], '383': [382], '385': [385], '388': [388], '411': [411], '426': [426], '477': [476], '481': [481], '508': [508], '531': [531, 534], '533': [533], '539': [538, 540], '559': [550, 555, 556], '554': [554], '561': [561], '593': [593], '596': [598], '601': [601], '611': [609], '626': [625, 633, 638], '652': [659], '672': [674, 687, 690, 693], '689': [689]}, 'explicit_1': [401, 402, 409], 'explicit_2': [], 'explicit_3': {181: [175, 182], 197: [196, 198], 485: [503]}}
        self.assertEqual(doc._.vwp_stance_markers,stance_markers)

    def test_propn_egocentric(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.propn_egocentric,0.421875)

    def test_propn_allocentric(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.propn_allocentric,0.08522727272727272)


    def test_propositional_attitudes(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        propositional_attitudes = {'implicit': [[[18, 36], None, 21], [[37, 51], 39, 44], [[114, 130], 118, 121], [[224, 241], 227, 233], [[351, 377], 352, 356], [[470, 483], 475, 477], [[547, 560], 555, 559], [[623, 641], 623, 626], [[642, 670], None, 652], [[671, 703], None, 672]], 'implicit_3': [[[68, 94], 72, 73], [[114, 130], 118, 125], [[132, 152], 133, 134], [[153, 174], 154, 155], [[175, 211], 181, 176], [[212, 222], 214, 218], [[242, 251], 244, 245], [[269, 282], 270, 273], [[269, 282], None, 275], [[378, 392], None, 378], [[394, 410], None, 395], [[528, 546], 530, 531], [[528, 546], None, 534], [[671, 703], None, 687]], 'explicit_1': [[[394, 410], 400, 403]], 'explicit_2': [[[0, 17], None, 1], [[411, 430], None, 411], [[561, 573], None, 561]], 'explicit_3': {181: [[[175, 211], 181, 183]]}}
        self.assertEqual(doc._.vwp_propositional_attitudes,propositional_attitudes)  
        
    def test_emotional_states(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        emotion_states = {'explicit_1': [], 'explicit_2': [], 'explicit_3': {'Worker': [199], 'Humans': [596]}}
        self.assertEqual(doc._.vwp_emotion_states,emotion_states)

    def test_character_traits(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        # No character traits detected in this essay. We may need another test
        # with a different text.
        character_traits = {'explicit_1': [], 'explicit_2': [], 'explicit_3': {'People': [169, 267]}}
        self.assertEqual(doc._.vwp_character_traits,character_traits)
                
    def test_subjectivity_ratings(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        subjectivity_ratings = [0.0, 0.0, 0.0, 0.0, 0.4, 0.0, 0.8, 0.0, 0.0, 0.0, 0.25, 0.1, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.8888888888888888, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5399999999999999, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.16666666666666666, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.45454545454545453, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.45454545454545453, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.9, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.9, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.16666666666666666, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06666666666666667, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.125, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6, 0.0, 0.0, 0.0, 0.0, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.45454545454545453, 0.0, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.45454545454545453, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.45454545454545453, 0.0, 0.0, 0.1, 0.0, 0.0]
        self.assertEqual(doc._.subjectivity_ratings,subjectivity_ratings)

    def test_mean_subjectivity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_subjectivity,0.056695505782462303)

    def test_med_subjectivity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.median_subjectivity,0.0)

    def test_max_subjectivity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.max_subjectivity,1.0)

    def test_min_subjectivity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.min_subjectivity,0.0)

    def test_std_subjectivity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdev_subjectivity,0.17940470549662493)

    def test_polarity_ratings(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        polarity_ratings = [0.0, 0.0, 0.0, 0.0, -0.3, 0.0, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.25, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.3333333333333333, 0.0, 0.0, 0.0, -0.16666666666666666, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.16, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.4333333333333333, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, -0.16666666666666666, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.13636363636363635, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.13636363636363635, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.13636363636363635, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.16666666666666666, -0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.3333333333333333, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.6666666666666666, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.3, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.13636363636363635, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.13636363636363635, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.13636363636363635, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.assertEqual(doc._.polarity_ratings,polarity_ratings)

    def test_mean_polarity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_polarity,0.004429512516469039)

    def test_med_polarity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.median_polarity,0.0)

    def test_max_polarity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.max_polarity,0.7)

    def test_min_polarity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.min_polarity,-0.6666666666666666)

    def test_stdev_polarity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdev_polarity,0.10743682466568848)

    def test_sentiment_ratings (self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        sentiment_ratings = [0, 0.08, 0, 0.13, -0.45, 0, 0.81, 0.15, 0, 0.08, 0.1, 0.36, 0.47000000000000003, 0.17, 0, 0.02, 0.09, 0, -0.15, 0, 0, 0, 0.08, -0.15, 0, -0.25, 0, 0, 0, 0, 0, -0.17, -0.21, -0.21, 0, -0.2, 0, 0.04, 0.27, 0.17, 0.08, 0.04, -0.1, 0.34, 0, 0, 0.13, 0, 0, 0, 0.36, 0, 0, 0.17, -0.21, 0, 0.01, 0, -0.07, 0.11, 0, 0, 0.08, -0.07, 0.04, -0.14, 0.12, 0, 0, 0, 0, 0, 0, 0, 0.19, 0, 0, 0.07, 0.08, 0.25, 0, 0.04, 0.46, 0, 0, 0.33, 0.08, 0.02, 0, 0, 0, 0, 0, -0.1, 0, 0, 0, 0.62, 0, 0.56, 0, 0.08, 0.29, 0, 0.13, 0.47000000000000003, 0, 0, 0.06, 0, 0, 0, 0.45, 0, 0, 0, 0, 0.23, 0, 0, 0.21, 0, 0.01, 0, 0, 0.11, 0, 0, 0, 0.09, 0, 0, 0, 0.08, 0, 0, 0.11, 0, 0.04, 0, 0, 0.04, 6.000000000000001e-05, 0, 0, 0.5, 0, 0, 0, 0.42, 0, 0, 0, 0, -0.17, 0, 0, -0.07, 0, 0.00048000000000000007, 0.08, 0.13, 0, 0, 0.11, 0, 0.17, 0, 0.42, 0.12, 0, 0.32, -0.06, 0, 0, 0.1, -0.06, 0, 0, 0.2, 0, 0.27, 0, -0.46, 0, 0, 0.04, 0.4, 0, 0.46, 0, 0, 0.2, 0.27, 0, 0, -0.01, 0.23, 0, 0.11, 0, 0.36, 0.03, 0, 0, 0.22, 0, 0.33, 0.13, 0, 0.43, 0, 0.13, 0.16, 0, 0, 0.15, -0.1, 0, 0, 0, -0.36, 0, 0, -0.08, 0, 0, -0.00048000000000000007, -0.08, -0.13, 0, 0.38, -0.16, -0.15, 0, -0.68, 0, 0, 0, -0.36, -0.06, 0, 0, -0.17, 0, 0.21, 0, 0.13, 0, 0, 0.53, 0, 0, 0.4, 0, 0.46, 0, 0.27, 0.21, 0.41000000000000003, 0.28, 0.15, 0, 0.17, 0, 0.73, 0, 0.15, 0, 0, -0.43, 0, 0.38, -0.15, 0, -0.11, 0, 0, 0, -0.42, 0, 0, 0, 0, 0.30000000000000004, 0, 0.13, 0, 0.44, 0, -0.38, 0.07, 0.09, 0.67, 0, 0, 0, 0.13, 0, 0.71, 0.67, 0, 0, 0, 0.38, -0.22, 0, -0.13, 0, 0, -0.02, 0, 0, 0, 0, 0, 0, 0, 0.04, 0.11, 0, -0.22, 0.05, 0.08, 0.04, 0.14, 0.01, 0, 0, 0, 0.47000000000000003, 0, 0, 0, 0, 0, 0.14, 0, 0, 0.04, 0.01, 0.01, 0, 0, 0.26, 0, 0, 0, -0.08, 0.27, 0, 0, -0.35000000000000003, 0.08, -0.27, 0, 0, 0.25, 0, 0, 0, 0, 0.38, 0.12, -0.08, -0.12, 0, 0, 0.19, 0, 0, 0.08, 0.06, 0, 0.07, 0.07, 0, 0, 0, 0, 0, -0.19, 0, -0.06, 0, -0.28, 0, 0, 0.4, 0, 0, 0, 0, 0, 0, 0.07, 0, 0, 0.08, 0, 0, 0.35000000000000003, 0.08, 0.31, 0, 0.13, 0, 0, 0.36, 0.55, 0, 0.39, 0, 0, 0.25, -0.04, 0, 0, 0.16, 0, 0, 0.42, 0, 0, 0, -0.07, 0.07, 0.22, 0, 0, 0, 0, 0, 0.04, 0.17, 0.42, 0.09, 0, 0.05, 0.33, 0, 0, 0, 0, 0.46, 0.37, 0, 0, 0.04, 0, 0.17, 0.23, 0.39, 0, 0, 0.33, 0, 0, 0, 0.15, 0, 0, 0, -0.26, -0.04, 0, 0, 0.05, 0.02, 0, 0, 0, -0.01, 0, 0, 0.38, 0.35000000000000003, 0.35000000000000003, 0, 0, 0, 0.43, 0, 0, 0, 0, 0, 0.27, 0, 0, 0, 0, 0, 0, 0, 0.06, 0, 0, 0, 0, 0, 0.08, -0.5700000000000001, 0.66, -0.29, 0, 0, 0, -0.28, 0.64, 0, 0.05, 0, 0.22, 0, 0.12, -0.56, 0, 0, 0, 0, 0.27, 0, 0, 0.09, 0, 0, 0, 0, 0.08, -0.02, 0, 0, 0, 0.62, 0, 0, 0.13, 0.16, 0, 0.62, 0, 0, 0.42, 0, 0.44, 0, -0.1, 0, 0, 0.00048000000000000007, 0.08, 0.13, 0, -0.37, 0, 0.35000000000000003, 0.06, 0.29, 0, 0, 0.39, 0, 0, -0.42, 0, 0.09, 0, 0, 0.37, -0.28, 0, -0.74, 0, 0, -0.8300000000000001, 0, -0.28, 0, 0.36, 0.11, 0, -0.07, 0, 0, 0, 0.00598, 0, 0, 0.13, 0, 0, 0, 0.81, 0.15, 0, 0, 0, 0.55, 0.04, 0.36, 0.81, 0, -0.74, 0, 0, 0.13, 0, -0.37, 0, 0, -0.22, -0.30000000000000004, 0, 0, -0.74, 0, 0.15, 0, 0, 0, 0, 0, 0.13, 0.08, 0.03, 0.21, 0, 0.36, 0.47000000000000003, 0, 0, 0, 0.45, 0, -0.17, 0, 0, 0, 0, 0, 0, -0.17, 0, -0.25, 0, 0, -0.36, -0.11, 0, 0, -0.08, -0.29, 0.08, 0.11, 0, 0, -0.14, 0, 0, 0, 0, -0.67, 0, 0.45, 0, 0, 0, 0, -0.09, 0, 0, 0, 0.08, -0.11, 0, 0.02, 0, -0.04, 0, 0.07, 0, -0.67, 0, 0, 0, 0.16, -0.5, -0.04, -0.61, 0.02, 0, 0, 0, 0, -0.13, 0, 0, -0.67, 0, 0, -0.36, -0.55, 0]
        self.assertEqual(doc._.sentiment_ratings,sentiment_ratings)
        
    def test_mean_sentiment(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_sentiment,0.06223344927536232)

    def test_med_sentiment(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.median_sentiment,0.0)

    def test_max_sentiment(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.max_sentiment,0.81)

    def test_min_sentiment(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.min_sentiment,-0.8300000000000001)

    def test_stdev_sentiment(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdev_sentiment,0.2668088492047069)

    def test_vwp_arguments(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        vwp_arguments = [0, 1, 2, 4, 5, 6, 7, 8, 9, 18, 19, 20, 21, 22, 26, 33, 34, 35, 37, 39, 40, 42, 44, 45, 47, 48, 72, 73, 75, 78, 79, 80, 114, 115, 116, 117, 118, 119, 120, 121, 122, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 148, 149, 150, 153, 154, 155, 156, 157, 158, 159, 160, 162, 163, 164, 165, 167, 168, 170, 171, 173, 175, 176, 177, 178, 179, 181, 182, 183, 184, 185, 196, 198, 199, 200, 201, 202, 203, 204, 217, 218, 219, 220, 221, 224, 226, 227, 228, 230, 231, 232, 233, 234, 235, 236, 242, 243, 244, 245, 246, 248, 249, 250, 269, 270, 271, 272, 273, 274, 275, 276, 278, 279, 280, 283, 284, 287, 289, 290, 291, 292, 294, 296, 297, 301, 302, 303, 304, 305, 306, 309, 310, 312, 313, 314, 316, 317, 318, 319, 320, 323, 339, 340, 341, 342, 351, 374, 375, 378, 379, 380, 381, 382, 383, 385, 388, 394, 395, 396, 397, 398, 400, 401, 402, 403, 404, 406, 411, 412, 422, 423, 424, 426, 427, 428, 429, 470, 471, 473, 475, 476, 478, 480, 481, 508, 528, 529, 530, 531, 532, 533, 534, 535, 536, 538, 539, 540, 541, 547, 548, 550, 554, 555, 556, 558, 559, 561, 562, 567, 585, 586, 587, 598, 601, 602, 624, 625, 626, 631, 632, 633, 634, 636, 637, 638, 639, 654, 655, 656, 657, 658, 659, 685, 687, 688, 689, 690, 691, 692, 693, 694, 696, 697]
        self.assertEqual(doc._.vwp_arguments,vwp_arguments)

    def test_propn_argument_words(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.propn_argument_words,0.3664772727272727)

    def test_vwp_interactives(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        vwp_interactives = [18, 19, 20, 32, 34, 47, 60, 73, 83, 89, 90, 102, 107, 116, 120, 137, 149, 155, 
168, 215, 226, 230, 236, 266, 269, 271, 279, 293, 300, 302, 303, 316, 355, 360, 
361, 374, 380, 400, 422, 449, 454, 460, 461, 514, 528, 538, 549, 558, 574, 576, 
610, 616, 650, 662, 667, 671, 672, 682, 683, 694, 698]
        self.assertEqual(doc._.vwp_interactives,vwp_interactives)

    def test_propn_interactive(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.propn_interactive,0.08664772727272728)

    # This text contains no quoted or direct speech. We need another test article
    # to do proper regression on these features.
    def test_vwp_quoted(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        vwp_quoted = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.assertEqual(doc._.vwp_quoted,vwp_quoted)

    def test_vwp_direct_speech_spans(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.vwp_direct_speech_spans,[[[400], [], [[394, 410]]]])

    def test_propn_direct_speech(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.propn_direct_speech,0.0)
      
    def test_governing_subjects(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        governing_subjects = [None, None, None, None, None, 3, None, None, 3, 3, None, None, None, 3, None, 3, 3, None, None, None, None, None, None, None, None, None, 31, None, None, None, None, None, None, 31, 31, 31, None, None, None, None, None, None, None, None, 39, 46, None, None, 46, None, None, None, None, None, 53, 53, None, 53, None, None, None, 59, 59, None, 66, None, None, None, None, None, None, None, None, 72, 72, None, None, None, None, 77, 77, None, None, None, 82, None, None, None, None, None, 88, None, None, 89, None, None, None, None, None, None, None, None, None, 100, 100, 100, 100, None, 106, None, None, None, None, None, None, None, None, None, None, None, None, 118, 118, 118, None, 118, 118, None, 118, 118, None, None, None, None, 133, None, 133, None, None, None, 139, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 154, None, None, None, None, None, None, 159, None, None, None, None, None, 166, 166, None, 166, None, None, None, 181, 181, 181, None, None, None, None, None, 181, None, 197, None, None, None, None, None, None, 193, None, None, None, 197, None, None, 197, None, 197, None, None, None, None, None, None, None, None, None, None, None, 214, None, None, 214, 214, 214, None, None, 220, None, None, 227, None, None, None, None, None, None, None, 227, 227, None, None, None, 235, None, None, None, None, None, None, None, 244, None, None, 247, 247, 247, None, None, None, None, None, None, None, None, 253, None, None, None, None, None, 263, 263, 263, None, None, None, None, None, 270, None, None, None, None, None, 277, 277, None, None, 288, None, None, None, 286, None, None, None, None, 288, None, None, None, None, None, None, 298, None, None, None, None, None, 301, 301, None, None, 319, None, None, None, None, None, None, None, 313, None, None, None, None, None, None, None, None, None, None, 337, 337, None, None, None, 334, None, None, None, None, 337, None, 337, 337, 337, None, None, None, None, None, None, 337, None, 352, None, None, None, None, 352, None, None, None, None, 359, None, 360, 360, 360, None, 360, None, None, None, 369, None, None, None, None, None, None, None, None, None, None, None, 378, None, None, None, None, 389, None, None, None, None, None, 400, None, None, None, None, None, None, None, 400, 400, 405, None, 405, None, None, None, None, None, 415, None, None, None, None, None, None, None, None, None, None, 415, 415, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 431, None, None, None, None, None, 442, None, 450, None, None, None, None, None, None, 455, None, None, None, None, None, None, 460, None, None, None, None, None, None, 475, None, None, None, None, None, None, 475, 475, None, 481, 482, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 485, None, 499, 499, None, None, None, None, None, None, None, None, None, None, None, None, None, 511, 511, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 530, None, None, None, None, 537, None, 537, 537, None, 540, None, 540, 540, 540, None, 555, 555, None, 549, 549, None, None, None, None, None, 555, None, 555, None, None, 566, None, None, None, None, 566, None, 570, None, None, None, None, None, None, None, 575, None, None, None, None, None, None, None, None, 575, 575, None, None, None, None, None, None, None, None, 595, None, 595, None, None, None, None, None, None, 609, None, None, None, None, None, 609, None, None, None, None, None, 615, 615, None, 615, None, None, None, None, 623, 623, None, None, None, None, 629, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 667, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 690, None, None, None, None, 695, 694, 699, None, None, None, None, None]
        self.assertEqual(doc._.governing_subjects,governing_subjects)

    def test_content_segments(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')      
        content_segments = [[224, 252, [[229, 247], [237], [239], [240]]], [269, 309, [[277, 288], [286, 307], [299]]], [328, 351, [[333, 334], [329], [330], [331], [336], [337], [344], [348], [349]]], [454, 470, [[459, 468], [455], [456], [457], [462], [463], [467]]], [528, 561, [[537, 552], [543], [545]]], [574, 622, [[579, 595], [589, 606], [575], [577], [580], [591], [593], [596], [603], [608], [609], [611], [615], [617], [618], [620]]], [623, 704, [[623, 640], [628, 647, 701], [629], [635], [642], [644], [648], [669], [676], [679], [680], [695], [699], [702]]]]
        self.assertEqual(doc._.content_segments,content_segments)
        
    def test_prompt_related(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')      
        prompt_related = [[14, 3.6747192922762837, ['technology', 'emerge', 'market', 'nanotechnology'], [3, 46, 161, 212, 229, 247, 286, 307, 333, 334, 405, 537, 552, 589, 606, 623, 640, 695]], [51, 2.7333009865760953, ['thinking', 'assumption', 'argue', 'hypothetical', 'think', 'fact', 'consider', 'layman', 'actually', 'imagine'], [7, 154, 183, 196, 216, 284, 411, 459, 468, 538, 561, 594, 598]], [33, 2.6008002462296087, ['human', 'earth', 'humanity'], [11, 112, 147, 239, 277, 288, 408, 545, 579, 595, 628, 647, 701]]]
        self.assertEqual(doc._.prompt_related,prompt_related)

        
    def test_prompt_language(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')      
        prompt_language = ['technology', 'think', 'thinking', 'human', 'imagine', 'imagination', 'imaginations', 'consider']
        self.assertEqual(doc._.prompt_language,prompt_language)

    def test_core_sentences(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')      
        core_sentences = [[0, 18], [132, 153], [153, 175], [212, 223], [224, 242], [269, 283], [283, 309], [394, 411], [528, 547], [623, 642], [671, 704]]
        self.assertEqual(doc._.core_sentences,core_sentences)

doc = holmes_manager.get_document('GRE_Sample_Essay')
print('a',doc._.content_segments)
print('b',doc._.prompt_related)
print('c',doc._.prompt_language)
print('d',doc._.core_sentences)

