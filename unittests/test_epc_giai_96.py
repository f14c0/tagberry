import unittest
from epc.EPCFactory import EPCFactory
from epc.GIAI96 import GIAI96
from utils.Partitions import Partitions
from bitstring import BitArray    

class GIAI96Test(unittest.TestCase):
    def setUp(self):
        self._giai96 = GIAI96()
        self._companyPrefix = "02345678"
        self._itemRef = "12345678901"
        self._filter = 7
    
    def test_Encode(self):
        
        epc = self._giai96.encode(self._companyPrefix, None,self._itemRef ,self._filter, None)
        bits = epc.toBinary()
        self.assertEquals(len(bits),96)
        self._checkFields(epc)
        
    
    def test_ParseHex(self):
        
        #Turn the tagpy number into a hex value and parse it through the factory
        epc = self._giai96.encode(self._companyPrefix, None,self._itemRef ,self._filter, None)
        hex_val = epc.toHex()
        factory = EPCFactory()
        epc = factory.parse(hex_val)
        self._checkFields(epc)
        
    def test_FromHex(self):
        
        #Turn the tagpy number into a hex value and parse it through the factory
        epc = self._giai96.encode(self._companyPrefix, None,self._itemRef ,self._filter, None)
        hex_val = epc.toHex()
        epc = epc.fromHex(hex_val)
        self._checkFields(epc)
        
    def test_ParseBinary(self):
        
        epc = self._giai96.encode(self._companyPrefix, None,self._itemRef ,self._filter, None)
        bin = epc.toBinary()
        self.assertEquals(len(bin),96)
        factory = EPCFactory()
        #Take the binary value and parse it through the factory
        sgtin96 = factory.parse(bin)
        self._checkFields(epc)
             
    def test_ParseEPCUri(self):
        
        #TagURI=urn:tagpy:id:sgtin:0358468.202339.000395
        tagUri = "urn:tagpy:id:giai:%s.%s" % (str(self._companyPrefix),str(self._itemRef))
        factory = EPCFactory()
        #Take the URI value and parse it through the factory
        epc = factory.parse(tagUri)
        #Change the filter because the filter is not part filter the pure identity is not available
        self._filter = 0
        self._checkFields(epc)
        
    def test_ParseEPCTagUri(self):
        
        tagUri = "urn:tagpy:tag:giai-96:%s.%s.%s" % (str(self._filter),str(self._companyPrefix),str(self._itemRef))
        factory = EPCFactory()
        #Take the Tag URI value and parse it through the factory
        epc = factory.parse(tagUri)
        self._checkFields(epc)
        
    def test_ToEPCTagUri(self):
        
        epc = self._giai96.encode(self._companyPrefix, None,self._itemRef ,self._filter, None)
        
    
    def test_ToGS1(self):
        
        epc = self._giai96.encode(self._companyPrefix, None,self._itemRef ,self._filter, None)
        
    def test_ToGS1WithAIInParens(self):
        epc = self._giai96.encode(self._companyPrefix, None,self._itemRef ,self._filter, None)
        
    def test_ToGS1WithAIWithoutParens(self):
        
        epc = self._giai96.encode(self._companyPrefix, None,self._itemRef ,self._filter, None)
        
    def test_ChangeFilter(self):
        
        epc = self._giai96.encode(self._companyPrefix, None,self._itemRef ,self._filter, None)
        hex_val = epc.toHex()
        
        if(self._filter < 1): 
            self._filter = self._filter + 1
        else:
            self._filter = self._filter - 1 
             
        epc.setFieldValue("Filter",self._filter)
        hex_val = epc.toHex()
        factory = EPCFactory()
        epc = factory.parse(hex_val)
        self._checkFields(epc)
        self.assertEquals(int(epc.getFieldValue("Filter")), self._filter)
        
    
    def test_Formats(self):
        #Start with this GTIN-14 20358468023395
        epc = self._giai96.encode(self._companyPrefix, None,self._itemRef ,self._filter, None)
        #Turn the tagpy number into a hex_val value and parse it through the factory
        hex_val = epc.toHex()
        factory = EPCFactory()
        epc = factory.parse(hex_val)
        
        
        
        
    def _checkFields(self,epc):
    
        partitions = Partitions()
        partitionValue = partitions.getPartitionValue(len(self._companyPrefix), "GIAI")
        
        self.assertEqual(epc.getFieldValue("Header"),"52")
        self.assertEqual(epc.getFieldValue("Filter"),str(self._filter))
        self.assertEqual(str(epc.getFieldValue("Partition")),str(partitionValue))
        self.assertEqual(epc.getFieldValue("CompanyPrefix"),str(self._companyPrefix))
        self.assertEqual(epc.getFieldValue("IndividualAssetReference"),str(self._itemRef))
        
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
        
        return True
        
        
            
if __name__ == "__main__":
    unittest.main()       