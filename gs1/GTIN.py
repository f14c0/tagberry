import re
from epcerrors.GS1Exception import GS1Exception 
from gs1.GS1Number import GS1Number
from gs1.Patterns import gtin_patterns
from future.types.newint import long


class GTIN(GS1Number):
	'''Represents a GS1 GTIN'''

	def __init__(self, companyPrefix="0000000"):
		super().__init__(companyPrefix)
		self._itemReference = None
		self._indicatorDigit = "0"
		self._gtin14 = ""
		self._encodingType = "GTIN"
		self._expirationDate = None
		self._lot=None
		self._fixedSerialNumber = False
		self._fixedSerialNumberLength=0
		self.hasAIs = False
		
	def encode(self, indicatorDigit, itemReference, serialNumber=0, serialNumberLength=1):
			self._applicationIdentifiersList.append("(01)")
			self._itemReference = itemReference
			self._indicatorDigit = indicatorDigit
			if(int(serialNumber)>0):
				self._serialNumber = serialNumber.zfill(serialNumberLength)
				self._applicationIdentifiersList.append("(21)")
			
			gs1 = "%s%s%s" % (self._indicatorDigit,self._companyPrefix,self._itemReference)
			checkDigit = self._calculateCheckDigit(gs1)
			if(int(serialNumber)>0):
				gs1 = "(01)%s%s(21)%s" % (gs1,checkDigit,self.getSerialNumber())
			else:
				gs1 = "(01)%s%s" % (gs1,checkDigit)
				
			self._gs1 = gs1
			self.parse(self._gs1)
			
	def toCoreNumber(self):
		'''Returns the Core Number e.g. GTIN-14, SSCC-18 without the App Identifiers'''
		return self._gtin14
	
	def getEncodingIdentifier(self):
		return self._companyPrefix
	
	def parse(self,gtin):
		'''The parse() method allows you to parse a valid GS1 GTIN-14 and then have access to its individual fields'''
		if(self.isValid(gtin)):
			#store the original gtin
			self._gs1=gtin	
		else:
			raise GS1Exception("The supplied GTIN, '%s' is invalid." % gtin) 
		
		self._parseAIs()
		if(len(self._applicationIdentifiersList)):
			self.hasAIs = True
		
		if(self.hasAIs):
			localGtin = self._gtin14
		else:
			localGtin = gtin
			self._gtin14 = gtin
			
		#finish parsing gtin
		self._indicatorDigit = localGtin[:1]
		#remove the last digit an
		if(len(localGtin)!=14):
			#Calculate Check Digit
			localGtin+=str(self._calculateCheckDigit(localGtin))
		self._encodingSize = len(localGtin)
		self._indicatorDigit = localGtin[:1]
		self._itemReference = localGtin[len(self._companyPrefix)+1:len(localGtin)-1]
		
			
	def getItemReference(self):
		return self._itemReference
	def setItemReference(self,value):
		self._itemReference = value
	def getIndicatorDigit(self):
		return self._indicatorDigit
	def setIndicatorDigit(self,value):
		self._indicatorDigit
	def getEncodingSize(self):
		return self._encodingSize
	def getExpirationDate(self):
		return self._expirationDate
	def setExpirationDate(self,value):
		self._expirationDate= value
	def getLot(self):
		return self._lot
	def setLot(self,value):
		self._lot= value
	def getUseFixedSerialNumber(self):
		return self._fixedSerialNumber
	def setUseFixedSerialNumber(self,value):
		self._fixedSerialNumber = value
	def getFixedSerialNumberLength(self):
		return self._fixedSerialNumberLength
	def setFixedSerialNumberLength(self,value):
		self._fixedSerialNumberLength = value
		
	
	def _parseAIs(self):
		if(len(self._gs1)<=14):
		#no A1 in this gs1
			self._applicationIdentifiersList = [] 
			return 
		
		#Pattern to find AIs e.g. (21)
		matchAiWithParens = r"(\(+\d*\)+)" 
		p = re.compile(matchAiWithParens)
		#Get all AIs
		ais = list(p.finditer(self._gs1))
		#Clear old _applicationIdentifires
		self._applicationIdentifiersList = []
		if(len(ais)):
			#build new AI List
			for match in ais:
				self._applicationIdentifiersList.append(self._gs1[match.start():match.end()])
				if(self._gs1[match.start():match.end()]=="(01)"):
					#get the gtin14 body
					self._gtin14 = self._gs1[match.start()+4:match.end()+14]
				if(self._gs1[match.start():match.end()]=="(21)"):
					self._serialNumber = self._gs1[match.start()+4:]
				if(self._gs1[match.start():match.end()]=="(17)"):
					self._expirationDate = self._gs1[match.start():match.end()]
				if(self._gs1[match.start():match.end()]=="(10)"):
					self._lot = self._gs1[match.start():match.end()]	
		else:
			strippedGS1 = ""
			matchAiWithOutParens = r"(^(01)+)" 
			p = re.compile(matchAiWithOutParens)
			ais = list(p.finditer(self._gs1))
			for match in ais:
				self._applicationIdentifiersList.append(self._gs1[match.start():match.end()])
				#get the gtin14 body
				self._gtin14 = self._gs1[match.start() + 2:16]
				strippedGS1 = self._gs1[16:]
			
			matchAiWithOutParens = r"17(\d{6})"
			p = re.compile(matchAiWithOutParens)
			ais = list(p.finditer(strippedGS1))
			for match in ais:
				self._applicationIdentifiersList.append(strippedGS1[match.start():match.start()+2])
				#get the gtin14 body
				self._expirationDate = strippedGS1[match.start()+2: match.end()]
				strippedGS1 = strippedGS1.replace("17%s" % (self._expirationDate), "")
			matchAiWithOutParens = r"10(\d{1,20})$"
			p = re.compile(matchAiWithOutParens)
			ais = list(p.finditer(self._gs1))
			for match in ais:
				self._applicationIdentifiersList.append(self._gs1[match.start():match.start()+2])
				#get the gtin14 body
				self._lot = self._gs1[match.start()+2: match.end()]
				strippedGS1 = strippedGS1.replace("10%s" % (self._lot), "")
			#for a gtin who has no parens, look for AI 21
			matchAiWithOutParens = r"21(\d{1,20})" 
			p = re.compile(matchAiWithOutParens)
			ais = list(p.finditer(strippedGS1))
			for match in ais:
				self._applicationIdentifiersList.append(strippedGS1[match.start():match.start()+2])
				#get the serial number
				self._serialNumber = strippedGS1[match.start()+2:match.end()]
			
	
	def isValid(self,gtin):
		'''Determines if the GTIN is valid'''
		for pat in gtin_patterns:
			m = re.match(pat,gtin)
			if(m!=None):
				return True
		#did not match any gtin patterns	
		return False	

	def toGTIN14(self):
		return self._gtin14
	def toGS1(self,useParenthesesAroundAIs=False):
		if useParenthesesAroundAIs==True:
			if self.getUseFixedSerialNumber()==True:
				return "(01)%s(21)%s" % (self._gtin14,str(self._serialNumber).zfill(self.getFixedSerialNumberLength()))
			else:
				return "(01)%s(21)%s" % (self._gtin14,str(self._serialNumber))
				
					
		else:
			if self.getUseFixedSerialNumber() == True:
				return "01%s21%s" % (self._gtin14,str(self._serialNumber).zfill(self.getFixedSerialNumberLength()))
			else:
				return "01%s21%s" % (self._gtin14, long(self._serialNumber))
					
	def toURN(self):
		return 'urn:tagpy:id:sgtin:{0}.{1}{2}.{3}'.format(self._companyPrefix, self._indicatorDigit, self._itemReference, int(self._serialNumber))			
	
	