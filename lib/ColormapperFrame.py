import wx
import os
from BlockWindow import BlockWindow
from ImageViewerPanel import ImageViewerPanel

# This is the class for the main window of the Colormapper App        
class ColormapperFrame(wx.Frame):
    # Internal class data
    defaultImageType = '.png'
    imageWildcard = "PNG (*.png)|*.png|JPEG (*.jpg,*.jpeg)|*.jpg;*.jpeg|All Files (*.*)|*.*"
    # More on imagetypes: http://www.wxpython.org/docs/api/wx.Image-class.html#__init__
    colormapperWildcard = "Colormapper files (*.colormapper)|*.colormapper|All Files (*.*)|*.*"
        

    def __init__(self):
        self.title = "Colormapper"
        wx.Frame.__init__(self, None, -1, self.title, size = (800, 600))
        self.SetMinSize((800,600))

        # High-level application data
        self.imageFilename = ""
        self.filename = ""
        self.exportFilename = ""

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
                        ("&Open...\tCtrl-O",            "Open colormapper file",        self.OnOpen),
                        ("&Save\tCtrl-S",               "Save colormapper file",        self.OnSave),
                        ("Save &As...\tShift-Ctrl-S",   "Save colormapper file as",     self.OnSaveAs),
                        ("&Import...\tCtrl-I",          "Import image for conversion",  self.OnImport),
                        ("&Export...\tCtrl-E",          "Export converted image",       self.OnExport),
                        ("&Quit\tCtrl-Q",               "Quit",                         self.OnCloseWindow)),
                        
                ("&Edit",
                        ("&Copy\tCtrl-C",       "Copy converted image to clipboard",    self.OnCopy),
                        ("C&ut",                "Cut converted image to clipboard",     self.OnCut),
                        ("&Paste\tCtrl-V",      "Paste original image from clipboard",  self.OnPaste),
                        ("",                    "",                                     ""),
                        ("&Options...",         "Display Options",                      self.OnOptions)))        
          
    
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
        

    # Menu event handlers
    def OnOpen(self, event):
        dlg = wx.FileDialog(self, "Open colormapper file...",
                os.getcwd(), style=wx.OPEN,
                wildcard = self.colormapperWildcard)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetPath()
            self.ReadFile()
            self.SetTitle(self.title + ' - ' + os.path.split(self.filename)[1])
        dlg.Destroy()


    def OnSave(self, event):
        if not self.filename:
            self.OnSaveAs(event)
        else:
            self.SaveFile()

            
    def OnSaveAs(self, event):
        dlg = wx.FileDialog(self, "Save colormapper file...",
                os.getcwd(), style = wx.SAVE | wx.OVERWRITE_PROMPT,
                wildcard = self.colormapperWildcard)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            if not os.path.splitext(filename)[1]:
                filename = filename + '.colormapper'
            self.filename = filename
            self.SaveFile()
            self.SetTitle(self.title + ' - ' + os.path.split(self.filename)[1])
        dlg.Destroy()


    def OnImport(self, event):
        dlg = wx.FileDialog(self, "Import image...",
                os.getcwd(), style=wx.OPEN,
                wildcard = self.imageWildcard)
        if dlg.ShowModal() == wx.ID_OK:
            self.imageFilename = dlg.GetPath()
            self.ImportImage()
            self.SetTitle(self.title + ' - ' + "Untitled")
        dlg.Destroy()


    def OnExport(self, event):
        dlg = wx.FileDialog(self, "Save colormapper file...",
                os.getcwd(), style=wx.SAVE | wx.OVERWRITE_PROMPT,
                wildcard = self.imageWildcard)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            if not os.path.splitext(filename)[1]:
                filename = filename + self.defaultImageType
            self.exportFilename = filename
            self.ExportImage()
        dlg.Destroy()

            
    def ReadFile(self):
        # This code reads a colormapper file
        pass
        

    def SaveFile(self):
        # This code saves a colormapper file
        pass


    def ImportImage(self):
        # This code imports the image
        
        # On a successful import, we should clear the colormapper filename to
        # prevent overwrites on the save command
        self.filename = ""

        
    def ExportImage(self):
        # This code exports the image
        pass
            

    # Group empty event handlers together
    def OnCopy(self, event): pass
    def OnCut(self, event): pass
    def OnPaste(self, event): pass
    def OnOptions(self, event): pass
    
    def OnCloseWindow(self, event):
        self.Destroy()                
