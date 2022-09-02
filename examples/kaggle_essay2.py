'''
This script takes unmasked essays and extracts Paul's features from them
'''

import json
import re
import sys
import os.path
import os
from example_lib import initialize, extract_features


def unmasked_kaggle_essays():
    '''
    Returns an iterator. Each element of the iterator is the text of
    a file. The files come from all the files in the directory
    # 'kaggle_processed' and ending in .unmasked
    '''
    for filename in os.listdir('kaggle_processed'):
        if filename.endswith('.unmasked'):
            with open(os.path.join('kaggle_processed',
                      filename), 'r') as f:
                yield f.read(), filename.replace(".unmasked", "")


spellchecker, parser, languagetool = initialize()

count = 0
errors = 0

for essay, label in unmasked_kaggle_essays():
    count = count + 1
    [corrected] = spellchecker.send([essay])
    # print(label)
    # print(essay)
    # print(corrected)
    try:
        features = extract_features(parser, corrected, label)
        with open("kaggle_processed/{label}.spellchecked".format(label=label),
                  "w") as corrected_essay:
            corrected_essay.write(corrected)
        with open("kaggle_processed/{label}.json".format(label=label),
                  "w") as features_fp:
            json.dump(features, features_fp, indent=2)
    except Exception as e:
        errors = errors + 1
    print(count, errors)
