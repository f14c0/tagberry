import unittest
from bitstring import BitArray, BitStream
from epc.EPCFactory import EPCFactory
from epc.SGTIN96 import SGTIN96
from utils.Partitions import Partitions  


class SGTIN96Test(unittest.TestCase):
    
    def setUp(self):
    #Change these values to test different scenarios
    #gs1 = 20358468023395
    #0120358468023395210000000003931734022810DF001122
        self._sgtin96 = SGTIN96()
        self._companyPrefix = "035846802"
        self._itemRef = "339"
        self._indicatorDigit = 0
        self._filter = 7
        self._serialNumber = 395
    
    def test_Encode(self):
        print ("==== Test Encode from Hex Value ====")
        #Start with this GTIN-14 20358468023395
        epc_num = self._sgtin96.encode(self._companyPrefix, self._indicatorDigit,self._itemRef ,self._filter, self._serialNumber)
        bits = epc_num.toBinary()
        self.assertEquals(len(bits),96)
        self._checkFields(epc)
        print (epc_num.toHex())
        print ("====END Test Decoding from Hex Value ====")
        print ("")
    
    def test_ParseHex(self):
        print ("==== Test Parse from Hex Value (Factory) ====")
        #Turn the epc number into a hex value and parse it through the factory
        sgtin96 = self._sgtin96.encode(self._companyPrefix, self._indicatorDigit,self._itemRef ,self._filter, self._serialNumber)
        hex = sgtin96.toHex()
        factory = EPCFactory()
        sgtin96 = factory.parse(hex)
        self._checkFields(sgtin96)
        print (sgtin96.toHex())
        print (sgtin96.toBinary())
        print ("====END Test Parse from Hex Value (Factory) ====")
        print ("")
        
    def test_FromHex(self):
        print ("==== Test Decoding from Hex Value ====")
        #Turn the tagpy number into a hex value and parse it through the factory
        epc_num = self._sgtin96.encode(self._companyPrefix, self._indicatorDigit,self._itemRef ,self._filter, self._serialNumber)
        hex = epc_num.toHex()
        epc = epc_num.fromHex(hex)
        self._checkFields(epc)
        print (epc_num.toHex())
        print (epc_num.toBinary())
        print ("====END Test Decoding from Hex Value ====")
        print ("")    
       
    def test_ParseBinary(self):
        
        sgtin96 = self._sgtin96.encode(self._companyPrefix, self._indicatorDigit,self._itemRef ,self._filter, self._serialNumber)
        bin = sgtin96.toBinary()
        self.assertEquals(len(bin),96)
        factory = EPCFactory()
        #Take the binary value and parse it through the factory
        sgtin96 = factory.parse(bin)
        self._checkFields(sgtin96)
        
    def test_ParseRawUri(self):
        
        sgtin96 = self._sgtin96.encode(self._companyPrefix, self._indicatorDigit,self._itemRef ,self._filter, self._serialNumber)
        rawUri = sgtin96.toEPCRawUri()
        factory = EPCFactory()
        #Take the Raw URI value and parse it through the factory
        sgtin96 = factory.parse(rawUri)
        self._checkFields(sgtin96)
        
    def test_ParseEPCUri(self):
        
        #TagURI=urn:tagpy:id:sgtin:0358468.202339.000395
        tagUri = "urn:tagpy:id:sgtin:%s.%s.%s" % (str(self._companyPrefix), str(self._indicatorDigit) + str(self._itemRef),str(self._serialNumber))
        factory = EPCFactory()
        #Take the Raw URI value and parse it through the factory
        sgtin96 = factory.parse(tagUri)
        #Change the filter because the filter is not part filter the pure identity is not available
        self._filter = 0
        self._checkFields(sgtin96)
        
    def test_ParseEPCTagUri(self):
        
        tagUri = "urn:tagpy:tag:sgtin-96:%s.%s.%s.%s" % (str(self._filter),str(self._companyPrefix), str(self._indicatorDigit) + str(self._itemRef),str(self._serialNumber))
        factory = EPCFactory()
        #Take the Tag URI value and parse it through the factory
        sgtin96 = factory.parse(tagUri)
        self._checkFields(sgtin96)
        
    def test_ToEPCTagUri(self):
        sgtin96 = self._sgtin96.encode(self._companyPrefix, self._indicatorDigit,self._itemRef ,self._filter, self._serialNumber)
        
    def test_ToRawUri(self):
        sgtin96 = self._sgtin96.encode(self._companyPrefix, self._indicatorDigit,self._itemRef ,self._filter, self._serialNumber)
        
    def test_ToGS1(self):
        
        sgtin96 = self._sgtin96.encode(self._companyPrefix, self._indicatorDigit,self._itemRef ,self._filter, self._serialNumber)
        
    def test_ToGS1WithAIInParens(self):
        
        sgtin96 = self._sgtin96.encode(self._companyPrefix, self._indicatorDigit,self._itemRef ,self._filter, self._serialNumber)
        gs1 = sgtin96.toGS1(True)
               
    def test_ToGS1WithAIWithoutParens(self):
        
        sgtin96 = self._sgtin96.encode(self._companyPrefix, self._indicatorDigit,self._itemRef ,self._filter, self._serialNumber)
        gs1 = sgtin96.toGS1(False)
         
        
        
    def test_ChangeSerialNumber(self):
        sgtin96 = self._sgtin96.encode(self._companyPrefix, self._indicatorDigit,self._itemRef ,self._filter, self._serialNumber)
        
        hex_val = sgtin96.toHex()
        newSerial = 12345678901
        sgtin96.setSerialNumber(newSerial)
        hex_val = sgtin96.toHex()
        factory = EPCFactory()
        sgtin96 = factory.parse(hex)
        self.assertEquals(int(sgtin96.getFieldValue("SerialNumber")), newSerial)
        
    
    def test_ChangeFilter(self):
        
        sgtin96 = self._sgtin96.encode(self._companyPrefix, self._indicatorDigit,self._itemRef ,self._filter, self._serialNumber)
        
        hex_val = sgtin96.toHex()
        
        if(self._filter < 1): 
            newFilter = self._filter + 1
        else:
            newFilter = self._filter - 1 
             
        sgtin96.setFieldValue("Filter",newFilter)
        hex_val = sgtin96.toHex()
        
        factory = EPCFactory()
        sgtin96 = factory.parse(hex)
        self.assertEquals(int(sgtin96.getFieldValue("Filter")),newFilter)
        
    
    def test_Formats(self):
        #Start with this GTIN-14 20358468023395
        sgtin96 = self._sgtin96.encode(self._companyPrefix, self._indicatorDigit,self._itemRef ,self._filter, self._serialNumber)
        #Turn the tagpy number into a hex value and parse it through the factory
        hex_val = sgtin96.toHex()
        factory = EPCFactory()
        sgtin96 = factory.parse(hex)
    
        hex_val = sgtin96.format("hex")
        binary = sgtin96.format("binarY")
        json = sgtin96.format("json")
        raw_uri = sgtin96.format("raw_uRI")
        f = sgtin96.format("DICTIONARY")
        gs1 = sgtin96.format("gs1")    
        
                
    def _checkFields(self,sgtin96):
        
        partitions = Partitions()
        partitionValue = partitions.getPartitionValue(len(self._companyPrefix), "SGTIN")
        
        self.assertEqual(sgtin96.getFieldValue("Header"),"48")
        self.assertEqual(sgtin96.getFieldValue("Filter"),str(self._filter))
        self.assertEqual(str(sgtin96.getFieldValue("Partition")),str(partitionValue))
        self.assertEqual(sgtin96.getFieldValue("CompanyPrefix"),str(self._companyPrefix))
        self.assertEqual(sgtin96.getFieldValue("ItemReference"),str(self._indicatorDigit) + str(self._itemRef))
        self.assertEqual(int(sgtin96.getFieldValue("SerialNumber")),int(self._serialNumber))
        
        self._checkBitsAndHex(sgtin96)     
        
    def _checkBitsAndHex(self,epc):
    
        bits = epc.toBinary()
        hex = epc.toHex()
        headerValue = bits[epc.getField("Header").getOffset():epc.getField("Header").getBitLength()]
        self.assertEquals(int(headerValue,2),48)
        
        headerValue = hex[:2]
        self.assertEquals(int(headerValue,16),48)
        
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
        itemReferenceBits = hexBodyBits[startPos:startPos+epc.getField("ItemReference").getBitLength()]
        
        
        itemReferenceValue = str(int(itemReferenceBits,2)).zfill(epc.getField("ItemReference").getDigitLength())
        self.assertEquals(str(itemReferenceValue),str(self._indicatorDigit) + str(self._itemRef))
           
        
        
            
if __name__ == "__main__":
    unittest.main()        