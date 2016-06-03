import re
import bitstring
from epc.EPCNumber import EPCNumber
from epcerrors.EncodingException import EncodingException
from schema.Field import Field

class GID96(EPCNumber):
    '''
    Represents an GID-96 EPC Encoding
    The General Identifier EPC scheme is independent of any specifications or identity
    scheme outside the EPCglobal Tag Data Standard.
    '''
    def __init__(self,startSerialNumber=0,numOfSerialNumbers=0):
        EPCNumber.__init__(self)
        self._loadFields()
        self._encodingType="GID96"
        
    def encode(self,generalManager,indicatorDigit,objectClass,filter_value,serialNumber=0):
        """
        encodes an GID-96. 
        """
        #Reload fields
        self._loadFields()
        
        
        #General Manager
        generalManagerField = self.getField("GeneralManager")
        generalManagerField.setBitLength(28)
        generalManagerField.setDigitLength(28/4)
        generalManagerField.setOffset(8)
        self.setFieldValue("GeneralManager",int(generalManager))
        
        #ObjectClass
        objectClassField = self.getField("ObjectClass")
        objectClassField.setBitLength(24)
        objectClassField.setDigitLength(24/8)
        objectClassField.setOffset(36)
        self.setFieldValue("ObjectClass",int(objectClass))
        #SerialNumber
        serialNumberField = self.getField("SerialNumber")
        serialNumberField.setBitLength(36)
        serialNumberField.setDigitLength(36/4)
        self.setFieldValue("SerialNumber",int(serialNumber))
        #Set the PackString Format
        self._packStringFormat = 'uint:8, uint:28, uint:24, uint:36'
        #Pack the bitstring
        bsp=  bitstring.pack(self._packStringFormat, 
                                int(self.getFieldValue("Header")), 
                                int(self.getFieldValue("GeneralManager")),
                                int(self.getFieldValue("ObjectClass")), 
                                int(self.getFieldValue("SerialNumber")))
         
        #Set the _bits for the GID-96
        self._bits = bsp.unpack("bin")[0][2:]
        
        return self
    
    def toEPCTagUri(self):
        '''
        Returns the GID-96 in an EPC URI Representation
        Example: urn:tagpy:tag:gid-96:0614141.812345.6789
        '''
        epcUri = "urn:tagpy:tag:gid-96:%s.%s.%s" % (int(self.getFieldValue("GeneralManager")),int(self.getFieldValue("ObjectClass")),int(self.getFieldValue("SerialNumber")))
        return epcUri

    def toEPCUri(self):
        '''
        Returns the GID-96 in an EPC Pure Identity
        Example: urn:tagpy:id:gid:0614141.812345.6789
        '''
        epcUri = "urn:tagpy:id:gid:%s.%s.%s" % (int(self.getFieldValue("GeneralManager")),int(self.getFieldValue("ObjectClass")),int(self.getFieldValue("SerialNumber")))
        return epcUri
    
    def fromEPCUri(self,epcUri):
        '''Parses the EPC from a epcURI - urn:tagpy:id:gid:358468.02339.95'''
        regEx = re.compile("\d+")
        s = regEx.findall(epcUri)
        generalManager = s[0]
        objectClass = s[1]
        serialNumber = s[2]
        self.encode(generalManager, None, objectClass, None, serialNumber)
        return self;
    
    def fromTagUri(self,tagUri):
        '''
        Parses the EPC from a TagURI
        Example: urn:tagpy:tag:gid-96:614141.812345.6789
        '''
        regEx = re.compile("\d+")
        s = regEx.findall(tagUri)
        generalManager = s[1]
        objectClass = s[2]
        serialNumber = s[3]
        self.encode(generalManager, None, objectClass, None, serialNumber)
        return self
    
    def toXml(self):
        xml = "<Tag type='%s'>\n" % (self._encodingType)
        xml += "\t<Fields>\n"
        xml +=  "\t\t<Field name='Header' value='%s'/>\n" % (self.getFieldValue("Header"))
        xml +=  "\t\t<Field name='GeneralManager' value='%s'/>\n"% (int(self.getFieldValue("GeneralManager")))
        xml +=  "\t\t<Field name='ObjectClass' value='%s'/>\n" % (int(self.getFieldValue("ObjectClass")))
        xml +=  "\t\t<Field name='SerialNumber' value='%s'/>\n" % (int(self.getFieldValue("SerialNumber")))
        xml += "\t</Fields>\n"
        xml += "\t<Hex>%s</Hex>\n" % (self.toHex())
        xml += "\t<Binary>%s</Binary>\n" % (self.toBinary())
        xml += "\t<TagUri>%s</TagUri>\n" % (self.toEPCTagUri())
        xml += "\t<PureIdentity>%s</PureIdentity>\n" % (self.toEPCUri())
        xml += "</Tag>"
        return xml;
    
    def toDictionary(self):
        return dict([('Type',self._encodingType),\
                ('Header',self.getFieldValue("Header")),\
                ('GeneralManager',int(self.getFieldValue("GeneralManager"))),\
                ('ObjectClass',int(self.getFieldValue("ObjectClass"))),\
                ('SerialNumber',self.getFieldValue("SerialNumber")),\
                ('Hex',self.toHex()),\
                ('Binary',self.toBinary()),\
                ('TagURI',self.toEPCTagUri()),\
                ('PureIdentity',self.toEPCUri())])
     
    def decodeFromBinary(self,binary):
        '''
        Decodes an GID-96 from BINARY string
        '''
        self._loadFields()
        if(len(binary)!=96):
            raise EncodingException("Binary string is not 96 bits. GID-96 Requires 96 bits to decode properly")
        
        
        
        self.getField("GeneralManager").setOffset(8)
        self.getField("GeneralManager").setBitLength(28)
        
        self.getField("ObjectClass").setOffset(36)
        self.getField("ObjectClass").setBitLength(24)
        
        self.getField("SerialNumber").setOffset(36+24)
        self.getField("SerialNumber").setBitLength(36)
        
        generalManager = binary[self.getField("GeneralManager").getOffset():self.getField("GeneralManager").getOffset() + self.getField("GeneralManager").getBitLength()]
        generalManager = int(generalManager,2)
        self.setFieldValue("GeneralManager",generalManager)
        
        objectClass = binary[self.getField("ObjectClass").getOffset():self.getField("ObjectClass").getOffset() + self.getField("ObjectClass").getBitLength()]
        objectClass = int(objectClass,2)
        self.setFieldValue("ObjectClass", objectClass)
        
        serialNumber = binary[self.getField("SerialNumber").getOffset():self.getField("SerialNumber").getOffset() + self.getField("SerialNumber").getBitLength()]
        serialNumber = int(serialNumber,2)
        self.setFieldValue("SerialNumber",serialNumber)
        
        return self
    
    def setSerialNumber(self,value):
        self.setFieldValue("SerialNumber",value)
    def getSerialNumber(self):
        self.getFieldValue("SerialNumber")
    
    def _updateBitString(self):
        self._packStringFormat = 'uint:8, uint:28, uint:24, uint:36'
        #Pack the bitstring
        bsp=  bitstring.pack(self._packStringFormat, 
            int(self.getFieldValue("Header")), 
            int(self.getFieldValue("GeneralManager")),
            int(self.getFieldValue("ObjectClass")), 
            int(self.getFieldValue("SerialNumber")))
        
        #Set the _bits for the GID-96
        self._bits = bsp.unpack("bin")[0][2:]
    def toGS1(self,serialNumberLength=0,useParenthesesAroundAIs=True):
        raise EncodingException("GID-96 Cannot be represented as a GS1")    
    def _loadFields(self):
        """
        Loads Fields for the GID-96 
        """
        header = Field(fieldName="Header",offset=0,bitLength=8,ordinal=1,fieldValue=53,digitLength=2)
        self.fieldDictionary["Header"] = header
        generalManager = Field(fieldName="GeneralManager",offset=8,bitLength=28,ordinal=2,fieldValue=0,digitLength=1) 
        self.fieldDictionary["GeneralManager"] = generalManager
        objectClass = Field(fieldName="ObjectClass",offset=11,bitLength=24,ordinal=3,fieldValue=0,digitLength=1) 
        self.fieldDictionary["ObjectClass"] = objectClass 
        serial = Field(fieldName="SerialNumber",offset=52,bitLength=36,ordinal=6,fieldValue=0,digitLength=0) 
        self.fieldDictionary["SerialNumber"] = serial