#coding:utf-8
#一个关于二维列表的通用的表
'''
GenericTable类要求一个数据的二维列表和一个可选的行和列标签列表。这
个类适合被导入任何wxPython程序中。使用一个做了微小改变的格式.
'''
import wx
import wx.grid

class GenericTable(wx.grid.GridTableBase):
    def __init__(self, data, colDataTypes= [], rowLabels=None, colLabels=None, onGridValueChanged=None):
        wx.grid.GridTableBase.__init__(self)
        self.data = data
        self.dataTypes = []
        if(colDataTypes == []):
            for i in range(len(self.data[0])):
                self.dataTypes.append(wx.grid.GRID_VALUE_STRING) 
        else:
            self.dataTypes = colDataTypes
            for i in range(len(self.data[0]) - len(colDataTypes)):
                self.dataTypes.append(wx.grid.GRID_VALUE_STRING)
        self.rowLabels = rowLabels
        self.colLabels = colLabels
        self.isModified = False
        self.onGridValueChanged = onGridValueChanged
    
    #---------------------------------------------------------------------
    '''    
    five required methods for the wxPyGridTableBase interface 
    '''  
    def GetNumberRows(self):
        if self.data is None:
            return 0
        return len(self.data)
    

    def GetNumberCols(self):
        """"""
        if self.colLabels is None or len(self.colLabels) == 0:
            return 0
        return len(self.data[0])
    
    def IsEmptyCell(self, row, col):
        try:
            return not self.data[row][col]
        except IndexError:
            return True
    
    '''Get/Set values in the table.  The Python version of these
    methods can handle any data-type, (as long as the Editor and
    Renderer understands the type too,) not just strings as in the
    C++ version.'''
    def GetValue(self, row, col):
        try:
            return self.data[row][col]
        except IndexError:
            return ''
            
    def SetValue(self, row, col, value):
        def innerSetValue(row, col, value):
            try:
                self.data[row][col] = value
                self.isModified = True
                if self.onGridValueChanged:
                    self.onGridValueChanged()
            except IndexError:
                # add a new row
                self.data.append([''] * self.GetNumberCols())
                innerSetValue(row, col, value)
                # tell the grid we've added a row
                msg = wx.grid.GridTableMessage(self,            # The table
                        wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED, # what we did to it
                        1                                       # how many
                        )
                self.GetView().ProcessTableMessage(msg)
        innerSetValue(row, col, value) 
        
#----------------------------------------------------------------------
# Some optional methods
    def GetColLabelValue(self, col):
        '''Called when the grid needs to display labels'''
        if self.colLabels:
            return self.colLabels[col]
    
    def GetRowLabelValue(self, row):
        if self.rowLabels:
            return self.rowLabels[row]
            
    # Called to determine the kind of editor/renderer to use by
    # default, doesn't necessarily have to be the same type used
    # natively by the editor/renderer if they know how to convert.
    def GetTypeName(self, row, col):
        if self.dataTypes:
            return self.dataTypes[col]
    
    # Called to determine how the data can be fetched and stored by the
    # editor and renderer.  This allows you to enforce some type-safety
    # in the grid.
    def CanGetValueAs(self, row, col, typeName):
        colType = self.dataTypes[col].split(':')[0]
        if typeName == colType:
            return True
        else:
            return False
        
    def CanSetValueAs(self, row, col, typeName):
        return self.CanGetValueAs(row, col, typeName)
    
    def InsertRows(self,pos=1,numRows=1):
        """"""
        for num in range(0,numRows):
            newData={};
            newData['lable'] = ''     
            self.data.insert(pos,newData)
            
        self.isModified = True
        gridView = self.GetView()
        gridView.BeginBatch()
        insertMsg = wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_NOTIFY_ROWS_INSERTED,pos,numRows)
        gridView.ProcessTableMessage(insertMsg)
        gridView.EndBatch()
        getValueMsg = wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
        gridView.ProcessTableMessage(getValueMsg)        
        
        if self.onGridValueChanged:
            self.onGridValueChanged()        
        return True
   
    def AppendRows(self,numRows=1):
        """"""
        for num in range(0,numRows):
            newData={};
            newData['lable'] = ''         
            self.data.append(newData)
        self.isModified = True
        gridView = self.GetView()
        gridView.BeginBatch()
        appendMsg = wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED,numRows)
        gridView.ProcessTableMessage(appendMsg)
        gridView.EndBatch()
        getValueMsg = wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
        gridView.ProcessTableMessage(getValueMsg)
        
        if self.onGridValueChanged:
            self.onGridValueChanged()  
            
        return True
    
    def DeleteRows(self,pos=0,numRows=1):
        if self.data is None or len(self.data) == 0:
            return False
        for rowNum in range(0, numRows):
            self.data.remove(self.data[pos+rowNum -1])

        gridView = self.GetView()
        gridView.BeginBatch()
        deleteMsg = wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED,pos,numRows)
        gridView.ProcessTableMessage(deleteMsg)
        gridView.EndBatch()
        getValueMsg = wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
        gridView.ProcessTableMessage(getValueMsg)
  
        if self.onGridValueChanged:
            self.onGridValueChanged()
            
        return True    

