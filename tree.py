#!/usr/bin/python3
__author__ = 'Jakub Pelikan'

class Tree:
    """
    Class Tree, building XML three from XML document.
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    def __init__(self):
        self.attributes = None
        self.parent = None
        self.child = []
        self.elementType = None
        self.textComments = None
        self.elClass= None
        self.singleTag = True
        self.tag = None

    ## Method append child to child list
    # @param child Append child.
    def setChild(self, child):
        self.child.append(child)

    ## Method return value of specific attribute
    # @param attribute Specific attribute name.
    def getAttribute(self, attribute):
        if self.attributes != None:
            if attribute in self.attributes:
                return self.attributes[attribute]
        return None

    ## Method remove child.
    # @param remChild RemChild is child which is remove.
    def removeChild(self, remChild):
        self.child.remove(remChild)