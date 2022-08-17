import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time
import json
import base64
from websocket import create_connection
import time

ws = create_connection("ws://10.5.35.22:8826/ws/saas")
startReplay = {
    "browserType": "edge",
    "task": "startReplay"
}
stopReplay = {
    "browserType": "edge",
    "task": "stopReplay"
}
startReplayStr = json.dumps(startReplay)
startTime = time.time()
ws.send(startReplayStr)
result = ws.recv()
endTime = time.time()
print("------%s seconds-------" % (endTime - startTime))
print("Received '%s'" % result)

time.sleep(10)
stopReplayStr = json.dumps(stopReplay)
startTime = time.time()
ws.send(stopReplayStr)
result = ws.recv()
endTime = time.time()
print("------%s seconds-------" % (endTime - startTime))
print("Received '%s'" % result)

ws.close()