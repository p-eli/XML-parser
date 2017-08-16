#!/usr/bin/python3
__author__ = 'Jakub Pelikan'
import re

class XmlDataTypes():
    """
    XmlDataTypes implement valid data types for XML. And check correct value.
    @author Jakub Pelikan
    @version 1.0
    @package xmlParser
    """
    pattern1 = re.compile('^[^:]+:')
    ## The constructor
    def __init__(self):
        self.all =  {'date':self.dtDate,'dateTime':self.dtDateTime,'duration':self.dtDuration,'gDay':self.dtGDay,'gMonth':self.dtGMonth,'gMonthDay': self.dtGMonthDay,'gYear':self.dtGYear,'gYearMonth':self.dtGYearMonth,'time':self.dtTime, 'ENTITIES':self.dtENTITIES,'ENTITY':self.dtENTITY, 'ID':self.dtID, 'IDREF':self.dtIDREF,'IDREFS':self.dtIDREFS,'language':self.dtLanguage,'Name':self.dtName,'NCName':self.dtNCName,'NMTOKEN':self.dtNMTOKEN,'NMTOKENS':self.dtNMTOKENS,'normalizedString':self.dtNormalizedString,'QName':self.dtQName,'string':self.dtString,'token':self.dtToken, 'byte':self.dtByte,'decimal':self.dtDecimal,'int':self.dtInt,'integer':self.dtInteger,'long':self.dtLong,'negativeInteger':self.dtNegativeInteger,'nonNegativeInteger':self.dtNonNegativeInteger,'nonPositiveInteger':self.dtNonPositiveInteger,'positiveInteger':self.dtPositiveInteger,'short':self.dtShort,'unsignedLong':self.dtUnsignedLong,'unsignedInt':self.dtUnsignedInt,'unsignedShort':self.dtUnsignedShort,'unsignedByte':self.dtUnsignedByte, 'anyURI':self.dtAnyURI, 'base64Binary':self.dtBase64Binary ,'boolean':self.dtBoolean, 'double':self.dtDouble, 'float':self.dtFloat, 'hexBinary':self.dtHexBinary, 'NOTATION':self.dtNOTATION, 'QName':self.dtQName}

    ## Method find data types name
    # @param type Type is a name of search data type.
    def findType(self, type):
        type = re.sub(self.pattern1, '', type)
        if type in self.all:
            return True
        else:
            raise ValueError

    ## Method find data types name
    # @param type Type is a name of search data type.
    # @param token Token is token with validate value.
    def validate(self,type, token):
        type = re.sub(self.pattern1, '', type)
        if (type in self.all):
            return self.all[type](token)
        else:
            raise ValueError

    ## Method validate data type Date
    # @param data Data is validate value.
    def dtDate (self, data):
        if re.search('^\d{4}-\d{2}-\d{2}$',data) or re.search('^\d{4}-\d{2}-\d{2}Z$',data) or re.search('^\d{4}-\d{2}-\d{2}-\d{2}:\d{2}$',data) or re.search('^\d{4}-\d{2}-\d{2}\+\d{2}:\d{2}$',data):
            return data
        raise ValueError

    ## Method validate data type DateTime
    # @param data Data is validate value.
    def dtDateTime (self, data):
        if re.search('^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$',data) or re.search('^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d$',data) or re.search('^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$',data) or re.search('^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}-\d{2}:\d{2}$',data) or re.search('^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{2}:\d{2}$',data):
            return data
        raise ValueError

    ## Method validate data type Duration
    # @param data Data is validate value.
    def dtDuration (self, data):
        if re.search('^-?P(\d+Y)?(\d+M)?(\d+D)?(T\d+H)?$',data):
            return data
        raise ValueError

    ## Method validate data type GDay
    # @param data Data is validate value.
    def dtGDay (self, data):
        if re.search('^[0123]\d$',data):
            return data
        raise ValueError

    ## Method validate data type GMonth
    # @param data Data is validate value.
    def dtGMonth (self, data):
        if re.search('^0[1-9]$',data) or re.search('^1[012]$',data):
            return data
        raise ValueError

    ## Method validate data type GMonthDay
    # @param data Data is validate value.
    def dtGMonthDay (self, data):
        if re.search('^0[1-9]-[0123]\d$',data) or re.search('^1[012]-[0123]\d$',data):
            return data
        raise ValueError

    ## Method validate data type GYear
    # @param data Data is validate value.
    def dtGYear (self, data):
        if re.search('^\d{4}$',data):
            return data
        raise ValueError

    ## Method validate data type GYearMonth
    # @param data Data is validate value.
    def dtGYearMonth (self, data):
        if re.search('^\d{4}-0[1-9]$',data) or re.search('^\d{4}-1[012]$',data):
            return data
        raise ValueError

    ## Method validate data type Time
    # @param data Data is validate value.
    def dtTime (self, data):
        if re.search('^\d{2}:\d{2}:\d{2}$',data) or re.search('^\d{2}:\d{2}:\d{2}\.\d$',data) or re.search('^\d{2}:\d{2}:\d{2}Z$',data) or re.search('^\d{2}:\d{2}:\d{2}-\d{2}:\d{2}$',data) or re.search('^\d{2}:\d{2}:\d{2}\+\d{2}:\d{2}$',data):
            return data
        raise ValueError

    ## Method validate data type ENTITIES
    # @param data Data is validate value.
    def dtENTITIES (self, data):
        return data

    ## Method validate data type ENTITY
    # @param data Data is validate value.
    def dtENTITY (self, data):
        return data

    ## Method validate data type ID
    # @param data Data is validate value.
    def dtID (self, data):
        return data

    ## Method validate data type IDREF
    # @param data Data is validate value.
    def dtIDREF (self, data):
        return data

    ## Method validate data type IDREFS
    # @param data Data is validate value.
    def dtIDREFS (self, data):
        return data

    ## Method validate data type Language
    # @param data Data is validate value.
    def dtLanguage (self, data):
        return data

    ## Method validate data type Name
    # @param data Data is validate value.
    def dtName (self, data):
        return data

    ## Method validate data type NCName
    # @param data Data is validate value.
    def dtNCName (self, data):
        return data

    ## Method validate data type NMTOKEN
    # @param data Data is validate value.
    def dtNMTOKEN (self, data):
        return data

    ## Method validate data type NMTOKENS
    # @param data Data is validate value.
    def dtNMTOKENS (self, data):
        return data

    ## Method validate data type NormalizedString
    # @param data Data is validate value.
    def dtNormalizedString (self, data):
        if re.search('[\n\r\t]+',data):
            return re.sub('[\n\r\t]+', ' ',data)
        return data

    ## Method validate data type QName
    # @param data Data is validate value.
    def dtQName (self, data):
        return data

    ## Method validate data type String
    # @param data Data is validate value.
    def dtString (self, data):
        return data

    ## Method validate data type Token
    # @param data Data is validate value.
    def dtToken (self, data):
        if re.search('\s+',data):
            return re.sub('\s+', ' ',data)
        return data

    ## Method validate data type Byte
    # @param data Data is validate value.
    def dtByte (self, data):
        if (data > int(pow(2,8)/-2)) and (int(pow(2,8)/2)-1):
            return data
        raise ValueError

    ## Method validate data type Decimal
    # @param data Data is validate value.
    def dtDecimal (self, data):
        if re.search('^[\+-]?\d+\.?\d*$', data):
            if len(re.sub('[^\d]+','',data)) <= 18:
                return data
        raise ValueError

    ## Method validate data type Int
    # @param data Data is validate value.
    def dtInt (self, data):
        if (data > int(pow(2,32)/-2)) and (int(pow(2,32)/2)-1):
            return data
        raise ValueError

    ## Method validate data type Integer
    # @param data Data is validate value.
    def dtInteger (self, data):
        if re.search('^[\+-]?\d+$', data):
            return data
        raise ValueError

    ## Method validate data type Long
    # @param data Data is validate value.
    def dtLong (self, data):
        if (data > int(pow(2,64)/-2)) and (int(pow(2,64)/2)-1):
            return data
        raise ValueError

    ## Method validate data type NegativeInteger
    # @param data Data is validate value.
    def dtNegativeInteger (self, data):
        if re.search('^-[1-9]\d*$', data):
            return data
        raise ValueError

    ## Method validate data type NonNegativeInteger
    # @param data Data is validate value.
    def dtNonNegativeInteger (self, data):
        if re.search('^\+?\d+$', data):
            return data
        raise ValueError

    ## Method validate data type NonPositiveInteger
    # @param data Data is validate value.
    def dtNonPositiveInteger (self, data):
        if re.search('^-\d+$', data) or re.search('^0$', data):
            return data
        raise ValueError

    ## Method validate data type PositiveInteger
    # @param data Data is validate value.
    def dtPositiveInteger (self, data):
        if re.search('^\+?[1-9]\d*$', data):
            return data
        raise ValueError

    ## Method validate data type Short
    # @param data Data is validate value.
    def dtShort (self, data):
        if (data > int(pow(2,16)/-2)) and (int(pow(2,16)/2)-1):
            return data
        raise ValueError

    ## Method validate data type UnsignedLong
    # @param data Data is validate value.
    def dtUnsignedLong (self, data):
        if (data > 0) and (data < pow(2,64)-1):
            return data
        raise ValueError

    ## Method validate data type UnsignedInt
    # @param data Data is validate value.
    def dtUnsignedInt (self, data):
        if (data > 0) and (data < pow(2,32)-1):
            return data
        raise ValueError

    ## Method validate data type UnsignedShort
    # @param data Data is validate value.
    def dtUnsignedShort (self, data):
        if (data > 0) and (data < pow(2,16)-1):
            return data
        raise ValueError

    ## Method validate data type UnsignedByte
    # @param data Data is validate value.
    def dtUnsignedByte (self, data):
        if (data > 0) and (data < pow(2,8)-1):
            return data
        raise ValueError

    ## Method validate data type AnyURI
    # @param data Data is validate value.
    def dtAnyURI (self, data):
        if re.search(' ', data):
            return re.sub(' ','%20',data)
        return data

    ## Method validate data type Base64Binary
    # @param data Data is validate value.
    def dtBase64Binary (self, data):
        return data

    ## Method validate data type Boolean
    # @param data Data is validate value.
    def dtBoolean (self, data):
        if re.search('^(true|1)$',data):
            return "true"
        if re.search('^(false|0)$',data):
            return "false"
        raise ValueError

    ## Method validate data type Double
    # @param data Data is validate value.
    def dtDouble (self, data):
        return data

    ## Method validate data type Float
    # @param data Data is validate value.
    def dtFloat (self, data):
        return data

    ## Method validate data type HexBinary
    # @param data Data is validate value.
    def dtHexBinary (self, data):
        return data

    ## Method validate data type NOTATION
    # @param data Data is validate value.
    def dtNOTATION (self, data):
        return data

    ## Method validate data type QName
    # @param data Data is validate value.
    def dtQName (self, data):
        return data