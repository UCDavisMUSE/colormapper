import wx
from ColorButton import ColorButton
from ColormapperSettings import ColormapperSettings

class UnmixPanel(wx.Panel):
    # Default Settings
    settings = ColormapperSettings()
    # Other Variables
    recomputeUnmix = False

    def __init__(self, parent, settings = settings, id = -1):
        # Optional Settings
        self.settings = settings
    
        # Construct Controls
        wx.Panel.__init__(self, parent, id)
        wx.StaticText(self, -1, "Unmix Controls:")

        wx.StaticText(self, -1, "Bulk Tissue:", pos = (0, 25))
        self.colorButtonBackgroundColor = ColorButton(self, -1, 
            color = self.settings.GetUnmixBackgroundColor(), pos = (100, 25),
            size = (20, 20))
        self.buttonBackgroundCrosshair = wx.Button(self, -1, 
            label = "+", pos = (125, 19), size = (25, 25))
        wx.StaticText(self, -1, "Spectrum:", pos = (170, 25))
        self.colorButtonBackgroundSpectrum = ColorButton(self, -1, 
            color = self.settings.GetUnmixBackgroundSpectrum(), pos = (250, 25),
            size = (20, 20))
            
        wx.StaticText(self, -1, "Nuclei:", pos = (0, 50))
        self.colorButtonNucleiColor = ColorButton(self, -1, 
            color = self.settings.GetUnmixNucleiColor(), pos = (100, 50),
            size = (20, 20))
        wx.Button(self, -1, label = "+", pos = (125, 43), size = (25, 25))
        wx.StaticText(self, -1, "Spectrum:", pos = (170, 50))
        self.colorButtonNucleiSpectrum = ColorButton(self, -1, 
            color = self.settings.GetUnmixNucleiSpectrum(), pos = (250, 50),
            size = (20, 20))

        self.checkBoxSubtractBackground = wx.CheckBox(self, -1,
            label = "Subtract Background (Pure Spectrum)", pos = (0, 75))
        self.checkBoxSubtractBackground.SetValue(self.settings.GetUnmixSubtractBackground())
        wx.StaticText(self, -1, "Amount:", pos = (0, 100))
        self.sliderSubtractBackground = wx.Slider(self, -1,
            self.settings.GetUnmixSubtractBackgroundAmount(), 0, 100,
            pos=(70, 100), size = (220, -1),
            style = wx.SL_HORIZONTAL)
        self.spinCtrlSubtractBackground = wx.SpinCtrl(self, -1,
            "%.2f" % self.settings.GetUnmixSubtractBackgroundAmount(),
            initial = self.settings.GetUnmixSubtractBackgroundAmount(), min = 0, max = 100,
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
        self.settings.SetUnmixSubtractBackgroundAmount(self.sliderSubtractBackground.GetValue())
        self.spinCtrlSubtractBackground.SetValue(self.settings.GetUnmixSubtractBackgroundAmount())
        # Update Nuclei Spectrum
        self.colorButtonNucleiSpectrum.SetBackgroundColour(self.settings.GetUnmixNucleiSpectrum())
        self.colorButtonNucleiSpectrum.Refresh()

    def OnSliderSubtractBackgroundScrollThumbrelease(self, event):
        # Update Unmix
        if self.settings.GetUnmixSubtractBackground():
            self.recomputeUnmix = True
        
    def OnSpinCtrlSubtractBackgroundSpinCtrl(self, event):
        # Update Slider
        self.settings.SetUnmixSubtractBackgroundAmount(self.spinCtrlSubtractBackground.GetValue())
        self.sliderSubtractBackground.SetValue(self.settings.GetUnmixSubtractBackgroundAmount())
        # Update Nuclei Spectrum
        self.colorButtonNucleiSpectrum.SetBackgroundColour(self.settings.GetUnmixNucleiSpectrum())
        self.colorButtonNucleiSpectrum.Refresh()
        if self.settings.GetUnmixSubtractBackground():
            self.recomputeUnmix = True
        
    def OnCheckBoxSubtractBackgroundCheckbox(self, event):
        self.settings.SetUnmixSubtractBackground(self.checkBoxSubtractBackground.GetValue())
        self.recomputeUnmix = True        

    def OnColorButtonBackgroundColorClick(self, event):
        self.settings.SetUnmixBackgroundColor(self.colorButtonBackgroundColor.GetBackgroundColour()[0:3])
        self.colorButtonBackgroundSpectrum.SetBackgroundColour(self.settings.GetUnmixBackgroundSpectrum())
        self.colorButtonBackgroundSpectrum.Refresh()
        self.recomputeUnmix = True
        
    def OnColorButtonBackgroundSpectrumClick(self, event):
        # Don't do anything, this just resets the color
        self.colorButtonBackgroundSpectrum.SetBackgroundColour(self.settings.GetUnmixBackgroundSpectrum())

    def OnColorButtonNucleiColorClick(self, event):
        self.settings.SetUnmixNucleiColor(self.colorButtonNucleiColor.GetBackgroundColour()[0:3])
        self.colorButtonNucleiSpectrum.SetBackgroundColour(self.settings.GetUnmixNucleiSpectrum())
        self.colorButtonNucleiSpectrum.Refresh()
        self.recomputeUnmix = True
        
    def OnColorButtonNucleiSpectrumClick(self, event):
        # Don't do anything, this just resets the color
        self.colorButtonNucleiSpectrum.SetBackgroundColour(self.settings.GetUnmixNucleiSpectrum())

    
if __name__ == "__main__":
    app = wx.App()
    frame = wx.Frame(None,title = "Test Frame")
    frame.SetSize((600,400))
    unmixPanel = UnmixPanel(frame)
    frame.Show()
    app.MainLoop()