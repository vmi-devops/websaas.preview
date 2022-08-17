from .context import getDescription
from .testObjectBase import TestObject
from .page import Page
from .context import getDescription, send

class Browser(TestObject):
    def __init__(self, name):
        super().__init__("Browser", name)

    def Page(self, name):
        p = Page(name)
        p.parent = self
        return p
    
    def Navigate(self, url):
        desc, _ = getDescription(self)
        action = {}
        action["method"] = "Navigate"
        action["unnamedArguments"] = [url]
        protocol = {}
        protocol["action"] = action
        protocol["testObject"] = desc
        protocol["version"] = 1
        send(protocol)
    
    def Close(self):
        desc, _ = getDescription(self)
        action = {}
        action["method"] = "Close"
        action["unnamedArguments"] = []
        protocol = {}
        protocol["action"] = action
        protocol["testObject"] = desc
        protocol["version"] = 1
        send(protocol)