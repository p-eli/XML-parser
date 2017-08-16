#!/usr/bin/python3
__author__ = 'Jakub Pelikan'
import re
import copy


class Element():
    """
    Element class search xml element and return class where is element implemented.
    http://www.w3schools.com/schema/schema_elements_ref.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    def __init__(self):
        self.xmlElements = {'documentation': DocumentationElement,'annotation': AnnotationElement,'restriction': RestrictionElement, 'union': UnionElement, 'list': ListElement, 'simpleType': SimpleTypeElement, 'attributeGroup': AttributeGroupElement, 'attribute':AttributeElement, 'redefine': RedefineElement, 'complexType': ComplexTypeElement, 'field': FieldElement, 'keyref': KeyrefElement, 'key': KeyElement, 'selector': SelectorElement, 'unique': UniqueElement, 'sequence':SequenceElement, 'group': GroupElement, 'all':AllElement, 'simpleContent': SimpleContentElement, 'complexContent': ComplexContentElement, 'extension': ExtensionElement, 'choice': ChoiceElement, 'element': ElementElement, 'schema': SchemaElement, 'any': AnyElement,'anyAttribute': AnyAttributeElement, 'appinfo': AppinfoElement, 'import': ImportElement, 'include': IncludeElement, 'notation': NotationElement, 'enumeration': EnumerationFacets, 'fractionDigits': FractionDigitsFacets, 'length': LengthFacets, 'maxExclusive': MaxExclusiveFacets, 'maxInclusive': MaxInclusiveFacets, 'maxLength': MaxLengthFacets, 'minExclusive': MinExclusiveFacets, 'minInclusive': MinInclusiveFacets, 'minLength':TagAttributeFacets, 'pattern': PatternFacets, 'totalDigits': TotalDigitsFacets, 'whiteSpace': WhiteSpaceFacets}

    ## Return search class
    # @param tag Tag which contains name of search element.
    def getElementClass(self,tag):
        if tag['startTag'] in self.xmlElements:
            return self.xmlElements[tag['startTag']](tag['tagAttribute'])
        raise ValueError


class XmlElement():
    """
    XmlElement contains a general implementation od XML element.
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes.
    def __init__(self,att):
        self.possibleXmlAtribute = {'id' : self.attId, 'attributeFormDefault': self.attAttributeFormDefault,'elementFormDefault':self.attElementFormDefault,'blockDefault':self.attBlockDefault,'finalDefault': self.attFinalDefault, 'targetNamespace': self.attTargetNamespace, 'version': self.attVersion, 'xmlns': self.attXmlns, 'name': self.attName ,  'ref': self.attRef, 'type': self.attType, 'substitutionGroup': self.attSubstitutionGroup, 'default': self.attDefault, 'fixed': self.attFixed, 'form': self.attForm, 'maxOccurs': self.attMaxOccurs, 'minOccurs': self.attMinOccurs, 'nillable': self.attNillable, 'abstract': self.attAbstract, 'block': self.attBlock , 'final': self.attFinal, 'use': self.attUse, 'base': self.attBase, 'mixed': self.attMixed, 'xpath': self.attXpath , 'refer':self.attRefer , 'schemaLocation': self.attSchemaLocation, 'itemType': self.attItemType, 'memberTypes': self.attMemberTypes, 'source': self.attSource, 'xml:lang':self.attXml_lang}
        self.useAttributes = att
        self.possibleAttributes= {}
        self.elementName = "None"
        self.In = None
        self.Out = None
        self.parentElement = []
        #DEFAULT VALUES
        self.maxOccurs = 1
        self.minOccurs = 1

    ## Method search attributes in list possible attributes.
    # @todo add implement using own attributes
    # @param attributes List of element attributes which are check.
    def checkAttributes(self,attributes):
        if attributes != None:
            for x in attributes:
                self.possibleAttributes[x] = attributes[x]
        return True

    ## Method check if element has valid parent.
    # @param parent Parent is element parent.
    def checkParent(self,parent):
        if parent in self.parentElement:
            return True
        return False

    ## Method validate attribute, search attribute in attribute list and invoke attribute method.
    def validateAttributeProcess(self):
        if self.useAttributes != None:
            for x in self.useAttributes:
                self.possibleXmlAtribute[x]()

    ## Method validate element attribute ID
    # @todo Not implemented
    def attId(self): # Specifies a unique ID for the element
        pass

    ## Method validate element attribute Attribute Form Default
    # @todo Not implemented
    def attAttributeFormDefault(self):
        pass

    ## Method validate element attribute Element Form Default
    # @todo Not implemented
    def attElementFormDefault(self):
        pass

    ## Method validate element attribute Block Default
    # @todo Not implemented
    def attBlockDefault(self):
        pass

    ## Method validate element attribute Final Default
    # @todo Not implemented
    def attFinalDefault(self):
        pass

    ## Method validate element attribute Target Namespace
    # @todo Not implemented
    def attTargetNamespace(self):
        pass

    ## Method validate element attribute Version
    # @todo Not implemented
    def attVersion(self):
        pass

    ## Method validate element attribute Xmlns
    # @todo Not implemented
    def attXmlns(self):
        pass

    ## Method validate element attribute Name
    def attName(self): #Specifies a name for the element.
        self.name = self.useAttributes['name']

    ## Method validate element attribute Ref
    def attRef(self):
        validateTreeCopy = self.In.validateTree
        self.In.searchTypeName = self.useAttributes['ref']
        cond = False
        while validateTreeCopy !=None:
            y = 0
            for x in validateTreeCopy.child:
                try:
                    if type(x.elClass) ==  AttributeGroupElement or type(x.elClass) ==  GroupElement:
                        if x.elClass.run(self.In.getCopy(x), self.Out):
                            cond = True
                except ValueError:
                    y += 1
            if validateTreeCopy.parent != None:
                validateTreeCopy.parent.removeChild(validateTreeCopy)
            validateTreeCopy = validateTreeCopy.parent
        if cond:
            return True
        raise ValueError

    ## Method validate element attribute Type
    def attType(self):
        cond = False
        self.In.searchTypeName = self.possibleAttributes['type']
        try:
            self.In.xmlDataType.findType(self.possibleAttributes['type'])
            if self.In.sp.token['text'] != None:
                self.Out.addTextValue(self.In.xmlDataType.validate(self.possibleAttributes['type'], self.In.sp.token['text']))
                self.In.sp.getNewToken()
        except ValueError:
            cond = True
        if cond:
            self.In.searchTypeName = self.possibleAttributes['type']
            self.searchParent()

    ## Method validate element attribute Substitution Group
    # @todo Not implemented
    def attSubstitutionGroup(self):
        pass

    ## Method validate element attribute Default
    # @todo Not implemented
    def attDefault(self):
        pass

    ## Method validate element attribute Fixed
    # @todo Not implemented
    def attFixed(self):
        pass

    ## Method validate element attribute Form
    # @todo Not implemented
    def attForm(self):
        pass

    ## Method validate element attribute Max Occurs
    def attMaxOccurs(self):
        self.maxOccurs = int(self.useAttributes['maxOccurs'])

    ## Method validate element attribute Min Occurs
    def attMinOccurs(self):
        self.minOccurs = int(self.useAttributes['minOccurs'])

    ## Method validate element attribute Nillable
    # @todo Not implemented
    def attNillable(self):
        pass

    ## Method validate element attribute Abstract
    # @todo Not implemented
    def attAbstract(self):
        pass

    ## Method validate element attribute Block
    # @todo Not implemented
    def attBlock(self):
        pass

    ## Method validate element attribute Final
    # @todo Not implemented
    def attFinal(self):
        pass

    ## Method validate element attribute Use
    # @todo Not implemented
    def attUse(self):
        pass

    ## Method validate element attribute Base
    def attBase(self):
        self.base = self.useAttributes['base']
        self.In.searchTypeName = self.possibleAttributes['base']

    ## Method validate element attribute Mixed
    # @todo Not implemented
    def attMixed(self):
        pass

    ## Method validate element attribute Xpath
    # @todo Not implemented
    def attXpath(self):
        pass

    ## Method validate element attribute Refer
    # @todo Not implemented
    def attRefer(self):
        pass

    ## Method validate element attribute Schema Location
    # @todo Not implemented
    def attSchemaLocation(self):
        pass

    ## Method validate element attribute Item Type
    def attItemType(self):
        self.itemType = self.useAttributes['itemType']

    ## Method validate element attribute Member Types
    def attMemberTypes(self):
        data = self.useAttributes['memberTypes']
        self.memberTypes = re.split('\s+',data)

    ## Method validate element attribute Source
    # @todo Not implemented
    def attSource(self):
        pass

    ## Method validate element attribute Xml_lang
    # @todo Not implemented
    def attXml_lang(self):
        pass

    ## Method check if is element searching child element.
    # @param In In is instance of class DataIn
    # @param Out is instance of class DataOut
    def itsYou(self,In,Out):
        if In.sp.token == None:
            raise ReferenceError
        if (self.useAttributes != None) and ("name" in self.useAttributes) and (self.useAttributes["name"] != None):
                if In.sp.token['startTag'] != None:

                    if In.sp.token['startTag'].replace(In.tagPrefix+':', '',1) == self.useAttributes["name"]:
                        return True
                if In.searchTypeName != self.useAttributes["name"]:
                    if ("minOccurs" in self.useAttributes) and (self.useAttributes["minOccurs"] == '0'):
                            return False
                    raise ReferenceError
        return True

    ## Method search child element between parents node in tree.
    def searchParent(self):
        validateTreeCopy = self.In.validateTree
        while validateTreeCopy.parent != None:
            validateTreeCopy = validateTreeCopy.parent
        cond = False
        for x in validateTreeCopy.child:
                try:
                    if type(x.elClass) != type(self) :
                        if x.elClass.run(self.In.getCopy(x), self.Out):
                            cond = True
                except ReferenceError:
                    pass
        if cond:
            return True
        raise ReferenceError

    ## Method search child element between child node in tree.
    def searchChild(self):
        cond = False
        for x in self.In.validateTree.child:
            try:
                if type(x.elClass) != type(self) :
                    if x.elClass.run(self.In.getCopy(x), self.Out):
                        cond = True
            except ReferenceError:
                pass
        if cond:
            return True
        raise ReferenceError

    ## Search element attributes which is define as instance of attribute element.
    def searchTagAttributes(self):
        cond = False
        if self.In.tagAttribute != None:
            if self.In.validateTree.child != []:
                for y in self.In.validateTree.child:
                        try:
                            if type(y.elClass) == AttributeElement or type(y.elClass) == AttributeGroupElement or type(y.elClass) == SimpleContentElement:
                                if y.elClass.run(self.In.getCopy(y), self.Out):
                                    cond = True
                        except ReferenceError:
                            pass
        if self.In.tagAttribute != {} and self.In.tagAttribute != None:
            raise ValueError
        return cond

    ## Method run implemented behavior of element.
    # @param In In is instance of class DataIn
    # @param Out is instance of class DataOut
    def run(self,In,Out):
            stat = self.itsYou(In,Out)
            if stat:
                self.In = In
                self.Out = Out
                stat = self.childProcess()
            return stat

    ## Method implemented behavior of element.
    def childProcess(self):
        pass


class AllElement(XmlElement):
    """
    AllElement is instance of XmlElement.
    AllElement implement XML Schema all Element
    http://www.w3schools.com/schema/el_all.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes.
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "ALL"
        self.useAttributes = att
        self.possibleAttributes = {'id':None, 'maxOccurs':None, 'minOccurs':None}
        self.parentElement = ['group', 'complexType', 'restriction', 'extension']

    ## Method implemented behavior of element.
    def childProcess(self):
        self.validateAttributeProcess()
        if (self.maxOccurs == 1) and ((self.minOccurs == 1) or (self.minOccurs == 0)):
            self.searchChild()
        else:
            raise SyntaxError
        return True

    ## Method search child element between child node in tree.
    def searchChild(self):
        trr = self.In.validateTree
        for y in range(len(trr.child)):
            count = 0
            for x in trr.child:
                try:
                    if type(x.elClass) != type(self) :
                        if not x.elClass.run(self.In.getCopy(x), self.Out):
                            raise ReferenceError
                        trr.removeChild(x)
                        break
                except ReferenceError:
                    count +=1
                    if (count == len(trr.child)) and (self.minOccurs == 1) :
                        raise ValueError from ReferenceError


class AnnotationElement(XmlElement):
    """
    AnnotationElement is instance of XmlElement.
    AnnotationElement implement XML Schema annotation Element.
    Top level element that specifies schema comments.
    http://www.w3schools.com/schema/el_annotation.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes.
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "ANNOTATION"
        self.useAttributes = att
        self.possibleAttributes= {'id':None}
        self.parentElement = ['enumeration','documentation','annotation','restriction','union','list','simpleType','attributeGroup','attribute', 'redefine','complexType','field','keyref','key','selector','unique','group','sequence','all','simpleContent','complexContent','extension','choice','element','schema'] #uplne vsichni

    ## Method implemented behavior of element.
    def childProcess(self):
        self.validateAttributeProcess()
        self.searchChild()
        return True

    ## Method search child element between child node in tree.
    def searchChild(self):
        trr = self.In.validateTree
        for y in range(len(trr.child)):
            count = 0
            for x in trr.child:
                try:
                    if type(x.elClass) != type(self) :
                        if not x.elClass.run(self.In.getCopy(x), self.Out):
                            raise ReferenceError
                        trr.removeChild(x)
                        break
                except ReferenceError:
                    count +=1
                    if (count == len(trr.child)) and (self.minOccurs == 1) :
                        raise ValueError from ReferenceError


class AnyElement(XmlElement):
    """
    AnyElement is instance of XmlElement.
    AnyElement implement XML Schema any Element.
    http://www.w3schools.com/schema/schema_complex_any.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes.
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "ANY"
        self.useAttributes = att
        self.possibleAttributes= {'id':None, 'maxOccurs':None, 'minOccurs':None, 'namespace':None, 'processContents':None}
        self.parentElement = ['choice', 'sequence']

    ## Method implemented behavior of element.
    def childProcess(self):
        self.validateAttributeProcess()
        if (self.maxOccurs >= 0) and (self.minOccurs >= 0):
            return self.searchParent()
        else:
            raise SyntaxError

    ## Method search child element between parents node in tree.
    def searchParent(self):
        count = 0
        cond = True
        validateTreeCopy = self.In.validateTree
        while validateTreeCopy.parent != None:
            validateTreeCopy = validateTreeCopy.parent
        while cond:
                for x in validateTreeCopy.child:
                    try:
                        if type(x.elClass) != type(self) :
                            if x.elClass.run(self.In.getCopy(x), self.Out):
                                count +=1
                                cond = True
                                break
                    except ReferenceError:
                        pass
                if cond:
                    break
        if (count < self.minOccurs) or (count > self.maxOccurs):
            if count != 0:
                raise ValueError
            else:
                raise ReferenceError
        if count == 0:
            return False
        else:
            return True


class AnyAttributeElement(XmlElement):
    """
    AnyAttributeElement is instance of XmlElement.
    AnyAttributeElement implement XML Schema anyAttribute Element.
    Add text comments to schema.
    http://www.w3schools.com/schema/el_anyattribute.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes.
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "ANYATTRIBUTE"
        self.useAttributes = att
        self.possibleAttributes= {'id':None, 'namespace':None,'processContents':None}
        self.parentElement = ['complexType', 'restriction', 'extension', 'attributeGroup']

    ## Method implemented behavior of element.
    # @todo Not implemented
    def childProcess(self):
        return True


class AppinfoElement(XmlElement):
    """
    AppinfoElement is instance of XmlElement.
    AppinfoElement implement XML Schema appinfo Element.
    The attribute element defines an attribute.
    http://www.w3schools.com/schema/el_appinfo.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes.
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "APPINFO"
        self.useAttributes = att
        self.possibleAttributes= {'default':None, 'fixed':None,'form':None,'id':None,'name':None,'ref':None,'type':None,'use':None}
        self.parentElement = ['annotation']

    ## Method implemented behavior of element.
    # @todo Not implemented
    def childProcess(self):
            return True


class AttributeElement(XmlElement):
    """
    AttributeElement is instance of XmlElement.
    AttributeElement implement XML Schema attribute Element.
    Check type of content.
    http://www.w3schools.com/schema/el_attribute.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes.
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "ATTRIBUTE"
        self.useAttributes = att
        self.possibleAttributes = {'default':None, 'fixed':None, 'form':None, 'id':None, 'name':None, 'ref':None, 'type':None, 'use':None}
        self.parentElement = ['attributeGroup', 'schema', 'complexType', 'restriction', 'extension']

    ## Method check if is element searching child element.
    # @param In In is instance of class DataIn
    # @param Out is instance of class DataOut
    def itsYou(self,In,Out):
        if In.tagAttribute == None:
            raise ReferenceError
        if self.useAttributes['name'] in In.tagAttribute:
            return True
        else:
            raise ReferenceError

    ## Method implemented behavior of element.
    def childProcess(self):
        self.In.validateValue = self.In.tagAttribute[self.useAttributes['name']]
        self.validateAttributeProcess()
        del self.In.tagAttribute[self.useAttributes['name']]
        return True

    def attType(self):
        cond = False
        try:
            self.In.xmlDataType.findType(self.possibleAttributes['type'])
            if self.In.tagAttribute[self.useAttributes['name']] != None:
                type = self.In.xmlDataType.validate(self.possibleAttributes['type'], self.In.tagAttribute[self.useAttributes['name']])
                self.Out.addAtributValue(self.useAttributes['name'],type)
        except ValueError:
            cond = True
        if cond:
            self.In.searchTypeName = self.possibleAttributes['type']
            self.searchParent()


class AttributeGroupElement(XmlElement):
    """
    AttributeGroupElement is instance of XmlElement.
    AttributeGroupElement implement XML Schema attributeGroup Element.
    http://www.w3schools.com/schema/el_attributeGroup.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes.
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "ATTRIBUTE GROUP"
        self.useAttributes = att
        self.possibleAttributes= {'id':None, 'name':None ,'ref':None}
        self.parentElement = ['attributeGroup', 'complexType', 'schema', 'restriction', 'extension']

    ## Method check if is element searching child element.
    # @param In In is instance of class DataIn
    # @param Out is instance of class DataOut
    def itsYou(self,In,Out):
        if In.tagAttribute == None:
            raise ReferenceError
        if ('ref' in self.useAttributes):
            return True
        elif('name' in self.useAttributes) and (self.useAttributes['name'] == In.searchTypeName):
            return True
        raise ReferenceError

    ## Method implemented behavior of element.
    def childProcess(self):
        self.validateAttributeProcess()
        if ('ref' in self.useAttributes):
            return True
        cond = self.searchTagAttributes()
        if not cond:
            raise ReferenceError
        return True


class ChoiceElement(XmlElement):
    """
    ChoiceElement is instance of XmlElement.
    ChoiceElement implement XML Schema choice Element.
    http://www.w3schools.com/schema/el_choice.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes.
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "CHOICE"
        self.useAttributes = att
        self.possibleAttributes = {'id':None, 'maxOccurs':None, 'minOccurs':None}
        self.parentElement = ['group', 'choice', 'sequence', 'complexType', 'restriction', 'extension']

    ## Method implemented behavior of element.
    def childProcess(self):
        self.validateAttributeProcess()
        self.searchChild()
        return True

    ## Method search child element between child node in tree.
    def searchChild(self):
        count = 0
        childType = None
        while True:
            cond = False
            for x in range(len(self.In.validateTree.child)):
                try:
                    if type(self.In.validateTree.child[x].elClass) != type(self) :
                        if (childType == None) or (childType == self.In.validateTree.child[x].elClass):
                            stat = self.In.validateTree.child[x].elClass.run(self.In.getCopy(self.In.validateTree.child[x]), self.Out)
                            if stat:
                                childType = self.In.validateTree.child[x].elClass
                                cond = True
                                count +=1
                            else:
                                if count <= self.minOccurs and count < self.minOccurs:
                                    count +=1
                except ReferenceError:
                    pass
            if not cond:
                if count > self.maxOccurs or count < self.minOccurs:
                    raise ValueError
                break


class ComplexContentElement(XmlElement):
    """
    ComplexContentElement is instance of XmlElement.
    ComplexContentElement implement XML Schema complexContent Element.
    http://www.w3schools.com/schema/el_complexcontent.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes.
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "COMPLEX CONTENT"
        self.useAttributes = att
        self.possibleAttributes = {'id':None, 'mixed':None}
        self.parentElement = {'complexType'}

    ## Method implemented behavior of element.
    def childProcess(self):
        self.searchChild()
        return True


class ComplexTypeElement(XmlElement):
    """
    ComplexTypeElement is instance of XmlElement.
    ComplexTypeElement implement XML Schema complexType Element.
    http://www.w3schools.com/schema/el_complextype.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes.
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "COMPLEX TYPE"
        self.useAttributes = att
        self.possibleAttributes= {'id':None, 'name':None, 'abstract':None, 'mixed':None, 'block':None, 'final':None}
        self.parentElement = ['element', 'redefine', 'schema']

    ## Method implemented behavior of element.
    def childProcess(self):
        self.validateAttributeProcess()
        cond = self.searchTagAttributes()
        try:
            self.searchChild()
        except ReferenceError:
            if not cond:
                raise ValueError from ReferenceError
        return True


class DocumentationElement(XmlElement):
    """
    DocumentationElement is instance of XmlElement.
    DocumentationElement implement XML Schema documentation Element.
    http://www.w3schools.com/schema/el_documentation.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "DOCUMENTATION"
        self.useAttributes = att
        self.possibleAttributes= {'source':None, 'xml:lang':None}
        self.parentElement = ['annotation']

    ## Method implemented behavior of element.
    # @todo Not implemented
    def childProcess(self):
        return True


class ElementElement(XmlElement):
    """
    ElementElement is instance of XmlElement.
    ElementElement implement XML Schema element Element.
    http://www.w3schools.com/schema/el_element.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "ELEMENT"
        self.useAttributes = att
        self.possibleAttributes = {'id': None, 'name': None, 'ref': None, 'type': None, 'substitutionGroup': None,
                           'default': None, 'fixed': None, 'form': None, 'maxOccurs': None, 'minOccurs': None,
                           'nillable': None, 'abstract': None, 'block': None, 'final': None}
        self.parentElement = ['schema', 'choice', 'all', 'sequence', 'group']

    ## Method implemented behavior of element.
    def childProcess(self):
            self.In.newXmlOutTree()
            self.Out = self.Out.new()
            token = copy.copy(self.In.sp.token)
            self.In.xmlOutTree.attribute = copy.copy(self.In.sp.token['tagAttribute'])
            if token != None:
                self.In.tagAttribute = self.In.sp.token['tagAttribute']
            if not token['singleTag']:
                self.In.sp.getNewToken()
            self.validateAttributeProcess()
            if not token['singleTag']:
                if self.In.validateTree.child != []:
                    try:
                        self.searchChild()
                    except ReferenceError:
                        pass

                if self.In.sp.token['endTag'] != token['startTag']:
                    raise ValueError
            self.In.sp.getNewToken()
            self.In.xmlOutTree.tag = token['startTag']
            self.In.xmlOutTree.text = self.Out.textValue
            return True


class ExtensionElement(XmlElement):
    """
    ExtensionElement is instance of XmlElement.
    ExtensionElement implement XML Schema extension Element.
    http://www.w3schools.com/schema/el_extension.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "EXTENSION"
        self.useAttributes = att
        self.possibleAttributes = {'id':None, 'base':None}
        self.parentElement = ['simpleContent', 'complexContent']

    ## Method implemented behavior of element.
    def childProcess(self):
        self.validateAttributeProcess()
        self.searchTagAttributes()
        cond = False
        if self.In.sp.token['text'] != None and self.In.searchTypeName != None:
            try:
                self.Out.addTextValue(self.In.xmlDataType.validate(self.In.searchTypeName, self.In.sp.token['text']))
                self.In.sp.getNewToken()
            except ValueError:
                cond = True
            if cond:
                self.searchParent()
                self.searchChild()
        else:
            self.searchParent()
            self.searchChild()
        return True


class FieldElement(XmlElement):
    """
    FieldElement is instance of XmlElement.
    FieldElement implement XML Schema field Element.
    http://www.w3schools.com/schema/el_field.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "FIELD"
        self.useAttributes = att
        self.possibleAttributes= {'id':None, 'xpath':None}
        self.parentElement = ['key', 'keyref', 'unique']

    ## Method implemented behavior of element.
    # @todo Not implemented
    def childProcess(self):
          return True


class GroupElement(XmlElement):
    """
    GroupElement is instance of XmlElement.
    GroupElement implement XML Schema group Element.
    http://www.w3schools.com/schema/el_group.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "GROUP"
        self.useAttributes = att
        self.possibleAttributes = {'id':None, 'name':None, 'ref':None, 'maxOccurs':None, 'minOccurs':None}
        self.parentElement = ['schema', 'choice', 'sequence', 'complexType', 'restriction', 'extension']

    ## Method implemented behavior of element.
    def childProcess(self):
        self.validateAttributeProcess()
        self.searchChild()
        return True


class ImportElement(XmlElement):
    """
    ImportElement is instance of XmlElement.
    ImportElement implement XML Schema import Element.
    http://www.w3schools.com/schema/el_import.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "IMPORT"
        self.useAttributes = att
        self.possibleAttributes= {'id':None, 'namespace':None,'schemaLocation':None}
        self.parentElement = ['schema']

    ## Method implemented behavior of element.
    # @todo Not implemented
    def childProcess(self):
        return True


class IncludeElement(XmlElement):
    """
    IncludeElement is instance of XmlElement.
    IncludeElement implement XML Schema include Element.
    http://www.w3schools.com/schema/el_include.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "INCLUDE"
        self.useAttributes = att
        self.possibleAttributes= {'id':None, 'schemaLocation':None}
        self.parentElement = ['schema']

    ## Method implemented behavior of element.
    # @todo Not implemented
    def childProcess(self):
        return True


class KeyElement(XmlElement):
    """
    KeyElement is instance of XmlElement.
    KeyElement implement XML Schema key Element.
    http://www.w3schools.com/schema/el_key.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "KEY"
        self.useAttributes = att
        self.possibleAttributes= {'id':None, 'name':None}
        self.parentElement = ['element']

    ## Method implemented behavior of element.
    # @todo Not implemented
    def childProcess(self):
          return True


class KeyrefElement(XmlElement):
    """
    KeyrefElement is instance of XmlElement.
    KeyrefElement implement XML Schema keyref Element.
    http://www.w3schools.com/schema/el_keyref.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "KEYREF"
        self.useAttributes = att
        self.possibleAttributes= {'id':None, 'name':None, 'refer':None}
        self.parentElement = ['element']

    ## Method implemented behavior of element.
    # @todo Not implemented
    def childProcess(self):
          return True


class ListElement(XmlElement):
    """
    ListElement is instance of XmlElement.
    ListElement implement XML Schema list Element.
    http://www.w3schools.com/schema/el_list.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "LIST"
        self.useAttributes = att
        self.possibleAttributes= {'id':None, 'itemType':None}
        self.parentElement = ['simpleType']
        self.itemType = None

    ## Method implemented behavior of element.
    def childProcess(self):
        self.validateAttributeProcess()
        if self.itemType != None:
            if self.In.sp.token['text'] != None:
                value = re.split(r'\s+', self.In.sp.token['text'])
                if 'itemType' in self.possibleAttributes:
                    for x in value:
                        self.In.xmlDataType.validate(self.possibleAttributes['itemType'],x)
                self.Out.addTextValue(value)
                self.In.sp.getNewToken()
        return True


class NotationElement(XmlElement):
    """
    NotationElement is instance of XmlElement.
    NotationElement implement XML Schema notation Element.
    http://www.w3schools.com/schema/el_notation.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "NOTATION"
        self.useAttributes = att
        self.possibleAttributes= {'id':None, 'name':None,'public':None, 'system':None}
        self.parentElement = ['schema']

    ## Method implemented behavior of element.
    # @todo Not implemented
    def childProcess(self):
        return True


class RedefineElement(XmlElement):
    """
    RedefineElement is instance of XmlElement.
    RedefineElement implement XML Schema redefine Element.
    http://www.w3schools.com/schema/el_redefine.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "REDEFINE"
        self.useAttributes = att
        self.possibleAttributes= {'id':None, 'schemaLocation':None}
        self.parentElement = ['schema']

    ## Method implemented behavior of element.
    # @todo Not implemented
    def childProcess(self):
          return True


class RestrictionElement(XmlElement): # defines restrictions
    """
    RestrictionElement is instance of XmlElement.
    RestrictionElement implement XML Schema restriction Element.
    http://www.w3schools.com/schema/el_restriction.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "RESTRICTION"
        self.useAttributes = att
        self.possibleAttributes= {'id':None, 'base':None}
        self.parentElement = ['simpleType', 'simpleContent', 'complexContent']
        self.base = None

    ## Method implemented behavior of element.
    def childProcess(self):
        self.validateAttributeProcess()
        if self.base != None:
            if self.In.validateValue != None:
                data = [self.In.validateValue]
            else:
                data = self.In.sp.token['text']
                self.Out.addTextValue(data)
                self.In.sp.getNewToken()
            if data != None and data != []:
                for x in data:
                    self.In.xmlDataType.validate(self.base, x)
            else:
                return False
        return True

    def attType(self):
        cond = False
        try:
            if self.useAttributes['name'] in self.In.tagAttribute:
                data = self.In.tagAttribute[self.useAttributes['name']]
                self.In.xmlDataType.findType(self.possibleAttributes['type'])
                if data != None:
                    type = self.In.xmlDataType.validate(self.possibleAttributes['type'], data)
                    self.Out.addAtributValue(self.useAttributes['name'],type)
            else:
                self.In.xmlDataType.findType(self.possibleAttributes['type'])
                if self.In.sp.token['text'] != None:
                    self.Out.addTextValue(self.In.xmlDataType.validate(self.possibleAttributes['type'], self.In.sp.token['text']))
                    self.In.sp.getNewToken()
        except ValueError:
            cond = True
        if cond:
            self.In.searchTypeName = self.possibleAttributes['type']
            self.searchParent()


class SchemaElement(XmlElement):
    """
    SchemaElement is instance of XmlElement.
    SchemaElement implement XML Schema Schema Element.
    http://www.w3schools.com/schema/el_schema.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes
    def __init__(self, att):
        super().__init__(att)
        self.elementName = "SCHEMA"
        self.useAttributes = att
        self.possibleAttributes = {'id': None, 'attributeFormDefault': None, 'elementFormDefault': None, 'blockDefault': None,'finalDefault': None, 'targetNamespace': None, 'version': None, 'xmlns': None}
        self.parentElement = [None]

    ## Method check if element has valid parent.
    # @param parent Parent is element parent.
    def checkParent(self,parent):
        if parent == None:
            return True
        return False

    ## Method check if is element searching child element.
    # @param In In is instance of class DataIn
    # @param Out is instance of class DataOut
    def itsYou(self,In,Out):
        return True

    ## Method implemented behavior of element.
    def childProcess(self):
        self.validateAttributeProcess()
        self.searchTagAttributes()
        if self.In.sp.token != None and self.In.sp.token['tagAttribute'] != None:
                for x in self.In.sp.token['tagAttribute']:
                    if re.search('^xmlns:.$', x):
                        self.In.tagPrefix = x.replace('xmlns:','',1)
                        self.In.sp.token['tagAttribute'] = None
        while self.In.sp.token != None:
            self.searchChild()
        if self.In.sp.token == None:
            return True
        else:
            raise ValueError


class SelectorElement(XmlElement):
    """
    SelectorElement is instance of XmlElement.
    SelectorElement implement XML Schema selector Element.
    http://www.w3schools.com/schema/el_selector.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "SELECTOR"
        self.useAttributes = att
        self.possibleAttributes= {'id':None, 'xpath':None}
        self.parentElement = ['key', 'keyref', 'unique']

    ## Method implemented behavior of element.
    # @todo Not implemented
    def childProcess(self):
          return True


class SequenceElement(XmlElement):
    """
    SequenceElement is instance of XmlElement.
    SequenceElement implement XML Schema sequence Element.
    http://www.w3schools.com/schema/el_sequence.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "SEQUENCE"
        self.useAttributes = att
        self.possibleAttributes= {'id':None,'maxOccurs':None, 'minOccurs':None}
        self.parentElement = ['group', 'choice', 'sequence', 'complexType', 'restriction', 'extension']

    ## Method implemented behavior of element.
    def childProcess(self):
        self.validateAttributeProcess()
        self.searchChild()
        return True

    ## Method search child element between child node in tree.
    def searchChild(self):
        trr = self.In.validateTree
        count = []
        for y in range(len(trr.child)):
            count.append(0)
        while True:
            cond = False
            for x in range(len(trr.child)):
                try:
                    if type(trr.child[x].elClass) != type(self) :
                        stat = trr.child[x].elClass.run(self.In.getCopy(trr.child[x]), self.Out)
                        if stat:
                            cond = True
                            count[x] +=1
                        else:
                            if count[x] <= self.minOccurs and count[x] < self.minOccurs:
                                count[x] +=1
                except ReferenceError:
                    pass
            if not cond:
                for x in range(len(trr.child)):
                    if count[x] > self.maxOccurs or count[x] < self.minOccurs:
                        if ("minOccurs" in (trr.child[x].elClass.useAttributes)) and (trr.child[x].elClass.useAttributes['minOccurs'] != '0'):
                            raise ValueError
                break


class SimpleContentElement(XmlElement):
    """
    SimpleContentElement is instance of XmlElement.
    SimpleContentElement implement XML Schema simpleContent Element.
    http://www.w3schools.com/schema/el_simpleContent.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "SIMPLE CONTETN ELEMENT"
        self.useAttributes = att
        self.possibleAttributes = {'id':None}
        self.parentElement = ['complexType']

    ## Method implemented behavior of element.
    def childProcess(self):
        self.searchChild()
        return True


class SimpleTypeElement(XmlElement):
    """
    SimpleTypeElement is instance of XmlElement.
    SimpleTypeElement implement XML Schema simpleType Element.
    http://www.w3schools.com/schema/el_simpletype.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "SIMPLE TYPE"
        self.useAttributes = att
        self.possibleAttributes= {'id':None, 'name':None}
        self.parentElement = ['attribute', 'element', 'list', 'restriction', 'schema', 'union']

    ## Method implemented behavior of element.
    def childProcess(self):
        self.validateAttributeProcess() 
        self.searchChild()
        return True


class UnionElement(XmlElement):
    """
    UnionElement is instance of XmlElement.
    UnionElement implement XML Schema union Element.
    http://www.w3schools.com/schema/el_union.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "UNION"
        self.useAttributes = att
        self.possibleAttributes= {'id':None, 'memberTypes':None}
        self.parentElement = ['simpleType']
        self.memberTypes = None

    ## Method implemented behavior of element.
    def childProcess(self):
        self.validateAttributeProcess()
        if self.memberTypes != None:
            cond = False
            for x in self.memberTypes:
                try:
                    self.In.searchTypeName=x
                    self.searchParent()
                    cond = True
                    break
                except ReferenceError:
                    pass
            if not cond:
                raise ValueError
        return True


class UniqueElement(XmlElement):
    """
    UniqueElement is instance of XmlElement.
    UniqueElement implement XML Schema unique Element.
    http://www.w3schools.com/schema/el_unique.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "UNIQUE"
        self.useAttributes = att
        self.possibleAttributes = {'id': None, 'name': None}
        self.parentElement = ['element']

    ## Method implemented behavior of element.
    # @todo Not implemented
    def childProcess(self):
        return True


############################################


class EnumerationFacets(XmlElement):
    """
    EnumerationFacets is instance of XmlElement.
    EnumerationFacets implement XML Schema enumeration Facets Element.
    http://www.w3schools.com/schema/schema_facets.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "EnumerationFacets"
        self.useAttributes = att
        self.possibleAttributes= {'value':None, }
        self.parentElement = ['restriction']

    ## Method check if is element searching child element.
    # @param In In is instance of class DataIn
    # @param Out is instance of class DataOut
    def itsYou(self,In,Out):
        for x in In.tagAttribute:
            if In.tagAttribute[x] in self.possibleAttributes['value']:
                return True
        raise ReferenceError

    ## Method implemented behavior of element.
    def childProcess(self):
            cond = False
            try:
                self.searchChild()
                cond = True
            except ValueError:
                if not cond:
                    raise
                else:
                    return True


class FractionDigitsFacets(XmlElement):
    """
    EnumerationFacets is instance of XmlElement.
    EnumerationFacets implement XML Schema fractionDigits Facets Element.
    http://www.w3schools.com/schema/schema_facets.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "FractionDigitsFacets"
        self.useAttributes = att
        self.possibleAttributes= {'value':None, }
        self.parentElement = ['restriction']

    ## Method implemented behavior of element.
    # @todo Not implemented specific behavior
    def childProcess(self):
            cond = False
            try:
                self.searchChild()
                cond = True
            except ValueError:
                if not cond:
                    raise
                else:
                    return True


class LengthFacets(XmlElement):
    """
    EnumerationFacets is instance of XmlElement.
    EnumerationFacets implement XML Schema length Facets Element.
    http://www.w3schools.com/schema/schema_facets.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "LengthFacets"
        self.useAttributes = att
        self.possibleAttributes= {'value':None, }
        self.parentElement = ['restriction']

    ## Method implemented behavior of element.
    # @todo Not implemented specific behavior
    def childProcess(self):
            cond = False
            try:
                self.searchChild()
                cond = True
            except ValueError:
                if not cond:
                    raise
                else:
                    return True
            return True


class MaxExclusiveFacets(XmlElement):
    """
    EnumerationFacets is instance of XmlElement.
    EnumerationFacets implement XML Schema maxExclusive Facets Element.
    http://www.w3schools.com/schema/schema_facets.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "MaxExclusiveFacets"
        self.useAttributes = att
        self.possibleAttributes= {'value':None, }
        self.parentElement = ['restriction']

    ## Method implemented behavior of element.
    # @todo Not implemented specific behavior
    def childProcess(self):
            return True


class MaxInclusiveFacets(XmlElement):
    """
    EnumerationFacets is instance of XmlElement.
    EnumerationFacets implement XML Schema maxInclusive Facets Element.
    http://www.w3schools.com/schema/schema_facets.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "MaxInclusiveFacets"
        self.useAttributes = att
        self.possibleAttributes= {'value':None, }
        self.parentElement = ['restriction']

    ## Method implemented behavior of element.
    # @todo Not implemented specific behavior
    def childProcess(self):
            return True


class MaxLengthFacets(XmlElement):
    """
    EnumerationFacets is instance of XmlElement.
    EnumerationFacets implement XML Schema maxLength Facets Element.
    http://www.w3schools.com/schema/schema_facets.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "MaxLengthFacets"
        self.useAttributes = att
        self.possibleAttributes= {'value':None, }
        self.parentElement = ['restriction']

    ## Method implemented behavior of element.
    # @todo Not implemented specific behavior
    def childProcess(self):
            cond = False
            try:
                self.searchChild()
                cond = True
            except ValueError:
                if not cond:
                    raise
                else:
                    return True


class MinExclusiveFacets(XmlElement):
    """
    EnumerationFacets is instance of XmlElement.
    EnumerationFacets implement XML Schema minExclusive Facets Element.
    http://www.w3schools.com/schema/schema_facets.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "MinExclusiveFacets"
        self.useAttributes = att
        self.possibleAttributes= {'value':None, }
        self.parentElement = ['restriction']

    ## Method implemented behavior of element.
    # @todo Not implemented specific behavior
    def childProcess(self):
            return True


class MinInclusiveFacets(XmlElement):
    """
    EnumerationFacets is instance of XmlElement.
    EnumerationFacets implement XML Schema minInclusive Facets Element.
    http://www.w3schools.com/schema/schema_facets.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "MinInclusiveFacets"
        self.useAttributes = att
        self.possibleAttributes= {'value':None, }
        self.parentElement = ['restriction']

    ## Method implemented behavior of element.
    # @todo Not implemented specific behavior
    def childProcess(self):
            return True

class TagAttributeFacets(XmlElement):
    """
    EnumerationFacets is instance of XmlElement.
    EnumerationFacets implement XML Schema tagAttribute Facets Element.
    http://www.w3schools.com/schema/schema_facets.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "TagAttributeFacets"
        self.useAttributes = att
        self.possibleAttributes= {'value':None, }
        self.parentElement = ['restriction']

    ## Method implemented behavior of element.
    # @todo Not implemented specific behavior
    def childProcess(self):
            cond = False
            try:
                self.searchChild()
                cond = True
            except ValueError:
                if not cond:
                    raise
                else:
                    return True


class PatternFacets(XmlElement):
    """
    EnumerationFacets is instance of XmlElement.
    EnumerationFacets implement XML Schema pattern Facets Element.
    http://www.w3schools.com/schema/schema_facets.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "PatternFacets"
        self.useAttributes = att
        self.possibleAttributes= {'value':None, }
        self.parentElement = ['restriction']

    ## Method implemented behavior of element.
    # @todo Not implemented specific behavior
    def childProcess(self):
            cond = False
            try:
                self.searchChild()
                cond = True
            except ValueError:
                if not cond:
                    raise
                else:
                    return True


class TotalDigitsFacets(XmlElement):
    """
    EnumerationFacets is instance of XmlElement.
    EnumerationFacets implement XML Schema totalDigits Facets Element.
    http://www.w3schools.com/schema/schema_facets.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "TotalDigitsFacets"
        self.useAttributes = att
        self.possibleAttributes= {'value':None, }
        self.parentElement = ['restriction']

    ## Method implemented behavior of element.
    # @todo Not implemented specific behavior
    def childProcess(self):
            cond = False
            try:
                self.searchChild()
                cond = True
            except ValueError:
                if not cond:
                    raise
                else:
                    return True



class WhiteSpaceFacets(XmlElement):
    """
    EnumerationFacets is instance of XmlElement.
    EnumerationFacets implement XML Schema whiteSpace Facets Element.
    http://www.w3schools.com/schema/schema_facets.asp
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    ## The constructor
    # @param att List of set element attributes
    def __init__(self, att):
        super().__init__(None)
        self.elementName = "WhiteSpaceFacets"
        self.useAttributes = att
        self.possibleAttributes= {'value':None, }
        self.parentElement = ['restriction']

    ## Method implemented behavior of element.
    # @todo Not implemented specific behavior
    def childProcess(self):
            cond = False
            try:
                self.searchChild()
                cond = True
            except ValueError:
                if not cond:
                    raise
                else:
                    return True