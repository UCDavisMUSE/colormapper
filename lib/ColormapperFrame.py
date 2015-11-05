import wx


# This is the class for the main window of the Colormapper App        
class ColormapperFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Colormapper", size = (800, 600))
        self.SetMinSize((800,600))

		# Attributes 
        statusBar = self.createStatusBar()
        menuuBar = self.createMenuBar()
        
    
    def createStatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([200, -2, -3])
        
    
    def menuData(self):
        return (("&File",
                        ("&Open",   "Open image for conversion",    self.OnOpen),
                        ("&Save",   "Save colormapper file",        self.OnSave),
                        ("&Export", "Export converted image",       self.OnExport),
                        ("&Quit",   "Quit",                         self.OnCloseWindow)),
                        
                ("&Edit",
                        ("&Copy",   "Copy converted image to clipboard",    self.OnCopy),
                        ("C&ut",    "Cut converted image to clipboard",     self.OnCut),
                        ("&Paste",  "Paste original image from clipboard",  self.OnPaste),
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
    def OnExport(self, event): pass
    def OnCopy(self, event): pass
    def OnCut(self, event): pass
    def OnPaste(self, event): pass
    def OnOptions(self, event): pass
    
    def OnCloseWindow(self, event):
        self.Destroy()                
