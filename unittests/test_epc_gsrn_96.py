import unittest
from bitstring import BitArray
from epc.EPCFactory import EPCFactory
from epc.GSRN96 import GSRN96
from utils.Partitions import Partitions  


class GSRN96Test(unittest.TestCase):
    def setUp(self):
    #Changes these values to test different scenarios
        self._gsrn96 = GSRN96()
        #GS-1 GSRN is 18 Digits (Company Prefix + ServiceReference = 17) + (CD=1)
        self._companyPrefix = "035846802"
        self._serviceReference = "12345689"
        self._filter = 7
        self._reserved = 0
        
    
    def test_Encode(self):
        print ("==== Test Encode from Hex Value ====")
        epc_num = self._gsrn96.encode(self._companyPrefix, 0,self._serviceReference ,self._filter, 0)
        bits = epc_num.toBinary()
        self.assertEquals(len(bits),96)
        self._checkFields(epc_num)
        print (epc_num.toHex())
        print ("====END Test Decoding from Hex Value ====")
        print ("")
    
    def test_ParseHex(self):
        print ("==== Test Decoding from Hex Value ====")
        #Turn the tagpy number into a hex value and parse it through the factory
        epc = self._gsrn96.encode(self._companyPrefix, 0,self._serviceReference ,self._filter, 0)
        hex = epc.toHex()
        factory = EPCFactory()
        epc = factory.parse(hex)
        self._checkFields(epc)
        print (epc.toHex())
        print (epc.toBinary())
        print ("====END Test Decoding from Hex Value ====")
        print ("")
        
    def test_ParseBinary(self):
        print ("***==== Test Decoding from Binary Value ====***")
        epc = self._gsrn96.encode(self._companyPrefix, 0, self._serviceReference, self._filter, 0)
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
       
    
    def test_FromHex(self):
        print ("==== Test Decoding from Hex Value ====")
        #Turn the epc number into a hex value and parse it through the factory
        epc_num = self._gsrn96.encode(self._companyPrefix, 0, self._serviceReference, self._filter, 0)
        hex = epc_num.toHex()
        epc_num = epc_num.fromHex(hex)
        self._checkFields(epc_num)
        print(epc_num.toHex())
        print(epc_num.toBinary())
        print ("====END Test Decoding from Hex Value ====")
        print ("")
    
    def test_ParseEPCUri(self):
        print ("***==== Test Decode EPC Uri Value ====***")
        #TagURI=urn:epc:id:sgrn:0358468.202339
        tagUri = "urn:epc:id:gsrn:%s.%s" % (str(self._companyPrefix), str(self._serviceReference))
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
        tagUri = "urn:tagpy:tag:gsrn-96:%s.%s" % (str(self._companyPrefix), str(self._serviceReference))
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
        epc = self._gsrn96.encode(self._companyPrefix, 0,self._serviceReference ,self._filter, 0)
        print epc.toEPCTagUri()
        print ("***==== END  Test To EPC Tag Uri Value ====***")
        print ("") 
    
    
    def test_ToGS1(self):
        print ("***==== Test GS1  ====***")
        epc = self._gsrn96.encode(self._companyPrefix, 0,self._serviceReference ,self._filter, 0)
        print epc.toGS1()
        print ("***==== END  Test To GS1 ====***") 
        print ("")
    
    def test_ToGS1WithAIInParens(self):
        print ("***==== Test GS1 With AI in Parens  ====***")
        epc = self._gsrn96.encode(self._companyPrefix, 0,self._serviceReference ,self._filter, 0)
        print epc.toGS1(True)
        print ("***==== END Test To GS1 With AI in Parens ====***") 
        print ("")
        
    def test_ToGS1WithAIWithoutParens(self):
        print ("***==== Test GS1 With AI Without Parens  ====***")
        epc = self._gsrn96.encode(self._companyPrefix, 0,self._serviceReference ,self._filter, 0)
        print epc.toGS1(True,0,False)
        print ("***==== END Test To GS1 With AI Without Parens ====***") 
        print ("")
    
    def test_ChangeSerialNumber(self):
        print ("***==== Change Serial Number  ====***")
        epc = self._gsrn96.encode(self._companyPrefix, 0,self._serviceReference ,self._filter, 0)
        print ("Serial Number Was %s" % epc.getFieldValue("ServiceReference"))
        hex = epc.toHex()
        print ("Old Hex = %s" % hex) 
        newSerial = 123456
        epc.setSerialNumber(newSerial)
        hex = epc.toHex()
        print ("New Serial Number = %s"  % newSerial)
        print ("New Hex = %s"  % hex)
        factory = EPCFactory()
        epc = factory.parse(hex)
        self.assertEquals(int(epc.getFieldValue("ServiceReference")),newSerial)
        print ("***====END Change Serial Number  ====***")
        print ("")
    
    def test_ChangeFilter(self):
        print ("***==== Change Filter Number  ====***")
        epc = self._gsrn96.encode(self._companyPrefix, 0,self._serviceReference ,self._filter, 0)
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
        
        epc = self._gsrn96.encode(self._companyPrefix, 0,self._serviceReference ,self._filter, 0)
        #Turn the epc number into a hex value and parse it through the factory
        hex = epc.toHex()
        factory = EPCFactory()
        gdti96 = factory.parse(hex)
        
        print ("=== Format to HEX ===")
        print (gdti96.format("hex"))
        print ("===========================")
        print ("=== Format to BINARY ===")
        print (gdti96.format("binarY"))
        print ("===========================")
        print ("=== Format to JSON ===")
        print (gdti96.format("json"))
        
        
        
        print (gdti96.format("xml"))
        
        
        f = gdti96.format("DICTIONARY")
        for k, v in f.items():       
            print ("%s=%s\n" % (k, v)
        
        
        print (gdti96.format("gs1"))   
        
    
            
    def _checkFields(self,epc):
        
        partitions = Partitions()
        partitionValue = partitions.getPartitionValue(len(self._companyPrefix), "GSRN")
        
        self.assertEqual(epc.getFieldValue("Header"),"45")
        self.assertEqual(epc.getFieldValue("Filter"),str(self._filter))
        self.assertEqual(str(epc.getFieldValue("Partition")),str(partitionValue))
        self.assertEqual(epc.getFieldValue("CompanyPrefix"),str(self._companyPrefix))
        self.assertEqual(epc.getFieldValue("ServiceReference"),str(self._serviceReference))
        self.assertEqual(int(epc.getFieldValue("Reserved")),int(self._reserved))
        print ("Field Values are Valid")
        self._checkBitsAndHex(epc)     
        
    def _checkBitsAndHex(self,epc):
    
        bits = epc.toBinary()
        hex = epc.toHex()
        headerValue = bits[epc.getField("Header").getOffset():epc.getField("Header").getBitLength()]
        self.assertEquals(int(headerValue,2),45)
        
        headerValue = hex[:2]
        self.assertEquals(int(headerValue,16),45)
        
        filterValue = bits[epc.getField("Filter").getOffset():int(epc.getField("Filter").getOffset()) + int(epc.getField("Filter").getBitLength())]
        self.assertEquals(int(filterValue,2),int(self._filter))
        partitionValue = bits[epc.getField("Partition").getOffset():int(epc.getField("Partition").getOffset()) + int(epc.getField("Partition").getBitLength())]
        partitionValue = int(partitionValue,2)
        #Check the bits, contained in the hex, for the company prefix
        
        
        companyPrefixBits = bits[14:14+epc.getField("CompanyPrefix").getBitLength()]
        companyPrefixValue = BitArray(bin=companyPrefixBits).uint 
        self.assertEquals(companyPrefixValue,int(self._companyPrefix))
        
        startPos = 14 + epc.getField("CompanyPrefix").getBitLength()
        serviceReferenceBits = bits[startPos:startPos+epc.getField("ServiceReference").getBitLength()]
        
        
        serviceReferenceValue = str(int(serviceReferenceBits,2)).zfill(epc.getField("ServiceReference").getDigitLength())
        self.assertEquals(str(serviceReferenceValue),str(self._serviceReference))
        print ("Bits and Hex are valid"   
        
        
            
if __name__ == "__main__":
    unittest.main()        