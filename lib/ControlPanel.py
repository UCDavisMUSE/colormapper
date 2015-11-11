import wx
import numpy as np
import colormappingMethods

class ControlPanel(wx.Panel):
    def __init__(self, parent, inputImagePanel, outputImagePanel, ID = -1, label = "",
                pos = wx.DefaultPosition, size = wx.DefaultSize):
        wx.Panel.__init__(self, parent, ID, pos, size, wx.NO_BORDER, label)
        self.inputImagePanel = inputImagePanel
        self.outputImagePanel = outputImagePanel
        
        self.panel = wx.Panel(self, -1, size = size)
        
        # ControlPanel attributes
        self.computeButton = wx.Button(self.panel, label = "Compute", pos = (0, 0))
        
        # Event handlers
        self.Bind(wx.EVT_BUTTON, self.OnComputeButtonClick, self.computeButton)
        
    def OnComputeButtonClick(self, event):
        if self.inputImagePanel.image.Ok():
            # Note: This is on the main thread, is there a way to put this
            # on a new thread as to not lock the GUI during computation?
        
            # Convert wx.Image to numpy array
            inputImageBuffer = self.inputImagePanel.image.GetDataBuffer()
            inputImageArray = np.frombuffer(inputImageBuffer, dtype='uint8')
            
            # Reshape the input numpy array to a width X height X 3 RGB image
            inputImageWidth = self.inputImagePanel.image.GetWidth()
            inputImageHeight = self.inputImagePanel.image.GetHeight()
            inputImageSize = inputImageArray.size     
            inputImageArray = inputImageArray.reshape(inputImageWidth, inputImageHeight, 3)
            # If we use OpenCV, the image is expected to be BGR
            # inputImageArray = cv2.cvtColor(inputImageArray, cv2.COLOR_RGB2BGR)
            
            # Do image processing, get dimensions of output image
            # Simple color invert as an example:
            outputImageArray = 255 - inputImageArray
            outputImageWidth = inputImageWidth
            outputImageHeight = inputImageHeight
            outputImageSize = inputImageSize
            
            # Reshape the output numpy array to a vector
            outputImageArray = outputImageArray.reshape(outputImageSize)
            
            # Convert the output numpy array to a wx.Image
            # First initialize with an empty image
            self.outputImagePanel.image = wx.EmptyImage(outputImageWidth, outputImageHeight)
            self.outputImagePanel.image.SetData(outputImageArray.tostring())

            # Tell the outputImagePanel to refresh the display            
            self.outputImagePanel.reInitBuffer = True
            