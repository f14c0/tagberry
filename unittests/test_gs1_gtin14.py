import unittest
from gs1.GTIN import GTIN
from epc.EPCFactory import EPCFactory
from epc.SGTIN96 import SGTIN96
class GTINTest(unittest.TestCase):
    def setUp(self):
        '''
        You can use one of these GTINS for test by setting the vars below (or another one that you have)
        012035846810144421000000050656
        (01)10370000020306(21)1457
        50370000020298
        011037000002030621000000001457
        '''
        self._gtin = "(01)00354092476121(21)900000001065"
        self._cp = "0354092"
    
    def test_parse(self):
        print ("===========ENTER test_parse======================"
        
        gs1 = GTIN(self._cp)
        gs1.parse(self._gtin)
        print ("IndicatorDigit = %s" % gs1.getIndicatorDigit()
        print ("CompanyPrefix = %s" % gs1.getCompanyPrefix()
        print ("ItemReference = %s" % gs1.getItemReference()
        print ("SerialNumber = %s" % gs1.getSerialNumber()
        print ("AIs = %s" % gs1.getAppIdentifiers()
        print ("toGS1(True) With Parens = %s" % gs1.toGS1(True)
        print ("toGS1(False) Without Parens = %s" % gs1.toGS1(False)
        print ("toGTIN14() = %s" % gs1.toGTIN14()
        print ("===========END test_parse======================"
        print (""
     
    def test_changeSerialNumber(self):
        print ("===========ENTER test_changeSerialNumber======================"
        gs1 = GTIN(self._cp)
        gs1.parse(self._gtin)
        
        print ("toGS1(True) = %s" % gs1.toGS1(True)
        print ("SerialNumber was %s" % gs1.getSerialNumber()
        print ("Changing Serial Number.... 12 with a length of 5"
        gs1.setSerialNumber("12",5)
        
        self.assertFalse(len(gs1.getSerialNumber())!=5)
        print ("SerialNumber is now %s" % gs1.getSerialNumber()
        print ("IndicatorDigit = %s" % gs1.getIndicatorDigit()
        print ("CompanyPrefix = %s" % gs1.getCompanyPrefix()
        print ("ItemReference = %s" % gs1.getItemReference()
        print ("AIs = %s" % gs1.getAppIdentifiers()
        print ("toGS1(True) is now = %s" % gs1.toGS1(True)
        print ("toGS1(False) is now = %s" % gs1.toGS1(False)
        print ("toGTIN14() = %s" % gs1.toGTIN14()
        print ("===========END test_changeSerialNumber======================"
        print (""
    
    def test_toEPC(self):
        gs1 = GTIN(self._cp)
        gs1.parse(self._gtin)
        epc = SGTIN96().encode(gs1._companyPrefix, gs1.getIndicatorDigit(), gs1.getItemReference(), 2, gs1.getSerialNumber()) 
        return epc.toHex()
           
    def test_parse_shire(self):
        gtin = GTIN("0354092")
        gtin.parse("01003540924761212110001700490817011215101000")
        print gtin.toGTIN14()
        
if __name__ == "__main__":
    unittest.main()  