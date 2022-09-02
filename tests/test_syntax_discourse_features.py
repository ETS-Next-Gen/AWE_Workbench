import awe_workbench.parser.manager as holmes
from awe_workbench.parser.components.utility_functions import print_parse_tree
import unittest
import json

import tensorflow as tf
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
    'en_core_web_lg', perform_coreference_resolution=False, number_of_workers=2)

# GRE Sample from https://www.ets.org/gre/revised_general/prepare/analytical_writing/issue/sample_responses
holmes_manager.parse_and_register_document(
            document_text="The statement linking technology negatively with free thinking plays on recent human experience over the past century. Surely there has been no time in history where the lived lives of people have changed more dramatically. A quick reflection on a typical day reveals how technology has revolutionized the world. Most people commute to work in an automobile that runs on an internal combustion engine. During the workday, chances are high that the employee will interact with a computer that processes information on silicon bridges that are .09 microns wide. Upon leaving home, family members will be reached through wireless networks that utilize satellites orbiting the earth. Each of these common occurrences could have been inconceivable at the turn of the 19th century.\n\nThe statement attempts to bridge these dramatic changes to a reduction in the ability for humans to think for themselves. The assumption is that an increased reliance on technology negates the need for people to think creatively to solve previous quandaries. Looking back at the introduction, one could argue that without a car, computer, or mobile phone, the hypothetical worker would need to find alternate methods of transport, information processing and communication. Technology short circuits this thinking by making the problems obsolete.\n\nHowever, this reliance on technology does not necessarily preclude the creativity that marks the human species. The prior examples reveal that technology allows for convenience. The car, computer and phone all release additional time for people to live more efficiently. This efficiency does not preclude the need for humans to think for themselves. In fact, technology frees humanity to not only tackle new problems, but may itself create new issues that did not exist without technology. For example, the proliferation of automobiles has introduced a need for fuel conservation on a global scale. With increasing energy demands from emerging markets, global warming becomes a concern inconceivable to the horse-and-buggy generation. Likewise dependence on oil has created nation-states that are not dependent on taxation, allowing ruling parties to oppress minority groups such as women. Solutions to these complex problems require the unfettered imaginations of maverick scientists and politicians.\n\nIn contrast to the statement, we can even see how technology frees the human imagination. Consider how the digital revolution and the advent of the internet has allowed for an unprecedented exchange of ideas. WebMD, a popular internet portal for medical information, permits patients to self research symptoms for a more informed doctor visit. This exercise opens pathways of thinking that were previously closed off to the medical layman. With increased interdisciplinary interactions, inspiration can arrive from the most surprising corners. Jeffrey Sachs, one of the architects of the UN Millenium Development Goals, based his ideas on emergency care triage techniques. The unlikely marriage of economics and medicine has healed tense, hyperinflation environments from South America to Eastern Europe.\n\nThis last example provides the most hope in how technology actually provides hope to the future of humanity. By increasing our reliance on technology, impossible goals can now be achieved. Consider how the late 20th century witnessed the complete elimination of smallpox. This disease had ravaged the human race since prehistorical days, and yet with the technology of vaccines, free thinking humans dared to imagine a world free of smallpox. Using technology, battle plans were drawn out, and smallpox was systematically targeted and eradicated.\n\nTechnology will always mark the human experience, from the discovery of fire to the implementation of nanotechnology. Given the history of the human race, there will be no limit to the number of problems, both new and old, for us to tackle. There is no need to retreat to a Luddite attitude to new things, but rather embrace a hopeful posture to the possibilities that technology provides for new avenues of human imagination.", label='GRE_Sample_Essay')


class SyntaxDiscourseFeatureTest(unittest.TestCase):

    def test_paragraph_breaks(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        paragraph_breaks = [131, 223, 393, 527, 622, 703]
        self.assertEqual(doc._.paragraph_breaks,paragraph_breaks)        

    def test_paragraph_lengths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        paragraph_lengths = [131, 92, 170, 134, 95, 81]
        self.assertEqual(doc._.paragraph_lengths,paragraph_lengths)        

    def test_mean_paragraph_length(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_paragraph_length,117.16666666666667)        

    def test_median_paragraph_length(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.median_paragraph_length,113.0)        

    def test_max_paragraph_length(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.max_paragraph_length,170)

    def test_min_paragraph_length(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.min_paragraph_length,81)

    def test_stdev_paragraph_length(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdev_paragraph_length,33.760430486986785)

    def test_transition_word_profile(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')   
        profile = [24, {'temporal': 5, 'PARAGRAPH': 5, 'contrastive': 5, 'illustrative': 6, 'emphatic': 2, 'comparative': 1}, {'no time in history': 1, 'During the workday': 1, 'Upon leaving home': 1, 'at the turn of the 19th century': 1, 'NEWLINE': 5, 'however': 1, 'the prior examples': 1, 'in fact': 1, 'not only': 1, 'but': 2, 'for example': 1, 'likewise': 1, 'such as': 1, 'in contrast': 1, 'consider how': 2, 'this last example': 1, 'since prehistorical days': 1, 'and yet': 1}, [['no time in history', 18, 22, 25, 'temporal'], ['During the workday', 68, 68, 70, 'temporal'], ['Upon leaving home', 95, 95, 97, 'temporal'], ['at the turn of the 19th century', 114, 123, 129, 'temporal'], ['NEWLINE', 131, 131, 131, 'PARAGRAPH'], ['NEWLINE', 223, 223, 223, 'PARAGRAPH'], ['however', 224, 224, 224, 'contrastive'], ['the prior examples', 242, 242, 245, 'illustrative'], ['in fact', 283, 283, 284, 'emphatic'], ['not only', 283, 290, 291, 'emphatic'], ['but', 283, 296, 296, 'contrastive'], ['for example', 309, 309, 310, 'illustrative'], ['likewise', 351, 351, 351, 'comparative'], ['such as', 351, 374, 375, 'illustrative'], ['NEWLINE', 393, 393, 393, 'PARAGRAPH'], ['in contrast', 394, 394, 395, 'contrastive'], ['consider how', 411, 411, 412, 'illustrative'], ['NEWLINE', 527, 527, 527, 'PARAGRAPH'], ['this last example', 528, 528, 531, 'illustrative'], ['consider how', 561, 561, 562, 'illustrative'], ['since prehistorical days', 574, 581, 583, 'temporal'], ['and yet', 574, 585, 586, 'contrastive'], ['NEWLINE', 622, 622, 622, 'PARAGRAPH'], ['but', 671, 685, 685, 'contrastive']]]
        self.assertEqual(doc._.transition_word_profile,profile)

    def test_total_transition_words(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.total_transition_words,24)

    def test_transition_category_count(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.transition_category_count,6)

    def test_transition_word_type_count(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.transition_word_type_count,18)
        
    def test_transition_words(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')       
        transition_words = [['no time in history', 18, 22, 25, 'temporal'], ['During the workday', 68, 68, 70, 'temporal'], ['Upon leaving home', 95, 95, 97, 'temporal'], ['at the turn of the 19th century', 114, 123, 129, 'temporal'], ['NEWLINE', 131, 131, 131, 'PARAGRAPH'], ['NEWLINE', 223, 223, 223, 'PARAGRAPH'], ['however', 224, 224, 224, 'contrastive'], ['the prior examples', 242, 242, 245, 'illustrative'], ['in fact', 283, 283, 284, 'emphatic'], ['not only', 283, 290, 291, 'emphatic'], ['but', 283, 296, 296, 'contrastive'], ['for example', 309, 309, 310, 'illustrative'], ['likewise', 351, 351, 351, 'comparative'], ['such as', 351, 374, 375, 'illustrative'], ['NEWLINE', 393, 393, 393, 'PARAGRAPH'], ['in contrast', 394, 394, 395, 'contrastive'], ['consider how', 411, 411, 412, 'illustrative'], ['NEWLINE', 527, 527, 527, 'PARAGRAPH'], ['this last example', 528, 528, 531, 'illustrative'], ['consider how', 561, 561, 562, 'illustrative'], ['since prehistorical days', 574, 581, 583, 'temporal'], ['and yet', 574, 585, 586, 'contrastive'], ['NEWLINE', 622, 622, 622, 'PARAGRAPH'], ['but', 671, 685, 685, 'contrastive']]
        self.assertEqual(doc._.transition_words,transition_words)         
        
    def test_transition_distances(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')       
        transition_distances = [0.18068242073059082, 0.3455371856689453, 0.5115512013435364, 0.29295045137405396, 0.26799535751342773, 0.2427629828453064, 0.2613025903701782, 0.3560638427734375, 0.36619603633880615, 0.3768072724342346, 0.171677827835083, 0.21559733152389526, 0.42869412899017334, 0.4524803161621094, 0.4260185956954956, 0.46465003490448, 0.26872915029525757, 0.580579549074173, 0.5725382268428802, 0.41816604137420654, 0.3364747166633606, 0.3091871738433838, 0.6479913592338562, 0.19418299198150635]
        self.assertEqual(doc._.transition_distances,transition_distances)         

    def test_mean_transition_distance(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_transition_distance,0.36203403274218243)        

    def test_median_transition_distance(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.median_transition_distance,0.3508005142211914)        

    def test_max_transition_distance(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.max_transition_distance,0.6479913592338562)

    def test_min_transition_distance(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.min_transition_distance,0.171677827835083)

    def test_stdev_transition_distance(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdev_transition_distance,0.13121922014592205)

    def test_intersentence_cohesions(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        intersentence_cohesions = [0.8988593220710754, 0.8736750483512878, 0.8477486968040466, 0.8780263066291809, 0.8904399871826172, 0.8478362560272217, 0.9370104670524597, 0.8875330090522766, 0.8721916675567627, 0.8789311647415161, 0.87635737657547, 0.8838761448860168, 0.9297630190849304, 0.8696791529655457, 0.8978860974311829, 0.8615327477455139, 0.855689525604248, 0.9006693363189697, 0.8269333839416504, 0.8536540865898132, 0.8761308789253235, 0.8271347880363464, 0.8295413255691528, 0.87627112865448, 0.7860766053199768, 0.8845039010047913, 0.8930788040161133, 0.9311631321907043, 0.9270924925804138]
        self.assertEqual(doc._.intersentence_cohesions,intersentence_cohesions)

    def test_mean_sent_cohesion(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_sent_cohesion,0.8758374432037617)        

    def test_median_sent_cohesion(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.median_sent_cohesion,0.87635737657547)        

    def test_max_sent_cohesion(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.max_sent_cohesion,0.9370104670524597)

    def test_min_sent_cohesion(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.min_sent_cohesion,0.7860766053199768)

    def test_stdev_sent_cohesion(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdev_sent_cohesion,0.034052641098106864)

    def test_sliding_window_cohesions(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        sliding_window_cohesions = [0.7181742191314697, 0.701263427734375, 0.6790735125541687, 0.6474848985671997, 0.6590394377708435, 0.7189511656761169, 0.6720224618911743, 0.7850678563117981, 0.8007805347442627, 0.7889644503593445, 0.7991914749145508, 0.8140134215354919, 0.8126447200775146, 0.7754191160202026, 0.7475166320800781, 0.7887311577796936, 0.6866664290428162, 0.7194632887840271, 0.7194632887840271, 0.6448104977607727, 0.6458194255828857, 0.6696494221687317, 0.5748744010925293, 0.5917541980743408, 0.4936998188495636, 0.6006785035133362, 0.5567438006401062, 0.5973606705665588, 0.6129812002182007, 0.659326434135437, 0.688444972038269, 0.7055871486663818, 0.6687339544296265, 0.6260309815406799, 0.5268124938011169, 0.5692242980003357, 0.5738590955734253, 0.5684884190559387, 0.6827142238616943, 0.6544976234436035, 0.6336449980735779, 0.5551523566246033, 0.571733832359314, 0.5404956936836243, 0.3755459487438202, 0.5269684791564941, 0.5898616313934326, 0.41509121656417847, 0.44168174266815186, 0.4371638000011444, 0.3960413932800293, 0.4594825208187103, 0.4970448911190033, 0.5166383981704712, 0.5925062298774719, 0.5895653367042542, 0.6845969557762146, 0.46040961146354675, 0.42461514472961426, 0.44434645771980286, 0.4096076488494873, 0.44259214401245117, 0.4406617283821106, 0.44507601857185364, 0.5546365976333618, 0.43519437313079834, 0.5321240425109863, 0.4746674597263336, 0.4140016734600067, 0.4774576425552368, 0.4703843891620636, 0.5924128293991089, 0.5924128293991089, 0.5004821419715881, 0.4637318253517151, 0.33062052726745605, 0.27226918935775757, 0.2537829577922821, 0.2854864001274109, 0.3904673755168915, 0.4211515188217163, 0.45139551162719727, 0.5127795934677124, 0.38112887740135193, 0.24094435572624207, 0.2918039858341217, 0.1845623105764389, 0.22997146844863892, 0.36806720495224, 0.4143584966659546, 0.3875931203365326, 0.38407766819000244, 0.4325980246067047, 0.4053116738796234, 0.3240915536880493, 0.3403795063495636, 0.3285251259803772, 0.3186679482460022, 0.38233309984207153, 0.40397265553474426, 0.4056640863418579, 0.423939049243927, 0.4444441497325897, 0.3398769795894623, 0.36920079588890076, 0.36920079588890076, 0.3883742094039917, 0.42753884196281433, 0.41213420033454895, 0.37709927558898926, 0.39389845728874207, 0.4492016136646271, 0.4492016136646271, 0.2987273335456848, 0.29447853565216064, 0.3743438422679901, 0.4030083119869232, 0.4750116765499115, 0.42504170536994934, 0.48562872409820557, 0.5353590846061707, 0.5397853255271912, 0.5397853255271912, 0.5133278369903564, 0.4792203903198242, 0.5079424977302551, 0.4732956290245056, 0.4496147334575653, 0.47529879212379456, 0.4816325306892395, 0.4889850616455078, 0.6232978701591492, 0.6232978701591492, 0.6785002946853638, 0.6828945279121399, 0.6430901288986206, 0.630759596824646, 0.7013497948646545, 0.7213090062141418, 0.7430066466331482, 0.7345995306968689, 0.7214844822883606, 0.6629474759101868, 0.6360165476799011, 0.6232730746269226, 0.5883044600486755, 0.6633849740028381, 0.6633849740028381, 0.7151890397071838, 0.7056543827056885, 0.6081593632698059, 0.5876198410987854, 0.5129061937332153, 0.5064864754676819, 0.5264977812767029, 0.45184406638145447, 0.5640366077423096, 0.5242792367935181, 0.5922706127166748, 0.5628295540809631, 0.5925487875938416, 0.6522911190986633, 0.5478234887123108, 0.5763028264045715, 0.618124783039093, 0.6638599634170532, 0.5731121897697449, 0.5437830686569214, 0.5437830686569214, 0.4712313711643219, 0.4569089710712433, 0.5454812049865723, 0.48367583751678467, 0.42092519998550415, 0.48569998145103455, 0.42305129766464233, 0.2977829873561859, 0.2977829873561859, 0.3928380012512207, 0.5374341607093811, 0.5031077861785889, 0.680233359336853, 0.680233359336853, 0.7139794230461121, 0.495082288980484, 0.4879363477230072, 0.4879363477230072, 0.5396188497543335, 0.5411055088043213, 0.5838121771812439, 0.5381329655647278, 0.6154993176460266, 0.6020007133483887, 0.5532087087631226, 0.5166041851043701, 0.6518845558166504, 0.6322896480560303, 0.6936717629432678, 0.7012785077095032, 0.6895168423652649, 0.7263908982276917, 0.6917502284049988, 0.702608048915863, 0.6224715709686279, 0.6139522194862366, 0.5929139256477356, 0.6004048585891724, 0.6113495230674744, 0.6583157777786255, 0.563602089881897, 0.5703687071800232, 0.624764621257782, 0.6356892585754395, 0.5418727993965149, 0.660626232624054, 0.6365984678268433, 0.6365984678268433, 0.6277673840522766, 0.6215293407440186, 0.6219359636306763, 0.5721964836120605, 0.5492886304855347, 0.5228410959243774, 0.5004310011863708, 0.5531101822853088, 0.5986908078193665, 0.5671816468238831, 0.5866214036941528, 0.5946487188339233, 0.721796989440918, 0.6296963095664978, 0.6760013103485107, 0.6499212980270386, 0.6191558241844177, 0.5661692023277283, 0.5312169790267944, 0.42728954553604126, 0.4562321603298187, 0.4211899936199188, 0.43973419070243835, 0.4918561577796936, 0.588962733745575, 0.6923847794532776, 0.7171835899353027, 0.6751047372817993, 0.7206659913063049, 0.6406289935112, 0.6438475251197815, 0.5796738266944885, 0.5699208974838257, 0.5898752808570862, 0.5684922337532043, 0.5515444278717041, 0.5951597690582275, 0.5218393206596375, 0.55599445104599, 0.4096278250217438, 0.5285232663154602, 0.5646203756332397, 0.6959474682807922, 0.7203365564346313, 0.7185603380203247, 0.6625391840934753, 0.6423453092575073, 0.4971276819705963, 0.5273186564445496, 0.3788944184780121, 0.48065927624702454, 0.6103437542915344, 0.7828500866889954, 0.7766262292861938, 0.7812368273735046, 0.6906050443649292, 0.696194589138031, 0.6632706522941589, 0.5880956053733826, 0.6033019423484802, 0.600532054901123, 0.6870222687721252, 0.5664738416671753, 0.6295509338378906, 0.6456001400947571, 0.6606005430221558, 0.6630827784538269, 0.6997432708740234, 0.7766095399856567, 0.822784423828125, 0.7297685742378235, 0.7680246829986572, 0.7385520935058594, 0.8694490194320679, 0.8062267899513245, 0.7353216409683228, 0.7639004588127136, 0.7887110114097595, 0.7451591491699219, 0.7286704182624817, 0.7197006344795227, 0.5714356899261475, 0.6237432956695557, 0.6275636553764343, 0.6628205180168152, 0.6909197568893433, 0.6639208197593689, 0.6479867696762085, 0.6235129833221436, 0.5890401601791382, 0.6758988499641418, 0.5882089138031006, 0.5884600877761841, 0.5746558904647827, 0.6486964821815491, 0.6165353655815125, 0.7018287181854248, 0.7054082751274109, 0.6990912556648254, 0.7131054401397705, 0.7826208472251892, 0.8002692461013794, 0.8187614679336548, 0.7922825217247009, 0.7839767336845398, 0.8015739917755127, 0.8150758743286133, 0.8106814026832581, 0.7866733074188232, 0.7180758714675903, 0.5957860350608826, 0.5097404718399048, 0.518147885799408, 0.42179739475250244, 0.3904438316822052, 0.34155407547950745, 0.4236290752887726, 0.5133522152900696, 0.5123850703239441, 0.6250080466270447, 0.5969473719596863, 0.5544553399085999, 0.5544728636741638, 0.49274978041648865, 0.4804668128490448, 0.393265962600708, 0.47033119201660156, 0.5464437007904053, 0.6502533555030823, 0.650912344455719, 0.6295266151428223, 0.6125736832618713, 0.7110123634338379, 0.6587409377098083, 0.6810725927352905, 0.6525141596794128, 0.5871813893318176, 0.5741062760353088, 0.6681912541389465, 0.6420008540153503, 0.6505707502365112, 0.5556239485740662, 0.5587475299835205, 0.5747273564338684, 0.6126003265380859, 0.6067212820053101, 0.5422795414924622, 0.4704667627811432, 0.5488695502281189, 0.536759078502655, 0.5157687664031982, 0.47764521837234497, 0.47986119985580444, 0.5271527767181396, 0.5498452186584473, 0.5290605425834656, 0.46688687801361084, 0.3602869212627411, 0.37699976563453674, 0.3809293508529663, 0.45073172450065613, 0.49928227066993713, 0.5415453314781189, 0.5122532844543457, 0.5543336272239685, 0.36085236072540283, 0.3665997087955475, 0.3116161823272705, 0.3116161823272705, 0.22969196736812592, 0.49183592200279236, 0.4778640866279602, 0.3747110962867737, 0.39294037222862244, 0.4299679398536682, 0.37511005997657776, 0.45231547951698303, 0.45231547951698303, 0.45231547951698303, 0.311810165643692, 0.6087309122085571, 0.6377063393592834, 0.5729437470436096, 0.5713992118835449, 0.5866880416870117, 0.5389125347137451, 0.5725162625312805, 0.5725162625312805, 0.6103866696357727, 0.5800052285194397, 0.6384758353233337, 0.6805055737495422, 0.6303063631057739, 0.632068932056427, 0.6773736476898193, 0.5216607451438904, 0.5345773100852966, 0.5092067718505859, 0.549133837223053, 0.5851325392723083, 0.6893542408943176, 0.6067965626716614, 0.5960580110549927, 0.6024318933486938, 0.6473482251167297, 0.5909489393234253, 0.622308611869812, 0.5430110096931458, 0.5262013673782349, 0.5152072906494141, 0.5069680213928223, 0.47498154640197754, 0.47355157136917114, 0.5156494379043579, 0.5657385587692261, 0.6107592582702637, 0.6410508751869202, 0.7491336464881897, 0.7429540157318115, 0.708656907081604, 0.7128888368606567, 0.7051429748535156, 0.7304097414016724, 0.7082116007804871, 0.7053606510162354, 0.6371103525161743, 0.6145652532577515, 0.6448284387588501, 0.5823889970779419, 0.47524186968803406, 0.4950029253959656, 0.5897514820098877, 0.733385443687439, 0.6809965372085571, 0.6470853686332703, 0.5646995306015015, 0.5743997693061829, 0.567176878452301, 0.5640305876731873, 0.5190287232398987, 0.5860862731933594, 0.45603713393211365, 0.601533830165863, 0.5251269936561584, 0.5251269936561584, 0.4691050052642822, 0.4861484169960022, 0.3381423354148865, 0.3549068570137024, 0.33667048811912537, 0.34557345509529114, 0.3017862141132355, 0.26958876848220825, 0.26958876848220825, 0.26958876848220825, 0.22090551257133484, 0.10331247001886368, 0.09946548193693161, 0.1849459409713745, 0.30455225706100464, 0.32518064975738525, 0.28176671266555786, 0.28176671266555786, 0.25893980264663696, 0.2179955095052719, 0.2763611972332001, 0.23003195226192474, 0.2358841449022293, 0.245754212141037, 0.2904397249221802, 0.45536285638809204, 0.5272293090820312, 0.5028709769248962, 0.5775105357170105, 0.5243103504180908, 0.5537710785865784, 0.609525203704834, 0.6606168746948242, 0.6810840368270874, 0.5901070833206177, 0.5769197940826416, 0.5662568211555481, 0.5474407076835632, 0.5445433855056763, 0.6205247640609741, 0.6047906279563904, 0.628349781036377, 0.5308804512023926, 0.5292799472808838, 0.49483180046081543, 0.4438880383968353, 0.44538453221321106, 0.39144372940063477, 0.32624340057373047, 0.33729884028434753, 0.36647048592567444, 0.5381368398666382, 0.5796362161636353, 0.4877815842628479, 0.4056786298751831, 0.3741012513637543, 0.3741012513637543, 0.41936007142066956, 0.3283812701702118, 0.2851704955101013, 0.43395164608955383, 0.5865570902824402, 0.5865570902824402, 0.6814536452293396, 0.8771107196807861, 0.8514654636383057, 0.8616060018539429, 0.8265013098716736, 0.7317827343940735, 0.6125732660293579, 0.6415880918502808, 0.6415880918502808, 0.6773134469985962, 0.7344356179237366, 0.7574276328086853, 0.7808356285095215, 0.7187724113464355, 0.6987088322639465, 0.7151852250099182, 0.6983718276023865, 0.6730572581291199, 0.6597504019737244, 0.606074333190918, 0.5605922937393188, 0.6138680577278137, 0.5882761478424072, 0.566649317741394, 0.5377964377403259, 0.4628887176513672, 0.5489749312400818, 0.5501205325126648, 0.572618842124939, 0.5328660607337952, 0.48593321442604065, 0.610148012638092, 0.5011742115020752, 0.42126917839050293, 0.43704622983932495, 0.35713109374046326, 0.39734765887260437, 0.5136548280715942, 0.5295951962471008, 0.5775947570800781, 0.6341943144798279, 0.6095657348632812, 0.5941829681396484, 0.4871390759944916, 0.4948325455188751, 0.33891695737838745, 0.3814352750778198, 0.40467697381973267, 0.5137110352516174, 0.4322446584701538, 0.4563347399234772, 0.4418659508228302, 0.5515823364257812, 0.5925307869911194, 0.5925307869911194, 0.41388991475105286, 0.42125800251960754, 0.44196179509162903, 0.5017839074134827, 0.4229195713996887, 0.6369653940200806, 0.7045741677284241, 0.7806202173233032, 0.8586754202842712, 0.8089002966880798, 0.701143205165863, 0.6780319809913635, 0.560285747051239, 0.6080725193023682, 0.6440467834472656, 0.6091873645782471, 0.6041891574859619, 0.7203472852706909, 0.6859999299049377, 0.6288899779319763, 0.5956356525421143, 0.6310295462608337, 0.6070647239685059, 0.6026177406311035, 0.37063199281692505, 0.5363000631332397, 0.5828129053115845, 0.5072140693664551, 0.5353472828865051, 0.5218008160591125, 0.5945451855659485, 0.4543611705303192, 0.3569714426994324, 0.3569714426994324, 0.352898508310318, 0.5161055326461792, 0.5477725267410278, 0.547351598739624, 0.5778474807739258, 0.49038827419281006, 0.5734430551528931, 0.6217519640922546, 0.656516969203949, 0.656516969203949, 0.5748251676559448, 0.6277108192443848, 0.6926324367523193, 0.6373811364173889, 0.6373811364173889, 0.6303789615631104, 0.5546615123748779, 0.5224807858467102, 0.5113321542739868, 0.4760902225971222, 0.492556631565094, 0.463143527507782, 0.5552494525909424, 0.5552494525909424, 0.4319190979003906, 0.4683215916156769, 0.48052531480789185, 0.5751261115074158, 0.5751261115074158, 0.4873209297657013, 0.5247870087623596, 0.45412883162498474, 0.5261881351470947, 0.5261881351470947, 0.4173544943332672, 0.4647064805030823, 0.36291688680648804, 0.4990863800048828, 0.4990863800048828, 0.44398272037506104, 0.5105710625648499, 0.34621956944465637, 0.5540810227394104, 0.5540810227394104, 0.5187355875968933, 0.5187355875968933, 0.4385828673839569, 0.39906346797943115, 0.4428623914718628, 0.4133220314979553, 0.49259528517723083, 0.3077422082424164, 0.48961880803108215, 0.4834340512752533, 0.515978991985321, 0.5658944249153137, 0.626227617263794, 0.5341516137123108, 0.6856047511100769, 0.6929025053977966, 0.6483656167984009, 0.6830957531929016, 0.6830957531929016, 0.6730726957321167, 0.5893316268920898, 0.6402474045753479, 0.6975016593933105, 0.6524498462677002, 0.6220090389251709, 0.5655167698860168]
        self.assertEqual(doc._.sliding_window_cohesions,sliding_window_cohesions)

    def test_mean_slider_cohesion(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_slider_cohesion,0.5534532958783253)        

    def test_median_slider_cohesion(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.median_slider_cohesion,0.5658164918422699)        

    def test_max_slider_cohesion(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.max_slider_cohesion,0.8771107196807861)

    def test_min_slider_cohesion(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.min_slider_cohesion,0.09946548193693161)

    def test_stdev_slider_cohesion(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdev_slider_cohesion,0.13222311851638907)

    def test_num_coref_chains(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.num_corefs,4)        

    def test_mean_coref_chain_len(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_coref_chain_len,2)        

    def test_median_coref_chain_len(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.median_coref_chain_len,2.0)        

    def test_max_coref_chain_len(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.max_coref_chain_len,2)

    def test_min_coref_chain_len(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.min_coref_chain_len,2)

    def test_stdev_coref_chain_len(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdev_coref_chain_len,0.0)

    def test_sentence_count(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.sentence_count,40)        

    def test_sentence_lengths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.sentence_lengths,[18, 19, 15, 16, 27, 19, 17, 1, 21, 22, 37, 11, 1, 18, 10, 17, 14, 26, 19, 23, 27, 15, 1, 17, 20, 23, 16, 14, 23, 20, 1, 19, 14, 13, 31, 17, 1, 19, 29, 33])        

    def test_mean_sentence_lengths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_sentence_len, 17.6)        

    def test_median_sentence_lengths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.median_sentence_len,18.0)        

    def test_max_sentence_lengths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.max_sentence_len,37)

    def test_min_sentence_lengths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.min_sentence_len,1)

    def test_stdev_sentence_lengths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.std_sentence_len,8.577848633514536)

    def test_sqrt_sentence_lengths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.sqrt_sentence_lengths,[4.242640687119285, 4.358898943540674, 3.872983346207417, 4.0, 5.196152422706632, 4.358898943540674, 4.123105625617661, 1.0, 4.58257569495584, 4.69041575982343, 6.082762530298219, 3.3166247903554, 1.0, 4.242640687119285, 3.1622776601683795, 4.123105625617661, 3.7416573867739413, 5.0990195135927845, 4.358898943540674, 4.795831523312719, 5.196152422706632, 3.872983346207417, 1.0, 4.123105625617661, 4.47213595499958, 4.795831523312719, 4.0, 3.7416573867739413, 4.795831523312719, 4.47213595499958, 1.0, 4.358898943540674, 3.7416573867739413, 3.605551275463989, 5.5677643628300215, 4.123105625617661, 1.0, 4.358898943540674, 5.385164807134504, 5.744562646538029])

    def test_mean_sqrt_sentence_lengths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_sqrt_sentence_len, 3.9925981953415106)        

    def test_median_sqrt_sentence_lengths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.median_sqrt_sentence_len,4.242640687119285)        

    def test_max_sqrt_sentence_lengths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.max_sqrt_sentence_len,6.082762530298219)

    def test_min_sqrt_sentence_lengths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.min_sqrt_sentence_len,1.0)

    def test_stdev_sqrt_sentence_lengths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.std_sqrt_sentence_len,1.3044930838061841)

    def test_words_to_sentence_root(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.words_before_sentence_root,[1, 3, 7, 2, 5, 22, 8, 7, 0, 2, 2, 8, 4, 0, 9, 3, 7, 4, 4, 8, 10, 5, 5, 0, 9, 0, 10, 2, 7, 14, 8, 0, 3, 11, 12, 0, 3, 6, 0, 3, 10, 1])

    def test_mean_words_to_sentence_root(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.mean_words_to_sentence_root, 5.357142857142857)        

    def test_median_words_to_sentence_root(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.median_words_to_sentence_root,4.5)        

    def test_max_words_to_sentence_root(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.max_words_to_sentence_root,22)

    def test_min_words_to_sentence_root(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.min_words_to_sentence_root,0)

    def test_stdev_words_to_sentence_root(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdev_words_to_sentence_root,4.621378891320518)

    def test_syntacticRhemeDepths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.syntacticRhemeDepths,[2.0, 2.0, 2.0, 0.0, 2.0, 2.0, 2.0, 2.0, 0.0, 2.0, 2.0, 2.0, 2.0, 0.0, 0.0, 2.0, 3.0, 3.0, 2.0, 3.0, 3.0, 2.0, 3.0, 5.0, 4.0, 2.0, 2.0, 2.0, 2.0, 2.0, 0.0, 2.0, 2.0, 0.0, 2.0, 3.0, 3.0, 3.0, 2.0, 2.0, 0.0])

    def test_meanRhemeDepth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.meanRhemeDepth, 1.975609756097561)        

    def test_medianRhemeDepth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.medianRhemeDepth,2.0)        

    def test_maxRhemeDepth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.maxRhemeDepth,5.0)

    def test_minRhemeDepth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.minRhemeDepth,0.0)

    def test_stdevRhemeDepth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdevRhemeDepth,1.1065216870456895)

    def test_syntacticThemeDepths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.syntacticThemeDepths,[1.0, 2.0, 3.0, 3.0, 3.0, 6.0, 5.0, 4.0, 5.0, 7.0, 7.0, 6.0, 5.0, 7.0, 7.0, 6.0, 2.0, 1.0, 3.0, 2.0, 3.0, 4.0, 6.0, 7.0, 7.0, 6.0, 7.0, 8.0, 6.0, 5.0, 7.0, 6.0, 2.0, 1.0, 3.0, 3.0, 3.0, 2.0, 4.0, 3.0, 2.0, 1.0, 2.0, 3.0, 2.0, 4.0, 3.0, 5.0, 4.0, 5.0, 7.0, 7.0, 7.0, 6.0, 2.0, 1.0, 2.0, 3.0, 4.0, 3.0, 3.0, 2.0, 3.0, 5.0, 4.0, 6.0, 5.0, 6.0, 7.0, 9.0, 8.0, 10.0, 9.0, 12.0, 11.0, 10.0, 2.0, 1.0, 2.0, 4.0, 3.0, 5.0, 4.0, 5.0, 6.0, 8.0, 7.0, 2.0, 1.0, 2.0, 2.0, 4.0, 3.0, 4.0, 6.0, 6.0, 5.0, 2.0, 1.0, 1.0, 3.0, 2.0, 4.0, 4.0, 3.0, 3.0, 5.0, 4.0, 5.0, 7.0, 6.0, 7.0, 8.0, 8.0, 7.0, 8.0, 9.0, 2.0, 1.0, 3.0, 4.0, 4.0, 3.0, 4.0, 5.0, 2.0, 4.0, 3.0, 5.0, 5.0, 5.0, 4.0, 5.0, 6.0, 5.0, 7.0, 6.0, 2.0, 1.0, 3.0, 3.0, 5.0, 4.0, 5.0, 4.0, 5.0, 5.0, 5.0, 4.0, 3.0, 4.0, 4.0, 3.0, 3.0, 2.0, 4.0, 3.0, 5.0, 4.0, 5.0, 6.0, 7.0, 7.0, 6.0, 7.0, 6.0, 2.0, 1.0, 2.0, 3.0, 6.0, 5.0, 4.0, 2.0, 1.0, 1.0, 3.0, 2.0, 4.0, 3.0, 5.0, 5.0, 4.0, 2.0, 1.0, 4.0, 3.0, 2.0, 3.0, 4.0, 2.0, 1.0, 3.0, 2.0, 3.0, 3.0, 3.0, 2.0, 4.0, 3.0, 2.0, 1.0, 3.0, 2.0, 4.0, 4.0, 4.0, 3.0, 4.0, 5.0, 2.0, 1.0, 2.0, 3.0, 3.0, 4.0, 2.0, 4.0, 3.0, 2.0, 2.0, 2.0, 2.0, 1.0, 3.0, 2.0, 4.0, 4.0, 4.0, 3.0, 4.0, 5.0, 2.0, 1.0, 3.0, 2.0, 3.0, 5.0, 4.0, 3.0, 5.0, 5.0, 4.0, 2.0, 1.0, 3.0, 2.0, 3.0, 4.0, 6.0, 6.0, 7.0, 7.0, 7.0, 6.0, 5.0, 2.0, 1.0, 3.0, 3.0, 2.0, 4.0, 3.0, 4.0, 4.0, 5.0, 6.0, 4.0, 4.0, 7.0, 6.0, 6.0, 5.0, 7.0, 6.0, 8.0, 7.0, 8.0, 2.0, 1.0, 3.0, 3.0, 2.0, 3.0, 5.0, 4.0, 5.0, 4.0, 2.0, 1.0, 1.0, 3.0, 3.0, 2.0, 4.0, 4.0, 3.0, 2.0, 1.0, 3.0, 4.0, 4.0, 3.0, 4.0, 4.0, 3.0, 4.0, 6.0, 5.0, 3.0, 2.0, 3.0, 5.0, 5.0, 4.0, 5.0, 6.0, 2.0, 1.0, 2.0, 5.0, 4.0, 3.0, 2.0, 2.0, 4.0, 5.0, 4.0, 4.0, 3.0, 2.0, 1.0, 2.0, 3.0, 4.0, 4.0, 4.0, 4.0, 3.0, 4.0, 5.0, 7.0, 7.0, 6.0, 2.0, 1.0, 2.0, 4.0, 5.0, 4.0, 3.0, 2.0, 1.0, 3.0, 2.0, 3.0, 7.0, 6.0, 5.0, 4.0, 2.0, 1.0, 2.0, 2.0, 3.0, 2.0, 3.0, 5.0, 4.0, 3.0, 5.0, 4.0, 2.0, 1.0, 1.0, 3.0, 3.0, 2.0, 3.0, 5.0, 5.0, 5.0, 4.0, 5.0, 5.0, 7.0, 6.0, 7.0, 8.0, 2.0, 1.0, 2.0, 1.0, 3.0, 4.0, 4.0, 4.0, 3.0, 2.0, 4.0, 4.0, 3.0, 4.0, 5.0, 2.0, 1.0, 3.0, 3.0, 2.0, 2.0, 4.0, 3.0, 2.0, 2.0, 2.0, 1.0, 3.0, 2.0, 3.0, 4.0, 2.0, 4.0, 3.0, 2.0, 1.0, 3.0, 2.0, 4.0, 3.0, 4.0, 5.0, 6.0, 2.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 2.0, 1.0, 2.0, 1.0, 1.0, 3.0, 3.0, 2.0, 2.0, 2.0, 4.0, 3.0, 4.0, 5.0, 4.0, 6.0, 5.0, 6.0, 7.0, 2.0, 1.0, 3.0, 2.0, 3.0, 5.0, 4.0, 5.0, 6.0, 5.0, 6.0, 5.0, 6.0, 5.0, 2.0, 3.0, 3.0, 3.0, 2.0, 2.0, 1.0, 3.0, 2.0, 4.0, 3.0, 4.0, 6.0, 6.0, 5.0, 4.0, 6.0, 5.0, 3.0, 2.0, 3.0, 1.0, 3.0, 3.0, 2.0, 2.0, 4.0, 3.0, 5.0, 5.0, 4.0, 5.0, 7.0, 6.0, 7.0, 9.0, 8.0, 2.0])

    def test_meanThemeDepth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.meanThemeDepth, 3.7890625)        

    def test_medianThemeDepth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.medianThemeDepth,4.0)        

    def test_maxThemeDepth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.maxThemeDepth,12.0)

    def test_minThemeDepth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.minThemeDepth,1.0)

    def test_stdevThemeDepth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdevThemeDepth,1.9278668895024682)

    def test_weightedSyntacticDepths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.weightedSyntacticDepths,[3.0, 1.0, 3.0, 4.0, 4.0, 4.0, 9.0, 7.0, 5.0, 6.0, 9.0, 9.0, 7.0, 6.0, 9.0, 9.0, 7.0, 2.0, 3.0, 3.0, 3.0, 1.0, 4.0, 2.0, 3.0, 4.0, 8.0, 10.0, 10.0, 8.0, 9.0, 10.0, 8.0, 6.0, 9.0, 7.0, 2.0, 5.0, 5.0, 3.0, 4.0, 7.0, 7.0, 5.0, 1.0, 4.0, 4.0, 4.0, 2.0, 5.0, 3.0, 2.0, 5.0, 3.0, 1.0, 2.0, 3.0, 2.0, 5.0, 3.0, 7.0, 5.0, 6.0, 9.0, 9.0, 9.0, 7.0, 2.0, 3.0, 6.0, 4.0, 3.0, 3.0, 1.0, 2.0, 4.0, 6.0, 4.0, 4.0, 2.0, 3.0, 6.0, 4.0, 8.0, 6.0, 7.0, 8.0, 11.0, 9.0, 3.0, 1.0, 6.0, 4.0, 2.0, 2.0, 3.0, 4.0, 5.0, 3.0, 6.0, 3.0, 3.0, 3.0, 1.0, 2.0, 5.0, 3.0, 7.0, 5.0, 6.0, 8.0, 11.0, 9.0, 2.0, 3.0, 4.0, 7.0, 7.0, 5.0, 3.0, 3.0, 1.0, 2.0, 2.0, 5.0, 3.0, 4.0, 7.0, 7.0, 5.0, 2.0, 1.0, 5.0, 3.0, 1.0, 4.0, 2.0, 5.0, 5.0, 3.0, 3.0, 6.0, 4.0, 5.0, 8.0, 6.0, 7.0, 8.0, 10.0, 8.0, 9.0, 10.0, 2.0, 5.0, 3.0, 1.0, 4.0, 6.0, 6.0, 4.0, 5.0, 6.0, 2.0, 5.0, 3.0, 7.0, 7.0, 7.0, 5.0, 6.0, 8.0, 6.0, 9.0, 7.0, 2.0, 3.0, 4.0, 5.0, 8.0, 6.0, 3.0, 3.0, 3.0, 1.0, 4.0, 4.0, 7.0, 5.0, 6.0, 5.0, 6.0, 6.0, 7.0, 5.0, 4.0, 6.0, 6.0, 4.0, 4.0, 2.0, 5.0, 3.0, 6.0, 4.0, 5.0, 6.0, 7.0, 8.0, 6.0, 7.0, 6.0, 2.0, 5.0, 5.0, 3.0, 3.0, 1.0, 2.0, 3.0, 8.0, 6.0, 4.0, 2.0, 1.0, 3.0, 3.0, 5.0, 3.0, 4.0, 5.0, 3.0, 3.0, 3.0, 1.0, 4.0, 2.0, 6.0, 4.0, 7.0, 7.0, 5.0, 2.0, 5.0, 5.0, 3.0, 1.0, 6.0, 4.0, 2.0, 3.0, 4.0, 2.0, 5.0, 3.0, 4.0, 3.0, 4.0, 3.0, 5.0, 1.0, 4.0, 2.0, 4.0, 4.0, 4.0, 2.0, 5.0, 3.0, 2.0, 5.0, 3.0, 3.0, 3.0, 1.0, 4.0, 2.0, 5.0, 5.0, 5.0, 3.0, 4.0, 5.0, 2.0, 3.0, 4.0, 3.0, 3.0, 1.0, 2.0, 4.0, 4.0, 5.0, 2.0, 5.0, 3.0, 2.0, 2.0, 3.0, 3.0, 1.0, 4.0, 2.0, 6.0, 6.0, 6.0, 4.0, 5.0, 6.0, 2.0, 3.0, 4.0, 3.0, 5.0, 3.0, 4.0, 5.0, 3.0, 1.0, 4.0, 2.0, 3.0, 6.0, 4.0, 3.0, 6.0, 6.0, 4.0, 2.0, 3.0, 4.0, 7.0, 5.0, 6.0, 9.0, 7.0, 3.0, 5.0, 3.0, 1.0, 4.0, 2.0, 3.0, 4.0, 7.0, 7.0, 8.0, 8.0, 9.0, 7.0, 5.0, 2.0, 3.0, 3.0, 4.0, 5.0, 3.0, 1.0, 4.0, 4.0, 2.0, 6.0, 4.0, 5.0, 5.0, 6.0, 7.0, 5.0, 5.0, 10.0, 8.0, 8.0, 6.0, 9.0, 7.0, 10.0, 8.0, 9.0, 2.0, 3.0, 4.0, 7.0, 7.0, 5.0, 1.0, 4.0, 4.0, 2.0, 3.0, 6.0, 4.0, 5.0, 4.0, 2.0, 1.0, 3.0, 4.0, 5.0, 8.0, 6.0, 3.0, 3.0, 3.0, 3.0, 1.0, 4.0, 4.0, 2.0, 5.0, 5.0, 3.0, 2.0, 1.0, 4.0, 6.0, 6.0, 4.0, 5.0, 6.0, 4.0, 5.0, 8.0, 6.0, 4.0, 2.0, 3.0, 6.0, 6.0, 4.0, 5.0, 6.0, 2.0, 3.0, 4.0, 7.0, 7.0, 7.0, 5.0, 6.0, 9.0, 7.0, 4.0, 1.0, 2.0, 8.0, 6.0, 4.0, 2.0, 2.0, 5.0, 7.0, 5.0, 5.0, 3.0, 2.0, 5.0, 3.0, 1.0, 2.0, 3.0, 4.0, 6.0, 6.0, 6.0, 4.0, 5.0, 6.0, 9.0, 9.0, 7.0, 2.0, 3.0, 6.0, 6.0, 4.0, 3.0, 3.0, 3.0, 1.0, 2.0, 5.0, 7.0, 5.0, 3.0, 2.0, 5.0, 3.0, 4.0, 5.0, 6.0, 9.0, 7.0, 8.0, 11.0, 11.0, 13.0, 11.0, 9.0, 4.0, 1.0, 4.0, 2.0, 3.0, 10.0, 8.0, 6.0, 4.0, 2.0, 5.0, 5.0, 3.0, 4.0, 5.0, 6.0, 5.0, 3.0, 1.0, 2.0, 2.0, 4.0, 2.0, 3.0, 6.0, 4.0, 3.0, 6.0, 4.0, 2.0, 1.0, 5.0, 5.0, 3.0, 1.0, 4.0, 4.0, 2.0, 3.0, 3.0, 3.0, 3.0, 1.0, 2.0, 2.0, 5.0, 3.0, 4.0, 5.0, 2.0, 3.0, 4.0, 7.0, 5.0, 6.0, 7.0, 3.0, 6.0, 3.0, 3.0, 3.0, 3.0, 1.0, 2.0, 1.0, 4.0, 6.0, 6.0, 6.0, 4.0, 2.0, 5.0, 5.0, 3.0, 4.0, 5.0, 2.0, 5.0, 3.0, 3.0, 1.0, 4.0, 4.0, 2.0, 2.0, 5.0, 3.0, 2.0, 2.0, 3.0, 1.0, 4.0, 2.0, 3.0, 4.0, 3.0, 7.0, 5.0, 3.0, 1.0, 4.0, 2.0, 5.0, 3.0, 4.0, 5.0, 6.0, 2.0, 3.0, 4.0, 3.0, 6.0, 3.0, 3.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 1.0, 2.0, 1.0, 2.0, 1.0, 3.0, 3.0, 3.0, 1.0, 4.0, 4.0, 2.0, 2.0, 2.0, 5.0, 3.0, 4.0, 5.0, 4.0, 7.0, 5.0, 6.0, 7.0, 2.0, 3.0, 6.0, 4.0, 5.0, 8.0, 8.0, 6.0, 3.0, 3.0, 3.0, 1.0, 4.0, 2.0, 3.0, 6.0, 4.0, 5.0, 6.0, 5.0, 7.0, 5.0, 6.0, 5.0, 2.0, 4.0, 4.0, 4.0, 2.0, 2.0, 3.0, 1.0, 4.0, 2.0, 6.0, 4.0, 5.0, 8.0, 8.0, 6.0, 5.0, 8.0, 6.0, 3.0, 2.0, 3.0, 1.0, 4.0, 4.0, 2.0, 2.0, 5.0, 3.0, 7.0, 7.0, 5.0, 6.0, 9.0, 7.0, 8.0, 11.0, 9.0, 2.0]
)

    def test_meanWeightedDepth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.meanWeightedDepth, 4.396306818181818)        

    def test_medianWeightedDepth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.medianWeightedDepth,4.0)        

    def test_maxThemeDepth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.maxWeightedDepth,13.0)

    def test_minWeightedDepth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.minWeightedDepth,1.0)

    def test_stdevWeightedDepth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdevWeightedDepth,2.2282392942379143)

    def test_weightedSyntacticBreadths(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.weightedSyntacticBreadths,[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 3.0, 3.0, 3.0, 3.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 2.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 3.0, 2.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0])

    def test_meanWeightedBreadth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.meanWeightedBreadth, 1.2954545454545454)        

    def test_medianWeightedBreadth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.medianWeightedBreadth,1.0)        

    def test_maxThemeBreadth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.maxWeightedBreadth,3.0)

    def test_minWeightedBreadth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.minWeightedBreadth,1.0)

    def test_stdevWeightedBreadth(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.stdevWeightedBreadth,0.5011302368540628)

    def test_syntacticProfile(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        profile = {'DET': 87, 'DET:Definite=Def': 47, 'DET:PronType=Art': 64, 'DET-det-NOUN': 74, 'NOUN': 187, 'NOUN:Number=Sing': 132, 'NOUN-ROOT-NOUN': 1, 'VERB': 83, 'VERB:Aspect=Prog': 12, 'VERB:Tense=Pres': 36, 'VERB:VerbForm=Part': 30, 'VERB-acl-NOUN': 4, 'NOUN-dobj-VERB': 36, 'ADV': 28, 'ADV-advmod-VERB': 21, 'ADP': 86, 'ADP-prep-VERB': 31, 'ADJ': 66, 'ADJ:Degree=Pos': 64, 'ADJ-amod-NOUN': 58, 'NOUN-compound-VERB': 1, 'VERB:Number=Sing': 16, 'VERB:Person=Three': 16, 'VERB:VerbForm=Fin': 27, 'VERB-pobj-ADP': 1, 'NOUN-pobj-ADP': 70, 'PUNCT': 69, 'PUNCT:PunctType=Peri': 35, 'PUNCT-punct-NOUN': 10, 'PRON': 11, 'PRON:AdvType=Ex': 3, 'PRON-expl-VERB': 2, 'AUX': 31, 'AUX-HAVE:Mood=Ind': 7, 'AUX-HAVE:Number=Sing': 6, 'AUX-HAVE:Person=3': 6, 'AUX-HAVE:Tense=Pres': 7, 'AUX-HAVE:VerbForm=Fin': 8, 'AUX-aux-VERB': 23, 'VERB:Tense=Past': 21, 'VERB-ROOT-VERB': 31, 'NOUN-attr-VERB': 3, 'ADP-prep-NOUN': 40, 'NOUN:Number=Plur': 55, 'NOUN-nsubj-VERB': 35, 'VERB:Aspect=Perf': 16, 'VERB-relcl-NOUN': 11, 'ADV:Degree=Cmp': 3, 'ADV-advmod-ADV': 2, 'PUNCT-punct-VERB': 51, 'DET:Definite=Ind': 17, 'VERB-ccomp-VERB': 7, 'ADJ:Degree=Sup': 2, 'DET-nsubj-VERB': 8, 'NOUN-compound-NOUN': 16, 'ADP-prep-AUX': 1, 'PUNCT:PunctType=Comm': 31, 'PUNCT-punct-AUX': 4, 'NOUN-nsubj-AUX': 2, 'AUX-BE:Mood=Ind': 6, 'AUX-BE:Tense=Pres': 5, 'AUX-BE:VerbForm=Fin': 9, 'AUX-ROOT-AUX': 3, 'ADJ-acomp-AUX': 1, 'SCONJ': 6, 'SCONJ-mark-VERB': 3, 'AUX-MODAL:VerbForm=Fin': 11, 'VERB:VerbForm=Inf': 26, 'VERB-ccomp-AUX': 2, 'VERB:Mood=Ind': 2, 'NUM': 2, 'NUM:NumType=Card': 2, 'NUM-nummod-NOUN': 1, 'NOUN-npadvmod-ADJ': 1, 'ADJ-acomp-VERB': 3, 'SCONJ-prep-VERB': 2, 'VERB-pcomp-SCONJ': 1, 'NOUN-nsubjpass-VERB': 4, 'AUX-BE:VerbForm=Inf': 2, 'AUX-auxpass-VERB': 5, 'ADP-prep-DET': 1, 'DET:Number=Plur': 3, 'DET:PronType=Dem': 9, 'AUX-HAVE:VerbForm=Inf': 1, 'SPACE': 5, 'SPACE-ROOT-SPACE': 5, 'PART': 18, 'PART-aux-VERB': 13, 'VERB-xcomp-VERB': 5, 'PRON:Case=Acc': 4, 'PRON:Number=Plur': 5, 'PRON:Person=3': 4, 'PRON:PronType=Prs': 8, 'PRON:Reflex=Yes': 3, 'PRON-pobj-ADP': 2, 'AUX-BE:Number=Sing': 5, 'AUX-BE:Person=3': 5, 'VERB-amod-NOUN': 4, 'ADP-mark-VERB': 4, 'VERB-advcl-VERB': 5, 'ADP-prep-ADV': 1, 'PRON-nsubj-VERB': 4, 'NOUN-conj-NOUN': 10, 'CCONJ': 14, 'CCONJ:ConjType=Cmp': 14, 'CCONJ-cc-NOUN': 7, 'NOUN-nmod-NOUN': 2, 'DET:Number=Sing': 6, 'DET-det-VERB': 1, 'VERB-pcomp-ADP': 4, 'NOUN-nsubj-ADJ': 1, 'ADJ-ccomp-VERB': 1, 'PART-neg-VERB': 4, 'SCONJ-det-NOUN': 1, 'DET-appos-NOUN': 1, 'VERB-advcl-NOUN': 1, 'PART-preconj-VERB': 1, 'ADV-advmod-PART': 1, 'CCONJ-cc-VERB': 4, 'PRON:Gender=Neut': 1, 'PRON:Number=Sing': 2, 'VERB-conj-VERB': 4, 'AUX-BE:Tense=Past': 4, 'ADP-prep-ADJ': 3, 'PUNCT:PunctType=Dash': 3, 'ADJ-amod-ADP': 1, 'PRON:Case=Nom': 1, 'PRON:Person=1': 3, 'PROPN': 11, 'PROPN:NounType=Prop': 11, 'PROPN:Number=Sing': 10, 'PROPN-nsubj-VERB': 2, 'PUNCT-punct-PROPN': 4, 'NOUN-appos-PROPN': 1, 'VERB-compound-NOUN': 1, 'ADV-advmod-ADJ': 2, 'DET-nsubjpass-VERB': 1, 'ADP-prt-VERB': 2, 'ADP-prep-ADP': 1, 'ADV:Degree=Sup': 1, 'PROPN-compound-PROPN': 6, 'NUM-appos-PROPN': 1, 'ADP-prep-NUM': 1, 'DET-det-PROPN': 1, 'PROPN:Number=Plur': 1, 'PROPN-pobj-ADP': 3, 'PRON:Gender=Masc': 1, 'PRON:Poss=Yes': 2, 'PRON-poss-NOUN': 2, 'ADJ-advmod-VERB': 1, 'NOUN-npadvmod-VERB': 1, 'AUX-HAVE:Tense=Past': 1, 'NOUN-pobj-SCONJ': 1, 'ADV-advmod-ADP': 1, 'ADP-conj-VERB': 1, 'VERB-prep-VERB': 1, 'NOUN-pobj-VERB': 1, 'CCONJ-preconj-ADJ': 1, 'CCONJ-cc-ADJ': 1, 'ADJ-conj-ADJ': 1, 'PRON-expl-AUX': 1, 'NOUN-attr-AUX': 1, 'CCONJ-cc-AUX': 1, 'ADV-advmod-CCONJ': 1, 'VERB-conj-AUX': 1, 'DET-dobj-VERB': 1}
        self.assertEqual(doc._.syntacticProfile,profile)       

    def test_syntacticProfileNormed(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        profileKeys = ["DET", "DET:Definite=Def", "DET:PronType=Art", "DET-det-NOUN", "NOUN", "NOUN:Number=Sing", "NOUN-ROOT-NOUN", "VERB", "VERB:Aspect=Prog", "VERB:Tense=Pres", "VERB:VerbForm=Part", "VERB-acl-NOUN", "NOUN-dobj-VERB", "ADV", "ADV-advmod-VERB", "ADP", "ADP-prep-VERB", "ADJ", "ADJ:Degree=Pos", "ADJ-amod-NOUN", "NOUN-compound-VERB", "VERB:Number=Sing", "VERB:Person=Three", "VERB:VerbForm=Fin", "VERB-pobj-ADP", "NOUN-pobj-ADP", "PUNCT", "PUNCT:PunctType=Peri", "PUNCT-punct-NOUN", "PRON", "PRON:AdvType=Ex", "PRON-expl-VERB", "AUX", "AUX-HAVE:Mood=Ind", "AUX-HAVE:Number=Sing", "AUX-HAVE:Person=3", "AUX-HAVE:Tense=Pres", "AUX-HAVE:VerbForm=Fin", "AUX-aux-VERB", "VERB:Tense=Past", "VERB-ROOT-VERB", "NOUN-attr-VERB", "ADP-prep-NOUN", "NOUN:Number=Plur", "NOUN-nsubj-VERB", "VERB:Aspect=Perf", "VERB-relcl-NOUN", "ADV:Degree=Cmp", "ADV-advmod-ADV", "PUNCT-punct-VERB", "DET:Definite=Ind", "VERB-ccomp-VERB", "ADJ:Degree=Sup", "DET-nsubj-VERB", "NOUN-compound-NOUN", "ADP-prep-AUX", "PUNCT:PunctType=Comm", "PUNCT-punct-AUX", "NOUN-nsubj-AUX", "AUX-BE:Mood=Ind", "AUX-BE:Tense=Pres", "AUX-BE:VerbForm=Fin", "AUX-ROOT-AUX", "ADJ-acomp-AUX", "SCONJ", "SCONJ-mark-VERB", "AUX-MODAL:VerbForm=Fin", "VERB:VerbForm=Inf", "VERB-ccomp-AUX", "VERB:Mood=Ind", "NUM", "NUM:NumType=Card", "NUM-nummod-NOUN", "NOUN-npadvmod-ADJ", "ADJ-acomp-VERB", "SCONJ-prep-VERB", "VERB-pcomp-SCONJ", "NOUN-nsubjpass-VERB", "AUX-BE:VerbForm=Inf", "AUX-auxpass-VERB", "ADP-prep-DET", "DET:Number=Plur", "DET:PronType=Dem", "AUX-HAVE:VerbForm=Inf", "SPACE", "SPACE-ROOT-SPACE", "PART", "PART-aux-VERB", "VERB-xcomp-VERB", "PRON:Case=Acc", "PRON:Number=Plur", "PRON:Person=3", "PRON:PronType=Prs", "PRON:Reflex=Yes", "PRON-pobj-ADP", "AUX-BE:Number=Sing", "AUX-BE:Person=3", "VERB-amod-NOUN", "ADP-mark-VERB", "VERB-advcl-VERB", "ADP-prep-ADV", "PRON-nsubj-VERB", "NOUN-conj-NOUN", "CCONJ", "CCONJ:ConjType=Cmp", "CCONJ-cc-NOUN", "NOUN-nmod-NOUN", "DET:Number=Sing", "DET-det-VERB", "VERB-pcomp-ADP", "NOUN-nsubj-ADJ", "ADJ-ccomp-VERB", "PART-neg-VERB", "SCONJ-det-NOUN", "DET-appos-NOUN", "VERB-advcl-NOUN", "PART-preconj-VERB", "ADV-advmod-PART", "CCONJ-cc-VERB", "PRON:Gender=Neut", "PRON:Number=Sing", "VERB-conj-VERB", "AUX-BE:Tense=Past", "ADP-prep-ADJ", "PUNCT:PunctType=Dash", "ADJ-amod-ADP", "PRON:Case=Nom", "PRON:Person=1", "PROPN", "PROPN:NounType=Prop", "PROPN:Number=Sing", "PROPN-nsubj-VERB", "PUNCT-punct-PROPN", "NOUN-appos-PROPN", "VERB-compound-NOUN", "ADV-advmod-ADJ", "DET-nsubjpass-VERB", "ADP-prt-VERB", "ADP-prep-ADP", "ADV:Degree=Sup", "PROPN-compound-PROPN", "NUM-appos-PROPN", "ADP-prep-NUM", "DET-det-PROPN", "PROPN:Number=Plur", "PROPN-pobj-ADP", "PRON:Gender=Masc", "PRON:Poss=Yes", "PRON-poss-NOUN", "ADJ-advmod-VERB", "NOUN-npadvmod-VERB", "AUX-HAVE:Tense=Past", "NOUN-pobj-SCONJ", "ADV-advmod-ADP", "ADP-conj-VERB", "VERB-prep-VERB", "NOUN-pobj-VERB", "CCONJ-preconj-ADJ", "CCONJ-cc-ADJ", "ADJ-conj-ADJ", "PRON-expl-AUX", "NOUN-attr-AUX", "CCONJ-cc-AUX", "ADV-advmod-CCONJ", "VERB-conj-AUX", "DET-dobj-VERB"]
        profileValues = [3.09925344619497e-05, 2.381496723060509e-06, 2.41457377537718e-06, 2.4145737852235797e-06, 0.11735102960330836, 0.11116866395711206, 0.0, 0.00017147603326440953, 9.851703401206693e-48, 0.00017147603314620065, 9.849051554685282e-30, 1.1815680504058217e-13, 3.9691612051008487e-07, 4.134542921980051e-09, 2.4435812228337238e-37, 0.01954851587711853, 0.0010299973586000103, 0.03909478256501433, 0.03909478256501433, 0.03909478256501433, 0.0, 0.00017146776406035664, 0.00017146776406035664, 0.00017147603314620065, 0.0, 0.1172934767658147, 0.3333333337927271, 0.3333333333333335, 4.593936580007611e-10, 4.732176569994638e-16, 4.688762106061444e-16, 1.2764370813621152e-25, 1.4066286318184332e-15, 5.8040282073865776e-92, 5.8040282073865776e-92, 5.8040282073865776e-92, 5.8040282073865776e-92, 2.3280915961880366e-61, 3.829311244087161e-25, 9.849051554685282e-30, 1.148793373226393e-24, 6.892760239355422e-24, 0.018518518518518517, 0.006182365646196301, 5.7155921353452216e-05, 9.849051554685282e-30, 0.00017146776406035664, 6.698926527397922e-124, 3.2501140186783067e-212, 1.5701564460093798e-16, 3.307705231667064e-08, 7.484862384863807e-66, 8.734690622853727e-82, 1.1225891916973421e-166, 4.433267234396991e-46, 4.851788436633592e-307, 4.593936587243355e-10, 0.3333333333333333, 1.0590767086750296e-265, 1.4066286314355018e-15, 1.4066286314355018e-15, 1.4066286314355018e-15, 1.4066286314355018e-15, 5.239931511564289e-304, 1.676225949255387e-58, 2.6143003211493685e-251, 3.829311244087161e-25, 1.1820890239845076e-13, 1.6013239835166486e-261, 2.2451783833946842e-166, 1.6532327314692685e-105, 1.6532327314692685e-105, 5.280643683436529e-296, 1.5841931050309616e-295, 2.2451783833946796e-165, 1.676225949255387e-58, 8.554642767167195e-294, 1.4377083358550976e-42, 2.5668252348641306e-70, 4.313125007565294e-42, 2.4246868836405845e-284, 1.5909064603328717e-157, 1.9400763301566974e-62, 5.2373236686636635e-282, 1.357377546321659e-38, 1.357377546321659e-38, 5.910445119865099e-14, 5.910445119865099e-14, 5.0677486631721614e-51, 4.3414463933194504e-18, 4.3414463933194504e-18, 2.925349027818391e-99, 4.3414463933194504e-18, 3.0326232454090583e-197, 2.547506970211642e-205, 1.4066286314355018e-15, 1.4066286314355018e-15, 1.4582104935001615e-113, 2.1707231966597252e-18, 5.20973567198334e-17, 1.3448046919491484e-254, 4.3414463933194504e-18, 1.9346760691288593e-92, 1.3781809740826803e-09, 1.3781809740826803e-09, 6.448920230429531e-93, 1.5088211535070855e-174, 1.9400763301566974e-62, 5.67057122245849e-237, 2.934373894356469e-75, 4.536456977966786e-234, 1.3609370933900368e-233, 1.1225891916973398e-165, 1.990775690600671e-221, 1.2539020133789764e-215, 4.2458449503527365e-206, 1.0399942455192024e-200, 2.079988491038405e-200, 3.0211824752344495e-40, 3.032623219933992e-197, 2.925349027818391e-99, 9.65246255162702e-40, 4.313125007565294e-42, 5.473168556225941e-49, 1.2473258505716168e-167, 4.9102051244841656e-160, 3.4630570810808796e-148, 4.3414463933194504e-18, 5.429958589420526e-86, 5.429958589420526e-86, 5.4299585894205086e-86, 1.3776939428910577e-106, 2.4377963672910956e-100, 5.3178238576737615e-130, 3.101354873795335e-126, 4.2521417990464783e-109, 2.109679533420373e-118, 7.979879754977418e-44, 3.375487253472596e-116, 4.2521417990464746e-109, 1.0859917178841042e-86, 1.6532327314692685e-105, 4.959698194407805e-105, 2.3806551333157466e-103, 6.094477141288311e-101, 4.343966871536417e-86, 2.925349027818391e-99, 1.4670926125195077e-74, 1.4670926125195077e-74, 2.0314098725853017e-90, 5.484806655980314e-89, 2.3280915961880366e-61, 1.0057355695532315e-57, 2.715486037793725e-56, 5.43097207558745e-56, 9.849051553720027e-30, 1.9698103107440057e-28, 8.93301727020463e-21, 8.039715543184167e-20, 2.41191466295525e-19, 4.688762104785006e-16, 1.969280084009703e-14, 1.3781809739933503e-09, 4.134542921980051e-09, 8.269085843960102e-09, 2.8577960676726108e-05]
        self.assertEqual(list(doc._.syntacticProfileNormed.keys()),profileKeys)
        self.assertEqual(list(doc._.syntacticProfileNormed.values()),profileValues)       

    def test_syntacticVariety(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.syntacticVariety,166)

    def test_pastTenseScope(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        pastTenseScope = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.assertEqual(doc._.pastTenseScope,pastTenseScope)

    def test_propn_past(self):
        doc = holmes_manager.get_document('GRE_Sample_Essay')
        self.assertEqual(doc._.propn_past,0.3338068181818182)

    doc = holmes_manager.get_document('GRE_Sample_Essay')
    print(doc._.pastTenseScope)
    print(doc._.propn_past)
    print(doc._.transition_word_type_count)
    print(doc._.total_transition_words)

