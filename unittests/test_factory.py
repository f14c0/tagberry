import unittest
from factories.EncodingFactory import EncodingFactory
from gs1.GS1Factory import GS1Factory
from epc.EPCFactory import EPCFactory
from gs1.GS1Number import GS1Number
"""
http://chucksailer.com/tagpy/get/50370000020298/GS1/1/
http://chucksailer.com/tagpy/get/301824221314CB4000000001/GS1/1/
http://chucksailer.com/tagpy/get/Product1/GS1/1/
http://chucksailer.com/tagpy/get/Product1/EPC/1/
http://chucksailer.com/tagpy/get/301824221314CB4000000001/EPC/1/ 
http://chucksailer.com/tagpy/get/50370000020298/EPC/1/
"""
  
class FactoryTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_createGS1Number(self):
        print('=====================Entering createGS1 Number Test ==============================')
        ef = EncodingFactory()
        print ("Checking Abstract Factory on GS1")
        gs1Number = ef.parse("012035846810144421000000050656","2035846")
        print("GS1 = %s" % gs1Number)
        self.assertTrue(isinstance(gs1Number,GS1Number))
        gs1Number = ef.parse("301824221314CB4000000001")
        self.assertFalse(isinstance(gs1Number,GS1Number))
        print("Pass")
        print("=====================END returnGS1Factory Test ==============================")
        print("")    
        
        
    def test_createEPCFactory(self):
        print("=====================Entering create EPC Factory Test ==============================")
        ef = EncodingFactory()
        print("Checking Abstract Factory on EPC")
        factory = ef.create("EPC")
        self.assertTrue(isinstance(factory,EPCFactory))
        factory = ef.create("Gs1")
        self.assertFalse(isinstance(factory,EPCFactory))
        print("Pass")
        print("=====================END create EPC Factory Test ==============================")
        print("")    
    
    def test_createGS1Factory(self):
        print("=====================Entering create EPC Factory Test ==============================")
        ef = EncodingFactory()
        print("Checking Abstract Factory on GS1")
        factory = ef.create("GS1")
        self.assertTrue(isinstance(factory,GS1Factory))
        factory = ef.create("EPC")
        self.assertFalse(isinstance(factory,GS1Factory))
        print("Pass")
        print("=====================END create EPC Factory Test ==============================")
        print("")    
            
if __name__ == "__main__":
    unittest.main()