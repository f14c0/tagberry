from math import ceil
from utils.abstract_wrapper import abstract
  
class GS1Number(object):  
  
    def __init__(self, company_prefix=None):
        self._check_digit = None 
        self._applicationIdentifiersList = []
        self._IdentificationKey=None
        self._serial_number=0
        self._encoding_type=None
        self._company_prefix=company_prefix
        self._gs1 = None
    
    class MetaClass:
        abstract = True     
    
    @abstract     
    def parse(self, gs1):
        '''
        Meant to be overridden in subclass
        '''    
    @property 
    def serial_number(self):
        '''
        Gets the SerialNumber
        '''
        return self._serial_number
    
    @serial_number.setter 
    def serial_number(self, value, serial_number_length=0):
        '''
        Sets the SerialNumber 
        if the serialNumberLength is greater than zero, the serialNumber will be padded to the left with zeros
        '''
        if(serial_number_length>0):
            self._serial_number=value.zfill(serial_number_length)
        else:
            self._serial_number=value
    
    @property
    def encoding_type(self):
        return self._encoding_type
    
    @property 
    def company_prefix(self):
        return self._company_prefix
    @company_prefix.setter 
    def company_prefix(self,value):
        self._company_prefix=value
    
    @property 
    def check_digit(self):
        '''
        Returns the calculated check digit
        '''
        return self._check_digit
    
    @abstract
    def is_valid(self, gs1):
        '''Determines if this is a valid GS-1 Encoding'''
    
    @abstract
    def to_epc(self):
        '''
        Returns an EPC Encoding of the same GS1 Encoding.
        '''
    
    @abstract
    def get_app_identifiers(self):
        '''
        If the GS1 was passed in with parens delimiting AIs then this
        method will find all app identifiers with in the GS1 Number. 
        '''
        
    @abstract
    def to_base_number(self):
        '''Returns the *base* number e.g. GTIN-14, SSCC-18 without the App Identifiers'''
        
    def calculate_check_digit(self, gs1):
        '''
        Calculates the check digit for a GS1 Encoding
        
        Args:
            gs1 (str) - a GS1 Number without a check digit.
        
        Returns:
            (int): The correct check digit.
        
        '''
        total = 0
        m = 1
        for c in str(gs1):
            if m == 1:
                m = 3
            else:
                m = 1
            total = total + (int(c) * m)
        #get the nearest value of 10
        tenVal = ceil(float(total) * .1) * 10
        return int(tenVal - total)
    
    
    def __str__(self):
        return self._gs1     
    