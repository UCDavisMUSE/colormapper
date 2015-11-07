import wx

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
            self.outputImagePanel.image = self.inputImagePanel.image.Mirror()
            self.outputImagePanel.reInitBuffer = True
#            self.computeButton.Show(False) # Can be used to hide UI