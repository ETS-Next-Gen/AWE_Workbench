'''
This script replaces Kaggle masks in essays with plausible replacements from
a Transformer model.

We wanted to extract features as well, but we need different virtual
environments to do that.
'''


import json
import re
import sys
from transformers import pipeline
# from example_lib import initialize, extract_features


def kaggle_essays():
    '''
    This will return an iterator of Kaggle essays.

    We don't use `csv.reader` since several of the essays have odd characters,
    and we want to handle unicode decoding to ignore errors.

    Perhaps they're not UTF-8?
    '''
    with open('essays/kaggle-data/training_set_rel3.tsv', "rb") as tsvfile:
        first_row = True
        for row in tsvfile:
            if first_row:
                first_row = False
                continue
            row_split = row.split(b'\t')
            if len(row_split) < 3:
                continue
            text = row_split[2][1: -1].strip()
            yield text.decode('utf-8',
                              errors='ignore').strip().replace('""', '"')


def break_on_at_and_mask(text):
    """
    Convert a text to a list, splitting on every word starting with @
    and replacing the word with <mask>

    E.g. "Hello @MASK How are you" ==> ["Hello", "<mask>", "How are you"]
    """
    return re.split(r'@\w+', text)


def interweave(l1, l2):
    """
    Create a list which is e.g.:

    l1[0], l2[0], l1[1], l2[1], ...

    l1 is one item longer than l2, and the extra item is included at the end
    """
    return [item for pair in zip(l1, l2) for item in pair] + [l1[-1]]


unmasker = pipeline("fill-mask")


def unmasked_essays():
    error = 0
    good = 0
    for essay in kaggle_essays():
        try:
            split = break_on_at_and_mask(essay)
            masked = "<mask>".join(split)
            # print(masked)
            unmasked = unmasker(masked, top_k=1)
            tokens = [d[0]["token_str"] for d in unmasked]
            yield "".join(interweave(split, tokens)), essay
            good = good + 1
        except Exception as e:
            error = error + 1
            print("Error", error, "good", good)

# spellchecker, parser, languagetool = initialize()


count = 0

for unmasked, source in unmasked_essays():
    # [corrected] = spellchecker.send([unmasked])
    count = count + 1
    label = "essay_{n}".format(n=count)
    # features = extract_features(parser, corrected, label)
    print(count, 12979)
    with open("kaggle_processed/{label}.masked".format(label=label),
              "w") as source_essay:
        source_essay.write(source)
    with open("kaggle_processed/{label}.unmasked".format(label=label),
              "w") as unmasked_essay:
        unmasked_essay.write(unmasked)
    # with open("kaggle_processed/{label}.corrected".format(label=label),
    #           "w") as corrected_essay:
    #    corrected_essay.write(corrected)
#    with open("kaggle_processed/{label}.json".format(label=label),
#              "w") as features_fp:
#        json.dump(features, features_fp, indent=2)
