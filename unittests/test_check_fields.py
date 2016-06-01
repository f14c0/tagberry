import unittest
from schema.Field import Field
from schema.FieldDictionary import FieldDictionary

class CheckFields(unittest.TestCase):
	"""
	Run tests to check the fields dictionary
	"""
	def setUp(self):
		self.field = Field("SerialNumber", offset=3, bitLength=8, ordinal=1, fieldValue=6, digitLength=1)	
		self.field2 = Field("CompanyPrefix", offset=0, bitLength=24, ordinal=2, fieldValue=49000, digitLength=6)
		
	def test_Name(self):
		self.assertEquals(self.field.getFieldName(),"SerialNumber")
		self.assertEquals(self.field2.getFieldName(),"CompanyPrefix")
	
	def test_Offset(self):
		self.assertEquals(self.field.offset, 3)
		self.assertEquals(self.field2.offset, 0)
	
	def test_BitLength(self):
		self.assertEquals(self.field.getBitLength(),8)
		self.assertEquals(self.field2.getBitLength(),24)
	
	def test_Ordinal(self):
		self.assertEquals(self.field.ordinal, 1)
		self.assertEquals(self.field2.ordinal, 2)
	
	def test_Value(self):
		self.assertEquals(int(self.field.value), 6)
		self.assertEquals(int(self.field2.value), 49000)
	
	def test_DigitLength(self):
		self.assertEquals(self.field.digit_length, 1)
		self.assertEquals(self.field2.digit_length, 6)
	
	def test_GetBits(self):
		self.assertEquals(len(self.field2.bits) , 8)
		
		
	def test_ToXml(self):
		"""
		Tests that the toXml method of the a field returns xml
		"""
		xml = self.field.toXml()
		self.assertNotEqual(len(xml),0)
		self.assertTrue(xml.startswith("<Field "))
		
	def test_AddFieldToDictionary(self):
		"""
		Tests adding fields to the dictionary
		"""
		self.fieldDictionary = FieldDictionary()
		self.field = Field("SerialNumber",offset=3,bitLength=8,ordinal=1,fieldValue=6,digitLength=1)	
		self.field2 = Field("CompanyPrefix",offset=0,bitLength=24,ordinal=2,fieldValue=49000,digitLength=6)
		self.fieldDictionary[self.field2.getFieldName()] = self.field2
		self.fieldDictionary[self.field.getFieldName()] = self.field
		self.assertEqual(len(self.fieldDictionary),2)
		
	def test_SortFields(self):
		"""
		Tests that the Field Dictionary returns fields ordered
		"""
		
		fieldDictionary = FieldDictionary()
		
		self.field = Field("SerialNumber",offset=3,bitLength=8,ordinal=1,fieldValue=6,digitLength=1)	
		self.field2 = Field("CompanyPrefix",offset=0,bitLength=24,ordinal=2,fieldValue=49000,digitLength=6)
		fieldDictionary[self.field.getFieldName()] = self.field
		fieldDictionary[self.field2.getFieldName()] = self.field2
	
		i=0
		for f in fieldDictionary.values():
			self.assertTrue(i<int(f.ordinal))
			i = int(f.ordinal)
			
		

if __name__ == "__main__":
	unittest.main()		
	