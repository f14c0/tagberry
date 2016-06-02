import re
import bitstring
from epc.EPCNumber import EPCNumber
from epcerrors.EncodingException import EncodingException
from utils.Partitions import Partitions
from utils.Conversion import Conversion
from gs1.GDTI import GDTI
from schema.Field import Field

class GDTI96(EPCNumber):
    '''
    Represents an GDTI-96 EPC Encoding
    The Global Document Type Identifier EPC scheme is used to assign a unique identity to
    a specific document, such as land registration papers, an insurance policy, and others.
    
    Only GDTIs that include the optional serial number may be represented as EPCs. A
    GDTI without a serial number represents a document class, rather than a specific
    document, and therefore may not be used as an EPC (just as a non-serialized GTIN may
    not be used as an EPC).
    '''
    def __init__(self, startSerialNumber=0, numOfSerialNumbers=0):
        EPCNumber.__init__(self)
        self._loadFields()
        self._encodingType="GDTI96"
    
    def encode(self, companyPrefix, documentType, filter_value=None, serialNumber=0):
        """
        encodes an GDTI-96. 
        """
        #Reload fields
        self._loadFields()
        #Get ref to conversion class
        conversion = Conversion()
        #Get the header bits
        
        #Filter
        if filter_value == None:
            filter_value = 0
        
        self.setFieldValue("Filter",filter_value)
        
        #Partition
        partition = Partitions()
        partitionValue = partition.getPartitionValue(len(companyPrefix), "GDTI")
        self.setFieldValue("Partition",conversion.uint32(partitionValue))
        #Company Prefix
        companyPrefixField = self.getField("CompanyPrefix")
        companyPrefixField.setBitLength(partition.getCompanyPrefixBitLength(partitionValue,"GDTI"))
        companyPrefixField.setDigitLength(partition.getCompanyPrefixDigitLength(partitionValue,"GDTI"))
        self.setFieldValue("CompanyPrefix",str(companyPrefix))
        
        #documentType
        documentTypeField = self.getField("DocumentType")
        documentTypeField.setBitLength(partition.getItemBitLength(partitionValue, "GDTI"))
        documentTypeField.setDigitLength(partition.getItemDigitLength(partitionValue, "GDTI"))
        documentTypeField.setOffset(int(companyPrefixField.getBitLength()) + int(companyPrefixField.getOffset()))
        
        self.setFieldValue("DocumentType",documentType)
        
        #SerialNumber
        serialNumberField = self.getField("Serial")
        serialNumberField.setDigitLength(len(str(serialNumber)))
        #there are no leading zeros in a GDTI-96 Serial Number, convert to int
        self.setFieldValue("Serial",int(serialNumber))
        
        #Set the PackString Format
        self._packStringFormat = 'uint:8, uint:3, uint:3, uint:%s, uint:%s, uint:41' % (companyPrefixField.getBitLength(),documentTypeField.getBitLength())
        #Pack the bitstring
        bsp=  bitstring.pack(self._packStringFormat, 
                                self.getFieldValue("Header"), 
                                self.getFieldValue("Filter"),
                                self.getFieldValue("Partition"), 
                                self.getFieldValue("CompanyPrefix"), 
                                self.getFieldValue("DocumentType"),
                                self.getFieldValue("Serial"))
         
        #Set the _bits for the GDTI-96
        self._bits = bsp.unpack("bin")[0][2:]
        
        return self
    
    def _updateBitString(self):
        #Set the PackString Format
        self._packStringFormat = 'uint:8, uint:3, uint:3, uint:%s, uint:%s, uint:41' % (self.getField("CompanyPrefix").getBitLength(),self.getField("DocumentType").getBitLength())
        #Pack the bitstring
        bsp=  bitstring.pack(self._packStringFormat, 
                                 self.getFieldValue("Header"), 
                                 self.getFieldValue("Filter"),
                                 self.getFieldValue("Partition"), 
                                 self.getFieldValue("CompanyPrefix"), 
                                 self.getFieldValue("DocumentType"),
                                 self.getFieldValue("Serial"))
          
        #Set the _bits for the GDTI-96
        self._bits = bsp.unpack("bin")[0][2:]
    
    def fromEPCUri(self,epcUri):
        '''Parses the EPC from a epcURI - urn:tagpy:id:gdti:0358468.202339.000395'''
        regEx = re.compile("\d+")
        s = regEx.findall(epcUri)
        companyPrefix = s[0] 
        documentType = s[1]
        #set the filter value to 0
        filter = 0
        serialNumber = s[2]
        self.encode(companyPrefix, 0, documentType, filter, serialNumber)
        return self;
    
    def fromTagUri(self,tagUri):
        '''
        Parses the EPC from a TagURI
        urn:tagpy:tag:gdti-96:<filter>.<companyPrefix>.<documentType>.<serial>
        ex: urn:tagpy:tag:gdti-96:2.0123345.12345.1234
        '''
        regEx = re.compile("\d+")
        s = regEx.findall(tagUri)
        filter = s[0]
        companyPrefix = s[1]
        documentType = s[2]
        serialNumber = int(s[3])
        self.encode(companyPrefix,0,documentType, filter, serialNumber)
        return self
     
    def toEPCTagUri(self):
        '''
        Returns the GDTI-96 in an EPC URI Representation
        Example: urn:tagpy:tag:gdti-96:3.0614141.812345.6789
        '''
        epcUri = "urn:tagpy:tag:gdti-96:%s.%s.%s.%s" % (self.getFieldValue("Filter"),self.getFieldValue("CompanyPrefix"),self.getFieldValue("DocumentType"),int(self.getFieldValue("Serial")))
        return epcUri
    
    def toGS1(self,useParenthesesAroundAIs=True):
        '''Returns the EPC epc translated to a full GS1 with App Identifiers''' 
        gdti= GDTI(self.getFieldValue("CompanyPrefix"))
        gdti.encode(self.getFieldValue("DocumentType"), self.getSerialNumber())
        return gdti.toGS1(useParenthesesAroundAIs) 
    
    def toGDTI(self,withSerialNumber=False):
        '''
        Returns the GDTI Without AIs and a choice to return with the Serial Number
        The serial number on a GS1 GDTI is optional. However, you cannot translate the GS1 GDTI to an EPC representation without
        the serial number. The parameter 'withSerialNumber', when set to True will return the GDTI with the serial Number.
        The default value for the parameter is False and will not return the serial number with the GDTI
        '''
        gdti = GDTI(self.getFieldValue("CompanyPrefix"))
        gdti.encode(self.getFieldValue("DocumentType"), self.getSerialNumber())
        return gdti.toGDTI(withSerialNumber)
    
    def toXml(self):
        xml = "<Tag type='%s'>\n" % (self._encodingType)
        xml += "\t<Fields>\n"
        xml +=  "\t\t<Field name='Header' value='%s'/>\n" % (self.getFieldValue("Header"))
        xml +=  "\t\t<Field name='Filter' value='%s'/>\n"% (self.getFieldValue("Filter"))
        xml +=  "\t\t<Field name='Partition' value='%s'/>\n" % (self.getFieldValue("Partition"))
        xml +=  "\t\t<Field name='CompanyPrefix' value='%s'/>\n" % (self.getFieldValue("CompanyPrefix"))
        xml +=  "\t\t<Field name='DocumentType' value='%s'/>\n" % (self.getFieldValue("DocumentType"))
        xml +=  "\t\t<Field name='Serial' value='%s'/>\n" % (self.getFieldValue("Serial"))
        xml += "\t</Fields>\n"
        xml += "\t<Hex>%s</Hex>\n" % (self.toHex())
        xml += "\t<Binary>%s</Binary>\n" % (self.toBinary())
        xml += "\t<TagUri>%s</TagUri>\n" % (self.toEPCTagUri())
        xml += "\t<PureIdentity>%s</PureIdentity>\n" % (self.toEPCUri())
        xml += "\t<GS1>%s</GS1>\n" % (self.toGS1())
        xml += "\t<GDTI>%s</GDTI>\n" % (self.toGDTI())
        xml += "</Tag>"
        return xml;
    
    def toDictionary(self):
        return dict([('Type',self._encodingType),\
                ('Header',self.getFieldValue("Header")),\
                ('Filter',self.getFieldValue("Filter")),\
                ('Partition',self.getFieldValue("Partition")),\
                ('Company Prefix',self.getFieldValue("CompanyPrefix")),\
                ('Document Type',self.getFieldValue("DocumentType")),\
                ('Serial',self.getFieldValue("Serial")),\
                ('Hex',self.toHex()),\
                ('Binary',self.toBinary()),\
                ('TagURI',self.toEPCTagUri()),\
                ('PureIdentity',self.toEPCUri()),\
                ('GDTI',self.toGDTI()),\
                ('GS1',self.toGS1())])
    
    def setSerialNumber(self,value):
        self.setFieldValue("Serial",value)
    def getSerialNumber(self):
        return self.getFieldValue("Serial")
    def toEPCUri(self):
        '''Returns the GDTI-96 in an EPC URI Representation'''
        epcUri = "urn:tagpy:id:gdti:%s.%s.%s" % (self.getFieldValue("CompanyPrefix"),self.getFieldValue("DocumentType"),int(self.getFieldValue("Serial")))
        return epcUri
    
    
    def decodeFromBinary(self,binary):
        '''
        Decodes a GDTI from BINARY string
        '''
        self._loadFields()
        if(len(binary)!=96):
            raise EncodingException("Binary string is not 96 bits. GDTI-96 Requires 96 bits to decode properly")
        
        
        
        #Filter
        filter = binary[self.getField("Filter").getOffset():self.getField("Filter").getOffset() + self.getField("Filter").getBitLength()]
        self.setFieldValue("Filter",int(filter,2))
        partitionValue = binary[self.getField("Partition").getOffset():self.getField("Partition").getOffset() + self.getField("Partition").getBitLength()]
        partitionValue = int(partitionValue,2)
        self.setFieldValue("Partition",partitionValue)
        
        #Partition
        partitions = Partitions()
        companyPrefixLength = partitions.getCompanyPrefixBitLength(partitionValue,"GDTI")
        companyPrefixDigitLength = partitions.getCompanyPrefixDigitLength(partitionValue,"GDTI")
        self.getField("CompanyPrefix").setOffset(14)
        self.getField("CompanyPrefix").setBitLength(companyPrefixLength)
        self.getField("CompanyPrefix").setDigitLength(companyPrefixDigitLength)
        documentTypeLength = partitions.getItemBitLength(partitionValue,"GDTI")
        documentTypeDigitLength = partitions.getItemDigitLength(partitionValue,"GDTI")
        
        self.getField("DocumentType").setOffset(14 + companyPrefixLength)
        self.getField("DocumentType").setBitLength(documentTypeLength)
        self.getField("DocumentType").setDigitLength(documentTypeDigitLength)
        
        companyPrefix = binary[self.getField("CompanyPrefix").getOffset():self.getField("CompanyPrefix").getOffset() + self.getField("CompanyPrefix").getBitLength()]
        companyPrefix = str(int(companyPrefix,2)).zfill(companyPrefixDigitLength)
        self.setFieldValue("CompanyPrefix",companyPrefix)
        documentType = binary[self.getField("DocumentType").getOffset():self.getField("DocumentType").getOffset() + self.getField("DocumentType").getBitLength()]
        #make sure we are on a 1 byte boundary
        
       
        documentType = str(int(documentType,2)).zfill(documentTypeDigitLength)
        
        self._ignoreUpdate = True
        self.setFieldValue("DocumentType", documentType)
        self._ignoreUpdate = False
        serialNumber = binary[self.getField("Serial").getOffset():self.getField("Serial").getOffset() + self.getField("Serial").getBitLength()]
        serialNumber = int(serialNumber,2)
        self.setFieldValue("Serial",serialNumber)
        
        return self
        
    def _loadFields(self):
        """
        Loads Fields for the GDTI-96 
        """
        header = Field(fieldName="Header",offset=0,bitLength=8,ordinal=1,fieldValue=44,digitLength=2)
        self.fieldDictionary["Header"] = header
        filter = Field(fieldName="Filter",offset=8,bitLength=3,ordinal=2,fieldValue=0,digitLength=1) 
        self.fieldDictionary["Filter"] = filter
        partition = Field(fieldName="Partition",offset=11,bitLength=3,ordinal=3,fieldValue=0,digitLength=1) 
        self.fieldDictionary["Partition"] = partition 
        #These next two fields will have their offset,bitLength,digitLength, and value determined at runtime
        companyPrefix = Field(fieldName="CompanyPrefix",offset=14,bitLength=24,ordinal=4,fieldValue=0,digitLength=6) 
        self.fieldDictionary["CompanyPrefix"] = companyPrefix
        documentType = Field(fieldName="DocumentType",offset=21,bitLength=24,ordinal=5,fieldValue=0,digitLength=6) 
        self.fieldDictionary["DocumentType"] = documentType
        serial = Field(fieldName="Serial",offset=55,bitLength=41,ordinal=6,fieldValue=0,digitLength=pow(2,41)) 
        self.fieldDictionary["Serial"] = serial