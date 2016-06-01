import unittest
from epc.GDTI113 import GDTI113
from utils.Partitions import Partitions  
from bitstring import BitArray

class GDTI113Test(unittest.TestCase):
    def setUp(self):
    #Change these values to test different scenarios
        self._gdti113 = GDTI113()
        self._companyPrefix = "012345678"
        self._documentType = "349"
        self._filter = 7
        self._serialNumber = 395
    
    def test_Encode(self):
        print("==== Test Encode from Hex Value ====")
        epc = self._gdti113.encode(self._companyPrefix, None,self._documentType ,self._filter, self._serialNumber)
        bits = epc.toBinary()
        self.assertEquals(len(bits),113)
        self._checkFields(epc)
        print(epc.toHex())
        print("====END Test Decoding from Hex Value ====")
        print("")
    
    def _checkFields(self,epc):
        
        partitions = Partitions()
        partitionValue = partitions.getPartitionValue(len(self._companyPrefix), "GDTI")
        
        self.assertEqual(epc.getFieldValue("Header"),"58")
        self.assertEqual(epc.getFieldValue("Filter"),str(self._filter))
        self.assertEqual(str(epc.getFieldValue("Partition")),str(partitionValue))
        self.assertEqual(epc.getFieldValue("CompanyPrefix"),str(self._companyPrefix))
        self.assertEqual(epc.getFieldValue("DocumentType"),str(self._documentType))
        self.assertEqual(int(epc.getSerialNumber()),int(self._serialNumber))
        print("Field Values are Valid")
        self._checkBitsAndHex(epc)     
        
    def _checkBitsAndHex(self,epc):
    
        bits = epc.toBinary()
        hex = epc.toHex()
        headerValue = bits[epc.getField("Header").getOffset():epc.getField("Header").getBitLength()]
        self.assertEquals(int(headerValue,2),58)
        
        headerValue = hex[:2]
        self.assertEquals(int(headerValue,16),58)
        
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
        print("Bits and Hex are valid")   
        
        
            
if __name__ == "__main__":
    unittest.main()