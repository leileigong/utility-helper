#! python
#
# Python Serial Port Extension for Win32, Linux, BSD, Jython
# see __init__.py
#
# This module implements a special URL handler that uses the port listing to
# find ports by searching the string descriptions.
#
# (C) 2011 Chris Liechti <cliechti@gmx.net>
# this is distributed under a free software license, see license.txt
#
# URL format:    hwgrep://regexp

import serial27
import serial27.tools.list_ports

class Serial(serial27.Serial):
    """Just inherit the native Serial port implementation and patch the open function."""

    def setPort(self, value):
        """translate port name before storing it"""
        if isinstance(value, str) and value.startswith('hwgrep://'):
            serial27.Serial.setPort(self, self.fromURL(value))
        else:
            serial27.Serial.setPort(self, value)

    def fromURL(self, url):
        """extract host and port from an URL string"""
        if url.lower().startswith("hwgrep://"): url = url[9:]
        # use a for loop to get the 1st element from the generator
        for port, desc, hwid in serial27.tools.list_ports.grep(url):
            return port
        else:
            raise serial27.SerialException('no ports found matching regexp %r' % (url,))

    # override property
    port = property(serial27.Serial.getPort, setPort, doc="Port setting")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == '__main__':
    #~ s = Serial('hwgrep://ttyS0')
    s = Serial(None)
    s.port = 'hwgrep://ttyS0'
    print(s)

