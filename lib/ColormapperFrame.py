import wx
import os
import cPickle
from BlockWindow import BlockWindow
from ImageViewerPanel import ImageViewerPanel
from ControlPanel import ControlPanel

# Class for file drop target
class MyFileDropTarget(wx.FileDropTarget):

    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window
    
    def OnDropFiles(self, x, y, filenames):
        if len(filenames) > 1:
            dlg = wx.MessageBox( 
                "This application only supports dragging a single file at a time.",
                "Multiple files detected", wx.OK | wx.ICON_EXCLAMATION)
            return
        if os.path.splitext(filenames[0])[1].lower() == ".colormapper":
            self.window.filename = filenames[0]
            self.window.ReadFile()
        else:
            self.window.imageFilename = filenames[0]
            self.window.ImportImage()

# This is the class for the main window of the Colormapper App        
class ColormapperFrame(wx.Frame):
    # Internal class data
    defaultImageType = '.png'
    imageWildcard = "PNG (*.png)|*.png|JPEG (*.jpg, *.jpeg)|*.jpg;*.jpeg|TIFF (*.tif, *.tiff)|*.tif;*.tiff|BMP (*.bmp)|*.bmp|All Files (*.*)|*.*"
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
        self.currentDirectory = ""
        self.numberOfColors = 3
        self.inputColors  = [ (  0,   0,   0), (228, 250, 166), (244, 205, 100) ]
        self.outputColors = [ (255, 255, 255), ( 70,  30, 150), (230, 160, 200) ]

        # Attributes 
        statusBar = self.createStatusBar()
        menuBar = self.createMenuBar()
        self.createMainInterfaceWindow()
        
        # Add drop target
        dropTarget = MyFileDropTarget(self)
        self.SetDropTarget(dropTarget)
        
        
    def createMainInterfaceWindow(self):
        # Create sub panels
        self.inputImagePanel = ImageViewerPanel(self, label = "Input Image", size = (300, 200))
        self.outputImagePanel = ImageViewerPanel(self, label = "Output Image", size = (300, 200))
        self.controlPanel = ControlPanel(self, 
            inputColors = self.inputColors, inputImagePanel = self.inputImagePanel,
            outputColors = self.outputColors, outputImagePanel = self.outputImagePanel,
            label = "Control Panel", size = (800, 100))                       
        # Arrange the input and output images side-by-side
        self.horizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.horizontalSizer.Add(self.inputImagePanel, 1, wx.EXPAND|wx.ALL, 2)
        self.horizontalSizer.Add(self.outputImagePanel, 1, wx.EXPAND|wx.ALL, 2)
        # Arrange the controls below the images
        self.verticalSizer = wx.BoxSizer(wx.VERTICAL)
        self.verticalSizer.Add(self.horizontalSizer, 1, flag=wx.EXPAND)
        self.verticalSizer.Add(self.controlPanel, flag=wx.EXPAND)
        # Set the sizer to be the main verticalSizer
        self.SetSizer(self.verticalSizer)
        
        self.inputImagePanel.Bind(wx.EVT_MOTION, self.OnInputMotion)
        self.outputImagePanel.Bind(wx.EVT_MOTION, self.OnOutputMotion)

        # Code for overriding button behavior to select colors from image
        for button in self.controlPanel.inputColorButtons:
            button.Bind(wx.EVT_BUTTON, self.OverrideInputColorButtons)
            
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnInputMotion)
            
        
    def OverrideInputColorButtons(self, event):
        self.currentButtonClicked = event.GetEventObject()
        if self.controlPanel.choice.GetSelection() == 1:
            self.CaptureMouse()        
        else:
            event.Skip()

    
    def OnLeftDown(self, event):
        if self.HasCapture():
            self.currentPosition = event.GetPositionTuple()

    
    def OnLeftUp(self, event):
        if self.HasCapture():
            # Update color selection if valid
            if self.inputImagePanel.image.Ok():
                currentPosition = (self.currentPosition[0] - self.inputImagePanel.translation[0],
                                   self.currentPosition[1] - self.inputImagePanel.translation[1])
                width = self.inputImagePanel.displayedImage.GetWidth()
                height = self.inputImagePanel.displayedImage.GetHeight()
                if (0 <= currentPosition[0] < width and 0 <= currentPosition[1] < height):
                    currentColor = (self.inputImagePanel.displayedImage.GetRed(currentPosition[0],currentPosition[1]),
                                    self.inputImagePanel.displayedImage.GetGreen(currentPosition[0],currentPosition[1]),
                                    self.inputImagePanel.displayedImage.GetBlue(currentPosition[0],currentPosition[1]))
                    self.currentButtonClicked.SetBackgroundColour(currentColor)
                    self.Refresh()
            self.ReleaseMouse()
            
            
    def OnMotion(self, event):
        currentPosition = event.GetPositionTuple()
       # self.statusbar.SetStatusText("Pos: %s" % str(currentPosition), 0)
        if self.inputImagePanel.image.Ok():
            currentPosition = (currentPosition[0] - self.inputImagePanel.translation[0],
                               currentPosition[1] - self.inputImagePanel.translation[1])
            width = self.inputImagePanel.displayedImage.GetWidth()
            height = self.inputImagePanel.displayedImage.GetHeight()
            if (0 <= currentPosition[0] < width and 0 <= currentPosition[1] < height):
                currentColor = (self.inputImagePanel.displayedImage.GetRed(currentPosition[0],currentPosition[1]),
                                self.inputImagePanel.displayedImage.GetGreen(currentPosition[0],currentPosition[1]),
                                self.inputImagePanel.displayedImage.GetBlue(currentPosition[0],currentPosition[1]))
                self.statusbar.SetStatusText("Color (R, G, B): %s" % str(currentColor), 1)
            else:
                self.statusbar.SetStatusText("", 1)
            self.Refresh()


    def createStatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([200, -2, -3])


    def OnInputMotion(self, event):
        currentPosition = event.GetPositionTuple()
       # self.statusbar.SetStatusText("Pos: %s" % str(currentPosition), 0)
        if self.inputImagePanel.image.Ok():
            currentPosition = (currentPosition[0] - self.inputImagePanel.translation[0],
                               currentPosition[1] - self.inputImagePanel.translation[1])
            width = self.inputImagePanel.displayedImage.GetWidth()
            height = self.inputImagePanel.displayedImage.GetHeight()
            if (0 <= currentPosition[0] < width and 0 <= currentPosition[1] < height):
                currentColor = (self.inputImagePanel.displayedImage.GetRed(currentPosition[0],currentPosition[1]),
                                self.inputImagePanel.displayedImage.GetGreen(currentPosition[0],currentPosition[1]),
                                self.inputImagePanel.displayedImage.GetBlue(currentPosition[0],currentPosition[1]))
                self.statusbar.SetStatusText("Color (R, G, B): %s" % str(currentColor), 1)
            else:
                self.statusbar.SetStatusText("", 1)
        event.Skip()
            

    def OnOutputMotion(self, event):
        currentPosition = event.GetPositionTuple()
        #self.statusbar.SetStatusText("Pos: %s" % str(currentPosition), 0)
        if self.outputImagePanel.image.Ok():
            currentPosition = (currentPosition[0] - self.outputImagePanel.translation[0],
                               currentPosition[1] - self.outputImagePanel.translation[1])
            width = self.outputImagePanel.displayedImage.GetWidth()
            height = self.outputImagePanel.displayedImage.GetHeight()
            if (0 <= currentPosition[0] < width and 0 <= currentPosition[1] < height):
                currentColor = (self.outputImagePanel.displayedImage.GetRed(currentPosition[0],currentPosition[1]),
                                self.outputImagePanel.displayedImage.GetGreen(currentPosition[0],currentPosition[1]),
                                self.outputImagePanel.displayedImage.GetBlue(currentPosition[0],currentPosition[1]))
                self.statusbar.SetStatusText("Color (R, G, B): %s" % str(currentColor), 1)
            else:
                self.statusbar.SetStatusText("", 1)
        event.Skip()
        
    
    def menuData(self):
        return (("&File",
                        ("&Open Colormap...\tCtrl-O",               "Open colormapper file",        self.OnOpen),
                        ("&Save Colormap\tCtrl-S",                  "Save colormapper file",        self.OnSave),
                        ("Save Colormap &As...\tShift-Ctrl-S",      "Save colormapper file as",     self.OnSaveAs),
                        ("&Import Image for Conversion...\tCtrl-I", "Import image for conversion",  self.OnImport),
                        ("&Export Converted Image...\tCtrl-E",      "Export converted image",       self.OnExport),
                        ("&Quit\tCtrl-Q",                           "Quit",                         self.OnCloseWindow)),
                        
                ("&Edit",
#                        ("&Copy\tCtrl-C",       "Copy converted image to clipboard",    self.OnCopy),
#                        ("C&ut",                "Cut converted image to clipboard",     self.OnCut),
#                        ("&Paste\tCtrl-V",      "Paste original image from clipboard",  self.OnPaste),
#                        ("",                    "",                                     ""),
                        ("&Number of Colors...",         "Change Number of Colors",                      self.OnOptions)))        
          
    
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
        if self.currentDirectory:
            dlg.SetDirectory(self.currentDirectory)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetPath()
            self.ReadFile()
            self.SetTitle(self.title + ' - ' + os.path.split(self.filename)[1])
            self.currentDirectory = os.path.split(self.filename)[0]
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
        if self.currentDirectory:
            dlg.SetDirectory(self.currentDirectory)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            if not os.path.splitext(filename)[1]:
                filename = filename + '.colormapper'
            self.filename = filename
            self.SaveFile()
            self.SetTitle(self.title + ' - ' + os.path.split(self.filename)[1])
            self.currentDirectory = os.path.split(self.filename)[0]
        dlg.Destroy()


    def OnImport(self, event):
        dlg = wx.FileDialog(self, "Import image for conversion...",
                os.getcwd(), style=wx.OPEN,
                wildcard = self.imageWildcard)
        if self.currentDirectory:
            dlg.SetDirectory(self.currentDirectory)                
        if dlg.ShowModal() == wx.ID_OK:
            self.imageFilename = dlg.GetPath()
            self.ImportImage()
            self.SetTitle(self.title + ' - ' + "Untitled")
            self.currentDirectory = os.path.split(self.imageFilename)[0]            
        dlg.Destroy()


    def OnExport(self, event):
        dlg = wx.FileDialog(self, "Export converted image...",
                os.getcwd(), style=wx.SAVE | wx.OVERWRITE_PROMPT,
                wildcard = self.imageWildcard)
        if self.currentDirectory:
            dlg.SetDirectory(self.currentDirectory)                
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            if not os.path.splitext(filename)[1]:
                filename = filename + self.defaultImageType
            self.exportFilename = filename
            self.ExportImage()
            self.currentDirectory = os.path.split(self.exportFilename)[0]
        dlg.Destroy()

            
    def ReadFile(self):
        # This code reads a colormapper file
        if self.filename:
            try:
                f = open(self.filename, 'r')
                (inputColors, outputColors) = cPickle.load(f)
                self.SetInputOutputColors(inputColors, outputColors)
            except cPickle.UnpicklingError:
                wx.MessageBox("%s is not a colormapper file." % self.filename, "oops!",
                    stype=wx.OK|wx.ICON_EXCLAMATION)


    def SaveFile(self):
        # This code saves a colormapper file
        if self.filename:
            (inputColors, outputColors) = self.GetInputOutputColors()
            f = open(self.filename, 'w')
            cPickle.dump((inputColors, outputColors), f)
            f.close()


    def GetInputOutputColors(self):
        inputColors = [];
        for color in range(len(self.controlPanel.inputColorButtons)):
            inputColors += [self.controlPanel.inputColorButtons[color].GetBackgroundColour()[0:3]]
        outputColors = [];
        for color in range(len(self.controlPanel.outputColorButtons)):
            outputColors += [self.controlPanel.outputColorButtons[color].GetBackgroundColour()[0:3]]
        return (inputColors, outputColors)

    
    def SetInputOutputColors(self,inputColors,outputColors):
        self.controlPanel.Destroy()
        self.controlPanel = ControlPanel(self,
            inputColors = inputColors, inputImagePanel = self.inputImagePanel, 
            outputColors = outputColors, outputImagePanel = self.outputImagePanel, 
            label = "Control Panel", size = (800, 100))                       
        self.verticalSizer.Add(self.controlPanel, flag=wx.EXPAND)
        self.verticalSizer.Layout()


    def ImportImage(self):
        # This code imports the image
        if self.imageFilename:
            try:
                fileExtension = os.path.splitext(self.imageFilename)[1]
                if fileExtension == ".png":
                    self.inputImagePanel.image = wx.Image(self.imageFilename, wx.BITMAP_TYPE_PNG)
                elif fileExtension == ".jpg" or fileExtension == ".jpeg":
                    self.inputImagePanel.image = wx.Image(self.imageFilename, wx.BITMAP_TYPE_JPEG)
                elif fileExtension == ".tif" or fileExtension == ".tiff":
                    self.inputImagePanel.image = wx.Image(self.imageFilename, wx.BITMAP_TYPE_TIF)
                elif fileExtension == ".bmp":
                    self.inputImagePanel.image = wx.Image(self.imageFilename, wx.BITMAP_TYPE_BMP)
                else:
                    # nolog = wx.LogNull() # Uncommenting will not log errors 
                    self.inputImagePanel.image = wx.Image(self.imageFilename, wx.BITMAP_TYPE_ANY)
                    #del nolog
                       
                # On a successful import, we should clear the colormapper filename to
                # prevent overwrites on the save command, as well as reinitialize the buffer
                # and clear the output image
                self.filename = ""
                self.inputImagePanel.newImageData = True
                self.inputImagePanel.reInitBuffer = True
                self.outputImagePanel.image = wx.EmptyImage()
                self.outputImagePanel.newImageData = True
                self.outputImagePanel.reInitBuffer = True
            except:
                wx.MessageBox("Error importing %s." % self.filename, "oops!",
                    stype=wx.OK|wx.ICON_EXCLAMATION)


    def ExportImage(self):
        # This code exports the image
        if self.exportFilename:
            try:
                fileExtension = os.path.splitext(self.exportFilename)[1]
                if fileExtension == ".png":
                    self.outputImagePanel.image.SaveFile(self.exportFilename, wx.BITMAP_TYPE_PNG)
                elif fileExtension == ".jpg" or fileExtension == ".jpeg":
                    self.outputImagePanel.image.SaveFile(self.exportFilename, wx.BITMAP_TYPE_JPEG)
                elif fileExtension == ".tif" or fileExtension == ".tiff":
                    self.outputImagePanel.image.SaveFile(self.exportFilename, wx.BITMAP_TYPE_TIF)
                elif fileExtension == ".bmp":
                    self.outputImagePanel.image.SaveFile(self.exportFilename, wx.BITMAP_TYPE_BMP)
                else:
                    # nolog = wx.LogNull() # Uncommenting will not log errors 
                    self.outputImagePanel.image.SaveFile(self.exportFilename, wx.BITMAP_TYPE_ANY)
                    #del nolog
            except:
                wx.MessageBox("Error exporting %s." % self.filename, "oops!",
                    stype=wx.OK|wx.ICON_EXCLAMATION)
            

    # Group empty event handlers together
    def OnCopy(self, event): pass
    def OnCut(self, event): pass
    def OnPaste(self, event): pass

    def OnOptions(self, event): 
        choices = ["3", "4", "5"]
        dialog = wx.SingleChoiceDialog(None, "Select the number of colors to map", "Number of Colors",
            choices)
        if dialog.ShowModal() == wx.ID_OK:
            newNumberOfColors = int(dialog.GetStringSelection())
            (inputColors, outputColors) = self.GetInputOutputColors()
            if newNumberOfColors > len(inputColors):
                # Need to add colors
                while len(inputColors) < newNumberOfColors:
                    inputColors += [(0, 0, 0)] # Append with Black
                while len(outputColors) < newNumberOfColors:
                    outputColors += [(0, 0, 0)] #Append with Black
                self.SetInputOutputColors(inputColors, outputColors)
                
            elif newNumberOfColors < len(inputColors):
                # Need to remove colors
                inputColors = inputColors[0:newNumberOfColors]
                outputColors = outputColors[0:newNumberOfColors]
                self.SetInputOutputColors(inputColors, outputColors)
        
        dialog.Destroy()
        
    
    def OnCloseWindow(self, event):
        self.Destroy()                
