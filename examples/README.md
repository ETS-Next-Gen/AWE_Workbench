Usage to run the examples

TO RUN THE ARGUMENT_ANALYSIS AND NARRATIVE_ANALYSIS EXAMPLES:

START THE SERVERS
python -m awe_workbench.web.startServers
python -m awe_workbench.wordprob.wordseqProbabilityServer

THEN EITHER
streamlit run argument_analysis.py OR streamlit run narrative_analysis.py

TO RUN THE PROCESS_ONE_ARGUMENT_ESSAY AND PROCESS_ONE_NARRATIVE EXAMPLES

python -m awe_workbench.web.startServers --fastpipe

cd to examples directory

python process_one_argument_essay.py OR python process_one_narrative.py

