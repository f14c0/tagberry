class Partitions():
        def __init__(self):
            self.PartitionValue = 0
            self.CompanyPrefixBits = 1
            self.CompanyPrefixDigits = 2
            self.ItemBits = 3
            self.ItemDigits = 4
            
            self.SGTIN  = [[0, 40,12,4,1], [1, 37,11,7,2], [2,34,10,10,3], [3,30,9,14,4], [4,27,8,17,5], [5,24,7,20,6], [6,20,6,24,7]]
            self.SSCC   = [[0, 40,12,18,5],[1, 37,11,20,6],[2,34,10,24,7], [3,30,9,27,8], [4,27,8,30,9], [5,24,7,34,10], [6,20,6,38,11]]
            self.GRAI   = [[0, 40,12,4,0], [1, 37,11,7,1], [2,34,10,10,2], [3,30,9,14,3], [4,27,8,17,4], [5,24,7,20,5], [6,20,6,24,6]]
            self.GIAI   = [[0, 40,12,42,12], [1, 37,11,45,13],[2,34,10,48,14], [3,30,9,52,15], [4,27,8,55,16],[5,24,7,58,17],[6,20,6,62,18]]
            self.SGLN   = [[0, 40,12,1,0],[1, 37,11,4,1], [2,34,10,7,2], [3,30,9,11,3], [4,27,8,14,4], [5,24,7,17,5], [6,20,6,21,6]]
            self.GIAI202 = [[0, 40,12,148,18],[1, 37,11,151,19], [2,34,10,154,20], [3,30,9,158,21], [4,27,8,161,22], [5,24,7,164,23], [6,20,6,168,24]]
            self.GSRN  =  [[0, 40,12,18,5],[1, 37,11,21,6], [2,34,10,24,7], [3,30,9,28,8], [4,27,8,31,9], [5,24,7,34,10], [6,20,6,38,11]]
            self.GDTI  =  [[0, 40,12,1,0],[1, 37,11,4,1], [2,34,10,7,2], [3,30,9,11,3], [4,27,8,14,4], [5,24,7,17,5], [6,20,6,21,6]]
            self.GID   = [] #No Partition Table for GID-96
        def getNumbers(self,partitionType):
            '''Returns the proper partition table array based on the the partition type e.g. SGTIN, SSCC etc.'''
            if partitionType=="SGTIN-96":
                return  self.SGTIN
            if partitionType=="SGTIN":
                return  self.SGTIN
            elif partitionType=="SSCC":
                return self.SSCC
            elif partitionType=="GRAI":
                return self.GRAI
            elif partitionType=="GIAI":
                return self.GIAI
            elif partitionType=="GIAI202":
                return self.GIAI202
            elif partitionType=="SGLN":
                return self.SGLN
            elif partitionType=="GSRN":
                return self.GSRN
            elif partitionType=="GDTI":
                return self.GDTI       
            elif partitionType=="GID":
                return self.GID        
        
        def getPartitionValue(self,prefixLength,partitionType):
            '''Returns the proper Partition Value based on the Company Prefix Length and Partion Type
            Example : print GetPartitionValue(6,"SGTIN")'''
            numbers = self.getNumbers(partitionType)
            
            if prefixLength==5:
                prefixLength=6
            
            for i in range(len(numbers)):
                if numbers[i][self.CompanyPrefixDigits] == prefixLength:
                    return numbers[i][self.PartitionValue]


        def getCompanyPrefixDigitLength(self,partitionValue,partitionType):
                """Returns the number of digits allowed in a Company Prefix for a given tagpy epc"""
                numbers = self.getNumbers(partitionType)
                for i in range(len(numbers)):
                        if numbers[i][self.PartitionValue] == partitionValue:
                                return numbers[i][self.CompanyPrefixDigits]

        def getCompanyPrefixBitLength(self,partitionValue, partitionType):
                """Returns the number of bits allowed in a Company Prefix for a given tagpy epc"""
                numbers = self.getNumbers(partitionType)
                for i in range(len(numbers)):
                        if numbers[i][self.PartitionValue] == partitionValue:
                                return numbers[i][self.CompanyPrefixBits]

        def getItemBitLength(self,partitionValue,partitionType):
                """Returns the number of bits allowed in an Item Ref for a given tagpy epc"""
                numbers = self.getNumbers(partitionType)
                for i in range(len(numbers)):
                        if numbers[i][self.PartitionValue] == partitionValue:
                                return numbers[i][self.ItemBits]


        def getItemDigitLength(self,partitionValue,partitionType):
                """Returns the number of digits allowed in an Item Ref for a given tagpy epc"""
                numbers = self.getNumbers(partitionType)
                for i in range(len(numbers)):
                        if numbers[i][self.PartitionValue] == partitionValue:
                                return numbers[i][self.ItemDigits]
                            