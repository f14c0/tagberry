import re
from epcerrors.GS1Exception import GS1Exception 
from gs1.GS1Number import GS1Number
from gs1.Patterns import grai_patterns

class GRAI(GS1Number):
    
    '''Represents a GS1 GRAI'''
    def __init__(self,companyPrefix):
        super(self, GS1Number).__init__(self,companyPrefix)
        self._assetType = None
        self._grai = ""
        self._encoding_type = "GRAI"
    
    def encode(self,assetType,serialNumber):
            self._applicationIdentifiersList.append("(8003)")
            self._assetType = assetType
            self._serial_number = serialNumber
                
            
            gs1 = "0%s%s" % (self._company_prefix,self._assetType)
            checkDigit = self.calculate_check_digit(gs1)
            
            gs1 = "(8003)%s%s%s" % (gs1,checkDigit,self._serial_number)
                
            self._gs1 = gs1
            self.parse(self._gs1)
            
        
    def parse(self,grai):
        '''The parse() method allows you to parse a valid GS1 GRAI and then have access to its individual fields'''
        hasAIs = False
        if(self.is_valid(grai)):
            #store the original grai
            self._gs1=grai    
        else:
            raise GS1Exception("The supplied GRAI, '%s' is invalid." % grai) 
        
        self._parseAIs()
        if(len(self._applicationIdentifiersList)):
            hasAIs = True
        
        if(hasAIs):
            if(grai.startswith("(")):
                localGRAI = grai[6:]
            elif(grai.startswith("8003")):
                localGRAI = grai[4:]
        else:
            localGRAI = grai
            
       
        #finish parsing grai
        
        
        
        
        self._encodingSize = len(localGRAI)
        atl = 13 - len(self._company_prefix)
        self._assetType = localGRAI[len(self._company_prefix):len(self._company_prefix)+atl]
        self._serial_number = localGRAI[len(self._company_prefix)+len(self._assetType)+1:]
        temp = "%s%s" % (self._company_prefix,self._assetType)
        self._check_digit=str(self.calculate_check_digit(temp))
        self._grai = "0%s%s%s%s" % (self._company_prefix,self._assetType,self._check_digit,self._serial_number)
        
            
    def getAssetType(self):
        return self._assetType
    def setAssetType(self,value):
        self._assetType = value
    def getEncodingSize(self):
        return self._encodingSize
    
    def _parseAIs(self):
        if(len(self._gs1)<=14):
        #no A1 in this gs1 
            return 
        
        #Pattern to find AIs e.g. (8003)
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
            matchAiWithOutParens = r"(^(8003)+)" 
            p = re.compile(matchAiWithOutParens)
            ais = list(p.finditer(self._gs1))
            for match in ais:
                self._applicationIdentifiersList.append(self._gs1[match.start():match.end()])
                
            
                        
        
    
    def is_valid(self,grai):
        '''Determines if the GRAI is valid'''
        for pat in grai_patterns:
            m = re.match(pat,grai)
            if(m!=None):
                return True
        #did not match any grai patterns    
        return False    

    def toGRAI(self):
        '''Returns the GRAI Without AIs or Serial Number'''
        return self._grai
    
    def toGS1(self,useParenthesesAroundAIs=False):
        '''Returns a full representation of the GS1 GRAI epc, including AIs with or without, parentheses'''
        retVal = ""
        #if there is a serial number add it to the GTIN with the proper AI
        if(useParenthesesAroundAIs):
            #Use Parens
            retVal = "(8003)%s" % (self._grai)
        else:
            #Do not use parens
            retVal = "8003%s" % (self._grai)
           
                        
        return retVal
            
    
    
    