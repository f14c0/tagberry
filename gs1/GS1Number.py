from math import ceil
  
class GS1Number(object):  
  
    def __init__(self, companyPrefix):
        self._checkDigit = None 
        self._applicationIdentifiersList = []
        self._IdentificationKey=None
        self._serialNumber=0
        self._encodingType=None
        self._companyPrefix=companyPrefix
        self._gs1 = None
        
        
    def parse(self,gs1):
        '''
        Meant to be overridden in subclass
        '''    
        pass
    
    def getSerialNumber(self):
        '''
        Gets the SerialNumber
        '''
        return self._serialNumber
    def setSerialNumber(self,value,serialNumberLength=0):
        '''
        Sets the SerialNumber 
        if the serialNumberLength is greater than zero, the serialNumber will be padded to the left with zeros
        '''
        if(serialNumberLength>0):
            self._serialNumber=value.zfill(serialNumberLength)
        else:
            self._serialNumber=value
    
    def getEncodingType(self):
        return self._encodingType
    
    def getCompanyPrefix(self):
        return self._companyPrefix
    def setCompanyPrefix(self,value):
        self._companyPrefix=value
    def getCheckDigit(self):
        return self._checkDigit
    
    
    def isValid(self,gs1):
        '''Determines if this is a valid GS-1 Encoding'''
    
    def toGS1(self,useParenthesesAroundAIs=False):
        '''Returns a full representation of the GS1 epc, including AIs with or without, parentheses'''
        pass 
    def getAppIdentifiers(self):
        '''
        If the GS1 was passed in with parens delimiting AIs then this
        method will find all app identifiers with in the GS1 Number 
        and place them in the _applicationIdentifiersList
        '''
        pass
    
    def toCoreNumber(self):
        '''Returns the Core Number e.g. GTIN-14, SSCC-18 without the App Identifiers'''
        pass
    
    def getEncodingIdentifier(self):
        '''Returns the portion of the epc that identifies the epc most. e.g. Company Prefix,  LocationReference, DocumentType etc'''
        pass
        
        
    def _calculateCheckDigit(self,gs1):
        total = 0
        m = 1
        for c in gs1:
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
    