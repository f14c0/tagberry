class CharacterSet:
    def __init__(self):
        #Graphic Symbol,Hex Value, Uri Form
        self._characterSets = \
        [
             ['!',0x21,'!'], 
             ['"',0x22,'%22'], 
             ['%',0x25,'%25'], 
             ['&',0x26,'%26'], 
             ["'",0x27,"'"], 
             ['(',0x28,'('], 
             [')',0x29,')'],
             ['*',0x2A,'*'],
             ['+',0x2B,'+'],
             [',',0x2C,','],
             ['-',0x2D,'-'],
             ['.',0x2E,'.'],
             ['/',0x2F,'%2F'],
             ['0',0x30,'0'],
             ['1',0x31,'1'],
             ['2',0x32,'2'],
             ['3',0x33,'3'],
             ['4',0x34,'4'],
             ['5',0x35,'5'],
             ['6',0x36,'6'],
             ['7',0x37,'7'],
             ['8',0x38,'8'],
             ['9',0x39,'9'],
             [':',0x3A,':'],
             [';',0x3B,';'],
             ['<',0x3C,'%3C'],
             ['=',0x3D,'='],
             ['>',0x3E,'%3E'],
             ['?',0x3F,'%3F'],
             ['A',0x41,'A'],
             ['B',0x42,'B'],
             ['C',0x43,'C'],
             ['D',0x44,'D'],
             ['E',0x45,'E'],
             ['F',0x46,'F'],
             ['G',0x47,'G'],
             ['H',0x48,'H'],
             ['I',0x49,'I'],
             ['J',0x4A,'J'],
             ['K',0x4B,'K'],
             ['L',0x4C,'L'],
             ['M',0x4D,'M'],
             ['N',0x4E,'N'],
             ['O',0x4F,'O'],
             ['P',0x50,'P'],
             ['Q',0x51,'Q'],
             ['R',0x52,'R'],
             ['S',0x53,'S'],
             ['T',0x54,'T'],
             ['U',0x55,'U'],
             ['V',0x56,'V'],
             ['W',0x57,'W'],
             ['X',0x58,'X'],
             ['Y',0x59,'Y'],
             ['Z',0x5A,'Z'],
             ['_',0x5F,'_'],
             ['a',0x61,'a'],
             ['b',0x62,'b'],
             ['c',0x63,'c'],
             ['d',0x64,'d'],
             ['e',0x65,'e'],
             ['f',0x66,'f'],
             ['g',0x67,'g'],
             ['h',0x68,'h'],
             ['i',0x69,'i'],
             ['j',0x6A,'j'],
             ['k',0x6B,'k'],
             ['l',0x6C,'l'],
             ['m',0x6D,'m'],
             ['n',0x6E,'n'],
             ['o',0x6F,'o'],
             ['p',0x70,'p'],
             ['q',0x71,'q'],
             ['r',0x72,'r'],
             ['s',0x73,'s'],
             ['t',0x74,'t'],
             ['u',0x75,'u'],
             ['v',0x76,'v'],
             ['w',0x77,'w'],
             ['x',0x78,'x'],
             ['y',0x79,'y'],
             ['z',0x7A,'z'] 
        ] 
        
        
    
    def getCharacterByHex(self, hex_val):
        '''
        A hexadecimal numeral that gives the 7-bit binary 3071 value for the character
        as used in EPC binary encodings. This hexadecimal value is always equal to the ISO
        (ASCII) code for the character.
        '''
        for i in range(len(self._characterSets)):
            if self._characterSets[i][1] == hex_val:
                return self._characterSets[i][0]
    
    def getCharacterByUriForm(self,uriRep):
       
        for i in range(len(self._characterSets)):
            if self._characterSets[i][2] == uriRep:
                return self._characterSets[i][0] 
        
    def getHexByCharacter(self,character):     
        for i in range(len(self._characterSets)):
            if self._characterSets[i][0] == character:
                return self._characterSets[i][1]
    
    def getHexByUriForm(self,uriForm):     
        for i in range(len(self._characterSets)):
            if self._characterSets[i][2] == uriForm:
                return self._characterSets[i][1]