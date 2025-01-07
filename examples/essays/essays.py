"""
--- [ Test: essays.py ] -----------------------------------------------------------------

Code for retrieving an essay from the set of all essays, using the filename.

Author: Caleb Scott (cwscott3@ncsu.edu)

-----------------------------------------------------------------------------------------
"""

import os
import re

def get_essay(essay_name: str) -> str:
    """
    Given :essay_name:, return the string of the entire essay.
    """
    target = os.path.join(os.path.dirname(__file__), essay_name)
    with open(target, 'r') as in_file:
        raw = in_file.read().replace('\n', ' ')
        return re.sub(' +', ' ', raw)
