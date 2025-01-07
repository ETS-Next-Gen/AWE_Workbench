"""
--- [ Test: startServers.py ] -----------------------------------------------------------

Code for kicking off the parserServer.

Author: Caleb Scott (cwscott3@ncsu.edu)

Copyright 2022, Educational Testing Service

-----------------------------------------------------------------------------------------
"""

# --- [ IMPORTS ] -----------------------------------------------------------------------

from multiprocessing import Process

import awe_languagetool.languagetoolServer
import awe_spellcorrect.spellcorrectServer
import awe_workbench.web.parserServer
import argparse
from awe_workbench.pipeline import pipeline_def

# --- [ CLASSES ] -----------------------------------------------------------------------

def startServers():

    p1 = Process(
        target=awe_languagetool.languagetoolServer.runServer, 
        args=()
    )
    p1.start()

    p2 = Process(
        target=awe_spellcorrect.spellcorrectServer.spellcorrectServer, 
        args=()
    )
    p2.start()

    p3 = Process(
        target=awe_workbench.web.parserServer.parserServer,args=(), 
        kwargs={
            'pipeline_def': pipeline_def
        }
    )
    p3.start()

# --- [ MAIN ] --------------------------------------------------------------------------

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run AWE Workbench server scripts')
    args = parser.parse_args()
    startServers()

# --- [ END ] ---------------------------------------------------------------------------
