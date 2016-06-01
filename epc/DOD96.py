from encoding.EPCNumber import EPCNumber
from schema.Field import Field 

class DOD96(EPCNumber):
    '''Represents a DOD-96 EPC Encoding'''
    def __init__(self,startSerialNumber=0,numOfSerialNumbers=0):
        EPCNumber.__init__(self)
        self._loadFields()
    
    
    def toEPCUri(self):
        '''Returns the DOD-96 in an EPC URI Representation'''
        #if(len(self.getFieldValue("Cage"))+len(self.getFieldValue("SerialNumber")) != 13):
            #raise EncodingException("The Length of the CompanyPrefix and the ItemReference must equal 13")
        epcUri = "urn:epc:id:usdod:%s.%s" % (self.getFieldValue("Cage"),self.getFieldValue("SerialNumber"))
        return epcUri    
    
    
    def _loadFields(self):
        """
        Loads Fields for the DOD-96 
        """
        header = Field(fieldName="Header",offset=0,bitLength=8,ordinal=1,fieldValue=48,digitLength=2)
        self.fieldDictionary["Header"] = header
        filter = Field(fieldName="Filter",offset=8,bitLength=3,ordinal=2,fieldValue=0,digitLength=1) 
        self.fieldDictionary["Filter"] = filter
        partition = Field(fieldName="Partition",offset=11,bitLength=3,ordinal=3,fieldValue=0,digitLength=1) 
        self.fieldDictionary["Partition"] = partition 
        #These next two fields will have their offset,bitLength,digitLength, and value determined at runtime
        companyPrefix = Field(fieldName="Cage",offset=14,bitLength=24,ordinal=4,fieldValue=0,digitLength=6) 
        self.fieldDictionary["Cage"] = companyPrefix
        serialNumber = Field(fieldName="SerialNumber",offset=58,bitLength=38,ordinal=5,fieldValue=0,digitLength=6) 
        self.fieldDictionary["SerialNumber"] = serialNumber