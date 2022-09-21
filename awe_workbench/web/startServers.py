#!/usr/bin/env python3.10
# Copyright 2022, Educational Testing Service

from multiprocessing import Process, Queue

import os
import time

import awe_languagetool.languagetoolServer
import awe_spellcorrect.spellcorrectServer
import awe_workbench.web.parserServer
import argparse
from awe_workbench.pipeline import pipeline_def


class startServers:

    # Initialize
    p1 = None
    p2 = None
    p3 = None
    queue = None

    def __init__(self):
        queue = Queue()

        p1 = \
            Process(target=awe_languagetool.languagetoolServer.runServer,
                    args=())
        p1.start()

        p2 = \
            Process(target=awe_spellcorrect.spellcorrectServer.spellcorrectServer,
                    args=())
        p2.start()

        p3 = Process(target=awe_workbench.web.parserServer.parserServer,
                     args=(),
                     kwargs={'pipeline_def': pipeline_def})
        p3.start()


if __name__ == '__main__':

    parser = \
       argparse.ArgumentParser(description='Run AWE Workbench server scripts')

    args = parser.parse_args()

    startServers()
