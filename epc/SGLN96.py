import re
import bitstring
from epc.EPCNumber import EPCNumber
from epcerrors.EncodingException import EncodingException
from utils.Partitions import Partitions
from utils.Conversion import Conversion
from gs1.GLN import GLN
from schema.Field import Field

class SGLN96(EPCNumber):
    '''
    Represents an SGLN-96 EPC Encoding
    The Serialized Global Location Number EPC scheme is used to assign a unique identity
    to a physical location, such as a specific building or a specific unit of shelving within a
    warehouse.
    '''
    def __init__(self,startSerialNumber=0,numOfSerialNumbers=0):
        EPCNumber.__init__(self)
        self._loadFields()
        self._encoding_type="SGLN96"
    
    def encode(self,companyPrefix,indicatorDigit,locationReference,filter_value,extension=0):
        """
        encodes an SGLN-96. 
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
        partitionValue = partition.getPartitionValue(len(companyPrefix), "SGLN")
        self.setFieldValue("Partition",conversion.uint32(partitionValue))
        #Company Prefix
        companyPrefixField = self.getField("CompanyPrefix")
        companyPrefixField.setBitLength(partition.getCompanyPrefixBitLength(partitionValue,"SGLN"))
        companyPrefixField.setDigitLength(partition.getCompanyPrefixDigitLength(partitionValue,"SGLN"))
        self.setFieldValue("CompanyPrefix",str(companyPrefix))
        
        #locationReference
        locationReferenceField = self.getField("LocationReference")
        locationReferenceField.setBitLength(partition.getItemBitLength(partitionValue, "SGLN"))
        locationReferenceField.setDigitLength(partition.getItemDigitLength(partitionValue, "SGLN"))
        locationReferenceField.setOffset(int(companyPrefixField.getBitLength()) + int(companyPrefixField.getOffset()))
        
        self.setFieldValue("LocationReference",locationReference)
        
        #SerialNumber
        serialNumberField = self.getField("Extension")
        serialNumberField.setDigitLength(len(str(extension)))
       
        self.setFieldValue("Extension",extension)
        
        #Set the PackString Format
        self._packStringFormat = 'uint:8, uint:3, uint:3, uint:%s, uint:%s, uint:41' % (companyPrefixField.getBitLength(),locationReferenceField.getBitLength())
        #Pack the bitstring
        bsp=  bitstring.pack(self._packStringFormat, 
                                self.getFieldValue("Header"), 
                                self.getFieldValue("Filter"),
                                self.getFieldValue("Partition"), 
                                self.getFieldValue("CompanyPrefix"), 
                                self.getFieldValue("LocationReference"),
                                self.getFieldValue("Extension"))
         
        #Set the _bits for the GDTI-96
        self._bits = bsp.unpack("bin")[0][2:]
        
        return self
    
    def _updateBitString(self):
        #Set the PackString Format
        self._packStringFormat = 'uint:8, uint:3, uint:3, uint:%s, uint:%s, uint:41' % (self.getField("CompanyPrefix").getBitLength(),self.getField("LocationReference").getBitLength())
        #Pack the bitstring
        bsp=  bitstring.pack(self._packStringFormat, 
                                 self.getFieldValue("Header"), 
                                 self.getFieldValue("Filter"),
                                 self.getFieldValue("Partition"), 
                                 self.getFieldValue("CompanyPrefix"), 
                                 self.getFieldValue("LocationReference"),
                                 self.getFieldValue("Extension"))
          
        #Set the _bits for the SGLN-96
        self._bits = bsp.unpack("bin")[0][2:]
    
    def fromEPCUri(self,epcUri):
        '''Parses the EPC from a epcURI - urn:tagpy:id:sgln:0358468.202339.000395'''
        regEx = re.compile("\d+")
        s = regEx.findall(epcUri)
        companyPrefix = s[0] 
        locationReference = s[1]
        extension = s[2]
        #set the filter value to 0
        self.encode(companyPrefix, 0, locationReference, 0, extension)
        return self;
    
    def fromTagUri(self,tagUri):
        '''Parses the EPC from a TagURI'''
        regEx = re.compile("\d+")
        s = regEx.findall(tagUri)
        
        companyPrefix = s[1]
        locationReference = s[2]
        extension = s[3]
        self.encode(companyPrefix,0,locationReference, 0, extension)
        return self
    
    def toEPCTagUri(self):
        '''
        Returns the sgln-96 in an EPC URI Representation
        Example: urn:tagpy:tag:sgln-96:3.0614141.812345.6789
        '''
        epcUri = "urn:tagpy:tag:sgln-96:%s.%s.%s.%s" % (self.getFieldValue("Filter"),self.getFieldValue("CompanyPrefix"),self.getFieldValue("LocationReference"),self.getFieldValue("Extension"))
        return epcUri 
    
    def toGS1(self,useParenthesesAroundAIs=True):
        '''Returns the EPC epc translated to a full GS1 with App Identifiers''' 
        gln = GLN(self.getFieldValue("CompanyPrefix"))
        gln.encode(self.getFieldValue("LocationReference"), self.getFieldValue("Extension"))
        return gln.toGS1(useParenthesesAroundAIs)
    
    def toGLN(self):
        '''Returns the EPC epc translated to a GS1 GLN with NO App Identifiers'''
        gln = GLN(self.getFieldValue("CompanyPrefix"))
        gln.encode(self.getFieldValue("LocationReference"), self.getFieldValue("Extension"))
        return gln.toGLN()
    
    def toXml(self):
        xml = "<Tag type='%s'>\n" % (self._encoding_type)
        xml += "\t<Fields>\n"
        xml +=  "\t\t<Field name='Header' value='%s'/>\n" % (self.getFieldValue("Header"))
        xml +=  "\t\t<Field name='Filter' value='%s'/>\n"% (self.getFieldValue("Filter"))
        xml +=  "\t\t<Field name='Partition' value='%s'/>\n" % (self.getFieldValue("Partition"))
        xml +=  "\t\t<Field name='CompanyPrefix' value='%s'/>\n" % (self.getFieldValue("CompanyPrefix"))
        xml +=  "\t\t<Field name='LocationReference' value='%s'/>\n" % (self.getFieldValue("LocationReference"))
        xml +=  "\t\t<Field name='Extension' value='%s'/>\n" % (self.getFieldValue("Extension"))
        xml += "\t</Fields>\n"
        xml += "\t<Hex>%s</Hex>\n" % (self.toHex())
        xml += "\t<Binary>%s</Binary>\n" % (self.toBinary())
        xml += "\t<TagUri>%s</TagUri>\n" % (self.toEPCTagUri())
        xml += "\t<PureIdentity>%s</PureIdentity>\n" % (self.toEPCUri())
        xml += "\t<GS1>%s</GS1>\n" % (self.toGS1())
        xml += "</Tag>"
        return xml;
    
    def toDictionary(self):
        return dict([('Type',self._encoding_type),\
                ('Header',self.getFieldValue("Header")),\
                ('Filter',self.getFieldValue("Filter")),\
                ('Partition',self.getFieldValue("Partition")),\
                ('CompanyPrefix',self.getFieldValue("CompanyPrefix")),\
                ('LocationReference',self.getFieldValue("LocationReference")),\
                ('Extension',self.getFieldValue("Extension")),\
                ('Hex',self.toHex()),\
                ('Binary',self.toBinary()),\
                ('TagURI',self.toEPCTagUri()),\
                ('PureIdentity',self.toEPCUri()),\
                ('GS1',self.toGS1())])
    
    def toEPCUri(self):
        '''Returns the SGLN-96 in an EPC URI Representation'''
        epcUri = "urn:tagpy:id:sgln:%s.%s.%s" % (self.getFieldValue("CompanyPrefix"),self.getFieldValue("LocationReference"),self.getFieldValue("Extension"))
        return epcUri 
    
    
    def setSerialNumber(self,value):
        self.setFieldValue("Extension",value)
    def serial_number(self):
        return self.getFieldValue("Extension")
    
    def decodeFromBinary(self,binary):
        '''
        Decodes a GDTI from BINARY string
        '''
        self._loadFields()
        if(len(binary)!=96):
            raise EncodingException("Binary string is not 96 bits. SGLN-96 Requires 96 bits to decode properly")
        
        
        
        #Filter
        filter = binary[self.getField("Filter").getOffset():self.getField("Filter").getOffset() + self.getField("Filter").getBitLength()]
        self.setFieldValue("Filter",int(filter,2))
        partitionValue = binary[self.getField("Partition").getOffset():self.getField("Partition").getOffset() + self.getField("Partition").getBitLength()]
        partitionValue = int(partitionValue,2)
        self.setFieldValue("Partition",partitionValue)
        
        #Partition
        partitions = Partitions()
        companyPrefixLength = partitions.getCompanyPrefixBitLength(partitionValue,"SGLN")
        companyPrefixDigitLength = partitions.getCompanyPrefixDigitLength(partitionValue,"SGLN")
        self.getField("CompanyPrefix").setOffset(14)
        self.getField("CompanyPrefix").setBitLength(companyPrefixLength)
        self.getField("CompanyPrefix").setDigitLength(companyPrefixDigitLength)
        locationReferenceLength = partitions.getItemBitLength(partitionValue,"SGLN")
        locationReferenceDigitLength = partitions.getItemDigitLength(partitionValue,"SGLN")
        
        self.getField("LocationReference").setOffset(14 + companyPrefixLength)
        self.getField("LocationReference").setBitLength(locationReferenceLength)
        self.getField("LocationReference").setDigitLength(locationReferenceDigitLength)
        
        companyPrefix = binary[self.getField("CompanyPrefix").getOffset():self.getField("CompanyPrefix").getOffset() + self.getField("CompanyPrefix").getBitLength()]
        companyPrefix = str(int(companyPrefix,2)).zfill(companyPrefixDigitLength)
        self.setFieldValue("CompanyPrefix",companyPrefix)
        locationReference = binary[self.getField("LocationReference").getOffset():self.getField("LocationReference").getOffset() + self.getField("LocationReference").getBitLength()]
        #make sure we are on a 1 byte boundary
        
       
        locationReference = str(int(locationReference,2)).zfill(locationReferenceDigitLength)
        
        self._ignoreUpdate = True
        self.setFieldValue("LocationReference", locationReference)
        self._ignoreUpdate = False
        extension = binary[self.getField("Extension").getOffset():self.getField("Extension").getOffset() + self.getField("Extension").getBitLength()]
        extension = int(extension,2)
        self.setFieldValue("Extension",extension)
        
        return self
     
    def _loadFields(self):
        """
        Loads Fields for the SGLN-96 
        """
        header = Field(fieldName="Header",offset=0,bitLength=8,ordinal=1,fieldValue=50,digitLength=2)
        self.fieldDictionary["Header"] = header
        filter = Field(fieldName="Filter",offset=8,bitLength=3,ordinal=2,fieldValue=0,digitLength=1) 
        self.fieldDictionary["Filter"] = filter
        partition = Field(fieldName="Partition",offset=11,bitLength=3,ordinal=3,fieldValue=0,digitLength=1) 
        self.fieldDictionary["Partition"] = partition 
        #These next two fields will have their offset,bitLength,digitLength, and value determined at runtime
        companyPrefix = Field(fieldName="CompanyPrefix",offset=14,bitLength=24,ordinal=4,fieldValue=0,digitLength=6) 
        self.fieldDictionary["CompanyPrefix"] = companyPrefix
        locationReference = Field(fieldName="LocationReference",offset=21,bitLength=24,ordinal=5,fieldValue=0,digitLength=6) 
        self.fieldDictionary["LocationReference"] = locationReference
        extension = Field(fieldName="Extension",offset=14+41,bitLength=41,ordinal=6,fieldValue=0,digitLength=0) 
        self.fieldDictionary["Extension"] = extension