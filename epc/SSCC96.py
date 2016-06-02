import bitstring
import re
from epc.EPCNumber import EPCNumber
from epcerrors.EncodingException import EncodingException
from gs1.SSCC import SSCC
from utils.Partitions import Partitions
from utils.Conversion import Conversion
from schema.Field import Field


class SSCC96(EPCNumber):
    '''
    Represents an SSCC-96 EPC Encoding.
    The Serial Shipping Container Code EPC scheme is used to assign a unique identity to a
    logistics handling unit, such as a the aggregate contents of a shipping container or a pallet
    load.
    '''
    def __init__(self,startSerialNumber=0,numOfSerialNumbers=0):
        EPCNumber.__init__(self)
        self._loadFields()
        self._ignoreUpdate=False
        self._encodingType="SSCC96"
        
    def encode(self,companyPrefix,extensionDigit=0,serialReference="0",filter_value=2,reserved=0):
        """
        encodes an SSCC-96. 
        """
        #Reload fields
        self._loadFields()
        #Get ref to conversion class
        conversion = Conversion()
        #Get the header bits
        
        #Filter
        self.setFieldValue("Filter",filter_value)
        
        #Partition
        partition = Partitions()
        partitionValue = partition.getPartitionValue(len(companyPrefix), "SSCC")
        self.setFieldValue("Partition",conversion.uint32(partitionValue))
        #Company Prefix
        companyPrefixField = self.getField("CompanyPrefix")
        companyPrefixField.setBitLength(partition.getCompanyPrefixBitLength(partitionValue,"SSCC"))
        companyPrefixField.setDigitLength(partition.getCompanyPrefixDigitLength(partitionValue,"SSCC"))
        self.setFieldValue("CompanyPrefix",companyPrefix)
        
        #serialReference
        serialReferenceField = self.getField("SerialReference")
        serialReferenceField.setBitLength(partition.getItemBitLength(partitionValue, "SSCC"))
        serialReferenceField.setDigitLength(partition.getItemDigitLength(partitionValue, "SSCC"))
        serialReferenceField.setOffset(int(companyPrefixField.getBitLength()) + int(companyPrefixField.getOffset()))
        self._ignoreUpdate = True
        serialReference = serialReference.zfill(partition.getItemDigitLength(partitionValue, "SSCC")-1)
        self.setFieldValue("SerialReference","%s%s" % (extensionDigit,serialReference))
        self._ignoreUpdate = False
        #Reserved
        self.setFieldValue("Reserved",0)
        #Set the PackString Format
        self._packStringFormat = 'uint:8, uint:3, uint:3, uint:%s, uint:%s, uint:24' % (companyPrefixField.getBitLength(),serialReferenceField.getBitLength())
        #Pack the bitstring
        bsp=  bitstring.pack(self._packStringFormat, 
                                self.getFieldValue("Header"), 
                                self.getFieldValue("Filter"),
                                self.getFieldValue("Partition"), 
                                self.getFieldValue("CompanyPrefix"), 
                                self.getFieldValue("SerialReference"),
                                self.getFieldValue("Reserved"))
         
        #Set the _bits for the SSCC-96
        self._bits = bsp.unpack("bin")[0][2:]
        
        return self
    
    def fromEPCUri(self,epcUri):
        '''Parses the EPC from a epcURI - urn:tagpy:id:sscc:0614141.1234567890'''
        regEx = re.compile("\d+")
        s = regEx.findall(epcUri)
        companyPrefix = s[0]
        extensionDigit = s[1][:1]
        serialReference = s[1][1:]
        #set the filter value to 0
        filter = 0
        
        self.encode(companyPrefix, extensionDigit, serialReference, filter, 0)
        return self;
    
    def fromTagUri(self,tagUri):
        '''Parses the EPC from a TagURI'''
        regEx = re.compile("\d+")
        s = regEx.findall(tagUri)
        filter = s[1]
        companyPrefix = s[2]
        extensionDigit = s[3][:1]
        serialReference = s[3][1:]
        
        self.encode(companyPrefix, extensionDigit, serialReference, filter, 0)
        return self
    
    def toEPCTagUri(self):
        '''
        Returns the SSCC-96 in an EPC URI Representation
        Example: urn:tagpy:tag:sscc-96:3.0614141.1234567890
        '''
        #if(len(self.getFieldValue("CompanyPrefix"))+len(self.getFieldValue("SerialReference")) != 17):
        #    raise EncodingException("The Length of the CompanyPrefix and the SerialReference must equal 17")
        epcUri = "urn:tagpy:tag:sscc-96:%s.%s.%s" % (self.getFieldValue("Filter"),self.getFieldValue("CompanyPrefix"),self.getFieldValue("SerialReference"))
        return epcUri
    
    def toEPCUri(self):
        '''
        Returns the SSCC-96 in an EPC Pure Identity
        Example: urn:tagpy:id:sscc:0614141.812345
        '''
        #if(len(self.getFieldValue("CompanyPrefix"))+len(self.getFieldValue("SerialReference")) != 17):
        #    raise EncodingException("The Length of the CompanyPrefix and the SerialReference must equal 17")
        epcUri = "urn:tagpy:id:sscc:%s.%s" % (str(self.getFieldValue("CompanyPrefix")),str(self.getFieldValue("SerialReference")))
        return epcUri 
    
    def toGS1(self,useParenthesesAroundAIs=True):
        '''Returns the EPC epc translated to a full GS1 with App Identifiers''' 
        sscc = SSCC(self.getFieldValue("CompanyPrefix"))
        #Make sure that the company prefix and Serial Reference are equal to 16
        serialLen = 16 - (len(self.getFieldValue("CompanyPrefix")))
        sn = str(self.getFieldValue("SerialReference")[1:]).zfill(serialLen)
        
        sscc.encode(self.getFieldValue("SerialReference")[0:1], sn)
        return sscc.toGS1(useParenthesesAroundAIs) 
    
    def toSSCC18(self):
        '''Returns the EPC epc translated to a GS1 GTIN-14 with NO App Identifiers'''
        sscc = SSCC(self.getFieldValue("CompanyPrefix"))
        sscc.encode(self.getFieldValue("SerialReference")[0:1], self.getFieldValue("SerialReference")[1:])
        return sscc.toSSCC18()
    
    def toXml(self):
        xml = "<Tag type='%s'>\n" % (self._encodingType)
        xml += "\t<Fields>\n"
        xml +=  "\t\t<Field name='Header' value='%s'/>\n" % (self.getFieldValue("Header"))
        xml +=  "\t\t<Field name='Filter' value='%s'/>\n"% (self.getFieldValue("Filter"))
        xml +=  "\t\t<Field name='Partition' value='%s'/>\n" % (self.getFieldValue("Partition"))
        xml +=  "\t\t<Field name='CompanyPrefix' value='%s'/>\n" % (self.getFieldValue("CompanyPrefix"))
        xml +=  "\t\t<Field name='SerialReference' value='%s'/>\n" % (self.getFieldValue("SerialReference"))
        xml +=  "\t\t<Field name='RawSerialReference' value='%s'/>\n" % (self.getFieldValue("SerialReference")[1:])
        xml +=  "\t\t<Field name='ExtensionDigit' value='%s'/>\n" % (self.getFieldValue("SerialReference")[0:1])
        xml += "\t</Fields>\n"
        xml += "\t<Hex>%s</Hex>\n" % (self.toHex())
        xml += "\t<Binary>%s</Binary>\n" % (self.toBinary())
        xml += "\t<TagUri>%s</TagUri>\n" % (self.toEPCTagUri())
        xml += "\t<PureIdentity>%s</PureIdentity>\n" % (self.toEPCUri())
        xml += "\t<GS1>%s</GS1>\n" % (self.toGS1(True))
        xml += "</Tag>"
        return xml;
    
    def toDictionary(self):
        return {
                "Filter Value":self.getFieldValue("Filter"),
                "Partition":self.getFieldValue("Partition"),
                "Company Prefix":self.getFieldValue("CompanyPrefix"),
                "Serial Reference": self.getFieldValue("SerialReference"),
                "Serial Number" : int(self.getFieldValue("SerialReference")[1:]),
                "Extension Digit" : self.getFieldValue("SerialReference")[0:1],
                "Hex": self.toHex(),
                "Bin": self.toBinary(),
                "Tag URN" : self.toEPCTagUri(),
                "Pure Identity" : self.toEPCUri(),
                "SSCC18" : self.toSSCC18(),
                "GS1" : self.toGS1(True)
                }
    
    def decodeFromBinary(self,binary):
        '''
        Decodes an SSCC from BINARY string
        '''
        self._loadFields()
        if(len(binary)!=96):
            raise EncodingException("Binary string is not 96 bits. SSCC-96 Requires 96 bits to decode properly")
        
        
        
        #Filter
        filter = binary[self.getField("Filter").getOffset():self.getField("Filter").getOffset() + self.getField("Filter").getBitLength()]
        self.setFieldValue("Filter",int(filter,2))
        partitionValue = binary[self.getField("Partition").getOffset():self.getField("Partition").getOffset() + self.getField("Partition").getBitLength()]
        partitionValue = int(partitionValue,2)
        self.setFieldValue("Partition",partitionValue)
        
        #Partition
        partitions = Partitions()
        companyPrefixLength = partitions.getCompanyPrefixBitLength(partitionValue,"SSCC")
        companyPrefixDigitLength = partitions.getCompanyPrefixDigitLength(partitionValue,"SSCC")
        self.getField("CompanyPrefix").setOffset(14)
        self.getField("CompanyPrefix").setBitLength(companyPrefixLength)
        serialReferenceLength = partitions.getItemBitLength(partitionValue,"SSCC")
        serialReferenceDigitLength = partitions.getItemDigitLength(partitionValue,"SSCC")
        
        self.getField("SerialReference").setOffset(14 + companyPrefixLength)
        self.getField("SerialReference").setBitLength(serialReferenceLength)
        self.getField("SerialReference").setDigitLength(serialReferenceDigitLength)
        
        companyPrefix = binary[self.getField("CompanyPrefix").getOffset():self.getField("CompanyPrefix").getOffset() + self.getField("CompanyPrefix").getBitLength()]
        companyPrefix = str(int(companyPrefix,2)).zfill(companyPrefixDigitLength)
        self.setFieldValue("CompanyPrefix",companyPrefix)
        serialReference = binary[self.getField("SerialReference").getOffset():self.getField("SerialReference").getOffset() + self.getField("SerialReference").getBitLength()]
        serialReference = str(int(serialReference,2)).zfill(serialReferenceDigitLength)
        self._ignoreUpdate = True
        self.setFieldValue("SerialReference", serialReference)
        self._ignoreUpdate = False
        self.setFieldValue("Reserved",0)
        
        return self
    
    def _updateBitString(self):
        self._packStringFormat = 'uint:8, uint:3, uint:3, uint:%s, uint:%s, uint:24' % (self.getField("CompanyPrefix").getBitLength(),self.getField("SerialReference").getBitLength())
        #Pack the bitstring
        bsp=  bitstring.pack(self._packStringFormat, 
                                self.getFieldValue("Header"), 
                                self.getFieldValue("Filter"),
                                self.getFieldValue("Partition"), 
                                self.getFieldValue("CompanyPrefix"), 
                                self.getFieldValue("SerialReference"),
                                self.getFieldValue("Reserved"))
         
        #Set the _bits for the SSCC-96
        self._bits = bsp.unpack("bin")[0][2:]
    
    
    def setFieldValue(self,fieldName,val):
        """
        Overriden from the base class because if the SerialReference changes the the extension digit must be preserved
        otherwise its a straight exchange
        """
        if(fieldName=="SerialReference" and (self._ignoreUpdate == False)):
            field = self._fieldDictionary[fieldName]
            extDigit = field.getFieldValue()[0:1]
            field.setFieldValue(str(extDigit)+str(val))
        else:
            field = self._fieldDictionary[fieldName]
            field.setFieldValue(val)
        
        self._updateBitString()
    
    def setSerialNumber(self,value):
        self._ignoreUpdate = False
        self.setFieldValue("SerialReference",value)
        self._ignoreUpdate = True
    def getSerialNumber(self):
        return self.getFieldValue("SerialReference")    
    def _loadFields(self):
        """
        Loads Fields for the SSCC-96 
        """
        
        header = Field(fieldName="Header",offset=0,bitLength=8,ordinal=1,fieldValue=49,digitLength=2)
        self._fieldDictionary["Header"] = header
        filter = Field(fieldName="Filter",offset=8,bitLength=3,ordinal=2,fieldValue=0,digitLength=1) 
        self._fieldDictionary["Filter"] = filter
        partition = Field(fieldName="Partition",offset=11,bitLength=3,ordinal=3,fieldValue=0,digitLength=1) 
        self._fieldDictionary["Partition"] = partition 
        #These next two fields will have their offset,bitLength,digitLength, and value determined at runtime
        companyPrefix = Field(fieldName="CompanyPrefix",offset=14,bitLength=24,ordinal=4,fieldValue=0,digitLength=6) 
        self._fieldDictionary["CompanyPrefix"] = companyPrefix
        serialReference = Field(fieldName="SerialReference",offset=14,bitLength=24,ordinal=5,fieldValue=0,digitLength=6) 
        self._fieldDictionary["SerialReference"] = serialReference
        reserved = Field(fieldName="Reserved",offset=58,bitLength=24,ordinal=6,fieldValue=0,digitLength=0) 
        self._fieldDictionary["Reserved"] = reserved