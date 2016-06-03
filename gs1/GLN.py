import re
from epcerrors.GS1Exception import GS1Exception 
from gs1.GS1Number import GS1Number
from gs1.Patterns import gln_patterns

class GLN(GS1Number):
    
    '''Represents a GS1 GLN'''
    def __init__(self,companyPrefix):
        super(self, GS1Number).__init__(self,companyPrefix)
        self._locationReference = None
        self._extension = 0
        self._gln = ""
        self._encodingType = "GLN"
        self._checkDigit = 0
    
    def encode(self,locationReference,extension):
            self._applicationIdentifiersList.append("(254)")
            self._locationReference = locationReference
            self._extension = extension
            self._applicationIdentifiersList.append("(414)")
            
            gs1 = "%s%s" % (self._companyPrefix,self._locationReference)
            checkDigit = self._calculateCheckDigit(gs1)
            if(int(extension)>0):
                gs1 = "(414)%s%s(254)%s" % (gs1,checkDigit,self.getExtensionNumber())
            else:
                gs1 = "(414)%s%s(254)0" % (gs1,checkDigit)
                
            
            self.parse(gs1)
            
        
    def parse(self,gln):
        '''The parse() method allows you to parse a valid GS1 GLN and then have access to its individual fields'''
        hasAIs = False
        if(self.isValid(gln)):
            #store the original gln
            self._gs1=gln    
        else:
            raise GS1Exception("The supplied GLN, '%s' is invalid." % gln) 
        
        self._parseAIs()
        localGLN = self._gln
            
        #remove the last digit an
        if(len(localGLN)<13):
            #Calculate Check Digit
            localGLN+=str(self._calculateCheckDigit(localGLN))
        elif(len(localGLN)==13):
            temp = localGLN[0:len(localGLN)-1]
            self._checkDigit = self._calculateCheckDigit(temp)
            localGLN = "%s%s" % (temp,self._checkDigit)
        self._encodingSize = len(localGLN)
        
        self._locationReference = localGLN[len(self._companyPrefix):len(localGLN)-1]
            
    def getLocationReference(self):
        return self._locationReference
    def setLocationReference(self,value):
        self._locationReference = value
    def getExtensionNumber(self):
        return self._extension
    def setExtensionNumber(self,value):
        self._extension = value
    def getEncodingSize(self):
        return self._encodingSize
    def getCheckDigit(self):
        return self._checkDigit
    def _parseAIs(self):
        if(len(self._gs1)<=13):
        #no A1 in this gs1
            self._applicationIdentifiersList = [] 
            return 
        
        #Pattern to find AIs e.g. (414)
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
                if(self._gs1[match.start():match.end()]=="(414)"):
                    #get the gln body
                    self._gln = self._gs1[match.end():match.end()+13]
                if(self._gs1[match.start():match.end()]=="(254)"):
                    self._extension = self._gs1[match.end():]
                         
        else:
            matchAiWithOutParens = r"(^(414)+)" 
            p = re.compile(matchAiWithOutParens)
            ais = list(p.finditer(self._gs1))
            for match in ais:
                self._applicationIdentifiersList.append(self._gs1[match.start():match.end()])
                #get the gln body
                self._gln = self._gs1[match.end:13]
            #for a gln who has no parens, look for AI 414
            matchAiWithOutParens = r"((254[0-9]{1,21})$)" 
            p = re.compile(matchAiWithOutParens)
            ais = list(p.finditer(self._gs1))
            for match in ais:
                self._applicationIdentifiersList.append(self._gs1[match.start():match.start()+2])
                #get the extension number
                self._extension = self._gs1[match.start()+2:match.end()]
                
        
    
    def isValid(self,gln):
        '''Determines if the GTIN is valid'''
        for pat in gln_patterns:
            m = re.match(pat,gln)
            if(m!=None):
                return True
        #did not match any gln patterns    
        return False    

    def toGLN(self):
        '''Returns the gln Without AIs or Serial Number'''
        return self._gln
    
    def toGS1(self,useParenthesesAroundAIs=False,serialNumberLength=0):
        '''Returns a full representation of the GS1 GTIN epc, including AIs with or without, parentheses'''
        retVal = ""
        if(len(self._applicationIdentifiersList)>0):
            if(useParenthesesAroundAIs):
                retVal = "(414)%s(254)%s" % (self._gln,self._extension)
            else:
                retVal = "414%s254%s" % (self._gln,self._extension)
        else:
            #No AIs Found at parse or encode but...
            if(self._serialNumber!=None):
                #if there is a serial number add it to the GTIN with the proper AI
                if(useParenthesesAroundAIs):
                    #Use Parens
                    retVal = "(414)%s(254)%s" % (self._gln,self._extension)
                else:
                    #Do not use parens
                    retVal = "414%s254%s" % (self._gln,self._extension)
            else:
                #No AIs found in parse or encode and there is no serial number
                retVal = self._gln
        
        return retVal