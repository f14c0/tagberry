import unittest
from gs1.GDTI import GDTI
class GDTITest(unittest.TestCase):
    def setUp(self):
        '''
        You can use one of these GTINS for test by setting the vars below (or another one that you have)
          25303700002103021457
         (253)03700002103021457
         03700002103021457
          AI = 253
          Company Prefix     = 0370000   
          DocumentType       = 21030
          Check Digit        = 2
          Serial             = 1457    
        '''
        self._gdti = "03700002103061457"
        self._cp = "0370000"
        self._documentType = "21030"
        self._serialNumber = "1457"
        
    
    def test_encode(self):
        print ("=============================Enter test_encode=========================")
        gdti = GDTI(self._cp)
        gdti.encode(self._documentType,self._serialNumber)
        print ("AIs = %s" % gdti.getAppIdentifiers())
        print ("CompanyPrefix = %s" % gdti.getCompanyPrefix())
        print ("DocumentType = %s" % gdti.getDocumentType())
        print ("Check Digit = %s" % gdti.getCheckDigit())
        print ("SerialNumber = %s" % gdti.getSerialNumber())
        print ("=============================END test_encode=========================")
        print ("")
    
    def test_parse(self):
        print ("=============================Enter test_parse=========================")
        gdti = GDTI(self._cp)
        gdti.parse(self._gdti)
        print ("AIs = %s" % gdti.getAppIdentifiers())
        print ("CompanyPrefix = %s" % gdti.getCompanyPrefix())
        print ("DocumentType = %s" % gdti.getDocumentType())
        print ("Check Digit = %s" % gdti.getCheckDigit())
        print ("SerialNumber = %s" % gdti.getSerialNumber())
        print ("=============================END test_parse=========================")
        print ("")