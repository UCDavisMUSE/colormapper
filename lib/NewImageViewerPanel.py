import wx
import os
import math


class ImageViewerPanel(wx.Panel):

    def __init__(self, parent, id = -1):
        wx.Panel.__init__(self, parent, id)
                                    
        # Default Parameters
        self.SetBackgroundColour("Black")        
        self.resizeMethod = wx.IMAGE_QUALITY_HIGH
        # wxIMAGE_QUALITY_NEAREST: 
        #   Simplest and fastest algorithm.
        # wxIMAGE_QUALITY_BILINEAR: 
        #   Compromise between wxIMAGE_QUALITY_NEAREST and
        #   wxIMAGE_QUALITY_BICUBIC.
        # wxIMAGE_QUALITY_BICUBIC: 
        #   Highest quality but slowest execution time.
        # wxIMAGE_QUALITY_BOX_AVERAGE: 
        #   Use surrounding pixels to calculate an
        #   average that will be used for new pixels. 
        #   This method is typically used when reducing
        #   the size of an image.
        # wxIMAGE_QUALITY_NORMAL:
        #   Default image resizing algorithm used 
        #   by wxImage::Scale(). Currently the same 
        #   as wxIMAGE_QUALITY_NEAREST.
        # wxIMAGE_QUALITY_HIGH: 
        #   Best image resizing algorithm. Since 
        #   version 2.9.2 this results in 
        #   wxIMAGE_QUALITY_BOX_AVERAGE being used when
        #   reducing the size of the image (meaning that 
        #   both the new width and height will be smaller 
        #   than the original size). 
        #   Otherwise wxIMAGE_QUALITY_BICUBIC is used.
        
        # Default Parameters
        self.maintainAspectRatio = True
        self.idleBuffer = True
        self.zoomToFit = False
        self.drawCrosshair = False


        # Working on these        
        self.zoomValues = [0.0625, 0.125, 0.25, 0.5, 0.75, 1.0, 
            1.25, 1.5, 1.75, 2.0, 3.0, 4.0, 6.0, 8.0]
        self.zoomIndex = 5
        self.zoomValue = self.zoomValues[self.zoomIndex]
                

        
        # Temporary state variables
        self.displayWidth = 1
        self.displayHeight = 1        
        self.resizedWidth = 1
        self.resizedHeight = 1
        self.buffer = None # This is the entire dc buffer
        self.image = wx.EmptyImage() # Initialize with an empty image
        self.resizedImage = wx.EmptyImage()
        self.bitmap = wx.EmptyBitmap(1,1) # This is a bitmap of the resized
        self.crosshairPosition = (0,0)
        self.cursorInWindow = True
        
        

        
        # Old values        
        self.zoomFactor = 1.0       # This is a temporary parameter
        self.zoomFactorMax = 8.0
        self.zoomFactorMin = 1.0/self.zoomFactorMax
        self.zoomFactorIncreaseMultiplier = 1.05
        self.zoomFactorDecreaseMultiplier = 1.0/self.zoomFactorIncreaseMultiplier
        self.translation = (0,0)
        self.viewModes = [
            'Actual Size - no interaction',
            'Zoom to Fit - no interaction',
            'Zoom',
            'Pan']
        self.viewMode = 1



        
        # Initialize Buffer
        if self.idleBuffer:
            self.InitBuffer()
        
        # Event handlers
        self.Bind(wx.EVT_SIZE, self.OnSize)       
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        # Mouse events
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnterWindow)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)


        # Mouse event handlers                
#        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
#        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
#        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
#        self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
#        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)

     
     
    ## Event Handlers
    
    def OnSize(self, event):
        self.ReInitBuffer()

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self, self.buffer)  
        
    def OnIdle(self, event):
        # Essentially, self.idleBuffer determines whether
        # the buffer is created when the program is idle. 
        # If set True, the UI chrome is more responsive on slow
        # systems, if set False, the content is more responsive
        # on fast systems. 
        if self.idleBuffer and self.reInitBuffer:
            self.InitBuffer()
            self.Refresh()
        self.reInitBuffer = False
        
    def OnMotion(self, event):
        if self.drawCrosshair:
            self.crosshairPosition = event.GetPositionTuple()
            self.ReInitBuffer() # Redraw with crosshair
            
    def OnLeaveWindow(self, event):
        # If the mouse leaves the ImageViewerPanel, 
        # refresh to remove the crosshair
        self.cursorInWindow = False
        if self.drawCrosshair:
            self.ReInitBuffer()

    def OnEnterWindow(self, event):
        # If the mouse returns to the ImageViewerPanel,
        # refresh to redraw the crosshair
        self.cursorInWindow = True
        if self.drawCrosshair:
            self.ReInitBuffer()

       
    ## Helper Methods           
        
    def InitBuffer(self):
        """
        This is where all drawing should occur.
        """
        (self.displayWidth, self.displayHeight) = self.GetClientSize()
        self.buffer = wx.EmptyBitmap(self.displayWidth, self.displayHeight)
        dc = wx.MemoryDC(self.buffer)
        
        if not self.image.Ok():
            return
            
        self.ResizeImageAndCreateBitmap()
                 
        dc.DrawBitmap(self.bitmap, 0, 0, True)
        
        if self.drawCrosshair and self.cursorInWindow:
            dc.DrawLine(0, self.crosshairPosition[1],
                self.displayWidth, self.crosshairPosition[1])
            dc.DrawLine(self.crosshairPosition[0], 0,
                self.crosshairPosition[0], self.displayHeight)
        
    def ReInitBuffer(self):
        if self.idleBuffer:
            self.reInitBuffer = True
        else:
            self.InitBuffer()
            self.Refresh()   
    
    def ResizeImageAndCreateBitmap(self):
        # First determine resized width and height
        if self.zoomToFit:
            if self.maintainAspectRatio:
                (imageWidth, imageHeight) = self.image.GetSize()
                self.resizedWidth = min(self.displayWidth,
                    math.floor(1.0*imageWidth*self.displayHeight/imageHeight))
                self.resizedHeight = min(self.displayHeight,
                    math.floor(1.0*imageHeight*self.displayWidth/imageWidth))
                self.zoomValue = 1.0*self.displayWidth/imageWidth
            else:
                self.resizedWidth = self.displayWidth
                self.resizedHeight = self.displayHeight
                self.zoomValue = None
        else:
            # Actual size for now
            (self.resizedWidth, self.resizedHeight) = self.image.GetSize()
            self.zoomValue = 1.0
        
        # If empty image or different than current, or perform resizing
        # and create bitmap
        if self.resizedImage.IsOk():
            if (self.resizedImage.GetWidth() != self.resizedWidth or
                self.resizedImage.GetHeight() != self.resizedHeight):
                self.resizedImage = \
                    self.image.Scale(self.resizedWidth, self.resizedHeight,
                        quality = self.resizeMethod)
                self.bitmap = wx.BitmapFromImage(self.resizedImage)
                        
        else:
            self.resizedImage = \
                self.image.Scale(self.resizedWidth, self.resizedHeight,
                    quality = self.resizeMethod)        
            self.bitmap = wx.BitmapFromImage(self.resizedImage)


    
        





# VVV OLD CODE VVV  

    def GetImageDisplaySize(self):
        # Should really clean this up!
        if not self.image.Ok():
            return (1,1)
    
        if self.viewMode == 0:
            (display_width, display_height) = self.image.GetSize()
            self.zoomFactor = 1.0
        elif self.viewMode == 1:
            self.translation = (0,0)
            (view_width, view_height) = self.GetClientSize()
            if self.maintainAspectRatio:
                (img_width, img_height) = self.image.GetSize()
                display_width  = min(view_width,
                    math.floor(1.0*img_width*view_height/img_height))
                display_height = min(view_height,
                    math.floor(1.0*img_height*view_width/img_width))
                self.zoomFactor = 1.0*display_width/img_width
            else:
                (display_width, display_height) = (view_width, view_height)
        elif self.viewMode == 2 or self.viewMode == 3:
            (img_width, img_height) = self.image.GetSize()
            display_width = round(1.0*self.zoomFactor*img_width)
            display_height = round(1.0*self.zoomFactor*img_height)
                
        return (display_width, display_height) 
                
    def OnLeftDown(self, event):
        if self.viewMode == 3:
            self.pos = event.GetPositionTuple()
            self.oldTranslation = self.translation
        self.CaptureMouse()     
        
    def OnLeftUp(self, event):
        if self.HasCapture():
            if self.viewMode == 0: 
                pass
            elif self.viewMode == 1: 
                pass
            elif self.viewMode == 2: 
                self.IncreaseZoomFactor()
                self.reInitBuffer = True
            elif self.viewMode == 3:
                self.reInitBuffer = True
            self.ReleaseMouse()
    

    def OnRightDown(self, event):
        self.CaptureMouse()

        
    def OnRightUp(self, event):
        if self.HasCapture():
            if self.viewMode == 0:
                pass
            elif self.viewMode == 1:
                pass
            elif self.viewMode == 2:
                self.DecreaseZoomFactor()
                self.reInitBuffer = True
            elif self.viewMode == 3:
                pass
            self.ReleaseMouse()
        
    def OldOnMotion(self, event):
        if self.viewMode == 3:
            if event.Dragging() and event.LeftIsDown():
                newPos = event.GetPositionTuple()
                delta = (newPos[0] - self.pos[0],
                    newPos[1] - self.pos[1])
                self.translation = (self.oldTranslation[0] + delta[0],
                    self.oldTranslation[1] + delta[1])
                self.reInitBuffer = True
                
        # Draw crosshairs if crosshairs are enabled
        if self.drawCrosshair:
            self.DrawCrosshair(event)
        event.Skip()
        
        
    def OnMouseWheel(self, event):
        if self.viewMode == 0:
            pass
        elif self.viewMode == 1:
            pass
        elif self.viewMode == 2 or self.viewMode == 3:
            x = event.GetWheelRotation()
            if x > 0:
                self.DecreaseZoomFactor()
                self.reInitBuffer = True
            elif x < 0:
                self.IncreaseZoomFactor()
                self.reInitBuffer = True
    

    def IncreaseZoomFactor(self):
        self.zoomFactor = self.zoomFactorIncreaseMultiplier*self.zoomFactor
        if self.zoomFactor > self.zoomFactorMax:
            self.zoomFactor = self.zoomFactorMax

    
    def DecreaseZoomFactor(self):
        self.zoomFactor = self.zoomFactorDecreaseMultiplier*self.zoomFactor
        if self.zoomFactor < self.zoomFactorMin:
            self.zoomFactor = self.zoomFactorMin
            
        
## ^^ OLD CODE ^^^


    
    ## Get and Set Methods
    
    def GetImage(self):
        return self.image    

    def SetImage(self, image):
        self.image = image
        # Clear old resized image, this tells
        # InitBuffer that there is new data
        self.resizedImage = wx.EmptyImage() 
        self.ReInitBuffer()
        
    def GetDisplayedImage(self):
        # This should return the portion of the image
        # that is actually displayed
        return self.image

    def GetZoomToFit(self):
        return self.zoomToFit

    def SetZoomToFit(self, value):
        self.zoomToFit = value
        self.ReInitBuffer()
        
    def GetIdleBuffer(self):
        return self.idleBuffer
        
    def SetIdleBuffer(self, value):
        self.idleBuffer = value

    def GetMaintainAspectRatio(self):
        return self.maintainAspectRatio        
        
    def SetMaintainAspectRatio(self, value):
        self.maintainAspectRatio = value
        self.ReInitBuffer()
        
    def GetDrawCrosshair(self):
        return self.drawCrosshair
        
    def SetDrawCrosshair(self, value):
        self.drawCrosshair = value
        self.ReInitBuffer()
                

class ImageControlPanel(wx.Panel):
    """
    This is a control panel for the ImageViewerPanel.
    """
    
    def __init__(self, parent, imageViewerPanel, id = -1):
        wx.Panel.__init__(self, parent, id)
        
        # Set the Image Viewer Panel that this Image Control Panel controls
        self.imageViewerPanel = imageViewerPanel

        # Construct controls
        self.maintainAspectRatioCheckBox = \
            wx.CheckBox(self, -1, "Maintain Aspect Ratio",
            (0, 0), (200, 20))
        self.maintainAspectRatioCheckBox.SetValue(
            self.imageViewerPanel.GetMaintainAspectRatio())
        self.Bind(wx.EVT_CHECKBOX, self.OnMaintainAspectRatioChecked,
            self.maintainAspectRatioCheckBox)

        self.idleBufferCheckBox = \
            wx.CheckBox(self, -1, "Idle Buffer", 
            (0, 20), (200, 20))
        self.idleBufferCheckBox.SetValue(
            self.imageViewerPanel.GetIdleBuffer())
        self.Bind(wx.EVT_CHECKBOX, self.OnIdleBufferChecked,
            self.idleBufferCheckBox)
            
        self.zoomToFitCheckBox = \
            wx.CheckBox(self, -1, "Zoom to Fit",
            (0, 40), (200, 20))
        self.zoomToFitCheckBox.SetValue(
            self.imageViewerPanel.GetZoomToFit())
        self.Bind(wx.EVT_CHECKBOX, self.OnZoomToFitChecked,
            self.zoomToFitCheckBox)
            
        self.drawCrosshairCheckBox = \
            wx.CheckBox(self, -1, "Draw Crosshair",
            (0, 60), (200, 20))
        self.drawCrosshairCheckBox.SetValue(
            self.imageViewerPanel.GetDrawCrosshair())
        self.Bind(wx.EVT_CHECKBOX, self.OnDrawCrosshairChecked,
            self.drawCrosshairCheckBox)
        
#        self.choice = wx.Choice(self, -1, (0, 60),
#            choices=self.imageViewerPanel.viewModes)
#        self.choice.SetSelection(self.imageViewerPanel.viewMode)
        
    # Event Handlers        
        
    def OnMaintainAspectRatioChecked(self, event):
        self.imageViewerPanel.SetMaintainAspectRatio(
            self.maintainAspectRatioCheckBox.IsChecked())
            
    def OnIdleBufferChecked(self, event):
        self.imageViewerPanel.SetIdleBuffer(
            self.idleBufferCheckBox.IsChecked())

    def OnZoomToFitChecked(self, event):
        self.imageViewerPanel.SetZoomToFit(
            self.zoomToFitCheckBox.IsChecked())        
            
    def OnDrawCrosshairChecked(self, event):
        self.imageViewerPanel.SetDrawCrosshair(
            self.drawCrosshairCheckBox.IsChecked())

class ControlledImageViewerPanel(wx.Panel):
    """
    This is an ImageViewerPanel with additional controls for 
    image panning, zooming, etc. 
    """
    
    def __init__(self, parent, id = -1):
        wx.Panel.__init__(self, parent, id)
        self.imageViewerPanel = ImageViewerPanel(self)
        self.imageControlPanel = ImageControlPanel(self, self.imageViewerPanel)
        
        # Create vertical boxsizer
        boxSizer = wx.BoxSizer(wx.VERTICAL)
        boxSizer.Add(self.imageControlPanel, 0, wx.EXPAND)
        boxSizer.Add(self.imageViewerPanel, 1, wx.EXPAND)
        self.SetSizer(boxSizer)
        
    def SetImage(self, image):
        self.imageViewerPanel.SetImage(image)


class ImageViewerFrame(wx.Frame):
    """
    This is a basic frame containing functionality to use the
    ControlledImageViewerPanel class.
    """
    # Class data
    imageWildcard = "All Files (*.*)|*.*|" \
                    "PNG (*.png)|*.png|" \
                    "JPEG (*.jpg, *.jpeg)|*.jpg;*.jpeg|" \
                    "TIFF (*.tif, *.tiff)|*.tif;*.tiff|" \
                    "BMP (*.bmp)|*.bmp|"

    def __init__(self):
        self.title = "Image Viewer"
        wx.Frame.__init__(self, None, -1, self.title, size = (800, 600))
        
        # High-level application data
        self.filename = ""
        self.currentDirectory = ""
        self.image = wx.EmptyImage()

        # Attributes 
        self.statusBar = self.createStatusBar()
        self.menuBar = self.createMenuBar()
        self.controlledImageViewerPanel = ControlledImageViewerPanel(self)

        # Add drop target
        dropTarget = MyFileDropTarget(self)
        self.SetDropTarget(dropTarget)
        
    # Get and Set Methods
    
    def SetImage(self, image):
        self.image = image
        # Set the image data of the Controlled Image ViewerPanel
        self.controlledImageViewerPanel.SetImage(self.image)
        
    def GetImage(self):
        return self.image
         
        
    # Event Handlers        
    def OnOpen(self, event):
        dlg = wx.FileDialog(self, "Open image...",
                os.getcwd(), style=wx.OPEN,
                wildcard = self.imageWildcard)
        if self.currentDirectory:
            dlg.SetDirectory(self.currentDirectory)                
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetPath()
            self.OpenImage()
        dlg.Destroy()

    def OpenImage(self):        
        # This code imports the image
        if self.filename:
            self.SetTitle(self.title + ' - ' +
                os.path.split(self.filename)[1])
            self.currentDirectory = os.path.split(self.filename)[0]
            fileExtension = os.path.splitext(self.filename)[1].lower()
            if fileExtension == ".png":
                self.SetImage(wx.Image(self.filename, wx.BITMAP_TYPE_PNG))
            elif fileExtension == ".jpg" or fileExtension == ".jpeg":
                self.SetImage(wx.Image(self.filename, wx.BITMAP_TYPE_JPEG))
            elif fileExtension == ".tif" or fileExtension == ".tiff":
                self.SetImage(wx.Image(self.filename, wx.BITMAP_TYPE_TIF))
            elif fileExtension == ".bmp":
                self.SetImage(wx.Image(self.filename, wx.BITMAP_TYPE_BMP))
            else:
                # nolog = wx.LogNull() # Uncommenting will not log errors
                self.SetImage(wx.Image(self.filename, wx.BITMAP_TYPE_ANY))
                #del nolog
                    
#         if self.filename:
#             try:
#                 self.SetTitle(self.title + ' - ' +
#                     os.path.split(self.filename)[1])
#                 self.currentDirectory = os.path.split(self.filename)[0]
#                 fileExtension = os.path.splitext(self.filename)[1].lower()
#                 if fileExtension == ".png":
#                     self.SetImage(wx.Image(self.filename, wx.BITMAP_TYPE_PNG))
#                 elif fileExtension == ".jpg" or fileExtension == ".jpeg":
#                     self.SetImage(wx.Image(self.filename, wx.BITMAP_TYPE_JPEG))
#                 elif fileExtension == ".tif" or fileExtension == ".tiff":
#                     self.SetImage(wx.Image(self.filename, wx.BITMAP_TYPE_TIF))
#                 elif fileExtension == ".bmp":
#                     self.SetImage(wx.Image(self.filename, wx.BITMAP_TYPE_BMP))
#                 else:
#                     # nolog = wx.LogNull() # Uncommenting will not log errors
#                     self.SetImage(wx.Image(self.filename, wx.BITMAP_TYPE_ANY))
#                     #del nolog
#             except:
#                 wx.MessageBox("Error importing %s." % self.filename, "oops!",
#                     stype=wx.OK|wx.ICON_EXCLAMATION)        
        
    def OnCloseWindow(self, event):
        self.Destroy()        
        
    def OnCopy(self, event):
        if self.outputImagePanel.image.IsOk():
            data = wx.BitmapDataObject()
            data.SetBitmap(wx.BitmapFromImage(self.GetImage()))
            if wx.TheClipboard.Open():
                wx.TheClipboard.SetData(data)
                wx.TheClipboard.Close()
            else:
                wx.MessageBox("Unable to open the clipboard", "Error")
        
    def OnPaste(self, event):
        success = False
        data = wx.BitmapDataObject()
        if wx.TheClipboard.Open():
            success = wx.TheClipboard.GetData(data)
            wx.TheClipboard.Close()
        if success:
            self.SetImage(wx.ImageFromBitmap(data.GetBitmap()))
        
    def createStatusBar(self):
        self.statusbar = self.CreateStatusBar()
        # self.statusbar.SetFieldsCount(3)
        # self.statusbar.SetStatusWidths([200, -2, -3])        

    def menuData(self):
        return (("&File",
                    ("&Open...\tCtrl-O",    "Open image",
                        self.OnOpen),
                    ("&Quit\tCtrl-Q",       "Quit",
                        self.OnCloseWindow)),
                ("&Edit",
                    ("&Copy\tCtrl-C",       "Copy image",   
                        self.OnCopy),
                    ("&Paste\tCtrl-V",      "Paste image",  
                        self.OnPaste))
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
        

class MyFileDropTarget(wx.FileDropTarget):

    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window
    
    def OnDropFiles(self, x, y, filenames):
        if len(filenames) > 1:
            dlg = wx.MessageBox( 
                "This application only supports opening a single image.",
                "Multiple images detected", wx.OK | wx.ICON_EXCLAMATION)
            return
        self.window.filename = filenames[0]
        self.window.OpenImage()
        

if __name__ == "__main__":
    app = wx.App()
    frame = ImageViewerFrame()
    frame.Show()
    app.MainLoop()
    
    
    
    
    
    
    
    
    
    
    
    
    
            
        
        
        
     