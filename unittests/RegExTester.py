import re
#([a-zA-Z]-\(d{2,3}):(\d{1})\.(\d{4,7})\.(\d{1,10})\.(\d)*$

#sgtin-96:7.035846802.0339.395
pattern = r"^urn:tagpy:tag:([a-zA-Z]{2,7}-\d{2,3}):\d{4,10}\.\d{1,10}\.\d{1,21}"
urn = "urn:tagpy:tag:gid-96:10240.19254.0"

m = re.match(pattern,urn)

print(m.group())