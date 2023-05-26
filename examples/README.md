Usage to run the examples

TO RUN THE ARGUMENT_ANALYSIS AND NARRATIVE_ANALYSIS EXAMPLES:

START THE SERVERS
python -m awe_workbench.web.startServers &
python -m awe_components.wordprobs.wordseqProbabilityServer &

THEN 
streamlit run multiple_essay_report.py

TO RUN THE PROCESS_ONE_ARGUMENT_ESSAY AND PROCESS_ONE_NARRATIVE EXAMPLES

python -m awe_workbench.web.startServers --fastpipe

cd to examples directory

python process_one_argument_essay.py OR python process_one_narrative.py

