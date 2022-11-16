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


# Parameters:
# ---------------------------------------------
PYTHON_CMD="python"
PIP_CMD="pip"

CODE_REPOS_LOC="../../"


# Argument
# --------------------------------------------
VIRTUAL_ENV="$1"
echo "USING VENV: $VIRTUAL_ENV"


# Activate VENV
# ---------------------------------------------------------
source "$VIRTUAL_ENV/bin/activate"


# Installation
# ----------------------------------------------------------
# 2) Change to Repo Directory and load Holmes Expandable:
#      pip install -e .

echo -e "\n=== Installing Holmes Extractor ==="
"$PIP_CMD" install -e "$CODE_REPOS_LOC/holmes-extractor-expandable/"


# 3) Repeat for Language tool.
echo -e "\n\n=== Installing Language Tool ==="
"$PIP_CMD" install -e "$CODE_REPOS_LOC/AWE_LanguageTool"


# 4) Install Spell Correction
echo -e "\n\n=== Installing Spell Correction ==="
"$PIP_CMD" install -e "$CODE_REPOS_LOC/AWE_SpellCorrect"

# 5) Install Lexica
echo -e "\n\n=== Installing Lexica ==="
"$PIP_CMD" install -e "$CODE_REPOS_LOC/AWE_Lexica"

# 6) Install Componrnts
echo -e "\n\n === Installing AWE Components ==="
"$PIP_CMD" install -e "$CODE_REPOS_LOC/AWE_Components"

# 7) Install AWE_Workbench
echo -e "\n\n=== Installing Workbench ==="
"$PIP_CMD" install -e "$CODE_REPOS_LOC/AWE_Workbench"



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
