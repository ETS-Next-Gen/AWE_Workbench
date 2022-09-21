#!/usr/bin/env python3.10
# Copyright 2022, Educational Testing Service

import awe_workbench
import holmes_extractor
import holmes_extractor.manager
import holmes_extractor.ontology
from holmes_extractor.manager import Manager
from holmes_extractor.ontology import Ontology
from awe_components.components.utility_functions \
    import print_parse_tree
from awe_workbench.pipeline import pipeline_def
import argparse

parser = argparse.ArgumentParser(description="Parse a student text file")
parser.add_argument(
    '--filename',
    default="essays/leprechaun.txt",
    help='Which file to parse'
)

args = parser.parse_args()
doc = open(args.filename).read()

manager = holmes_extractor.manager.Manager(
            model='en_core_web_lg',
            perform_coreference_resolution=True,
            extra_components=pipeline_def
       )

manager.parse_and_register_document(doc, 'temp')
out = manager.get_document('temp')
print_parse_tree(out)
print(out._.vwp_statements_of_fact)
