import string 
from gs1.Patterns import gtin_patterns, sscc_patterns, gln_patterns
import re

def ishex(s):
    if(s==None): return False
    if(len(s)==0): return False
    if(isbinary(s)):return False
    for c in s:
        if not c in string.hexdigits: return False
    return True

def isbinary(s):
    if(s==None): return False
    if(len(s)==0): return False
    for c in s:
        if c != "1" and c!="0": return False
    
    return True

def isGS1(val):
        '''
        Determines if the value passed in is a GS1 Encoding.
        
        Args:
            val (str) - A string that needs to be evaluated as a GS1 Encoding
        
        Returns:
            (bool) - True, if the val is a GS1 Encoding. False, if not.
            
        '''
        
        for pat in gtin_patterns:
            m = re.match(pat, val)
            if(m!=None):
                return True
        
        for pat in sscc_patterns:
            m = re.match(pat, val)
            if(m!=None):
                return True
        
        for pat in gln_patterns:
            m = re.match(pat, val)
            if(m!=None):
                return True
            
        return False

def hextobin(hexval):
        '''
        Takes a string representation of hex data with
        arbitrary length and converts to string representation
        of binary.  Includes padding 0s
        '''
        thelen = len(hexval)*4
        binval = bin(int(hexval, 16))[2:]
        while ((len(binval)) < thelen):
            binval = '0' + binval
        return binval  