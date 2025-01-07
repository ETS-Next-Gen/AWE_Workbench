"""
--- [ Test: startServers.py ] -----------------------------------------------------------

Code for kicking off the parserServer.

Author: Caleb Scott (cwscott3@ncsu.edu)

Copyright 2022, Educational Testing Service

-----------------------------------------------------------------------------------------
"""

# --- [ IMPORTS ] -----------------------------------------------------------------------

import json
from websocket import create_connection

# --- [ CLASSES ] -----------------------------------------------------------------------

class websocketClient:

    def __init__(self):
        self.uri = "ws://localhost:8765"

    def set_uri(self, uri):
        self.uri = uri

    def send(self, texts: list):
        if texts is None:
            print('no texts!')
            return None
        try:
            ws = create_connection(self.uri)
            ws.send(json.dumps(texts))
            result = ws.recv()
            ws.close()
            return json.loads(result)
        except Exception as e:
            print(e)
            return None

    def sendraw(self, texts: list):
        if texts is None:
            return None
        try:
            ws = create_connection(self.uri)
            ws.send(json.dumps(texts))
            result = ws.recv()
            ws.close()
            return result
        except Exception as e:
            print(e)
            return None

# --- [ MAIN ] --------------------------------------------------------------------------

if __name__ == '__main__':
    wsc = websocketClient()
    test = wsc.check(['The grrls are happpy.'])
    print(test)

# --- [ END ] ---------------------------------------------------------------------------
