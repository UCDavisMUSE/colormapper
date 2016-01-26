import wx
import os
import cPickle
import numpy as np
import copy
from BlockWindow import BlockWindow
from ImageViewerPanel import ImageViewerPanel
from ControlPanel import ControlPanel
from UnmixPanel import UnmixPanel
from RemixPanel import RemixPanel
from colormappingMethods import remixImage, unmixParallelTileGradProjNNLS
from OpenCLGradProjNNLS import *

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
        self.inputColors  = [ (228, 250, 166), (244, 205, 100)]
        self.outputColors = [ ( 70,  30, 150), (230, 160, 200)]

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
        self.unmixPanel = UnmixPanel(self)
        self.remixPanel = RemixPanel(self)
        # Arrange the input and output images side-by-side
        self.horizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.horizontalSizer.Add(self.inputImagePanel, 1, wx.EXPAND|wx.ALL, 2)
        self.horizontalSizer.Add(self.outputImagePanel, 1, wx.EXPAND|wx.ALL, 2)
        # Arrange the controls side-by-side
        self.horizontalControlSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.horizontalControlSizer.Add(self.unmixPanel, 1, wx.EXPAND | wx.ALL, 2)
        self.horizontalControlSizer.Add(self.remixPanel, 1, wx.EXPAND | wx.ALL, 2)
        
        # Arrange the controls below the images
        self.verticalSizer = wx.BoxSizer(wx.VERTICAL)
        self.verticalSizer.Add(self.horizontalSizer, 1, flag=wx.EXPAND)
        self.verticalSizer.Add(self.horizontalControlSizer, flag=wx.EXPAND)
        # Set the sizer to be the main verticalSizer
        self.SetSizer(self.verticalSizer)
        
        self.inputImagePanel.Bind(wx.EVT_MOTION, self.OnInputMotion)
        self.outputImagePanel.Bind(wx.EVT_MOTION, self.OnOutputMotion)
        
        # Add code to initialize input / output colors.
        
        # Add code for crosshair button click in Unmix and Remix Panels
        self.Bind(wx.EVT_BUTTON, self.OverrideInputColorButtons,
            self.unmixPanel.buttonBackgroundCrosshair)
        
#         for button in self.controlPanel.inputColorButtons:
#             button.Bind(wx.EVT_BUTTON, self.OverrideInputColorButtons)
            
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnInputMotion)
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.Bind(wx.EVT_CHAR_HOOK, self.OnKey)
        
    def OnKey(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            if self.HasCapture():
                self.ReleaseMouse()
                self.inputImagePanel.reInitBuffer = True
                self.inputImagePanel.InitBuffer()
                self.Refresh()
        event.Skip()
                
        
    def OnIdle(self, event):
        # This is where we recompute the unmix and remix:
        if self.unmixPanel.recomputeUnmix:
#            print("Unmixing...")
            self.UnmixImage()
            self.remixPanel.recomputeRemix = True
            self.unmixPanel.recomputeUnmix = False 
            
        if self.remixPanel.recomputeRemix:
#            print("Remixing...")
            self.RemixImage()
            self.remixPanel.recomputeRemix = False       
        
    def OverrideInputColorButtons(self, event):
        self.currentButtonClicked = event.GetEventObject()
        self.CaptureMouse()        
    
    def OnLeftDown(self, event):
        if self.HasCapture():
            self.currentPosition = event.GetPositionTuple()
    
    def OnLeftUp(self, event):
        if self.HasCapture():
            # Update color selection if valid
            if self.inputImagePanel.displayedImage.Ok():
                currentPosition = (self.currentPosition[0] - self.inputImagePanel.translation[0],
                                   self.currentPosition[1] - self.inputImagePanel.translation[1])
                width = self.inputImagePanel.displayedImage.GetWidth()
                height = self.inputImagePanel.displayedImage.GetHeight()
                if (0 <= currentPosition[0] < width and 0 <= currentPosition[1] < height):
                    currentColor = (self.inputImagePanel.displayedImage.GetRed(currentPosition[0],currentPosition[1]),
                                    self.inputImagePanel.displayedImage.GetGreen(currentPosition[0],currentPosition[1]),
                                    self.inputImagePanel.displayedImage.GetBlue(currentPosition[0],currentPosition[1]))
                    self.colorButtonBackgroundColor.SetBackgroundColour(currentColor)
                    self.Refresh()
            self.ReleaseMouse()
            self.inputImagePanel.InitBuffer()

    def createStatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([200, -2, -3])

    def OnInputMotion(self, event):
        currentPosition = event.GetPositionTuple()
       # self.statusbar.SetStatusText("Pos: %s" % str(currentPosition), 0)
        if self.inputImagePanel.displayedImage.Ok():
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
        if self.HasCapture():
            self.inputImagePanel.DrawCrosshair(event)
        event.Skip()

    def OnOutputMotion(self, event):
        currentPosition = event.GetPositionTuple()
        #self.statusbar.SetStatusText("Pos: %s" % str(currentPosition), 0)
        if self.outputImagePanel.displayedImage.Ok():
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
                        ("&Open Settings...\tCtrl-O",               "Open colormapper file",        self.OnOpen),
                        ("&Save Settings\tCtrl-S",                  "Save colormapper file",        self.OnSave),
                        ("Save Settings &As...\tShift-Ctrl-S",      "Save colormapper file as",     self.OnSaveAs),
                        ("&Import Image for Conversion...\tCtrl-I", "Import image for conversion",  self.OnImport),
                        ("&Export Converted Image...\tCtrl-E",      "Export converted image",       self.OnExport),
                        ("&Quit\tCtrl-Q",                           "Quit",                         self.OnCloseWindow)),
                        
#                ("&Edit",
#                        ("&Copy\tCtrl-C",       "Copy converted image to clipboard",    self.OnCopy),
#                        ("C&ut",                "Cut converted image to clipboard",     self.OnCut),
#                        ("&Paste\tCtrl-V",      "Paste original image from clipboard",  self.OnPaste),
#                        ("",                    "",                                     ""),
#                        ("&Number of Colors...",         "Change Number of Colors",                      self.OnOptions))
                )        
          
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
        dlg.Destroy()
            
    def ReadFile(self):
        # This code reads a colormapper file
        if self.filename:
            try:
                f = open(self.filename, 'r')
                (inputColors, outputColors) = cPickle.load(f)
                self.SetInputOutputColors(inputColors, outputColors)
                self.currentDirectory = os.path.split(self.filename)[0]
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
            self.currentDirectory = os.path.split(self.filename)[0]

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
        # Code for overriding button behavior to select colors from image
        for button in self.controlPanel.inputColorButtons:
            button.Bind(wx.EVT_BUTTON, self.OverrideInputColorButtons)

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
                self.SetTitle(self.title + ' - ' + os.path.split(self.imageFilename)[1])
                self.currentDirectory = os.path.split(self.imageFilename)[0]            
                       
                # On a successful import, we should clear the colormapper filename to
                # prevent overwrites on the save command, as well as reinitialize the buffer
                # and clear the output image
                self.filename = ""
                self.inputImagePanel.newImageData = True
                self.inputImagePanel.reInitBuffer = True
                self.outputImagePanel.image = wx.EmptyImage()
                self.outputImagePanel.newImageData = True
                self.outputImagePanel.reInitBuffer = True
                self.unmixPanel.recomputeUnmix = True
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
                self.currentDirectory = os.path.split(self.exportFilename)[0]    
            except:
                wx.MessageBox("Error exporting %s." % self.filename, "oops!",
                    stype=wx.OK|wx.ICON_EXCLAMATION)
                    
    def UnmixImage(self):
        if not self.inputImagePanel.image.Ok():
            return
    
        # Convert wx.Image to numpy array
        inputImageBuffer = self.inputImagePanel.image.GetDataBuffer()
        inputImageArray = np.frombuffer(inputImageBuffer, dtype='uint8')
            
        # Reshape the input numpy array to a width X height X 3 RGB image
        self.inputImageWidth = self.inputImagePanel.image.GetWidth()
        self.inputImageHeight = self.inputImagePanel.image.GetHeight()
        self.inputImageSize = inputImageArray.size     
        self.inputImageArray = inputImageArray.reshape(self.inputImageWidth, self.inputImageHeight, 3)
        self.outputImageArray = copy.copy(self.inputImageArray)
        # If we use OpenCV, the image is expected to be BGR
        # inputImageArray = cv2.cvtColor(inputImageArray, cv2.COLOR_RGB2BGR)
        
        # Do Unmixing
        A = np.zeros((3, 2), dtype = np.float64)
        A[:,0] = self.unmixPanel.backgroundSpectrum
        A[:,1] = self.unmixPanel.nucleiSpectrum
        if self.unmixPanel.subtractBackground:
            maxAmount = np.inf
            for color in range(A.shape[0]):
                if A[color,0] != 0:
                    maxAmount = min(maxAmount, 1.0*A[color,1]/A[color,0])
            A[:,1] = A[:,1] - 1.0*(self.unmixPanel.subtractBackgroundAmount/100.0)*maxAmount*A[:,0]
            A[:,1] = 255.0*A[:,1]/np.sum(A[:,1])            
            
        # Faster (Open CL-based) Method:
        self.unmixComponents = OpenCLGradProjNNLS(self.outputImageArray, A,
            tolerance = 1e-1, maxiter = 100, context = 0)
        # Slower (Multithreaded) Method:
#         self.unmixComponents = unmixParallelTileGradProjNNLS(self.outputImageArray, A,
#             tolerance = 1e-1, maxiter = 100)
            
        # May need to add code here if I want to display the unmixComponents

    def RemixImage(self):
        if not self.inputImagePanel.image.Ok():
            return
    
        components = copy.copy(self.unmixComponents)
        B = np.zeros((3, 2), dtype = np.float64)
        B[:,0] = self.remixPanel.backgroundColor
        B[:,1] = self.remixPanel.nucleiColor
        thresh = [self.remixPanel.backgroundThresh, self.remixPanel.nucleiThresh]
        gain = [self.remixPanel.backgroundGain, self.remixPanel.nucleiGain]
        gamma = [self.remixPanel.backgroundGamma, self.remixPanel.nucleiGamma]
        method = self.remixPanel.remixMode
        
        # Do Remixing        
        self.outputImageArray = remixImage(components, B, thresh, gain, gamma, method)
        
        # Get/set dimensions of output image
        outputImageWidth = self.inputImageWidth
        outputImageHeight = self.inputImageHeight
        outputImageSize = self.inputImageSize
        
        # Reshape the output numpy array to a vector
        self.outputImageArray = self.outputImageArray.reshape(outputImageSize)

        # Convert the output numpy array to a wx.Image
        # First initialize with an empty image
        self.outputImagePanel.image = wx.EmptyImage(outputImageWidth, outputImageHeight)
        self.outputImagePanel.image.SetData(self.outputImageArray.tostring())

        # Tell the outputImagePanel to refresh the display    
        self.outputImagePanel.newImageData = True        
        self.outputImagePanel.reInitBuffer = True
            
    # Group empty event handlers together
    def OnCopy(self, event): pass
    def OnCut(self, event): pass
    def OnPaste(self, event): pass

    def OnCloseWindow(self, event):
        self.Destroy()        
        
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
                
