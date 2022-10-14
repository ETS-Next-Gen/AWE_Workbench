import spacy
import awe_components.components.lexicalFeatures

nlp = spacy.load("en_core_web_lg")
nlp.add_pipe('lexicalfeatures')

doc = nlp("Apple is considering acquiring a U.K. startup for $1 billion")  
data = doc.to_bytes()

doc = nlp("Testing another document")
print(doc)
for token in doc:
    print(token.text, token.pos_, token._.is_academic)

print('------------------------')
doc2 = nlp('')
doc2.from_bytes(data)
print(doc2)
for token in doc2:
    print(token.text, token.pos_, token._.is_academic)
    
print('percent academic: ',
      doc2._.AWE_Info(indicator='is_academic', summaryType='percent'))

print(doc2._.AWE_Info(indicator='is_academic'))

