# Copyright 2021 Educational Testing Service
import awe_workbench
import holmes_extractor
import holmes_extractor.manager
import holmes_extractor.ontology
from holmes_extractor.manager import Manager
from holmes_extractor.ontology import Ontology
from awe_workbench_components.components.utility_functions \
    import print_parse_tree

pipeline_def = [('spacytextblob',
                 'spacytextblob',
                 'spacytextblob'),
                ('awe_workbench_components.components',
                 'lexicalFeatures',
                 'lexicalfeatures'),
                ('awe_workbench_components.components',
                 'syntaxDiscourseFeats',
                 'syntaxdiscoursefeatures'),
                ('awe_workbench_components.components',
                 'viewpointFeatures',
                 'viewpointfeatures'),
                ('awe_workbench_components.components',
                 'lexicalClusters',
                 'lexicalclusters'),
                ('awe_workbench_components.components',
                 'contentSegmentation',
                 'contentsegmentation')]

parser = holmes_extractor.manager.Manager(
            model='en_core_web_lg',
            perform_coreference_resolution=True,
            extra_components=pipeline_def
       )

doc = "Practice What You Preach\n     The U.S. is considered one of the greatest countries in the world because it is a free country. In the 1800's people migrated here to escape the control that their government had in their homeland. In America we practice freedom of speech. If we censor materials like books, music, movies, etc. it would defeat the entire purpose of America and it's Constitution.\n     Everyone has their own personality with likes and dislikes. Not everyone likes the same music or is interested in reading the same subject, thats why its wonderful that their is a variety of everything. If you start banning or censoring certain things then how will people learn? There is nothing wrong with learning about negative things because that teaches people lessons so they know What or What not to do if in that situation. When you censor 'bad things' it creates naive thinkers, which only leads to discrimination.\n      I agree that for children there should warnings for material that parents may find offensive. For example, movies have ratings for different age groups, and books could do the same. Of course its up to the parents if they want to follow the recommendations but banning something all together is not neccessary.\n     I personally learned a lot of things from Shows I've seen on television. Whats on television may be considered 'street smart' education but that is good. Today we live in a scary and violent society, so being 'street smart' is an advantage. If television was censored then people would not know what to do in a bad situation because they have never experienced or seen of it before.\n     If books, movies, magazines, music, etc. are removed from shelves then America is not practicing What it preaches to the many of people who come here in search of freedom."

parser.parse_and_register_document(doc, 'temp')
out = parser.get_document('temp')
print_parse_tree(out)
print(out)
