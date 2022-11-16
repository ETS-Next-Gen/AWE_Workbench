#!/usr/bin/env bash
#
# AWELanguage Tool, Install Script.
# Collin F. Lynch

# This script provides for the automated installation of the
# now componentized AWE Tool in a virtual env.  When run it
# will carry out the steps serailly.  

# Shared parameters:

PYTHON_CMD="python3.9"
PIP_CMD="pip"

VIRTUAL_ENV_LOC="../../../VirtualENVs"
VIRTUAL_ENV_NAME="AWEWorkbenchVENV39"

CODE_REPOS_LOC="../../"


# ---------------------------------------------------------
# 1) Generate new VirtualEnv:

#     python -m venv ../VirtualENVs/AWEWorkbenchVENV

#    Use this format below to set a version:
   
#     python3.10 -m venv ../VirtualENVs/AWEWorkbenchVENV-3-10

# produce the virtual env.
echo -n "=== generating venv ==="
"$PYTHON_CMD" -m venv "$VIRTUAL_ENV_LOC/$VIRTUAL_ENV_NAME"

# Initialize
echo -e "\n=== Starting venv ==="
source "$VIRTUAL_ENV_LOC/$VIRTUAL_ENV_NAME/bin/activate"

# Update the Pip Version.
pip install --upgrade pip


# ----------------------------------------------------------
# Package Installation.

# 2) Change to Repo Directory and load Holmes Expandable:
#      pip install -e .

echo -e "\n=== Installing Holmes Extractor ==="
pip install -e "$CODE_REPOS_LOC/holmes-extractor-expandable/"


# 3) Repeat for Language tool.
echo -e "\n\n=== Installing Language Tool ==="
pip install -e "$CODE_REPOS_LOC/AWE_LanguageTool"


# 4) Install Spell Correction
echo -e "\n\n=== Installing Spell Correction ==="
pip install -e "$CODE_REPOS_LOC/AWE_SpellCorrect"

# 5) Install Lexica
echo -e "\n\n=== Installing Lexica ==="
pip install -e "$CODE_REPOS_LOC/AWE_Lexica"

# 6) Install Componrnts
echo -e "\n\n === Installing AWE Components ==="
pip install -e "$CODE_REPOS_LOC/AWE_Components"

# 7) Install AWE_Workbench
echo -e "\n\n=== Installing Workbench ==="
pip install -e "$CODE_REPOS_LOC/AWE_Workbench"



# -----------------------------------------------
# Now install the direct support packages.

echo -e "\n\n=== Installing shared data. ==="

# Should be unneeded.
# Install spacy en_core_web_sm
#python -m spacy download en_core_web_sm
# NLK Data.
#python -m nltk.downloader all

# And set up the data.
#python -m awe_workbench.setup.data --install (--develop if installing in development mode)
python -m awe_workbench.setup.data --develop



# # 5) Install Lexica
# echo "=== Installing Lexica ==="
# pip install -e "$CODE_REPOS_LOC/




# Holmes Expandable; then language tool; then spell correct; then lexxica then components; then workbench.
