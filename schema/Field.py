from bitstring import BitArray
from utils.Conversion import Conversion
from epcerrors.FieldValueException import FieldValueException  

class Field(object):
    """
    Field Class represents a single field within an EPC Encoding
    """
    def __init__(self,fieldName=None, offset=None, bitLength=None, ordinal=None, fieldValue=None, digitLength=None, isPadded=False):
        self.setFieldName(fieldName)
        self.setOffset(offset)
        self.setBitLength(bitLength)
        self.setOrdinal(ordinal)
        self.setFieldValue(fieldValue)
        self.setDigitLength(digitLength)
        self.isPadded = isPadded 
        
        

    def getFieldName(self):
        """Returns the Name of the Field"""
        return self._fieldName
    
    def setFieldName(self,value):
        """Sets the Name of the Field"""
        self._fieldName=value
        
    
    
    def getFieldValue(self):
        """Gets the Value of the Field"""
        if(self.isPadded==True):
            return str(self._fieldValue).zfill(self.getDigitLength())
        else:
            return str(self._fieldValue)
    
    def setFieldValue(self,value):
        """Sets the Value of the Field"""
        #self.validateSize(value)
        self._fieldValue=str(value)
       
        #refresh fieldBits value
        self.getBits()
       

    def getOffset(self):
        return self._offset
    def setOffset(self,value):
        self._offset=value
    

    def getBits(self):
        if(self._fieldValue!=None and self._bitLength!=None and self._bitLength>0):
            ui = BitArray(uint = Conversion().uint32(self._fieldValue),length=self._bitLength)
            return ui.bin[2:]
        else:
            return "0".zfill(self._bitLength)
        
    
    
    def getBitLength(self):
        """Gets the Bit Length of the Field"""
        return self._bitLength
    def setBitLength(self, value):
        """Sets the Bit Length of the Field"""
        self._bitLength=value
    

    def getDigitLength(self):
        return self._digitLength
    def setDigitLength(self,value):
        self._digitLength=value
    

    def getOrdinal(self):
        return self._ordinal
    def setOrdinal(self,value):
        self._ordinal=value
    
    ordinal = property(getOrdinal, setOrdinal)
    digit_length = property(getDigitLength, setDigitLength)
    bit_length = property(getBitLength, setBitLength)
    bits = property(getBits)
    name = property(getFieldName, setFieldName)
    value = property(getFieldValue, setFieldValue)
    offset = property(getOffset, setOffset)
    
    def validateSize(self, value):
        if(value>pow(2,self._bitLength)):
            raise FieldValueException("%s value is too large" % self._fieldName)


    def toXml(self):
        #hex='%s' binary='%s' length='%d' ordinal='%d' offset='%d' self.hex
        return "<Field name='%s' value='%s'/>" % (self._fieldName,str(self._fieldValue), )
    
    
    def __lt__(self, object):
        return (int(self._ordinal) < int(object._ordinal))
    
    def __getitem__(self, idx):
        return self._ordinal
        
       
    def __repr__(self):
        return "{0}:{1}:{2}:{3}:{4}:{5}".format(self._ordinal,self._fieldName,self._fieldValue,self._bitLength,self._offset,self._digitLength)
    
    def __str__(self):
        return self.name     




        
    

    