import wx
from BlockWindow import BlockWindow


# This is the class for the main window of the Colormapper App        
class ColormapperFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Colormapper", size = (800, 600))
        self.SetMinSize((800,600))

        # High-level application data
        self.imageFilename = ""
        self.filename = ""

        # Attributes 
        statusBar = self.createStatusBar()
        menuBar = self.createMenuBar()
        self.createMainInterfaceWindow()
        
        
    def createMainInterfaceWindow(self):
        # Create sub panels
        inputImagePanel = BlockWindow(self, label = "Input Image: " + self.imageFilename, size = (400, 300))
        outputImagePanel = BlockWindow(self, label = "Output Image", size = (400, 300))
        controlPanel = BlockWindow(self, label = "Controls", size = (800, 200))                       
        # Arrange the input and output images side-by-side
        horizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
        horizontalSizer.Add(inputImagePanel, 1, flag=wx.EXPAND)
        horizontalSizer.Add(outputImagePanel, 1, flag=wx.EXPAND)
        # Arrange the controls below the images
        verticalSizer = wx.BoxSizer(wx.VERTICAL)
        verticalSizer.Add(horizontalSizer, 1, flag=wx.EXPAND)
        verticalSizer.Add(controlPanel, flag=wx.EXPAND)
        # Set the sizer to be the main verticalSizer
        self.SetSizer(verticalSizer)

    
    def createStatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([200, -2, -3])
        
    
    def menuData(self):
        return (("&File",
                        ("&Open...\tCtrl-O",   "Open colormapper file",    self.OnOpen),
                        ("&Save\tCtrl-S",   "Save colormapper file",        self.OnSave),
                        ("Save &As...\tShift-Ctrl-S", "Save colormapper file as", self.OnSaveAs),
                        ("&Import...", "Import image for conversion", self.OnImport),
                        ("&Export...", "Export converted image",       self.OnExport),
                        ("&Quit\tCtrl-Q",   "Quit",                         self.OnCloseWindow)),
                        
                ("&Edit",
                        ("&Copy\tCtrl-C",   "Copy converted image to clipboard",    self.OnCopy),
                        ("C&ut",    "Cut converted image to clipboard",     self.OnCut),
                        ("&Paste\tCtrl-V",  "Paste original image from clipboard",  self.OnPaste),
                        ("",        "",                     ""),
                        ("&Options...", "Display Options",                  self.OnOptions)))        
          
    
    def createMenuBar(self):
        menuBar = wx.MenuBar()
        for eachMenuData in self.menuData():
            menuLabel = eachMenuData[0]
            menuItems = eachMenuData[1:]
            menu = self.createMenu(menuItems)
            menuBar.Append(menu, menuLabel)        
        self.SetMenuBar(menuBar)
        return menuBar
        
    
    def createMenu(self, menuItems):
        menu = wx.Menu()
        for eachLabel, eachStatus, eachHandler in menuItems:
            if not eachLabel:
                menu.AppendSeparator()
                continue
            menuItem = menu.Append(-1, eachLabel, eachStatus)
            self.Bind(wx.EVT_MENU, eachHandler, menuItem)
        return menu
        
    
    # Group empty event handlers together
    def OnOpen(self, event): pass
    def OnSave(self, event): pass
    def OnSaveAs(self, event): pass
    def OnImport(self, event): pass
    def OnExport(self, event): pass
    def OnCopy(self, event): pass
    def OnCut(self, event): pass
    def OnPaste(self, event): pass
    def OnOptions(self, event): pass
    
    def OnCloseWindow(self, event):
        self.Destroy()                
