#coding:utf-8
'''
Created on 2016年6月29日

@author: Leo
'''
import wx
import wx.lib.buttons  as  buttons
import wx.lib.agw.aquabutton as agwAquabutton
import wx.lib.agw.shapedbutton as agwShapedbutton

class extGenBitmapToggleButton(buttons.GenBitmapToggleButton):
    def __init__(self, parent, objid=-1, bmp1=wx.NullBitmap, bmp2=wx.NullBitmap, tgl=False):
        buttons.GenBitmapToggleButton.__init__(self, parent, objid, bmp1)
        self.SetBitmapLabel(bmp1)
        self.SetBitmapSelected(bmp2)
        self.SetToggle(tgl)
        self.SetInitialSize()

class extSBBitmapToggleButton(agwShapedbutton.SBitmapToggleButton):
    def __init__(self, parent, objid=-1, bmp1=wx.NullBitmap, bmp2=wx.NullBitmap, tgl=False):
        agwShapedbutton.SBitmapToggleButton.__init__(self, parent, objid, bmp1)
        #self.SetBitmapLabel(bmp1)
        self.SetBitmapSelected(bmp2)
        self.SetToggle(tgl)
        self.SetUseFocusIndicator(True)
        #self.SetInitialSize()
