#coding:utf-8
import wx
import wx.grid
import myGridTable


############################################################
class myGrid(wx.grid.Grid):
    def __init__(self, parent, dataTable, dataTypes = [], rowLabels=None, colLabels=None):
        wx.grid.Grid.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        
        self.tableBase = myGridTable.GenericTable(dataTable, dataTypes, rowLabels, colLabels)
        
        self.SetTable(self.tableBase)
        
        #不显示行标题
        self.HideRowLabels()
        #self.SetRowLabelSize(0)
        
        #第一列设置为复选框
        self.SetColFormatBool(0) 
        
        #防止较宽列的数据重叠显示到附近的列
        self.SetDefaultCellOverflow(False)
        
        #行列宽度自适应 
        self.AutoSizeColumns(True)
        self.AutoSizeRows(True) 
        
        #表格单元格属性
        attr = wx.grid.GridCellAttr()
        attr.SetReadOnly(True)
        #除第一列外，表格不可编辑
        for i in range(1, len(dataTable[0])):
            self.SetColAttr(i, attr)  
        
        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick)
        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_DCLICK, self.OnLabelLeftDClick)

        self.Bind(wx.grid.EVT_GRID_RANGE_SELECT, self.OnRangeSelect)
        self.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.OnSelectCell)
         
    def OnLabelLeftClick(self, evt):
        print "OnCellLeftClick: (%d,%d) %s\n" %(evt.GetRow(), evt.GetCol(), evt.GetPosition())        
        evt.Skip() 
 
    def OnLabelLeftDClick(self, evt):
        '''双击标题全选
        evt.GetRow(), 选中的行编号:当单击列标题时，返回行号为-1，列号从0开始
        evt.GetCol(), 选中的列编号:当单击行标题时，返回列号为-1，行号从0开始
        evt.GetPosition(),相对于网格左上角的坐标,表示为(x,y)
        '''
        print ("OnLabelLeftDClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        
        allrows = self.GetNumberRows()
        for row in range(0, allrows):
            print "row(%d)=%s"%(row, self.GetCellValue(row, 0))            
            if(self.GetCellValue(row, 0) == '1'):
                self.SetCellValue(row, 0 , '0')     
            else:
                self.SetCellValue(row, 0 , '1')         
        evt.Skip()

    def OnRangeSelect(self, evt):
        if evt.Selecting():
            top = (evt.GetTopLeftCoords().GetRow(),evt.GetTopLeftCoords().GetCol())
            bottom = (evt.GetBottomRightCoords().GetRow(),evt.GetBottomRightCoords().GetCol())

            for row in range(top[0], bottom[0]):
#                 booleditor = wx.grid.GridCellBoolEditor()
#                 self.SetCellEditor(row, top[1], booleditor)
                
#                 render = wx.grid.GridCellBoolRenderer()
#                 self.SetCellRenderer(row, top[1], render)
                
                pass 
#                 print "(%d,%d)=%s, %s", row, top[1], self.GetCellValue(row, top[1]), type(self.GetCellValue(row, top[1]))            
#                 print "int()=", int(self.GetCellValue(row, top[1]))
#                 print "==", self.GetCellEditor(row, top[1])                               
#                 if(self.GetCellValue(row, top[1]) != '' and
#                     int(self.GetCellValue(row, top[1])) == 0):
#                     self.SetCellValue(row, 0 , '1')
#                 else:
#                     self.SetCellValue(row, 0, '0')
                              
        else:
            pass

        evt.Skip()

    def OnSelectCell(self, evt):
        if evt.Selecting():
            msg = 'Selected'
        else:
            msg = 'Deselected'
        print ("OnSelectCell: %s (%d,%d) %s\n" %
                       (msg, evt.GetRow(), evt.GetCol(), evt.GetPosition()))

        # Another way to stay in a cell that has a bad value...
        row = self.GetGridCursorRow()
        col = self.GetGridCursorCol()

        if self.IsCellEditControlEnabled():
            self.HideCellEditControl()
            self.DisableCellEditControl()

        value = self.GetCellValue(row, col)

        evt.Skip()
        
        self.tableBase.DeleteRows(1, 2)
#         def DeleteRows(self, pos=3, numRows=1):
#             print "DeleteRows"

############################################################    
#使用这通用的表来显示阵容
colLabels = ('Select', 'Last', 'First')
rowLabels = None
data = [[0, 'zhangsan', 26, 'man'],
        [0, 'lisi', 25, 'man']]
dataTypes = [wx.grid.GRID_VALUE_STRING,
             wx.grid.GRID_VALUE_STRING,
             wx.grid.GRID_VALUE_STRING]

class Frame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, 'A Grid',
        size=(275, 275))
        grid = myGrid(self, data, dataTypes, rowLabels, colLabels)
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = Frame(None)
    frame.Show(True)
    app.MainLoop()