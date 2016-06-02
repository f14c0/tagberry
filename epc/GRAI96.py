import re
import bitstring
from epc.EPCNumber import EPCNumber 
from epcerrors.EncodingException import EncodingException
from utils.Partitions import Partitions
from utils.Conversion import Conversion
from gs1.GRAI import GRAI
from schema.Field import Field

class GRAI96(EPCNumber):
    '''
    Represents an GRAI-96 EPC Encoding
    The Global Returnable Asset Identifier EPC scheme is used to assign a unique identity to
    a specific returnable asset, such as a reusable shipping container or a pallet skid.
    '''
    def __init__(self,startSerialNumber=0,numOfSerialNumbers=0):
        EPCNumber.__init__(self)
        self._loadFields()
        self._encodingType="GRAI96"
    
    def setSerialNumber(self,value):
        self.setFieldValue("Serial", value)
    def getSerialNumber(self):
        return self.getFieldValue("Serial")
    
    def encode(self,companyPrefix, assetType, filter_value=0, serialNumber=0):
        """
        encodes an GRAI-96. 
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
        partitionValue = partition.getPartitionValue(len(companyPrefix), "GRAI")
        self.setFieldValue("Partition",conversion.uint32(partitionValue))
        #Company Prefix
        companyPrefixField = self.getField("CompanyPrefix")
        companyPrefixField.setBitLength(partition.getCompanyPrefixBitLength(partitionValue,"GRAI"))
        companyPrefixField.setDigitLength(partition.getCompanyPrefixDigitLength(partitionValue,"GRAI"))
        self.setFieldValue("CompanyPrefix",companyPrefix)
        
        #ItemReference
        assetTypeField = self.getField("AssetType")
        assetTypeField.setBitLength(partition.getItemBitLength(partitionValue, "GRAI"))
        assetTypeField.setDigitLength(partition.getItemDigitLength(partitionValue, "GRAI"))
        assetTypeField.setOffset(int(companyPrefixField.getBitLength()) + int(companyPrefixField.getOffset()))
        self.setFieldValue("AssetType", str(assetType))
        #SerialNumber
        serialNumberField = self.getField("Serial")
        serialNumberField.setDigitLength(len(str(serialNumber)))
       
        self.setFieldValue("Serial",serialNumber)
        
        #Set the PackString Format
        self._packStringFormat = 'uint:8, uint:3, uint:3, uint:%s, uint:%s, uint:38' % (companyPrefixField.getBitLength(),assetTypeField.getBitLength())
        #Pack the bitstring
        bsp=  bitstring.pack(self._packStringFormat, 
                                self.getFieldValue("Header"), 
                                self.getFieldValue("Filter"),
                                self.getFieldValue("Partition"), 
                                self.getFieldValue("CompanyPrefix"), 
                                self.getFieldValue("AssetType"),
                                self.getFieldValue("Serial"))
         
        #Set the _bits for the GRAI-96
        self._bits = bsp.unpack("bin")[0][2:]
        
        return self
    
        
    def toEPCUri(self):
        '''Returns the GRAI-96 in an EPC URI Representation'''
        if(len(self.getFieldValue("CompanyPrefix"))+len(self.getFieldValue("AssetType")) != 12):
            raise EncodingException("The Length of the CompanyPrefix and the AssetType must equal 12")
        epcUri = "urn:tagpy:id:grai:%s.%s.%s" % (self.getFieldValue("CompanyPrefix"),self.getFieldValue("AssetType"),self.getFieldValue("Serial"))
        return epcUri
    
    def fromEPCUri(self,epcUri):
        '''Parses the EPC from a epcURI - urn:tagpy:id:grai:0358468.202339.000395'''
        regEx = re.compile("\d+")
        s = regEx.findall(epcUri)
        companyPrefix = s[0]
        itemReference = s[1]
        #set the filter value to 0
        filter = 0
        serialNumber = s[2]
        self.encode(companyPrefix, None, itemReference, filter, serialNumber)
        return self;
    
    def fromTagUri(self,tagUri):
        '''Parses the EPC from a TagURI'''
        regEx = re.compile("\d+")
        s = regEx.findall(tagUri)
        filter = s[1]
        companyPrefix = s[2]
        itemReference = s[3]
        serialNumber = s[4]
        self.encode(companyPrefix, None, itemReference, filter, serialNumber)
        return self
            
    def toEPCTagUri(self):
        '''
        Returns the SGTIN-96 in an EPC URI Representation
        Example: urn:tagpy:tag:grai-96:3.0614141.812345.6789
        '''
        epcUri = "urn:tagpy:tag:grai-96:%s.%s.%s.%s" % (self.getFieldValue("Filter"),self.getFieldValue("CompanyPrefix"),self.getFieldValue("AssetType"),self.getFieldValue("Serial"))
        return epcUri
    
    def decodeFromBinary(self,binary):
        '''
        Decodes an GRAI from BINARY string
        '''
        self._loadFields()
        if(len(binary)!=96):
            raise EncodingException("Binary string is not 96 bits. GRAI-96 Requires 96 bits to decode properly")
        
        
        
        #Filter
        filter = binary[self.getField("Filter").getOffset():self.getField("Filter").getOffset() + self.getField("Filter").getBitLength()]
        self.setFieldValue("Filter",int(filter,2))
        partitionValue = binary[self.getField("Partition").getOffset():self.getField("Partition").getOffset() + self.getField("Partition").getBitLength()]
        partitionValue = int(partitionValue,2)
        self.setFieldValue("Partition",partitionValue)
        
        #Partition
        partitions = Partitions()
        companyPrefixLength = partitions.getCompanyPrefixBitLength(partitionValue,"GRAI")
        companyPrefixDigitLength = partitions.getCompanyPrefixDigitLength(partitionValue,"GRAI")
        self.getField("CompanyPrefix").setOffset(14)
        self.getField("CompanyPrefix").setBitLength(companyPrefixLength)
        self.getField("CompanyPrefix").setDigitLength(companyPrefixDigitLength)
        
        assetTypeLength = partitions.getItemBitLength(partitionValue,"GRAI")
        assetTypeDigitLength = partitions.getItemDigitLength(partitionValue,"GRAI")
        
        self.getField("AssetType").setOffset(14 + companyPrefixLength)
        self.getField("AssetType").setBitLength(assetTypeLength)
        self.getField("AssetType").setDigitLength(assetTypeDigitLength)
        
        companyPrefix = binary[self.getField("CompanyPrefix").getOffset():self.getField("CompanyPrefix").getOffset() + self.getField("CompanyPrefix").getBitLength()]
        companyPrefix = str(int(companyPrefix,2)).zfill(companyPrefixDigitLength)
        self.setFieldValue("CompanyPrefix",companyPrefix)
        assetType = binary[self.getField("AssetType").getOffset():self.getField("AssetType").getOffset() + self.getField("AssetType").getBitLength()]
        #make sure we are on a 1 byte boundary
        
        
        assetType = str(int(assetType,2)).zfill(assetTypeDigitLength)
        
        self.setFieldValue("AssetType", assetType)
        serialOffset = 14 + companyPrefixLength + assetTypeLength
        self.getField("Serial").setOffset(serialOffset)
        serialLength = 96 - serialOffset
        self.getField("Serial").setBitLength(serialLength)
        self.getField("Serial").setDigitLength(len(str(pow(2,serialLength))))
        
        serialNumber = binary[serialOffset:]
        serialNumber = int(serialNumber,2)
        self.setFieldValue("Serial",serialNumber)
        
        return self
    
    def toGS1(self,useParenthesesAroundAIs=True):
        '''Returns the EPC epc translated to a full GS1 with App Identifiers''' 
        grai = GRAI(self.getFieldValue("CompanyPrefix"))
        grai.encode(self.getFieldValue("AssetType"), self.getFieldValue("Serial"))
        return grai.toGS1(useParenthesesAroundAIs) 
    
    def toGRAI(self):
        '''Returns the EPC epc translated to a GS1 GRAI with NO App Identifiers'''
        grai = GRAI(self.getFieldValue("CompanyPrefix"))
        grai.encode(self.getFieldValue("AssetType"), self.getFieldValue("Serial"))
        return grai.toGRAI()
        
    def toXml(self):
        xml = "<Tag type='%s'>\n" % (self._encodingType)
        xml += "\t<Fields>\n"
        xml +=  "\t\t<Field name='Header' value='%s'/>\n" % (self.getFieldValue("Header"))
        xml +=  "\t\t<Field name='Filter' value='%s'/>\n"% (self.getFieldValue("Filter"))
        xml +=  "\t\t<Field name='Partition' value='%s'/>\n" % (self.getFieldValue("Partition"))
        xml +=  "\t\t<Field name='CompanyPrefix' value='%s'/>\n" % (self.getFieldValue("CompanyPrefix"))
        xml +=  "\t\t<Field name='ItemReference' value='%s'/>\n" % (self.getFieldValue("AssetType"))
        xml +=  "\t\t<Field name='Serial' value='%s'/>\n" % (self.getFieldValue("Serial"))
        xml += "\t</Fields>\n"
        xml += "\t<Hex>%s</Hex>\n" % (self.toHex())
        xml += "\t<Binary>%s</Binary>\n" % (self.toBinary())
        xml += "\t<TagUri>%s</TagUri>\n" % (self.toEPCTagUri())
        xml += "\t<PureIdentity>%s</PureIdentity>\n" % (self.toEPCUri())
        xml += "\t<GS1>%s</GS1>\n" % (self.toGS1())
        xml += "</Tag>"
        return xml;
    
    def toDictionary(self):
        return dict([('Type',self._encodingType),\
                ('Header',self.getFieldValue("Header")),\
                ('Filter',self.getFieldValue("Filter")),\
                ('Partition',self.getFieldValue("Partition")),\
                ('Company Prefix',self.getFieldValue("CompanyPrefix")),\
                ('Asset Type',self.getFieldValue("AssetType")),\
                ('Serial',self.getFieldValue("Serial")),\
                ('Hex',self.toHex()),\
                ('Binary',self.toBinary()),\
                ('TagURI',self.toEPCTagUri()),\
                ('PureIdentity',self.toEPCUri()),\
                ('GS1',self.toGS1())])
    
    def _updateBitString(self):
       
        #Set the PackString Format
        self._packStringFormat = 'uint:8, uint:3, uint:3, uint:%s, uint:%s, uint:38' % (self.getField("CompanyPrefix").getBitLength(),self.getField("AssetType").getBitLength())
        #Pack the bitstring
        bsp=  bitstring.pack(self._packStringFormat, 
            self.getFieldValue("Header"), 
            self.getFieldValue("Filter"),
            self.getFieldValue("Partition"), 
            self.getFieldValue("CompanyPrefix"), 
            self.getFieldValue("AssetType"),
            self.getFieldValue("Serial"))
        #Set the _bits for the GRAI-96
        self._bits = bsp.unpack("bin")[0][2:] 
    
    def _loadFields(self):
        """
        Loads Fields for the GRAI-96 
        """
        header = Field(fieldName="Header",offset=0,bitLength=8,ordinal=1,fieldValue=51,digitLength=2)
        self.fieldDictionary["Header"] = header
        filter = Field(fieldName="Filter",offset=8,bitLength=3,ordinal=2,fieldValue=0,digitLength=1) 
        self.fieldDictionary["Filter"] = filter
        partition = Field(fieldName="Partition",offset=11,bitLength=3,ordinal=3,fieldValue=0,digitLength=1) 
        self.fieldDictionary["Partition"] = partition 
        #These next two fields will have their offset,bitLength,digitLength, and value determined at runtime
        companyPrefix = Field(fieldName="CompanyPrefix",offset=14,bitLength=24,ordinal=4,fieldValue=0,digitLength=6,isPadded=True) 
        self.fieldDictionary["CompanyPrefix"] = companyPrefix
        assetType = Field(fieldName="AssetType",offset=21,bitLength=24,ordinal=5,fieldValue=0,digitLength=6,isPadded=True) 
        self.fieldDictionary["AssetType"] = assetType
        serial = Field(fieldName="Serial",offset=47,bitLength=38,ordinal=6,fieldValue=0,digitLength=0) 
        self.fieldDictionary["Serial"] = serial