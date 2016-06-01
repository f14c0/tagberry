from schema.FieldDictionary import FieldDictionary
from bitstring import BitArray
from utils.JSONEncoder import JSONEncoder
from bitstring import ConstBitArray
from epcerrors import FieldValueException
from utils.abstract_wrapper import abstract


class EPCNumber(object):
    """
    Base Class for all EPC Encodings
    """
    def __init__(self, startSerialNumber=0, numOfSerialNumbers=0, fixedSerialNumberLength=0):
        """Initializes the data for the EPCNumber Class"""
        self._fieldDictionary = FieldDictionary()
        self._bits = None
        self._packStringFormat = ''
        self._encodingType=''
        self._startSerialNumber = startSerialNumber
        self._numOfSerialNumbers = numOfSerialNumbers
        self._fixedSerialNumberLength = fixedSerialNumberLength
        self._serailNumber
    
    class Meta:
        """
        Meta class that makes EPCNumber Abstract
        """
        abstract = True
        
    @abstract    
    def loadFields(self):
        """
        Loads Fields for the Derived EPC Number. This method must be overridden in the derived class
        and should not be called from the base class as it will throw an exception. 
        """
        
    
    @abstract
    def encode(self, *args, **kwargs):
        """
        Encodes an EPC number with the given fields.  
        This method must be overridden in a derived class and should not be called from 
        the base class as it will throw an exception.
        """
        
    def setFieldValue(self, fieldName, val):
        """
        Sets the Value of the supplied fieldName with the supplied val
        example: sgtin.setFieldValue("SerialNumber",1)
        """
        if fieldName.lower() == "serialnumber":
            field = self.validate_serial_number(val)
            field.value = val
        else:
            field = self._fieldDictionary[fieldName] 
            field.value = val
        self._updateBitString()
        
    def getFieldValue(self,fieldName):
        """
        Gets the Value of the supplied fieldName
        example: serialNumber = sgtin.getFieldValue("SerialNumber")
        """  
        field = self._fieldDictionary[fieldName]
        return field.getFieldValue()
    
    def getField(self,fieldName):
        """
        Gets the Value of the supplied fieldName
        example: serialNumber = sgtin.getField("SerialNumber")
        """  
        return self._fieldDictionary[fieldName]
    
    
    def getEncodingType(self):
        '''Returns the Type of EPC Encoding represented by the derivative. eg. SGTIN96, SSCC96 etc'''
        return self._encodingType
    
    
    def getFieldDictionary(self):
        """Returns the Name of the Field"""
        if self._fieldDictionary is None:
            self._fieldDictionary = FieldDictionary()
        
        return self._fieldDictionary
    
    fieldDictionary = property(getFieldDictionary) 
    
    @property 
    def fixedSerialNumberLength(self):
        """
        Gets the Fixed Serial Number Length.
        
        Description:
            The Fixed Serial Number Length is only required when a fixed serial number length is required.
            If the value of Fixed Serial Number is zero (0), then tagberry will assume that no fixed serial
            number is required.
            
            However, if this number is set to a value greater than zero (0) tagberry will apply the
            rules in the Tag Data Specification 1.9 to the serial number. 
            
        Returns:
            int : the fixed serial number length
         
        """
        return self._fixedSerialNumberLength
    
    @fixedSerialNumberLength.setter 
    def fixedSerialNumberLength(self, value):
        """
        Gets the Fixed Serial Number Length.
        
        Args:
            value (int): The fixed-length of the serial number. 
        
        Description:
            The Fixed Serial Number Length is only required when a fixed serial number length is required.
            If the value of Fixed Serial Number is zero (0), then tagberry will assume that no fixed serial
            number is required.
            
            However, if this number is set to a value greater than zero (0) tagberry will apply the
            rules in the Tag Data Specification 1.9 to the serial number. 
        
        Returns:
            int : the fixed serial number length
        
        """
        self._fixedSerialNumberLength = value 
    
     
    
    
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
        Abstract. Sets the serial number value.
        
        Args:
            value (int): The value of the serial number
        
        Description:
            This method can be used to set the value of the encoding's or a property is available.
        
        Example:
            Both calls have the same result and are provided for preference.
            >>> sgtin = EPCFactory.create("SGTIN96")
            >>> sgtin.serialnumber = 123456
            >>> sgtin.setSerialNumber(123456)
        
        Raises:
            NotImplemented : will be raise if this setter is not overridden in the derived class when it is called.
        '''
        
    @abstract
    def toTagURI(self):
        '''Override in derived class'''
        
    
    @abstract
    def toURI(self):
        '''Override in derived class'''
    
    def toRawURI(self):
        '''Returns the <ENCODING> in an EPC Raw URI Representation'''
        epcUri = "urn:tagpy:raw:96.x%s" % (self.toHex())
        return epcUri
    
    @abstract
    def fromURI(self, uri):
        '''Override in derived class. Parses the EPC from a TagURI'''
    @abstract
    def fromTagURI(self, uri):
        '''Parses the EPC from a TagURI'''
        
    def fromRawURI(self, uri):
        '''Parses the EPC from a EPC Raw URI'''
        hex_val = uri.split(".x")
        return self._parseHex(hex_val[1])
    
    def fromHex(self, hex_val):
        '''Parses the EPC from a Hex Value''' 
        return self._decodeFromHex(hex_val)
    
    def toHex(self):
        '''Returns a hex representation of the EPCNumber'''   
        h = BitArray("0b%s" % self._bits)
        return h.hex[2:].upper()
    
    @abstract
    def toGS1(self):
        '''Override in derived class'''
    
    def toBinary(self):
        '''Returns a binary representation of the EPCNumber'''
        return self._bits
    
    @abstract
    def toXml(self):
        """Meant to be overriden in the derived class"""
    
    def toJSON(self):
        return JSONEncoder().encode(self.toDictionary())
    
    def toIDPAT(self, *args):
        '''
        Returns an urn:epc:idpat
        '''
        return "urn:epc:idpat:{0}:{1}.{2}.{3}".format(self._encodingType,self.getField("companyPrefix"),args)
    
    @abstract
    def toDictionary(self):
        """Meant to be overriden in the derived class"""
    
    def format(self, format="HEX"):
        """
        Returns a string representation of the EPC Number in the provided format
        """
        if(format.lower()=="hex"):
            return self.toHex()
        elif(format.lower()=="xml"):
            return self.toXml()
        elif(format.lower()=="json"):
            return self.toJSON()
        elif(format.lower()=="dict"):
            return self.toDictionary()
        elif(format.lower()=="dictionary"):
            return self.toDictionary()
        elif(format.lower()=="binary"):
            return self.toBinary()
        elif(format.lower()=="bin"):
            return self.toBinary()
        elif(format.lower()=="raw"):
            return self.toEPCRawUri()
        elif(format.lower()=="epcraw"):
            return self.toEPCRawUri()
        elif(format.lower()=="epcrawuri"):
            return self.toEPCRawUri()
        elif(format.lower()=="tag"):
            return self.toEPCTagUri()
        elif(format.lower()=="epctag"):
            return self.toEPCTagUri()
        elif(format.lower()=="epctaguri"):
            return self.toEPCTagUri()
        elif(format.lower()=="gs1"):
            return self.toGS1()
    
    def increment(self, count=1):
        cur = int(self.getFieldValue('SerialNumber')) + count
        self.setFieldValue('SerialNumber', cur)
        return cur
        
    def decrement(self, count=1):
        cur = int(self.getFieldValue('SerialNumber')) - count
        if cur < 0:
            raise FieldValueException("Serial number field may not be below 0.")
        self.setFieldValue('SerialNumber', cur)
        return cur
        
    @abstract    
    def encodeFromURI(self,tagURI, format='JSON'):
        """Meant to be overridden in the derived class"""    
    
    @abstract
    def encodeFromGS1(self, gs1):
        """Meant to be overridden in the derived class"""
        
    @abstract    
    def decodeFromURI(self, tagUri, format='JSON'):
        """Meant to be overridden in the derived class"""
    
    @abstract
    def decodeFromGS1(self,gs1):
        """Meant to be overridden in the derived class"""
    
    @abstract
    def decodeFromBinary(self,binary):
        """Meant to be overridden in the derived class"""
    
    
    def decodeFromHex(self, hex_val):
        '''
        Encodes an EPCNumber from BINARY string
        '''
        s = ConstBitArray("0x%s"%hex)
        return self._decodeFromBinary(s.bin[2:])
    
    @abstract        
    def updateBitString(self):
        '''Override in derived class'''
    
    def validate_serial_number(self, serial_number):
        """
        Validates a serial number to ensure it fits in the confines of the encoding.
        
        Args:
        serial_number int: Serial Number that will be assigned to the encoding
        
        Raises:
            InvalidSerialNumber: if serial_number is invalid this exception is raised
        Returns:
            serial_number int: 
        """
            
        
