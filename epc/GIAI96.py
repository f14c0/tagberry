import bitstring
import re
from encoding.EPCNumber import EPCNumber 
from epcerrors.EncodingException import EncodingException
from utils.Partitions import Partitions
from utils.Conversion import Conversion
from gs1.GS1Number import GS1Number
from schema.Field import Field

class GIAI96(EPCNumber):
    '''
    Represents an GIAI-96 EPC Encoding
    The Global Individual Asset Identifier EPC scheme is used to assign a unique identity to
    a specific asset, such as a forklift or a computer.
    '''
    def __init__(self,startSerialNumber=0,numOfSerialNumbers=0):
        EPCNumber.__init__(self)
        self._loadFields()
        self._encodingType="GIAI96"
    
    def encode(self,companyPrefix,indicatorDigit,itemReference,filter_value,serialNumber=0):
        """
        encodes an GIAI-96. 
        """
        #Reload fields
        self._loadFields()
        #Get ref to conversion class
        conversion = Conversion()
        #Filter
        self.setFieldValue("Filter",filter_value)
        
        #Partition
        partition = Partitions()
        partitionValue = partition.getPartitionValue(len(companyPrefix), "GIAI")
        self.setFieldValue("Partition",conversion.uint32(partitionValue))
        #Company Prefix
        companyPrefixField = self.getField("CompanyPrefix")
        companyPrefixField.setBitLength(partition.getCompanyPrefixBitLength(partitionValue,"GIAI"))
        companyPrefixField.setDigitLength(partition.getCompanyPrefixDigitLength(partitionValue,"GIAI"))
        self.setFieldValue("CompanyPrefix",companyPrefix)
        
        #ItemReference
        individualAssetReferenceField = self.getField("IndividualAssetReference")
        individualAssetReferenceField.setBitLength(partition.getItemBitLength(partitionValue, "GIAI"))
        individualAssetReferenceField.setDigitLength(partition.getItemDigitLength(partitionValue, "GIAI"))
        individualAssetReferenceField.setOffset(int(companyPrefixField.getBitLength()) + int(companyPrefixField.getOffset()))
        self.setFieldValue("IndividualAssetReference",itemReference)
        
        #Set the PackString Format
        self._packStringFormat = 'uint:8, uint:3, uint:3, uint:%s, uint:%s' % (companyPrefixField.getBitLength(),individualAssetReferenceField.getBitLength())
        #Pack the bitstring
        bsp=  bitstring.pack(self._packStringFormat, 
                                self.getFieldValue("Header"), 
                                self.getFieldValue("Filter"),
                                self.getFieldValue("Partition"), 
                                self.getFieldValue("CompanyPrefix"), 
                                self.getFieldValue("IndividualAssetReference"))
                                
         
        #Set the _bits for the GIAI-96
        self._bits = bsp.unpack("bin")[0][2:]
        
        return self
    def setSerialNumber(self,value):
        self.setFieldValue("IndividualAssetReference",value)
    
    
    def setFieldValue(self,fieldName,val):
        """
        Overriden from the base class because if the SerialNumber changes the indicator digit must be preserved
        otherwise its a straight exchange
        """
        field = self._fieldDictionary[fieldName]
        field.setFieldValue(val)
        
        self._updateBitString()
    
    def _updateBitString(self):
        self._packStringFormat = 'uint:8, uint:3, uint:3, uint:%s, uint:%s' % (self.getField("CompanyPrefix").getBitLength(),self.getField("IndividualAssetReference").getBitLength())
        #Pack the bitstring
        bsp=  bitstring.pack(self._packStringFormat, 
                               self.getFieldValue("Header"), 
                               self.getFieldValue("Filter"),
                               self.getFieldValue("Partition"), 
                               self.getFieldValue("CompanyPrefix"), 
                               self.getFieldValue("IndividualAssetReference"))
        
        #Set the _bits for the SGTIN-96
        self._bits = bsp.unpack("bin")[0][2:]
     
    def _decodeFromBinary(self,binary):
        '''
        Decodes an GIAI-96 from BINARY string
        '''
        self._loadFields()
        if(len(binary)!=96):
            raise EncodingException("Binary string is not 96 bits. GIAI-96 Requires 96 bits to decode properly")
        
        
        
        #Filter
        filter = binary[self.getField("Filter").getOffset():self.getField("Filter").getOffset() + self.getField("Filter").getBitLength()]
        self.setFieldValue("Filter",int(filter,2))
        partitionValue = binary[self.getField("Partition").getOffset():self.getField("Partition").getOffset() + self.getField("Partition").getBitLength()]
        partitionValue = int(partitionValue,2)
        self.setFieldValue("Partition",partitionValue)
        
        #Partition
        partitions = Partitions()
        companyPrefixLength = partitions.getCompanyPrefixBitLength(partitionValue,"GIAI")
        companyPrefixDigitLength = partitions.getCompanyPrefixDigitLength(partitionValue,"GIAI")
        self.getField("CompanyPrefix").setOffset(14)
        self.getField("CompanyPrefix").setBitLength(companyPrefixLength)
        self.getField("CompanyPrefix").setDigitLength(companyPrefixDigitLength)
        individualAssetReferenceLength = partitions.getItemBitLength(partitionValue,"GIAI")
        individualAssetReferenceDigitLength = partitions.getItemDigitLength(partitionValue,"GIAI")
        
        self.getField("IndividualAssetReference").setOffset(14 + companyPrefixLength)
        self.getField("IndividualAssetReference").setBitLength(individualAssetReferenceLength)
        self.getField("IndividualAssetReference").setDigitLength(individualAssetReferenceDigitLength)
        
        companyPrefix = binary[self.getField("CompanyPrefix").getOffset():self.getField("CompanyPrefix").getOffset() + self.getField("CompanyPrefix").getBitLength()]
        companyPrefix = str(int(companyPrefix,2)).zfill(companyPrefixDigitLength)
        self.setFieldValue("CompanyPrefix",companyPrefix)
        individualAssetReference = binary[self.getField("IndividualAssetReference").getOffset():self.getField("IndividualAssetReference").getOffset() + self.getField("IndividualAssetReference").getBitLength()]
        #make sure we are on a 1 byte boundary
        
       
        individualAssetReference = str(int(individualAssetReference,2))
        
        self.setFieldValue("IndividualAssetReference", individualAssetReference)
       
        
        
        return self    
    
    def fromEPCUri(self,epcUri):
        '''Parses the EPC from a epcURI - urn:tagpy:id:giai:0358468.202339'''
        regEx = re.compile("\d+")
        s = regEx.findall(epcUri)
        companyPrefix = s[0]
        itemReference = s[1]
        #set the filter value to 0
        filter = 0
        self.encode(companyPrefix,None,itemReference, filter, None)
        return self;
    
    def fromTagUri(self,tagUri):
        '''Parses the EPC from a TagURI'''
        regEx = re.compile("\d+")
        s = regEx.findall(tagUri)
        filter = s[1]
        companyPrefix = s[2]
        itemReference = s[3]
        self.encode(companyPrefix, None, itemReference, filter, None)
        return self
     
    def toEPCUri(self):
        '''
        Returns the GIAI-96 in an EPC Pure Identity
        Example: urn:tagpy:id:sgtin:0614141.812345.6789
        '''
        epcUri = "urn:tagpy:id:giai:%s.%s" % (self.getFieldValue("CompanyPrefix"),self.getFieldValue("IndividualAssetReference"))
        return epcUri
    
    def toEPCTagUri(self):
        '''
        Returns the GIAI-96 in an EPC URI Representation
        Example: urn:tagpy:tag:giai-96:3.0614141.812345
        '''
        epcUri = "urn:tagpy:tag:sgtin-96:%s.%s.%s" % (self.getFieldValue("Filter"),self.getFieldValue("CompanyPrefix"),self.getFieldValue("IndividualAssetReference"))
        return epcUri
    
    def toGS1(self,includeAppIdentifier=False,serialNumberLength=0,useParens=True):
        '''
        Returns the GIAI GS1 Encoding - with or without AIs 8004
        
        includeAppIdentifier
        Use the includeAppIdentifier to indicate that the GS1 value should be returned with AIs.
        
        serialNumberLength
        Use the serialNumberLength to indicate that a fixed length serial number is expected. The default is zero.
        
        useParens
        If this is set to true, the GS1 number will have parens wrapped around the AIs if not there will be no parens
        
        NOTE:
        This method only deals with two AIs 01 and 21.
        '''
        
        giai = self.getFieldValue("CompanyPrefix")+self.getFieldValue("IndividualAssetReference")
        
        
        gs1Number = GS1Number()
        cd = gs1Number._calculateCheckDigit(giai) 
        
        if(includeAppIdentifier==False):
            gs1 = "%s%s" % (giai,cd)
        else:
            
            if(useParens):
                gs1 = "(8004)%s" % giai
            else:
                gs1 = "8004%s" % giai
            
        return gs1
    
    def toXml(self):
        xml = "<Tag type='%s'>\n" % (self._encodingType)
        xml += "\t<Fields>\n"
        xml +=  "\t\t<Field name='Header' value='%s'/>\n" % (self.getFieldValue("Header"))
        xml +=  "\t\t<Field name='Filter' value='%s'/>\n"% (self.getFieldValue("Filter"))
        xml +=  "\t\t<Field name='Partition' value='%s'/>\n" % (self.getFieldValue("Partition"))
        xml +=  "\t\t<Field name='CompanyPrefix' value='%s'/>\n" % (self.getFieldValue("CompanyPrefix"))
        xml +=  "\t\t<Field name='IndividualAssetReference' value='%s'/>\n" % (self.getFieldValue("IndividualAssetReference"))
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
            ('IndividualAssetReference',self.getFieldValue("IndividualAssetReference")),\
            ('Hex',self.toHex()),\
            ('Binary',self.toBinary()),\
            ('TagURI',self.toEPCTagUri()),\
            ('TagRawURI',self.toEPCRawUri()),\
            ('PureIdentity',self.toEPCUri()),\
            ('GS1',self.toGS1())])
        
    def _loadFields(self):
        """
        Loads Fields for the GIAI-96 
        """
        header = Field(fieldName="Header",offset=0,bitLength=8,ordinal=1,fieldValue=52,digitLength=2)
        self.fieldDictionary["Header"] = header
        filter = Field(fieldName="Filter",offset=8,bitLength=3,ordinal=2,fieldValue=0,digitLength=1) 
        self.fieldDictionary["Filter"] = filter
        partition = Field(fieldName="Partition",offset=11,bitLength=3,ordinal=3,fieldValue=0,digitLength=1) 
        self.fieldDictionary["Partition"] = partition 
        #These next two fields will have their offset,bitLength,digitLength, and value determined at runtime
        companyPrefix = Field(fieldName="CompanyPrefix",offset=14,bitLength=24,ordinal=4,fieldValue=0,digitLength=6) 
        self.fieldDictionary["CompanyPrefix"] = companyPrefix
        assetReference = Field(fieldName="IndividualAssetReference",offset=21,bitLength=24,ordinal=5,fieldValue=0,digitLength=6) 
        self.fieldDictionary["IndividualAssetReference"] = assetReference
        