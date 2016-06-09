import re
from epcerrors.GS1Exception import GS1Exception 
from gs1.GS1Number import GS1Number
from gs1.Patterns import gdti_patterns

class GDTI(GS1Number):
    
    '''Represents a GS1 GTIN'''
    def __init__(self,companyPrefix):
        super(self, GS1Number).__init__(self,companyPrefix)
        self._documentType = None
        self._gdti = ""
        self._serial_number=""
        self._encoding_type = "GDTI" 
    
    def encode(self,documentType,serialNumber):
            self._documentType = documentType
            self._serial_number = serialNumber
            
            gs1 = "%s%s" % (self._company_prefix,self._documentType)
            self._check_digit = self.calculate_check_digit(gs1)
            self._gdti = "%s%s" % (gs1,self._check_digit)
            self._serial_number = serialNumber
            if(int(serialNumber)>0):
                gs1 = "(253)%s%s" % (self._gdti,serialNumber)
                self._gdti = "%s%s" % (self._gdti,serialNumber)
            else:
                gs1 = "(253)%s" % (self._gdti)
            
            self.parse(gs1)
            
        
    def parse(self,gdti):
        '''The parse() method allows you to parse a valid GS1 DTI and then have access to its individual fields'''
        hasAIs = False
        if(self.is_valid(gdti)):
            #store the original gdti
            self._gs1=gdti    
        else:
            raise GS1Exception("The supplied GDTI, '%s' is invalid." % gdti) 
        
        self._parseAIs()
        if(len(self._applicationIdentifiersList)):
            hasAIs = True    
        #finish parsing gdti
        cpl = len(self._company_prefix)
        dtl = 12-cpl
        self._documentType = self._gdti[cpl:cpl+dtl]
        self._check_digit = self._gdti[cpl+dtl:cpl+dtl+1]
        self._serial_number = self._gdti[cpl+dtl+1:]
        
            
    def getDocumentType(self):
        return self._documentType
    def setDocumentType(self,value):
        self._documentType = value
    
    def _parseAIs(self):
        if(len(self._gs1)<=17):
        #no A1 in this gs1
            self._applicationIdentifiersList = [] 
            return 
        
        #Pattern to find AIs e.g. (253)
        matchAiWithParens = r"(\(+\d*\)+)" 
        p = re.compile(matchAiWithParens)
        #Get all AIs
        ais = list(p.finditer(self._gs1))
        #Clear old _applicationIdentifires
        self._applicationIdentifiersList = []
        if(len(ais)):
            #build new AI List
            for match in ais:
                self._applicationIdentifiersList.append(self._gs1[match.start():match.end()])         
        else:
            matchAiWithOutParens = r"(^(253)+)" 
            p = re.compile(matchAiWithOutParens)
            ais = list(p.finditer(self._gs1))
            for match in ais:
                self._applicationIdentifiersList.append(self._gs1[match.start():match.end()])
                
                
        
    
    def is_valid(self,gdti):
        '''Determines if the GTIN is valid'''
        for pat in gdti_patterns:
            m = re.match(pat,gdti)
            if(m!=None):
                return True
        #did not match any gdti patterns    
        return False    

    def toGDTI(self,withSerialNumber=False):
        '''
        Returns the GDTI Without AIs and a choice to return with the Serial Number
        The serial number on a GS1 GDTI is optional. However, you cannot translate the GS1 GDTI to an EPC representation without
        the serial number. The parameter 'withSerialNumber', when set to True will return the GDTI with the serial Number.
        The default value for the parameter is False and will not return the serial number with the GDTI
        '''
        if(withSerialNumber==False):
            return self._gdti
        else:
            if(self._serial_number != None):
                return "%s%s" % (self._gdti,str(self._serial_number))
    
    def toGS1(self,useParenthesesAroundAIs=False,serialNumberLength=0):
        '''Returns a full representation of the GS1 GTIN epc, including AIs with or without, parentheses'''
        retVal = ""
        
        #if there is a serial number add it to the GTIN with the proper AI
        if(useParenthesesAroundAIs):
            #Use Parens
            retVal = "(253)%s" % (self._gdti)
        else:
            #Do not use parens
            retVal = "253%s" % (self._gdti)
            
        
        return retVal
            
    