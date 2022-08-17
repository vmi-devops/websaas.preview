from codecs import getdecoder
from .testObjectBase import TestObject
from .context import getDescription, send

class WebButton(TestObject):
    def __init__(self, name):
        super().__init__("WebButton", name)
    
    def Click(self):
        desc, _ = getDescription(self)
        action = {}
        action["method"] = "Click"
        action["unnamedArguments"] = []
        protocol = {}
        protocol["action"] = action
        protocol["testObject"] = desc
        protocol["version"] = 1
        send(protocol)
        print(protocol)

class WebEdit(TestObject):
    def __init__(self, name):
        super().__init__("WebEdit", name)
    
    def Set(self, value):
        desc, _ = getDescription(self)
        action = {}
        action["method"] = "Set"
        action["unnamedArguments"] = [value]
        protocol = {}
        protocol["action"] = action
        protocol["testObject"] = desc
        protocol["version"] = 1
        send(protocol)
        print(protocol)

class WebRange(TestObject):
    def __init__(self, name):
        super().__init__("WebRange", name)
    
    def Set(self, value):
        desc, _ = getDescription(self)
        action = {}
        action["method"] = "Set"
        action["unnamedArguments"] = [value]
        protocol = {}
        protocol["action"] = action
        protocol["testObject"] = desc
        protocol["version"] = 1
        send(protocol)
        print(protocol)