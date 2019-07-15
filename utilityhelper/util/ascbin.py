#coding:utf-8
"""
binascii模块:二进制和ASCII互转.Python版本：1.5及以后版本
    1)包含很多在二进制和ASCII编码的二进制表示转换的方法;
    2)包含更高级别的模块使用的，用C语言编写的低级高效功能;
    3)偶有使用于字符串和ASCII的转换;
通常情况不会直接使用这些功能，而是使用像UU，base64编码，或BinHex封装模块。
"""
import binascii
import struct
import base64


def string_to_string_list(strs, sep=' '):
    """字符串转列表。根据指定字符串sep拆分字符串
    >>> s = 'a b c'
    >>> string_to_string_list(s)
    ['a', 'b', 'c']
    >>> string_to_string_list('x11x22x33', 'x')
    ['', '11', '22', '33']
    """
    return [s for s in strs.split(sep)]


def string_list_to_string(stringli, sep=''):
    """列表转字符串
    :param stringli:
    :param sep:
    :return:
    >>> string_list_to_string(['1', '2', '3', '4', '5'])
    '12345'
    >>> string_list_to_string(['1', '2', '3', '4', '5'], '.')
    '1.2.3.4.5'
    >>> string_list_to_string(['1', '2', '3', '4', '5'], ' ')
    '1 2 3 4 5'
    """
    return sep.join(stringli)


def int_list_to_string(intli, sep=''):
    """整数列表转字符串
    :param intli:
    :param sep:
    :return:
    >>> int_list_to_string([1,2])
    '\\x01\\x02'
    """
    return sep.join([chr(n) for n in intli])

def structedhex_string_to_bytes(hexString, sep1, sep2):
    """十六进制字符串格式化成带特定分隔符的二进制
    :param hexString:
    :param sep1:
    :param sep2:
    :return:
    >>> structedhex_string_to_bytes("AA:BB:11:22:33", ':', '')
    '\\xaa\\xbb\\x11"3'
    >>> structedhex_string_to_bytes("31:32:33:34:35", ':', '*')
    '1*2*3*4*5'
    >>> structedhex_string_to_bytes("31:32:33:34:35", ':', '*')
    '1*2*3*4*5'
    """
    return sep2.join([chr(int(c, 16)) for c in hexString.split(sep1)])


def bytes_to_string_list(bytes):
    """
    :param bytes:
    :return:
    >>> bytes_to_string_list('\x12\x34')
    ['\\x12', '4']
    """
    li = []
    li = map(lambda c: c, bytes)
    return li


def bytes_to_int_list(bytes):
    """bytesToIntergerList
    :param bytes:
    :return:
    >>> bytes_to_int_list("12")
    [49, 50]
    """
    li = map(lambda c: ord(c), bytes)
    return li

# 过时的方法名
bytesToIntergerList = bytes_to_int_list

def bytes_to_wint_list(bytes, bitwidth=8, edian='B'):
    """bytesToIntList
    Args:
        bytes:
        bitwidth:
        edian:

    Returns:
    >>> bytes_to_wint_list("12")
    [49, 50]
    >>> s = '\x01\x02\x03\x04\x05\x06\x07\x08'
    >>> bytes_to_wint_list(s, bitwidth=8)
    [1, 2, 3, 4, 5, 6, 7, 8]
    >>> bytes_to_wint_list(s, bitwidth=16)
    [258, 772, 1286, 1800]
    >>> bytes_to_wint_list(s, bitwidth=32)
    [16909060, 84281096]
    """
    li = []
    if bitwidth==8:
            tp = struct.unpack("B" * len(bytes), bytes)
            li = list(tp)
    elif bitwidth==16: # short
        if edian.upper() == 'B':
            tp = struct.unpack(("!" + "H" * (len(bytes)/2)), bytes)
            li = list(tp)
        else:
            tp = struct.unpack(("H" * (len(bytes) / 2)), bytes)
            li = list(tp)
    elif bitwidth==32: # int or long
        if edian.upper() == 'B':
            tp = struct.unpack(("!" + "I" * (len(bytes)/4)), bytes)
            li = list(tp)
        else:
            tp = struct.unpack(("I" * (len(bytes)/4)), bytes)
            li = list(tp)

    return li


def int_list_to_bytes(bytes):
    """
    ASCII码值列表转字符串
    :param bytes:
    :return:
    >>> int_list_to_bytes([48,49])
    '01'
    >>> int_list_to_bytes([0x48,0x49])
    'HI'
    """
    return ''.join(map(chr, bytes))


bytesToString = int_list_to_bytes

def string_split_by_length(data, step):
    """按照给定的宽度切割字符串
    :param data:
    :param step:
    :return:
    >>> string_split_by_length("123", 1)
    ['1', '2', '3']
    >>> string_split_by_length("123", 2)
    ['12', '3']
    >>> string_split_by_length(b"123", 3)
    ['123']
    """
    hexlist = [data[i:i + step] for i in xrange(0, len(data), step)]
    return hexlist


def bytes_to_hex_string(strs, sep=''):
    """bytes_to_hex_string
    二进制字符串格式化成十六进制字符串；字符串转ASCII码；
    并使用连接字符串sep连接
    :param strs:
    :param sep:
    :return:
    >>> bytes_to_hex_string('hello')
    '68656C6C6F'
    >>> bytes_to_hex_string('\x11\x22')
    '1122'
    >>> bytes_to_hex_string(",\xFF,\xFF", '')
    '2CFF2CFF'
    """
    if sep != '':
        hexstring = sep.join(map(lambda c: "%02X" % ord(c), strs))
    else:
        # hexstring = binascii.hexlify(data)
        hexstring = binascii.b2a_hex(strs).upper()
    return hexstring

# 过时的方法名
BytesToFormatHexString = bytes_to_hex_string

def hex_string_to_bytes(strHex, sep=''):
    """hex_string_to_bytes
    十六进表示的字符串转二进制；ASCII码转字符串；
    使用连接字符串sep连接
    :param strHex:
    :param sep:
    :return:
    >>> hex_string_to_bytes('68656c6c6f')
    'hello'
    >>> hex_string_to_bytes('313233')
    '123'

    """
    if sep != '':
        binstr = sep.join(map(lambda h: chr(int(h, 16)), string_split_by_length(strHex, 2)))
    else:
        # binstr =  binascii.unhexlify(strHex)
        binstr = binascii.a2b_hex(strHex)
    return binstr

hexToString = hex_string_to_bytes


def hex_string_to_int_list(strHex):
    """十六进制字符串转整数列表
    :param strHex:
    :return:
    >>> hex_string_to_int_list('12ab34')
    [18, 171, 52]
    """
    return map(lambda h: int(h, 16), string_split_by_length(strHex, 2))


hexToIntList = hex_string_to_int_list

def hex_string_to_hex_list(strHex):
    """十六进制字符串转为列表
    :param strHex:
    :return:
     >>> hex_string_to_hex_list('12ab34')
     ['0x12', '0xab', '0x34']
    """
    return map(lambda h: hex(int(h, 16)), string_split_by_length(strHex, 2))


def int_number_to_hex_string(num, strlen):
    """把整数格式化成指定长度的十六进制字符串
    :param num:
    :param strlen:
    :return:
    >>> int_number_to_hex_string(65535, 4)
    'FFFF'
    >>> int_number_to_hex_string(65536, 8)
    '00010000'
    """
    return ''.join(("%" + "0%d" % strlen + "X") % num)


def bcd_string_to_int_number(bcdBytes):
    """8421BCD码与十进制数字字符串之间的转换。
    :param bcdBytes:
    :return:
    >>> bcd_string_to_int_number('\x12\x34')
    1234
    >>> bcd_string_to_int_number('1234')
    31323334
    >>> bcd_string_to_int_number('0023')
    30303233
    """
    IntVal = 0
    for (i, val) in enumerate(bcdBytes):
        # 这种编码形式利用四个位来储存一个十进制数,4位一组取值
        IntVal = IntVal * 10 + (ord(val) >> 4)      # 取字节高4bits
        IntVal = IntVal * 10 + (ord(val) & 0x0F)    # 取字节低4bits
    return IntVal


def int_number_to_bcd_string(integer):
    """整数转8421BCD码
    :param int:
    :return:
    >>> int_number_to_bcd_string(100)
    '000100000000'
    >>> int_number_to_bcd_string(65535)
    '01100101010100110101'
    """
    bcd = ''
    s = str(integer)
    for _ in s:
        bcd += '{0:0>4}'.format(bin(int(_)).replace('0b', ''))
    return bcd


def string_xor(str):
    """16进制字符串取反
    >>> string_xor('1234')
    'EDCB'
    >>> string_xor('FFFF')
    '0000'
    """
    by = 0
    bytes = hex_string_to_bytes(str)
    rbytes = ''
    for i in range(0,len(bytes)):
        rbytes += unichr((~ord(bytes[i]))&0xFF)
    return bytes_to_hex_string(rbytes)


strXor = string_xor


#for python 2
def _is_stringish(x):
    return isinstance(x, (str, basestring, bytes, unicode))


def _is_unicode(val):
    return isinstance(val, unicode)


def _is_intish(x):
    return isinstance(x, (int, long))


def tuple_to_string(tup_):
    """tuple2str
    :param tup_:
    :return:
    >>> tuple_to_string((1,2))
    '(1, 2, )'
    """
    s = ''
    s += '('
    for i in tup_:
        if _is_stringish(i):
            if _is_stringish(i):
                s += '\''
                if _is_unicode(i):
                    s += i.encode('utf8')
                else:
                    s += i
                s += '\''
        elif _is_intish(i):
            s += str(i)
        elif isinstance(i, list):
            s += list_to_string(i)
        s += ', '
    s += ')'
    return s


def list_to_string(li_):
    """list2str
    :param li_:
    :return:
    """
    s = '['
    for i in li_:
        if _is_stringish(i):
            s += '\''
            if _is_unicode(i):
                s += i.encode('utf8')
            else:
                s += i
            s += '\''
        elif _is_intish(i):
            s + str(i)
        elif isinstance(i, list):
            s += list_to_string(i)
        s += ', '
    s += ']'
    return s


def dict_to_string(dict_):
    """dict2str
    :param dict_:
    :return:
    """
    s = '{'
    for k, v in dict_.iteritems():
        # key
        # key type is str or unicode or int, tuple, fun
        if _is_stringish(k):
            s += '\''
            if _is_unicode(k):
                s += k.encode('utf8')
            else:
                s += k
            s += '\''
        elif _is_intish(k):
            s += str(k)
        elif isinstance(k, tuple):
            s += tuple_to_string(k)
        s += ": "

        # value
        if _is_stringish(v):
            s += '\''
            if _is_unicode(v):
                s += v.encode('utf8')
            else:
                s += v
            s += '\''
        elif _is_intish(v):
            s += str(v)
        elif isinstance(v, list):
            s += list_to_string(v)
        s += ', '
    s += '}'
    return s


def struct_data_to_string(data):
    """
    结构化的数据转为字符串，主要用于当数据对象里的元素包含中文的情况下，使用print打印不能输出中文的情况。
    支持多层嵌套，如{[{}, {}], {}, binary string, unicode string}
    :param data:
    :return:
    """
    s = ''
    if isinstance(data, dict):
        s += dict_to_string(data)
    elif isinstance(data, list):
        s += list_to_string(data)
    elif isinstance(data, tuple):
        s += tuple_to_string(data)
    return s


def hex_string_base64_encode(HexString):
    """Base64Encoder
    :param HexString:
    :return:
    """
    s = hex_string_to_bytes(HexString)
    return base64.b64encode(s)


def hex_string_base64_decode(HexString):
    s = hex_string_to_bytes(HexString)
    return base64.b64decode(s)


if __name__ == '__main__':
    dic = {
            'test str key1': u'测试Unicode值1', '测试str键1': u'test str value1', '测试str键2': ['', '测试str值2'],
            u'测试Unicode键1': ['', '测试str值2'],
            u'测试Unicode键2': ['', u'测试Unicode值2'],
            u'测试混合值': ['', {u'嵌套建1' : u'嵌套值1'}],
           (u'列表混合键1-Unicode', '列表混合键2-str'): u'测试混合键',
           }

    # print struct2str(dic)
    # print Base64Encoder("000345d2da3fce")
    # print Base64Encoder("0003376CD12FDE")
    # s = "414542474D502F2F2F2F2F2F2F2F2F2F2F2F395552554E495530684A546B386751554A4461476C755953417449455A70626D646C6369424C5A586C5164574A7361574D67566D567963326C76626942574D6A41314145726D7748303D"
    # print hexToString(s)
    print bytes_to_hex_string(hex_string_base64_decode("414151344D57414D7977453D"))

    template = "FGWFDYYRozEqfKgzCAdI5GhQcIgTE4mgo8SJLKaxL6KK43ShsmyVGQtJgRhRuDUcRpwU5YUREQaCEuDSHH4gSMbkmGKMsjIWGQMlIzwtLn4dDxGCdPpOfiNWjcjrMnBdeEMYMAqhdlnEuNQyhd1W4GilFMWGEQ1CYhJwThhvDkdFIpgiXGosD5GCJJJMJRZZHKWN01DCPF48SZHEyhLJUWhfLLZOBCbqBGDhSRudBgA2KAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=="
    feature = "FIWFFSSE4gAAFUieHAACTR26AABQg7hAAAHYrBgAAU+XYgAAInNnGAAAUntiAACMkSwgABNSfHgAAotTE4AARCsEsAAJ1WZiAAEertEAACWl2fAABTzKMQAAlVx6YAAC+7HQAAIyd5WAAFQvE6AAAiXmiAAAnxIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD0/wGQoFwCgABIAZAkAQCQAAAAAAcAAJAHAAKAAAAAAGDkAoD8rAKAAAAAAAAAAAAAAAAAAAAAAA=="
    print bytes_to_hex_string(base64.b64decode(template))
    print bytes_to_hex_string(base64.b64decode(feature))


