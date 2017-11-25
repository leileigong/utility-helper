#coding:utf-8
import string
import wx

class TreeCtrlPanel(wx.Panel):
    def __init__(self, parent, log):
        # Use the WANTS_CHARS style so the panel doesn't eat the Return key.
        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS)
        self.log = log
        self.tree = wx.TreeCtrl(self, wx.ALL, wx.DefaultPosition, wx.DefaultSize,
                               wx.TR_HAS_BUTTONS
                               | wx.TR_EDIT_LABELS
                               #| wx.TR_MULTIPLE
                               #| wx.TR_HIDE_ROOT
                               )
        self.root = None

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded, self.tree)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed, self.tree)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.tree)
        self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.OnBeginEdit, self.tree)
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnEndEdit, self.tree)
        # self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivate, self.tree)

        self.tree.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        self.tree.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.tree.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)

    def AddTreeRoot(self, strname, pydata=None, imagenorm=None, imageExp=None, imageSel=None):
        # NOTE:  For some reason tree items have to have a data object in
        #        order to be sorted.  Since our compare just uses the labels
        #        we don't need any real data, so we'll just use None below for
        #        the item data.
        self.root = self.tree.AddRoot(strname)
        self.tree.SetPyData(self.root, pydata)
        if imagenorm:
            self.tree.SetItemImage(self.root, imagenorm, wx.TreeItemIcon_Normal)
        if imageExp:
            self.tree.SetItemImage(self.root, imageExp, wx.TreeItemIcon_Expanded)
        if imageSel:
            self.tree.SetItemImage(self.root, imageSel, wx.TreeItemIcon_Selected)

    def AddChildNode(self, strparent, strname, pydata=None, imagenorm=None, imageExp=None):
        print "************search [", strparent, "] from root!!!!"
        item = self.SearchChildNode(self.root, strparent)
        if item is None:
            print "FIND NONE----------append----", strname, "into "
            # self.tree.AppendItem(self.root, strname)
        else:
            print "FIND OK----------append----", strname, "into "
            self.tree.AppendItem(item, strname)
            self.tree.SetPyData(item, pydata)

    def SearchChildNode(self, parent, strname):
        """先序遍历从指定的节点下查找标签值为strname的节点
        SearchChildNode(self, TreeItemId parent, String strname) -> TreeItemId
        :param parent:
        :param strname:
        :return:
        """
        if parent is None:
            return None
        # 根
        label = self.tree.GetItemText(parent)
        print "FIND root lab=", label
        if label == strname:
            print "========return label [%s] from root %s"%(label, parent)
            return parent

        childrenCounts = self.tree.GetChildrenCount(parent, False)
        print "********************************************************childrenCounts", childrenCounts

        childindex = 0
        if childrenCounts > 0:
            childindex += 1
            item, cookie = self.tree.GetFirstChild(parent)
            print "Get first Child label=", self.tree.GetItemText(item)
            child = self.SearchChildNode(item, strname)
            if child:
                return child
            else:
                while childindex < childrenCounts:
                    childindex += 1
                    item, cookie = self.tree.GetNextChild(parent, cookie)
                    print "Get Next Child label=", self.tree.GetItemText(item)
                    child = self.SearchChildNode(item, strname)
                    if child:
                        return child
        else:
            return None

    def EnabeTreeImageList(self, imageList):
        self.tree.SetImageList(imageList)

    def OnRightDown(self, event):
        pt = event.GetPosition();
        item, flags = self.tree.HitTest(pt)
        if item:
            self.log.WriteText("OnRightClick: %s, %s, %s\n" %
                               (self.tree.GetItemText(item), type(item), item.__class__))
            self.tree.SelectItem(item)

    def OnRightUp(self, event):
        pt = event.GetPosition();
        item, flags = self.tree.HitTest(pt)
        if item:
            self.log.WriteText("OnRightUp: %s (manually starting label edit)\n"
                               % self.tree.GetItemText(item))
            self.tree.EditLabel(item)

    def OnBeginEdit(self, event):
        self.log.WriteText("OnBeginEdit\n")
        # show how to prevent edit...
        item = event.GetItem()
        if item and self.tree.GetItemText(item) == "The Root Item":
            wx.Bell()
            self.log.WriteText("You can't edit this one...\n")

            # Lets just see what's visible of its children
            cookie = 0
            root = event.GetItem()
            (child, cookie) = self.tree.GetFirstChild(root)

            while child.IsOk():
                self.log.WriteText("Child [%s] visible = %d" %
                                   (self.tree.GetItemText(child),
                                    self.tree.IsVisible(child)))
                (child, cookie) = self.tree.GetNextChild(root, cookie)

            event.Veto()

    def OnEndEdit(self, event):
        self.log.WriteText("OnEndEdit: %s %s\n" %
                           (event.IsEditCancelled(), event.GetLabel()) )
        # show how to reject edit, we'll not allow any digits
        for x in event.GetLabel():
            if x in string.digits:
                self.log.WriteText("You can't enter digits...\n")
                event.Veto()
                return

    def OnLeftDClick(self, event):
        pt = event.GetPosition();
        item, flags = self.tree.HitTest(pt)
        if item:
            self.log.WriteText("OnLeftDClick: %s\n" % self.tree.GetItemText(item))
            parent = self.tree.GetItemParent(item)
            if parent.IsOk():
                self.tree.SortChildren(parent)
        event.Skip()
        pass

    def OnSize(self, event):
        w,h = self.GetClientSizeTuple()
        self.tree.SetDimensions(0, 0, w, h)

    def OnItemExpanded(self, event):
        item = event.GetItem()
        if item:
            self.log.WriteText("OnItemExpanded: %s\n" % self.tree.GetItemText(item))

    def OnItemCollapsed(self, event):
        pass
        item = event.GetItem()
        if item:
            self.log.WriteText("OnItemCollapsed: %s\n" % self.tree.GetItemText(item))

    def OnSelChanged(self, event):
        self.item = event.GetItem()
        if self.item:
            self.log.WriteText("OnSelChanged: %s\n" % self.tree.GetItemText(self.item))
            if wx.Platform == '__WXMSW__':
                self.log.WriteText("BoundingRect: %s\n" %
                                   self.tree.GetBoundingRect(self.item, True))
            #items = self.tree.GetSelections()
            #print map(self.tree.GetItemText, items)
        event.Skip()

    def OnActivate(self, event):
        pass
        if self.item:
            self.log.WriteText("OnActivate: %s\n" % self.tree.GetItemText(self.item))


#####################################################################
# test demo
class Example(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        bSizer1.Add(bSizer2, 1, wx.EXPAND, 5)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        self.log = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        bSizer3.Add(self.log, 1, wx.ALL | wx.EXPAND, 5)

        self.pnl = TreeCtrlPanel(self, self.log)
        bSizer2.Add(self.pnl, 1, wx.ALL | wx.EXPAND, 5)
        #####################################
        isz = (16, 16)
        il = wx.ImageList(isz[0], isz[1])
        fldridx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, isz))
        fldropenidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, isz))
        fileidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))
        selidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))

        self.pnl.EnabeTreeImageList(il)
        self.pnl.AddTreeRoot("The Root Item", None, fldridx, fldropenidx, fileidx)
        self.pnl.tree.SetItemImage(self.pnl.root, fldridx, wx.TreeItemIcon_Normal)
        self.pnl.tree.SetItemImage(self.pnl.root, fldropenidx, wx.TreeItemIcon_Expanded)
        self.pnl.tree.SetItemImage(self.pnl.root, selidx, wx.TreeItemIcon_SelectedExpanded)

        self.pnl.AddChildNode("The Root Item", 'a')
        self.pnl.AddChildNode('a', 'aa')
        self.pnl.AddChildNode("The Root Item", 'b')
        self.pnl.AddChildNode('b', 'bb')
        self.pnl.AddChildNode("The Root Item", 'c')
        self.pnl.AddChildNode('bb', 'bbb')
        self.pnl.AddChildNode('b', 'bb2')
        self.pnl.AddChildNode('bbb', 'bbbb')
        self.pnl.AddChildNode("aa", 'aaa')
        self.pnl.AddChildNode("aaa", 'aaaa')
        self.pnl.AddChildNode("The Root Item", 'd')
        self.pnl.AddChildNode("e", 'ee')
        self.pnl.tree.Expand(self.pnl.root)
        #####################################

        bSizer1.Add(bSizer3, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        self.Show(True)

    def __del__(self):
        pass

def main():
    ex = wx.App()
    Example(None)
    ex.MainLoop()

if __name__ == '__main__':
    main()