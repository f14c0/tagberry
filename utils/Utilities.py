import string 

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