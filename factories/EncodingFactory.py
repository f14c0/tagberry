import re
from epc.EPCFactory import EPCFactory
from epcerrors.GS1Exception import GS1Exception
from gs1.GS1Factory import GS1Factory
from gs1.Patterns import sscc_patterns
from utils.Utilities import isGS1


class EncodingFactory:
    def __init__(self):
        self.sscc_patterns = []
        for pat in sscc_patterns:
            self.sscc_patterns.append(re.compile(pat))

    def create(self, data):

        if(isGS1(data)):
            return GS1Factory()
        else:
            return EPCFactory()

    def parse(self, data, companyPrefix=None):
        retVal = None

        if(isGS1(data)):
            if(companyPrefix == None):
                raise GS1Exception("In order to create a GS1 Encoding a company prefix is required")
            retVal = GS1Factory().parse(data, companyPrefix)
        else:
            retVal = EPCFactory().parse(data)

        return retVal
    
    def isSSCC(self, gs1):
        ret = False
        for pat in self.sscc_patterns:
            m = pat.match(gs1)
            if(m!=None):
                ret = True
                break
        return ret