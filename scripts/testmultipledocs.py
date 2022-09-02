import awe_workbench.parser.manager as holmes

holmes_manager = holmes.Manager(
    'en_core_web_trf', perform_coreference_resolution=False, number_of_workers=2)
    
    
    with open(os.path.expanduser('~/code/data/sample_essays.csv'), 'r', newline='', encoding='utf-8', errors='ignore') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            text = row['essay_text']

            holmes_manager.parse_and_register_document(document_text=text)
