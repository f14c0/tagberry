import re 
from factories.FactoryBase import FactoryBase
from gs1.Patterns import gtin_patterns, sscc_patterns, gln_patterns, gdti_patterns
from gs1 import GTIN, SSCC, GLN, GDTI

class GS1Factory(FactoryBase):
    def __init__(self):
        pass
    def parse(self, gs1, companyPrefix):
        
        retVal = self.__createGTIN__(companyPrefix, gs1)
        
        if(retVal==None):
            retVal = self.__createSSCC__(companyPrefix, gs1)
        if(retVal==None):
            retVal = self.__createGLN__(companyPrefix, gs1)
        if(retVal==None):
            retVal = self.__createGDTI__(companyPrefix, gs1)
            
                
        return retVal
    
    def toURN(self):
        pass
    
    def __createGTIN__(self, companyPrefix, gs1):
        for pat in gtin_patterns:
            m = re.match(pat,gs1)
            if(m!=None):
                gtin = GTIN(companyPrefix)
                gtin.parse(gs1)
                return gtin
    
    def __createSSCC__(self,companyPrefix, gs1):
        for pat in sscc_patterns:
            m = re.match(pat,gs1)
            if(m!=None):
                sscc = SSCC(companyPrefix)
                sscc.parse(gs1)
                return sscc
    
    def __createGLN__(self,companyPrefix, gs1):
        for pat in gln_patterns:
            m = re.match(pat,gs1)
            if(m!=None):
                gln = GLN(companyPrefix)
                gln.parse(gs1)
                return gln
            
    def __createGDTI__(self,companyPrefix, gs1):
        for pat in gdti_patterns:
            m = re.match(pat, gs1)
            if(m!=None):
                gdti = GDTI(companyPrefix)
                gdti.parse(gs1)
                return gdti
    
    