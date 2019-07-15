#coding:utf-8

import crc16
import struct
from utilityhelper.util import ascbin
from .serial_port_manager import SerialPortManager


def listports():
    serialReaderlist = []
    ports_info = SerialPortManager.find_port()
    # serialReaderlist.append(serialReader('COM4'))
    for port in ports_info:
        serialReaderlist.append(serialReader(port[0]))
    return serialReaderlist


class serialReader(object):
    def __init__(self, port):
        """Constructs a new reader and store port."""
        self.port = port

    def createConnection(self):
        return SerialConnection(self.port)

    def __str__(self):
        return self.port

    def __repr__(self):
        return self.port


class SerialConnection(object):
    def __init__(self, port, baudrate=115200, bytesize=8, timeout=30):
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.timeout = timeout
        self.serialport = None

    def connect(self):
        self.serialport = SerialPortManager.open_port(self.port, self.baudrate, self.bytesize, timeout=self.timeout)

    def disconnect(self):
        SerialPortManager.close_port(self.serialport)

    def transmit(self, data):
        data = ascbin.int_list_to_string(data)
        package = chr(0x5A)
        package += chr(0x5B)
        payloadlen = len(data) + 2  # data + crc
        prototype = 8  # b'1000'
        package += struct.pack("H", (prototype << 12) + payloadlen)
        package += data
        cal_crc = crc16.crc16xmodem(package)
        package += struct.pack("H", cal_crc)
        # print "write=", ascbin.StringToHex(package)
        self.serialport.write(package)
        resppkgheader = self.serialport.read(4)
        if not resppkgheader:
            raise Exception("serial read time out")
        # print "read header=", ascbin.StringToHex(resppkgheader)
        if resppkgheader and len(resppkgheader) == 4 and resppkgheader[0] == chr(0x5B):
            result = resppkgheader[1]
            data = struct.unpack("H", resppkgheader[2:4])[0]
            prototype = data >> 12
            payloadlen = data & 0x0FFF
            # print "calc proto=", hex(prototype)
            # print "calc payloadlen=", payloadlen
            payload = self.serialport.read(payloadlen)
            if not payload:
                raise Exception("serial read time out")
            # print "read payload=", ascbin.StringToHex(payload)
            if payloadlen >= 4:
                sw1 = ord(payload[-4:-3])
                sw2 = ord(payload[-3:-2])
                data = payload[:-4]
                rcv_crc = struct.unpack("H", payload[-2:])[0]
                cal_crc = crc16.crc16xmodem(resppkgheader + payload[:-2])
                if rcv_crc == cal_crc:
                    data = map(lambda x: (ord(x) + 256) % 256, data)
                    return data, sw1, sw2