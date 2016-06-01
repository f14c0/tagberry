class Conversion:

	def int8(self,val):
		"""convert to signed 8 bit integer"""
		i = self._toInt(val)
		return (i + 2**7) % 2**8 - 2**7
	
	def uint8(self,val):
		"""convert to unsigned 8 bit integer"""
		i = self._toInt(val)
		return (i + 2**7) % 2**8 - 2**7
	
	def int16(self,val):
		"""convert to signed 16-bit integer"""
		i = self._toInt(val)
		return (i + 2**15) % 2**16 - 2**15  
	
	def uint16(self,val):
		"""convert to unsigned 16-bit integer"""
		i = self._toInt(val)
		return i % 2**16
	
	def int32(self,val):
		"""convert to signed 32-bit integer"""
		i = self._toInt(val)
		return (i + 2**31) % 2**32 - 2**31  
	
	def uint32(self,val):
		"""convert to unsigned 32-Bit integer"""
		i = self._toInt(val)
		return i % 2**32                    
	
	def int64(self,val):
		"""convert to signed 64-bit integer"""
		i = self._toInt(val)
		return (i + 2**63) % 2**64 - 2**63  
	
	def uint64(self,val):
		"""convert to unsigned 64-bit integer"""
		i = self._toInt(val)
		return i % 2**64

	def _toInt(self,val):
		"""converts types not of integer to an integer"""
		if(not isinstance(val,int)):
			return int(val)
		else:
			return val
		
	
