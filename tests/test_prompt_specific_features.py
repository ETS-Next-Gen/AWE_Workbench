#!/usr/bin/env python3.10
# Copyright 2022, Educational Testing Service

import holmes_extractor.manager as holmes
from awe_components.components.utility_functions import print_parse_tree
from awe_components.components.contentSegmentation import *
import unittest
from awe_workbench.pipeline import pipeline_def

holmes_manager = holmes.Manager(
    'en_core_web_lg', perform_coreference_resolution=False, number_of_workers=2, extra_components=pipeline_def)

# GRE Sample from https://www.ets.org/gre/revised_general/prepare/analytical_writing/issue/sample_responses
text = "The statement linking technology negatively with free thinking plays on recent human experience over the past century. Surely there has been no time in history where the lived lives of people have changed more dramatically. A quick reflection on a typical day reveals how technology has revolutionized the world. Most people commute to work in an automobile that runs on an internal combustion engine. During the workday, chances are high that the employee will interact with a computer that processes information on silicon bridges that are .09 microns wide. Upon leaving home, family members will be reached through wireless networks that utilize satellites orbiting the earth. Each of these common occurrences could have been inconceivable at the turn of the 19th century.\n\nThe statement attempts to bridge these dramatic changes to a reduction in the ability for humans to think for themselves. The assumption is that an increased reliance on technology negates the need for people to think creatively to solve previous quandaries. Looking back at the introduction, one could argue that without a car, computer, or mobile phone, the hypothetical worker would need to find alternate methods of transport, information processing and communication. Technology short circuits this thinking by making the problems obsolete.\n\nHowever, this reliance on technology does not necessarily preclude the creativity that marks the human species. The prior examples reveal that technology allows for convenience. The car, computer and phone all release additional time for people to live more efficiently. This efficiency does not preclude the need for humans to think for themselves. In fact, technology frees humanity to not only tackle new problems, but may itself create new issues that did not exist without technology. For example, the proliferation of automobiles has introduced a need for fuel conservation on a global scale. With increasing energy demands from emerging markets, global warming becomes a concern inconceivable to the horse-and-buggy generation. Likewise dependence on oil has created nation-states that are not dependent on taxation, allowing ruling parties to oppress minority groups such as women. Solutions to these complex problems require the unfettered imaginations of maverick scientists and politicians.\n\nIn contrast to the statement, we can even see how technology frees the human imagination. Consider how the digital revolution and the advent of the internet has allowed for an unprecedented exchange of ideas. WebMD, a popular internet portal for medical information, permits patients to self research symptoms for a more informed doctor visit. This exercise opens pathways of thinking that were previously closed off to the medical layman. With increased interdisciplinary interactions, inspiration can arrive from the most surprising corners. Jeffrey Sachs, one of the architects of the UN Millenium Development Goals, based his ideas on emergency care triage techniques. The unlikely marriage of economics and medicine has healed tense, hyperinflation environments from South America to Eastern Europe.\n\nThis last example provides the most hope in how technology actually provides hope to the future of humanity. By increasing our reliance on technology, impossible goals can now be achieved. Consider how the late 20th century witnessed the complete elimination of smallpox. This disease had ravaged the human race since prehistorical days, and yet with the technology of vaccines, free thinking humans dared to imagine a world free of smallpox. Using technology, battle plans were drawn out, and smallpox was systematically targeted and eradicated.\n\nTechnology will always mark the human experience, from the discovery of fire to the implementation of nanotechnology. Given the history of the human race, there will be no limit to the number of problems, both new and old, for us to tackle. There is no need to retreat to a Luddite attitude to new things, but rather embrace a hopeful posture to the possibilities that technology provides for new avenues of human imagination."
label = 'GRE_Sample_Essay'

prompt = "As people rely more and more on technology to solve problems, the ability of humans to think for themselves will surely deteriorate."
prompt_label = 'Prompt texst'

holmes_manager.parse_and_register_document(text, label)


class PromptSpecificFeatureTest(unittest.TestCase):

    def test_content_segments(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        content_segments = [[18, 37], [37, 52], [52, 68], [68, 95], [95, 114], [114, 131], [242, 269], [309, 328], [328, 351], [351, 392], [411, 470], [470, 526], [527, 547], [547, 561], [561, 574], [574, 621]]
        self.assertEqual(doc._.content_segments,
                         content_segments)

    def test_prompt_related(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        prompt_related = [[14, 3.6747192922762837, ['technology', 'emerge', 'market', 'Technology', 'nanotechnology'], [3, 46, 161, 212, 229, 247, 286, 307, 333, 334, 405, 537, 552, 589, 606, 623, 640, 695]], [51, 2.7333009865760953, ['thinking', 'assumption', 'argue', 'hypothetical', 'fact', 'consider', 'layman', 'actually', 'imagine'], [7, 154, 183, 196, 216, 284, 411, 459, 468, 538, 561, 594, 598]], [33, 2.6008002462296087, ['human', 'earth', 'humanity'], [11, 112, 147, 239, 277, 288, 408, 545, 579, 595, 628, 647, 701]]]
        self.assertEqual(doc._.prompt_related,
                         prompt_related)

    def test_prompt_language(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        prompt_language = ['technology', 'think', 'thinking', 'human', 'sure', 'surely', 'chance', 'chances', 'conceive', 'inconceivable', 'look', 'looking', 'argue', 'however', 'necessary', 'necessarily', 'create', 'creativity', 'efficient', 'efficiency', 'fact', 'only', 'imagine', 'imagination', 'imaginations', 'contrast', 'consider', 'hope', 'yet', 'embrace']
        self.assertEqual(doc._.prompt_language,
                         prompt_language)

    def test_core_sentences(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        core_sentences = [[0, 18], [131, 153], [153, 175], [212, 223], [283, 309], [393, 411], [671, 704]]
        self.assertEqual(doc._.core_sentences,
                         core_sentences)

    def test_extended_core_sentences(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        extended_core_sentences = [[175, 212], [223, 242], [269, 283], [622, 642], [642, 671]]
        self.assertEqual(doc._.extended_core_sentences,
                         extended_core_sentences)
