import json
import io

def convertToFastRunDescription(uftObjDescription):
    allDesc = {}
    fastDesc = {}
    allDesc["Description properties"] = fastDesc
    propertys = uftObjDescription['Properties']['Property']
    def _queryValueFromProps(propName):
        for prop in propertys:
            if prop["@Name"] == k:
                if "#text" not in prop["Value"]:
                    return None
                value = prop["Value"]["#text"]
                valueType = prop["@Type"]
                if valueType == "NUMBER":
                    value = int(value)
                elif valueType == "I2":
                    value = int(value)
                elif valueType == "BOOL":
                    value = value.lower() in ("yes", "true", "1")
                return value
        return None
    if "BasicIdentification" in uftObjDescription:
        mandatoryDesc = {}
        if "PropertyRef" in uftObjDescription["BasicIdentification"]:
            mandatory = uftObjDescription["BasicIdentification"]["PropertyRef"]
            if type(mandatory) == str:
                mandatory = [mandatory]
            if type(mandatory) == list:
                for k in mandatory:
                    for prop in propertys:
                        if prop["@Name"] == k:
                            value = prop["Value"]["#text"]
                            valueType = prop["@Type"]
                            if valueType == "NUMBER":
                                value = int(value)
                            elif valueType == "I2":
                                value = int(value)
                            elif valueType == "BOOL":
                                value = value.lower() in ("yes", "true", "1")
                            mandatoryDesc[k] = value
                            break
        if "OrdinalIdentifier" in uftObjDescription["BasicIdentification"]:
            ordinalDesc = {}
            ordinalObj = uftObjDescription["BasicIdentification"]["OrdinalIdentifier"]
            ordinalDesc[ordinalObj["@Type"]] = int(ordinalObj["Value"])
            fastDesc["ordinal"] = ordinalDesc
        fastDesc["mandatory"] = mandatoryDesc
    if "SmartIdentification" in uftObjDescription:
        smartDesc = {}
        if "BaseFilter" in uftObjDescription["SmartIdentification"]:
            baseProps = uftObjDescription["SmartIdentification"]["BaseFilter"]
            if "PropertyRef" in baseProps:
                smartDesc["Base"] = []
                basePropsRef = baseProps["PropertyRef"]
                if type(basePropsRef) == str:
                    basePropsRef = [basePropsRef]
                if type(basePropsRef) == list:
                    for k in basePropsRef:
                        propValue = _queryValueFromProps(k)
                        if propValue is None:
                            continue
                        tempValue = {}
                        tempValue["compareType"] = 0
                        tempValue["name"] = k
                        tempValue["value"] = propValue
                        smartDesc["Base"].append(tempValue)

        if "OptionalFilter" in uftObjDescription["SmartIdentification"]:
            optionalProps = uftObjDescription["SmartIdentification"]["OptionalFilter"]
            if "PropertyRef" in optionalProps:
                smartDesc["Optional"] = []
                optionalProps = optionalProps["PropertyRef"]
                if type(optionalProps) == str:
                    optionalProps = [optionalProps]
                if type(optionalProps) == list:
                    for k in optionalProps:
                        #print(k)
                        propValue = _queryValueFromProps(k)
                        if propValue is None:
                            continue
                        tempValue = {}
                        tempValue["compareType"] = 0
                        tempValue["name"] = k
                        tempValue["value"] = propValue
                        smartDesc["Optional"].append(tempValue)
        fastDesc["smart identification"] = smartDesc
                        
    allDesc["name"] = uftObjDescription["@Name"]
    allDesc["class"] = uftObjDescription["@ObjectClass"]
    return allDesc
                            
   
def _parseOrFile(childObj):
    #print("func call")
    if childObj is None:
        return None
    if "Objects" in childObj:
        if "Object" in childObj["Objects"]:
            allObject = childObj["Objects"]["Object"]
            AllDesc = {}
            AllDesc["testObject"] = []
            if type(allObject) == dict:
                allObject = [allObject]
            if type(allObject) == list:
                for obj in allObject:
                    #print("try here")
                    desc = _parseOrFile(obj)
                    #print(3, desc)
                    AllDesc["testObject"].append(desc)
            #print(AllDesc)
            return AllDesc
    if "ChildObjects" in childObj:
        #print("childObj in here")
        if type(childObj["ChildObjects"]) != dict:
            #print("it is not dict")
            desc = convertToFastRunDescription(childObj)
            #print("1",desc)
            return desc
        if "Object" in childObj["ChildObjects"]:
            allObject = childObj["ChildObjects"]["Object"]
            AllDesc = {}
            AllDesc["child"] = []
            if type(allObject) == dict:
                allObject = [allObject]
            if type(allObject) == list:
                for obj in allObject:
                    desc = _parseOrFile(obj)
                    AllDesc["child"].append(desc)
            thisDesc = convertToFastRunDescription(childObj)
            #print(thisDesc)
            thisDesc["child"] = AllDesc["child"]
            #print(2, thisDesc)
            return thisDesc

class Adapter:
    def __init__(self):
        self._orPath = []
        self._parsedOR = []

    def addORPath(self, path):
        self._orPath.append(path)
        with io.open(path, 'r', encoding='utf8') as f:
            orFileData = f.read()
            y = json.loads(orFileData)
            ret = _parseOrFile(y)
            print(ret)
            self._parsedOR.append(ret)
    
    def parseORFiles(self):
        for p in self._orPath:
            with io.open(p, 'r', encoding='utf8') as f:
                orFileData = f.read()
                y = json.loads(orFileData)
                ret = _parseOrFile(y)
                self._parsedOR.append(ret)
    
    @property
    def parsedOR(self):
        return self._parsedOR



class OR:
    def __init__(self):
        self._orPath=[]
        self._adapter = Adapter()
        pass

    def imports(self, path):
        self._orPath.append(path)
        self._adapter.addORPath(path=path)
        
    '''
    testObject interface:
    class testObject:
        def __init__(self):
            self.className=xxx
            self.objectName=yyy
            pass
        @property
        def parent(self):
            pass
        @property.setter
        def parent(self, _parent):
            pass
    '''    
    def getDescription(self, testObject):
        if testObject.parent is not None:
            formatToDesc, toHirchyDesc = self.getDescription(testObject=testObject.parent)
            if formatToDesc is None and toHirchyDesc is None:
                return None, None
            if "child" in toHirchyDesc:
                for eachTODesc in toHirchyDesc["child"]:
                    if eachTODesc["class"] == testObject.className and \
                        eachTODesc["name"] == testObject.objectName:
                        formatDesc = {}
                        formatDesc ["Description properties"] = eachTODesc["Description properties"]
                        # if "ordinal" in eachTODesc:
                        #     formatDesc["ordinal"] = eachTODesc["ordinal"]
                        # if "mandatory" in eachTODesc:
                        #     formatDesc["mandatory"] = eachTODesc["mandatory"]
                        # if "smart identification" in eachTODesc:
                        #     formatDesc["smart identification"] = eachTODesc["smart identification"]
                        lastChildDesc = formatToDesc
                        while True:
                            if "child" in lastChildDesc:
                                lastChildDesc = lastChildDesc["child"]
                            else:
                                lastChildDesc["child"] = formatDesc
                                return formatToDesc, eachTODesc
                            
        else:
            for orDescription in self._adapter.parsedOR:
                if "testObject" in orDescription:
                    for eachTODesc in orDescription["testObject"]:
                        if eachTODesc["class"] == testObject.className and \
                            eachTODesc["name"] == testObject.objectName:
                            formatDesc = {}
                            formatDesc["Description properties"] = eachTODesc["Description properties"]
                            # if "ordinal" in eachTODesc:
                            #     formatDesc["ordinal"] = eachTODesc["ordinal"]
                            # if "mandatory" in eachTODesc:
                            #     formatDesc["mandatory"] = eachTODesc["mandatory"]
                            # if "smart identification" in eachTODesc:
                            #     formatDesc["smart identification"] = eachTODesc["smart identification"]
                            return formatDesc, eachTODesc
            return None, None