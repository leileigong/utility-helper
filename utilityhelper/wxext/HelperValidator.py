#coding:utf-8
'''
Created on 2016年6月25日

@author: Leo
'''

import string
import wx
from HelperToasterBox import ToasterBox

#----------------------------------------------------------------------

ALPHA_ONLY = 1
DIGIT_ONLY = 2

class MyValidator(wx.PyValidator):
    def __init__(self, flag=None, pyVar=None):
        wx.PyValidator.__init__(self)
        self.flag = flag
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        return MyValidator(self.flag)

    def Validate(self, win, *args, **kwargs):
        tc = self.GetWindow()
        val = tc.GetValue()
        ret = self.Validate_TC_Content(win)
        if(ret == False):
            return False
        
        if self.flag == ALPHA_ONLY:
            for x in val:
                if x not in string.letters:
                    return False

        elif self.flag == DIGIT_ONLY:
            for x in val:
                if x not in string.digits:
                    return False

        return True

    def Validate_TC_Content(self, win):
        """ Validate the contents of the given text control.
        """
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue()

        if len(text) == 0:
            tbox = ToasterBox.MakeText(win, u"请输入数据")
            tbox.Show()
            
            textCtrl.SetBackgroundColour("pink")
            textCtrl.SetFocus()
            textCtrl.Refresh()
            return False
        else:
            textCtrl.SetBackgroundColour(
                wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
            textCtrl.Refresh()
            return True

    def OnChar(self, event):
        key = event.GetKeyCode()
        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return

        if self.flag == ALPHA_ONLY and chr(key) in string.letters:
            event.Skip()
            return

        if self.flag == DIGIT_ONLY and chr(key) in string.digits:
            event.Skip()
            return

        if not wx.Validator_IsSilent():
            wx.Bell()

        # Returning without calling even.Skip eats the event before it
        # gets to the text control
        return

    def TransferToWindow(self):
        """ Transfer data from validator to window.

            The default implementation returns False, indicating that an error
            occurred.  We simply return True, as we don't do any data transfer.
        """
        return True # Dialog对象不会报警.


    def TransferFromWindow(self):
        """ Transfer data from window to validator.

            The default implementation returns False, indicating that an error
            occurred.  We simply return True, as we don't do any data transfer.
        """
        return True # Prevent wxDialog from complaining.
#----------------------------------------------------------------------


#----------------------------------------------------------------------
class TestValidateDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, "Validated Dialog")

        self.SetAutoLayout(True)
        VSPACE = 10

        fgs = wx.FlexGridSizer(cols=2)

        fgs.Add((1,1));
        fgs.Add(wx.StaticText(self, -1,
                             "These controls must have text entered into them.  Each\n"
                             "one has a validator that is checked when the Ok\n"
                             "button is clicked."))

        fgs.Add((1,VSPACE)); fgs.Add((1,VSPACE))

        label = wx.StaticText(self, -1, "First: ")
        fgs.Add(label, 0, wx.ALIGN_RIGHT|wx.CENTER)

        fgs.Add(wx.TextCtrl(self, -1, "", validator = MyValidator(ALPHA_ONLY)))

        fgs.Add((1,VSPACE)); fgs.Add((1,VSPACE))

        label = wx.StaticText(self, -1, "Second: ")
        fgs.Add(label, 0, wx.ALIGN_RIGHT|wx.CENTER)
        fgs.Add(wx.TextCtrl(self, -1, "", validator = MyValidator(ALPHA_ONLY)))


        buttons = wx.StdDialogButtonSizer() #wx.BoxSizer(wx.HORIZONTAL)
        b = wx.Button(self, wx.ID_OK, "OK")
        b.SetDefault()
        buttons.AddButton(b)
        buttons.AddButton(wx.Button(self, wx.ID_CANCEL, "Cancel"))
        buttons.Realize()

        border = wx.BoxSizer(wx.VERTICAL)
        border.Add(fgs, 1, wx.GROW|wx.ALL, 25)
        border.Add(buttons, 0, wx.GROW|wx.BOTTOM, 5)
        self.SetSizer(border)
        border.Fit(self)
        self.Layout()
        
class MyApp(wx.App):
    def OnInit(self):
        self.frame = TestValidateDialog(None)

        self.frame.Show()
        
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
