#coding:utf-8

#字节串转为16进制字符串
#"\xff\x01" --> "ff01" 
def toHexString(strs, sep=''):
    return sep.join(map(lambda c: "%02X" % ord(c), strs))

def bytesToHexStringList(bytes):
    li = []
    li = map(lambda c: c, bytes)
    return li

def bytesToIntergerList(bytes):
    li = []
    li = map(lambda c: ord(c), bytes) 
    return li

def bytesToString(bytes):
    return ''.join(map(chr, bytes))
    
def splitByLength(data, step):
    hexlist = [data[i:i+step] for i in xrange(0, len(data), step)]
    return hexlist   
    
def hexToString(strHex):
    return ''.join(map(lambda h: chr(int(h, 16)), splitByLength(strHex,2)))

#16进制字符串转为整数列表
#"ff01" --> [255, 1] 
def hexStringToIntList(strHex):
    return map(lambda h: int(h, 16), splitByLength(strHex,2))  

#16进制字符串转为字节串
#"ff01" --> "\xff\x01" 
def hexStringToBytes(strHex):
    return "".join(map(lambda h: chr(int(h, 16)), splitByLength(strHex,2))) 

def BCDtoInteger(bcdBytes):
    IntVal = 0
    for (i, val) in enumerate(bcdBytes):
        IntVal = IntVal * 10 + (ord(val)>>4)
        IntVal = IntVal * 10 + (ord(val)&0x0F)
    return IntVal
