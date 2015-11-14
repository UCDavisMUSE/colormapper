import wx
import numpy as np
import colormappingMethods
from ColorButton import ColorButton



class ControlPanel(wx.Panel):
    def __init__(self, parent, inputImagePanel, outputImagePanel, ID = -1, label = "",
                pos = wx.DefaultPosition, size = wx.DefaultSize):
        wx.Panel.__init__(self, parent, ID, pos, size, wx.NO_BORDER, label)
        self.inputImagePanel = inputImagePanel
        self.outputImagePanel = outputImagePanel
                
        # ControlPanel attributes
        # Panel for buttons
        self.buttonPanel = wx.Panel(self, size = (120, 40))
        self.computeButton = wx.Button(self.buttonPanel, label = "Compute", size = (100, 20))
        
        # Add input and output colors
        self.numberOfColors = 3
        self.inputColors  = [ (  0,   0,   0), (228, 250, 166), (244, 205, 100) ]
        self.outputColors = [ (255, 255, 255), ( 70,  30, 150), (230, 160, 200) ]


        self.labels = map(str, range(self.numberOfColors))        
        (box1, self.inputColorButtons) = self.MakeColorButtonsBoxSizer("Input Colors", self.inputColors)
        (box2, self.outputColorButtons) = self.MakeColorButtonsBoxSizer("Output Colors", self.outputColors)

        # Arrange the input and output colors side-by-side
        horizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
        horizontalSizer.Add(box1, 1, flag=wx.EXPAND)
        horizontalSizer.Add(box2, 1, flag=wx.EXPAND)

        # Arrange the controls below input and output colors
        verticalSizer = wx.BoxSizer(wx.VERTICAL)
        verticalSizer.Add(horizontalSizer, 0, flag=wx.EXPAND)
        verticalSizer.Add(self.buttonPanel, 1, flag=wx.ALIGN_RIGHT)

        # Set the sizer to be the verticalSizer
        self.SetSizer(verticalSizer)
        verticalSizer.Fit(self)

        # Event handlers
        self.Bind(wx.EVT_BUTTON, self.OnComputeButtonClick, self.computeButton)


    def MakeColorButtonsBoxSizer(self, boxlabel, buttonColors):
        box = wx.StaticBox(self, -1, boxlabel)
        sizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        colorButtons = []
        for color in buttonColors:
            colorButton = ColorButton(self, color = color, size = (30, 30))
            sizer.Add(colorButton, 1, wx.ALL, 1)
            colorButtons.append(colorButton)
        
        return (sizer, colorButtons)

        
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
            
            # Do image processing and color conversion here
            X = np.array([ [  0, 228, 244],
                           [  0, 250, 205],
                           [  0, 166, 100] ])
               
            Y = np.array([ [255,  70, 230],
                           [255,  30, 160],
                           [255, 150, 200] ])

            (A, c) = colormappingMethods.learnAffineColorspaceMap(X,Y)

            outputImageArray = colormappingMethods.applyAffineColorspaceMap(inputImageArray,A,c)
            
            # Get/set dimensions of output image
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
            