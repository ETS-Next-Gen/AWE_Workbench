#!/usr/bin/env bash

# AWE Workbench Install Script (for conda)
# Author: Caleb Scott

# This script installs all necessary dependencies for AWE for python 3.11.
# We make the following assumptions:
# * You have a working conda environment running on python 3.11.
# * You are cd'd into the AWE_Workbench project directory.
# * You have pip installed in the conda environment.

# Sanity Check: let the user know the preconditions.

echo "========================= WARNING ==========================="
echo "\nYou are about to install AWE on this system."
echo "\nYou must have the following conditions met:"
echo "\n* You are currently using a python3.11 conda environment"
echo "\n* You are currently in the AWE_Workbench/installation dir" 
echo "\n* All other repos have been downloaded:"
echo "\n  > holmes-extractor-expandable"
echo "\n  > AWE_LanguageTool"
echo "\n  > AWE_SpellCorrect"
echo "\n  > AWE_Lexica"
echo "\n  > AWE_Components"
echo "\n============================================================="

read -p "\n\n Continue [Y/N]? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    # Install repositories
    
    CODE_REPOS_LOC="../../"
    echo "\n\n Installing from Source..."

    pip install -e "$CODE_REPOS_LOC/holmes-extractor-expandable/"
    pip install -e "$CODE_REPOS_LOC/AWE_LanguageTool/"
    pip install -e "$CODE_REPOS_LOC/AWE_SpellCorrect/"
    pip install -e "$CODE_REPOS_LOC/AWE_Lexica/"
    pip install -e "$CODE_REPOS_LOC/AWE_Components/"
    pip install -e "$CODE_REPOS_LOC/AWE_Workbench/"

    # Patch: protobuf==3.20.0
    # Data does not properly install without this patch.
    pip install protobuf==3.20.0

    # Install data
    echo "\n\n Installing data..."

    python -m awe_workbench.setup.data --develop
fi

# Optional: prompt user input to install the proper java version?
# Source; https://askubuntu.com/questions/1279677/how-to-install-openjdk-14-jdk-on-ubuntu-16-04
