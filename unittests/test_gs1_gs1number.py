import unittest

from gs1.GS1Number import GS1Number

class GS1NumberTest(unittest.TestCase):
    '''
    Unit Tests for the base class GS1Number 
    '''
    def broken_function(self):
        '''
        Used for testing assertRaises
        '''
        raise Exception('Did not raise expected exception')
        
    def setUp(self):
        pass 
    
    def test_create_gtin(self):
        '''
        Test the creation of the GTIN Abstract class
        '''
        gs1 = GS1Number()
        self.assertIsInstance(gs1, GS1Number, "GS1Number Was not instantiated correctly")
        self.assertEqual(gs1.company_prefix, None, "The company prefix returned an unexpected value")
    
    def test_set_get_serial_number(self):
        '''
        Test the assignment and retrieval of a serial number
        '''
        gs1 = GS1Number()
        gs1.serial_number = 123456
        self.assertEqual(gs1.serial_number, 123456, "The serial number was not processed correctly")
    
    def test_get_content_type(self):
        '''
        Test the content_type value.
        '''
        gs1 = GS1Number()
        self.assertEqual(gs1.encoding_type, None, "The encoding type was not set correctly. The value should be none")
    
    def test_get_check_digit(self):
        '''
        Tests the check digit value on the GS1 Number. The value should be None here.
        '''
        gs1 = GS1Number()
        self.assertEqual(gs1.check_digit, None, "The check digit was invalid. Should be None")
    
    def test_parse(self):
        '''
        Test the abstract parse method to ensure it raises a NotImplementedError.
        '''
        gs1 = GS1Number()
         
        with self.assertRaises(NotImplementedError) as cm:
            gs1.parse("")
        exception_raised = cm.exception 
        self.assertIsInstance(exception_raised, NotImplementedError, "Incorrect exception raised from GS1Number.parse")
    
    def test_is_valid(self):
        '''
        Test the abstract is_valid method to ensure it raises a NotImplementedError.
        '''
        gs1 = GS1Number()
         
        with self.assertRaises(NotImplementedError) as cm:
            gs1.is_valid("")
        exception_raised = cm.exception 
        self.assertIsInstance(exception_raised, NotImplementedError, "Incorrect exception raised from GS1Number.is_valid")
            
    def test_to_epc(self):
        '''
        Test the abstract to_epc method to ensure it raises a NotImplementedError when not implemented.
        '''
        gs1 = GS1Number()
         
        with self.assertRaises(NotImplementedError) as cm:
            gs1.to_epc()
        exception_raised = cm.exception 
        self.assertIsInstance(exception_raised, NotImplementedError, "Incorrect exception raised from GS1Number.test_to_epc")
    
    def test_get_app_identifiers(self):
        '''
        Test the abstract get_app_identifiers method to ensure it raises a NotImplementedError when not implemented.
        '''
        gs1 = GS1Number()
         
        with self.assertRaises(NotImplementedError) as cm:
            gs1.get_app_identifiers()
        exception_raised = cm.exception 
        self.assertIsInstance(exception_raised, NotImplementedError, "Incorrect exception raised from GS1Number.test_get_app_identifiers")
        
    def test_to_base_number(self):
        '''
        Test the abstract to_base_number method to ensure it raises a NotImplementedError when not implemented.
        '''
        gs1 = GS1Number()
         
        with self.assertRaises(NotImplementedError) as cm:
            gs1.to_base_number()
        exception_raised = cm.exception 
        self.assertIsInstance(exception_raised, NotImplementedError, "Incorrect exception raised from GS1Number.to_base_number")
    
    def test_calculate_check_digit(self):
        '''
        Tests the check digit calculation
        '''
        data = "1234567890123"
        gs1 = GS1Number()
        check_digit = gs1.calculate_check_digit(data)
        self.assertEqual(check_digit, 1, "The Check digit should have been 1. Instead the check digit was %s" % check_digit)
        
        data = "4900012309874"
        check_digit = gs1.calculate_check_digit(data)
        self.assertEqual(check_digit, 7, "The Check digit should have been 7. Instead the check digit was %s" % check_digit)
        
        
if __name__ == '__main__':
    unittest.main()