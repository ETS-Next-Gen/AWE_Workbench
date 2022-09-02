import awe_workbench.parser.manager as holmes
from awe_workbench.parser.components.utility_functions import print_parse_tree

import unittest

holmes_manager = holmes.Manager(
    'en_core_web_lg', perform_coreference_resolution=False, number_of_workers=2)

# GRE Sample from https://www.ets.org/gre/revised_general/prepare/analytical_writing/issue/sample_responses
holmes_manager.parse_and_register_document(
            document_text="In all actuality, I think it is more probable that our bodies will surely deteriorate long before our minds do in any significant amount. Who can't say that technology has made us lazier, but that's the key word, lazy, not stupid. The ever increasing amount of technology that we incorporate into our daily lives makes people think and learn every day, possibly more than ever before. Our abilities to think, learn, philosophize, etc. may even reach limits never dreamed of before by average people. Using technology to solve problems will continue to help us realize our potential as a human race.\n\nIf you think about it, using technology to solve more complicating problems gives humans a chance to expand their thinking and learning, opening up whole new worlds for many people. Many of these people are glad for the chance to expand their horizons by learning more, going to new places, and trying new things. If it wasn't for the invention of new technological devices, I wouldn't be sitting at this computer trying to philosophize about technology. It would be extremely hard for children in much poorer countries to learn and think for themselves with out the invention of the internet. Think what an impact the printing press, a technologically superior mackine at the time, had on the ability of the human race to learn and think.\n\nRight now we are seeing a golden age of technology, using it all the time during our every day lives. When we get up there's instant coffee and the microwave and all these great things that help us get ready for our day. But we aren't allowing our minds to deteriorate by using them, we are only making things easier for ourselves and saving time for other important things in our days. Going off to school or work in our cars instead of a horse and buggy. Think of the brain power and genius that was used to come up with that single invention that has changed the way we move across this globe.\n\nUsing technology to solve our continually more complicated problems as a human race is definately a good thing. Our ability to think for ourselves isn't deteriorating, it's continuing to grow, moving on to higher though functions and more ingenious ideas. The ability to use what technology we have is an example", label='GRE_Sample_Essay')


class ViewpointPerspectiveFeatureTest(unittest.TestCase):

    def test_vwp_perspective(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        perspective_spans = {'implicit': {'29': [26, 27, 28, 29, 36, 37], '33': [30, 31, 32, 33, 35], '39': [38, 39, 40, 42, 43, 44, 45, 48], '41': [41], '47': [46, 47], '62': [49, 50, 51, 52, 53, 54, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75], '105': [99, 100, 101, 102, 103, 104, 105, 106, 107, 109, 111, 112, 113, 114, 115, 116], '117': [117], '206': [204, 205, 206, 207, 208, 228], '216': [209, 210, 211, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227], '213': [212, 213], '229': [229, 257], '245': [230, 231, 232, 233, 234, 235, 236, 237, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256], '239': [238, 239], '258': [258], '279': [279, 280], '286': [285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 296, 305], '295': [295], '298': [297, 298, 300, 301, 302, 304], '332': [332], '354': [354, 355, 356, 357, 358, 359, 360, 381], '363': [361, 362, 363, 364, 365, 366, 367, 368, 369, 370], '373': [371, 372, 373, 374, 375], '396': [382, 383, 384, 385, 386, 391, 392, 393, 394, 395, 396, 397, 398, 400, 401], '399': [399], '414': [411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428], '437': [429, 430, 431, 432, 437, 438, 439]}, 'explicit_1': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 34, 55, 56, 57, 58, 59, 60, 61, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 108, 110, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 281, 282, 283, 284, 299, 303, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 333, 334, 335, 336, 337, 345, 376, 377, 378, 379, 380, 387, 388, 389, 390, 402, 403, 404, 405, 406, 407, 408, 409, 410, 433, 434, 435, 436], 'explicit_2': [119], 'explicit_3': {132: [118, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150], 154: [151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177], 341: [338, 339, 340, 341, 342, 343, 344, 346, 347, 348, 349, 350, 351, 352, 353]}}
        self.assertEqual(doc._.vwp_perspective_spans,perspective_spans)

    def test_vwp_stance_markers(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        stance_markers = {'implicit': {'29': [29], '33': [35], '41': [41], '47': [47], '62': [64, 70], '105': [103], '206': [205, 208], '213': [213], '216': [216, 218], '229': [229], '239': [239], '245': [254], '295': [295], '298': [301], '332': [332], '354': [354, 358], '396': [391], '399': [399]}, 'explicit_1': [0, 1, 2, 9, 14, 23, 87, 88, 91, 178, 191, 263, 270, 321, 324, 345, 390, 405], 'explicit_2': [], 'explicit_3': {132: [118, 124, 129, 130, 134, 148], 154: [151, 159]}}
        self.assertEqual(doc._.vwp_stance_markers,stance_markers)

    def test_propn_egocentric(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.propn_egocentric,0.3977272727272727)

    def test_propn_allocentric(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.propn_allocentric,0.17272727272727273)


    def test_propositional_attitudes(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        propositional_attitudes = {'implicit': [[[0, 25], 6, 7], [[26, 48], 26, 29], [[76, 98], 77, 89], [[178, 203], 190, 194], [[204, 228], 204, 206], [[204, 228], 204, 206], [[306, 337], 307, 310]], 'implicit_3': [[[354, 381], None, 354], [[429, 439], 430, 437]], 'explicit_1': [[[0, 25], 4, 5]], 'explicit_2': [[[229, 257], None, 229]], 'explicit_3': {154: [[[151, 177], 154, 156]], 383: [[[382, 401], 383, 396]]}}
        self.assertEqual(doc._.vwp_propositional_attitudes,propositional_attitudes)  
        
    def test_emotional_states(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        emotion_states = {'explicit_1': [], 'explicit_2': [], 'explicit_3': {'People': [156]}}
        self.assertEqual(doc._.vwp_emotion_states,emotion_states)

    def test_character_traits(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        # No character traits detected in this essay. We may need another test
        # with a different text.
        character_traits = {'explicit_1': [35], 'explicit_2': [], 'explicit_3': {}}
        self.assertEqual(doc._.vwp_character_traits,character_traits)
                
    def test_subjectivity_ratings(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        subjectivity_ratings = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.8888888888888888, 0.0, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.39999999999999997, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.45454545454545453, 0.0, 0.0, 0.5, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.45454545454545453, 0.0, 0.0, 0.0, 0.0, 0.45454545454545453, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.45454545454545453, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.5416666666666666, 0.0, 0.0, 0.0, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.9, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5357142857142857, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6666666666666666, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.75, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.375, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.21428571428571427, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 1.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.6000000000000001, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.5, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.assertEqual(doc._.subjectivity_ratings,subjectivity_ratings)

    def test_mean_subjectivity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_subjectivity,0.11994355317884729)

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
        self.assertEqual(doc._.stdev_subjectivity,0.28616783063337886)

    def test_polarity_ratings(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        polarity_ratings = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, -0.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.375, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.25, 0.0, 0.0, -0.7999999999999999, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.15, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.13636363636363635, 0.0, 0.0, 0.5, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.13636363636363635, 0.0, 0.0, 0.0, 0.0, 0.13636363636363635, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.13636363636363635, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.125, -0.2916666666666667, 0.0, 0.0, 0.0, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2857142857142857, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.125, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.07142857142857142, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.assertEqual(doc._.polarity_ratings,polarity_ratings)

    def test_mean_polarity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_polarity,0.022459256429844664)

    def test_med_polarity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.median_polarity,0.0)

    def test_max_polarity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.max_polarity,0.8)

    def test_min_polarity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.min_polarity,-0.7999999999999999)

    def test_stdev_polarity(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdev_polarity,0.15416665096742294)

    def test_sentiment_ratings (self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        sentiment_ratings = [0, 0.21, 0.1, 0, -0.19, 0.42, 0, 0, 0, 0.11, 0, 0, 0, 0.08, 0.15, -0.34, -0.05, 0, 0, 0, 0.1, 0, 0, 0.4, 0.1, 0, 0, 0, 0, -0.22, 0, -0.13, 0, -0.12, 0, 0, 0, 0, 0, 0, 0, 0.30000000000000004, 0.19, 0, -0.48, 0, -0.38, -0.54, 0, 0, 0, 0, 0.1, 0, 0.13, 0, 0, 0.09, 0, 0, 0.18, 0, 0, 0.17, 0.42, 0, 0.46, 0.1, 0.34, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.42, 0, 0.46, 0, 0.15, 0, 0, 0, 0.13, 0.08, 0.19, 0, 0.39, 0.28, 0, 0, 0.1, 0.02, -0.17, 0, 0, 0.13, 0, 0.32, 0, 0.08, 0.15, 0, 0.48, 0, 0.36, 0, 0.46, -0.07, 0.04, 0.36, 0.11, 0, 0, 0, 0, 0.42, 0.11, 0, 0, 0, 0.13, 0, 0.32, 0, 0, 0, 0, 0, 0.04, 0.26, 0, 0.08, 0, 0.15, 0, 0.17, 0, 0.23, 0.34, 0.21, 0.67, 0, 0, 0, 0.17, 0, 0, 0, 0, 0.17, 0, 0.63, 0, 0, 0.26, 0, 0.08, 0, 0, -0.1, 0.17, 0, 0, -0.01, 0, 0.67, 0, 0, 0, -0.38, 0.67, 0, 0, 0, 0, 0, 0, 0, 0, 0.35000000000000003, 0, 0.67, 0.07, 0, 0, 0.19, 0, 0, -0.29, 0.16, 0, 0, -0.46, 0.38, 0, -0.15, -0.11, -0.13, 0, 0, 0, 0.29, 0.30000000000000004, -0.16, 0, 0, 0, 0.19, 0, 0, 0, 0.46, 0, 0.42, 0, 0, 0, -0.30000000000000004, 0, 0.35000000000000003, 0, 0, 0.42, 0, 0.42, 0, -0.07, 0.19, 0, 0.08, 0.09, 0, 0.04, 0, 0.34, 0, 0, 0, 0.15, 0, 0, 0.08, 0, 0.5, 0, 0, 0.36, 0.11, 0, 0.46, 0, 0.42, 0, 0, 0.58, 0.06, 0, 0, -0.02, 0.04, 0.6900000000000001, 0.19, 0, 0.13, 0, 0, 0, 0.21, 0, 0.15, 0, 0, 0.1, 0.34, 0, 0, 0, 0, 0.27, 0.34, 0, 0, 0.21, 0.5, 0, 0, 0.06, 0, 0.21, 0, 0.62, 0, 0, 0.48, 0, 0.27, 0.41000000000000003, 0, 0, 0.34, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.34, 0.1, 0, 0, 0, 0, 0, -0.07, 0, 0, 0, 0, 0, 0, -0.25, -0.15, 0, -0.1, -0.45, 0, 0, 0, 0, 0, -0.01, -0.04, 0, 0.1, 0, 0.01, 0, 0, 0, -0.08, 0, 0.04, 0.26, 0, -0.08, 0, 0.42, 0, 0, 0.30000000000000004, 0.24, 0, 0.63, 0, 0, 0.13, 0, 0.16, 0.34, 0, 0, 0.09, 0.35000000000000003, 0, 0, 0.21, 0, 0.22, 0, -0.01, 0, 0, 0.28, 0, 0, 0, 0.13, 0, 0.32, 0, 0.12, 0, -0.29, 0, -0.07, 0.04, 0.36, 0.11, 0, 0, 0.04, 0.72, 0.13, 0, 0, -0.5, 0, -0.42, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.32, 0, 0.15, 0.08, 0, 0.1, 0, 0, 0, 0, 0.15, 0, 0, 0, 0.5, 0, 0.04, 0, 0.13, 0, 0.21, 0, -0.07, -0.02]
        self.assertEqual(doc._.sentiment_ratings,sentiment_ratings)
        
    def test_mean_sentiment(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_sentiment,0.1507058823529412)

    def test_med_sentiment(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.median_sentiment,0.13)

    def test_max_sentiment(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.max_sentiment,0.72)

    def test_min_sentiment(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.min_sentiment,-0.54)

    def test_stdev_sentiment(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdev_sentiment,0.24638349016431318)

    def test_vwp_arguments(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        vwp_arguments = [0, 1, 2, 4, 5, 7, 8, 9, 10, 13, 14, 20, 21, 22, 23, 24, 26, 27, 28, 29, 30, 32, 33, 34, 35, 37, 66, 70, 71, 72, 76, 77, 78, 79, 87, 88, 90, 91, 93, 95, 99, 101, 102, 103, 104, 106, 107, 118, 120, 124, 126, 127, 128, 129, 130, 131, 133, 134, 135, 136, 138, 157, 158, 159, 160, 161, 164, 165, 166, 178, 180, 181, 182, 183, 184, 185, 190, 191, 192, 198, 199, 200, 201, 229, 230, 232, 245, 246, 247, 248, 249, 253, 254, 306, 319, 320, 321, 322, 324, 325, 354, 355, 356, 358, 361, 362, 363, 364, 383, 386, 387, 389, 390, 391, 392, 399, 422, 430, 431, 432, 438, 439]

        self.assertEqual(doc._.vwp_arguments,vwp_arguments)

    def test_propn_argument_words(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.propn_argument_words,0.2772727272727273)

    def test_vwp_interactives(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        vwp_interactives = [4, 5, 8, 11, 14, 18, 28, 32, 34, 38, 39, 47, 55, 56, 59, 64, 71, 76, 79, 108, 110, 119, 120, 128, 145, 153, 155, 156, 170, 175, 176, 181, 186, 190, 192, 193, 196, 207, 218, 229, 256, 261, 262, 272, 276, 282, 285, 286, 293, 294, 295, 296, 297, 299, 303, 307, 308, 309, 311, 319, 320, 323, 326, 333, 335, 345, 354, 361, 362, 368, 371, 372, 376, 379, 387, 389, 396, 399, 400, 402, 405, 407, 408, 409, 413, 421, 425, 435, 437]
        self.assertEqual(doc._.vwp_interactives,vwp_interactives)

    def test_propn_interactive(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.propn_interactive,0.20227272727272727)

    # This text contains no quoted or direct speech. We need another test article
    # to do proper regression on these features.
    def test_vwp_quoted(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        vwp_quoted = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.assertEqual(doc._.vwp_quoted,vwp_quoted)

    def test_vwp_direct_speech_spans(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.vwp_direct_speech_spans,[[[4], [], [[0, 25]]]])

    def test_propn_direct_speech(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.propn_direct_speech,0.0)
      
    def test_governing_subjects(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        governing_subjects = [4, None, 4, None, None, 4, None, 6, 9, 6, None, None, 11, None, 12, 12, 12, None, None, 18, 19, 19, None, 19, 19, None, None, None, None, 26, None, None, None, 31, None, 34, None, None, None, 38, None, 38, 38, None, 38, None, None, 38, None, None, None, None, None, None, None, None, None, 56, 55, None, 59, 59, 54, None, 63, None, 63, None, None, None, 63, 63, None, None, None, None, None, 76, None, 76, None, 76, None, 76, None, 76, None, None, 77, 77, None, None, None, None, None, None, None, None, None, None, None, None, 100, None, None, 99, None, 99, None, 108, None, 110, 110, None, 110, 110, None, None, None, None, 119, 119, None, None, None, None, None, 125, None, None, None, 124, None, None, None, None, None, None, 137, None, None, None, None, None, None, None, None, 146, 146, 146, None, None, None, None, None, 154, 154, 154, None, 154, None, None, None, 162, 163, 163, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 179, None, 179, None, None, None, None, None, None, None, None, None, None, None, 190, 190, None, None, 190, None, 190, 190, None, None, None, None, 204, 208, 204, None, None, None, 213, None, None, None, 210, None, 210, 210, None, 210, 210, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 239, None, None, None, None, None, None, 235, 232, None, 232, 232, None, 232, 232, None, None, None, None, None, None, 261, 261, None, None, 261, None, None, None, None, None, None, 261, None, None, None, None, 271, None, None, 276, None, None, 282, None, 282, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 296, None, 299, 299, 299, None, 303, None, None, None, None, None, 307, None, 311, None, 312, 312, 312, None, None, None, None, 319, 319, None, 323, 323, None, None, 319, None, 329, 329, 329, 329, 329, None, 335, None, None, None, None, None, None, None, None, None, 345, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 361, None, 361, None, 361, None, None, None, None, None, 370, None, None, None, 376, 376, None, None, None, None, None, None, None, None, None, 390, 390, 387, 387, None, None, None, None, 383, 383, None, 383, 383, None, None, 402, None, 402, 402, None, None, None, 403, None, None, None, 412, None, 412, None, 412, None, 412, 412, None, None, None, 426, None, None, None, None, None, None, None, None, None, None, 435, 430, None, 430]
        self.assertEqual(doc._.governing_subjects,governing_subjects)

    def test_content_segments(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')      
        content_segments = [[0, 26, [[12, 19], [15]]], [26, 76, [[31, 54], [41], [42], [44], [47], [51], [57], [60], [61], [62]]], [178, 204, [[187, 188, 202], [194], [197]]]]
        self.assertEqual(doc._.content_segments,content_segments)
        
    def test_prompt_related(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')      
        prompt_related = [[16, 2.0255215718047395, ['technology', 'technological', 'device'], [31, 54, 100, 125, 187, 188, 202, 268, 384, 434]], [14, 1.7660044150110379, ['solve', 'problem', 'complicating', 'complicated'], [102, 103, 127, 129, 130, 386, 390, 391]], [18, 1.6330696606277109, ['body', 'mind', 'human', 'brain'], [12, 19, 114, 132, 251, 312, 357, 394]]]
        self.assertEqual(doc._.prompt_related,prompt_related)
        
    def test_prompt_language(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')      
        prompt_language = ['mind', 'minds', 'technology', 'solve', 'problem', 'problems', 'human', 'complicate', 'complicating']
        self.assertEqual(doc._.prompt_language,prompt_language)

    def test_core_sentences(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')      
        core_sentences = [[99, 117], [118, 151], [229, 258], [382, 402]]
        self.assertEqual(doc._.core_sentences,core_sentences)

doc = holmes_manager.get_document('GRE_Sample_Essay')
print('a',doc._.content_segments)
print('b',doc._.prompt_related)
print('c',doc._.prompt_language) 
print('d',doc._.core_sentences)

