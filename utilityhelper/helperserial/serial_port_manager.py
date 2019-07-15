#!/usr/bin/env python
# coding:utf-8
"""
# This is a wrapper module for module for pySerial by Liechti <cliechti@gmx.net>
#
# This file is part of pySerial. https://github.com/pyserial/pyserial
# by leo gong
#
"""
# 2017.09.17, gongleilei, pyserial 3.0之后的版本不兼容XP系统，增加对XP系统的兼容
import serial
from serial.tools import list_ports


class SerialPortManager(object):
    serialdevices = []
    ports_info = {}

    @staticmethod
    def find_port(vid=None, pid=None):
        ports_info = []
        # pyserial=2.7， comports得到的是一个comports函数生成器对象(<generator object comports at ...>),
        # pyserial>3.0， comports得到的是一个列表（内部把得到的iterate_comports函数生成器对象转成了列表）
        comports = list_ports.comports()
        portinfolist = [SerialPortManager.__update_port_info(comport) for comport in comports]

        if vid is None and pid is None:
            ports_info = [(portinfo['device'], portinfo['description']) for portinfo in portinfolist]
        elif vid is not None and pid is None:
            for portinfo in portinfolist:
                if portinfo['vid'] == vid:
                    ports_info.append((portinfo['device'], portinfo['description']))
        elif vid is None and pid is not None:
            for portinfo in portinfolist:
                if portinfo['pid'] == pid:
                    ports_info.append((portinfo['device'], portinfo['description']))
        else:
            for portinfo in portinfolist:
                if portinfo['vid'] == vid and portinfo['pid'] == pid:
                    ports_info.append((portinfo['device'], portinfo['description']))

        return ports_info

    @staticmethod
    def __update_port_info(comport):
        """
        device ,name ,description, hwid
        #USB specific data
        vid ,pid ,serial_number,location ,manufacturer,product ,interface

        :param comport:
        :return:
        """
        # pyserial=2.7， comports得到的是一个comports函数生成器对象(<generator object comports at ...>),
        # yield 返回的数据格式(port, description, szHardwareID_str)
        # port: 串口名称
        # description: 友好名称
        # szHardwareID_str: 设备实例路径的描述
        # 对于USB串口，u'USB\\VID_10C4&PID_EA60\\0001'==> 'USB VID:PID=10C4:EA60 SNR=0001'
        # 对于其他串口不做处理，原样输出。'ACPI\\PNP0501\\1' ==> 'ACPI\\PNP0501\\1'
        #
        # pyserial>3.0， comports得到的是一个列表（内部把得到的iterate_comports函数生成器对象转成了列表）,
        # 列表元素是ListPortInfo的实例对象。
        # 字段device : unicode编码的串口名称
        # 字段description: 友好名称（从注册表中读取PnP设备的属性）
        # 以下为从设备实例路径szHardwareID_str（如，u'USB\\VID_10C4&PID_EA60\\0001'）中解析出的信息
        # 字段vid: 2字节16进制整数，0x10C4
        # 字段pid: 2字节16进制整数, 0xEA60
        # 字段serial_number: u'0001'
        # bInterfaceNumber: 无
        # 字段location: 由位置路径和bInterfaceNumber得出。
        # 如位置路径：1-1.4；PCIROOT(0)#PCI(1D00)#USBROOT(0)#USB(1)#USB(4)，bInterfaceNumber为空
        # 字段hwid: 对于USB,FTDIBUS和其他设备分别处理
        # 字段manufacturer: 厂商
        portinfodic = {}

        # pyserial = 2.7
        if isinstance(comport, tuple):
            portinfodic['device'] = comport[0]
            portinfodic['description'] = comport[1]
            portinfodic['hwid'] = comport[2]
            if comport[2].startswith('USB'):
                portinfodic['vid'] = int(comport[2].split("=")[1].split(':')[0][:4], 16)
                portinfodic['pid'] = int(comport[2].split("=")[1].split(':')[1][:4], 16)
            else:
                portinfodic['vid'] = None
                portinfodic['pid'] = None
        else:  # pyserial >= 3.0
            portinfodic['device'] = comport.device
            portinfodic['description'] = comport.description
            portinfodic['hwid'] = comport.hwid
            portinfodic['vid'] = comport.vid
            portinfodic['pid'] = comport.pid
        return portinfodic

    @staticmethod
    def open_port(portname, baudrate=115200, bytesize=8, timeout=None):
        try:
            serialport = serial.Serial()
            serialport.port = portname
            serialport.baudrate = baudrate
            serialport.stopbits = 1
            serialport.parity = 'N'
            serialport.bytesize = bytesize
            serialport.xonxoff = 0
            serialport.rtscts = 0
            serialport.timeout = timeout
            serialport.open()
            return serialport
        except serial.serialutil.SerialException as serialexp:
            errmesglist = str(serialexp).split(":")
            if len(errmesglist) == 2:
                obj = eval(errmesglist[1])
                if isinstance(obj, WindowsError):
                    winerrmsg = str(obj).decode('gbk').encode('utf8')
                    raise Exception("{}({})".format(errmesglist[0], winerrmsg))
            raise Exception(errmesglist[0])
        except Exception as e:
            raise e

    @staticmethod
    def close_port(serialport):
        if not isinstance(serialport, serial.Serial):
            return
        serialport.close()

    @staticmethod
    def send_to_port(serialport, bytestring):
        if not isinstance(serialport, serial.Serial):
            return
        serialport.write(bytestring)

    @staticmethod
    def read_from_port(serialport, size=1):
        if not isinstance(serialport, serial.Serial):
            return
        text = serialport.read(size)  # read one, with timout
        return text

    @staticmethod
    def read_set_timeout(serialport, timeout):
        """设置接收超时时间
        :param serialport:
        :param timeout:None-阻塞模式，其他情况：整数或浮点数
        :return:
        """
        serialport.timeout = timeout


if __name__ == "__main__":
    import ABCodeUtil
    from utilityhelper.loggingHelper import *  # @UnusedWildImport

    __fmt = '【%(levelname)s】 - %(asctime)s - %(name)s - %(process)d - %(thread)d -%(threadName)s - %(message)s'
    _g_logger = LogManger.getLogger(None, LEVEL_DEBUG)
    LogManger.addHandler((_g_logger,), HANDLER_TYPE_STREAM, LEVEL_DEBUG, __fmt)
    portlist = SerialPortManager.find_port()
    print("portlist=", portlist)
    serialport = SerialPortManager.open_port('COM5')
    _g_logger.debug("serialport=%s" % serialport)

    SerialPortManager.send_to_port(serialport, "\x01\x27\x00")
    _g_logger.debug("inwaiting=%d" % serialport.in_waiting)
    evt_op_len = SerialPortManager.read_from_port(serialport, 3)
    _g_logger.debug("event=%s" % ABCodeUtil.StringToHex(evt_op_len))
    if evt_op_len[0] == '\x02' and evt_op_len[1] == '\x06':
        _g_logger.debug("inwaiting=%d" % serialport.in_waiting)
        payload = SerialPortManager.read_from_port(serialport, ord(evt_op_len[2]))
        _g_logger.debug("pyload=%s" % ABCodeUtil.StringToHex(payload))
        if len(payload) >= 2:
            if payload[1] != '\x00':
                pass

    _g_logger.debug("connect.........")
    SerialPortManager.send_to_port(serialport, "\x01\x26\x06\x2F\xF7\x82\xE2\xB2\x4E")
    _g_logger.debug("inwaiting=%d" % serialport.in_waiting)
    evt_op_len = SerialPortManager.read_from_port(serialport, 3)
    _g_logger.debug("event=%s" % ABCodeUtil.StringToHex(evt_op_len))
    if evt_op_len[0] == '\x02' and evt_op_len[1] == '\x06':
        _g_logger.debug("inwaiting=%d" % serialport.in_waiting)
        payload = SerialPortManager.read_from_port(serialport, ord(evt_op_len[2]))
        _g_logger.debug("pyload=%s" % ABCodeUtil.StringToHex(payload))
        if len(payload) >= 2:
            if payload[1] != '\x00':
                pass
            else:
                _g_logger.debug("inwaiting=%d" % serialport.in_waiting)
                evt_op_len = SerialPortManager.read_from_port(serialport, 3)
                _g_logger.debug("pyload=%s" % ABCodeUtil.StringToHex(evt_op_len))

    _g_logger.debug("senddata.........")
    SerialPortManager.send_to_port(serialport, "\x01\x09\x0c\x2d\x00\x5a\x5b\x00\x00\x00\x00\x01\x02\x03\x04")
    _g_logger.debug("inwaiting=%d" % serialport.in_waiting)
    evt_op_len = SerialPortManager.read_from_port(serialport, 3)
    _g_logger.debug("event=%s" % ABCodeUtil.StringToHex(evt_op_len))
    if evt_op_len[0] == '\x02' and evt_op_len[1] == '\x06':
        _g_logger.debug("inwaiting=%d" % serialport.in_waiting)
        payload = SerialPortManager.read_from_port(serialport, ord(evt_op_len[2]))
        _g_logger.debug("pyload=%s" % ABCodeUtil.StringToHex(payload))
        if len(payload) >= 2:
            if payload[1] != '\x00':
                pass
            else:
                _g_logger.debug("inwaiting=%d" % serialport.in_waiting)
                evt_op_len = SerialPortManager.read_from_port(serialport, 3)
                _g_logger.debug("evt_op_len=%s" % ABCodeUtil.StringToHex(evt_op_len))
                if evt_op_len[0] == '\x02' and evt_op_len[1] == '\x08':
                    _g_logger.debug("inwaiting=%d" % serialport.in_waiting)
                    payload = SerialPortManager.read_from_port(serialport, ord(evt_op_len[2]))
                    _g_logger.debug("pyload=%s" % ABCodeUtil.StringToHex(payload))

    _g_logger.debug("disconnect.........")
    SerialPortManager.send_to_port(serialport, "\x01\x12\x00")
    _g_logger.debug("inwaiting=%d" % serialport.in_waiting)
    evt_op_len = SerialPortManager.read_from_port(serialport, 3)
    _g_logger.debug("event=%s" % ABCodeUtil.StringToHex(evt_op_len))
    if evt_op_len[0] == '\x02' and evt_op_len[1] == '\x06':
        _g_logger.debug("inwaiting=%d" % serialport.in_waiting)
        payload = SerialPortManager.read_from_port(serialport, ord(evt_op_len[2]))
        _g_logger.debug("pyload=%s" % ABCodeUtil.StringToHex(payload))
        if len(payload) >= 2:
            if payload[1] != '\x00':
                pass
            else:
                _g_logger.debug("inwaiting=%d" % serialport.in_waiting)
                evt_op_len = SerialPortManager.read_from_port(serialport, 3)
                _g_logger.debug("evt_op_len=%s" % ABCodeUtil.StringToHex(evt_op_len))
