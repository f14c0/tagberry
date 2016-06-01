import unittest
from gs1.GLN import GLN
class GLNTest(unittest.TestCase):
    def setUp(self):
        '''
        You can use one of these GLNs for test by setting the vars below (or another one that you have)
        41403700000203712441457
        (414)0370000020304(254)1457
        0370000020304
        (414)0370000210287(254)1234567890
        41403700002102872541234567890
        0370000210287
        '''
        self._gln = "(414)0370000027304(254)1457"
        self._cp = "0370000"
    
    def test_parse(self):
        print ("===========ENTER test_parse======================")
        
        gs1 = GLN(self._cp)
        gs1.parse(self._gln)
        print ("CompanyPrefix = %s" % gs1.getCompanyPrefix())
        print ("LocationReference = %s" % gs1.getLocationReference())
        print ("ExtensionNumber = %s" % gs1.getExtensionNumber())
        print ("CheckDigit = %s" % gs1.getCheckDigit())
        print ("AIs = %s" % gs1.getAppIdentifiers())
        print ("toGS1(True) With Parens = %s" % gs1.toGS1(True))
        print ("toGS1(False) Without Parens = %s" % gs1.toGS1(False))
        print ("toGLN() = %s" % gs1.toGLN())
        print ("===========END test_parse======================")
        print ("")
     
    def test_changeExtensionNumber(self):
        print ("===========ENTER test_changeExtensionNumber======================")
        gs1 = GLN(self._cp)
        gs1.parse(self._gln)
        
        print ("toGS1(True) = %s" % gs1.toGS1(True))
        print ("ExtensionNumber was %s" % gs1.getExtensionNumber())
        print ("Changing Extension Number.... 12 ")
        gs1.setExtensionNumber(12)
        
        
        print ("ExtensionNumber is now %s" % gs1.getExtensionNumber())
        print ("CompanyPrefix = %s" % gs1.getCompanyPrefix())
        print ("LocationReference = %s" % gs1.getLocationReference())
        print ("CheckDigit = %s" % gs1.getCheckDigit())
        print ("AIs = %s" % gs1.getAppIdentifiers())
        print ("toGS1(True) is now = %s" % gs1.toGS1(True))
        print ("toGS1(False) is now = %s" % gs1.toGS1(False))
        print ("toGLN() = %s" % gs1.toGLN())
        print ("===========END test_changeSerialNumber======================")
        print ("")
        
        
        
if __name__ == "__main__":
    unittest.main()  
    