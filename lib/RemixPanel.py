import wx
from ColorButton import ColorButton

class RemixPanel(wx.Panel):
    # Data Defaults
    backgroundColor = (230, 160, 200)
    backgroundSpectrum = (36, 138, 80)
    backgroundThresh = 0.0
    backgroundGain = 1.0
    backgroundGamma = 1.0
    nucleiColor = ( 70,  30, 150)
    nucleiSpectrum = (92, 111, 52)
    nucleiThresh = 0.0
    nucleiGain = 1.0
    nucleiGamma = 1.0
    remixMode = 0
    
    # 
    recomputeRemix = False


    def __init__(self, parent, id = -1):
    
        # Construct Controls
        wx.Panel.__init__(self, parent, id)
        wx.StaticText(self, -1, "Remix Controls")
        
        wx.StaticText(self, -1, "Bulk Tissue:", pos = (0, 25))
        self.colorButtonBackgroundColor = ColorButton(self, -1,
            color = self.backgroundColor, pos = (100, 25),
            size = (20, 20))
        wx.Button(self, -1, label = "+", pos = (125, 19), size = (25, 25))
        wx.StaticText(self, -1, "Spectrum:", pos = (170, 25))
        self.colorButtonBackgroundSpectrum = ColorButton(self, -1,
            color = self.backgroundSpectrum, pos = (250, 25),
            size = (20, 20))
        wx.StaticText(self, -1, "Thresh:", pos = (0, 50))
        wx.Slider(self, -1, self.backgroundThresh, 0, 100, pos=(80, 50),
                   size=(200, -1),
                  style=wx.SL_HORIZONTAL)
        wx.SpinCtrl(self, -1, str(self.backgroundThresh), (300, 50), (100, -1))
        wx.StaticText(self, -1, "Gain:", pos = (0, 75))
        wx.Slider(self, -1, self.backgroundGain, 0, 100, pos=(80, 75),
                   size=(200, -1),
                  style=wx.SL_HORIZONTAL)
        wx.SpinCtrl(self, -1, str(self.backgroundGain), (300, 75), (100, -1))
        wx.StaticText(self, -1, "Gamma:", pos = (0, 100))
        wx.Slider(self, -1, self.backgroundGamma, 0, 100, pos=(80, 100),
                   size=(200, -1),
                  style=wx.SL_HORIZONTAL)
        wx.SpinCtrl(self, -1, str(self.backgroundGamma), (300, 100), (100, -1))
        
        wx.StaticText(self, -1, "Nuclei:", pos = (0, 125))
        self.colorButtonNucleiColor = ColorButton(self, -1,
            color = self.nucleiColor, pos = (100, 125),
            size = (20, 20))
        wx.Button(self, -1, label = "+", pos = (125, 119), size = (25, 25))
        wx.StaticText(self, -1, "Spectrum:", pos = (170, 125))
        self.colorButtonNucleiSpectrum = ColorButton(self, -1,
            color = self.nucleiSpectrum, pos = (250, 125),
            size = (20, 20))
        wx.StaticText(self, -1, "Thresh:", pos = (0, 150))
        wx.Slider(self, -1, self.nucleiThresh, 0, 100, pos=(80, 150),
                   size=(200, -1),
                  style=wx.SL_HORIZONTAL)
        wx.SpinCtrl(self, -1, str(self.nucleiThresh), (300, 150), (100, -1))
        wx.StaticText(self, -1, "Gain:", pos = (0, 175))
        wx.Slider(self, -1, self.nucleiGain, 0, 100, pos=(80, 175),
                   size=(200, -1),
                  style=wx.SL_HORIZONTAL)
        wx.SpinCtrl(self, -1, str(self.nucleiGain), (300, 175), (100, -1))
        wx.StaticText(self, -1, "Gamma:", pos = (0, 200))
        wx.Slider(self, -1, self.nucleiGamma, 0, 100, pos=(80, 200),
                   size=(200, -1),
                  style=wx.SL_HORIZONTAL)
        wx.SpinCtrl(self, -1, str(self.nucleiGamma), (300, 200), (100, -1))
        
        wx.StaticText(self, -1, "Remix Mode:", pos = (0, 225))
        self.choiceRemixMode = wx.Choice(self, -1, pos = (100, 225), 
            choices = (
                "Brightfield (Beer-Lambert)",
                "Brightfield (Invert-Multiply)",
                "Fluorescence"))
        self.choiceRemixMode.SetSelection(self.remixMode)
        

        # Event Handlers
        self.Bind(wx.EVT_BUTTON, self.OnColorButtonBackgroundColorClick,
            self.colorButtonBackgroundColor)
        self.Bind(wx.EVT_BUTTON, self.OnColorButtonBackgroundSpectrumClick,
            self.colorButtonBackgroundSpectrum)
        self.Bind(wx.EVT_BUTTON, self.OnColorButtonNucleiColorClick,
            self.colorButtonNucleiColor)
        self.Bind(wx.EVT_BUTTON, self.OnColorButtonNucleiSpectrumClick,
            self.colorButtonNucleiSpectrum)      
            
        self.Bind(wx.EVT_IDLE, self.OnIdle)
                                  

                
    def OnColorButtonBackgroundColorClick(self, event):
        self.backgroundColor = \
            self.colorButtonBackgroundColor.GetBackgroundColour()[0:3]
        norm = self.backgroundColor[0] + self.backgroundColor[1] \
            + self.backgroundColor[2]
        self.backgroundSpectrum = (
            int(round(255.0*self.backgroundColor[0]/norm)),
            int(round(255.0*self.backgroundColor[1]/norm)),
            int(round(255.0*self.backgroundColor[2]/norm)))
        self.colorButtonBackgroundSpectrum.SetBackgroundColour( \
            self.backgroundSpectrum)
        self.colorButtonBackgroundSpectrum.Refresh()
        self.recomputeRemix = True
        
    def OnColorButtonBackgroundSpectrumClick(self, event):
        self.colorButtonBackgroundColor.SetBackgroundColour(
            self.colorButtonBackgroundSpectrum.GetBackgroundColour()[0:3])
        self.colorButtonBackgroundColor.Refresh()
        self.backgroundColor = \
            self.colorButtonBackgroundColor.GetBackgroundColour()[0:3]
        norm = self.backgroundColor[0] + self.backgroundColor[1] \
            + self.backgroundColor[2]
        self.backgroundSpectrum = (
            int(round(255.0*self.backgroundColor[0]/norm)),
            int(round(255.0*self.backgroundColor[1]/norm)),
            int(round(255.0*self.backgroundColor[2]/norm)))
        self.colorButtonBackgroundSpectrum.SetBackgroundColour( \
            self.backgroundSpectrum)
        self.colorButtonBackgroundSpectrum.Refresh()
        self.recomputeRemix = True

    def OnColorButtonNucleiColorClick(self, event):
        self.nucleiColor = \
            self.colorButtonNucleiColor.GetBackgroundColour()[0:3]
        norm = self.nucleiColor[0] + self.nucleiColor[1] \
            + self.nucleiColor[2]
        self.nucleiSpectrum = (
            int(round(255.0*self.nucleiColor[0]/norm)),
            int(round(255.0*self.nucleiColor[1]/norm)),
            int(round(255.0*self.nucleiColor[2]/norm)))
        self.colorButtonNucleiSpectrum.SetBackgroundColour( \
            self.nucleiSpectrum)
        self.colorButtonNucleiSpectrum.Refresh()
        self.recomputeRemix = True
        
    def OnColorButtonNucleiSpectrumClick(self, event):
        self.colorButtonNucleiColor.SetBackgroundColour(
            self.colorButtonNucleiSpectrum.GetBackgroundColour()[0:3])
        self.colorButtonNucleiColor.Refresh()            
        self.nucleiColor = \
            self.colorButtonNucleiColor.GetBackgroundColour()[0:3]
        norm = self.nucleiColor[0] + self.nucleiColor[1] \
            + self.nucleiColor[2]
        self.nucleiSpectrum = (
            int(round(255.0*self.nucleiColor[0]/norm)),
            int(round(255.0*self.nucleiColor[1]/norm)),
            int(round(255.0*self.nucleiColor[2]/norm)))
        self.colorButtonNucleiSpectrum.SetBackgroundColour( \
            self.nucleiSpectrum)
        self.colorButtonNucleiSpectrum.Refresh()
        self.recomputeRemix = True

    def OnIdle(self, event):
        if self.recomputeRemix:
            print("Remixing...")
            self.recomputeRemix = False         

        
        
    
if __name__ == "__main__":
    app = wx.App()
    frame = wx.Frame(None,title = "Test Frame")
    frame.SetSize((600,400))
    unmixPanel = RemixPanel(frame)
    frame.Show()
    app.MainLoop()