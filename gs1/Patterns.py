import re

"""GTIN Patterns"""
gtin14_AI01P_AI21P = r"^\(01\)(?P<gtin14>\d{14})\(21\)(?P<serialNumber>[A-Za-z0-9]{1,20})$"
gtin14_AI01_AI21 = r"^01(?P<gtin14>\d{14})21(?P<serialNumber>[A-Za-z0-9]{1,20})$"
gtin14_AI01_AI21_FIXEDLEN = r'^01(?P<gtin14>\d{14})21(?P<serialNumber>\d{12})'
gtin14_AI01_AI21_FIXEDLEN_PARAMS = r"^01(?P<gtin14>\d{14})21(?P<serialNumber>[A-Za-z0-9]{12})"
gtin14_AI01_AI21_VARIABLELEN_PARAMS = r"^01(?P<gtin14>\d{14})21(?P<serialNumber>[A-Za-z0-9]{1,20})$"
gtin14_AI01_AI21_FIXEDLEN_START = r'^01(?P<gtin14>\d{14})21(?P<serialNumber>\d{12})([A-Za-z0-9]*)'
gtin14_AI01_AI21_FIXEDLEN_START_PARAMS = r"^01(?P<gtin14>\d{14})21(?P<serialNumber>[A-Za-z0-9]{12})(\d*)"
gtin_AI01P_AI21P_AI10P_AI17P = r"^\(01\)(?P<gtin14>\d{14})\(21\)([A-Za-z0-9]{1,20})\(17\)(\d{6})\(10\)(\d{1,20})$"
gtin_AI01_AI21_AI10_AI17 = r"^01(?P<gtin14>\d{14})21(?P<serialNumber>[A-Za-z0-9]{1,20})17(\d{6})10(\d{1,20})$"
gtin_AI01_AI21_UNIVERSAL = r"^(\(01\)|01)(?P<gtin14>\d{14})(\(21\)|21)(?P<serialNumber>[A-Za-z0-9]{1,20})(\((d{2})\)|17)?(.)*"
gtin14_AI01P = r"^\(01\)(?P<gtin14>\d{14})$"
gtin14_AI01 = r"^01(?P<gtin14>\d{14})$"
gtin14 = r"(?P<gtin14>\d{14})$"
gtin_patterns = [gtin_AI01_AI21_UNIVERSAL,
                 gtin14_AI01P_AI21P,
                 gtin14_AI01_AI21,
                 gtin14,
                 gtin14_AI01,
                 gtin14_AI01P,
                 gtin_AI01P_AI21P_AI10P_AI17P,
                 gtin_AI01_AI21_AI10_AI17,
                 gtin14_AI01_AI21_FIXEDLEN,
                 gtin14_AI01_AI21_VARIABLELEN_PARAMS]

def get_compiled_sgtin_patterns():
    '''
    Compiles the patterns defined in gtin_patterns and returns an array
    of regular expression objects.
    '''
    ret = []
    for pattern in gtin_patterns:
        regex = re.compile(pattern)
        ret.append(regex)
    return ret


"""SSCC Patterns"""
sscc18_universal_params = r'^(\(00\)|00)?(?P<sscc18>[0-9]{18})$'
sscc18_universal = r'^(\(00\)|00)?(?P<sscc18>[0-9]{18})$'
sscc18_A100P = r"^\(00\)(?P<sscc18>[0-9]{18})$"
sscc18_A100 = r"^00(?P<sscc18>[0-9]{18})$"
sscc18 = r"^(?P<sscc18>[0-9]{18})$"
sscc_patterns = [sscc18,sscc18_A100P,sscc18_A100,sscc18_universal_params, sscc18_universal]

def get_compiled_sscc_patterns():
    '''
    Compiles the patterns defined in sscc_patterns and returns an array
    of regular expression objects.
    '''
    ret = []
    for pattern in sscc_patterns:
        regex = re.compile(pattern)
        ret.append(regex)
    return ret

"""GLN Patterns"""
gln_p = r"^\(414\)([0-9]{13})\(254\)([0-9]{1,20})$"
gln_np = r"^414([0-9]{13})254([0-9]{1,20})$"
gln_noext = r"^\(414\)([0-9]{13})$"
gln_noext_np = r"^414([0-9]{13})$"
gln = "^([0-9]{13})$"
gln_patterns = [gln,gln_np,gln_noext,gln_noext_np,gln_p]

"""GDTI Patterns"""
gdti_p = r"^\(253\)([0-9]{13})([0-9]{1,17})$"
gdti_p_nsn = r"^\(253\)([0-9]{13})$"
gdti_np_nsn = "^253([0-9]{13})$"
gdti_np_sn = "^253([0-9]{13})([0-9]{1,17})$"
gdti_nai_sn = "^([0-9]{13})([0-9]{1,17})$"
gdti_nai_nsn = "^([0-9]{13})$"
gdti_patterns = [gdti_p,gdti_p_nsn,gdti_np_sn,gdti_nai_sn,gdti_nai_nsn]

"""GRAI Patterns"""
grai_p = r"^\(8003\)0([0-9]{13,30})$"
grai_np = r"^(8003)0([0-9]{13,30})$"
grai = "^0([0-9]{13})([1,16])$"
grai_patterns = [grai_p,grai_np,grai]

