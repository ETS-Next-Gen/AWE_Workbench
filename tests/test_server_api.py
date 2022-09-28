#!/usr/bin/env python3.10
# Copyright 2022, Educational Testing Service

import pickle
import base64
import math
import time
import os
import sys
import pandas as pd
import pandas.testing as pd_testing
import random
import threading
import unittest
from multiprocessing import Process, Queue

import awe_languagetool.languagetoolServer
import awe_spellcorrect.spellcorrectServer
import awe_workbench.web.parserServer
from awe_workbench.web.websocketClient import websocketClient
from awe_languagetool.languagetoolClient import languagetoolClient


def startServers():
    queue = Queue()
    p1 = Process(target=awe_languagetool.languagetoolServer.runServer, args=())
    p1.start()

    p2 = Process(target=awe_spellcorrect.spellcorrectServer.spellcorrectServer, args=())
    p2.start()

    p3 = Process(target=awe_workbench.web.parserServer.parserServer, args=())
    p3.start()
    time.sleep(60)
    return p1, p2, p3


def initialize():
    """
    Initialize our CorpusSpellcheck and parser objects (for spell-
    correction and parsing with spacy + coreferee and other extensions
    using a modified version of the holmes extractor library. While
    doing so, we initialize a series of lexical databases that support
    some of the metrics we want to capture.
    """
    # Initialize the spellchecker
    cs = websocketClient()
    lt = languagetoolClient()

    # Initialize the parser
    parser = websocketClient()
    parser.set_uri("ws://localhost:8766")

    # return spellchecker and parser objects
    return cs, parser, lt

# GRE Samples from https://www.ets.org/gre/revised_general/prepare/analytical_writing/issue/sample_responses
# Aesop's fable is a public domain document available
# at http://read.gov/aesop/007.html


labels = ['GRE_Sample_Essay_1', 'GRE_Sample_Essay_2', 'Aesop']
texts = ["The statement linking technology negatively with free thinking plays on recent human experience over the past century. Surely there has been no time in history where the lived lives of people have changed more dramatically. A quick reflection on a typical day reveals how technology has revolutionized the world. Most people commute to work in an automobile that runs on an internal combustion engine. During the workday, chances are high that the employee will interact with a computer that processes information on silicon bridges that are .09 microns wide. Upon leaving home, family members will be reached through wireless networks that utilize satellites orbiting the earth. Each of these common occurrences could have been inconceivable at the turn of the 19th century.\n\nThe statement attempts to bridge these dramatic changes to a reduction in the ability for humans to think for themselves. The assumption is that an increased reliance on technology negates the need for people to think creatively to solve previous quandaries. Looking back at the introduction, one could argue that without a car, computer, or mobile phone, the hypothetical worker would need to find alternate methods of transport, information processing and communication. Technology short circuits this thinking by making the problems obsolete.\n\nHowever, this reliance on technology does not necessarily preclude the creativity that marks the human species. The prior examples reveal that technology allows for convenience. The car, computer and phone all release additional time for people to live more efficiently. This efficiency does not preclude the need for humans to think for themselves. In fact, technology frees humanity to not only tackle new problems, but may itself create new issues that did not exist without technology. For example, the proliferation of automobiles has introduced a need for fuel conservation on a global scale. With increasing energy demands fropython force script to exitm emerging markets, global warming becomes a concern inconceivable to the horse-and-buggy generation. Likewise dependence on oil has created nation-states that are not dependent on taxation, allowing ruling parties to oppress minority groups such as women. Solutions to these complex problems require the unfettered imaginations of maverick scientists and politicians.\n\nIn contrast to the statement, we can even see how technology frees the human imagination. Consider how the digital revolution and the advent of the internet has allowed for an unprecedented exchange of ideas. WebMD, a popular internet portal for medical information, permits patients to self research symptoms for a more informed doctor visit. This exercise opens pathways of thinking that were previously closed off to the medical layman. With increased interdisciplinary interactions, inspiration can arrive from the most surprising corners. Jeffrey Sachs, one of the architects of the UN Millenium Development Goals, based his ideas on emergency care triage techniques. The unlikely marriage of economics and medicine has healed tense, hyperinflation environments from South America to Eastern Europe.\n\nThis last example provides the most hope in how technology actually provides hope to the future of humanity. By increasing our reliance on technology, impossible goals can now be achieved. Consider how the late 20th century witnessed the complete elimination of smallpox. This disease had ravaged the human race since prehistorical days, and yet with the technology of vaccines, free thinking humans dared to imagine a world free of smallpox. Using technology, battle plans were drawn out, and smallpox was systematically targeted and eradicated.\n\nTechnology will always mark the human experience, from the discovery of fire to the implementation of nanotechnology. Given the history of the human race, there will be no limit to the number of problems, both new and old, for us to tackle. There is no need to retreat to a Luddite attitude to new things, but rather embrace a hopeful posture to the possibilities that technology provides for new avenues of human imagination.", "In recent centuries, humans have developed the technology very rapidly, and you may accept some merit of it, and you may see a distortion in society occured by it. To be lazy for human in some meaning is one of the fashion issues in thesedays. There are many symptoms and resons of it. However, I can not agree with the statement that the technology make humans to be reluctant to thinkng thoroughly.\n\nOf course, you can see the phenomena of human laziness along with developed technology in some place. However, they would happen in specific condition, not general. What makes human to be laze of thinking is not merely technology, but the the tendency of human that they treat them as a magic stick and a black box. Not understanding the aims and theory of them couses the disapproval problems.\n\nThe most important thing to use the thechnology, regardless the new or old, is to comprehend the fundamental idea of them, and to adapt suit tech to tasks in need. Even if you recognize a method as a all-mighty and it is extremely over-spec to your needs, you can not see the result you want. In this procedure, humans have to consider as long as possible to acquire adequate functions. Therefore, humans can not escape from using their brain.\n\nIn addition, the technology as it is do not vain automatically, the is created by humans. Thus, the more developed tech and the more you want a convenient life, the more you think and emmit your creativity to breakthrough some banal method sarcastically.\n\nConsequently, if you are not passive to the new tech, but offensive to it, you would not lose your ability to think deeply. Furthermore, you may improve the ability by adopting it.", "A lion lay asleep in the forest, his great head resting on his paws. A timid little mouse came upon him unexpectedly, and in her fright and haste to get away, ran across the lion's nose. Roused from his nap, the lion laid his huge paw angrily on the tiny creature to kill her.\n\n\"Spare me!\" begged the poor mouse. \"Please let me go and some day I will surely repay you.\"\n\nThe lion was much amused to think that a mouse could ever help him. But he was generous and finally let the mouse go.\n\nSome days later, while stalking his prey in the forest, the lion was caught in the toils of a hunter's net. Unable to free himself, he filled the forest with his angry roaring. The mouse knew the voice and quickly found the lion struggling in the net. Running to one of the great ropes that bound him, she gnawed it until it parted, and soon the lion was free.\n\n\"You laughed when I said I would repay you,\" said the Mouse. \"Now you see that even a Mouse can help a Lion.\""]


class ServerAPITest(unittest.TestCase):

    p1 = None
    p2 = None
    p3 = None
    cs = None
    parser = None
    lt = None

    @classmethod
    def setUpClass(self):
        self.p1, self.p2, self.p3 = startServers()
        self.cs, self.parser, self.lt = initialize()

    @classmethod
    def tearDownClass(self):
        self.p1.terminate()
        self.p2.terminate()
        self.p3.terminate()
        self.p1 = None
        self.p2 = None
        self.p3 = None
        self.cs = None
        self.parser = None
        self.lt = None

    def testLTMatch(self):
        record = None
        matches = self.lt.processText(record, texts[1])
        # with open("pickles/ltmatches.pkl", "wb") as fp:
        #     pickle.dump(matches, fp)
        #     fp.close()
        with open("pickles/ltmatches.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(matches, comparison)

    def testLTSummary(self):
        df1 = self.lt.summarizeMultipleTexts(labels, texts)
        df1.set_index('ID', inplace=True)
        print(df1)
        # with open("pickles/languagetool_summary.pkl", "wb") as fp:
        #     pickle.dump(df1, fp)
        #     fp.close()
        df2 = pd.read_pickle('pickles/languagetool_summary.pkl')
        pd_testing.assert_frame_equal(df1, df2)

    def testSpellCorrect(self):
        corrected = self.cs.send(texts)
        # with open("pickles/spellcorrected.pkl", "wb") as fp:
        #     pickle.dump(corrected, fp)
        #     fp.close()
        with open('pickles/spellcorrected.pkl', 'rb') as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(corrected, comparison)

    def test_parseset(self):
        ok = self.parser.send(['PARSESET', [labels, texts]])
        print('parsed', ok)
        self.assertEqual(ok, True)
        labels2 = self.parser.send(['LABELS'])
        self.assertEqual(labels.sort(), labels2.sort())
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def test_parseone(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        print('parsed', ok)
        self.assertEqual(ok, True)
        ok = self.parser.send(['REMOVE', labels[0]])
        self.assertEqual(ok, True)

    def testDocTokens(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        tokens = self.parser.send(['DOCTOKENS', labels[0]])
        #with open("pickles/doctokens.pkl", "wb") as fp:
        #    pickle.dump(tokens, fp)
        #    fp.close()
        with open("pickles/doctokens.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(tokens, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testDocHeads(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['DOCHEADS', labels[0]])
        # with open("pickles/docheads.pkl", "wb") as fp:
        #     pickle.dump(data, fp)
        #     fp.close()
        with open("pickles/docheads.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testDocDependencies(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['DOCDEPENDENCIES', labels[0]])
        # with open("pickles/docdependencies.pkl", "wb") as fp:
        #     pickle.dump(data, fp)
        #     fp.close()
        with open("pickles/docdependencies.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testDocEntities(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['DOCENTITIES', labels[0]])
        # with open("pickles/docentities.pkl", "wb") as fp:
        #     pickle.dump(data, fp)
        #     fp.close()
        with open("pickles/docentities.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testSearchPhrase(self):
        ok = self.parser.send(['PARSEONE',
                               'test',
                               'A dog barked at a cat'])
        self.assertEqual(ok, True)
        self.parser.send(['NEWSEARCHPHRASE', 'dogs bark', 'db'])
        matches = self.parser.send(['MATCH_DOCUMENTS'])
        # with open("pickles/matches_docs.pkl", "wb") as fp:
        #     pickle.dump(matches, fp)
        #     fp.close()
        with open("pickles/matches_docs.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        ok = self.parser.send(['REMOVELABELEDSEARCH', 'db'])
        self.assertEqual(ok, True)
        ok = self.parser.send(['CLEARSEARCHES'])
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testSearchPhrase2(self):
        ok = self.parser.send(['PARSESET', [labels, texts]])
        self.assertEqual(ok, True)
        ok = self.parser.send(['NEWSEARCHPHRASE',
                               'A mouse helps a lion', 'ml'])
        ok = self.parser.send(['NEWSEARCHPHRASE',
                               'Technology encourages thinking', 'tt'])
        ok = self.parser.send(['NEWSEARCHPHRASE',
                               'No man saw me', 'nm'])
        ok = self.parser.send(['REMOVELABELEDSEARCH', 'nm'])
        self.assertEqual(ok, True)
        info = self.parser.send(['SHOWSEARCHLABELS'])
        # with open("pickles/searchlabels.pkl", "wb") as fp:
        #     pickle.dump(info, fp)
        #     fp.close()
        with open("pickles/searchlabels.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        print(info, '\n', comparison)
        self.assertEqual(info, comparison)
        matches = self.parser.send(['MATCH_DOCUMENTS'])
        # with open("pickles/matches_docs.pkl", "wb") as fp:
        #     pickle.dump(matches, fp)
        #     fp.close()
        with open("pickles/matches_docs.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(matches, comparison)
        ok = self.parser.send(['CLEARSEARCHES'])
        self.assertEqual(ok, True)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testTopicMatches(self):
        ok = self.parser.send(['PARSESET', [labels, texts]])
        self.assertEqual(ok, True)
        matches = self.parser.send(['TOPIC_MATCHES',
                                   'A mouse helps a lion.'])
        # with open("pickles/topicmatches.pkl", "wb") as fp:
        #     pickle.dump(matches, fp)
        #     fp.close()
        with open("pickles/topicmatches.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(comparison, matches)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testLemmas(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['LEMMAS', labels[0]])
        # with open("pickles/lemmas.pkl", "wb") as fp:
        #     pickle.dump(data, fp)
        #     fp.close()
        with open("pickles/lemmas.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testWordTypes(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['WORDTYPES', labels[0]])
        # with open("pickles/wordtypes.pkl", "wb") as fp:
        #     pickle.dump(data, fp)
        #     fp.close()
        with open("pickles/wordtypes.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testRoots(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['ROOTS', labels[0]])
        # with open("pickles/roots.pkl", "wb") as fp:
        #     pickle.dump(data, fp)
        #     fp.close()
        with open("pickles/roots.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testSyllables(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['SYLLABLES', labels[0]])
        # with open("pickles/syllables.pkl", "wb") as fp:
        #     pickle.dump(data, fp)
        #     fp.close()
        with open("pickles/syllables.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testWordLength(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['WORDLENGTH', labels[0]])
        # with open("pickles/wordlength.pkl", "wb") as fp:
        #     pickle.dump(data, fp)
        #     fp.close()
        with open("pickles/wordlength.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testLatinates(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['LATINATES', labels[0]])
        # with open("pickles/latinates.pkl", "wb") as fp:
        #     pickle.dump(data, fp)
        #     fp.close()
        with open("pickles/latinates.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testAcademics(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['ACADEMICS', labels[0]])
        # with open("pickles/academics.pkl", "wb") as fp:
        #     pickle.dump(data, fp)
        #     fp.close()
        with open("pickles/academics.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testFamilySizes(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['FAMILYSIZES', labels[0]])
        # with open("pickles/familysizes.pkl", "wb") as fp:
        #     pickle.dump(data, fp)
        #     fp.close()
        with open("pickles/familysizes.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testSenseNums(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['SENSENUMS', labels[0]])
        # with open("pickles/sensenums.pkl", "wb") as fp:
        #     pickle.dump(data, fp)
        #     fp.close()
        with open("pickles/sensenums.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testLogSenseNums(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['LOGSENSENUMS', labels[0]])
        # with open("pickles/logsensenums.pkl", "wb") as fp:
        #     pickle.dump(data, fp)
        #     fp.close()
        with open("pickles/logsensenums.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testMorpholex(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['MORPHOLOGY', labels[0]])
        # with open("pickles/morpholex.pkl", "wb") as fp:
        #     pickle.dump(data, fp)
        #     fp.close()
        with open("pickles/morpholex.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testMorphNums(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['MORPHNUMS', labels[0]])
        # with open("pickles/morphnums.pkl", "wb") as fp:
        #     pickle.dump(data, fp)
        #     fp.close()
        with open("pickles/morphnums.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testHALRootFreqs(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['HALROOTFREQS', labels[0]])
        # with open("pickles/halrootfreqs.pkl", "wb") as fp:
        #     pickle.dump(data, fp)
        #     fp.close()
        with open("pickles/halrootfreqs.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testHALLogRootFreqs(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['HALLOGROOTFREQS', labels[0]])
        # with open("pickles/hallogrootfreqs.pkl", "wb") as fp:
        #     pickle.dump(data, fp)
        #     fp.close()
        with open("pickles/hallogrootfreqs.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testRootFamSizes(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['ROOTFAMSIZES', labels[0]])
        # with open("pickles/rootfamsizes.pkl", "wb") as fp:
        #     pickle.dump(data, fp)
        #     fp.close()
        with open("pickles/rootfamsizes.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testRootPFMFs(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['ROOTPFMFS', labels[0]])
        # with open("pickles/rootpfmfs.pkl", "wb") as fp:
        #     pickle.dump(data, fp)
        #     fp.close()
        with open("pickles/rootpfmfs.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testLemmaFreqs(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['LEMMAFREQS', labels[0]])
        # with open("pickles/lemmafreqs.pkl", "wb") as fp:
        #     pickle.dump(data, fp)
        #     fp.close()
        with open("pickles/lemmafreqs.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testRootFreqs(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['ROOTFREQS', labels[0]])
        # with open("pickles/rootfreqs.pkl", "wb") as fp:
        #     pickle.dump(data, fp)
        #     fp.close()
        with open("pickles/rootfreqs.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testMaxFreqs(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['MAXFREQS', labels[0]])
        # with open("pickles/maxfreqs.pkl", "wb") as fp:
        #     pickle.dump(data, fp)
        #     fp.close()
        with open("pickles/maxfreqs.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testConcretes(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['CONCRETES', labels[0]])
        # with open("pickles/concretes.pkl", "wb") as fp:
        #     pickle.dump(data, fp)
        #     fp.close()
        with open("pickles/concretes.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testAnimates(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['ANIMATES', labels[0]])
        # with open("pickles/animates.pkl", "wb") as fp:
        #      pickle.dump(data, fp)
        #      fp.close()
        with open("pickles/animates.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testAbstractTraits(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['ABSTRACTTRAITS', labels[0]])
        # with open("pickles/abstracttraits.pkl", "wb") as fp:
        #      pickle.dump(data, fp)
        #      fp.close()
        with open("pickles/abstracttraits.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testDeictics(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['DEICTICS', labels[0]])
        # with open("pickles/deictics.pkl", "wb") as fp:
        #      pickle.dump(data, fp)
        #      fp.close()
        with open("pickles/deictics.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testParagraphs(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['PARAGRAPHS', labels[0]])
        # with open("pickles/paragraphs.pkl", "wb") as fp:
        #      pickle.dump(data, fp)
        #      fp.close()
        with open("pickles/paragraphs.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testParagraphLens(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['PARAGRAPHLENS', labels[0]])
        # with open("pickles/paragraphlens.pkl", "wb") as fp:
        #      pickle.dump(data, fp)
        #      fp.close()
        with open("pickles/paragraphlens.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testTransitionProfile(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['TRANSITIONPROFILE', labels[0]])
        # with open("pickles/transitionprofile.pkl", "wb") as fp:
        #      pickle.dump(data, fp)
        #      fp.close()
        with open("pickles/transitionprofile.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testTransitionDistances(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['TRANSITIONDISTANCES', labels[0]])
        # with open("pickles/transitiondistances.pkl", "wb") as fp:
        #      pickle.dump(data, fp)
        #      fp.close()
        with open("pickles/transitiondistances.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testSentenceCohesions(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['SENTENCECOHESIONS', labels[0]])
        # with open("pickles/sentencecohesions.pkl", "wb") as fp:
        #      pickle.dump(data, fp)
        #      fp.close()
        with open("pickles/sentencecohesions.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testSliderCohesions(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['SLIDERCOHESIONS', labels[0]])
        # with open("pickles/slidercohesions.pkl", "wb") as fp:
        #      pickle.dump(data, fp)
        #      fp.close()
        with open("pickles/slidercohesions.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testRhemeDepths(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['RHEMEDEPTHS', labels[0]])
        # with open("pickles/rhemedepths.pkl", "wb") as fp:
        #      pickle.dump(data, fp)
        #      fp.close()
        with open("pickles/rhemedepths.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testThemeDepths(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['THEMEDEPTHS', labels[0]])
        # with open("pickles/themedepths.pkl", "wb") as fp:
        #      pickle.dump(data, fp)
        #      fp.close()
        with open("pickles/themedepths.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testWeightedDepths(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['WEIGHTEDDEPTHS', labels[0]])
        # with open("pickles/weighteddepths.pkl", "wb") as fp:
        #      pickle.dump(data, fp)
        #      fp.close()
        with open("pickles/weighteddepths.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testWeightedBreadths(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['WEIGHTEDBREADTHS', labels[0]])
        # with open("pickles/weightedbreadths.pkl", "wb") as fp:
        #      pickle.dump(data, fp)
        #      fp.close()
        with open("pickles/weightedbreadths.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testSyntacticProfile(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['SYNTACTICPROFILE', labels[0]])
        # with open("pickles/syntacticprofile.pkl", "wb") as fp:
        #      pickle.dump(data, fp)
        #      fp.close()
        with open("pickles/syntacticprofile.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testNormedSyntacticProfile(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['NORMEDSYNTACTICPROFILE', labels[0]])
        # with open("pickles/normedsyntacticprofile.pkl", "wb") as fp:
        #      pickle.dump(data, fp)
        #      fp.close()
        with open("pickles/normedsyntacticprofile.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testDirectSpeechSpans(self):
        ok = self.parser.send(['PARSEONE', labels[2], texts[2]])
        self.assertEqual(ok, True)
        data = self.parser.send(['DIRECTSPEECHSPANS', labels[2]])
        # with open("pickles/directspeechspans.pkl", "wb") as fp:
        #      pickle.dump(data, fp)
        #      fp.close()
        with open("pickles/directspeechspans.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        print('data',data)
        print('comparison', comparison)
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testInteractiveLanguage(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['INTERACTIVELANGUAGE', labels[0]])
        # with open("pickles/interactivelanguage.pkl", "wb") as fp:
        #      pickle.dump(data, fp)
        #      fp.close()
        with open("pickles/interactivelanguage.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testSubjectivityRatingsLanguage(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['SUBJECTIVITYRATINGS', labels[0]])
        # with open("pickles/subjectivityratings.pkl", "wb") as fp:
        #      pickle.dump(data, fp)
        #      fp.close()
        with open("pickles/subjectivityratings.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testPolarityRatings(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['POLARITYRATINGS', labels[0]])
        # with open("pickles/polarityratings.pkl", "wb") as fp:
        #      pickle.dump(data, fp)
        #      fp.close()
        with open("pickles/polarityratings.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testAssessments(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['ASSESSMENTS', labels[0]])
        # with open("pickles/assessments.pkl", "wb") as fp:
        #      pickle.dump(data, fp)
        #      fp.close()
        with open("pickles/assessments.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testSentimentRatings(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['SENTIMENTRATINGS', labels[0]])
        # with open("pickles/sentimentratings.pkl", "wb") as fp:
        #      pickle.dump(data, fp)
        #      fp.close()
        with open("pickles/sentimentratings.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testPerspectiveSpans(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['PERSPECTIVESPANS', labels[0]])
        # with open("pickles/perspectivespans.pkl", "wb") as fp:
        #      pickle.dump(data, fp)
        #      fp.close()
        with open("pickles/perspectivespans.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testStanceMarkers(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['STANCEMARKERS', labels[0]])
        # with open("pickles/stancemarkers.pkl", "wb") as fp:
        #      pickle.dump(data, fp)
        #      fp.close()
        with open("pickles/stancemarkers.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testEmotionalStates(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['EMOTIONALSTATES', labels[0]])
        # with open("pickles/emotionalstates.pkl", "wb") as fp:
        #      pickle.dump(data, fp)
        #      fp.close()
        with open("pickles/emotionalstates.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testCharacterTraits(self):
        ok = self.parser.send(['PARSEONE', labels[2], texts[2]])
        self.assertEqual(ok, True)
        data = self.parser.send(['CHARACTERTRAITS', labels[2]])
        # with open("pickles/charactertraits.pkl", "wb") as fp:
        #      pickle.dump(data, fp)
        #      fp.close()
        with open("pickles/charactertraits.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testPropositionalAttitudes(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['PROPOSITIONALATTITUDES', labels[0]])
        # with open("pickles/propositionalattitudes.pkl", "wb") as fp:
        #      pickle.dump(data, fp)
        #      fp.close()
        with open("pickles/propositionalattitudes.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testGoverningSubjects(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['GOVERNINGSUBJECTS', labels[0]])
        # with open("pickles/governingsubjects.pkl", "wb") as fp:
        #      pickle.dump(data, fp)
        #      fp.close()
        with open("pickles/governingsubjects.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testDevWords(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['DEVWORDS', labels[0]])
        # with open("pickles/devwords.pkl", "wb") as fp:
        #      pickle.dump(data, fp)
        #      fp.close()
        with open("pickles/devwords.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testClusterInfo(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['CLUSTERINFO', labels[0]])
        # with open("pickles/clusterinfo.pkl", "wb") as fp:
        #      pickle.dump(data, fp)
        #      fp.close()
        with open("pickles/clusterinfo.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testDocSummaryLabels(self):
        data = self.parser.send(['DOCSUMMARYLABELS'])
        # with open("pickles/docsummarylabels.pkl", "wb") as fp:
        #      pickle.dump(data, fp)
        #      fp.close()
        with open("pickles/docsummarylabels.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)

    def testDocSummaryFeats(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['DOCSUMMARYFEATS', labels[0]])
        #with open("pickles/docsummaryfeats2.pkl", "wb") as fp:
        #    pickle.dump(data, fp)
        #    fp.close()
        with open("pickles/docsummaryfeats.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testTokVecs(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        data = self.parser.send(['TOKVECS',  labels[0]])
        # with open("pickles/tokvecs.pkl", "wb") as fp:
        #     pickle.dump(data, fp)
        #     fp.close()
        with open("pickles/tokvecs.pkl", "rb") as fp:
            comparison = pickle.load(fp)
            fp.close()
        self.assertEqual(data, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

#    Serialization seems not to return exactly the same
#    binary result every run. Not sure why. Comment out
#    for now.
#    def testSerialized(self):
#        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
#        self.assertEqual(ok, True)
#        data = self.parser.sendraw(['SERIALIZED', labels[0]])
#        fp = open("pickles/serialized.dat", "wb")
#        fp.write(data)
#        fp.close()
#        fp = open("pickles/serialized.dat", "rb")
#        comparison = fp.read()
#        fp.close()
#        self.assertEqual(data, comparison)
#        ok = self.parser.send(['CLEARPARSED'])
#        self.assertEqual(ok, True)

    def testIndirectSpeech(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        locations = self.parser.send(['IN_DIRECT_SPEECH', labels[0]])
        # fp = open("pickles/in_direct_speech.dat", "wb")
        # pickle.dump(locations, fp)
        # fp.close()
        fp = open("pickles/in_direct_speech.dat", "rb")
        comparison = pickle.load(fp)
        fp.close()
        self.assertEqual(locations, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testTenseChanges(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        locations = self.parser.send(['TENSECHANGES', labels[0]])
        # fp = open("pickles/tenseChanges.dat", "wb")
        # pickle.dump(locations, fp)
        # fp.close()
        fp = open("pickles/tenseChanges.dat", "rb")
        comparison = pickle.load(fp)
        fp.close()
        self.assertEqual(locations, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testSocialAwareness(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        locations = self.parser.send(['SOCIAL_AWARENESS', labels[0]])
        # fp = open("pickles/socialAwareness.dat", "wb")
        # pickle.dump(locations, fp)
        # fp.close()
        fp = open("pickles/socialAwareness.dat", "rb")
        comparison = pickle.load(fp)
        fp.close()
        self.assertEqual(locations, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testConcreteDetails(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        locations = self.parser.send(['CONCRETEDETAILS', labels[0]])
        # fp = open("pickles/concreteDetails.dat", "wb")
        # pickle.dump(locations, fp)
        # fp.close()
        fp = open("pickles/concreteDetails.dat", "rb")
        comparison = pickle.load(fp)
        fp.close()
        self.assertEqual(locations, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testLocations(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        locations = self.parser.send(['LOCATIONS', labels[0]])
        # fp = open("pickles/locations.dat", "wb")
        # pickle.dump(locations, fp)
        # fp.close()
        fp = open("pickles/locations.dat", "rb")
        comparison = pickle.load(fp)
        fp.close()
        self.assertEqual(locations, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testPromptLanguage(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        promptlanguage = self.parser.send(['PROMPTLANGUAGE', labels[0]])
        # fp = open("pickles/promptlanguage.dat", "wb")
        # pickle.dump(promptlanguage, fp)
        # fp.close()
        fp = open("pickles/promptlanguage.dat", "rb")
        comparison = pickle.load(fp)
        fp.close()
        self.assertEqual(promptlanguage, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testContentSegments(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        contentsegments = self.parser.send(['CONTENTSEGMENTS', labels[0]])
        # fp = open("pickles/contentsegments.dat", "wb")
        # pickle.dump(contentsegments, fp)
        # fp.close()
        fp = open("pickles/contentsegments.dat", "rb")
        comparison = pickle.load(fp)
        fp.close()
        self.assertEqual(contentsegments, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testPromptRelated(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        locations = self.parser.send(['PROMPTRELATED', labels[0]])
        # fp = open("pickles/promptrelated.dat", "wb")
        # pickle.dump(locations, fp)
        # fp.close()
        fp = open("pickles/promptrelated.dat", "rb")
        comparison = pickle.load(fp)
        fp.close()
        self.assertEqual(locations, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testCoreSentences(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        locations = self.parser.send(['CORESENTENCES', labels[0]])
        # fp = open("pickles/coresentences.dat", "wb")
        # pickle.dump(locations, fp)
        # fp.close()
        fp = open("pickles/coresentences.dat", "rb")
        comparison = pickle.load(fp)
        fp.close()
        self.assertEqual(locations, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testClaimTexts(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        locations = self.parser.send(['CLAIMTEXTS', labels[0]])
        # fp = open("pickles/claimtexts.dat", "wb")
        # pickle.dump(locations, fp)
        # fp.close()
        fp = open("pickles/claimtexts.dat", "rb")
        comparison = pickle.load(fp)
        fp.close()
        self.assertEqual(locations, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

    def testDiscussionTexts(self):
        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
        self.assertEqual(ok, True)
        locations = self.parser.send(['DISCUSSIONTEXTS', labels[0]])
        # fp = open("pickles/discussiontexts.dat", "wb")
        # pickle.dump(locations, fp)
        # fp.close()
        fp = open("pickles/discussiontexts.dat", "rb")
        comparison = pickle.load(fp)
        fp.close()
        self.assertEqual(locations, comparison)
        ok = self.parser.send(['CLEARPARSED'])
        self.assertEqual(ok, True)

#    For some reason this test returns an error due to the AWE_Info extension
#    not being registered. This probably is due to parserServer somehow not
#    getting all the global information about extensions handled properly,
#    or at least that's what internet search suggests, but the code is exactly
#    the same here as in all the other tests and I can't find out what's triggering
#    the error. The code works when called normally rather than from pytest ...
#    def testTokFreqs(self):
#        ok = self.parser.send(['PARSEONE', labels[0], texts[0]])
#        self.assertEqual(ok, True)
#        data = self.parser.send(['TOKFREQS', labels[0]])
#        print(data, file=sys.stderr)
#        # with open("pickles/tokfreqs.pkl", "wb") as fp:
#        #     pickle.dump(data, fp)
#        #     fp.close()
#        with open("pickles/tokfreqs.pkl", "rb") as fp:
#            comparison = pickle.load(fp)
#            fp.close()
#        self.assertEqual(data, comparison)
#        ok = self.parser.send(['CLEARPARSED'])
#        self.assertEqual(ok, True)
