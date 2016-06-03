from epc.EPCNumber import EPCNumber
from epcerrors.EncodingException import EncodingException
from schema.Field import Field 
class GIAI202(EPCNumber):
    '''
    Represents an GIAI-202 EPC Encoding
    The Global Individual Asset Identifier EPC scheme is used to assign a unique identity to
    a specific asset, such as a forklift or a computer.
    '''
    def __init__(self,startSerialNumber=0,numOfSerialNumbers=0):
        EPCNumber.__init__(self)
        self._loadFields()
    
    def toEPCUri(self):
        '''Returns the GIAI-202 in an EPC URI Representation'''
        if(len(self.getFieldValue("CompanyPrefix"))+len(self.getFieldValue("IndividualAssetReference")) != 13):
            raise EncodingException("The Length of the CompanyPrefix and the IndividualAssetReference must equal 13")
        epcUri = "urn:tagpy:id:giai:%s.%s" % (self.getFieldValue("CompanyPrefix"),self.getFieldValue("IndividualAssetReference"))
        return epcUri 
    
        
    def _loadFields(self):
        """
        Loads Fields for the GIAI-202
        """
        header = Field(fieldName="Header",offset=0,bitLength=8,ordinal=1,fieldValue=56,digitLength=2)
        self.fieldDictionary["Header"] = header
        filter = Field(fieldName="Filter",offset=8,bitLength=3,ordinal=2,fieldValue=0,digitLength=1) 
        self.fieldDictionary["Filter"] = filter
        partition = Field(fieldName="Partition",offset=11,bitLength=3,ordinal=3,fieldValue=0,digitLength=1) 
        self.fieldDictionary["Partition"] = partition 
        #These next two fields will have their offset,bitLength,digitLength, and value determined at runtime
        companyPrefix = Field(fieldName="CompanyPrefix",offset=14,bitLength=24,ordinal=4,fieldValue=0,digitLength=6) 
        self.fieldDictionary["CompanyPrefix"] = companyPrefix
        assetReference = Field(fieldName="IndividualAssetReference",offset=21,bitLength=24,ordinal=5,fieldValue=0,digitLength=6) 
        self.fieldDictionary["IndividualAssetReference"] = assetReference