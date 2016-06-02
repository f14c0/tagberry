import unittest
from bitstring import BitArray, BitStream
from epc.EPCFactory import EPCFactory
from epc.SGTIN96 import SGTIN96
from utils.Partitions import Partitions  


class SGTIN96Test(unittest.TestCase):
    
    def setUp(self):
    
        self._sgtin96 = SGTIN96()
        self._companyPrefix = "035846802"
        self._itemRef = "339"
        self._indicatorDigit = 1
        self._filter = 3
        self._serialNumber = 395
    
    def test_encode(self):
        """
        Test that the SGTIN can be encoded using the encode method. 
        """
        
        sgtin96 = self._sgtin96.encode(companyPrefix=self._companyPrefix, 
                                       indicatorDigit=self._indicatorDigit,
                                       itemReference=self._itemRef,
                                       filter=self._filter, 
                                       serialNumber=self._serialNumber)
        
        
        #Check Field Values
        partitions = Partitions()
        partitionValue = partitions.getPartitionValue(len(self._companyPrefix), "SGTIN")
        
        self.assertEqual(sgtin96.getFieldValue("Header"), "48")
        self.assertEqual(sgtin96.getFieldValue("Filter"), str(self._filter))
        self.assertEqual(str(sgtin96.getFieldValue("Partition")), str(partitionValue))
        self.assertEqual(sgtin96.getFieldValue("CompanyPrefix"), str(self._companyPrefix))
        self.assertEqual(sgtin96.getFieldValue("ItemReference"), str(self._indicatorDigit) + str(self._itemRef))
        self.assertEqual(int(sgtin96.getFieldValue("SerialNumber")), int(self._serialNumber))
        
       
    def test_convert_from_hex(self):
        """
        Test to ensure SGTIN96 can convert from a hex value to an SGTIN96 Instance
        """
        #Create the SGTIN-96
        sgtin96 = self._sgtin96.encode(companyPrefix=self._companyPrefix, 
                                       indicatorDigit=self._indicatorDigit,
                                       itemReference=self._itemRef,
                                       filter=self._filter, 
                                       serialNumber=self._serialNumber)
        #Convert
        hex_val = sgtin96.toHex()
        #Parse Hex through Factory
        factory = EPCFactory()
        sgtin96 = factory.parse(hex_val)
        
        self.assertIsInstance(sgtin96, SGTIN96, "EPCFactory did not return SGTIN96 instances")
        
        #Check Fields
        partitions = Partitions()
        partitionValue = partitions.getPartitionValue(len(self._companyPrefix), "SGTIN")
        
        self.assertEqual(sgtin96.getFieldValue("Header"), "48")
        self.assertEqual(sgtin96.getFieldValue("Filter"), str(self._filter))
        self.assertEqual(str(sgtin96.getFieldValue("Partition")), str(partitionValue))
        self.assertEqual(sgtin96.getFieldValue("CompanyPrefix"), str(self._companyPrefix))
        self.assertEqual(sgtin96.getFieldValue("ItemReference"), str(self._indicatorDigit) + str(self._itemRef))
        self.assertEqual(int(sgtin96.getFieldValue("SerialNumber")), int(self._serialNumber))
        
    def test_from_hex(self):
        
        
        sgtin96 = self._sgtin96.encode(companyPrefix=self._companyPrefix, 
                                       indicatorDigit=self._indicatorDigit,
                                       itemReference=self._itemRef,
                                       filter=self._filter, 
                                       serialNumber=self._serialNumber)
        
        
        #Check Fields
        partitions = Partitions()
        partitionValue = partitions.getPartitionValue(len(self._companyPrefix), "SGTIN")
        
        self.assertEqual(sgtin96.getFieldValue("Header"), "48")
        self.assertEqual(sgtin96.getFieldValue("Filter"), str(self._filter))
        self.assertEqual(str(sgtin96.getFieldValue("Partition")), str(partitionValue))
        self.assertEqual(sgtin96.getFieldValue("CompanyPrefix"), str(self._companyPrefix))
        self.assertEqual(sgtin96.getFieldValue("ItemReference"), str(self._indicatorDigit) + str(self._itemRef))
        self.assertEqual(int(sgtin96.getFieldValue("SerialNumber")), int(self._serialNumber))
        
       
    def test_ParseBinary(self):
        
        sgtin96 = self._sgtin96.encode(companyPrefix=self._companyPrefix, 
                                       indicatorDigit=self._indicatorDigit,
                                       itemReference=self._itemRef,
                                       filter=self._filter, 
                                       serialNumber=self._serialNumber)
        bin = sgtin96.toBinary()
        self.assertEquals(len(bin), 96)
        factory = EPCFactory()
        #Take the binary value and parse it through the factory
        sgtin96 = factory.parse(bin)
        self._checkFields(sgtin96)
    
        
        self.assertEqual(sgtin96.getFieldValue("Header"), "48")
        self.assertEqual(sgtin96.getFieldValue("Filter"), str(self._filter))
        self.assertEqual(str(sgtin96.getFieldValue("Partition")), str(partitionValue))
        self.assertEqual(sgtin96.getFieldValue("CompanyPrefix"), str(self._companyPrefix))
        self.assertEqual(sgtin96.getFieldValue("ItemReference"), str(self._indicatorDigit) + str(self._itemRef))
        self.assertEqual(int(sgtin96.getFieldValue("SerialNumber")), int(self._serialNumber))
        
    def test_parse_epc_uri(self):
        
        #TagURI=urn:epc:id:sgtin:0358468.202339.000395
        epcUri = "urn:epc:id:sgtin:%s.%s.%s" % (str(self._companyPrefix), str(self._indicatorDigit) + str(self._itemRef),str(self._serialNumber))
        factory = EPCFactory()
        #Take the URI value and parse it through the factory
        sgtin96 = factory.parse(epcUri)
        
        #Change the filter because the filter is not part of the pure identity is not available
        self._filter = 0
        
        #Check Fields
        partitions = Partitions()
        partitionValue = partitions.getPartitionValue(len(self._companyPrefix), "SGTIN")
        
        self.assertEqual(sgtin96.getFieldValue("Header"), "48")
        self.assertEqual(sgtin96.getFieldValue("Filter"), str(self._filter))
        self.assertEqual(str(sgtin96.getFieldValue("Partition")), str(partitionValue))
        self.assertEqual(sgtin96.getFieldValue("CompanyPrefix"), str(self._companyPrefix))
        self.assertEqual(sgtin96.getFieldValue("ItemReference"), str(self._indicatorDigit) + str(self._itemRef))
        self.assertEqual(int(sgtin96.getFieldValue("SerialNumber")), int(self._serialNumber))
        
    def test_ParseEPCTagUri(self):
        
        tagUri = "urn:epc:tag:sgtin-96:%s.%s.%s.%s" % (str(self._filter),str(self._companyPrefix), str(self._indicatorDigit) + str(self._itemRef),str(self._serialNumber))
        factory = EPCFactory()
        #Take the Tag URI value and parse it through the factory
        sgtin96 = factory.parse(tagUri)
        #Check Fields
        partitions = Partitions()
        partitionValue = partitions.getPartitionValue(len(self._companyPrefix), "SGTIN")
        
        self.assertEqual(sgtin96.getFieldValue("Header"), "48")
        self.assertEqual(sgtin96.getFieldValue("Filter"), str(self._filter))
        self.assertEqual(str(sgtin96.getFieldValue("Partition")), str(partitionValue))
        self.assertEqual(sgtin96.getFieldValue("CompanyPrefix"), str(self._companyPrefix))
        self.assertEqual(sgtin96.getFieldValue("ItemReference"), str(self._indicatorDigit) + str(self._itemRef))
        self.assertEqual(int(sgtin96.getFieldValue("SerialNumber")), int(self._serialNumber))
        
    def test_ToEPCTagUri(self):
        sgtin96 = self._sgtin96.encode(companyPrefix=self._companyPrefix, 
                                       indicatorDigit=self._indicatorDigit,
                                       itemReference=self._itemRef,
                                       filter=self._filter, 
                                       serialNumber=self._serialNumber)
        
        
    def test_ToGS1(self):
        
        sgtin96 = self._sgtin96.encode(companyPrefix=self._companyPrefix, 
                                       indicatorDigit=self._indicatorDigit,
                                       itemReference=self._itemRef,
                                       filter=self._filter, 
                                       serialNumber=self._serialNumber)
        
    def test_ToGS1WithAIInParens(self):
        
        sgtin96 = self._sgtin96.encode(companyPrefix=self._companyPrefix, 
                                       indicatorDigit=self._indicatorDigit,
                                       itemReference=self._itemRef,
                                       filter=self._filter, 
                                       serialNumber=self._serialNumber)
        gs1 = sgtin96.toGS1(True)
               
    def test_ToGS1WithAIWithoutParens(self):
        
        sgtin96 =self._sgtin96.encode(companyPrefix=self._companyPrefix, 
                                       indicatorDigit=self._indicatorDigit,
                                       itemReference=self._itemRef,
                                       filter=self._filter, 
                                       serialNumber=self._serialNumber)
        gs1 = sgtin96.toGS1(False)
         
        
        
    def test_change_serial_number(self):
        """
        Test the ability to change the serial number
        """
        
        sgtin96 = self._sgtin96.encode(companyPrefix=self._companyPrefix, 
                                       indicatorDigit=self._indicatorDigit,
                                       itemReference=self._itemRef,
                                       filter=self._filter, 
                                       serialNumber=self._serialNumber)
        
        hex_val = sgtin96.toHex()
        
        newSerial = 12345678901
        sgtin96.serialnumber = newSerial
        new_hex_val = sgtin96.toHex()
        
        factory = EPCFactory()
        sgtin96 = factory.parse(new_hex_val)
        
        self.assertIsInstance(sgtin96, SGTIN96, "EPCFactory did not return an SGTIN96 instance.")
        self.assertEquals(int(sgtin96.getFieldValue("SerialNumber")), newSerial)
        self.assertNotEqual(hex_val, new_hex_val, "The Serial Number was not changed")
        
    
    def test_ChangeFilter(self):
        
        sgtin96 = self._sgtin96.encode(companyPrefix=self._companyPrefix, 
                                       indicatorDigit=self._indicatorDigit,
                                       itemReference=self._itemRef,
                                       filter=self._filter, 
                                       serialNumber=self._serialNumber)
        
        hex_val = sgtin96.toHex()
        
        if(self._filter < 1): 
            newFilter = self._filter + 1
        else:
            newFilter = self._filter - 1 
             
        sgtin96.setFieldValue("Filter",newFilter)
        new_hex_val = sgtin96.toHex()
        self.assertNotEqual(new_hex_val, hex_val, "Filter value did not change")
        
        factory = EPCFactory()
        sgtin96 = factory.parse(new_hex_val)
        self.assertIsInstance(sgtin96, SGTIN96, "parseFromHex failed to return the correct EPC Encoding")
        self.assertEquals(int(sgtin96.getFieldValue("Filter")), newFilter)
        
    
    def test_Formats(self):
        #Start with this GTIN-14 20358468023395
        sgtin96 = self._sgtin96.encode(companyPrefix=self._companyPrefix, 
                                       indicatorDigit=self._indicatorDigit,
                                       itemReference=self._itemRef,
                                       filter=self._filter, 
                                       serialNumber=self._serialNumber)
        #Turn the tagpy number into a hex value and parse it through the factory
        hex_val = sgtin96.toHex()
        factory = EPCFactory()
        sgtin96 = factory.parse(hex_val)
    
        hex_val = sgtin96.format("hex")
        binary = sgtin96.format("binarY")
        json = sgtin96.format("json")
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
        
    def _checkBitsAndHex(self, epc):
    
        bits = epc.toBinary()
        hex_val = epc.toHex()
        headerValue = bits[0:8]
        self.assertEquals(int(headerValue, 2), 48)
        
        headerValue = hex_val[:2]
        self.assertEquals(int(headerValue, 16), 48)
        
        filterValue = bits[epc.getField("Filter").getOffset():int(epc.getField("Filter").getOffset()) + int(epc.getField("Filter").getBitLength())]
        self.assertEquals(int(filterValue,2),int(self._filter))
        hexBodyValue = hex_val[2:18]
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