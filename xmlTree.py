#!/usr/bin/python3
__author__ = 'Jakub Pelikan'

class XmlTree:
    """
    XmlDataTypes implement valid data types for XML. And check correct value.
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    def __init__(self):
        self.tag = None
        self.attribute = None
        self.child = []
        self.text = None
        self.parent = None

    ## Method create new tree node
    def createChild(self):
        newChild = XmlTree()
        self.child.append(newChild)
        return newChild

    ## Method print tree structure in text form
    def printTree(self):
        print(self.returnChildTree())

    ## Method return tree structure in text form
    def returnChildTree(self):
        line = []
        if self.child != []:
            for x in self.child:
                line.append(x.returnChildTree())
            return (" TAG: "+str(self.tag)+" ATTRIB: "+str(self.attribute)+" TEXT: "+str(self.text)+" CHILD: "+str(line))
        else:
            return(" TAG: "+str(self.tag)+" ATTRIB: "+str(self.attribute)+" TEXT: "+str(self.text))