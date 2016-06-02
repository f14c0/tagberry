import unittest
from epc.EPCFactory import EPCFactory
from epc.GDTI96 import GDTI96
from utils.Partitions import Partitions  
from bitstring import BitArray

class GDTI96Test(unittest.TestCase):
    def setUp(self):
    #Change these values to test different scenarios
        self._gdti96 = GDTI96()
        self._companyPrefix = "012345678"
        self._documentType = "349"
        self._filter = 7
        self._serialNumber = 395
    
    def test_Encode(self):
        print("==== Test Encode from Hex Value ====")
        epc = self._gdti96.encode(self._companyPrefix, None,self._documentType ,self._filter, self._serialNumber)
        bits = epc.toBinary()
        self.assertEquals(len(bits),96)
        self._checkFields(epc)
        print (epc.toHex())
        print ("====END Test Decoding from Hex Value ====")
        print ("")
    
    def test_ParseHex(self):
        print ("==== Test Parse Hex Value ====")
        #Turn the tagpy number into a hex value and parse it through the factory
        epc = self._gdti96.encode(self._companyPrefix, None,self._documentType ,self._filter, self._serialNumber)
        hex = epc.toHex()
        factory = EPCFactory()
        epc = factory.parse(hex)
        self._checkFields(epc)
        print (epc.toHex())
        print (epc.toBinary())
        print ("====END Test Parse Hex Value ====")
        print ("")
    
    def test_FromHex(self):
        print ("==== Test Decoding from Hex Value ====")
        #Turn the tagpy number into a hex value and parse it through the factory
        epc = self._gdti96.encode(self._companyPrefix, None,self._documentType ,self._filter, self._serialNumber)
        hex = epc.toHex()
        epc = epc.fromHex(hex)
        self._checkFields(epc)
        print (epc.toHex())
        print (epc.toBinary())
        print ("====END Test Decoding from Hex Value ====")
        print ("")
    
    
    def test_ParseBinary(self):
        print ("***==== Test Decoding from Binary Value ====***")
        epc = self._gdti96.encode(self._companyPrefix, None,self._documentType ,self._filter, self._serialNumber)
        bin = epc.toBinary()
        self.assertEquals(len(bin),96)
        factory = EPCFactory()
        #Take the binary value and parse it through the factory
        epc = factory.parse(bin)
        self._checkFields(epc)
        print (epc.toHex())
        print (epc.toBinary())
        print ("====END Test Decoding from Binary Value ====")
        print ("")
    
    
    def test_ParseEPCUri(self):
        print ("***==== Test Decode EPC Uri Value ====***")
        #TagURI=urn:tagpy:id:gdti:0358468.202339.000395
        tagUri = "urn:tagpy:id:gdti:%s.%s.%s" % (str(self._companyPrefix), str(self._documentType),str(self._serialNumber))
        factory = EPCFactory()
        #Take the URI value and parse it through the factory
        epc = factory.parse(tagUri)
        #Change the filter because the filter is not part filter the pure identity is not available
        #Set the filter to the test's module level filter value
        epc.setFieldValue("Filter", self._filter)
        self._checkFields(epc)
        print (tagUri)
        print (epc.toHex())
        print (epc.toBinary())
        print ("***==== END Test EPC URI Value ====***")
        print ("")
    
    def test_ParseEPCTagUri(self):
        print ("***==== Test Decode EPC Tag Uri Value ====***")
        tagUri = "urn:tagpy:tag:gdti-96:%s.%s.%s.%s" % (self._filter,str(self._companyPrefix), str(self._documentType),str(self._serialNumber))
        factory = EPCFactory()
        #Take the Tag URI value and parse it through the factory
        epc = factory.parse(tagUri)
        #Set the filter to the test's module level filter value
        epc.setFieldValue("Filter", self._filter)
        self._checkFields(epc)
        print (epc.toHex())
        print ("***==== END Test Decode EPC Tag Uri Value ====***")
        print ("")
        
    def test_ToEPCTagUri(self):
        print ("***==== Test To EPC Tag Uri Value ====***")
        epc = self._gdti96.encode(self._companyPrefix, None,self._documentType ,self._filter, self._serialNumber)
        print (epc.toEPCTagUri())
        print ("***==== END  Test To EPC Tag Uri Value ====***")
        print ("")
        
   
    def test_ToGS1(self):
        print ("***==== Test GS1  ====***")
        epc = self._gdti96.encode(self._companyPrefix, 0,self._documentType ,self._filter, self._serialNumber)
        print (epc.toGS1())
        print ("***==== END  Test To GS1 ====***") 
        print ("")
    
    def test_ToGS1WithAIInParens(self):
        print ("***==== Test GS1 With AI in Parens  ====***")
        epc = self._gdti96.encode(self._companyPrefix, 0,self._documentType ,self._filter, self._serialNumber)
        print (epc.toGS1(True))
        print ("***==== END Test To GS1 With AI in Parens ====***") 
        print ("")
    
    def test_ToGS1WithAIWithoutParens(self):
        print ("***==== Test GS1 With AI Without Parens  ====***")
        epc = self._gdti96.encode(self._companyPrefix, 0,self._documentType ,self._filter, self._serialNumber)
        print (epc.toGS1(False))
        print ("***==== END Test To GS1 With AI Without Parens ====***") 
        print ("")
    
    def test_ChangeSerialNumber(self):
        print ("***==== Change Serial Number  ====***")
        epc = self._gdti96.encode(self._companyPrefix, 0,self._documentType ,self._filter, self._serialNumber)
        print ("Serial Number Was %s" % epc.getFieldValue("Serial"))
        hex = epc.toHex()
        print ("Old Hex = %s" % hex )
        newSerial = 123456
        epc.setSerialNumber(newSerial)
        hex = epc.toHex()
        print ("New Serial Number = %s"  % newSerial)
        print ("New Hex = %s"  % hex)
        factory = EPCFactory()
        epc = factory.parse(hex)
        self.assertEquals(int(epc.getFieldValue("Serial")),newSerial)
        print ("***====END Change Serial Number  ====***")
        print ("")
    
    def test_ChangeFilter(self):
        print ("***==== Change Filter Number  ====***")
        epc = self._gdti96.encode(self._companyPrefix, 0,self._documentType ,self._filter, self._serialNumber)
        print ("Filter Number Was %s" % epc.getFieldValue("Filter"))
        hex = epc.toHex()
        print ("Old Hex = %s" % hex)
        if(self._filter < 1): 
            newFilter = self._filter + 1
        else:
            newFilter = self._filter - 1 
        
        epc.setFieldValue("Filter",newFilter)
        hex = epc.toHex()
        print ("New Filter Number = %s " % newFilter)
        print ("New Hex = %s " % hex)
        factory = EPCFactory()
        epc = factory.parse(hex)
        self.assertEquals(int(epc.getFieldValue("Filter")),newFilter)
        print ("***====END Change Filter Number  ====***")
    
    def test_Formats(self):
        
        print ("***==== Test Formatting ====***")
        
        epc = self._gdti96.encode(self._companyPrefix, 0, self._documentType, self._filter, self._serialNumber)
        #Turn the tagpy number into a hex value and parse it through the factory
        hex = epc.toHex()
        factory = EPCFactory()
        gdti96 = factory.parse(hex)
        
        print ("=== Format to HEX ===")
        print (gdti96.format("hex"))
        print ("===========================")
        print ("=== Format to BINARY ===")
        print (gdti96.format("binary"))
        print ("===========================")
        print ("=== Format to JSON ===")
        print (gdti96.format("json"))
        print ("===========================")
       
        print ("===========================")
        print ("=== Format to XML ===")
        print (gdti96.format("xml"))
        print ("===========================")
        print ("=== Format to DICTIONARY ===")
        f = gdti96.format("DICTIONARY")
        for k, v in f.items():       
            print ("%s=%s\n" % (k, v))
        print ("===========================")
        print ("=== Format to gs1 ===")
        print (gdti96.format("gs1"))    
        print ("===========================")
        print ("")
        
    def test_toGDTI(self):
        print ("***==== Test toGDTI ====***")
        epc = self._gdti96.encode(self._companyPrefix, 0,self._documentType ,self._filter, self._serialNumber)
        print (epc.toGDTI())
        print ("===========================")
        print ("")
    def _checkFields(self,epc):
        
        partitions = Partitions()
        partitionValue = partitions.getPartitionValue(len(self._companyPrefix), "GDTI")
        
        self.assertEqual(epc.getFieldValue("Header"),"44")
        self.assertEqual(epc.getFieldValue("Filter"),str(self._filter))
        self.assertEqual(str(epc.getFieldValue("Partition")),str(partitionValue))
        self.assertEqual(epc.getFieldValue("CompanyPrefix"),str(self._companyPrefix))
        self.assertEqual(epc.getFieldValue("DocumentType"),str(self._documentType))
        self.assertEqual(int(epc.getSerialNumber()),int(self._serialNumber))
        print ("Field Values are Valid")
        self._checkBitsAndHex(epc)     
    
    
        
    def _checkBitsAndHex(self,epc):
    
        bits = epc.toBinary()
        hex = epc.toHex()
        headerValue = bits[epc.getField("Header").getOffset():epc.getField("Header").getBitLength()]
        self.assertEquals(int(headerValue,2),44)
        
        headerValue = hex[:2]
        self.assertEquals(int(headerValue,16),44)
        
        filterValue = bits[epc.getField("Filter").getOffset():int(epc.getField("Filter").getOffset()) + int(epc.getField("Filter").getBitLength())]
        self.assertEquals(int(filterValue,2),int(self._filter))
        hexBodyValue = hex[2:]
        hexBodyBits = BitArray(hex=hexBodyValue).bin[2:]
        partitionValue = bits[epc.getField("Partition").getOffset():int(epc.getField("Partition").getOffset()) + int(epc.getField("Partition").getBitLength())]
        partitionValue = int(partitionValue,2)
        #Check the bits, contained in the hex, for the company prefix
        
        
        companyPrefixBits = bits[epc.getField("CompanyPrefix").getOffset():epc.getField("CompanyPrefix").getOffset()+epc.getField("CompanyPrefix").getBitLength()]
        companyPrefixValue = BitArray(bin=companyPrefixBits).uint 
        self.assertEquals(companyPrefixValue,int(self._companyPrefix))
        
        
        documentTypeBits = bits[epc.getField("DocumentType").getOffset():epc.getField("DocumentType").getOffset()+epc.getField("DocumentType").getBitLength()]
        
        
        documentTypeValue = str(int(documentTypeBits,2)).zfill(epc.getField("DocumentType").getDigitLength())
        self.assertEquals(str(documentTypeValue),str(self._documentType))
        print ("Bits and Hex are valid")   
        
        
            
if __name__ == "__main__":
    unittest.main()        
    
    