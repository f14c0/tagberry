import bitstring
from encoding.EPCNumber import EPCNumber
from epcerrors.EncodingException import EncodingException
from utils.Partitions import Partitions
from utils.Conversion import Conversion
from gs1.GS1Number import GS1Number

import re 
class GSRN96(EPCNumber):
    '''Represents an GSRN-96 EPC Encoding'''
    def __init__(self,startSerialNumber=0,numOfSerialNumbers=0):
        EPCNumber.__init__(self)
        self._loadFields()
        self._ignoreUpdate = False
        self._encodingType="GSRN-96"
    
    def encode(self, companyPrefix, indicatorDigit, serviceReference, filter_value, reserved=0):
        """
        encodes an GSRN-96. 
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
        partitionValue = partition.getPartitionValue(len(companyPrefix), "GSRN")
        self.setFieldValue("Partition",conversion.uint32(partitionValue))
        #Company Prefix
        companyPrefixField = self.getField("CompanyPrefix")
        companyPrefixField.setBitLength(partition.getCompanyPrefixBitLength(partitionValue,"GSRN"))
        companyPrefixField.setDigitLength(partition.getCompanyPrefixDigitLength(partitionValue,"GSRN"))
        self.setFieldValue("CompanyPrefix",companyPrefix)
        
        #ServiceReference
        serviceReferenceField = self.getField("ServiceReference")
        serviceReferenceField.setBitLength(partition.getItemBitLength(partitionValue, "GSRN"))
        serviceReferenceField.setDigitLength(partition.getItemDigitLength(partitionValue, "GSRN"))
        serviceReferenceField.setOffset(int(companyPrefixField.getBitLength()) + int(companyPrefixField.getOffset()))
        self._ignoreUpdate=True
        self.setFieldValue("ServiceReference","%s" % str(serviceReference))
        self._ignoreUpdate=False
        #Reserved
        serialNumberField = self.getField("Reserved")
        serialNumberField.setDigitLength(len(str(0)))
       
        self.setFieldValue("Reserved",0)
        
        #Set the PackString Format
        self._packStringFormat = 'uint:8, uint:3, uint:3, uint:%s, uint:%s, uint:24' % (companyPrefixField.getBitLength(),serviceReferenceField.getBitLength())
        #Pack the bitstring
        bsp=  bitstring.pack(self._packStringFormat, 
                                self.getFieldValue("Header"), 
                                self.getFieldValue("Filter"),
                                self.getFieldValue("Partition"), 
                                self.getFieldValue("CompanyPrefix"), 
                                self.getFieldValue("ServiceReference"),
                                self.getFieldValue("Reserved"))
         
        #Set the _bits for the GSRN-96
        self._bits = bsp.unpack("bin")[0][2:]
        
        return self
   
    def _updateBitString(self):
        self._packStringFormat = 'uint:8, uint:3, uint:3, uint:%s, uint:%s, uint:24' % (self.getField("CompanyPrefix").getBitLength(),self.getField("ServiceReference").getBitLength())
        #Pack the bitstring
        bsp=  bitstring.pack(self._packStringFormat, 
                           self.getFieldValue("Header"), 
                           self.getFieldValue("Filter"),
                           self.getFieldValue("Partition"), 
                           self.getFieldValue("CompanyPrefix"), 
                           self.getFieldValue("ServiceReference"),
                           self.getFieldValue("Reserved"))
        
        #Set the _bits for the GSRN-96
        self._bits = bsp.unpack("bin")[0][2:]
    
    def toEPCTagUri(self):
        '''
        Returns the GSRN-96 in an EPC URI Representation
        Example: urn:tagpy:tag:gsrn-96:3.0614141.812345
        '''
        epcUri = "urn:tagpy:tag:sgrn-96:%s.%s.%s" % (self.getFieldValue("Filter"),self.getFieldValue("CompanyPrefix"),self.getFieldValue("ServiceReference"))
        return epcUri
    
    def toGS1(self,includeAppIdentifier=False,serialNumberLength=0,useParens=True):
        '''
        Returns the GSRN GS1 Encoding - with or without AIs
        
        includeAppIdentifier
        Use the includeAppIdentifier to indicate that the GS1 value should be returned with AIs.
        
        serialNumberLength
        Use the serialNumberLength to indicate that a fixed length serial number is expected. The default is zero.
        
        useParens
        If this is set to true, the GS1 number will have parens wrapped around the AIs if not there will be no parens
        
        NOTE:
        This method only deals with two AIs 01 and 21.
        '''
        
        gdti = self.getFieldValue("CompanyPrefix")+self.getFieldValue("ServiceReference")
        gs1Number = GS1Number()
        cd = gs1Number._calculateCheckDigit(gdti) 
        
        if(includeAppIdentifier==False):
            gs1 = "%s%s" % (gdti,cd)
        else:
            if(useParens):
                gs1 = "(8018)%s%s" % (gdti,cd)     
            else:    
                gs1 = "8018%s%s" % (gdti,cd)
        return gs1
    
    def toXml(self):
        xml = "<Tag type='%s'>\n" % (self._encodingType)
        xml += "\t<Fields>\n"
        xml +=  "\t\t<Field name='Header' value='%s'/>\n" % (self.getFieldValue("Header"))
        xml +=  "\t\t<Field name='Filter' value='%s'/>\n"% (self.getFieldValue("Filter"))
        xml +=  "\t\t<Field name='Partition' value='%s'/>\n" % (self.getFieldValue("Partition"))
        xml +=  "\t\t<Field name='CompanyPrefix' value='%s'/>\n" % (self.getFieldValue("CompanyPrefix"))
        xml +=  "\t\t<Field name='ServiceReference' value='%s'/>\n" % (self.getFieldValue("ServiceReference"))
        xml +=  "\t\t<Field name='Reserved' value='%s'/>\n" % (self.getFieldValue("Reserved"))
        xml += "\t</Fields>\n"
        xml += "\t<Hex>%s</Hex>\n" % (self.toHex())
        xml += "\t<Binary>%s</Binary>\n" % (self.toBinary())
        xml += "\t<TagUri>%s</TagUri>\n" % (self.toEPCTagUri())
        xml += "\t<TagRawUri>%s</TagRawUri>\n" % (self.toEPCRawUri())
        xml += "\t<PureIdentity>%s</PureIdentity>\n" % (self.toEPCUri())
        xml += "\t<GS1>%s</GS1>\n" % (self.toGS1())
        xml += "</Tag>"
        return xml;
    
    def toDictionary(self):
        return dict([('Type',self._encodingType),\
                ('Header',self.getFieldValue("Header")),\
                ('Filter',self.getFieldValue("Filter")),\
                ('Partition',self.getFieldValue("Partition")),\
                ('CompanyPrefix',self.getFieldValue("CompanyPrefix")),\
                ('ServiceReference',self.getFieldValue("ServiceReference")),\
                ('Reserved',self.getFieldValue("Reserved")),\
                ('Hex',self.toHex()),\
                ('Binary',self.toBinary()),\
                ('TagURI',self.toEPCTagUri()),\
                ('TagRawURI',self.toEPCRawUri()),\
                ('PureIdentity',self.toEPCUri()),\
                ('GS1',self.toGS1())])
    
    def setSerialNumber(self,value):
        self.setFieldValue("ServiceReference",value)
    def getSerialNumber(self):
        return self.getFieldValue("ServiceReference")
    
    def setFieldValue(self,fieldName,val):
        """
        Overriden from the base class for serial ref changes
        """
        field = self._fieldDictionary[fieldName]
        field.setFieldValue(val)
        
        self._updateBitString()
    
   
    
    def fromEPCUri(self,epcUri):
        '''Parses the EPC from a epcURI - urn:tagpy:id:gsrn:0358468.202339'''
        regEx = re.compile("\d+")
        s = regEx.findall(epcUri)
        companyPrefix = s[0] 
        serviceReference = s[1]
        #set the filter value to 0
        filter = 0
        self.encode(companyPrefix, 0, serviceReference, filter, 0)
        return self;
    
    def fromTagUri(self,tagUri):
        '''Parses the EPC from a TagURI'''
        regEx = re.compile("\d+")
        s = regEx.findall(tagUri)
        companyPrefix = s[1]
        serviceReference = s[2]
        self.encode(companyPrefix,0,serviceReference, 0, 0)
        return self
    
    def toEPCUri(self):
        '''Returns the GSRN-96 in an EPC URI Representation'''
        epcUri = "urn:tagpy:id:gsrn:%s.%s" % (self.getFieldValue("CompanyPrefix"),self.getFieldValue("ServiceReference"))
        return epcUri 
    
    def _decodeFromBinary(self,binary):
        '''
        Decodes a GSRN from BINARY string
        '''
        self._loadFields()
        if(len(binary)!=96):
            raise EncodingException("Binary string is not 96 bits. GSRN-96 Requires 96 bits to decode properly")
        
        
        
        #Filter
        filter = binary[self.getField("Filter").getOffset():self.getField("Filter").getOffset() + self.getField("Filter").getBitLength()]
        self.setFieldValue("Filter",int(filter,2))
        partitionValue = binary[self.getField("Partition").getOffset():self.getField("Partition").getOffset() + self.getField("Partition").getBitLength()]
        partitionValue = int(partitionValue,2)
        self.setFieldValue("Partition",partitionValue)
        
        #Partition
        partitions = Partitions()
        companyPrefixLength = partitions.getCompanyPrefixBitLength(partitionValue,"GSRN")
        companyPrefixDigitLength = partitions.getCompanyPrefixDigitLength(partitionValue,"GSRN")
        self.getField("CompanyPrefix").setOffset(14)
        self.getField("CompanyPrefix").setBitLength(companyPrefixLength)
        self.getField("CompanyPrefix").setDigitLength(companyPrefixDigitLength)
        serviceReferenceLength = partitions.getItemBitLength(partitionValue,"GSRN")
        serviceReferenceDigitLength = partitions.getItemDigitLength(partitionValue,"GSRN")
        
        self.getField("ServiceReference").setOffset(14 + companyPrefixLength)
        self.getField("ServiceReference").setBitLength(serviceReferenceLength)
        self.getField("ServiceReference").setDigitLength(serviceReferenceDigitLength)
        
        companyPrefix = binary[self.getField("CompanyPrefix").getOffset():self.getField("CompanyPrefix").getOffset() + self.getField("CompanyPrefix").getBitLength()]
        companyPrefix = str(int(companyPrefix,2)).zfill(companyPrefixDigitLength)
        self.setFieldValue("CompanyPrefix",companyPrefix)
        serviceReference = binary[self.getField("ServiceReference").getOffset():self.getField("ServiceReference").getOffset() + self.getField("ServiceReference").getBitLength()]
        #make sure we are on a 1 byte boundary
        
       
        serviceReference = str(int(serviceReference,2)).zfill(serviceReferenceDigitLength)
        
        self._ignoreUpdate = True
        self.setFieldValue("ServiceReference", serviceReference)
        self._ignoreUpdate = False
        reserved = binary[self.getField("Reserved").getOffset():self.getField("Reserved").getOffset() + self.getField("Reserved").getBitLength()]
        reserved = int(reserved,2)
        self.setFieldValue("Reserved",reserved)
        
        return self
        
    def _loadFields(self):
        """
        Loads Fields for the GSRN-96 
        """
        header = Field(fieldName="Header",offset=0,bitLength=8,ordinal=1,fieldValue=45,digitLength=2)
        self.fieldDictionary["Header"] = header
        filter = Field(fieldName="Filter",offset=8,bitLength=3,ordinal=2,fieldValue=0,digitLength=1) 
        self.fieldDictionary["Filter"] = filter
        partition = Field(fieldName="Partition",offset=11,bitLength=3,ordinal=3,fieldValue=0,digitLength=1) 
        self.fieldDictionary["Partition"] = partition 
        #These next two fields will have their offset,bitLength,digitLength, and value determined at runtime
        companyPrefix = Field(fieldName="CompanyPrefix",offset=14,bitLength=24,ordinal=4,fieldValue=0,digitLength=6) 
        self.fieldDictionary["CompanyPrefix"] = companyPrefix
        serviceReference = Field(fieldName="ServiceReference",offset=21,bitLength=24,ordinal=5,fieldValue=0,digitLength=6) 
        self.fieldDictionary["ServiceReference"] = serviceReference
        reserved = Field(fieldName="Reserved",offset=72,bitLength=24,ordinal=6,fieldValue=0,digitLength=0) 
        self.fieldDictionary["Reserved"] = reserved