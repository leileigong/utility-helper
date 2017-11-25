#-*- coding:utf-8 -*-
'''
helper.HelperPieCtrl
~~~~~~~~~~~~~~~~~~~~~~~~~
控制饼状图操作

使用方法：
    #创建饼状图
    self._pie = PieGraph(self, 50, -1, wx.DefaultPosition, wx.Size(180,270))
    self._pie.SetLegend()
    self._pie.AddPiePart("l1", 1, wx.Colour(200, 50, 50))
    self._pie.AddPiePart("l2", 1, wx.Colour( 50, 200, 50))
    self._pie.AddPiePart("l3", 1, wx.Colour( 50, 50, 200))

Created on 2016年7月7日

@author: 龚磊磊
'''

from math import pi
try:
    import agw.piectrl
    from agw.piectrl import PieCtrl, ProgressPie, PiePart
    docs = agw.piectrl.__doc__
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.piectrl
    from wx.lib.agw.piectrl import PieCtrl, ProgressPie, PiePart
    docs = wx.lib.agw.piectrl.__doc__
    
class MyTimer(wx.Timer):


    def __init__(self, parent):

        wx.Timer.__init__(self)
        self._parent = parent
        

    def Notify(self):
        
        if self._parent._progresspie.GetValue() <= 0:
            self._parent._incr = 1

        if self._parent._progresspie.GetValue() >= self._parent._progresspie.GetMaxValue():
            self._parent._incr = -1

        self._parent._progresspie.SetValue(self._parent._progresspie.GetValue() + self._parent._incr)
        self._parent._progresspie.Refresh()

class ProgressPie(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        # Create A ProgressPie
        self._progresspie = ProgressPie(self, 100, 50, -1, wx.DefaultPosition,
                                        wx.Size(180, 200), wx.SIMPLE_BORDER)
        
        self._progresspie.SetBackColour(wx.Colour(150, 200, 255))
        self._progresspie.SetFilledColour(wx.Colour(255, 0, 0))
        self._progresspie.SetUnfilledColour(wx.WHITE)
        self._progresspie.SetHeight(20)

#
class PieGraph(PieCtrl):
    '''初始化饼状图，设置饼状图的参数
    '''
    def __init__(self, parent, height, ctrlid = -1, pos = wx.DefaultPosition,
                  size=wx.DefaultSize, style=0, name="PieCtrl"):
        PieCtrl.__init__(self, parent, ctrlid, pos, size, style, name)
        self.SetHeight(height)
        # Create A Simple PieCtrl With 3 Sectors
        #self._pie = PieCtrl(self, -1, wx.DefaultPosition, wx.Size(180,270))
    
    def SetLegend(self, transparent = True, 
                        hborder = 5,
                        winstyle = wx.STATIC_BORDER,
                        labelFont = None,
                        labelCol = None):
        
        self.GetLegend().SetTransparent(transparent)
        self.GetLegend().SetHorizontalBorder(hborder)
        self.GetLegend().SetWindowStyle(winstyle)
        if not labelFont:
            labelFont =  wx.Font(10, wx.FONTFAMILY_DEFAULT,
                               wx.FONTSTYLE_NORMAL,
                               wx.FONTWEIGHT_NORMAL,
                               False, "Courier New")
        self.GetLegend().SetLabelFont(labelFont)
        
        if not labelCol:
            labelCol = wx.Colour(0, 0, 127)
        self.GetLegend().SetLabelColour(labelCol)

    def AddPiePart(self, label, value, colour):
        '''添加一块Pie饼
        @param label: 标签
        @param value: 
        @param colour: 
        wx.Colour(200, 50, 50), (50, 200, 50), (50, 50, 200)
        '''
        part = PiePart()
        
        part.SetLabel(label)
        part.SetValue(value)
        part.SetColour(colour)
        self._series.append(part)

    def SeteTransparency(self, value = True):

        self.GetLegend().SetTransparent(value)
        self.Refresh()


    def SetShowableEdges(self, value = True):

        self.SetShowEdges(value)

    def SetShowableLegend(self, value = True):
        
        if not value:
            self.GetLegend().Hide()
        else:
            self.GetLegend().Show()

        self.Refresh()
        
        
    def SetSlider(self, angle):

        self.SetAngle(float(angle)/180.0*pi)

    def SetAngleSlider(self, angle):

        self.SetRotationAngle(float(angle)/180.0*pi)
#
class PieCtrlPanel(wx.Panel):
    '''在一个panel中显示的饼状图
    '''
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self._hiddenlegend = False
        
        self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_BTNFACE))

        #创建饼状图
        self._pie = PieGraph(self, 50, -1, wx.DefaultPosition, wx.Size(180,270))
        self._pie.SetLegend()
        self._pie.AddPiePart("l1", 1, wx.Colour(200, 50, 50))
        self._pie.AddPiePart("l2", 1, wx.Colour( 50, 200, 50))
        self._pie.AddPiePart("l3", 1, wx.Colour( 50, 50, 200))
        
        cb1 = wx.CheckBox(self, -1, u"图例透明")
        cb1.SetValue(True)
        cb2 = wx.CheckBox(self, -1, "显示边缘")
        cb3 = wx.CheckBox(self, -1, "图例隐藏")
        
        #垂直滑动条，控制上下旋转角度
        self._slider = wx.Slider(self, -1, 25, 0, 90, wx.DefaultPosition, wx.DefaultSize, wx.SL_VERTICAL | wx.SL_LABELS)
        #水平角度滑动条，控制左右旋转角度
        self._angleslider = wx.Slider(self, -1, 200, 0, 360, wx.DefaultPosition, wx.DefaultSize, wx.SL_LABELS | wx.SL_TOP)
        sizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        
        #复选框布局器
        cbsizer = wx.BoxSizer(wx.HORIZONTAL)

        cbsizer.AddMany([cb1, cb2, cb3])
        hsizer.Add(self._pie, 1, wx.EXPAND | wx.ALL, 5)
        hsizer.Add(self._slider, 0, wx.GROW | wx.ALL, 5)
        
        vsizer.Add(self._angleslider, 0, wx.GROW | wx.ALL, 5)
 
        sizer.Add(cbsizer, 1, wx.EXPAND | wx.ALL, 1)
        sizer.Add(hsizer, 1, wx.EXPAND | wx.ALL, 1)
        sizer.Add(vsizer, 1, wx.EXPAND | wx.ALL, 1)
        
        self.SetSizer(sizer)
        sizer.Layout()

        self._slider.Bind(wx.EVT_SLIDER, self.OnSlider)
        self._angleslider.Bind(wx.EVT_SLIDER, self.OnAngleSlider)
        cb1.Bind(wx.EVT_CHECKBOX, self.OnToggleTransparency)
        cb2.Bind(wx.EVT_CHECKBOX, self.OnToggleEdges)
        cb3.Bind(wx.EVT_CHECKBOX, self.OnToggleLegend)

        self.OnAngleSlider(None)
        self.OnSlider(None)


    def OnToggleTransparency(self, event):

        self._pie.GetLegend().SetTransparent(not self._pie.GetLegend().IsTransparent())
        self._pie.Refresh()


    def OnToggleEdges(self, event):

        self._pie.SetShowEdges(not self._pie.GetShowEdges())

    def OnToggleLegend(self, event):

        self._hiddenlegend = not self._hiddenlegend
        
        if self._hiddenlegend:
            self._pie.GetLegend().Hide()
        else:
            self._pie.GetLegend().Show()

        self._pie.Refresh()
        
        
    def OnSlider(self, event):

        self._pie.SetAngle(float(self._slider.GetValue())/180.0*pi)

    def OnAngleSlider(self, event):

        self._pie.SetRotationAngle(float(self._angleslider.GetValue())/180.0*pi)

##############################################################
#test
if __name__ == '__main__':
    class MyApp(wx.App):
        def OnInit(self):
            self.frame = Frame(None)
            self.SetTopWindow(self.frame)
            self.frame.Show()
            
            return True
    
    class Frame(wx.Frame):
        def __init__(self, parent):
            wx.Frame.__init__(self, parent)
            pnl = PieCtrlPanel(self)
            self.Show()
            
    app = MyApp()
    app.MainLoop()
