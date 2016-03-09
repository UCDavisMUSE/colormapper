import wx
import os
import math

# To Do:
#   - Create an eyedropper tool (simple crosshair first, then
#       more complicated with a zoom loupe)
#   - A mouse mode where one can adjust brightness
#       and contrast by scrubbing along X and Y directions
#   - What is the best way to ignore accidental right-click while
#       holding down left-click (and vice-versa)?
#       Could introduce a flag, but I feel th0at there must
#       be a better way.


class ImageViewerPanel(wx.Panel):

    def __init__(self, parent, id = -1):
        wx.Panel.__init__(self, parent, id)
                                    
        # Default Parameters
        self.SetBackgroundColour("Black")        
        self.resizeMethod = wx.IMAGE_QUALITY_BOX_AVERAGE
        # wx.IMAGE_QUALITY_NEAREST: 
        #   Simplest and fastest algorithm.
        # wx.IMAGE_QUALITY_BILINEAR: 
        #   Compromise between wxIMAGE_QUALITY_NEAREST and
        #   wxIMAGE_QUALITY_BICUBIC.
        # wx.IMAGE_QUALITY_BICUBIC: 
        #   Highest quality but slowest execution time.
        # wx.IMAGE_QUALITY_BOX_AVERAGE: 
        #   Use surrounding pixels to calculate an
        #   average that will be used for new pixels. 
        #   This method is typically used when reducing
        #   the size of an image.
        # wx.IMAGE_QUALITY_NORMAL:
        #   Default image resizing algorithm used 
        #   by wxImage::Scale(). Currently the same 
        #   as wxIMAGE_QUALITY_NEAREST.
        # wx.IMAGE_QUALITY_HIGH: 
        #   Best image resizing algorithm. Since 
        #   version 2.9.2 this results in 
        #   wxIMAGE_QUALITY_BOX_AVERAGE being used when
        #   reducing the size of the image (meaning that 
        #   both the new width and height will be smaller 
        #   than the original size). 
        #   Otherwise wxIMAGE_QUALITY_BICUBIC is used.
        
        # Default Parameters
        self.maintainAspectRatio = True
        self.idleBuffer = False
        self.zoomToFit = False
        self.drawCrosshair = False
        self.drawRectangle = False
        self.mouseModes = [
            'Disabled',
            'Pan',
            'Zoom',
            'Eyedropper']
        self.mouseMode = 1
        self.zoomValues = [0.03125, 0.0625, 0.125, 0.25, 0.5, 0.75, 1.0, 
            1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0]
        self.actualSizeZoomIndex = 6
        self.zoomIndex = self.actualSizeZoomIndex
        self.zoomValue = self.zoomValues[self.zoomIndex]
        # Zoom in x and y directions        
        self.userScale = (self.zoomValue, self.zoomValue)
        # Used in ZoomToClick calculation
        self.oldUserScale = (self.zoomValue, self.zoomValue)
        self.panBorder = 50
        
        # Temporary state variables
        self.displayWidth = 1
        self.displayHeight = 1
        self.imageWidth = 1
        self.imageHeight = 1        
        self.clickPosition = (0, 0)
        self.dragPosition = (0, 0)
        self.translation = (0, 0) # Prior to userScale (screen coordinates)
        self.oldTranslation = (0, 0)
        self.buffer = None # This is the entire dc buffer
        self.image = wx.EmptyImage() # Initialize with an empty image
        self.bitmap = wx.EmptyBitmap(1, 1) # This is a bitmap of the resized
        self.copyDisplayedBitmap = False
        self.displayedBitmap = wx.EmptyBitmap(1, 1)
        self.crosshairPosition = (0, 0)
        self.cursorInWindow = True
        
        # Initialize Buffer
        if self.idleBuffer:
            self.InitBuffer()
        
        # Bind event handlers
        self.Bind(wx.EVT_SIZE, self.OnSize)       
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        # Mouse events
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnterWindow)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)


    ## Event handlers
    
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
        if self.mouseMode == 1:
            if self.HasCapture() and event.Dragging() and event.LeftIsDown():
                newPos = event.GetPositionTuple()
                delta = (
                    newPos[0] - self.clickPosition[0],
                    newPos[1] - self.clickPosition[1])
                self.SetTranslation((
                    self.oldTranslation[0] + delta[0],
                    self.oldTranslation[1] + delta[1]))
                self.ReInitBuffer()
        if self.mouseMode == 2:
            if self.HasCapture and event.Dragging() and event.LeftIsDown():
                self.drawRectangle = True
                self.dragPosition = event.GetPositionTuple()
                self.ReInitBuffer()
                
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

    def OnLeftDown(self, event):
        self.CaptureMouse()    
        if self.mouseMode == 1:
            self.clickPosition = event.GetPositionTuple()
            self.oldTranslation = self.GetTranslation()
        if self.mouseMode == 2:
            self.clickPosition = event.GetPositionTuple()
        
    def OnLeftUp(self, event):
        if self.HasCapture():
            if self.mouseMode == 1:
                self.ReInitBuffer() #Probably unneccessary?
            if self.mouseMode == 2:
                if self.drawRectangle:
                    self.ZoomToRectangle()
                    self.drawRectangle = False
                    self.ReInitBuffer() # Needed to clear the rectangle
                else:
                    self.IncreaseZoomValue(self.clickPosition)
            self.ReleaseMouse()    
            
    def OnRightDown(self, event):
        self.CaptureMouse()    
        if self.mouseMode == 2:
            self.clickPosition = event.GetPositionTuple()
        
    def OnRightUp(self, event):
        if self.HasCapture():
            if self.mouseMode == 2:
                self.DecreaseZoomValue(self.clickPosition)            
            self.ReleaseMouse()
        
    def OnMouseWheel(self, event):
        if self.mouseMode == 1 or self.mouseMode == 2:
            x = event.GetWheelRotation()
            if x > 0:
                self.DecreaseZoomValue(event.GetPositionTuple())
            elif x < 0:
                self.IncreaseZoomValue(event.GetPositionTuple())
                
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
            
        if self.zoomToFit:
            if self.maintainAspectRatio:
                self.zoomValue = min(
                    1.0*self.displayWidth/self.imageWidth,
                    1.0*self.displayHeight/self.imageHeight)
                self.userScale = (self.zoomValue, self.zoomValue)
                # Set translation to center
                self.CenterImage()                
            else:
                self.userScale = (
                    1.0*self.displayWidth/self.imageWidth,
                    1.0*self.displayHeight/self.imageHeight)
                self.zoomValue = None
                self.SetTranslation((0, 0))
        else:
            # Draw image with current width, height, and
            # translation as calculated in zoom methods
            pass
                            
        dc.SetUserScale(self.userScale[0], self.userScale[1])
        dc.DrawBitmap(self.bitmap, 
            1.0*self.translation[0]/self.userScale[0],
            1.0*self.translation[1]/self.userScale[1], True)
            
        if self.copyDisplayedBitmap:
            self.displayedBitmap = dc.GetAsBitmap()
            self.copyDisplayedBitmap = False

        # Draw all lines at user scale (1, 1)            
        dc.SetUserScale(1, 1)
      
        if self.drawCrosshair and self.cursorInWindow:
            # Draws crosshair
            dc.DrawLine(
                0, 
                self.crosshairPosition[1],
                self.displayWidth,
                self.crosshairPosition[1])
            dc.DrawLine(
                self.crosshairPosition[0],
                0,
                self.crosshairPosition[0],
                self.displayHeight)
                
        if self.drawRectangle:
            # Draws a rectangle for zooming into an ROI
            dc.DrawLine(
                self.clickPosition[0],
                self.clickPosition[1],
                self.clickPosition[0],
                self.dragPosition[1])
            dc.DrawLine(
                self.clickPosition[0],
                self.dragPosition[1],
                self.dragPosition[0],
                self.dragPosition[1])
            dc.DrawLine(
                self.dragPosition[0],
                self.dragPosition[1],
                self.dragPosition[0],
                self.clickPosition[1])
            dc.DrawLine(
                self.dragPosition[0],
                self.clickPosition[1],
                self.clickPosition[0],
                self.clickPosition[1])
        
    def ReInitBuffer(self):
        if self.idleBuffer:
            self.reInitBuffer = True
        else:
            self.InitBuffer()
            self.Refresh()
               
    def CenterImage(self):
        self.SetTranslation((
            0.5*self.displayWidth - 0.5*self.userScale[0]*self.imageWidth,
            0.5*self.displayHeight - 0.5*self.userScale[1]*self.imageHeight))
            
    def CenterImageAndReInitBuffer(self):
        self.CenterImage()
        self.ReInitBuffer()
        
    def IncreaseZoomValue(self, clickPosition = None):
        # Ensure zoomToFit is off, maintainAspectRatio is on (for now)
        self.zoomToFit = False
        self.maintainAspectRatio = True
        # First find the next highest zoom level
        self.zoomValue = next(
            (x for x in self.zoomValues if x > self.zoomValue),
            self.zoomValues[-1])
        self.zoomIndex = self.zoomValues.index(self.zoomValue)
        self.SetUserScale((self.zoomValue, self.zoomValue))
        self.ZoomToClick(clickPosition)        
        # Redraw
        self.ReInitBuffer()
        
    def DecreaseZoomValue(self, clickPosition = None):
        # Ensure zoomToFit is off, maintainAspectRatio is on (for now)
        self.zoomToFit = False
        self.maintainAspectRatio = True
        # First find the next lowest zoom level
        self.zoomValue = next(
            (x for x in reversed(self.zoomValues) if x < self.zoomValue),
            self.zoomValues[0])
        self.zoomIndex = self.zoomValues.index(self.zoomValue)
        self.SetUserScale((self.zoomValue, self.zoomValue))  
        self.ZoomToClick(clickPosition)        
        # Redraw
        self.ReInitBuffer()
        
    def ActualSizeZoomValue(self, clickPosition = None):
        # Ensure zoomToFit is off, maintainAspectRatio is on (for now)
        self.zoomToFit = False
        self.maintainAspectRatio = True
        # Set zoomValue at 1.0
        self.zoomIndex = self.actualSizeZoomIndex
        self.zoomValue = self.zoomValues[self.zoomIndex]
        self.SetUserScale((self.zoomValue, self.zoomValue))
        self.ZoomToClick(clickPosition)
        # Redraw
        self.ReInitBuffer()
        
    def ZoomToClick(self, clickPosition = None):
        if clickPosition is None:
            self.clickPosition = (0.5*self.displayWidth,
                0.5*self.displayHeight)
        else:
            self.clickPosition = clickPosition
        self.SetTranslation((
            self.clickPosition[0]
            - 1.0*self.userScale[0]*(self.clickPosition[0]
                - self.translation[0])/self.oldUserScale[0],
            self.clickPosition[1]
            - 1.0*self.userScale[1]*(self.clickPosition[1]
                - self.translation[1])/self.oldUserScale[1]))

    def ZoomToRectangle(self):
        """
        This zooms to a rectangle defined by self.clickPosition and
        self.dragPosition
        """
        # Ensure zoomToFit is off, maintainAspectRatio is on (for now)
        self.zoomToFit = False
        self.maintainAspectRatio = True
        # Calculate rectangle size and center position               
        rectWidth = abs(self.clickPosition[0] - self.dragPosition[0])
        rectHeight = abs(self.clickPosition[1] - self.dragPosition[1])
        rectCenterPosition = (
            0.5*(self.clickPosition[0] + self.dragPosition[0]),
            0.5*(self.clickPosition[1] + self.dragPosition[1]))
        # Note: we are calculating the increase/decrease in the zoomValue
        self.zoomValue = self.zoomValue*min(
            1.0*self.displayWidth/rectWidth,
            1.0*self.displayHeight/rectHeight)
        self.zoomIndex = None # Indicate not a valid zoom index
        # If zoomValue goes beyond maximum allowed zoom, set to maximum
        if self.zoomValue > self.zoomValues[-1]:
            self.zoomValue = self.zoomValues[-1]
            self.zoomIndex = self.zoomValues.index(self.zoomValue)

            
        self.zoomValue = min(self.zoomValue, self.zoomValues[-1])
        self.SetUserScale((self.zoomValue, self.zoomValue))
        self.SetTranslation((
            0.5*self.displayWidth 
            - 1.0*self.userScale[0]*(rectCenterPosition[0]
                - self.translation[0])/self.oldUserScale[0],
            0.5*self.displayHeight
            - 1.0*self.userScale[1]*(rectCenterPosition[1]
                - self.translation[1])/self.oldUserScale[1]))
        # Redraw
        self.ReInitBuffer()
        
    ## Get and Set Methods
    
    def GetImage(self):
        return self.image    

    def SetImage(self, image):
        self.image = image
        self.bitmap = wx.BitmapFromImage(self.image)
        (self.imageWidth, self.imageHeight) = self.image.GetSize()
        self.CenterImage()
        self.ReInitBuffer()        
        
    def GetDisplayedBitmap(self):
        self.copyDisplayedBitmap = True
        # Always force InitBuffer (versus calling ReInitBuffer())
        self.InitBuffer()
        self.Refresh()
        return self.displayedBitmap
        
    def SetUserScale(self, scale = (1, 1)):
        self.oldUserScale = self.userScale
        self.userScale = scale
        
    def GetUserScale(self):
        return self.userScale
        
    def GetTranslation(self):
        return self.translation        
        
    def SetTranslation(self, translation = (0, 0)):
        self.translation = translation
        # Constrain translation so the image does not
        # leave the frame
        self.translation = (
            max(
                min(1.0*self.translation[0], 
                self.displayWidth - self.panBorder),
                self.panBorder - 
                    1.0*self.userScale[0]*self.imageWidth),
            max(
                min(1.0*self.translation[1],
                self.displayHeight - self.panBorder),
                self.panBorder - 
                    1.0*self.userScale[1]*self.imageHeight))                    
        
    def GetZoomToFit(self):
        return self.zoomToFit

    def SetZoomToFit(self, value):
        self.zoomToFit = value
        self.zoomIndex = None
        self.ReInitBuffer()
        
    def GetZoomValue(self):
        return self.zoomValue
        
    def GetZoomIndex(self):
        return self.zoomIndex
        
    def SetZoomIndex(self, index):
        # Ensure zoomToFit is off, maintainAspectRatio is on (for now)
        self.zoomToFit = False
        self.maintainAspectRatio = True
        # Set zoomValue at 1.0
        self.zoomIndex = index
        self.zoomValue = self.zoomValues[self.zoomIndex]
        self.SetUserScale((self.zoomValue, self.zoomValue))
        self.ZoomToClick()
        # Redraw
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
 
    def SetMouseMode(self, value):
        self.mouseMode = value
        
    def GetMouseMode(self):
        return self.mouseMode


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

        self.idleBufferCheckBox = \
            wx.CheckBox(self, -1, "Idle Buffer", 
            (0, 20), (200, 20))
        self.idleBufferCheckBox.SetValue(
            self.imageViewerPanel.GetIdleBuffer())
            
        self.zoomToFitCheckBox = \
            wx.CheckBox(self, -1, "Zoom to Fit",
            (0, 40), (200, 20))
        self.zoomToFitCheckBox.SetValue(
            self.imageViewerPanel.GetZoomToFit())
            
        self.drawCrosshairCheckBox = \
            wx.CheckBox(self, -1, "Draw Crosshair",
            (0, 60), (200, 20))
        self.drawCrosshairCheckBox.SetValue(
            self.imageViewerPanel.GetDrawCrosshair())
            
        self.zoomOutButton = \
            wx.Button(self, -1, "Zoom Out",
            (0, 80), (100, 20))

        self.zoomInButton = \
            wx.Button(self, -1, "Zoom In",
            (100, 80), (100, 20))

        self.actualSizeButton = \
            wx.Button(self, -1, "Actual Size",
            (200, 80), (100, 20))
            
        zoomChoices = [100.0*x for x in self.imageViewerPanel.zoomValues]
        zoomChoices = map(str, zoomChoices)
        zoomChoices = [x + "%" for x in zoomChoices]
        self.zoomComboBox = \
            wx.ComboBox(self, -1,
            ("%.1f" % (100.0*self.imageViewerPanel.GetZoomValue())) + "%",
            (320, 82), (100, 26),
            choices = zoomChoices,
            style = wx.CB_DROPDOWN)
        self.zoomComboBox.SetEditable(False)

        self.mouseChoice = \
            wx.Choice(self, -1,
            (0, 112), (100, 20),
            choices = self.imageViewerPanel.mouseModes)
        self.mouseChoice.SetSelection(self.imageViewerPanel.GetMouseMode())
        self.Bind(wx.EVT_CHOICE, self.OnMouseChoice, self.mouseChoice)
        
        self.centerImageButton = \
            wx.Button(self, -1, "Center Image",
            (0, 140), (100, 20))
            
        # Initialie UI State
        self.InitUIState()
        self.reInitUIState = False            
            
        # Bind event handlers
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_IDLE, self.OnIdle)        
        # Controls
        self.Bind(wx.EVT_CHECKBOX, self.OnMaintainAspectRatioChecked,
            self.maintainAspectRatioCheckBox)
        self.Bind(wx.EVT_CHECKBOX, self.OnIdleBufferChecked,
            self.idleBufferCheckBox)
        self.Bind(wx.EVT_CHECKBOX, self.OnZoomToFitChecked,
            self.zoomToFitCheckBox)
        self.Bind(wx.EVT_CHECKBOX, self.OnDrawCrosshairChecked,
            self.drawCrosshairCheckBox)
        self.Bind(wx.EVT_BUTTON, self.OnZoomOutButton, 
            self.zoomOutButton)
        self.Bind(wx.EVT_BUTTON, self.OnZoomInButton, 
            self.zoomInButton)
        self.Bind(wx.EVT_BUTTON, self.OnActualSizeButton, 
            self.actualSizeButton)
        self.Bind(wx.EVT_COMBOBOX, self.OnZoomComboBoxChoice,
            self.zoomComboBox)
        self.Bind(wx.EVT_BUTTON, self.OnCenterImageButton,
            self.centerImageButton)
        # Mouse events
        self.imageViewerPanel.Bind(wx.EVT_LEFT_UP, self.OnLeftOrRightUp)
        self.imageViewerPanel.Bind(wx.EVT_RIGHT_UP, self.OnLeftOrRightUp)
        self.imageViewerPanel.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)

    # Event Handlers
    
    def OnSize(self, event):
        if self.imageViewerPanel.GetZoomToFit():
            self.reInitUIState = True
    
    def OnIdle(self, event):
        if self.reInitUIState:
            self.InitUIState()
            self.reInitUIState = False
#         if self.idleBuffer and self.reInitBuffer:
#             self.InitBuffer()
#             self.Refresh()
#         self.reInitBuffer = False
    
    
    def InitUIState(self):
        """
        This sets the Control Panel UI State to reflect
        that of the ImageViewerPanel
        """
        if self.imageViewerPanel.GetZoomIndex() is None:
            # Set explicitly to zoom level
            self.zoomComboBox.SetValue(
                ("%.1f" % (100.0*self.imageViewerPanel.GetZoomValue())) + "%")
        else:
            self.zoomComboBox.SetSelection(
                self.imageViewerPanel.GetZoomIndex())          
        
    def OnMaintainAspectRatioChecked(self, event):
        self.imageViewerPanel.SetMaintainAspectRatio(
            self.maintainAspectRatioCheckBox.IsChecked())
        self.zoomComboBox.Enable(
            self.imageViewerPanel.GetMaintainAspectRatio())
            
    def OnIdleBufferChecked(self, event):
        self.imageViewerPanel.SetIdleBuffer(
            self.idleBufferCheckBox.IsChecked())

    def OnZoomToFitChecked(self, event):
        self.imageViewerPanel.SetZoomToFit(
            self.zoomToFitCheckBox.IsChecked())
        self.zoomComboBox.Enable(
            self.imageViewerPanel.GetMaintainAspectRatio())
        self.reInitUIState = True
            
    def OnDrawCrosshairChecked(self, event):
        self.imageViewerPanel.SetDrawCrosshair(
            self.drawCrosshairCheckBox.IsChecked())
            
    def OnZoomOutButton(self, event):
        self.imageViewerPanel.DecreaseZoomValue()
        self.zoomComboBox.SetSelection(self.imageViewerPanel.GetZoomIndex())
        self.zoomToFitCheckBox.SetValue(False)
        self.zoomComboBox.Enable(True)        
                
    def OnZoomInButton(self, event):
        self.imageViewerPanel.IncreaseZoomValue()
        self.zoomComboBox.SetSelection(self.imageViewerPanel.GetZoomIndex())
        self.zoomToFitCheckBox.SetValue(False)
        self.zoomComboBox.Enable(True)
        
    def OnActualSizeButton(self, event):
        self.imageViewerPanel.ActualSizeZoomValue()
        self.zoomComboBox.SetSelection(self.imageViewerPanel.GetZoomIndex())
        self.zoomToFitCheckBox.SetValue(False)
        self.zoomComboBox.Enable(True)
                
    def OnZoomComboBoxChoice(self, event):
        self.imageViewerPanel.SetZoomToFit(False)    
        self.imageViewerPanel.SetZoomIndex(self.zoomComboBox.GetSelection())
        self.zoomToFitCheckBox.SetValue(False)
        
    def OnMouseChoice(self, event):
        self.imageViewerPanel.SetMouseMode(self.mouseChoice.GetSelection())
        
    def OnCenterImageButton(self, event):
        self.imageViewerPanel.CenterImageAndReInitBuffer()
        
    # Mouse event handlers
    
    def OnLeftOrRightUp(self, event):
        if self.imageViewerPanel.GetMouseMode() == 2:
            self.reInitUIState = True
        event.Skip()

    def OnMouseWheel(self, event):
        # The zoom level may change upon mouse wheel
        if (self.imageViewerPanel.GetMouseMode() == 1 or
            self.imageViewerPanel.GetMouseMode() == 2):
            self.reInitUIState = True
        event.Skip() 

        

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
        
    # Get and Set Methods
    
    def SetImage(self, image):
        self.image = image
        # Set the image data of the Controlled Image ViewerPanel
        self.controlledImageViewerPanel.SetImage(self.image)
        
    def GetImage(self):
        return self.image

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
    