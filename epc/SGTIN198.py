from epc.EPCNumber import EPCNumber
from epcerrors.EncodingException import EncodingException
from schema.Field import Field
 
class SGTIN198(EPCNumber):
    '''Represents an SGTIN-198 EPC Encoding'''
    def __init__(self, startSerialNumber=0, numOfSerialNumbers=0):
        
        EPCNumber.__init__(self)
        self._loadFields()
    
    def toEPCUri(self):
        '''Returns the SGTIN-198 in an EPC URI Representation'''
        if(len(self.getFieldValue("CompanyPrefix"))+len(self.getFieldValue("ItemReference")) != 13):
            raise EncodingException("The Length of the CompanyPrefix and the ItemReference must equal 13")
        epcUri = "urn:tagpy:id:sgtin:%s.%s.%s" % (self.getFieldValue("CompanyPrefix"),self.getFieldValue("ItemReference"),self.getFieldValue("SerialNumber"))
        return epcUri
    
        
    def _loadFields(self):
        """
        Loads Fields for the SGTIN-198 
        """
        header = Field(fieldName="Header",offset=0,bitLength=8,ordinal=1,fieldValue=54,digitLength=2)
        self.fieldDictionary["Header"] = header
        filter = Field(fieldName="Filter",offset=8,bitLength=3,ordinal=2,fieldValue=0,digitLength=1) 
        self.fieldDictionary["Filter"] = filter
        partition = Field(fieldName="Partition",offset=11,bitLength=3,ordinal=3,fieldValue=0,digitLength=1) 
        self.fieldDictionary["Partition"] = partition 
        #These next two fields will have their offset,bitLength,digitLength, and value determined at runtime
        companyPrefix = Field(fieldName="CompanyPrefix",offset=14,bitLength=24,ordinal=4,fieldValue=0,digitLength=6) 
        self.fieldDictionary["CompanyPrefix"] = companyPrefix
        itemReference = Field(fieldName="ItemReference",offset=38,bitLength=24,ordinal=5,fieldValue=0,digitLength=6) 
        self.fieldDictionary["ItemReference"] = itemReference
        serialNumber = Field(fieldName="SerialNumber",offset=58,bitLength=140,ordinal=6,fieldValue=0,digitLength=6) 
        self.fieldDictionary["SerialNumber"] = serialNumber