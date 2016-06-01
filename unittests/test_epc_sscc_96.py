import unittest
from epc.EPCFactory import EPCFactory
from epc.SSCC96 import SSCC96
from utils.Partitions import Partitions
from bitstring import BitArray    

class SSCC96Test(unittest.TestCase):
    def setUp(self):
        #Changes these values to test different scenarios
        #SSCC -(00) 1 0614141 234567890 8
        
        #urn:tagpy:id:sscc:0358468.8000000279
        self._sscc96 = SSCC96()
        self._companyPrefix = "0358468"
        self._serialRef = "000000279"
        self._extensionDigit = "8"
        self._filter = 2
        
    def test_Encode(self):
        print("==== Test Encode from Hex Value ====")
        #Start with this SSCC-18 20358468023395
        sscc96 = self._sscc96.encode(self._companyPrefix, self._extensionDigit,self._serialRef ,self._filter, 0)
        bits = sscc96.toBinary()
        
        self.assertEquals(len(bits),96)
        self._checkFields(sscc96)
        print( sscc96.toHex() )
        print ( bits )
        print ("====END Test Decoding from Hex Value ====" )
        print ("")
    
    def test_ParseHex(self):
        print ("==== Test Decoding from Hex Value ===="
        #Turn the tagpy number into a hex value and parse it through the factory
        sscc96 = self._sscc96.encode(self._companyPrefix, self._extensionDigit,self._serialRef ,self._filter, 0)
        factory = EPCFactory()
        sscc96 = factory.parse(sscc96.toHex())
        self._checkFields(sscc96)
        print sscc96.toHex()
        print sscc96.toBinary()
        print ("====END Test Decoding from Hex Value ===="
        print (""
    
    def test_ParseBinary(self):
        print ("***==== Test Decoding from Binary Value ====***"
        sscc96 = self._sscc96.encode(self._companyPrefix, self._extensionDigit,self._serialRef ,self._filter, 0)
        bin = sscc96.toBinary()
        self.assertEquals(len(bin),96)
        factory = EPCFactory()
        #Take the binary value and parse it through the factory
        sscc96 = factory.parse(bin)
        self._checkFields(sscc96)
        print sscc96.toHex()
        print sscc96.toBinary()
        print ("====END Test Decoding from Binary Value ===="
        print (""
     
    def test_ParseRawUri(self):
        print ("***==== Test Decode Raw Uri Value ====***"
        
        sscc96 = self._sscc96.encode(self._companyPrefix, self._extensionDigit,self._serialRef ,self._filter, 0)
        rawUri = sscc96.toEPCRawUri()
        print ("Raw URI = " + rawUri 
        factory = EPCFactory()
        #Take the Raw URI value and parse it through the factory
        sscc96 = factory.parse(rawUri)
        self._checkFields(sscc96)
        print sscc96.toHex()
        print sscc96.toBinary()
        print ("***==== END Test Decode Raw Uri Value ====***"
        print (""
    
    def test_FromHex(self):
        print ("==== Test Decoding from Hex Value ===="
        epc = self._sscc96.encode(self._companyPrefix, self._extensionDigit,self._serialRef ,self._filter, 0)
        hex = epc.toHex()
        epc = epc.fromHex(hex)
        self._checkFields(epc)
        print epc.toHex()
        print epc.toBinary()
        print ("====END Test Decoding from Hex Value ===="
        print (""  
        
    def test_ParseEPCUri(self):
        print ("***==== Test Decode EPC Uri Value ====***"
        #TagURI=urn:tagpy:id:sscc:0358468.202339
        sscc96 = self._sscc96.encode(self._companyPrefix, self._extensionDigit,self._serialRef ,self._filter, 0)
        tagUri = sscc96.toEPCUri()
        print ("EPC URI = " + tagUri
        factory = EPCFactory()
        #Take the Raw URI value and parse it through the factory
        sscc96 = factory.parse(tagUri)
        #Change the filter because the filter is not part filter the pure identity is not available
        self._filter = 0
        self._checkFields(sscc96)
        print sscc96.toHex()
        print sscc96.toBinary()
        print ("***==== END Test EPC URI Value ====***"
        print (""
    
    def test_ParseEPCTagUri(self):
        print ("***==== Test Decode EPC Tag Uri Value ====***"
        sscc96 = self._sscc96.encode(self._companyPrefix, self._extensionDigit,self._serialRef ,self._filter, 0)
        tagUri = sscc96.toEPCTagUri()
        print ("Tag URI = " + tagUri
        factory = EPCFactory()
        #Take the Tag URI value and parse it through the factory
        sscc96 = factory.parse(tagUri)
        self._checkFields(sscc96)
        print sscc96.toHex()
        print ("***==== END Test Decode EPC Tag Uri Value ====***"
        print (""
    
    def test_ToEPCTagUri(self):
        print ("***==== Test To EPC Tag Uri Value ====***"
        sscc96 = self._sscc96.encode(self._companyPrefix, self._extensionDigit,self._serialRef ,self._filter)
        print sscc96.toEPCTagUri()
        print ("***==== END  Test To EPC Tag Uri Value ====***" 
        print (""
    
    def test_ToRawUri(self):
        print ("***==== Test To Raw Uri Value ====***"
        sscc96 = self._sscc96.encode(self._companyPrefix, self._extensionDigit,self._serialRef ,self._filter)
        print sscc96.toEPCRawUri()
        print ("***==== END  Test To EPC Tag Uri Value ====***" 
        print (""
    
    def test_GS1(self):
        print ("***==== Test To GS1 Value ====***"
        sscc96 = self._sscc96.encode(self._companyPrefix, self._extensionDigit,self._serialRef ,self._filter)
        print sscc96.toGS1()
        print ("***==== END  Test To GS1 Value ====***" 
        print (""
    
    def test_ToGS1WithAIInParens(self):
        print ("***==== Test GS1 With AI in Parens  ====***"
        sscc96 = self._sscc96.encode(self._companyPrefix, self._extensionDigit,self._serialRef ,self._filter)
        print sscc96.toGS1()
        print ("***==== END Test To GS1 With AI in Parens ====***" 
        print (""
            
    def test_ToGS1WithAIWithoutParens(self):
        print ("***==== Test GS1 With AI Without Parens  ====***"
        sscc96 = self._sscc96.encode(self._companyPrefix, self._extensionDigit,self._serialRef ,self._filter)
        print sscc96.toGS1(False)
        print ("***==== END Test To GS1 With AI Without Parens ====***" 
        print (""  
    
    def test_ToSSCC18(self):
        print ("***==== Test SSCC18  ====***"
        sscc96 = self._sscc96.encode(self._companyPrefix, self._extensionDigit,self._serialRef ,self._filter)
        print sscc96.toSSCC18()
        print ("***==== END To SSCC18 ====***" 
        print (""  
    
    def test_ChangeSerialNumber(self):
        print ("***==== Change Serial Number  ====***"
        sscc96 = self._sscc96.encode(self._companyPrefix, self._extensionDigit,self._serialRef ,self._filter)
        print ("Serial Number Was %s" % sscc96.getFieldValue("SerialReference")
        extDigit = sscc96.getFieldValue("SerialReference")[0:1]
        hex = sscc96.toHex()
        print ("Old Hex = %s" % hex
        partition = Partitions()
        pv = partition.getPartitionValue(len(str(self._companyPrefix)), "SSCC")
        serialLength = partition.getItemDigitLength(pv,"SSCC")
        newSerial=""
        while(len(newSerial)< int(serialLength-1)): 
            newSerial = newSerial + "1"
            
        sscc96.setSerialNumber(newSerial)
        hex = sscc96.toHex()
        print ("New Serial Number = %s" % sscc96.getFieldValue("SerialReference")
        print ("New Hex  = %s" % hex
        factory = EPCFactory()
        sscc96 = factory.parse(hex)
        self.assertEquals(str(sscc96.getFieldValue("SerialReference")),str(str(extDigit) + str(newSerial)).zfill(sscc96.getField("SerialReference").getDigitLength()))
        print ("***====END Change Serial Number  ====***"
    
    def test_ChangeFilter(self):
        print ("***==== Change Filter Number  ====***"
        sscc96 = self._sscc96.encode(self._companyPrefix, self._extensionDigit,self._serialRef ,self._filter)
        print ("Filter Number Was %s" % sscc96.getFieldValue("Filter")
        hex = sscc96.toHex()
        print ("Old Hex = %s" % hex
        if(self._filter < 1): 
            newFilter = self._filter + 1
        else:
            newFilter = self._filter - 1 
             
        sscc96.setFieldValue("Filter",newFilter)
        hex = sscc96.toHex()
        print ("New Filter Number = %s " % newFilter
        print ("New Hex = %s " % hex
        factory = EPCFactory()
        sscc96 = factory.parse(hex)
        self.assertEquals(int(sscc96.getFieldValue("Filter")),newFilter)
        print ("***====END Change Filter Number  ====***"
    
    def test_Formats(self):
        print ("***==== Test Formatting ====***"
        epc = self._sscc96.encode(self._companyPrefix, self._extensionDigit,self._serialRef ,self._filter)
        #Turn the tagpy number into a hex value and parse it through the factory
        hex = epc.toHex()
        factory = EPCFactory()
        sscc96 = factory.parse(hex)
        
        print ("=== Format to HEX ==="
        print sscc96.format("hex")
        print ("==========================="
        print ("=== Format to BINARY ==="
        print sscc96.format("binarY")
        print ("==========================="
        print ("=== Format to JSON ==="
        print sscc96.format("json")
        print ("==========================="
        print ("=== Format to RAW_URI ==="
        print sscc96.format("raw_uRI")
        print ("==========================="
        print ("=== Format to DICTIONARY ==="
        f = sscc96.format("DICTIONARY")
        for k, v in f.items():       
            print ("%s=%s\n" % (k, v)
        print ("==========================="
        print ("=== Format to gs1 ==="
        print sscc96.format("gs1")    
        print ("==========================="
        print ("***====END Test Formatting ====***"
        print (""
    
    
    def _checkFields(self,sscc96):
        
        partitions = Partitions()
        partitionValue = partitions.getPartitionValue(len(self._companyPrefix), "SSCC")
        
        self.assertEqual(sscc96.getFieldValue("Header"),"49")
        self.assertEqual(sscc96.getFieldValue("Filter"),str(self._filter))
        self.assertEqual(str(sscc96.getFieldValue("Partition")),str(partitionValue))
        self.assertEqual(sscc96.getFieldValue("CompanyPrefix"),str(self._companyPrefix))
        serialRef = self._serialRef.zfill(partitions.getItemDigitLength(partitionValue, "SSCC")-1)
        self.assertEqual(sscc96.getFieldValue("SerialReference"),"%s%s" % (self._extensionDigit,serialRef))
        self.assertEqual(int(sscc96.getFieldValue("Reserved")),int("0"))
        print ("Field Values are Valid"
        self._checkBitsAndHex(sscc96)
        
    def _checkBitsAndHex(self,epc):
    
        partitions = Partitions()
        partitionValue = partitions.getPartitionValue(len(self._companyPrefix), "SSCC")
        
        bits = epc.toBinary()
        hex = epc.toHex()
        headerValue = bits[epc.getField("Header").getOffset():epc.getField("Header").getBitLength()]
        self.assertEquals(int(headerValue,2),49)
        
        headerValue = hex[:2]
        self.assertEquals(int(headerValue,16),49)
        
        filterValue = bits[epc.getField("Filter").getOffset():int(epc.getField("Filter").getOffset()) + int(epc.getField("Filter").getBitLength())]
        self.assertEquals(int(filterValue,2),int(self._filter))
        hexBodyValue = hex[2:18]
        hexBodyBits = BitArray(hex=hexBodyValue).bin[2:]
        partitionValue = bits[epc.getField("Partition").getOffset():int(epc.getField("Partition").getOffset()) + int(epc.getField("Partition").getBitLength())]
        partitionValue = int(partitionValue,2)
        #Check the bits, contained in the hex, for the company prefix
        startPos = 6
        companyPrefixBits = hexBodyBits[startPos:startPos+epc.getField("CompanyPrefix").getBitLength()]
        companyPrefixValue = BitArray(bin=companyPrefixBits).uint 
        self.assertEquals(companyPrefixValue,int(self._companyPrefix))
        
        startPos = startPos + epc.getField("CompanyPrefix").getBitLength()
        serialReferenceBits = hexBodyBits[startPos:startPos+epc.getField("SerialReference").getBitLength()]
        serialReferenceValue = str(BitArray(bin=serialReferenceBits).uint)
        serialRef = self._serialRef.zfill(partitions.getItemDigitLength(partitionValue, "SSCC")-1)
        serialReferenceValue = serialReferenceValue.zfill(partitions.getItemDigitLength(partitionValue, "SSCC"))
        self.assertEquals(serialReferenceValue,"%s%s" % (self._extensionDigit,serialRef))
        print ("Bits and Hex are valid"
         
        
if __name__ == "__main__":
    unittest.main()              
        
        
        
            
        