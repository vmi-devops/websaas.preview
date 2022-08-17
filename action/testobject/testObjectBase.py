class TestObject:
    def __init__(self, testObjClass, name):
        self._className = testObjClass
        self._objectName = name
        self._parent = None
    @property
    def className(self):
        return self._className
    
    @property
    def objectName(self):
        return self._objectName
    @property
    def parent(self):
        return self._parent
    
    @parent.setter
    def parent(self, parentObj):
        self._parent = parentObj