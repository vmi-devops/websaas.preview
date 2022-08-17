from tracemalloc import start
from orHub import OR
from testobject import Browser
from testobject import startReplayContext, endReplayContext
import time


def main():
    orService = OR()
    orService.imports("./orRepo/to.json")
    orService.imports("./orRepo/html5testing.json")
    startReplayContext(orService, browser="edge",remoteUrl="ws://preview.vmilabs.com/ws/saas")
    time.sleep(3)
    print("start navigate")
    Browser("HTML5 testing").Navigate("http://mama.swinfra.net/war/HTML5/HTML5%20Tests.html")
    time.sleep(3)
    Browser("HTML5 testing").Page("HTML5 testing").WebEdit("url").Set("kai.zhou@microfocus.com")
    time.sleep(1)
    Browser("HTML5 testing").Page("HTML5 testing").WebEdit("text1").Set("hello, this is my description")
    time.sleep(1)
    Browser("HTML5 testing").Page("HTML5 testing").WebEdit("number").Set("2022")
    time.sleep(1)
    Browser("HTML5 testing").Page("HTML5 testing").WebEdit("fullname").Set("kern")
    time.sleep(1)
    Browser("HTML5 testing").Page("HTML5 testing").WebRange("rangeexample").Set(4.3)
    time.sleep(1)
    Browser("HTML5 testing").Page("HTML5 testing").WebButton("Submit").Click()
    time.sleep(5)
    Browser("HTML5 testing").Close()
    endReplayContext()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("quit the process")