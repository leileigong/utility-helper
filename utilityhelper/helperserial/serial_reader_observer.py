#coding:utf-8

import time
from threading import Thread, Event
from utilityhelper.util.Observer import *
from utilityhelper.common import HelperDecorator
from utilityhelper.helperserial.serial_port_manager import *

_START_ON_DEMAND_ = False


@HelperDecorator.singleton
class SerialReaderMonitor(Observable):
    """"""
    def __init__(self):
        Observable.__init__(self)
        if _START_ON_DEMAND_:
            self.rmthread = None
        else:
            self.rmthread = _SerialReaderMonitoringThread(self)
            self.rmthread.start()

    def addObserver(self, observer):
        Observable.addObserver(self, observer)
        if _START_ON_DEMAND_:
            if self.countObservers() > 0 and self.rmthread is None:
                self.rmthread = _SerialReaderMonitoringThread(self)
                self.rmthread.start()
        else:
            if self.rmthread.devs:
                observer.update(self, (self.rmthread.devs, []))

    def deleteObserver(self, observer):
        """Remove an observer.

        We delete the _BLESerialDevMonitoringThread reference when there
        are no more observers.
        """
        Observable.deleteObserver(self, observer)
        if _START_ON_DEMAND_:
            if self.countObservers() == 0:
                if self.rmthread is not None:
                    self.rmthread = None

@HelperDecorator.singleton
class _SerialReaderMonitoringThread(Thread):
    """Card insertion thread.
    This thread waits for card insertion.
    """
    def __init__(self, observable):
        Thread.__init__(self)
        self.observable = observable
        self.stopEvent = Event()
        self.stopEvent.clear()
        self.devs = []
        self.setDaemon(True)

    # the actual monitoring thread
    def run(self):
        while self.stopEvent.isSet() != 1:
            time.sleep(0.5)
            try:
                currentdevs = SerialPortManager.find_port()

                addeddevs = []
                for dev in currentdevs:
                    if not self.devs.__contains__(dev):
                        addeddevs.append(dev)

                removeddevs = []
                for dev in self.devs:
                    if not currentdevs.__contains__(dev):
                        removeddevs.append(dev)

                if addeddevs != [] or removeddevs != []:
                    self.devs = currentdevs
                    self.observable.setChanged()
                    self.observable.notifyObservers((addeddevs, removeddevs))
            except TypeError:
                    pass
            except AttributeError:
                    pass
            except Exception as e:
                pass

    # stop the thread by signaling stopEvent
    def stop(self):
        self.stopEvent.set()


class SerialReaderObserver(Observer):
    """串口读卡器设备检测"""

    def __init__(self, observable, callback):
        """实例化观察者
        :param observable:被观察对象
        :param callback: 观察者注册的事件回调方法，当方法中有UI操作时的，必须使用异步调用，用相应的跨线程处理机制包装。
                          1）wxpython，使用wx.CallAfter方法包装；
                          2）pyqt，使用QMetaObject.invokeMethod方法包装
        """
        self.callback = callback
        self.observable = observable
        # 新建观察者默认添加到被观察者维护的队列中
        observable.addObserver(self)

    def update(self, observable, args):
        plugins, plugouts = args
        self.callback(plugins, plugouts)

