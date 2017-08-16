#!/usr/bin/python3
__author__ = 'Jakub Pelikan'
import re


class SourceParser:
    """
    SourceParser class parsing the XML Document.
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    pattern1s = re.compile('^\s*<\/').search
    pattern2 = re.compile('^\s*<\s*\/([^>]*)>')
    pattern3 = re.compile('^\s*<[^>]*>')
    pattern3s = re.compile('^\s*<[^>]*>').search
    pattern4s = re.compile('\/>$').search
    pattern5s = re.compile('<\s*[^\s]*\s[^>]+>').search
    pattern6 = re.compile('<([^>| |\/]*).*>')
    pattern7s = re.compile('^\s*$').search
    pattern8s = re.compile('^[^<]+').search
    pattern9 = re.compile('^[^<]*')
    pattern10 = re.compile('\s+')
    pattern11 = re.compile('<\s?[^\s]*\s')
    pattern12 = re.compile('\s*/?\s*>\s*$')
    pattern13 = re.compile('"\s+([A-Za-z])')
    pattern14 = re.compile('[\'\"]([^\'\"]*)[\'\"]')

    ## The constructor
    # @param source Source XML code.
    def __init__(self, source):
        self.head = None
        self.token = None
        self.source = source

    ## Initialize source parser
    def inicialize(self):
        self.source = re.sub('>\s+<', '><', self.source)
        self.source = re.sub('\n+', ' ', self.source)
        if re.search('^<\?xml[^>]*>', self.source):
            self.head = re.search('^<\?xml[^>]*>', self.source).group(0)
            self.source = re.sub('^<\?xml[^>]*>', '', self.source)
            return True
        else:
            return False

    ## Method get new token
    def getNewToken(self):
        if self.pattern1s(self.source):
            endTag = re.search(self.pattern2 , self.source).group(0)
            self.source = self.source.replace(endTag,'',1)
            endTag = re.sub(self.pattern2, '\\1', endTag)
            self.token = {'startTag': None, 'singleTag':False, 'tagAttribute': None, 'endTag': endTag, 'text': None}
        elif self.pattern3s(self.source):
            startTag = self.pattern3s(self.source).group(0)
            if self.pattern4s(startTag):
                tagSingle = True
            else:
                tagSingle = False
            tagAttribute = None
            if self.pattern5s(startTag):
                tagAttribute = self.parseAttribute(startTag)
            self.source = self.source.replace(startTag,'',1)
            startTag = re.sub(self.pattern6, '\\1', startTag)
            self.token = {'startTag': startTag, 'singleTag':tagSingle, 'tagAttribute': tagAttribute, 'endTag': None, 'text': None}
        elif self.pattern7s(self.source):
            self.token = None
        else:
            text = self.pattern8s(self.source).group(0)
            self.source = self.source.replace(text,'',1)
            self.token = {'startTag': None, 'singleTag':False, 'tagAttribute': None, 'endTag': None, 'text': text}
        return self.token

    ## Method parse attribute
    # @param startTag StartTag is XML start tag with attributes.
    def parseAttribute(self, startTag):
        tagAttribute = {}
        atributes = re.sub(self.pattern10, ' ', startTag)
        atributes = re.sub(self.pattern11, '', atributes)
        atributes = re.sub(self.pattern12, '', atributes)
        atributes = re.sub(self.pattern10, ' ', atributes)
        atributes = re.sub(self.pattern13, '"|||\\1', atributes)
        atributes = atributes.split(r'|||')
        for x in atributes:
            x = x.split('=')
            if len(x) > 1:
                tagAttribute[x[0]] = re.sub(self.pattern14, '\\1', x[1])
        return tagAttribute