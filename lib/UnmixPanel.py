import wx
from ColorButton import ColorButton

class UnmixPanel(wx.Panel):
    # Data Defaults
    backgroundColor = (244, 205, 100)
    backgroundSpectrum = (113, 95, 46)
    nucleiColor = (228, 250, 166)
    nucleiSpectrum = (90, 99, 66)
    subtractBackground = False
    subtractBackgroundAmount = 0
    
    # Other Variables
    recomputeUnmix = False

    def __init__(self, parent, id = -1):
    
        # Construct Controls
        wx.Panel.__init__(self, parent, id)
        wx.StaticText(self, -1, "Unmix Controls:")

        wx.StaticText(self, -1, "Bulk Tissue:", pos = (0, 25))
        self.colorButtonBackgroundColor = ColorButton(self, -1, 
            color = self.backgroundColor, pos = (100, 25),
            size = (20, 20))
        self.buttonBackgroundCrosshair = wx.Button(self, -1, 
            label = "+", pos = (125, 19), size = (25, 25))
        wx.StaticText(self, -1, "Spectrum:", pos = (170, 25))
        self.colorButtonBackgroundSpectrum = ColorButton(self, -1, 
            color = self.backgroundSpectrum, pos = (250, 25),
            size = (20, 20))
            
        wx.StaticText(self, -1, "Nuclei:", pos = (0, 50))
        self.colorButtonNucleiColor = ColorButton(self, -1, 
            color = self.nucleiColor, pos = (100, 50),
            size = (20, 20))
        wx.Button(self, -1, label = "+", pos = (125, 43), size = (25, 25))
        wx.StaticText(self, -1, "Spectrum:", pos = (170, 50))
        self.colorButtonNucleiSpectrum = ColorButton(self, -1, 
            color = self.nucleiSpectrum, pos = (250, 50),
            size = (20, 20))

        self.checkBoxSubtractBackground = wx.CheckBox(self, -1,
            label = "Subtract Background (Pure Spectrum)", pos = (0, 75))
        self.checkBoxSubtractBackground.SetValue(self.subtractBackground)
        wx.StaticText(self, -1, "Amount:", pos = (0, 100))
        self.sliderSubtractBackground = wx.Slider(self, -1,
            self.subtractBackgroundAmount, 0, 100,
            pos=(70, 100), size = (220, -1),
            style = wx.SL_HORIZONTAL)
        self.spinCtrlSubtractBackground = wx.SpinCtrl(self, -1,
            "%.2f" % self.subtractBackgroundAmount,
            initial = self.subtractBackgroundAmount, min = 0, max = 100,
            pos = (290, 100), size = (100, -1),
            style = wx.SP_ARROW_KEYS)
            
            
        # Event Handlers
        self.Bind(wx.EVT_BUTTON, self.OnColorButtonBackgroundColorClick,
            self.colorButtonBackgroundColor)
        self.Bind(wx.EVT_BUTTON, self.OnColorButtonBackgroundSpectrumClick,
            self.colorButtonBackgroundSpectrum)
        self.Bind(wx.EVT_BUTTON, self.OnColorButtonNucleiColorClick,
            self.colorButtonNucleiColor)
        self.Bind(wx.EVT_BUTTON, self.OnColorButtonNucleiSpectrumClick,
            self.colorButtonNucleiSpectrum)                                

        self.Bind(wx.EVT_SCROLL_THUMBTRACK,
            self.OnSliderSubtractBackgroundScrollThumbtrack,
            self.sliderSubtractBackground)
        self.Bind(wx.EVT_SCROLL_THUMBRELEASE,
            self.OnSliderSubtractBackgroundScrollThumbrelease,
            self.sliderSubtractBackground)
        self.Bind(wx.EVT_SPINCTRL, 
            self.OnSpinCtrlSubtractBackgroundSpinCtrl,
            self.spinCtrlSubtractBackground)

        self.Bind(wx.EVT_CHECKBOX, self.OnCheckBoxSubtractBackgroundCheckbox,
            self.checkBoxSubtractBackground)
        
            
    def OnSliderSubtractBackgroundScrollThumbtrack(self, event):
        # Update Spin Control
        self.subtractBackgroundAmount = \
            self.sliderSubtractBackground.GetValue()
        self.spinCtrlSubtractBackground.SetValue(self.subtractBackgroundAmount)

    def OnSliderSubtractBackgroundScrollThumbrelease(self, event):
        # Update Unmix
        if self.subtractBackground:
            self.recomputeUnmix = True
        
    def OnSpinCtrlSubtractBackgroundSpinCtrl(self, event):
        # Update Slider
        self.subtractBackgroundAmount = \
            self.spinCtrlSubtractBackground.GetValue()
        self.sliderSubtractBackground.SetValue(self.subtractBackgroundAmount)
        if self.subtractBackground:
            self.recomputeUnmix = True
        
    def OnCheckBoxSubtractBackgroundCheckbox(self, event):
        self.subtractBackground = self.checkBoxSubtractBackground.GetValue()
        self.recomputeUnmix = True        

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
        self.recomputeUnmix = True
        
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
        self.recomputeUnmix = True

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
        self.recomputeUnmix = True
        
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
        self.recomputeUnmix = True

    
if __name__ == "__main__":
    app = wx.App()
    frame = wx.Frame(None,title = "Test Frame")
    frame.SetSize((600,400))
    unmixPanel = UnmixPanel(frame)
    frame.Show()
    app.MainLoop()