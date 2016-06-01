import unittest
from encoding.EPCFactory import EPCFactory
from encoding.GIAI96 import GIAI96
from utils.Partitions import Partitions
from bitstring import BitArray    

class GIAI96Test(unittest.TestCase):
    def setUp(self):
        self._giai96 = GIAI96()
        self._companyPrefix = "02345678"
        self._itemRef = "12345678901"
        self._filter = 7
    
    def test_Encode(self):
        print ("==== Test Encode from Hex Value ====")
        epc = self._giai96.encode(self._companyPrefix, None,self._itemRef ,self._filter, None)
        bits = epc.toBinary()
        self.assertEquals(len(bits),96)
        self._checkFields(epc)
        print (epc.toHex())
        print (bits)
        print ("====END Test Decoding from Hex Value ====")
        print ("")
    
    def test_ParseHex(self):
        print ("==== Test Decoding from Hex Value ====")
        #Turn the tagpy number into a hex value and parse it through the factory
        epc = self._giai96.encode(self._companyPrefix, None,self._itemRef ,self._filter, None)
        hex = epc.toHex()
        factory = EPCFactory()
        epc = factory.parse(hex)
        self._checkFields(epc)
        print (epc.toHex())
        print (epc.toBinary())
        print ("====END Test Decoding from Hex Value ====")
        print ("")
    
    def test_FromHex(self):
        print ("==== Test Decoding from Hex Value ====")
        #Turn the tagpy number into a hex value and parse it through the factory
        epc = self._giai96.encode(self._companyPrefix, None,self._itemRef ,self._filter, None)
        hex = epc.toHex()
        epc = epc.fromHex(hex)
        self._checkFields(epc)
        print (epc.toHex())
        print (epc.toBinary())
        print ("====END Test Decoding from Hex Value ====")
        print ("")
    
    def test_ParseBinary(self):
        print ("***==== Test Decoding from Binary Value ====***")
        epc = self._giai96.encode(self._companyPrefix, None,self._itemRef ,self._filter, None)
        bin = epc.toBinary()
        self.assertEquals(len(bin),96)
        factory = EPCFactory()
        #Take the binary value and parse it through the factory
        sgtin96 = factory.parse(bin)
        self._checkFields(epc)
        print (sgtin96.toHex())
        print (sgtin96.toBinary())
        print ("====END Test Decoding from Binary Value ====")
        print ("")
    
    def test_ParseRawUri(self):
        print ("***==== Test Decode Raw Uri Value ====***")
        epc = self._giai96.encode(self._companyPrefix, None,self._itemRef ,self._filter, None)
        rawUri = epc.toEPCRawUri()
        factory = EPCFactory()
        #Take the Raw URI value and parse it through the factory
        epc = factory.parse(rawUri)
        self._checkFields(epc)
        print (epc.toHex())
        print (epc.toBinary())
        print ("***==== END Test Decode Raw Uri Value ====***")
        print ("")
   
    def test_ParseEPCUri(self):
        print ("***==== Test Decode EPC Uri Value ====***")
        #TagURI=urn:tagpy:id:sgtin:0358468.202339.000395
        tagUri = "urn:tagpy:id:giai:%s.%s" % (str(self._companyPrefix),str(self._itemRef))
        factory = EPCFactory()
        #Take the Raw URI value and parse it through the factory
        epc = factory.parse(tagUri)
        #Change the filter because the filter is not part filter the pure identity is not available
        self._filter = 0
        self._checkFields(epc)
        print (tagUri)
        print (epc.toHex())
        print (epc.toBinary())
        print ("***==== END Test EPC URI Value ====***")
        print ("")
    
    def test_ParseEPCTagUri(self):
        print ("***==== Test Decode EPC Tag Uri Value ====***")
        tagUri = "urn:tagpy:tag:giai-96:%s.%s.%s" % (str(self._filter),str(self._companyPrefix),str(self._itemRef))
        factory = EPCFactory()
        #Take the Tag URI value and parse it through the factory
        epc = factory.parse(tagUri)
        self._checkFields(epc)
        print (epc.toHex())
        print (epc.toBinary())
        print ("***==== END Test Decode EPC Tag Uri Value ====***")
        print ("")
        
    def test_ToEPCTagUri(self):
        print ("***==== Test To EPC Tag Uri Value ====***")
        epc = self._giai96.encode(self._companyPrefix, None,self._itemRef ,self._filter, None)
        print (epc.toEPCTagUri())
        print ("***==== END  Test To EPC Tag Uri Value ====***")
        print ("")
    
    def test_ToRawUri(self):
        print ("***==== Test To Raw Uri Value ====***")
        epc = self._giai96.encode(self._companyPrefix, None,self._itemRef ,self._filter, None)
        print (epc.toEPCRawUri())
        print ("***==== END  Test To EPC Tag Uri Value ====***") 
        print ("")
    
    def test_ToGS1(self):
        print ("***==== Test GS1  ====***")
        epc = self._giai96.encode(self._companyPrefix, None,self._itemRef ,self._filter, None)
        print (epc.toGS1())
        print ("***==== END  Test To GS1 ====***") 
        print ("")
        
    def test_ToGS1WithAIInParens(self):
        print ("***==== Test GS1 With AI in Parens  ====***")
        epc = self._giai96.encode(self._companyPrefix, None,self._itemRef ,self._filter, None)
        print (epc.toGS1(True))
        print ("***==== END Test To GS1 With AI in Parens ====***") 
        print ("")
        
    def test_ToGS1WithAIWithoutParens(self):
        print ("***==== Test GS1 With AI Without Parens  ====***")
        epc = self._giai96.encode(self._companyPrefix, None,self._itemRef ,self._filter, None)
        print (epc.toGS1(True,0,False))
        print ("***==== END Test To GS1 With AI Without Parens ====***") 
        print ("")
    
    def test_ChangeFilter(self):
        print ("***==== Change Filter Number  ====***")
        epc = self._giai96.encode(self._companyPrefix, None,self._itemRef ,self._filter, None)
        print ("Filter Number Was %s" % epc.getFieldValue("Filter"))
        hex_val = epc.toHex()
        print ("Old Hex = %s" % hex_val)
        if(self._filter < 1): 
            self._filter = self._filter + 1
        else:
            self._filter = self._filter - 1 
             
        epc.setFieldValue("Filter",self._filter)
        hex_val = epc.toHex()
        print ("New Filter Number = %s " % self._filter)
        print ("New Hex = %s " % hex_val)
        factory = EPCFactory()
        epc = factory.parse(hex_val)
        self._checkFields(epc)
        self.assertEquals(int(epc.getFieldValue("Filter")), self._filter)
        print ("***====END Change Filter Number  ====***")
    
    def test_Formats(self):
        
        print ("***==== Test Formatting ====***")
        #Start with this GTIN-14 20358468023395
        epc = self._giai96.encode(self._companyPrefix, None,self._itemRef ,self._filter, None)
        #Turn the tagpy number into a hex_val value and parse it through the factory
        hex_val = epc.toHex()
        factory = EPCFactory()
        epc = factory.parse(hex_val)
        
        print ("=== Format to HEX ===")
        print (epc.format("hex"))
        print ("==========================="
        print ("=== Format to BINARY ===")
        print (epc.format("binary"))
        print ("=== Format to XML ==="
        print (epc.format("xml"))
        print ("===========================")
        print ("=== Format to JSON ===")
        print (epc.format("json"))
        print ("===========================")
        print ("=== Format to RAW_URI ===")
        print (epc.format("raw_uri"))
        print ("==========================="
        print ("=== Format to DICTIONARY ==="
        f = epc.format("DICTIONARY")
        for k, v in f.items():       
            print ("%s=%s\n" % (k, v)
        print ("===========================")
        print ("=== Format to gs1 ===")
        print (epc.format("gs1"))    
        print ("===========================")
    
        
    def _checkFields(self,epc):
    
        partitions = Partitions()
        partitionValue = partitions.getPartitionValue(len(self._companyPrefix), "GIAI")
        
        self.assertEqual(epc.getFieldValue("Header"),"52")
        self.assertEqual(epc.getFieldValue("Filter"),str(self._filter))
        self.assertEqual(str(epc.getFieldValue("Partition")),str(partitionValue))
        self.assertEqual(epc.getFieldValue("CompanyPrefix"),str(self._companyPrefix))
        self.assertEqual(epc.getFieldValue("IndividualAssetReference"),str(self._itemRef))
        
        print ("Field Values are Valid"
        self._checkBitsAndHex(epc)     
        
    def _checkBitsAndHex(self,epc):
    
        bits = epc.toBinary()
        hex_val = epc.toHex()
        headerValue = bits[epc.getField("Header").getOffset():epc.getField("Header").getBitLength()]
        self.assertEquals(int(headerValue,2),52)
        
        headerValue = hex_val[:2]
        self.assertEquals(int(headerValue,16),52)
        
        filterValue = bits[epc.getField("Filter").getOffset():int(epc.getField("Filter").getOffset()) + int(epc.getField("Filter").getBitLength())]
        self.assertEquals(int(filterValue,2),int(self._filter))
        
        hexBodyBits = BitArray(hex_val=hex_val).bin[2:]
        partitionValue = bits[epc.getField("Partition").getOffset():int(epc.getField("Partition").getOffset()) + int(epc.getField("Partition").getBitLength())]
        partitionValue = int(partitionValue,2)
        #Check the bits, contained in the hex_val, for the company prefix
        
        companyPrefixBits = hexBodyBits[epc.getField("CompanyPrefix").getOffset():epc.getField("CompanyPrefix").getOffset()+epc.getField("CompanyPrefix").getBitLength()]
        companyPrefixValue = BitArray(bin=companyPrefixBits).uint 
        self.assertEquals(companyPrefixValue,int(self._companyPrefix))
        
        
        itemReferenceBits = hexBodyBits[epc.getField("IndividualAssetReference").getOffset():epc.getField("IndividualAssetReference").getOffset()+epc.getField("IndividualAssetReference").getBitLength()]
        itemReferenceValue = BitArray(bin=itemReferenceBits).uint
        self.assertEquals(int(itemReferenceValue),int(self._itemRef))
        print ("Bits and Hex are valid"   
        
        
            
if __name__ == "__main__":
    unittest.main()       