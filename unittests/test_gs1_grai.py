import unittest
from gs1.GRAI import GRAI
class GRAITest(unittest.TestCase):
    def setUp(self):
        '''
        You can use one of these GRAIs for test by setting the vars below (or another one that you have)
        (8003)003700000203061457
        003700000203061457
        '''
        self._grai = "(8003)003700000203061457"
        self._cp = "0370000"
    
    def test_parse(self):
        print ("===========ENTER test_parse======================")
        
        gs1 = GRAI(self._cp)
        gs1.parse(self._grai)
        print ("CompanyPrefix = %s" % gs1.getCompanyPrefix())
        print ("AssetType = %s" % gs1.getAssetType())
        print ("SerialNumber = %s" % gs1.getSerialNumber())
        print ("AIs = %s" % gs1.getAppIdentifiers())
        print ("CheckDigit = %s" % gs1.getCheckDigit())
        print ("toGS1(True) With Parens = %s" % gs1.toGS1(True))
        print ("toGS1(False) Without Parens = %s" % gs1.toGS1(False))
        print ("toGRAI() = %s" % gs1.toGRAI())
        print ("===========END test_parse======================")
        print ("")
     
    def test_changeSerialNumber(self):
        print ("===========ENTER test_changeSerialNumber======================")
        gs1 = GRAI(self._cp)
        gs1.parse(self._grai)
        
        print ("toGS1(True) = %s" % gs1.toGS1(True))
        print ("SerialNumber was %s" % gs1.getSerialNumber())
        print ("Changing Serial Number.... 12")
        gs1.setSerialNumber("12")
        print ("CompanyPrefix = %s" % gs1.getCompanyPrefix())
        print ("AssetType = %s" % gs1.getAssetType())
        print ("NEW SerialNumber = %s" % gs1.getSerialNumber())
        print ("CheckDigit = %s" % gs1.getCheckDigit())
        print ("AIs = %s" % gs1.getAppIdentifiers())
        print ("toGS1(True) With Parens = %s" % gs1.toGS1(True))
        print ("toGS1(False) Without Parens = %s" % gs1.toGS1(False))
        print ("toGRAI() = %s" % gs1.toGRAI())
        print ("===========END test_changeSerialNumber======================")
        print ("")
        
        
        
if __name__ == "__main__":
    unittest.main()  