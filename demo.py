import re

username = 'admin001'

result = re.search('^[a-zA-Z]\w{5,}$',username)
print(result)


msg = "aa.py  ab.txt. bb.py .kk.png uu.py"
result1 = re.findall("py\\b", msg)
print(result1)