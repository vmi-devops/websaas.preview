from glob import glob
from multiprocessing.connection import wait
from textwrap import wrap
from urllib import request
import websocket
import json

globalORService = None
replayChannel = None
globalBrowserType = None
def getDescription(obj):
    global globalORService
    if globalORService is None:
        raise Exception("please setup context before run")
    return globalORService.getDescription(obj)

def startReplayContext(orService,browser="edge",remoteUrl="ws://10.5.35.22:8826/ws/saas"):
    global globalORService
    global globalBrowserType
    globalORService = orService
    globalBrowserType = browser
    global replayChannel
    ws = websocket.WebSocket()
    ws.connect(remoteUrl)
    replayChannel = ws
    send("startReplay")

def send(desc, waitRecv=True):
    global globalBrowserType
    global replayChannel
    descStr = ""
    if type(desc) == dict:
        wraper = {}
        wraper["type"] = "request"
        wraper["uid"] = 345
        wraper["data"]={}
        wraper["data"]["data"] = desc
        descStr = json.dumps(wraper)
    if type(desc) == str:
        descStr = desc
    protocol = {}
    protocol["browserType"] = globalBrowserType
    protocol["task"] = descStr
    sendData = json.dumps(protocol)
    replayChannel.send(sendData)
    if waitRecv:
        print(replayChannel.recv())



def endReplayContext():
    global globalORService
    send("stopReplay", waitRecv=False)
    globalORService = None