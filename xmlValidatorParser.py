#!/usr/bin/python3
__author__ = 'Jakub Pelikan'
from xmlParser.xmlElement import Element
from xmlParser.sourceParser import  SourceParser
from xmlParser.tree import Tree
from xmlParser.xmlTree import XmlTree
from xmlParser.dataInOut import DataIn,DataOut
import re

class XmlValidatorParser():
    """
    Class XmlValidatorParser, Validate and parsing XSD and then validate, parsing and made xml tree from XML file.
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param xmlFile Xml File data.
    # @param xsdFile Xsd File data.
    def __init__(self,xmlFile, xsdFile):
        self.xmlFile = xmlFile
        self.xsdFile = xsdFile
        self.rulesTree = None
        self.root = None
        self.prefix = re.compile('^.{3}:')
        self.parseRules()
        self.parseXml()

    ## Method parse, validate and make XSD tree.
    def parseRules(self):
        stack = Stack()
        sp = SourceParser(self.xsdFile)
        sp.inicialize()
        self.rulesTree = Tree()
        treeItem = self.rulesTree
        elements = Element()
        item = sp.getNewToken()
        if item['tagAttribute'] != None:
            for x in item['tagAttribute']:
                if re.search('^xmlns:.{3}',x):
                    self.prefix = re.compile(re.sub('^xmlns:(.{3})','\\1:',x))
        item['tagAttribute'] = None
        while item != None:
            if item['startTag'] != None:
                item['startTag'] = re.sub(self.prefix,'',item['startTag'])
                treeItem.elementType = item['startTag']
                el = elements.getElementClass(item)
                treeItem.elClass = el
                parent = None
                if not stack.isEmpty():
                    treeItem.parent = stack.top()
                    stack.top().setChild(treeItem)
                    parent = stack.top().elementType
                if not el.checkParent(parent):
                    raise ValueError("XSD ELEMENT PARENT IS NOT VALID")
                if item['tagAttribute'] != None:
                    el.checkAttributes(item['tagAttribute'])
                    treeItem.attributes = item['tagAttribute']
                if not item['singleTag']:
                    treeItem.singleTag = False
                    stack.push(treeItem)
            elif item['endTag'] != None:
                item['endTag'] = re.sub(self.prefix,'',item['endTag'])
                if stack.isEmpty():
                    raise SyntaxError("XSD SYNTAX ERROR")
                if (stack.pop().elementType != item['endTag']):
                    raise SyntaxError("XSD SYNTAX ERROR")
            elif item['text']:
                stack.top().textComments = item['text']
            treeItem = Tree()
            item = sp.getNewToken()
        if not stack.isEmpty():
            raise SyntaxError("XSD SYNTAX ERROR")
        return True

    ## Method parse, validate and make XML tree.
    def parseXml(self):
        IN = DataIn()
        OUT = DataOut()
        IN.sp = SourceParser(self.xmlFile)
        IN.sp.inicialize()
        IN.setXmlOutTree()
        IN.xmlTree = XmlTree()
        IN.validateTree = self.rulesTree
        IN.sp.getNewToken()
        try:
            IN.validateTree.elClass.run(IN,OUT)
            self.root = IN.xmlOutTree.child[0]
        except ValueError:
            raise ValueError("XML VALIDATE ERROR") from ValueError
        except SyntaxWarning:
            raise SyntaxWarning("XML SYNTAX ERROR") from SyntaxWarning
        except SyntaxError:
            raise SyntaxError("XML SYNTAX ERROR") from SyntaxError


class Stack:
    """
    Class Stack, implement stack for XSD parser.
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    def __init__(self):
        self.storage = []

    ## Method return True if is stack empty, else return False.
    def isEmpty(self):
        return len(self.storage) == 0

    ## Method push object on stack
    # @param object Object is object to push.
    def push(self, object):
        self.storage.append(object)

    ## Method return and remove object on stack top.
    def pop(self):
        return self.storage.pop()

    ## Method return object on stack top.
    def top(self):
        if len(self.storage) == 0:
            return None
        return self.storage[len(self.storage) - 1]




