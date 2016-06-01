import unittest
from utils.CharacterSet import CharacterSet


class CheckFields(unittest.TestCase):
    """
    Test special field values.
    """
    def setUp(self):
        pass
    def test_GetCharByHex(self):
        vhex = 0x21
        cs = CharacterSet();
        val = cs.getCharacterByHex(vhex)
        self.assertEquals(val,"!")
    
    def test_GetCharByUriForm(self):
        uri = "%3F"
        cs = CharacterSet();
        val = cs.getCharacterByUriForm(uri)
        self.assertEquals(val,"?")
    
    def test_GetHexFromUriForm(self):
        uri = "%3F"
        cs = CharacterSet();
        val = cs.getHexByUriForm(uri)
        self.assertEquals(val,0x3F)
    
    def test_GetHexFromChar(self):
        char = "?"
        cs = CharacterSet();
        val = cs.getHexByCharacter(char)
        self.assertEquals(val,0x3F) 
        
if __name__ == "__main__":
    unittest.main()    