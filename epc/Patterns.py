import re 
from collections import OrderedDict
sgtin96 = ""

SGTIN198_PAT = r"^(P<gtin-14>([0-9]{14})?(?P<serialNumber>([!%-?A-Z_a-z\x22]{1,20})"
sgtin198_patterns = [SGTIN198_PAT,]



def compile_patterns(*args):
    '''
    Compiles the epc regex patterns returns an array
    of regular expression objects.
    '''
    ret = OrderedDict()
    for pats in args:
        for pattern in pats:
            regex = re.compile(pattern)
            ret.append(regex)
    return ret

compile_patterns(sgtin198_patterns)

if __name__ == "main":
    compile_patterns(sgtin198_patterns)