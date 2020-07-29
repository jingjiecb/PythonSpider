import re
content='here is a num: 123, and here is a string: ABC, then here is a number: 456'
patten=re.compile('.*?(\d+).*?([A-Z]+)')
res=re.findall(patten,content)
print(res)