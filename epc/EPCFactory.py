import math
from bitstring import ConstBitArray
from utils.Utilities import ishex, isbinary
from factories.FactoryBase import FactoryBase
from epcerrors.EncodingException import EncodingException
from epc.SGTIN96 import SGTIN96
from epc.SGTIN198 import SGTIN198
from epc.SSCC96 import SSCC96
from epc.SGLN96 import SGLN96
from epc.SGLN195 import SGLN195
from epc.GRAI96 import GRAI96
from epc.GIAI96 import GIAI96
from epc.GIAI202 import GIAI202
from epc.GSRN96 import GSRN96
from epc.GDTI96 import GDTI96
from epc.GDTI113 import GDTI113
from epc.GID96 import GID96
from epc.DOD96 import DOD96


class EPCFactory(FactoryBase):

    def create(self, epcType):
        '''
        Creates a new EPC Encoding based on the supplied type. The Choices are:
        SGTIN96
        SGTIN198
        SSCC96
        SGLN96
        SGLN195
        GRAI96
        GIAI96
        GIAI202
        GSRN96
        GDTI96
        GDTI113
        GID96
        DOD96
        '''
        if(epcType.upper() == "SGTIN96" or epcType.upper() == "SGTIN-96"):
            epc = SGTIN96(0, 0)
        if(epcType.upper() == "SGTIN198" or epcType.upper() == "SGTIN-198"):
            epc = SGTIN198(0, 0)
        if(epcType.upper() == "SSCC96" or epcType.upper() == "SSSCC-96"):
            epc = SSCC96(0, 0)
        if(epcType.upper() == "SGLN96" or epcType.upper() == "SGLN-96"):
            epc = SGLN96(0, 0)
        if(epcType.upper() == "SGLN195" or epcType.upper() == "SGLN-195"):
            epc = SGLN195(0, 0)
        if(epcType.upper() == "GRAI96" or epcType.upper() == "GRAI-96"):
            epc = GRAI96(0, 0)
        if(epcType.upper() == "GIAI96" or epcType.upper() == "GIAI-96"):
            epc = GIAI96(0, 0)
        if(epcType.upper() == "GIAI202" or epcType.upper() == "GIAI-202"):
            epc = GIAI202(0, 0)
        if(epcType.upper() == "GSRN96" or epcType.upper() == "GSRN-96"):
            epc = GSRN96(0, 0)
        if(epcType.upper() == "GDTI96" or epcType.upper() == "GDTI-96"):
            epc = GDTI96(0, 0)
        if(epcType.upper() == "GDTI113" or epcType.upper() == "GDTI-113"):
            epc = GDTI113(0, 0)
        if(epcType.upper() == "GID96" or epcType.upper() == "GID-96"):
            epc = GID96(0, 0)
        if(epcType.upper() == "DOD96" or epcType.upper() == "DOD-96"):
            epc = DOD96(0, 0)
        return epc

    def parse(self, value):
        '''
        Decodes a given value into an epc number
        '''
        epcNumber = None

        if((len(str(value)) >= 24) and (ishex(value))):
            epcNumber = self._parseHex(value)
        elif((len(str(value)) >= 96) and (isbinary(value))):
            epcNumber = self._parseBinary(value)
        elif(value.startswith("urn:epc:raw:")):
            epcNumber = self._parseRawUri(value)
        elif(value.startswith("urn:epc:id:")):
            epcNumber = self._parseEpcUri(value)
        elif(value.startswith("urn:epc:tag:")):
            epcNumber = self._parseTagUri(value)
        elif(value.startswith("urn:epc:idpat:")):
            #TODO Add idpat parsing to Base Class
            pass
        elif(self._isGS1(value)):
            #TODO Check the GS1 Parsing
            epcNumber = self._parseGS1(value)
        
        if epcNumber is None:
            raise EncodingException('The value %s is an invalid EPC value and could not be parsed.' % value)
        
        return epcNumber
        
    def _parseHex(self,hexValue):
        epc = None
        s = ConstBitArray("0x%s"%hexValue)
        bits = s.bin[2:]
        headerValue = bits[0:8]
        if(int(headerValue,2)==48):
            epc = SGTIN96()
        elif(int(headerValue,2)==49):
            epc = SSCC96()
        elif(int(headerValue,2)==53):
            epc = GID96()    
        elif(int(headerValue,2)==52):
            epc = GIAI96()           
        elif(int(headerValue,2)==51):
            epc = GRAI96()
        elif(int(headerValue,2)==44):
            epc = GDTI96()
        elif(int(headerValue,2)==45):
            epc = GSRN96()
        elif(int(headerValue,2)==50):
            epc = SGLN96()
            
        if not epc:
            raise EncodingException('The value %s is an invalid EPC and could not be parsed.' % hexValue)
        
        epc._decodeFromHex(hexValue)    
        return epc
    
    def _parseBinary(self,binary):
        headerValue = binary[0:8]
        if(int(headerValue,2)==48):
            epc = SGTIN96()
        elif(int(headerValue,2)==49):
            epc = SSCC96() 
        elif(int(headerValue,2)==53):
            epc = GID96()
        elif(int(headerValue,2)==52):
            epc = GIAI96()
        elif(int(headerValue,2)==51):
            epc = GRAI96()
        elif(int(headerValue,2)==44):
            epc = GDTI96()
        elif(int(headerValue,2)==45):
            epc = GSRN96()
        elif(int(headerValue,2)==50):
            epc = SGLN96()
        elif(int(headerValue,2)==58):
            epc = GDTI113()            
        epc._decodeFromBinary(binary)
        return epc 
    
    def _parseRawUri(self,rawUri):
        #urn:epc:raw:96.x30F415E110C598C00000018B
        hex_val = rawUri.split(".x")
        return self._parseHex(hex_val[1]) 
     
    def _parseEpcUri(self,epcUri):
        #urn:epc:id:sgtin:0358468.202339.000395
        epc = None 
        if(epcUri.startswith("urn:epc:id:sgtin")):
            epc = SGTIN96()
        elif(epcUri.startswith("urn:epc:id:sscc")):
            epc = SSCC96()
        elif(epcUri.startswith("urn:epc:id:gid")):
            epc = GID96()
        elif(epcUri.startswith("urn:epc:id:giai")):
            epc = GIAI96()
        elif(epcUri.startswith("urn:epc:id:grai")):
            epc = GRAI96()
        elif(epcUri.startswith("urn:epc:id:gdti")):
            sn = epcUri.split(".")
            if(int(sn)<= math.pow(2,41)):
                epc = GDTI96()
            else:
                epc = GDTI113()
        elif(epcUri.startswith("urn:epc:id:gsrn")):
            epc = GSRN96()
        elif(epcUri.startswith("urn:epc:id:sgln")):
            epc = SGLN96()
            
        epc = epc.fromEPCUri(epcUri)
        return epc
     
    def _parseTagUri(self,tagUri):
        epc = None
        if(tagUri.startswith("urn:epc:tag:sgtin-96:")):
            epc = SGTIN96()
        elif(tagUri.startswith("urn:epc:tag:sscc-96:")):
            epc = SSCC96()
        elif(tagUri.startswith("urn:epc:tag:gid-96:")):
            epc = GID96()
        elif(tagUri.startswith("urn:epc:tag:giai-96:")):
            epc = GIAI96()
        elif(tagUri.startswith("urn:epc:tag:grai-96:")):
            epc = GRAI96()
        elif(tagUri.startswith("urn:epc:tag:gdti-96:")):
            epc = GDTI96()
        elif(tagUri.startswith("urn:epc:tag:gdti-113:")):
            epc = GDTI96()
        elif(tagUri.startswith("urn:epc:tag:gsrn-96:")):
            epc = GSRN96()
        elif(tagUri.startswith("urn:epc:tag:sgln-96:")):
            epc = SGLN96()
            
        epc = epc.fromTagUri(tagUri)     
        return epc
    
    
    