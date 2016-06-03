import re
import bitstring
from epc.EPCNumber import EPCNumber
from epcerrors.EncodingException import EncodingException
from utils.Partitions import Partitions
from utils.Conversion import Conversion
from schema.Field import Field
from gs1.GTIN import GTIN  
from epcerrors.FieldValueException import FieldValueException
import math
from epcerrors import InvalidSerialNumber

class SGTIN96(EPCNumber):
    '''
    Represents an SGTIN-96 EPC Encoding
    '''
    
    def __init__(self, startSerialNumber=0, numOfSerialNumbers=0, fixedSerialNumberLength=0):
        """
        Constructor for SGTIN96
        
        Args:
        startSerialNumber (Optional[int]): Used to seed the starting serial number for the SGTIN-96
        numOfSerialNumbers (Optional[int]): Used to set the number of serial numbers used by the SGTIN-96
        fixedSerialNumberLength (Optional[int]): Used to instruct tagberry that this SGTIN-96 will have 
                                                 a fixed-length serial number. 
        
        """
        EPCNumber.__init__(self, startSerialNumber, numOfSerialNumbers, fixedSerialNumberLength)
        self._loadFields()
        self._ignoreUpdate = False
        self._fixedSerialNumberLength = fixedSerialNumberLength
        self._encodingType="SGTIN96"
    
    def encode(self, *args, **kwargs):       
        """
        Encodes an SGTIN-96 with the values supplied in **kwargs.
        Args:
            *args:
                Empty and ignored
            **kwargs:
                companyPrefix 
                indicatorDigit - default is 0
                itemReference
                filter - default is 3
                serialNumber - default is 0
        Returns:
           EPCNumber : An encode instance of an SGTIN-96  
        """
        self._loadFields()
        conversion = Conversion()
        
        companyPrefix = kwargs.get("companyPrefix")
        indicatorDigit = kwargs.get("indicatorDigit", 0)
        itemReference = kwargs.get("itemReference")
        filter_val = kwargs.get("filter", 3)
        serialNumber = kwargs.get("serialNumber", 0)
        
        #Filter
        self.setFieldValue("Filter", filter_val)
        
        #Partition
        partition = Partitions()
        
        partitionValue = partition.getPartitionValue(len(companyPrefix), "SGTIN")
        self.setFieldValue("Partition", conversion.uint32(partitionValue))
        #Company Prefix
        companyPrefixField = self.getField("CompanyPrefix")
        companyPrefixField.setBitLength(partition.getCompanyPrefixBitLength(partitionValue, "SGTIN"))
        companyPrefixField.setDigitLength(partition.getCompanyPrefixDigitLength(partitionValue, "SGTIN"))
        self.setFieldValue("CompanyPrefix", companyPrefix)
        
        #ItemReference
        itemReferenceField = self.getField("ItemReference")
        itemReferenceField.setBitLength(partition.getItemBitLength(partitionValue, "SGTIN"))
        itemReferenceField.setDigitLength(partition.getItemDigitLength(partitionValue, "SGTIN"))
        itemReferenceField.setOffset(int(companyPrefixField.getBitLength()) + int(companyPrefixField.getOffset()))
        self._ignoreUpdate=True
        
        self.setItemReference(itemReference)
        self.setIndicatorDigit(indicatorDigit)
        self.setFieldValue("ItemReference","%s%s" % (str(indicatorDigit),str(itemReference)), True)
        self._ignoreUpdate=False
        
        #SerialNumber
        serialNumberField = self.getField("SerialNumber")
        serialNumberField.setDigitLength(len(str(serialNumber)))
       
        self.setFieldValue("SerialNumber",serialNumber)
        
        #Set the PackString Format
        self._packStringFormat = 'uint:8, uint:3, uint:3, uint:%s, uint:%s, uint:38' % (companyPrefixField.getBitLength(), itemReferenceField.getBitLength())
        #Pack the bitstring
        bsp =  bitstring.pack(self._packStringFormat, 
                                self.getFieldValue("Header"), 
                                self.getFieldValue("Filter"),
                                self.getFieldValue("Partition"), 
                                self.getFieldValue("CompanyPrefix"), 
                                self.getFieldValue("ItemReference"),
                                int(self.getFieldValue("SerialNumber")))
         
        #Set the _bits for the SGTIN-96
        self._bits = bsp.unpack("bin")[0]
        
        return self
    
    @property
    def serialnumber(self, value):
        '''
        Gets method for a Serial Number.
                        
        Example:
            >>> sgtin = EPCFactory.create("SGTIN96")
            >>> sgtin.serialnumber = 123456
            >>> print(sgtin.serialnumber)
        
        Returns:
            int: The current serial number for the encoding
        
        '''
        return self.getFieldValue("SerialNumber")
    
    @serialnumber.setter
    def serialnumber(self, value):
        '''
        Sets the serial number value for the SGTIN-96.
        
        Args:
            value (int): The value of the serial number
        
        Description:
            This method can be used to set the value of the encoding's or a property is available.
            An SGTIN-96 serial number can only include digits. Leading Zeros are not allowed in the
            SGTIN-96 serial number, unless the serial number is equal to zero (0).
        
        Example:
            Both calls have the same result and are provided for preference.
            >>> sgtin96 = EPCFactory.create("SGTIN96")
            >>> sgtin96.serialnumber = 123456
            >>> print(sgtin96.serialnumber)
        
        Raises:
            InvalidSerialNumber : will be raised if the serial number is invalid.
        '''
        
        value = self.validate_serial_number(value)
        self.setFieldValue("SerialNumber",value)
    
    def validate_serial_number(self, serial_number):
        """
        Validates the serial number assigned to the SGTIN-96.
        
        Description:
        An SGTIN-96 serial number must be numeric and cannot be left padded with zeros. A fixed-length serial number is
        possible. However, fixing the length of the serial number will limit the serial numbers that can be used. For example,
        The number of bits allowed for an SGTIN-96 serial number is (2^38)-1. Which provides an integer range from 0 to 274,877,906,943.
        
        If, however, the *fixedSerialNumberLength* property is set to a value of 12, the integer range becomes 100,000,000,000 to 274,877,906,943.
        Essentially, the SGTIN-96 will have lost 99,999,999,999 potential serial numbers. 
        
        If the *fixedSerialNumberLength* property is set lower, say to 10, the available serial numbers become even lower as the range will be 
        1,000,000,000 to 9,999,999,999.
        
        Returns:
            int: The serial number passed into the function without leading zeros.
        
        Raises:
            InvalidSerialNumber: If the serial number is in anyway invalid, this exception is raised with a detailed description of the issue.
        
        """
        if self.fixedSerialNumberLength>0:
            if self.fixedSerialNumberLength==12:
                upper_bound = int(math.pow(2,38) - 1)
            else:
                upper_bound = int("9".ljust(self.fixedSerialNumberLength,"9"))
                                  
            lower_bound = int("1".ljust(self.fixedSerialNumberLength,"0"))
            
            if int(serial_number) < lower_bound or int(serial_number) > upper_bound:
                raise InvalidSerialNumber("A fixed-length serial number of {0} digits must be a value between {1} and {2}. The value supplied was {3}", self.fixedSerialNumberLength, lower_bound, upper_bound, serial_number) 
        else:
            if int(serial_number) > int(math.pow(2,38) - 1):
                raise InvalidSerialNumber("The serial number is out of range. The serial number must be less than or equal to {0}. The value supplied was {1}", upper_bound, serial_number)  
    
        return int(serial_number)
     
    def setFieldValue(self, fieldName, val, ItemReference=False):
        """
        Overriden from the base class because if the SerialNumber changes the indicator digit must be preserved
        otherwise its a straight exchange
        """
        if not ItemReference and fieldName == 'ItemReference':
            raise FieldValueException('To change the ItemReference value after construction use the setItemReference and setIndicatorDigit helper functions.  Otherwise, set ItemReference to True.')
        field = self._fieldDictionary[fieldName]
        if val is None:
            s = val
        field.setFieldValue(val) 
        self.updateBitString()
    
    def updateBitString(self):
        self._packStringFormat = 'uint:8, uint:3, uint:3, uint:%s, uint:%s, uint:38' % (self.getField("CompanyPrefix").getBitLength(),self.getField("ItemReference").getBitLength())
        #Pack the bitstring
        bsp=  bitstring.pack(self._packStringFormat, 
                                self.getFieldValue("Header"), 
                                self.getFieldValue("Filter"),
                                self.getFieldValue("Partition"), 
                                self.getFieldValue("CompanyPrefix"), 
                                self.getFieldValue("ItemReference"),
                                int(self.getFieldValue("SerialNumber")))
         
        #Set the _bits for the SGTIN-96
        self._bits = bsp.unpack("bin")[0]
            
    def fromURI(self, uri):
        '''
        Parses the EPC from a epcURI 
        Args:
            uri (str): An EPC Pure Identity URI. e.g. urn:epc:id:sgtin:0358468.202339.395
        Returns:
            EPCNumber: An SGTIN96 instance derived from EPCNumber
        '''
        regEx = re.compile("\d+")
        s = regEx.findall(uri)
        companyPrefix = s[0]
        indicatorDigit = s[1][0:1]
        itemReference = s[1][1:]
        #set the filter value to 0
        filter_value = 0
        serialNumber = s[2]
        self.encode(companyPrefix=companyPrefix, indicatorDigit=indicatorDigit, itemReference=itemReference, filter=filter_value, serialNumber=int(serialNumber))
        return self
    
    def fromTagUri(self,tagUri):
        '''Parses the EPC from a TagURI'''
        regEx = re.compile("\d+")
        s = regEx.findall(tagUri)
        filter_val = s[1]
        companyPrefix = s[2]
        indicatorDigit = s[3][0:1]
        itemReference = s[3][1:]
        serialNumber = s[4]
        self.encode(companyPrefix=companyPrefix, indicatorDigit=indicatorDigit, itemReference=itemReference, filter=filter_val, serialNumber=int(serialNumber))
        return self
            
    def toTagURI(self):
        '''
        Creates an EPC Tag URI Representation of this SGTIN-96.
        
        Returns:
         (str) - An EPC Tag URI
        
        Example:
            >>> sgtin96 = sgtin96.encode(companyPrefix="035846802", 
                                       indicatorDigit=0,
                                       itemReference=339,
                                       filter=3, 
                                       serialNumber=123) 
            >>> tag_uri = sgtin96.toTagURI()
            >>> assert tag_uri == 'urn:epc:tag:sgtin-96:3.035846802.0339.123'
        '''
        
        if(len(self.getFieldValue("CompanyPrefix"))+len(self.getFieldValue("ItemReference")) != 13):
            raise EncodingException("The Length of the CompanyPrefix and the ItemReference must equal 13")
        
        epcUri = "urn:epc:tag:sgtin-96:%s.%s.%s.%s" % (self.getFieldValue("Filter"), self.getFieldValue("CompanyPrefix"), 
                                                       self.getFieldValue("ItemReference"), int(self.getFieldValue("SerialNumber")))
        return epcUri
    
    def toEPCUri(self):
        '''
        Returns the SGTIN-96 in an EPC Pure Identity
        Example: urn:tagpy:id:sgtin:0614141.812345.6789
        '''
        if(len(self.getFieldValue("CompanyPrefix"))+len(self.getFieldValue("ItemReference")) != 13):
            raise EncodingException("The Length of the CompanyPrefix and the ItemReference must equal 13")
        epcUri = "urn:epc:id:sgtin:%s.%s.%s" % (self.getFieldValue("CompanyPrefix"), self.getFieldValue("ItemReference"), int(self.getFieldValue("SerialNumber")))
        return epcUri 
    
    
    def toGS1(self,useParenthesesAroundAIs=True):
        '''Returns the EPC epc translated to a full GS1 with App Identifiers.''' 
        gtin = GTIN(self.getFieldValue("CompanyPrefix"))
        gtin.setUseFixedSerialNumber((self.fixedGS1SerialNumberLength>0))
        gtin.setFixedSerialNumberLength(self.fixedGS1SerialNumberLength)
        gtin.encode(self.getFieldValue("ItemReference")[0:1], self.getFieldValue("ItemReference")[1:], self.getFieldValue("SerialNumber"))
        return gtin.toGS1(useParenthesesAroundAIs) 
    
    def toGTIN14(self):
        '''Returns the EPC epc translated to a GS1 GTIN-14 with NO App Identifiers'''
        gtin = GTIN(self.getFieldValue("CompanyPrefix"))
        gtin.encode(self.getFieldValue("ItemReference")[0:1], self.getFieldValue("ItemReference")[1:], self.getFieldValue("SerialNumber"))
        return gtin.toGTIN14()
    
    def setIndicatorDigit(self, indicatorDigit):
        cur = '{0}{1}'.format(indicatorDigit, self.getFieldValue("ItemReference")[1:])
        self.setFieldValue('ItemReference', cur, True)
        
    def getIndicatorDigit(self):
        ret = ''
        try:
            ret = self.getFieldValue("ItemReference")[0:1]
        except:
            pass
        return ret
    
    def getItemReference(self):
        ret = ''
        try:
            ret = self.getFieldValue("ItemReference")[1:]
        except:
            pass
        return ret
    
    def setItemReference(self, itemReference):
        cur = '{0}{1}'.format(self.getFieldValue("ItemReference")[0:1], itemReference)
        self.setFieldValue('ItemReference', cur, True)
    
    def toXml(self):
        xml = "<Tag type='%s'>\n" % (self._encodingType)
        xml += "\t<Fields>\n"
        xml +=  "\t\t<Field name='Header' value='%s'/>\n" % (self.getFieldValue("Header"))
        xml +=  "\t\t<Field name='Filter' value='%s'/>\n"% (self.getFieldValue("Filter"))
        xml +=  "\t\t<Field name='Partition' value='%s'/>\n" % (self.getFieldValue("Partition"))
        xml +=  "\t\t<Field name='CompanyPrefix' value='%s'/>\n" % (self.getFieldValue("CompanyPrefix"))
        xml +=  "\t\t<Field name='ItemReference' value='%s'/>\n" % (self.getFieldValue("ItemReference"))
        xml +=  "\t\t<Field name='IndicatorDigit' value='%s'/>\n" % (self.getFieldValue("ItemReference")[0:1])
        xml +=  "\t\t<Field name='SerialNumber' value='%s'/>\n" % (int(self.getFieldValue("SerialNumber")))
        xml +=  "\t\t<Field name='RawItemReference' value='%s'/>\n" % (self.getFieldValue("ItemReference")[1:])
        
        xml += "\t</Fields>\n"
        xml += "\t<Hex>%s</Hex>\n" % (self.toHex())
        xml += "\t<Binary>%s</Binary>\n" % (self.toBinary())
        xml += "\t<TagUrn>%s</TagUrn>\n" % (self.toEPCTagUri())
        xml += "\t<PureIdentity>%s</PureIdentity>\n" % (self.toEPCUri())
        xml += "\t<GTIN14>%s</GTIN14>\n" % (self.toGTIN14())
        xml += "\t<GS1>%s</GS1>\n" % (self.toGS1(True))
        xml += "</Tag>"
        return xml;
    
    def toDictionary(self):
            return {"Filter Value": self.getFieldValue("Filter"),
                "Partition" : self.getFieldValue("Partition"),
                "Company Prefix" : self.getFieldValue("CompanyPrefix"),
                "Item Reference" : self.getFieldValue("ItemReference")[1:],
                "Indicator Digit" : self.getFieldValue("ItemReference")[0:1],
                "Serial Number" : int(self.getFieldValue("SerialNumber")),
                "Hex" : self.toHex(),
                "Bin" : self.toBinary(),
                "Tag URN" : self.toTagURI(),
                "EPC URI" : self.toEPCUri(),
                "GTIN14" : self.toGTIN14(),
                "GS1" : self.toGS1(True),
                }
        
    
    def decodeFromBinary(self, binary):
        '''
        Decodes an SGTIN from BINARY string
        
        Args:
          binary (str) - A 96 bit binary string representing an SGTIN-96
        Returns:
          (SGTIN96) - An instance of the SGTIN96 Class. 
        
        Raises:
            EncodingException - If the binary string passed in is not 96 bits, this exception is thrown.
        '''
        self._loadFields()
        
        if(len(binary)!=96):
            raise EncodingException("Binary string is not 96 bits. SGTIN-96 Requires 96 bits to decode properly")
        
        #Filter
        filter_value = binary[8:11]
        self.setFieldValue("Filter",int(filter_value, 2))
        partitionValue = binary[11:14]
        partitionValue = int(partitionValue, 2)
        self.setFieldValue("Partition",partitionValue)
        
        #Partition
        partitions = Partitions()
        companyPrefixBitLength = partitions.getCompanyPrefixBitLength(partitionValue,"SGTIN")
        companyPrefixDigitLength = partitions.getCompanyPrefixDigitLength(partitionValue,"SGTIN")
        self.getField("CompanyPrefix").setOffset(14)
        self.getField("CompanyPrefix").setBitLength(companyPrefixBitLength)
        self.getField("CompanyPrefix").setDigitLength(companyPrefixDigitLength)
        itemReferenceBitLength = partitions.getItemBitLength(partitionValue,"SGTIN")
        itemReferenceDigitLength = partitions.getItemDigitLength(partitionValue,"SGTIN")
        
        self.getField("ItemReference").setOffset(14 + companyPrefixBitLength)
        self.getField("ItemReference").setBitLength(itemReferenceBitLength)
        self.getField("ItemReference").setDigitLength(itemReferenceDigitLength)
        
        companyPrefix = binary[14:14 + self.getField("CompanyPrefix").getBitLength()]
        companyPrefix = str(int(companyPrefix, 2)).zfill(companyPrefixDigitLength)
        self.setFieldValue("CompanyPrefix",companyPrefix)
        itemReference = binary[self.getField("ItemReference").getOffset():self.getField("ItemReference").getOffset() + self.getField("ItemReference").getBitLength()]
        #make sure we are on a 1 byte boundary
        
       
        itemReference = str(int(itemReference,2)).zfill(itemReferenceDigitLength)
        
        self._ignoreUpdate = True
        self.setFieldValue("ItemReference", itemReference, True)
        self._ignoreUpdate = False
        serialNumber = binary[self.getField("SerialNumber").getOffset():self.getField("SerialNumber").getOffset() + self.getField("SerialNumber").getBitLength()]
        
        self.serialnumber=int(serialNumber,2)
        
        return self
                 
    def _loadFields(self):
        """
        Loads Fields for the SGTIN-96 
        """
        
        header = Field(fieldName="Header",offset=0,bitLength=8,ordinal=1,fieldValue=48,digitLength=2)
        self._fieldDictionary["Header"] = header
        filter = Field(fieldName="Filter",offset=8,bitLength=3,ordinal=2,fieldValue=0,digitLength=1) 
        self._fieldDictionary["Filter"] = filter
        partition = Field(fieldName="Partition",offset=11,bitLength=3,ordinal=3,fieldValue=0,digitLength=1) 
        self._fieldDictionary["Partition"] = partition 
        #These next two fields will have their offset,bitLength,digitLength, and value determined at runtime
        companyPrefix = Field(fieldName="CompanyPrefix",offset=14,bitLength=24,ordinal=4,fieldValue=0,digitLength=6,isPadded=True) 
        self._fieldDictionary["CompanyPrefix"] = companyPrefix
        itemReference = Field(fieldName="ItemReference",offset=38,bitLength=24,ordinal=5,fieldValue=0,digitLength=6) 
        self._fieldDictionary["ItemReference"] = itemReference
        serialNumber = Field(fieldName="SerialNumber",offset=58,bitLength=38,ordinal=6,fieldValue=0,digitLength=6) 
        self._fieldDictionary["SerialNumber"] = serialNumber
        
        
        