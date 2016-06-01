import unittest
from gs1.SSCC import SSCC
class SSCCTest(unittest.TestCase):
    def setUp(self):
        '''
        You can use one of these SSCCs for test by setting the vars below (or another one that you have)
        00006141411234567890
        (00)006141411234567890
        006141411234567890
        '''
        self._sscc = "(00)006141411234567890"
        self._cp = "0614141"
    
    def test_parse(self):
        print("===========ENTER test_parse======================")
        
        gs1 = SSCC(self._cp)
        gs1.parse(self._sscc)
        print("ExtensionDigit = %s" % gs1.getExtensionDigit())
        print("CompanyPrefix = %s" % gs1.getCompanyPrefix())
        print("SerialNumber = %s" % gs1.getSerialNumber())
        print("AIs = %s" % gs1.getAppIdentifiers())
        print("toGS1(True) With Parens = %s" % gs1.toGS1(True))
        print("toGS1(False) Without Parens = %s" % gs1.toGS1(False))
        print("toSSCC18() = %s" % gs1.toSSCC18())
        print("===========END test_parse======================")
        print("")
            
    def test_generate(self):
        self._cp = "030046"
        
        serials = [1000000000,1000000001,1000000002,1000000003,1000000004,1000000005,1000000006,]
        for serial in serials:
            gs1 = SSCC(self._cp)
            gs1.encode(0, serial)
            print("00%s") % (gs1.toSSCC18(),)
        
        
if __name__ == "__main__":
    unittest.main() 