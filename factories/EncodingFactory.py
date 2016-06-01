import re
from encoding.EPCFactory import EPCFactory
from epcerrors.GS1Exception import GS1Exception
from gs1.GS1Factory import GS1Factory
from gs1.Patterns import gtin_patterns, sscc_patterns, gln_patterns


class EncodingFactory:
    def __init__(self):
        self.sscc_patterns = []
        for pat in sscc_patterns:
            self.sscc_patterns.append(re.compile(pat))

    def create(self, data):

        if(self._isGS1(data)):
            return GS1Factory()
        else:
            return EPCFactory()

    def parse(self, data, companyPrefix=None):
        retVal = None

        if(self._isGS1(data)):
            if(companyPrefix == None):
                raise GS1Exception("In order to create a GS1 Encoding a company prefix is required")
            retVal = GS1Factory().parse(data, companyPrefix)
        else:
            retVal = EPCFactory().parse(data)

        return retVal

    def _isGS1(self,gs1):
        #gotta make this method better
        
        for pat in gtin_patterns:
            m = re.match(pat,gs1)
            if(m!=None):
                return True
        
        for pat in sscc_patterns:
            m = re.match(pat,gs1)
            if(m!=None):
                return True
        
        for pat in gln_patterns:
            m = re.match(pat,gs1)
            if(m!=None):
                return True
            
        return False  
    
    def isSSCC(self, gs1):
        ret = False
        for pat in self.sscc_patterns:
            m = pat.match(gs1)
            if(m!=None):
                ret = True
                break
        return ret