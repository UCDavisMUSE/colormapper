import wx
import numpy as np
import copy
import colormappingMethods
from ColorButton import ColorButton


class ControlPanel(wx.Panel):
    def __init__(self, parent, inputColors, inputImagePanel, outputColors, outputImagePanel, ID = -1, label = "",
                pos = wx.DefaultPosition, size = wx.DefaultSize):
        wx.Panel.__init__(self, parent, ID, pos, size, wx.NO_BORDER, label)
        self.inputColors = inputColors
        self.inputImagePanel = inputImagePanel
        self.outputColors = outputColors
        self.outputImagePanel = outputImagePanel
                
        # ControlPanel attributes
        # Panel for buttons
        self.buttonPanel = wx.Panel(self, size = (120, 40))
        self.computeButton = wx.Button(self.buttonPanel, label = "Compute", size = (100, 20), pos = (0, 0))
        
        self.choicePanel = wx.Panel(self, size = (300, 40))
        self.choiceText = wx.StaticText(self.choicePanel, -1, "Select Input Colors From:", size = (150, 30), pos = (10, 5))
        choicePos = (170, 0)
        if wx.Platform == "__WXMAC__":
            choicePos = (170, -7)
        self.choice = wx.Choice(self.choicePanel, -1, size = (130, 40), pos = choicePos, choices=("Color Picker","Input Image"))
        self.choice.SetSelection(0)
        
        self.methodText = wx.StaticText(self.choicePanel, -1, "Method:", size = (60, 30), pos = (350, 5))
        methodPos = (410, 0)
        if wx.Platform == "__WXMAC__":
            methodPos = (410, -7)
        self.methodChoice = wx.Choice(self.choicePanel, -1, size = (200, 40), pos = methodPos, choices=("Affine", "Logistic (LSQ)", "Logistic (Likelihood)", "Unmix & Brightfield (NNLS, slow)", "Unmix & Brightfield (LS)", "Unmix & Fluorescent (NNLS, slow)", "Unmix & Fluorescent (LS)"))
        self.methodChoice.SetSelection(0)

        # Add input and output colors
        (box1, self.inputColorButtons) = self.MakeColorButtonsBoxSizer("Input Colors", self.inputColors)
        (box2, self.outputColorButtons) = self.MakeColorButtonsBoxSizer("Output Colors", self.outputColors)
        
        # Arrange the input and output colors side-by-side
        horizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
        horizontalSizer.Add(box1, 1, flag=wx.EXPAND)
        horizontalSizer.Add(box2, 1, flag=wx.EXPAND)
        
        # Arrange the choice panel and button panel side-by-side
        horizontalSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        horizontalSizer2.Add(self.choicePanel, 1, flag=wx.EXPAND)
        horizontalSizer2.Add(self.buttonPanel, 0, flag=wx.EXPAND)

        # Arrange the controls below input and output colors
        verticalSizer = wx.BoxSizer(wx.VERTICAL)
        verticalSizer.Add(horizontalSizer, 0, flag=wx.EXPAND)
        verticalSizer.Add(horizontalSizer2, 1, flag=wx.EXPAND)

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
            # This works, but maybe there is a cleaner way to get the colors from the buttons?
            inputColorMatrix = np.zeros((3, len(self.inputColorButtons)))
            outputColorMatrix = np.zeros((3, len(self.outputColorButtons)))
            for color in range(len(self.inputColorButtons)):
                inputColorMatrix[:, color] = self.inputColorButtons[color].GetBackgroundColour()[0:3]
            
            for color in range(len(self.outputColorButtons)):
                outputColorMatrix[:, color] = self.outputColorButtons[color].GetBackgroundColour()[0:3]

            outputImageArray = copy.copy(inputImageArray)
            if self.methodChoice.GetSelection() == 0:
                # Affine Color Map                
                (A, c) = colormappingMethods.learnAffineColorspaceMap(inputColorMatrix, outputColorMatrix)
                outputImageArray = colormappingMethods.applyAffineColorspaceMap(outputImageArray,A,c,method = 3, tileSize = (64, 64))
            elif self.methodChoice.GetSelection() == 1:
                # Logistic Color Map 
                (A, c) = colormappingMethods.learnLogisticColorspaceMap(inputColorMatrix, outputColorMatrix)
                outputImageArray = colormappingMethods.applyLogisticColorspaceMap(outputImageArray,A,c)
            elif self.methodChoice.GetSelection() == 2:
                # Logistic Color Map Gradient Descent 
                (A, c) = colormappingMethods.learnLogisticColorspaceMapGradient(inputColorMatrix, outputColorMatrix)
                outputImageArray = colormappingMethods.applyLogisticColorspaceMap(outputImageArray,A,c)
            elif self.methodChoice.GetSelection() == 3:
                # Unmix and Recolor
                outputImageArray = colormappingMethods.unmixAndRecolor(inputColorMatrix, outputColorMatrix, outputImageArray,verbose=False)
            elif self.methodChoice.GetSelection() == 4:
                # Unmix and Recolor, Least-Squares
                outputImageArray = colormappingMethods.unmixAndRecolor(inputColorMatrix, outputColorMatrix, outputImageArray,verbose=False,method='ls')
            elif self.methodChoice.GetSelection() == 5:
                # Unmix and Recolor Fluorescent
                outputImageArray = colormappingMethods.unmixAndRecolorFluorescent(inputColorMatrix, outputColorMatrix, outputImageArray,verbose=True)
            elif self.methodChoice.GetSelection() == 6:
                # Unmix and Recolor Fluorescent, Least-Squares
                outputImageArray = colormappingMethods.unmixAndRecolorFluorescent(inputColorMatrix, outputColorMatrix, outputImageArray,verbose=True,method='ls')
                


            
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
            self.outputImagePanel.newImageData = True        
            self.outputImagePanel.reInitBuffer = True
            