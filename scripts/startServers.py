from multiprocessing import Process, Queue

import os
import awe_workbench.languagetool.languagetoolServer
import awe_workbench.spellcorrect.spellcorrectServer
import awe_workbench.web.parserServer

def runLT(q, x):
    q.put(x+100)

if __name__ == '__main__':
    queue = Queue()
    p1 = Process(target=awe_workbench.languagetool.languagetoolServer.runServer, args=())
    p1.start()

    p2 = Process(target=awe_workbench.spellcorrect.spellcorrectServer.spellcorrectServer, args=())
    p2.start()

    p3 = Process(target=awe_workbench.web.parserServer.parserServer, args=())
    p3.start()

