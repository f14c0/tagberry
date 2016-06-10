import re
from epcerrors.GS1Exception import GS1Exception 
from gs1.GS1Number import GS1Number
from gs1.Patterns import sscc_patterns

class SSCC(GS1Number):
    '''Represents a GS1 SSCC'''
    def __init__(self,companyPrefix):
        super(self, GS1Number).__init__(self,companyPrefix)
        self._serialReference = None
        self._extensionDigit = "0"
        self._sscc18 = ""
        self._encoding_type = "SSCC"
        self.hasAIs = False
        
    def encode(self,extensionDigit,serialReference):
            self._applicationIdentifiersList.append("(00)")
            self._serialReference = serialReference
            self._serial_number = serialReference
            self._extensionDigit = extensionDigit  
            gs1 = "%s%s%s" % (self._extensionDigit,self._company_prefix,self._serialReference)
            self._check_digit = self.calculate_check_digit(gs1)
            gs1 = "(00)%s%s" % (gs1,self._check_digit)
                
            self._gs1 = gs1
            self.parse(self._gs1)
            
        
    def parse(self,sscc):
        '''The parse() method allows you to parse a valid GS1 SSCC-18 and then have access to its individual fields'''
       
        if(self.is_valid(sscc)):
            #store the original sscc
            self._gs1=sscc    
        else:
            raise GS1Exception("The supplied SSCC, '%s' is invalid." % sscc) 
        
        self._parseAIs()
        if(len(self._applicationIdentifiersList)):
            self.hasAIs = True
        
        if(self.hasAIs):
            localSSCC = self._sscc18
        else:
            localSSCC = sscc
            self._sscc18 = sscc
            
        #finish parsing sscc
        self._extensionDigit = localSSCC[:1]
        #remove the last digit an
        if(len(localSSCC)!=18):
            #Calculate Check Digit
            localSSCC+=str(self.calculate_check_digit(localSSCC))
        self._encodingSize = len(localSSCC)
        self._extensionDigit = localSSCC[:1]
        #step over the Extension Digit to parse on the CP and backoff one to ignore the check digit
        serialRef = localSSCC[len(self._company_prefix)+1:len(localSSCC)-1]
        self.setSerialReference(serialRef)
            
    def getSerialReference(self):
        return self._serialReference
    def setSerialReference(self,value):
        self._serial_number = value
        self._serialReference = value
    def getExtensionDigit(self):
        return self._extensionDigit
    def setExtensionDigit(self,value):
        self._extensionDigit
    def getEncodingSize(self):
        return self._encodingSize
    
    def _parseAIs(self):
        if(len(self._gs1)<=18):
        #no A1 in this gs1
            self._applicationIdentifiersList = [] 
            return 
        
        #Pattern to find AIs e.g. (21)
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
                if(self._gs1[match.start():match.end()]=="(00)"):
                    #get the sscc body
                    self._sscc18 = self._gs1[match.end():match.end()+18]
                
                         
        else:
            matchAiWithOutParens = r"(^(00)+)" 
            p = re.compile(matchAiWithOutParens)
            ais = list(p.finditer(self._gs1))
            for match in ais:
                self._applicationIdentifiersList.append(self._gs1[match.start():match.end()])
                #get the gtin14 body
                self._sscc18 = self._gs1[match.end():18]
            
            
                
        
    
    def is_valid(self,sscc):
        '''Determines if the SSCC is valid'''
        for pat in sscc_patterns:
            m = re.match(pat,sscc)
            if(m!=None):
                return True
        #did not match any sscc patterns    
        return False    

    def toSSCC18(self):
        '''Returns the SSCC18-18 Without AIs'''
        return self._sscc18
    
    def toGS1(self,useParenthesesAroundAIs=False):
        '''Returns a full representation of the GS1 GTIN epc, including AIs with or without, parentheses'''
        retVal = ""
        if(len(self._applicationIdentifiersList)>0):
            if(useParenthesesAroundAIs):
                retVal = "(00)%s" % (self._sscc18)
            else:
                retVal = "00%s" % (self._sscc18)
        else:
            retVal = self._sscc18
        
        return retVal
    
    def getEncodingIdentifier(self):
        '''Returns the Company Prefix. This method is here to preserve polymorphic behavior'''
        return self._company_prefix  
    
    def to_base_number(self):
        '''Returns the Core Number e.g. GTIN-14, SSCC-18 without the App Identifiers'''
        return self._sscc18     
    