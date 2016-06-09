import unittest
from gs1.GTIN import GTIN

class GTINTest(unittest.TestCase):
    '''
    Unit Tests for a GTIN
    '''    
    def setUp(self):
        pass 
    
    def test_create_gtin(self):
        '''
        Test the creation of the GTIN Abstract class
        '''
        gtin = GTIN()
        self.assertIsInstance(gtin, GTIN, "GTIN Was not instantiated correctly")
        self.assertEqual(gtin.company_prefix, None, "The company prefix returned an unexpected value")
    
    def test_check_digit(self):    