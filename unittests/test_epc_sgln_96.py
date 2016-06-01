import unittest
from bitstring import BitArray
from epc.EPCFactory import EPCFactory
from epc.SGLN96 import SGLN96
from utils.Partitions import Partitions  

class SGLN96Test(unittest.TestCase):
    def setUp(self):
    #Change these values to test different scenarios
        self._sgln96 = SGLN96()
        self._companyPrefix = "0370000"
        self._locationReference = "21028"
        self._filter = 7
        self._extension = 1234567890
    
    def test_Encode(self):
        print ("==== Test Encode from Hex Value ====")
        epc_num = self._sgln96.encode(self._companyPrefix, None,self._locationReference ,self._filter, self._extension)
        bits = epc.toBinary()
        self.assertEquals(len(bits),96)
        self._checkFields(epc_num)
        print (epc_num.toHex())
        print ("====END Test Decoding from Hex Value ====")
        print ("")
    
    def test_ParseHex(self):
        print ("==== Test Decoding from Hex Value ===="
        #Turn the tagpy number into a hex value and parse it through the factory
        epc = self._sgln96.encode(self._companyPrefix, None,self._locationReference ,self._filter, self._extension)
        hex = epc.toHex()
        factory = EPCFactory()
        epc = factory.parse(hex)
        self._checkFields(epc)
        print epc.toHex()
        print epc.toBinary()
        print ("====END Test Decoding from Hex Value ===="
        print (""
    
    def test_ParseBinary(self):
        print ("***==== Test Decoding from Binary Value ====***"
        epc = self._sgln96.encode(self._companyPrefix, None,self._locationReference ,self._filter, self._extension)
        bin = epc.toBinary()
        self.assertEquals(len(bin),96)
        factory = EPCFactory()
        #Take the binary value and parse it through the factory
        epc = factory.parse(bin)
        self._checkFields(epc)
        print epc.toHex()
        print epc.toBinary()
        print ("====END Test Decoding from Binary Value ===="
        print (""
    
    def test_ParseRawUri(self):
        print ("***==== Test Decode Raw Uri Value ====***"
        epc = self._sgln96.encode(self._companyPrefix, None,self._locationReference ,self._filter, self._extension)
        rawUri = epc.toEPCRawUri()
        factory = EPCFactory()
        #Take the Raw URI value and parse it through the factory
        epc = factory.parse(rawUri)
        self._checkFields(epc)
        print epc.toHex()
        print epc.toBinary()
        print ("***==== END Test Decode Raw Uri Value ====***"
        print (""
    
    def test_ParseEPCUri(self):
        print ("***==== Test Decode EPC Uri Value ====***"
        #TagURI=urn:tagpy:id:sgln:0358468.202339.000395
        tagUri = "urn:tagpy:id:sgln:%s.%s.%s" % (str(self._companyPrefix), str(self._locationReference),str(self._extension))
        factory = EPCFactory()
        #Take the Raw URI value and parse it through the factory
        epc = factory.parse(tagUri)
        #Change the filter because the filter is not part filter the pure identity is not available
        #Set the filter to the test's module level filter value
        epc.setFieldValue("Filter", self._filter)
        self._checkFields(epc)
        print tagUri
        print epc.toHex()
        print epc.toBinary()
        print ("***==== END Test EPC URI Value ====***"
        print (""
    
    def test_ParseEPCTagUri(self):
        print ("***==== Test Decode EPC Tag Uri Value ====***"
        tagUri = "urn:tagpy:tag:sgln-96:%s.%s.%s" % (str(self._companyPrefix), str(self._locationReference),str(self._extension))
        factory = EPCFactory()
        #Take the Tag URI value and parse it through the factory
        epc = factory.parse(tagUri)
        #Set the filter to the test's module level filter value
        epc.setFieldValue("Filter", self._filter)
        self._checkFields(epc)
        print epc.toHex()
        print ("***==== END Test Decode EPC Tag Uri Value ====***"
        print (""
    
    def test_ToEPCTagUri(self):
        print ("***==== Test To EPC Tag Uri Value ====***"
        epc = self._sgln96.encode(self._companyPrefix, None,self._locationReference ,self._filter, self._extension)
        print epc.toEPCTagUri()
        print ("***==== END  Test To EPC Tag Uri Value ====***"
        print (""
    
    def test_ToRawUri(self):
        print ("***==== Test To Raw Uri Value ====***"
        epc = self._sgln96.encode(self._companyPrefix, None,self._locationReference ,self._filter, self._extension)
        print epc.toEPCRawUri()
        print ("***==== END  Test To EPC Tag Uri Value ====***" 
        print ("" 
    
    def test_ToGS1(self):
        print ("***==== Test GS1  ====***"
        epc = self._sgln96.encode(self._companyPrefix, None,self._locationReference ,self._filter, self._extension)
        print epc.toGS1()
        print ("***==== END  Test To GS1 ====***" 
        print (""
    
    def test_ToGS1WithAIInParens(self):
        print ("***==== Test GS1 With AI in Parens  ====***"
        epc = self._sgln96.encode(self._companyPrefix, None,self._locationReference ,self._filter, self._extension)
        print epc.toGS1(True)
        print ("***==== END Test To GS1 With AI in Parens ====***" 
        print (""
    
    def test_ToGS1WithAIWithoutParens(self):
        print ("***==== Test GS1 With AI Without Parens  ====***"
        epc = self._sgln96.encode(self._companyPrefix, None,self._locationReference ,self._filter, self._extension)
        print epc.toGS1(False)
        print ("***==== END Test To GS1 With AI Without Parens ====***" 
        print (""
    
    def test_ChangeSerialNumber(self):
        print ("***==== Change Serial Number  ====***"
        epc = self._sgln96.encode(self._companyPrefix, None,self._locationReference ,self._filter, self._extension)
        print ("Extension Was %s" % epc.getFieldValue("Extension")
        hex = epc.toHex()
        print ("Old Hex = %s" % hex 
        newSerial = 123456
        epc.setSerialNumber(newSerial)
        hex = epc.toHex()
        print ("New Extension Number = %s"  % newSerial
        print ("New Hex = %s"  % hex
        factory = EPCFactory()
        epc = factory.parse(hex)
        self.assertEquals(int(epc.getFieldValue("Extension")),newSerial)
        print ("***====END Change Serial Number  ====***"
        print (""
    
    def test_ChangeFilter(self):
        print ("***==== Change Filter Number  ====***"
        epc = self._sgln96.encode(self._companyPrefix, None,self._locationReference ,self._filter, self._extension)
        print ("Filter Number Was %s" % epc.getFieldValue("Filter")
        hex = epc.toHex()
        print ("Old Hex = %s" % hex
        if(self._filter < 1): 
            newFilter = self._filter + 1
        else:
            newFilter = self._filter - 1 
        
        epc.setFieldValue("Filter",newFilter)
        hex = epc.toHex()
        print ("New Filter Number = %s " % newFilter
        print ("New Hex = %s " % hex
        factory = EPCFactory()
        epc = factory.parse(hex)
        self.assertEquals(int(epc.getFieldValue("Filter")),newFilter)
        print ("***====END Change Filter Number  ====***"
    
    def test_Formats(self):
        
        print ("***==== Test Formatting ====***"
        
        epc = self._sgln96.encode(self._companyPrefix, None,self._locationReference ,self._filter, self._extension)
        #Turn the tagpy number into a hex value and parse it through the factory
        hex = epc.toHex()
        factory = EPCFactory()
        sgln96 = factory.parse(hex)
        
        print ("=== Format to HEX ==="
        print sgln96.format("hex")
        print ("==========================="
        print ("=== Format to BINARY ==="
        print sgln96.format("binarY")
        print ("==========================="
        print ("=== Format to JSON ==="
        print sgln96.format("json")
        print ("==========================="
        print ("=== Format to RAW_URI ==="
        print sgln96.format("raw_uRI")
        print ("==========================="
        print ("=== Format to XML ==="
        print sgln96.format("xml")
        print ("==========================="
        print ("=== Format to DICTIONARY ==="
        f = sgln96.format("DICTIONARY")
        for k, v in f.items():       
            print ("%s=%s\n" % (k, v)
        print ("==========================="
        print ("=== Format to gs1 ==="
        print sgln96.format("gs1")    
        print ("==========================="
    
    
    
    def _checkFields(self,epc):
        
        partitions = Partitions()
        partitionValue = partitions.getPartitionValue(len(self._companyPrefix), "GDTI")
        
        self.assertEqual(epc.getFieldValue("Header"),"50")
        self.assertEqual(epc.getFieldValue("Filter"),str(self._filter))
        self.assertEqual(str(epc.getFieldValue("Partition")),str(partitionValue))
        self.assertEqual(epc.getFieldValue("CompanyPrefix"),str(self._companyPrefix))
        self.assertEqual(int(epc.getFieldValue("LocationReference")),int(self._locationReference))
        self.assertEqual(int(epc.getSerialNumber()),int(self._extension))
        print ("Field Values are Valid"
        self._checkBitsAndHex(epc)     
        
    def _checkBitsAndHex(self,epc):
    
        bits = epc.toBinary()
        hex = epc.toHex()
        headerValue = bits[epc.getField("Header").getOffset():epc.getField("Header").getBitLength()]
        self.assertEquals(int(headerValue,2),50)
        
        headerValue = hex[:2]
        self.assertEquals(int(headerValue,16),50)
        
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
        
        
        locationReferenceBits = bits[epc.getField("LocationReference").getOffset():epc.getField("LocationReference").getOffset()+epc.getField("LocationReference").getBitLength()]
        
        
        locationReferenceValue = str(int(locationReferenceBits,2)).zfill(epc.getField("LocationReference").getDigitLength())
        self.assertEquals(int(locationReferenceValue),int(self._locationReference))
        print ("Bits and Hex are valid"   
        
        
            
if __name__ == "__main__":
    unittest.main()       