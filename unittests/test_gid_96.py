import unittest
from encoding.EPCFactory import EPCFactory
from encoding.GID96 import GID96
from utils.Partitions import Partitions  
from bitstring import BitArray
class GID96Test(unittest.TestCase):
    def setUp(self):
        self._gid96 = GID96()
        self._generalManager = "10240"
        self._objectClass = "19254"
        self._serialNumber = 0
        
    def test_Encode(self):
        print ("==== Test Encode from Hex Value ====")
        gid96 = self._gid96.encode(self._generalManager, None,self._objectClass ,None, self._serialNumber)
        bits = (gid96.toBinary())
        self.assertEquals(len(bits),96)
        self._checkFields(gid96)
        print (gid96.toBinary())
        print (gid96.toHex())
        print ("====END Test Decoding from Hex Value ====")
        print ("")    
    
    def test_ParseHex(self):
        print ("==== Test Decoding from Hex Value ====")
        #Turn the tagpy number into a hex value and parse it through the factory
        gid96 = self._gid96.encode(self._generalManager, None,self._objectClass ,None, self._serialNumber)
        hex = gid96.toHex()
        factory = EPCFactory()
        gid96 = factory.parse(hex)
        self._checkFields(gid96)
        print (gid96.toHex())
        print (gid96.toBinary())
        print ("====END Test Decoding from Hex Value ====")
        print ("")
    
    def test_FromHex(self):
        print ("==== Test Decoding from Hex Value ====")
        #Turn the tagpy number into a hex value and parse it through the factory
        epc = self._gid96.encode(self._generalManager, None,self._objectClass ,None, self._serialNumber)
        hex = epc.toHex()
        epc = epc.fromHex(hex)
        self._checkFields(epc)
        print (epc.toHex())
        print (epc.toBinary())
        print ("====END Test Decoding from Hex Value ====")
        print ("")
    
    def test_ParseBinary(self):
        print ("***==== Test Decoding from Binary Value ====***")
        gid96 = self._gid96.encode(self._generalManager, None,self._objectClass ,None, self._serialNumber)
        bin = gid96.toBinary()
        self.assertEquals(len(bin),96)
        factory = EPCFactory()
        #Take the binary value and parse it through the factory
        gid96 = factory.parse(bin)
        self._checkFields(gid96)
        print (gid96.toHex())
        print (gid96.toBinary())
        print ("====END Test Decoding from Binary Value ====")
        print ("")
    
    def test_ParseRawUri(self):
        print ("***==== Test Decode Raw Uri Value ====***")
        gid96 = self._gid96.encode(self._generalManager, None,self._objectClass ,None, self._serialNumber)
        rawUri = gid96.toEPCRawUri()
        factory = EPCFactory()
        #Take the Raw URI value and parse it through the factory
        gid96 = factory.parse(rawUri)
        self._checkFields(gid96)
        print(rawUri)
        print(gid96.toHex())
        print(gid96.toBinary())
        print ("***==== END Test Decode Raw Uri Value ====***")
        print ("")
    
    def test_ParseEPCUri(self):
        print ("***==== Test Decode EPC Uri Value ====***")
        #TagURI=urn:tag:id:gid:358468.2339.395
        gid96 = self._gid96.encode(self._generalManager, None,self._objectClass ,None, self._serialNumber)
        factory = EPCFactory()
        #Take the Raw URI value and parse it through the factory
        tagUri = gid96.toEPCUri()
        gid96 = factory.parse(tagUri)
        self._checkFields(gid96)
        print (tagUri)
        print (gid96.toHex())
        print (gid96.toBinary())
        print ("***==== END Test EPC URI Value ====***")
        print ("")
    
    def test_ParseEPCTagUri(self):
        print ("***==== Test Decode EPC Tag Uri Value ====***")
        tagUri = "urn:tagpy:tag:gid-96:%s.%s.%s" % (self._generalManager,self._objectClass,self._serialNumber)
        factory = EPCFactory()
        #Take the Tag URI value and parse it through the factory
        gid96 = factory.parse(tagUri)
        self._checkFields(gid96)
        print (tagUri)
        print (gid96.toHex())
        print (gid96.toBinary())
        print ("***==== END Test Decode EPC Tag Uri Value ====***")
        print ("")
    
    def test_ToEPCTagUri(self):
        print ("***==== Test To EPC Tag Uri Value ====***")
        gid96 = self._gid96.encode(self._generalManager, None,self._objectClass ,None, self._serialNumber)
        print (gid96.toEPCTagUri())
        print ("***==== END  Test To EPC Tag Uri Value ====***")
        print ("")
    
    def test_ToRawUri(self):
        print ("***==== Test To Raw Uri Value ====***")
        gid96 = self._gid96.encode(self._generalManager, None,self._objectClass ,None, self._serialNumber)
        print (gid96.toEPCRawUri())
        print ("***==== END  Test To EPC Tag Uri Value ====***") 
        print ("")
    
    def test_Formats(self):
        print ("***==== Test Formatting ====***")
        epc = self._gid96.encode(self._generalManager, None,self._objectClass ,None, self._serialNumber)
        #Turn the tagpy number into a hex value and parse it through the factory
        hex = epc.toHex()
        factory = EPCFactory()
        gid96 = factory.parse(hex)
        
        print ("=== Format to HEX ===")
        print (gid96.format("hex"))
        print ("===========================")
        print ("=== Format to BINARY ===")
        print (gid96.format("binarY"))
        print ("===========================")
        print ("=== Format to JSON ===")
        print (gid96.format("json"))
        print ("===========================")
        print ("=== Format to RAW_URI ===")
        print (gid96.format("raw_uRI"))
        print ("===========================")
        print ("=== Format to DICTIONARY ===")
        f = gid96.format("DICTIONARY")
        for k, v in f.items():       
            print ("%s=%s\n" % (k, v))
        print ("===========================")
        
    def test_ChangeSerialNumber(self):
        print ("***==== Change Serial Number  ====***")
        gid96 = self._gid96.encode(self._generalManager, None,self._objectClass ,None, self._serialNumber)
        print ("Serial Number Was %s" % gid96.getFieldValue("SerialNumber"))
        hex = gid96.toHex()
        print ("Old Hex = %s" % hex) 
        newSerial = 45678901
        gid96.setSerialNumber(newSerial)
        hex = gid96.toHex()
        print ("New Serial Number = %s" % newSerial)
        print ("New Hex  = %s"  % hex)
        factory = EPCFactory()
        gid96 = factory.parse(hex)
        print ("Serial Number after factory parse = %s" % int(gid96.getFieldValue("SerialNumber")))
        self.assertEquals(int(gid96.getFieldValue("SerialNumber")),newSerial)
        print ("***====END Change Serial Number  ====***")
    
    
    def _checkFields(self, epc):
        self.assertEqual(epc.getFieldValue("Header"),"53")
        self.assertEqual(int(epc.getFieldValue("GeneralManager")),int(self._generalManager))
        self.assertEqual(int(epc.getFieldValue("ObjectClass")),int(self._objectClass))
        self.assertEqual(int(epc.getFieldValue("SerialNumber")),int(self._serialNumber))
        print ("Field Values are Valid")
        self._checkBitsAndHex(epc)     
        
    def _checkBitsAndHex(self,epc):
    
        bits = epc.toBinary()
        hex = epc.toHex()
        headerValue = bits[epc.getField("Header").getOffset():epc.getField("Header").getBitLength()]
        self.assertEquals(int(headerValue,2),53)
        
        headerValue = hex[:2]
        self.assertEquals(int(headerValue,16),53)
         
        #Check the bits, contained in the hex, for the general manager 
        startPos = 8
        generalManagerBits = bits[8:8+28]
        generalManagerValue = BitArray(bin=generalManagerBits).uint 
        self.assertEquals(generalManagerValue,int(self._generalManager))
        
        startPos = startPos + epc.getField("GeneralManager").getBitLength()
        objectClassBits = bits[36:36+24]
        
        objectClassValue = BitArray(bin=objectClassBits).uint
        self.assertEquals(int(objectClassValue),int(self._objectClass))
        
        
        serialNumberBits = bits[36+24:36+24+36]
        serialNumberValue = BitArray(bin=serialNumberBits).uint
        self.assertEquals(serialNumberValue,int(self._serialNumber))
        print ("Bits and Hex are valid")
    
        
if __name__ == "__main__":
    unittest.main() 