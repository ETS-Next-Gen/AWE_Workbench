#!/usr/bin/env python3.10
# Copyright 2022, Educational Testing Service

import holmes_extractor.manager as holmes
from awe_components.components.utility_functions import print_parse_tree
import unittest
import json

import tensorflow as tf
from awe_workbench.pipeline import pipeline_def

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        # Currently, memory growth needs to be the same across GPUs
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        # Memory growth must be set before GPUs have been initialized
        print(e)

holmes_manager = holmes.Manager(
    'en_core_web_lg', perform_coreference_resolution=False, number_of_workers=2, extra_components=pipeline_def)

# GRE Sample from https://www.ets.org/gre/revised_general/prepare/analytical_writing/issue/sample_responses
holmes_manager.parse_and_register_document(
            document_text="The statement linking technology negatively with free thinking plays on recent human experience over the past century. Surely there has been no time in history where the lived lives of people have changed more dramatically. A quick reflection on a typical day reveals how technology has revolutionized the world. Most people commute to work in an automobile that runs on an internal combustion engine. During the workday, chances are high that the employee will interact with a computer that processes information on silicon bridges that are .09 microns wide. Upon leaving home, family members will be reached through wireless networks that utilize satellites orbiting the earth. Each of these common occurrences could have been inconceivable at the turn of the 19th century.\n\nThe statement attempts to bridge these dramatic changes to a reduction in the ability for humans to think for themselves. The assumption is that an increased reliance on technology negates the need for people to think creatively to solve previous quandaries. Looking back at the introduction, one could argue that without a car, computer, or mobile phone, the hypothetical worker would need to find alternate methods of transport, information processing and communication. Technology short circuits this thinking by making the problems obsolete.\n\nHowever, this reliance on technology does not necessarily preclude the creativity that marks the human species. The prior examples reveal that technology allows for convenience. The car, computer and phone all release additional time for people to live more efficiently. This efficiency does not preclude the need for humans to think for themselves. In fact, technology frees humanity to not only tackle new problems, but may itself create new issues that did not exist without technology. For example, the proliferation of automobiles has introduced a need for fuel conservation on a global scale. With increasing energy demands from emerging markets, global warming becomes a concern inconceivable to the horse-and-buggy generation. Likewise dependence on oil has created nation-states that are not dependent on taxation, allowing ruling parties to oppress minority groups such as women. Solutions to these complex problems require the unfettered imaginations of maverick scientists and politicians.\n\nIn contrast to the statement, we can even see how technology frees the human imagination. Consider how the digital revolution and the advent of the internet has allowed for an unprecedented exchange of ideas. WebMD, a popular internet portal for medical information, permits patients to self research symptoms for a more informed doctor visit. This exercise opens pathways of thinking that were previously closed off to the medical layman. With increased interdisciplinary interactions, inspiration can arrive from the most surprising corners. Jeffrey Sachs, one of the architects of the UN Millenium Development Goals, based his ideas on emergency care triage techniques. The unlikely marriage of economics and medicine has healed tense, hyperinflation environments from South America to Eastern Europe.\n\nThis last example provides the most hope in how technology actually provides hope to the future of humanity. By increasing our reliance on technology, impossible goals can now be achieved. Consider how the late 20th century witnessed the complete elimination of smallpox. This disease had ravaged the human race since prehistorical days, and yet with the technology of vaccines, free thinking humans dared to imagine a world free of smallpox. Using technology, battle plans were drawn out, and smallpox was systematically targeted and eradicated.\n\nTechnology will always mark the human experience, from the discovery of fire to the implementation of nanotechnology. Given the history of the human race, there will be no limit to the number of problems, both new and old, for us to tackle. There is no need to retreat to a Luddite attitude to new things, but rather embrace a hopeful posture to the possibilities that technology provides for new avenues of human imagination.", label='GRE_Sample_Essay')


class SyntaxDiscourseFeatureTest(unittest.TestCase):

    def test_paragraph_breaks(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        paragraph_breaks = [131, 223, 393, 527, 622, 703]
        self.assertEqual(doc._.paragraph_breaks,
                         paragraph_breaks)

    def test_paragraph_lengths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        paragraph_lengths = [131, 92, 170, 134, 95, 81]
        self.assertEqual(doc._.paragraph_lengths,
                         paragraph_lengths)

    def test_mean_paragraph_length(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_paragraph_length,
                         117.16666666666667)

    def test_median_paragraph_length(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.median_paragraph_length, 113.0)

    def test_max_paragraph_length(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.max_paragraph_length, 170)

    def test_min_paragraph_length(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.min_paragraph_length, 81)

    def test_stdev_paragraph_length(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdev_paragraph_length,
                         33.760430486986785)

    def test_transition_word_profile(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        profile = [25, {'temporal': 6, 'PARAGRAPH': 5, 'contrastive': 5, 'illustrative': 6, 'emphatic': 2, 'comparative': 1}, {'over the past century': 1, 'no time in history': 1, 'During the workday': 1, 'Upon leaving home': 1, 'at the turn of the 19th century': 1, 'NEWLINE': 5, 'however': 1, 'the prior examples': 1, 'in fact': 1, 'not only': 1, 'but': 2, 'for example': 1, 'likewise': 1, 'such as': 1, 'in contrast': 1, 'consider how': 2, 'this last example': 1, 'since prehistorical days': 1, 'and yet': 1}, [['over the past century', 0, 13, 16, 'temporal'], ['no time in history', 18, 22, 25, 'temporal'], ['During the workday', 68, 68, 70, 'temporal'], ['Upon leaving home', 95, 95, 97, 'temporal'], ['at the turn of the 19th century', 114, 123, 129, 'temporal'], ['NEWLINE', 131, 131, 131, 'PARAGRAPH'], ['NEWLINE', 223, 223, 223, 'PARAGRAPH'], ['however', 223, 224, 224, 'contrastive'], ['the prior examples', 242, 242, 245, 'illustrative'], ['in fact', 283, 283, 284, 'emphatic'], ['not only', 283, 290, 291, 'emphatic'], ['but', 283, 296, 296, 'contrastive'], ['for example', 309, 309, 310, 'illustrative'], ['likewise', 351, 351, 351, 'comparative'], ['such as', 351, 374, 375, 'illustrative'], ['NEWLINE', 393, 393, 393, 'PARAGRAPH'], ['in contrast', 393, 394, 395, 'contrastive'], ['consider how', 411, 411, 412, 'illustrative'], ['NEWLINE', 527, 527, 527, 'PARAGRAPH'], ['this last example', 527, 528, 531, 'illustrative'], ['consider how', 561, 561, 562, 'illustrative'], ['since prehistorical days', 574, 581, 583, 'temporal'], ['and yet', 574, 585, 586, 'contrastive'], ['NEWLINE', 622, 622, 622, 'PARAGRAPH'], ['but', 671, 685, 685, 'contrastive']]]
        self.assertEqual(doc._.transition_word_profile,
                         profile)

    def test_total_transition_words(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.total_transition_words, 25)

    def test_transition_category_count(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.transition_category_count, 6)

    def test_transition_word_type_count(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.transition_word_type_count, 19)

    def test_transition_words(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        transition_words = [['over the past century', 0, 13, 16, 'temporal'], ['no time in history', 18, 22, 25, 'temporal'], ['During the workday', 68, 68, 70, 'temporal'], ['Upon leaving home', 95, 95, 97, 'temporal'], ['at the turn of the 19th century', 114, 123, 129, 'temporal'], ['NEWLINE', 131, 131, 131, 'PARAGRAPH'], ['NEWLINE', 223, 223, 223, 'PARAGRAPH'], ['however', 223, 224, 224, 'contrastive'], ['the prior examples', 242, 242, 245, 'illustrative'], ['in fact', 283, 283, 284, 'emphatic'], ['not only', 283, 290, 291, 'emphatic'], ['but', 283, 296, 296, 'contrastive'], ['for example', 309, 309, 310, 'illustrative'], ['likewise', 351, 351, 351, 'comparative'], ['such as', 351, 374, 375, 'illustrative'], ['NEWLINE', 393, 393, 393, 'PARAGRAPH'], ['in contrast', 393, 394, 395, 'contrastive'], ['consider how', 411, 411, 412, 'illustrative'], ['NEWLINE', 527, 527, 527, 'PARAGRAPH'], ['this last example', 527, 528, 531, 'illustrative'], ['consider how', 561, 561, 562, 'illustrative'], ['since prehistorical days', 574, 581, 583, 'temporal'], ['and yet', 574, 585, 586, 'contrastive'], ['NEWLINE', 622, 622, 622, 'PARAGRAPH'], ['but', 671, 685, 685, 'contrastive']]
        self.assertEqual(doc._.transition_words,
                         transition_words)

    def test_transition_distances(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        transition_distances = [0.2754433751106262, 0.18068242073059082, 0.3455371856689453, 0.5115512013435364, 0.29295045137405396, 0.26799535751342773, 0.2427629828453064, 0.2613025903701782, 0.3560638427734375, 0.36619603633880615, 0.3768072724342346, 0.171677827835083, 0.21559733152389526, 0.42869412899017334, 0.4524803161621094, 0.4260185956954956, 0.46465003490448, 0.26872915029525757, 0.580579549074173, 0.5725382268428802, 0.41816604137420654, 0.3364747166633606, 0.3091871738433838, 0.6479913592338562, 0.19418299198150635]
        self.assertEqual(doc._.transition_distances,
                         transition_distances)

    def test_mean_transition_distance(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_transition_distance,
                         0.3585704064369202)

    def test_median_transition_distance(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.median_transition_distance,
                         0.3455371856689453)

    def test_max_transition_distance(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.max_transition_distance,
                         0.6479913592338562)

    def test_min_transition_distance(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.min_transition_distance,
                         0.171677827835083)

    def test_stdev_transition_distance(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdev_transition_distance,
                         0.1296185349128186)

    def test_intersentence_cohesions(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        intersentence_cohesions = [0.8988593220710754, 0.8736750483512878, 0.8477486968040466, 0.8780263066291809, 0.8904399871826172, 0.8478362560272217, 0.8970850110054016, 0.9370104074478149, 0.8875330090522766, 0.8721916675567627, 0.8623306155204773, 0.8789313435554504, 0.87635737657547, 0.8838761448860168, 0.9297630190849304, 0.8696791529655457, 0.8978860974311829, 0.8615327477455139, 0.855689525604248, 0.8783911466598511, 0.900669276714325, 0.8269333839416504, 0.8536540865898132, 0.8761308789253235, 0.8271347880363464, 0.8295413255691528, 0.8300540447235107, 0.8762711882591248, 0.7860766053199768, 0.8845039010047913, 0.8930788040161133, 0.8380871415138245, 0.9311631321907043, 0.9270924925804138]
        self.assertEqual(doc._.intersentence_cohesions,
                         intersentence_cohesions)

    def test_mean_sent_cohesion(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_sent_cohesion,
                         0.8736833509276895)

    def test_median_sent_cohesion(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.median_sent_cohesion,
                         0.8763142824172974)

    def test_max_sent_cohesion(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.max_sent_cohesion,
                         0.9370104074478149)

    def test_min_sent_cohesion(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.min_sent_cohesion,
                         0.7860766053199768)

    def test_stdev_sent_cohesion(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdev_sent_cohesion,
                         0.033244800492783624)

    def test_sliding_window_cohesions(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        sliding_window_cohesions = [0.7181742191314697, 0.701263427734375, 0.6790735125541687, 0.6474848985671997, 0.6590394377708435, 0.7189511656761169, 0.6720224618911743, 0.7850678563117981, 0.8007805347442627, 0.7889644503593445, 0.7991914749145508, 0.8140134215354919, 0.8126447200775146, 0.7754191160202026, 0.7475166320800781, 0.7887311577796936, 0.6866664290428162, 0.7194632887840271, 0.7194632887840271, 0.6448104977607727, 0.6458194255828857, 0.6696494221687317, 0.5748744010925293, 0.5917541980743408, 0.4936998188495636, 0.6006785035133362, 0.5567438006401062, 0.5973606705665588, 0.6129812002182007, 0.659326434135437, 0.688444972038269, 0.7055871486663818, 0.6687339544296265, 0.6260309815406799, 0.5268124938011169, 0.5692242980003357, 0.5738590955734253, 0.5684884190559387, 0.6827142238616943, 0.6544976234436035, 0.6336449980735779, 0.5551523566246033, 0.571733832359314, 0.5404956936836243, 0.3755459487438202, 0.5269684791564941, 0.5898616313934326, 0.41509121656417847, 0.44168174266815186, 0.4371638000011444, 0.3960413932800293, 0.4594825208187103, 0.4970448911190033, 0.5166383981704712, 0.5925062298774719, 0.5895653367042542, 0.6845969557762146, 0.46040961146354675, 0.42461514472961426, 0.44434645771980286, 0.4096076488494873, 0.44259214401245117, 0.4406617283821106, 0.44507601857185364, 0.5546365976333618, 0.43519437313079834, 0.5321240425109863, 0.4746674597263336, 0.4140016734600067, 0.4774576425552368, 0.4703843891620636, 0.5924128293991089, 0.5924128293991089, 0.5004821419715881, 0.4637318253517151, 0.33062052726745605, 0.27226918935775757, 0.2537829577922821, 0.2854864001274109, 0.3904673755168915, 0.4211515188217163, 0.45139551162719727, 0.5127795934677124, 0.38112887740135193, 0.24094435572624207, 0.2918039858341217, 0.1845623105764389, 0.22997146844863892, 0.36806720495224, 0.4143584966659546, 0.3875931203365326, 0.38407766819000244, 0.4325980246067047, 0.4053116738796234, 0.3240915536880493, 0.3403795063495636, 0.3285251259803772, 0.3186679482460022, 0.38233309984207153, 0.40397265553474426, 0.4056640863418579, 0.423939049243927, 0.4444441497325897, 0.3398769795894623, 0.36920079588890076, 0.36920079588890076, 0.3883742094039917, 0.42753884196281433, 0.41213420033454895, 0.37709927558898926, 0.39389845728874207, 0.4492016136646271, 0.4492016136646271, 0.2987273335456848, 0.29447853565216064, 0.3743438422679901, 0.4030083119869232, 0.4750116765499115, 0.42504170536994934, 0.48562872409820557, 0.5353590846061707, 0.5397853255271912, 0.5397853255271912, 0.5133278369903564, 0.4792203903198242, 0.5079424977302551, 0.4732956290245056, 0.4496147334575653, 0.47529879212379456, 0.4816325306892395, 0.4889850616455078, 0.6232978701591492, 0.6232978701591492, 0.5230883359909058, 0.5245723128318787, 0.47190043330192566, 0.45224520564079285, 0.52435302734375, 0.5436772704124451, 0.7187649011611938, 0.8517671227455139, 0.804987907409668, 0.6629474759101868, 0.5680908560752869, 0.5643051862716675, 0.5234549045562744, 0.5782879590988159, 0.5782879590988159, 0.692085325717926, 0.7090957760810852, 0.6492884159088135, 0.62215256690979, 0.5129061937332153, 0.5064864754676819, 0.5264977812767029, 0.45184406638145447, 0.5640366077423096, 0.5242792367935181, 0.5922706127166748, 0.5628295540809631, 0.5925487875938416, 0.6522911190986633, 0.5478234887123108, 0.5763028264045715, 0.618124783039093, 0.6638599634170532, 0.5731121897697449, 0.5437830686569214, 0.5437830686569214, 0.4712313711643219, 0.4569089710712433, 0.5454812049865723, 0.48367583751678467, 0.42092519998550415, 0.48569998145103455, 0.42305129766464233, 0.2977829873561859, 0.2977829873561859, 0.3928380012512207, 0.5374341607093811, 0.5031077861785889, 0.680233359336853, 0.680233359336853, 0.7139794230461121, 0.495082288980484, 0.4879363477230072, 0.4879363477230072, 0.5396188497543335, 0.5411055088043213, 0.5838121771812439, 0.5381329655647278, 0.6154993176460266, 0.6020007133483887, 0.5532087087631226, 0.5166041851043701, 0.6518845558166504, 0.6322896480560303, 0.6936717629432678, 0.7012785077095032, 0.6895168423652649, 0.7263908982276917, 0.6917502284049988, 0.702608048915863, 0.6224715709686279, 0.6139522194862366, 0.5929139256477356, 0.6004048585891724, 0.6113495230674744, 0.6583157777786255, 0.563602089881897, 0.5703687071800232, 0.624764621257782, 0.6356892585754395, 0.5418727993965149, 0.660626232624054, 0.6365984678268433, 0.6365984678268433, 0.6277673840522766, 0.6215293407440186, 0.6219359636306763, 0.5721964836120605, 0.5492886304855347, 0.5228410959243774, 0.5004310011863708, 0.5531101822853088, 0.5986908078193665, 0.5671816468238831, 0.5866214036941528, 0.5946487188339233, 0.721796989440918, 0.6296963095664978, 0.6760013103485107, 0.6499212980270386, 0.6191558241844177, 0.5661692023277283, 0.5312169790267944, 0.42728954553604126, 0.4562321603298187, 0.4211899936199188, 0.43973419070243835, 0.4918561577796936, 0.588962733745575, 0.6923847794532776, 0.7171835899353027, 0.6751047372817993, 0.7206659913063049, 0.6406289935112, 0.6438475251197815, 0.5796738266944885, 0.5699208974838257, 0.5898752808570862, 0.5684922337532043, 0.5515444278717041, 0.5951597690582275, 0.5218393206596375, 0.55599445104599, 0.4096278250217438, 0.5285232663154602, 0.5646203756332397, 0.6959474682807922, 0.7203365564346313, 0.7185603380203247, 0.6625391840934753, 0.6423453092575073, 0.4971276819705963, 0.5273186564445496, 0.3788944184780121, 0.48065927624702454, 0.6103437542915344, 0.7828500866889954, 0.7766262292861938, 0.7812368273735046, 0.6906050443649292, 0.696194589138031, 0.6632706522941589, 0.5880956053733826, 0.6033019423484802, 0.600532054901123, 0.6870222687721252, 0.5664738416671753, 0.6295509338378906, 0.6456001400947571, 0.6606005430221558, 0.6630827784538269, 0.6997432708740234, 0.7766095399856567, 0.822784423828125, 0.7297685742378235, 0.7680246829986572, 0.7385520935058594, 0.8694490194320679, 0.8062267899513245, 0.7353216409683228, 0.7639004588127136, 0.7887110114097595, 0.7451591491699219, 0.7286704182624817, 0.7197006344795227, 0.5714356899261475, 0.6237432956695557, 0.6275636553764343, 0.6628205180168152, 0.6909197568893433, 0.6639208197593689, 0.6479867696762085, 0.6235129833221436, 0.5890401601791382, 0.6758988499641418, 0.5882089138031006, 0.5884600877761841, 0.5746558904647827, 0.6486964821815491, 0.6165353655815125, 0.7018287181854248, 0.7054082751274109, 0.6990912556648254, 0.7131054401397705, 0.7826208472251892, 0.8002692461013794, 0.8187614679336548, 0.7922825217247009, 0.7839767336845398, 0.8015739917755127, 0.8150758743286133, 0.8106814026832581, 0.7866733074188232, 0.7180758714675903, 0.5957860350608826, 0.5097404718399048, 0.518147885799408, 0.42179739475250244, 0.3904438316822052, 0.34155407547950745, 0.4236290752887726, 0.5133522152900696, 0.5123850703239441, 0.6250080466270447, 0.5969473719596863, 0.5544553399085999, 0.5544728636741638, 0.49274978041648865, 0.4804668128490448, 0.393265962600708, 0.47033119201660156, 0.5464437007904053, 0.6502533555030823, 0.650912344455719, 0.6295266151428223, 0.6125736832618713, 0.7110123634338379, 0.6587409377098083, 0.6810725927352905, 0.6525141596794128, 0.5871813893318176, 0.5741062760353088, 0.6681912541389465, 0.6420008540153503, 0.6505707502365112, 0.5556239485740662, 0.5587475299835205, 0.5747273564338684, 0.6126003265380859, 0.6067212820053101, 0.5422795414924622, 0.4704667627811432, 0.5488695502281189, 0.536759078502655, 0.5157687664031982, 0.47764521837234497, 0.47986119985580444, 0.5271527767181396, 0.5498452186584473, 0.5290605425834656, 0.46688687801361084, 0.3602869212627411, 0.37699976563453674, 0.3809293508529663, 0.45073172450065613, 0.49928227066993713, 0.5415453314781189, 0.5122532844543457, 0.5543336272239685, 0.36085236072540283, 0.3665997087955475, 0.3116161823272705, 0.3116161823272705, 0.22969196736812592, 0.49183592200279236, 0.4778640866279602, 0.3747110962867737, 0.39294037222862244, 0.4299679398536682, 0.37511005997657776, 0.45231547951698303, 0.45231547951698303, 0.45231547951698303, 0.311810165643692, 0.6087309122085571, 0.6377063393592834, 0.5729437470436096, 0.5713992118835449, 0.5866880416870117, 0.5389125347137451, 0.5725162625312805, 0.5725162625312805, 0.6103866696357727, 0.5800052285194397, 0.6384758353233337, 0.6805055737495422, 0.6303063631057739, 0.632068932056427, 0.6773736476898193, 0.5216607451438904, 0.5345773100852966, 0.5092067718505859, 0.549133837223053, 0.5851325392723083, 0.6893542408943176, 0.6067965626716614, 0.5960580110549927, 0.6024318933486938, 0.6473482251167297, 0.5909489393234253, 0.622308611869812, 0.5430110096931458, 0.5262013673782349, 0.5152072906494141, 0.5069680213928223, 0.47498154640197754, 0.47355157136917114, 0.5156494379043579, 0.5657385587692261, 0.6107592582702637, 0.6410508751869202, 0.7491336464881897, 0.7429540157318115, 0.708656907081604, 0.7128888368606567, 0.7051429748535156, 0.7304097414016724, 0.7082116007804871, 0.7053606510162354, 0.6371103525161743, 0.6145652532577515, 0.6448284387588501, 0.5823889970779419, 0.47524186968803406, 0.4950029253959656, 0.5897514820098877, 0.733385443687439, 0.6809965372085571, 0.6470853686332703, 0.5646995306015015, 0.5743997693061829, 0.567176878452301, 0.5640305876731873, 0.5190287232398987, 0.5860862731933594, 0.45603713393211365, 0.601533830165863, 0.5251269936561584, 0.5251269936561584, 0.4691050052642822, 0.4861484169960022, 0.3381423354148865, 0.3549068570137024, 0.33667048811912537, 0.34557345509529114, 0.3017862141132355, 0.26958876848220825, 0.26958876848220825, 0.26958876848220825, 0.22090551257133484, 0.10331247001886368, 0.09946548193693161, 0.1849459409713745, 0.30455225706100464, 0.32518064975738525, 0.28176671266555786, 0.28176671266555786, 0.25893980264663696, 0.43409574031829834, 0.4541017711162567, 0.43791645765304565, 0.43601515889167786, 0.393983393907547, 0.31059807538986206, 0.4658436179161072, 0.5241922736167908, 0.4947414696216583, 0.5775105357170105, 0.4995882511138916, 0.5370966196060181, 0.6021908521652222, 0.6589798331260681, 0.6821597814559937, 0.5967273116111755, 0.582856297492981, 0.5628841519355774, 0.5423623919487, 0.5445433855056763, 0.6205247640609741, 0.6047906279563904, 0.628349781036377, 0.5308804512023926, 0.5292799472808838, 0.49483180046081543, 0.4438880383968353, 0.44538453221321106, 0.39144372940063477, 0.32624340057373047, 0.33729884028434753, 0.36647048592567444, 0.5381368398666382, 0.5796362161636353, 0.4877815842628479, 0.4056786298751831, 0.3741012513637543, 0.3741012513637543, 0.41936007142066956, 0.3283812701702118, 0.2851704955101013, 0.43395164608955383, 0.5865570902824402, 0.5865570902824402, 0.6814536452293396, 0.8771107196807861, 0.8514654636383057, 0.8616060018539429, 0.8265013098716736, 0.7317827343940735, 0.6125732660293579, 0.6415880918502808, 0.6415880918502808, 0.6773134469985962, 0.7344356179237366, 0.7574276328086853, 0.7808356285095215, 0.7187724113464355, 0.6987088322639465, 0.7151852250099182, 0.6983718276023865, 0.6730572581291199, 0.6597504019737244, 0.606074333190918, 0.5605922937393188, 0.6138680577278137, 0.5882761478424072, 0.566649317741394, 0.5377964377403259, 0.4628887176513672, 0.5489749312400818, 0.5501205325126648, 0.572618842124939, 0.5328660607337952, 0.48593321442604065, 0.610148012638092, 0.5011742115020752, 0.42126917839050293, 0.43704622983932495, 0.35713109374046326, 0.39734765887260437, 0.5136548280715942, 0.5295951962471008, 0.5775947570800781, 0.6341943144798279, 0.6095657348632812, 0.5941829681396484, 0.4871390759944916, 0.4948325455188751, 0.33891695737838745, 0.3814352750778198, 0.40467697381973267, 0.5137110352516174, 0.4322446584701538, 0.4563347399234772, 0.4418659508228302, 0.5515823364257812, 0.5925307869911194, 0.5925307869911194, 0.41388991475105286, 0.42125800251960754, 0.44196179509162903, 0.5017839074134827, 0.4229195713996887, 0.6369653940200806, 0.7045741677284241, 0.7806202173233032, 0.8586754202842712, 0.8089002966880798, 0.701143205165863, 0.6780319809913635, 0.560285747051239, 0.6080725193023682, 0.6440467834472656, 0.6091873645782471, 0.6041891574859619, 0.7203472852706909, 0.6859999299049377, 0.6288899779319763, 0.5956356525421143, 0.6310295462608337, 0.6070647239685059, 0.6026177406311035, 0.37063199281692505, 0.5363000631332397, 0.5828129053115845, 0.5072140693664551, 0.5353472828865051, 0.5218008160591125, 0.5945451855659485, 0.4543611705303192, 0.3569714426994324, 0.3569714426994324, 0.352898508310318, 0.5161055326461792, 0.5477725267410278, 0.547351598739624, 0.5778474807739258, 0.49038827419281006, 0.5734430551528931, 0.6217519640922546, 0.656516969203949, 0.656516969203949, 0.5748251676559448, 0.6277108192443848, 0.6926324367523193, 0.6373811364173889, 0.6373811364173889, 0.6303789615631104, 0.5546615123748779, 0.5224807858467102, 0.5113321542739868, 0.4760902225971222, 0.492556631565094, 0.463143527507782, 0.5552494525909424, 0.5552494525909424, 0.4319190979003906, 0.4683215916156769, 0.48052531480789185, 0.5751261115074158, 0.5751261115074158, 0.4873209297657013, 0.5247870087623596, 0.45412883162498474, 0.5261881351470947, 0.5261881351470947, 0.4173544943332672, 0.4647064805030823, 0.36291688680648804, 0.4990863800048828, 0.4990863800048828, 0.44398272037506104, 0.5105710625648499, 0.34621956944465637, 0.5540810227394104, 0.5540810227394104, 0.5187355875968933, 0.5187355875968933, 0.4385828673839569, 0.39906346797943115, 0.4428623914718628, 0.4133220314979553, 0.49259528517723083, 0.3077422082424164, 0.48961880803108215, 0.4834340512752533, 0.515978991985321, 0.5658944249153137, 0.626227617263794, 0.5341516137123108, 0.6856047511100769, 0.6929025053977966, 0.6483656167984009, 0.6830957531929016, 0.6830957531929016, 0.6730726957321167, 0.5893316268920898, 0.6402474045753479, 0.6975016593933105, 0.6524498462677002, 0.6220090389251709, 0.5655167698860168]
        self.assertEqual(doc._.sliding_window_cohesions,
                         sliding_window_cohesions)

    def test_mean_slider_cohesion(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_slider_cohesion,
                         0.5531269748482788)

    def test_median_slider_cohesion(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.median_slider_cohesion,
                         0.5628568530082703)

    def test_max_slider_cohesion(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.max_slider_cohesion,
                         0.8771107196807861)

    def test_min_slider_cohesion(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.min_slider_cohesion,
                         0.09946548193693161)

    def test_stdev_slider_cohesion(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdev_slider_cohesion,
                         0.12972704854938172)

    def test_num_coref_chains(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.num_corefs, 4)

    def test_mean_coref_chain_len(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_coref_chain_len, 2)

    def test_median_coref_chain_len(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.median_coref_chain_len, 2.0)

    def test_max_coref_chain_len(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.max_coref_chain_len, 2)

    def test_min_coref_chain_len(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.min_coref_chain_len, 2)

    def test_stdev_coref_chain_len(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdev_coref_chain_len, 0.0)

    def test_sentence_count(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.sentence_count, 35)

    def test_sentence_lengths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.sentence_lengths,
                         [18, 19, 15, 16, 27, 19, 17, 22, 22, 37, 11, 19, 10, 17, 14, 26, 19, 23, 27, 15, 18, 20, 23, 16, 14, 23, 20, 20, 14, 13, 31, 17, 20, 29, 33])

    def test_mean_sentence_lengths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_sentence_len,
                         20.114285714285714)

    def test_median_sentence_lengths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.median_sentence_len, 19)

    def test_max_sentence_lengths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.max_sentence_len, 37)

    def test_min_sentence_lengths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.min_sentence_len, 10)

    def test_stdev_sentence_lengths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.std_sentence_len,
                         6.153771815969878)

    def test_sqrt_sentence_lengths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.sqrt_sentence_lengths,
                         [4.242640687119285, 4.358898943540674, 3.872983346207417, 4.0, 5.196152422706632, 4.358898943540674, 4.123105625617661, 4.69041575982343, 4.69041575982343, 6.082762530298219, 3.3166247903554, 4.358898943540674, 3.1622776601683795, 4.123105625617661, 3.7416573867739413, 5.0990195135927845, 4.358898943540674, 4.795831523312719, 5.196152422706632, 3.872983346207417, 4.242640687119285, 4.47213595499958, 4.795831523312719, 4.0, 3.7416573867739413, 4.795831523312719, 4.47213595499958, 4.47213595499958, 3.7416573867739413, 3.605551275463989, 5.5677643628300215, 4.123105625617661, 4.47213595499958, 5.385164807134504, 5.744562646538029])

    def test_mean_sqrt_sentence_lengths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_sqrt_sentence_len,
                         4.436401006267681)

    def test_median_sqrt_sentence_lengths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.median_sqrt_sentence_len,
                         4.358898943540674)

    def test_max_sqrt_sentence_lengths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.max_sqrt_sentence_len,
                         6.082762530298219)

    def test_min_sqrt_sentence_lengths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.min_sqrt_sentence_len,
                         3.1622776601683795)

    def test_stdev_sqrt_sentence_lengths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.std_sqrt_sentence_len,
                         0.6673502014232635)

    def test_words_to_sentence_root(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.words_before_sentence_root,
                         [8, 3, 7, 2, 5, 8, 7, 3, 2, 8, 2, 10, 3, 7, 4, 4, 8, 10, 5, 5, 10, 0, 10, 2, 7, 14, 8, 4, 12, 0, 3, 6, 4, 10, 1])

    def test_mean_words_to_sentence_root(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_words_to_sentence_root,
                         5.771428571428571)

    def test_median_words_to_sentence_root(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.median_words_to_sentence_root, 5)

    def test_max_words_to_sentence_root(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.max_words_to_sentence_root, 14)

    def test_min_words_to_sentence_root(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.min_words_to_sentence_root, 0)

    def test_stdev_words_to_sentence_root(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdev_words_to_sentence_root,
                         3.507015777533022)

    def test_syntacticThemeDepths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.syntacticThemeDepths,
                         [2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 3, 3, 2, 3, 3, 2, 3, 5, 4, 2, 2, 2, 2, 2, 0, 2, 3, 3, 3, 2, 2])

    def test_meanThemeDepth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.meanThemeDepth, 2.28125)

    def test_medianThemeDepth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.medianThemeDepth, 2.0)

    def test_maxThemeDepth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.maxThemeDepth, 5.0)

    def test_minThemeDepth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.minThemeDepth, 0.0)

    def test_stdevThemeDepth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdevThemeDepth,
                         0.9240295694193397)

    def test_syntacticRhemeDepths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.syntacticRhemeDepths,
                         [1.0, 2.0, 4.0, 4.0, 3.0, 2.0, 4.0, 4.0, 3.0, 2.0, 1.0, 3.0, 2.0, 3.0, 4.0, 4.0, 5.0, 5.0, 4.0, 5.0, 6.0, 4.0, 3.0, 5.0, 4.0, 2.0, 1.0, 3.0, 3.0, 3.0, 2.0, 4.0, 3.0, 2.0, 1.0, 2.0, 3.0, 4.0, 6.0, 5.0, 7.0, 6.0, 7.0, 9.0, 9.0, 9.0, 8.0, 2.0, 1.0, 2.0, 3.0, 4.0, 3.0, 3.0, 2.0, 3.0, 5.0, 4.0, 6.0, 5.0, 6.0, 7.0, 9.0, 8.0, 10.0, 9.0, 12.0, 11.0, 10.0, 2.0, 1.0, 2.0, 4.0, 3.0, 5.0, 4.0, 5.0, 6.0, 8.0, 7.0, 2.0, 1.0, 2.0, 2.0, 4.0, 3.0, 4.0, 6.0, 6.0, 5.0, 2.0, 1.0, 3.0, 2.0, 4.0, 4.0, 3.0, 3.0, 5.0, 4.0, 5.0, 7.0, 6.0, 8.0, 8.0, 8.0, 7.0, 8.0, 9.0, 2.0, 1.0, 3.0, 4.0, 4.0, 3.0, 4.0, 5.0, 2.0, 4.0, 3.0, 5.0, 5.0, 5.0, 4.0, 5.0, 6.0, 5.0, 7.0, 6.0, 2.0, 1.0, 3.0, 3.0, 5.0, 4.0, 5.0, 4.0, 5.0, 5.0, 5.0, 4.0, 3.0, 4.0, 4.0, 3.0, 3.0, 2.0, 4.0, 3.0, 5.0, 4.0, 5.0, 6.0, 7.0, 7.0, 6.0, 7.0, 6.0, 2.0, 1.0, 3.0, 2.0, 2.0, 3.0, 6.0, 5.0, 4.0, 2.0, 1.0, 3.0, 2.0, 4.0, 3.0, 5.0, 5.0, 4.0, 2.0, 1.0, 3.0, 3.0, 2.0, 3.0, 4.0, 2.0, 1.0, 3.0, 2.0, 3.0, 3.0, 3.0, 2.0, 4.0, 3.0, 2.0, 1.0, 3.0, 2.0, 4.0, 4.0, 4.0, 3.0, 4.0, 5.0, 2.0, 1.0, 2.0, 3.0, 3.0, 4.0, 2.0, 4.0, 3.0, 2.0, 2.0, 2.0, 2.0, 1.0, 3.0, 2.0, 4.0, 4.0, 4.0, 3.0, 4.0, 5.0, 2.0, 1.0, 3.0, 2.0, 3.0, 5.0, 4.0, 5.0, 7.0, 7.0, 6.0, 2.0, 1.0, 3.0, 2.0, 3.0, 4.0, 6.0, 6.0, 7.0, 7.0, 7.0, 6.0, 5.0, 2.0, 1.0, 3.0, 3.0, 2.0, 4.0, 3.0, 4.0, 4.0, 5.0, 6.0, 2.0, 2.0, 5.0, 4.0, 4.0, 3.0, 5.0, 4.0, 6.0, 5.0, 6.0, 2.0, 1.0, 3.0, 3.0, 2.0, 3.0, 5.0, 4.0, 5.0, 4.0, 2.0, 1.0, 3.0, 3.0, 2.0, 4.0, 4.0, 3.0, 2.0, 1.0, 3.0, 4.0, 4.0, 3.0, 4.0, 4.0, 3.0, 4.0, 6.0, 5.0, 3.0, 2.0, 3.0, 5.0, 5.0, 4.0, 5.0, 6.0, 2.0, 1.0, 2.0, 2.0, 4.0, 4.0, 3.0, 2.0, 4.0, 5.0, 4.0, 4.0, 3.0, 2.0, 1.0, 2.0, 3.0, 4.0, 4.0, 4.0, 4.0, 3.0, 4.0, 4.0, 6.0, 6.0, 5.0, 2.0, 1.0, 2.0, 4.0, 5.0, 4.0, 3.0, 2.0, 1.0, 3.0, 2.0, 3.0, 7.0, 6.0, 5.0, 4.0, 2.0, 1.0, 3.0, 3.0, 3.0, 2.0, 3.0, 5.0, 4.0, 2.0, 4.0, 3.0, 2.0, 1.0, 3.0, 3.0, 2.0, 3.0, 5.0, 5.0, 5.0, 4.0, 5.0, 5.0, 7.0, 6.0, 7.0, 8.0, 2.0, 1.0, 2.0, 1.0, 3.0, 4.0, 4.0, 4.0, 3.0, 2.0, 4.0, 4.0, 3.0, 4.0, 5.0, 2.0, 1.0, 3.0, 3.0, 2.0, 2.0, 4.0, 3.0, 2.0, 2.0, 3.0, 2.0, 4.0, 3.0, 4.0, 5.0, 2.0, 4.0, 3.0, 2.0, 1.0, 3.0, 2.0, 5.0, 4.0, 3.0, 4.0, 5.0, 2.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 2.0, 1.0, 2.0, 1.0, 3.0, 3.0, 2.0, 2.0, 2.0, 4.0, 3.0, 4.0, 5.0, 4.0, 6.0, 5.0, 6.0, 7.0, 2.0, 1.0, 3.0, 2.0, 3.0, 5.0, 4.0, 5.0, 6.0, 5.0, 6.0, 5.0, 6.0, 5.0, 2.0, 3.0, 3.0, 3.0, 2.0, 2.0, 1.0, 3.0, 2.0, 4.0, 3.0, 4.0, 6.0, 6.0, 5.0, 4.0, 6.0, 5.0, 2.0, 2.0, 3.0, 1.0, 3.0, 3.0, 2.0, 2.0, 4.0, 3.0, 5.0, 5.0, 4.0, 5.0, 7.0, 6.0, 7.0, 9.0, 8.0, 2.0])

    def test_meanRhemeDepth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.meanRhemeDepth,
                         3.733067729083665)

    def test_medianRhemeDepth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.medianRhemeDepth, 3.0)

    def test_maxRhemeDepth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.maxRhemeDepth, 12.0)

    def test_minRhemeDepth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.minRhemeDepth, 1.0)

    def test_stdevThemeDepth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdevRhemeDepth,
                         1.8765445139321595)

    def test_weightedSyntacticDepths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.weightedSyntacticDepths,
                         [5.0, 3.0, 5.0, 6.0, 8.0, 6.0, 9.0, 7.0, 1.0, 2.0, 5.0, 5.0, 3.0, 2.0, 5.0, 5.0, 3.0, 2.0, 3.0, 3.0, 3.0, 1.0, 4.0, 2.0, 3.0, 4.0, 6.0, 8.0, 8.0, 6.0, 7.0, 8.0, 6.0, 4.0, 7.0, 5.0, 2.0, 5.0, 5.0, 3.0, 4.0, 7.0, 7.0, 5.0, 1.0, 4.0, 4.0, 4.0, 2.0, 5.0, 3.0, 2.0, 5.0, 3.0, 1.0, 2.0, 3.0, 4.0, 7.0, 5.0, 9.0, 7.0, 8.0, 11.0, 11.0, 11.0, 9.0, 2.0, 3.0, 6.0, 4.0, 3.0, 3.0, 1.0, 2.0, 4.0, 6.0, 4.0, 4.0, 2.0, 3.0, 6.0, 4.0, 8.0, 6.0, 7.0, 8.0, 11.0, 9.0, 3.0, 1.0, 6.0, 4.0, 2.0, 2.0, 3.0, 4.0, 5.0, 3.0, 6.0, 3.0, 3.0, 3.0, 1.0, 2.0, 5.0, 3.0, 7.0, 5.0, 6.0, 8.0, 11.0, 9.0, 2.0, 3.0, 4.0, 7.0, 7.0, 5.0, 3.0, 3.0, 1.0, 2.0, 2.0, 5.0, 3.0, 4.0, 7.0, 7.0, 5.0, 2.0, 3.0, 5.0, 3.0, 1.0, 4.0, 2.0, 5.0, 5.0, 3.0, 3.0, 6.0, 4.0, 5.0, 8.0, 6.0, 10.0, 10.0, 10.0, 8.0, 9.0, 10.0, 2.0, 5.0, 3.0, 1.0, 4.0, 6.0, 6.0, 4.0, 5.0, 6.0, 2.0, 5.0, 3.0, 7.0, 7.0, 7.0, 5.0, 6.0, 8.0, 6.0, 9.0, 7.0, 2.0, 3.0, 4.0, 4.0, 7.0, 5.0, 3.0, 3.0, 3.0, 1.0, 4.0, 4.0, 7.0, 5.0, 6.0, 5.0, 6.0, 6.0, 7.0, 5.0, 4.0, 6.0, 6.0, 4.0, 4.0, 2.0, 5.0, 3.0, 6.0, 4.0, 5.0, 6.0, 7.0, 8.0, 6.0, 7.0, 6.0, 2.0, 3.0, 3.0, 1.0, 4.0, 2.0, 2.0, 3.0, 8.0, 6.0, 4.0, 2.0, 3.0, 3.0, 3.0, 5.0, 3.0, 4.0, 5.0, 3.0, 3.0, 3.0, 1.0, 4.0, 2.0, 6.0, 4.0, 7.0, 7.0, 5.0, 2.0, 5.0, 5.0, 3.0, 1.0, 4.0, 4.0, 2.0, 3.0, 4.0, 2.0, 5.0, 3.0, 4.0, 3.0, 4.0, 3.0, 5.0, 1.0, 4.0, 2.0, 4.0, 4.0, 4.0, 2.0, 5.0, 3.0, 2.0, 5.0, 3.0, 3.0, 3.0, 1.0, 4.0, 2.0, 6.0, 6.0, 6.0, 4.0, 5.0, 6.0, 2.0, 3.0, 4.0, 3.0, 3.0, 1.0, 2.0, 4.0, 4.0, 5.0, 2.0, 5.0, 3.0, 2.0, 2.0, 3.0, 3.0, 1.0, 4.0, 2.0, 6.0, 6.0, 6.0, 4.0, 5.0, 6.0, 2.0, 3.0, 4.0, 3.0, 5.0, 3.0, 4.0, 5.0, 3.0, 1.0, 4.0, 2.0, 3.0, 6.0, 4.0, 5.0, 8.0, 8.0, 6.0, 2.0, 3.0, 6.0, 6.0, 4.0, 5.0, 8.0, 6.0, 3.0, 5.0, 3.0, 1.0, 4.0, 2.0, 3.0, 4.0, 7.0, 7.0, 8.0, 8.0, 9.0, 7.0, 5.0, 2.0, 3.0, 3.0, 4.0, 5.0, 3.0, 1.0, 4.0, 4.0, 2.0, 6.0, 4.0, 5.0, 5.0, 6.0, 7.0, 2.0, 2.0, 7.0, 5.0, 5.0, 3.0, 6.0, 4.0, 7.0, 5.0, 6.0, 2.0, 3.0, 4.0, 7.0, 7.0, 5.0, 1.0, 4.0, 4.0, 2.0, 3.0, 6.0, 4.0, 5.0, 4.0, 2.0, 3.0, 3.0, 4.0, 5.0, 8.0, 6.0, 3.0, 3.0, 3.0, 3.0, 1.0, 4.0, 4.0, 2.0, 5.0, 5.0, 3.0, 2.0, 1.0, 4.0, 6.0, 6.0, 4.0, 5.0, 6.0, 4.0, 5.0, 8.0, 6.0, 4.0, 2.0, 3.0, 6.0, 6.0, 4.0, 5.0, 6.0, 2.0, 3.0, 4.0, 7.0, 7.0, 7.0, 5.0, 6.0, 9.0, 7.0, 4.0, 1.0, 2.0, 2.0, 5.0, 5.0, 3.0, 2.0, 5.0, 7.0, 5.0, 5.0, 3.0, 2.0, 5.0, 3.0, 1.0, 2.0, 3.0, 4.0, 6.0, 6.0, 6.0, 4.0, 5.0, 5.0, 8.0, 8.0, 6.0, 2.0, 3.0, 6.0, 6.0, 4.0, 3.0, 3.0, 3.0, 1.0, 2.0, 5.0, 7.0, 5.0, 3.0, 2.0, 5.0, 3.0, 4.0, 5.0, 6.0, 9.0, 7.0, 8.0, 11.0, 11.0, 11.0, 11.0, 9.0, 10.0, 1.0, 4.0, 2.0, 3.0, 10.0, 8.0, 6.0, 4.0, 2.0, 5.0, 5.0, 3.0, 4.0, 5.0, 6.0, 5.0, 3.0, 1.0, 4.0, 4.0, 4.0, 2.0, 3.0, 6.0, 4.0, 2.0, 5.0, 3.0, 2.0, 3.0, 5.0, 5.0, 3.0, 1.0, 4.0, 4.0, 2.0, 3.0, 3.0, 3.0, 3.0, 1.0, 2.0, 2.0, 5.0, 3.0, 4.0, 5.0, 2.0, 3.0, 4.0, 7.0, 5.0, 6.0, 7.0, 3.0, 6.0, 3.0, 3.0, 3.0, 3.0, 1.0, 2.0, 1.0, 4.0, 6.0, 6.0, 6.0, 4.0, 2.0, 5.0, 5.0, 3.0, 4.0, 5.0, 2.0, 5.0, 3.0, 3.0, 1.0, 4.0, 4.0, 2.0, 2.0, 5.0, 3.0, 2.0, 2.0, 5.0, 3.0, 6.0, 4.0, 5.0, 6.0, 3.0, 7.0, 5.0, 3.0, 1.0, 4.0, 2.0, 7.0, 5.0, 3.0, 4.0, 5.0, 2.0, 3.0, 4.0, 3.0, 6.0, 3.0, 3.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 1.0, 2.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0, 1.0, 4.0, 4.0, 2.0, 2.0, 2.0, 5.0, 3.0, 4.0, 5.0, 4.0, 7.0, 5.0, 6.0, 7.0, 2.0, 3.0, 6.0, 4.0, 5.0, 8.0, 8.0, 6.0, 3.0, 3.0, 3.0, 1.0, 4.0, 2.0, 3.0, 6.0, 4.0, 5.0, 6.0, 5.0, 7.0, 5.0, 6.0, 5.0, 2.0, 4.0, 4.0, 4.0, 2.0, 2.0, 3.0, 1.0, 4.0, 2.0, 6.0, 4.0, 5.0, 8.0, 8.0, 6.0, 5.0, 8.0, 6.0, 2.0, 2.0, 3.0, 1.0, 4.0, 4.0, 2.0, 2.0, 5.0, 3.0, 7.0, 7.0, 5.0, 6.0, 9.0, 7.0, 8.0, 11.0, 9.0, 2.0])

    def test_meanWeightedDepth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.meanWeightedDepth,
                         4.353693181818182)

    def test_medianWeightedDepth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.medianWeightedDepth, 4.0)

    def test_maxWeightedDepth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.maxWeightedDepth, 11.0)

    def test_minWeightedDepth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.minWeightedDepth, 1.0)

    def test_stdevWeightedDepth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdevWeightedDepth,
                         2.1464617078006403)

    def test_weightedSyntacticBreadths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.weightedSyntacticBreadths,
                         [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 3.0, 3.0, 3.0, 3.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 2.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 3.0, 2.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0])

    def test_meanWeightedBreadth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.meanWeightedBreadth,
                         1.3053977272727273)

    def test_medianWeightedBreadth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.medianWeightedBreadth, 1.0)

    def test_maxThemeBreadth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.maxWeightedBreadth, 3.0)

    def test_minWeightedBreadth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.minWeightedBreadth, 1.0)

    def test_stdevWeightedBreadth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdevWeightedBreadth,
                         0.5078886772161095)

    def test_syntacticProfile(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        profile = {'DET': 76, 'DET:Definite=Def': 47, 'DET:PronType=Art': 64, 'DET-det-NOUN': 75, 'NOUN': 189, 'NOUN:Number=Sing': 134, 'NOUN-nsubj-VERB': 35, 'VERB': 78, 'VERB:Aspect=Prog': 11, 'VERB:Tense=Pres': 33, 'VERB:VerbForm=Part': 28, 'VERB-acl-NOUN': 3, 'NOUN-dobj-VERB': 34, 'ADV': 23, 'ADV-advmod-ADP': 2, 'ADP': 81, 'ADP-prep-VERB': 32, 'ADJ': 62, 'ADJ:Degree=Pos': 60, 'ADJ-amod-NOUN': 54, 'NOUN-pobj-ADP': 71, 'VERB:Number=Sing': 17, 'VERB:Person=3': 17, 'VERB:VerbForm=Fin': 25, 'VERB-ROOT-VERB': 29, 'PUNCT': 69, 'PUNCT:PunctType=Peri': 35, 'PUNCT-punct-VERB': 47, 'ADV-advmod-AUX': 1, 'PRON': 22, 'PRON-expl-AUX': 2, 'AUX': 36, 'AUX-HAVE:Mood=Ind': 7, 'AUX-HAVE:Number=Sing': 6, 'AUX-HAVE:Person=3': 6, 'AUX-HAVE:Tense=Pres': 7, 'AUX-HAVE:VerbForm=Fin': 8, 'AUX-aux-AUX': 4, 'AUX-BE:Tense=Past': 6, 'AUX-BE:VerbForm=Part': 2, 'AUX-ROOT-AUX': 5, 'NOUN-attr-AUX': 2, 'ADP-prep-NOUN': 40, 'SCONJ': 17, 'SCONJ-advmod-VERB': 6, 'VERB:Aspect=Perf': 17, 'VERB:Tense=Past': 20, 'VERB-amod-NOUN': 6, 'NOUN:Number=Plur': 55, 'AUX-aux-VERB': 20, 'VERB-relcl-NOUN': 11, 'ADV:Degree=Cmp': 3, 'ADV-advmod-ADV': 2, 'ADV-advmod-VERB': 13, 'PUNCT-punct-AUX': 8, 'DET:Definite=Ind': 17, 'VERB-ccomp-VERB': 7, 'ADJ:Degree=Sup': 2, 'PRON:PronType=Rel': 9, 'PRON-nsubj-VERB': 9, 'NOUN-compound-NOUN': 18, 'ADP-prep-AUX': 2, 'PUNCT:PunctType=Comm': 31, 'NOUN-nsubj-AUX': 2, 'AUX-BE:Mood=Ind': 9, 'AUX-BE:Tense=Pres': 6, 'AUX-BE:VerbForm=Fin': 10, 'ADJ-acomp-AUX': 3, 'SCONJ-mark-VERB': 9, 'AUX-MODAL:VerbForm=Fin': 11, 'VERB:VerbForm=Inf': 25, 'VERB-ccomp-AUX': 2, 'PRON-nsubj-AUX': 3, 'AUX-relcl-NOUN': 2, 'NUM': 2, 'NUM:NumType=Card': 2, 'NUM-nummod-NOUN': 1, 'NOUN-npadvmod-ADV': 1, 'ADV-acomp-AUX': 1, 'SCONJ-prep-VERB': 2, 'VERB-pcomp-SCONJ': 1, 'NOUN-nsubjpass-VERB': 4, 'AUX-BE:VerbForm=Inf': 3, 'AUX-auxpass-VERB': 5, 'ADP-prep-PRON': 1, 'DET:Number=Plur': 3, 'DET:PronType=Dem': 9, 'AUX-HAVE:VerbForm=Inf': 1, 'SPACE': 5, 'SPACE-dep-VERB': 5, 'PART': 17, 'PART-aux-VERB': 11, 'VERB-xcomp-VERB': 3, 'PRON:Case=Acc': 4, 'PRON:Number=Plur': 5, 'PRON:Person=3': 4, 'PRON:PronType=Prs': 8, 'PRON:Reflex=Yes': 3, 'PRON-pobj-ADP': 2, 'AUX-BE:Number=Sing': 4, 'AUX-BE:Person=3': 4, 'VERB-advcl-VERB': 6, 'PUNCT-punct-NOUN': 10, 'NOUN-conj-NOUN': 10, 'CCONJ': 14, 'CCONJ:ConjType=Cmp': 14, 'CCONJ-cc-NOUN': 7, 'NOUN-nmod-NOUN': 2, 'NOUN-ROOT-NOUN': 1, 'DET:Number=Sing': 6, 'NOUN-appos-NOUN': 1, 'VERB-pcomp-ADP': 3, 'NOUN-nsubj-ADJ': 2, 'ADJ-ccomp-VERB': 2, 'PART:Polarity=Neg': 5, 'PART-neg-VERB': 3, 'PRON-appos-NOUN': 1, 'PART-preconj-VERB': 1, 'ADV-advmod-PART': 1, 'CCONJ-cc-VERB': 5, 'PRON:Gender=Neut': 1, 'PRON:Number=Sing': 2, 'VERB-conj-VERB': 5, 'NOUN-attr-VERB': 2, 'ADP-prep-ADJ': 3, 'PUNCT:PunctType=Dash': 3, 'PART-neg-AUX': 1, 'ADJ-amod-ADP': 1, 'ADJ-compound-NOUN': 1, 'PRON:Case=Nom': 1, 'PRON:Person=1': 3, 'PROPN': 13, 'PROPN:Number=Sing': 13, 'PROPN-nsubj-VERB': 3, 'PUNCT-punct-PROPN': 4, 'NOUN-appos-PROPN': 1, 'PART-prep-VERB': 1, 'NOUN-pobj-PART': 1, 'ADV-advmod-ADJ': 2, 'PRON-nsubjpass-VERB': 1, 'ADP-prt-VERB': 2, 'ADV:Degree=Sup': 1, 'PROPN-compound-PROPN': 6, 'NUM-appos-PROPN': 1, 'ADP-prep-NUM': 1, 'DET-det-PROPN': 1, 'PROPN-pobj-ADP': 3, 'PRON:Gender=Masc': 1, 'PRON:Poss=Yes': 2, 'PRON-poss-NOUN': 2, 'AUX-HAVE:Tense=Past': 1, 'NOUN-pobj-SCONJ': 1, 'VERB-prep-AUX': 1, 'NOUN-pobj-VERB': 1, 'CCONJ-preconj-ADJ': 1, 'CCONJ-cc-ADJ': 1, 'ADJ-conj-ADJ': 1, 'VERB-advcl-AUX': 1, 'PRON-expl-VERB': 1, 'VERB:Mood=Ind': 1, 'PROPN-compound-NOUN': 1, 'ADV-advmod-CCONJ': 1, 'PRON-dobj-VERB': 1}
        self.assertEqual(doc._.syntacticProfile,
                         profile)

    def test_syntacticProfileNormed(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        profileKeys = ['DET', 'DET:Definite=Def', 'DET:PronType=Art', 'DET-det-NOUN', 'NOUN', 'NOUN:Number=Sing', 'NOUN-nsubj-VERB', 'VERB', 'VERB:Aspect=Prog', 'VERB:Tense=Pres', 'VERB:VerbForm=Part', 'VERB-acl-NOUN', 'NOUN-dobj-VERB', 'ADV', 'ADV-advmod-ADP', 'ADP', 'ADP-prep-VERB', 'ADJ', 'ADJ:Degree=Pos', 'ADJ-amod-NOUN', 'NOUN-pobj-ADP', 'VERB:Number=Sing', 'VERB:Person=3', 'VERB:VerbForm=Fin', 'VERB-ROOT-VERB', 'PUNCT', 'PUNCT:PunctType=Peri', 'PUNCT-punct-VERB', 'ADV-advmod-AUX', 'PRON', 'PRON-expl-AUX', 'AUX', 'AUX-HAVE:Mood=Ind', 'AUX-HAVE:Number=Sing', 'AUX-HAVE:Person=3', 'AUX-HAVE:Tense=Pres', 'AUX-HAVE:VerbForm=Fin', 'AUX-aux-AUX', 'AUX-BE:Tense=Past', 'AUX-BE:VerbForm=Part', 'AUX-ROOT-AUX', 'NOUN-attr-AUX', 'ADP-prep-NOUN', 'SCONJ', 'SCONJ-advmod-VERB', 'VERB:Aspect=Perf', 'VERB:Tense=Past', 'VERB-amod-NOUN', 'NOUN:Number=Plur', 'AUX-aux-VERB', 'VERB-relcl-NOUN', 'ADV:Degree=Cmp', 'ADV-advmod-ADV', 'ADV-advmod-VERB', 'PUNCT-punct-AUX', 'DET:Definite=Ind', 'VERB-ccomp-VERB', 'ADJ:Degree=Sup', 'PRON:PronType=Rel', 'PRON-nsubj-VERB', 'NOUN-compound-NOUN', 'ADP-prep-AUX', 'PUNCT:PunctType=Comm', 'NOUN-nsubj-AUX', 'AUX-BE:Mood=Ind', 'AUX-BE:Tense=Pres', 'AUX-BE:VerbForm=Fin', 'ADJ-acomp-AUX', 'SCONJ-mark-VERB', 'AUX-MODAL:VerbForm=Fin', 'VERB:VerbForm=Inf', 'VERB-ccomp-AUX', 'PRON-nsubj-AUX', 'AUX-relcl-NOUN', 'NUM', 'NUM:NumType=Card', 'NUM-nummod-NOUN', 'NOUN-npadvmod-ADV', 'ADV-acomp-AUX', 'SCONJ-prep-VERB', 'VERB-pcomp-SCONJ', 'NOUN-nsubjpass-VERB', 'AUX-BE:VerbForm=Inf', 'AUX-auxpass-VERB', 'ADP-prep-PRON', 'DET:Number=Plur', 'DET:PronType=Dem', 'AUX-HAVE:VerbForm=Inf', 'SPACE', 'SPACE-dep-VERB', 'PART', 'PART-aux-VERB', 'VERB-xcomp-VERB', 'PRON:Case=Acc', 'PRON:Number=Plur', 'PRON:Person=3', 'PRON:PronType=Prs', 'PRON:Reflex=Yes', 'PRON-pobj-ADP', 'AUX-BE:Number=Sing', 'AUX-BE:Person=3', 'VERB-advcl-VERB', 'PUNCT-punct-NOUN', 'NOUN-conj-NOUN', 'CCONJ', 'CCONJ:ConjType=Cmp', 'CCONJ-cc-NOUN', 'NOUN-nmod-NOUN', 'NOUN-ROOT-NOUN', 'DET:Number=Sing', 'NOUN-appos-NOUN', 'VERB-pcomp-ADP', 'NOUN-nsubj-ADJ', 'ADJ-ccomp-VERB', 'PART:Polarity=Neg', 'PART-neg-VERB', 'PRON-appos-NOUN', 'PART-preconj-VERB', 'ADV-advmod-PART', 'CCONJ-cc-VERB', 'PRON:Gender=Neut', 'PRON:Number=Sing', 'VERB-conj-VERB', 'NOUN-attr-VERB', 'ADP-prep-ADJ', 'PUNCT:PunctType=Dash', 'PART-neg-AUX', 'ADJ-amod-ADP', 'ADJ-compound-NOUN', 'PRON:Case=Nom', 'PRON:Person=1', 'PROPN', 'PROPN:Number=Sing', 'PROPN-nsubj-VERB', 'PUNCT-punct-PROPN', 'NOUN-appos-PROPN', 'PART-prep-VERB', 'NOUN-pobj-PART', 'ADV-advmod-ADJ', 'PRON-nsubjpass-VERB', 'ADP-prt-VERB', 'ADV:Degree=Sup', 'PROPN-compound-PROPN', 'NUM-appos-PROPN', 'ADP-prep-NUM', 'DET-det-PROPN', 'PROPN-pobj-ADP', 'PRON:Gender=Masc', 'PRON:Poss=Yes', 'PRON-poss-NOUN', 'AUX-HAVE:Tense=Past', 'NOUN-pobj-SCONJ', 'VERB-prep-AUX', 'NOUN-pobj-VERB', 'CCONJ-preconj-ADJ', 'CCONJ-cc-ADJ', 'ADJ-conj-ADJ', 'VERB-advcl-AUX', 'PRON-expl-VERB', 'VERB:Mood=Ind', 'PROPN-compound-NOUN', 'ADV-advmod-CCONJ', 'PRON-dobj-VERB']
        profileValues = [1.6097160165462159e-06, 1.5876644820403395e-06, 1.6097160077938598e-06, 1.6097160165462159e-06, 0.11734772195100875, 0.1111685316507911, 5.7155921353452216e-05, 0.00017147511446523268, 1.5762725441930697e-47, 0.000171467764061607, 1.9698103109370564e-29, 1.0502827114718416e-13, 2.6461074700672327e-07, 3.6751492639822676e-09, 4.344777660469962e-56, 0.01954811895812287, 0.0010296004396043517, 0.03909473845471586, 0.03909473845471586, 0.03909473845471586, 0.11729030141889078, 0.000171467764061607, 0.000171467764061607, 0.000171467764061607, 1.2503365612760016e-15, 0.33333333374168345, 0.33333333333333354, 0.3333333337416833, 0.0, 1.905197378511503e-05, 2.5528741627242305e-25, 2.0422993301795482e-24, 2.934975251537704e-91, 2.934975251537704e-91, 2.934975251537704e-91, 2.934975251537704e-91, 3.724946553900859e-61, 5.105748325448461e-25, 8.624654039179588e-42, 2.0644014691841255e-281, 1.5317244976345382e-24, 9.19034698580723e-24, 0.018518518518518517, 2.8942975955463003e-18, 5.544342507309039e-68, 1.9698103109370564e-29, 1.9698103109370564e-29, 4.1431205309012577e-112, 0.006179190300217641, 1.6288530555859902e-37, 0.00017146776406035664, 1.0151057579821045e-122, 5.764954127036667e-212, 4.8871624456674475e-37, 2.093541928296115e-16, 2.205152575352049e-08, 1.1975779815782083e-65, 1.3975504996565956e-81, 1.9051973784484073e-05, 5.7885951910926005e-18, 7.093227575035193e-46, 2.477281763020949e-280, 4.08349919188988e-10, 1.3915246613768347e-265, 8.624654039179588e-42, 3.0241575045854284e-165, 8.624654039179588e-42, 4.536236256878146e-164, 2.8942975955463003e-18, 5.105748325450092e-25, 7.350403625698821e-09, 2.103985288001771e-261, 1.0080525015284763e-165, 3.0241575045854284e-165, 2.6421889416752313e-104, 2.6421889416752313e-104, 6.938256552387698e-296, 2.081476965716311e-295, 6.244430897148933e-295, 2.68196151880862e-58, 7.49331707657872e-294, 2.8748846797265295e-42, 1.5317244976345382e-24, 8.624654039179588e-42, 3.185804736395259e-284, 3.2143225767887714e-156, 3.104122128250716e-62, 6.881338230613748e-282, 2.714755092643318e-38, 2.714755092643318e-38, 5.2548867144738624e-14, 5.2548867144738624e-14, 8.108397861075463e-51, 5.7885951910926005e-18, 5.7885951910926005e-18, 1.4792876071535965e-98, 5.7885951910926005e-18, 1.210314497464257e-196, 6.778036433725769e-205, 8.61827013537561e-42, 8.61827013537561e-42, 1.5762725441930697e-47, 3.970229897868724e-21, 9.783250838459017e-92, 1.2250497547798627e-09, 1.2250497547798627e-09, 3.261083612819672e-92, 1.3548775895946469e-173, 2.48352791178414e-237, 3.104122128250716e-62, 2.980233494140968e-236, 4.694998230970349e-75, 9.730077433290555e-50, 2.9190232299871665e-49, 1.5120787522927123e-164, 3.137135159858683e-193, 2.2241335366653768e-215, 2.767065593704205e-200, 8.301196781112616e-200, 1.225049754660756e-09, 1.2103144906862195e-196, 1.4792876071535965e-98, 7.350298527964535e-09, 1.7504711857864028e-14, 8.757069689961499e-49, 1.1200623996644071e-166, 1.5120787522927123e-164, 9.920748693792508e-159, 3.3326096476146002e-152, 6.996880607359798e-147, 5.7885951910926005e-18, 2.52067850753242e-12, 2.52067850753242e-12, 5.429510185286636e-38, 1.2327484799244677e-99, 8.058236787314125e-129, 2.3497818471807976e-125, 4.229607324925436e-124, 1.2081339468108072e-107, 3.196852261497882e-117, 1.5959759509954837e-43, 1.2081339468108052e-107, 3.1618488384815892e-86, 2.6421889416752313e-104, 7.926566825025699e-104, 3.804752076012338e-102, 9.48554651544475e-86, 1.4792876071535965e-98, 2.347348180031211e-74, 2.347348180031211e-74, 3.724946553900859e-61, 1.6091769112851713e-57, 1.9698103107440054e-29, 3.9396206214880114e-28, 1.1910689693606172e-20, 1.0719620724245555e-19, 3.2158862172736668e-19, 6.946314229311121e-17, 6.251682806380008e-16, 1.2503365612760016e-15, 2.52067850753242e-12, 3.6751492639822676e-09, 1.9051973784484073e-05]
        self.assertEqual(list(doc._.syntacticProfileNormed.keys()),
                         profileKeys)
        self.assertEqual(list(doc._.syntacticProfileNormed.values()),
                         profileValues)

    def test_syntacticVariety(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.syntacticVariety, 163)

    def test_pastTenseScope(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        pastTenseScope = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.assertEqual(doc._.pastTenseScope,
                         pastTenseScope)

    def test_propn_past(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.propn_past,
                         0.3252840909090909)

    doc = holmes_manager.get_document('GRE_Sample_Essay')
