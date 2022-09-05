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

doc = "In society today, people take things in very many different ways. So things that might help one person, may offend other.\n      In libraries, there are different kinds of books; fiction, non fiction..(etc). So if you dont like a particular book, maybe you should try looking in a different area. I do not think books should be removed from the shelf because the book has offened a few people.\n      We are blessed to live in America, where we have freedom of speech. So authors have freedom to write what they would like to. They work long hard hours getting a book ready to be published and then someone wants to take it off the shelf becasue it offened a few people? I do not think that is right.\n     'One man's junk is another man's treasure.' I think this quote goes along with this topic very well, because the book may not mean something to one person but it may mean the word to someone else.\n      You never know what people may need to hear. Maybe an alcoholic is at a point in his/her life and is ready to change, and someone has a book about a recovering alcoholic. Now, this kind of book may offend a few people, but it may save a family, a friendship or maybe even a life.\n      Take Alice Walker for intance, her journal is now a book. Now this may offend a few people that might have been thereor maybe don't like The Color Purple, but her story has the right to be told. Yes, there is violence in it, and i understand that maybe you don't want your 8 year old to hear about how they use to treat African-American women, but the story has the right to be told, and should be told.\n      I do not think that the librarian has the right to take a book off the shelf at the library, just because it has offened a few. There are lots of different kinds of books, if the books you are reading offend you, look for a different type of book"

#doc = "In our society today there is always going to be something that someone disagrees with or dislikes.  Items should not be removed from the shelves just because someone takes offense to it.  Everyone has a book or movie out there that they disagree with, but if it is removed just for that reason then there would be a very limited selection left.  Students would take advantage of this and they would have educational books removed.\n     Removing items from shelves removes history.  Our history books tell us stories of slavery and descrimination.  If someone takes offense to this and has it removed then we are losing a part of our history that needs to be heard and taught so that it does not occur again.  Items in the library are items that you can choose to check out or choose to not check out.  If you take offense to an item in the library then you do not have to read it.  Something that you may take as offensive may be something that inspires and encourages someone else.  Wether you like an item or dislike it is a matter of your own personal opinion and decisions should not be made based on someones opinion alone.\n    Think about it.  If you have a favorite book, movie, or song then would you want it to be gotten rid of based on someones opinion?  You have the right to be able to read,watch, or listen to whatever you want.  It should not be limited based on someone elses opinion.  It would cause much argument among people.  Some have different opinions then others on a certain item in the library which will lead to argument and possible violence.\n     There are so many wonderful and inspiring books and movies out there and there is always going to be someone who does not like at least one of them.  If items are removed based on someones opinion then there will be a very limited selection left.  People read for enjoyment and knowledge.  They deserve to have a wide selction to choose from.\n     In our society today there is always going to be something that someone disagrees with or dislikes.  Our opinions should not be based on a person's dislike of something.  If they take offense to it then they have the right to ignore it.  There are so many books and movies out there that teach us of life before our generation.  We need these books and movies so that there are not repeat events of all of the rough times our ancestors had to go through.  We need these books for future generations so that we are able to teach and guide them.  Items should not be removed from the shelves ba,sed on the fact that someone takes offense to it."

#doc = "Practice What You Preach\n     The U.S. is considered one of the greatest countries in the world because it is a free country. In the 1800's people migrated here to escape the control that their government had in their homeland. In America we practice freedom of speech. If we censor materials like books, music, movies, etc. it would defeat the entire purpose of America and it's Constitution.\n     Everyone has their own personality with likes and dislikes. Not everyone likes the same music or is interested in reading the same subject, thats why its wonderful that their is a variety of everything. If you start banning or censoring certain things then how will people learn? There is nothing wrong with learning about negative things because that teaches people lessons so they know What or What not to do if in that situation. When you censor 'bad things' it creates naive thinkers, which only leads to discrimination.\n      I agree that for children there should warnings for material that parents may find offensive. For example, movies have ratings for different age groups, and books could do the same. Of course its up to the parents if they want to follow the recommendations but banning something all together is not neccessary.\n     I personally learned a lot of things from Shows I've seen on television. Whats on television may be considered 'street smart' education but that is good. Today we live in a scary and violent society, so being 'street smart' is an advantage. If television was censored then people would not know what to do in a bad situation because they have never experienced or seen of it before.\n     If books, movies, magazines, music, etc. are removed from shelves then America is not practicing What it preaches to the many of people who come here in search of freedom."

parser.parse_and_register_document(doc, 'temp')
out = parser.get_document('temp')
print_parse_tree(out)
print(out)
