import awe_workbench.parser.manager as holmes
import os
import csv

holmes_manager = holmes.Manager(
    'en_core_web_trf', perform_coreference_resolution=False, number_of_workers=2)
    
    
with open(os.path.expanduser('~/code/data/scores_and_crs.csv'), 'r', newline='', encoding='utf-8', errors='ignore') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        ID = row['essay_id']
        text = row['essay_text']

        holmes_manager.parse_and_register_document(text,ID)
        print('.')
        holmes_manager.remove_document(ID)
         
