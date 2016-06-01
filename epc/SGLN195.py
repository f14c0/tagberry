from encoding.EPCNumber import EPCNumber
from epcerrors.EncodingException import EncodingException
from schema.Field import Field 
class SGLN195(EPCNumber):
    '''
     Represents an SGLN-195 EPC Encoding
     The Serialized Global Location Number EPC scheme is used to assign a unique identity
     to a physical location, such as a specific building or a specific unit of shelving within a
     warehouse.
     '''
    def __init__(self,startSerialNumber=0,numOfSerialNumbers=0):
        EPCNumber.__init__(self)
        self._loadFields()
        self._encodingType="SGLN-195"
    def toEPCUri(self):
        '''Returns the SGLN-195 in an EPC URI Representation'''
        if(len(self.getFieldValue("CompanyPrefix"))+len(self.getFieldValue("LocationReference")) != 12):
            raise EncodingException("The Length of the CompanyPrefix and the ItemReference must equal 12")
        epcUri = "urn:tagpy:id:sgln:%s.%s.%s" % (self.getFieldValue("CompanyPrefix"),self.getFieldValue("LocationReference"),self.getFieldValue("Extension"))
        return epcUri 
        
    def _loadFields(self):
        """
        Loads Fields for the SGLN-195 
        """
        header = Field(fieldName="Header",offset=0,bitLength=8,ordinal=1,fieldValue=49,digitLength=2)
        self.fieldDictionary["Header"] = header
        filter = Field(fieldName="Filter",offset=8,bitLength=3,ordinal=2,fieldValue=0,digitLength=1) 
        self.fieldDictionary["Filter"] = filter
        partition = Field(fieldName="Partition",offset=11,bitLength=3,ordinal=3,fieldValue=0,digitLength=1) 
        self.fieldDictionary["Partition"] = partition 
        #These next two fields will have their offset,bitLength,digitLength, and value determined at runtime
        companyPrefix = Field(fieldName="CompanyPrefix",offset=14,bitLength=24,ordinal=4,fieldValue=0,digitLength=6) 
        self.fieldDictionary["CompanyPrefix"] = companyPrefix
        locationReference = Field(fieldName="LocationReference",offset=21,bitLength=24,ordinal=5,fieldValue=0,digitLength=6) 
        self.fieldDictionary["LocationReference"] = locationReference
        extension = Field(fieldName="Extension",offset=41,bitLength=140,ordinal=6,fieldValue=0,digitLength=0) 
        self.fieldDictionary["Extension"] = extension