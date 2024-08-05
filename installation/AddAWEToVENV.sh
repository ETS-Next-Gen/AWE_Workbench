#!/usr/bin/env bash
#
# Add AWEToVENV
# Collin F. Lynch

# This script takes as argument a specified VENV.  It
# then adds the workbench modules to the VENV through
# the basic install process.  This assumes that it is
# run in the specified install directory, that all of
# the necessary modules are present, and that the venv
# has already been constructed using the script in the
# servermanagement directory.


# Argument
# --------------------------------------------
# This script takes one argument which should be the
# path to the same VENV that we are using for writing
# observer.

VIRTUAL_ENV="$1"
echo "USING VENV: $VIRTUAL_ENV"


# Parameters:
# ---------------------------------------------
PYTHON_CMD="python"
PIP_CMD="pip"

CODE_REPOS_LOC="../../"




# Activate VENV
# ---------------------------------------------------------
source "$VIRTUAL_ENV/bin/activate"


# GPU Installation
# ----------------------------------------------------------
# If we plan to use a GPU then this line must also                                                                                     
# be run.  Comment out the code below if you do                                                                                        
# not want cuda installed or edit it for your                                                                                          
# library version.                                                                                                                     
#                                                                                                                                      
# Note that by default we seem to be unable to rely                                                                                    
# on spacy to pull the right cuda on its own                                                                                           
echo -e "\n=== Installing Spacy CUDA, comment out if not needed. ==="
echo -e "\n    Using CUDA v. 117"                                                                                                     
"$PIP_CMD" install spacy[cuda117]

# If you are using cuda 12.1 as we are on some                                                                                         
# systems then spacy's passthrough install will                                                                                        
# not work.  Therefore you will need a two-step                                                                                        
# process.                                                                                                                             
#echo -e "\n    Using CUDA v. 12.x"
#"$PIP_CMD" install cupy-cuda12x
#"$PIP_CMD" install spacy[cuda12x]


# Package Installation
# ----------------------------------------------------------
echo -e "\n=== Installing Holmes Extractor ==="
"$PIP_CMD" install -e "$CODE_REPOS_LOC/holmes-extractor-expandable/"

echo -e "\n\n=== Installing Language Tool ==="
"$PIP_CMD" install -e "$CODE_REPOS_LOC/AWE_LanguageTool"

echo -e "\n\n=== Installing Spell Correction ==="
"$PIP_CMD" install -e "$CODE_REPOS_LOC/AWE_SpellCorrect"

echo -e "\n\n=== Installing Lexica ==="
"$PIP_CMD" install -e "$CODE_REPOS_LOC/AWE_Lexica"

echo -e "\n\n === Installing AWE Components ==="
"$PIP_CMD" install -e "$CODE_REPOS_LOC/AWE_Components"

echo -e "\n\n=== Installing Workbench ==="
"$PIP_CMD" install -e "$CODE_REPOS_LOC/AWE_Workbench"


# Necessary Datafiles.
# -----------------------------------------------

echo -e "\n\n=== Installing shared data. ==="

# Should be unneeded.
# Install spacy en_core_web_sm
#python -m spacy download en_core_web_sm
# NLK Data.
#python -m nltk.downloader all

# And set up the data.
#python -m awe_workbench.setup.data --install (--develop if installing in development mode)
python -m awe_workbench.setup.data --develop

