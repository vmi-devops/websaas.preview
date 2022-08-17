from .testObjectBase import TestObject
from .webbutton import WebButton, WebEdit, WebRange

class Page(TestObject):
    def __init__(self, name):
        super().__init__("Page", name)
    
    def WebButton(self, name):
        b = WebButton(name)
        b.parent = self
        return b
    
    def WebEdit(self, name):
        e = WebEdit(name)
        e.parent = self
        return e
        
    def WebRange(self, name):
        r = WebRange(name)
        r.parent = self
        return r
