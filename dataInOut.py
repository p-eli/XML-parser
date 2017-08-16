#!/usr/bin/python3
__author__ = 'Jakub Pelikan'
from xmlParser.xmlDataTypes import XmlDataTypes
from xmlParser.xmlTree import XmlTree


class DataIn():
    """
    DataIn is class, where are data need for verification XML.
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    xmlDataType = XmlDataTypes()
    ## The constructor
    def __init__(self):
        self.sp = None
        self.validateTree = None
        self.searchTypeName = None
        self.validateValue = None
        self.xmlOutTree = None
        self.tagAttribute = None
        self.tagPrefix = ''

    ## Method get copy of data
    def getCopy(self,validateTree):
        cop = DataIn()
        cop.tagPrefix = self.tagPrefix
        cop.sp = self.sp
        cop.xmlOutTree = self.xmlOutTree
        cop.tagAttribute = self.tagAttribute
        cop.validateTree = validateTree
        cop.searchTypeName = self.searchTypeName
        cop.validateValue = self.validateValue
        return cop

    ## Method set XmlOutTree
    def setXmlOutTree(self):
        self.xmlOutTree = XmlTree()

    ## Method create new child in XmlOutTree
    def newXmlOutTree(self):
        self.xmlOutTree = self.xmlOutTree.createChild()


class DataOut():
    """
    DataOut is class, where is building structure of xml data tree.
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    def __init__(self):
        self.atributValue = {}
        self.textValue = None

    ## Method add
    def addAtributValue(self,key,value):
        self.atributValue[key] = value

    def addTextValue(self,value):
        self.textValue = value

    def new(self):
        return DataOut()