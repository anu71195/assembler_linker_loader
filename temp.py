import re;
print(re.compile(r'glob var (.*)=(.*)').match("glob var sda=basf ").group(2));
print(re.compile(r'extern(.*)').match("extern a").group(1));
print(re.compile(r'var (.*)=(.*)').match(""));

print(re.compile(r'(.+)=(.+)\+(.+)').match("a=bb\+3").group(2));
print(re.compile(r'(.+)=(.+)\-(.+)').match(""));
print(re.compile(r'(.+)=(.+)\&(.+)').match(""));
print(re.compile(r'(.+)=(.+)\|(.+)').match(""));
print(re.compile(r'loop(.+)').match(""));
print(re.compile(r'endloop(.*)').match(""));
print(re.compile(r'if (.*)>(.*)').match(""));
print(re.compile(r'endif(.*)').match(""));
print(re.compile(r'if (.*)=(.*)').match(""));
