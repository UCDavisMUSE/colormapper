import wx
import numpy as np
from ColorButton import ColorButton
from ColormapperSettings import ColormapperSettings

class RemixPanel(wx.Panel):     
    # Default Settings
    settings = ColormapperSettings()
    # Other variables
    recomputeRemix = False
   
 
    # Data Defaults
    backgroundColor = (230, 160, 200)
    backgroundSpectrum = (99, 69, 86)
    backgroundBrightness = 0
    backgroundBrightnessSetting = 50
    backgroundContrast = 1.0
    backgroundContrastSetting = 50
    backgroundGamma = 1.0
    backgroundGammaSetting = 50
    nucleiColor = ( 70,  30, 150)
    nucleiSpectrum = (71, 31, 153)
    nucleiBrightness = 0
    nucleiBrightnessSetting = 50
    nucleiContrast = 1.0
    nucleiContrastSetting = 50
    nucleiGamma = 1.0
    nucleiGammaSetting = 50
    remixMode = 0
    brightnessValuesStart = -10
    brightnessValuesEnd = 10
    contrastValuesStart = -1
    contrastValuesEnd = 1
    gammaValuesStart = -1
    gammaValuesEnd = 1
    

    brightnessValues = np.linspace(brightnessValuesStart, 
        brightnessValuesEnd, 101)
    contrastValues = np.logspace(contrastValuesStart, 
        contrastValuesEnd, 101)
    gammaValues = np.logspace(gammaValuesStart, 
        gammaValuesEnd, 101)

    def __init__(self, parent, settings = settings, id = -1):
        # Optional Settings
        self.settings = settings
   
        # Construct Controls
        wx.Panel.__init__(self, parent, id)
        wx.StaticText(self, -1, "Remix Controls:")
        
        # Background
        wx.StaticText(self, -1, "Background:", 
            pos = (0, 25))
        self.colorButtonBackgroundColor = ColorButton(self, -1,
            color = self.settings.GetRemixBackgroundColor(), 
            pos = (100, 25), size = (20, 20))
        self.buttonBackgroundCrosshair = wx.Button(self, -1,
            label = "+", 
            pos = (125, 19), size = (25, 25))

        wx.StaticText(self, -1, "Spectrum:", pos = (170, 25))
        self.colorButtonBackgroundSpectrum = ColorButton(self, -1,
            color = self.settings.GetRemixBackgroundSpectrum(), 
            pos = (250, 25), size = (20, 20))

        wx.StaticText(self, -1, "Brightness:", 
            pos = (0, 50))
        self.sliderBackgroundBrightness = wx.Slider(self, -1, 
            self.settings.GetRemixBackgroundBrightnessSetting(), 0, 100, 
            pos = (70, 50), size = (220, -1),
            style=wx.SL_HORIZONTAL)
        self.textCtrlBackgroundBrightness = wx.TextCtrl(self, -1,
            value = "%.2f" % settings.GetRemixBackgroundBrightness(),
            pos = (290, 50), size = (83, -1))
        self.spinButtonBackgroundBrightness = wx.SpinButton(self, -1,
            pos = (374, 50), size = (-1, -1),
            style = wx.SB_VERTICAL | wx.SP_WRAP)

        wx.StaticText(self, -1, "Contrast:", 
            pos = (0, 75))
        self.sliderBackgroundContrast = wx.Slider(self, -1,
            self.settings.GetRemixBackgroundContrastSetting(), 0, 100, 
            pos = (70, 75), size = (220, -1),
            style = wx.SL_HORIZONTAL)
        self.textCtrlBackgroundContrast = wx.TextCtrl(self, -1,
            value = "%.2f" % settings.GetRemixBackgroundContrast(),
            pos = (290, 75), size = (83, -1))
        self.spinButtonBackgroundContrast = wx.SpinButton(self, -1, 
            pos = (374, 75), size = (-1, -1), 
            style = wx.SB_VERTICAL | wx.SP_WRAP)

        wx.StaticText(self, -1, "Gamma:", 
            pos = (0, 100))
        self.sliderBackgroundGamma = wx.Slider(self, -1, 
            self.settings.GetRemixBackgroundGammaSetting(), 0, 100, 
            pos = (70, 100), size = (220, -1),
            style = wx.SL_HORIZONTAL)
        self.textCtrlBackgroundGamma = wx.TextCtrl(self, -1,
            value = "%.2f" % self.settings.GetRemixBackgroundGamma(),
            pos = (290, 100), size = (83, -1))
        self.spinButtonBackgroundGamma = wx.SpinButton(self, -1,
            pos = (374, 100), size = (-1, -1),
            style = wx.SB_VERTICAL | wx.SP_WRAP)
        
        # Nuclei
        wx.StaticText(self, -1, "Nuclei:", 
            pos = (0, 125))
        self.colorButtonNucleiColor = ColorButton(self, -1,
            color = self.settings.GetRemixNucleiColor(), 
            pos = (100, 125), size = (20, 20))
        self.buttonNucleiCrosshair = wx.Button(self, -1, 
            label = "+", 
            pos = (125, 119), size = (25, 25))
            
        wx.StaticText(self, -1, "Spectrum:", pos = (170, 125))
        self.colorButtonNucleiSpectrum = ColorButton(self, -1,
            color = self.settings.GetRemixNucleiSpectrum(), 
            pos = (250, 125), size = (20, 20))

        wx.StaticText(self, -1, "Brightness:", 
            pos = (0, 150))
        self.sliderNucleiBrightness = wx.Slider(self, -1,
            self.settings.GetRemixNucleiBrightnessSetting(), 0, 100, 
            pos = (70, 150), size = (220, -1),
            style=wx.SL_HORIZONTAL)
        self.textCtrlNucleiBrightness = wx.TextCtrl(self, -1,
            value = "%.2f" % settings.GetRemixNucleiBrightness(),
            pos = (290, 150), size = (83, -1))
        self.spinButtonNucleiBrightness = wx.SpinButton(self, -1,
            pos = (374, 150), size = (-1, -1),
            style = wx.SB_VERTICAL | wx.SP_WRAP)

        wx.StaticText(self, -1, "Contrast:",
            pos = (0, 175))
        self.sliderNucleiContrast = wx.Slider(self, -1,
            self.settings.GetRemixNucleiContrastSetting(), 0, 100, 
            pos = (70, 175), size = (220, -1),
            style = wx.SL_HORIZONTAL)
        self.textCtrlNucleiContrast = wx.TextCtrl(self, -1,
            value = "%.2f" % self.settings.GetRemixNucleiContrast(),
            pos = (290, 175), size = (83, -1))
        self.spinButtonNucleiContrast = wx.SpinButton(self, -1, 
            pos = (374, 175), size = (-1, -1), 
            style = wx.SB_VERTICAL | wx.SP_WRAP)
            
        wx.StaticText(self, -1, "Gamma:",
            pos = (0, 200))
        self.sliderNucleiGamma = wx.Slider(self, -1, 
            self.settings.GetRemixNucleiGammaSetting(), 0, 100, 
            pos = (70, 200), size = (220, -1),
            style = wx.SL_HORIZONTAL)
        self.textCtrlNucleiGamma = wx.TextCtrl(self, -1,
            value = "%.2f" % self.settings.GetRemixNucleiGamma(),
            pos = (290, 200), size = (83, -1))
        self.spinButtonNucleiGamma = wx.SpinButton(self, -1,
            pos = (374, 200), size = (-1, -1),
            style = wx.SB_VERTICAL | wx.SP_WRAP)
        
        wx.StaticText(self, -1, "Remix Mode:", pos = (0, 225))
        self.choiceRemixMode = wx.Choice(self, -1, pos = (85, 223), 
            choices = (
                "Brightfield (Beer-Lambert)",
                "Brightfield (Invert-Multiply)",
                "Fluorescence"))
        self.choiceRemixMode.SetSelection(self.settings.GetRemixRemixMode())
        

        # Event Handlers
        ## Background
        ### Colors
        self.Bind(wx.EVT_BUTTON, self.OnColorButtonBackgroundColorClick,
            self.colorButtonBackgroundColor)
        self.Bind(wx.EVT_BUTTON, self.OnColorButtonBackgroundSpectrumClick,
            self.colorButtonBackgroundSpectrum)
        ### Brightness
        self.Bind(wx.EVT_SCROLL_THUMBTRACK,
            self.OnSliderBackgroundBrightnessScrollThumbtrack,
            self.sliderBackgroundBrightness)
        self.Bind(wx.EVT_SCROLL_THUMBRELEASE,
            self.OnSliderBackgroundBrightnessScrollThumbrelease,
            self.sliderBackgroundBrightness)
        self.Bind(wx.EVT_SPIN_UP,
            self.OnSpinButtonBackgroundBrightnessSpinUp,
            self.spinButtonBackgroundBrightness)
        self.Bind(wx.EVT_SPIN_DOWN,
            self.OnSpinButtonBackgroundBrightnessSpinDown,
            self.spinButtonBackgroundBrightness)        
        ### Contrast            
        self.Bind(wx.EVT_SCROLL_THUMBTRACK,
            self.OnSliderBackgroundContrastScrollThumbtrack,
            self.sliderBackgroundContrast)
        self.Bind(wx.EVT_SCROLL_THUMBRELEASE,
            self.OnSliderBackgroundContrastScrollThumbrelease,
            self.sliderBackgroundContrast)
        self.Bind(wx.EVT_SPIN_UP,
            self.OnSpinButtonBackgroundContrastSpinUp,
            self.spinButtonBackgroundContrast)
        self.Bind(wx.EVT_SPIN_DOWN,
            self.OnSpinButtonBackgroundContrastSpinDown,
            self.spinButtonBackgroundContrast)
        ### Gamma            
        self.Bind(wx.EVT_SCROLL_THUMBTRACK,
            self.OnSliderBackgroundGammaScrollThumbtrack,
            self.sliderBackgroundGamma)
        self.Bind(wx.EVT_SCROLL_THUMBRELEASE,
            self.OnSliderBackgroundGammaScrollThumbrelease,
            self.sliderBackgroundGamma)
        self.Bind(wx.EVT_SPIN_UP,
            self.OnSpinButtonBackgroundGammaSpinUp,
            self.spinButtonBackgroundGamma)
        self.Bind(wx.EVT_SPIN_DOWN,
            self.OnSpinButtonBackgroundGammaSpinDown,
            self.spinButtonBackgroundGamma)
        ## Nuclei
        ### Colors
        self.Bind(wx.EVT_BUTTON, self.OnColorButtonNucleiColorClick,
            self.colorButtonNucleiColor)
        self.Bind(wx.EVT_BUTTON, self.OnColorButtonNucleiSpectrumClick,
            self.colorButtonNucleiSpectrum)      
        ### Brightness
        self.Bind(wx.EVT_SCROLL_THUMBTRACK,
            self.OnSliderNucleiBrightnessScrollThumbtrack,
            self.sliderNucleiBrightness)
        self.Bind(wx.EVT_SCROLL_THUMBRELEASE,
            self.OnSliderNucleiBrightnessScrollThumbrelease,
            self.sliderNucleiBrightness)
        self.Bind(wx.EVT_SPIN_UP,
            self.OnSpinButtonNucleiBrightnessSpinUp,
            self.spinButtonNucleiBrightness)
        self.Bind(wx.EVT_SPIN_DOWN,
            self.OnSpinButtonNucleiBrightnessSpinDown,
            self.spinButtonNucleiBrightness)            
        ### Contrast
        self.Bind(wx.EVT_SCROLL_THUMBTRACK,
            self.OnSliderNucleiContrastScrollThumbtrack,
            self.sliderNucleiContrast)
        self.Bind(wx.EVT_SCROLL_THUMBRELEASE,
            self.OnSliderNucleiContrastScrollThumbrelease,
            self.sliderNucleiContrast)
        self.Bind(wx.EVT_SPIN_UP,
            self.OnSpinButtonNucleiContrastSpinUp,
            self.spinButtonNucleiContrast)
        self.Bind(wx.EVT_SPIN_DOWN,
            self.OnSpinButtonNucleiContrastSpinDown,
            self.spinButtonNucleiContrast)
        ### Gamma
        self.Bind(wx.EVT_SCROLL_THUMBTRACK,
            self.OnSliderNucleiGammaScrollThumbtrack,
            self.sliderNucleiGamma)
        self.Bind(wx.EVT_SCROLL_THUMBRELEASE,
            self.OnSliderNucleiGammaScrollThumbrelease,
            self.sliderNucleiGamma)
        self.Bind(wx.EVT_SPIN_UP,
            self.OnSpinButtonNucleiGammaSpinUp,
            self.spinButtonNucleiGamma)
        self.Bind(wx.EVT_SPIN_DOWN,
            self.OnSpinButtonNucleiGammaSpinDown,
            self.spinButtonNucleiGamma)
        ## Remix Mode
        self.Bind(wx.EVT_CHOICE,
            self.OnChoiceRemixModeChoice,
            self.choiceRemixMode)            

    ## Background
    ### Colors            
    def OnColorButtonBackgroundColorClick(self, event):
        self.settings.SetRemixBackgroundColor(self.colorButtonBackgroundColor.GetBackgroundColour()[0:3])
        self.RefreshBackgroundColorButtons()
        self.recomputeRemix = True
        
    def OnColorButtonBackgroundSpectrumClick(self, event):
        # Don't do anything, this just resets the color
        self.colorButtonBackgroundSpectrum.SetBackgroundColour(self.settings.GetRemixBackgroundSpectrum())
            
    ### Brightness
    def OnSliderBackgroundBrightnessScrollThumbtrack(self, event):
        # Update Text Control
        self.settings.SetRemixBackgroundBrightnessSetting(self.sliderBackgroundBrightness.GetValue())
        self.textCtrlBackgroundBrightness.SetValue("%.2f" % self.settings.GetRemixBackgroundBrightness())
        
    def OnSliderBackgroundBrightnessScrollThumbrelease(self, event):
        # Update Remix
        self.recomputeRemix = True                    
        
    def OnSpinButtonBackgroundBrightnessSpinUp(self, event):
        if self.settings.GetRemixBackgroundBrightnessSetting() < 100:
            self.settings.SetRemixBackgroundBrightnessSetting(self.settings.GetRemixBackgroundBrightnessSetting() + 1)
            self.sliderBackgroundBrightness.SetValue(self.settings.GetRemixBackgroundBrightnessSetting())
            self.textCtrlBackgroundBrightness.SetValue("%.2f" % self.settings.GetRemixBackgroundBrightness())
            self.recomputeRemix = True
    
    def OnSpinButtonBackgroundBrightnessSpinDown(self, event):
        if self.backgroundBrightnessSetting > 0:
            self.settings.SetRemixBackgroundBrightnessSetting(self.settings.GetRemixBackgroundBrightnessSetting() - 1)
            self.sliderBackgroundBrightness.SetValue(self.settings.GetRemixBackgroundBrightnessSetting())
            self.textCtrlBackgroundBrightness.SetValue("%.2f" % self.settings.GetRemixBackgroundBrightness())
            self.recomputeRemix = True 

    ### Contrast
    def OnSliderBackgroundContrastScrollThumbtrack(self, event):
        # Update Text Control
        self.settings.SetRemixBackgroundContrastSetting(self.sliderBackgroundContrast.GetValue())
        self.textCtrlBackgroundContrast.SetValue("%.2f" % self.settings.GetRemixBackgroundContrast())
        
    def OnSliderBackgroundContrastScrollThumbrelease(self, event):
        # Update Remix
        self.recomputeRemix = True                    
        
    def OnSpinButtonBackgroundContrastSpinUp(self, event):
        if self.settings.GetRemixBackgroundContrastSetting() < 100:
            self.settings.SetRemixBackgroundContrastSetting(self.settings.GetRemixBackgroundContrastSetting() + 1)
            self.sliderBackgroundContrast.SetValue(self.settings.GetRemixBackgroundContrastSetting())
            self.textCtrlBackgroundContrast.SetValue("%.2f" % self.settings.GetRemixBackgroundContrast())
            self.recomputeRemix = True
    
    def OnSpinButtonBackgroundContrastSpinDown(self, event):
        if self.backgroundContrastSetting > 0:
            self.settings.SetRemixBackgroundContrastSetting(self.settings.GetRemixBackgroundContrastSetting() - 1)
            self.sliderBackgroundContrast.SetValue(self.settings.GetRemixBackgroundContrastSetting())
            self.textCtrlBackgroundContrast.SetValue("%.2f" % self.settings.GetRemixBackgroundContrast())
            self.recomputeRemix = True            

    ### Gamma
    def OnSliderBackgroundGammaScrollThumbtrack(self, event):
        # Update Text Control
        self.settings.SetRemixBackgroundGammaSetting(self.sliderBackgroundGamma.GetValue())
        self.textCtrlBackgroundGamma.SetValue("%.2f" % self.settings.GetRemixBackgroundGamma())
        
    def OnSliderBackgroundGammaScrollThumbrelease(self, event):
        # Update Remix
        self.recomputeRemix = True                    
        
    def OnSpinButtonBackgroundGammaSpinUp(self, event):
        if self.backgroundGammaSetting < 100:
            self.settings.SetRemixBackgroundGammaSetting(self.settings.GetRemixBackgroundGammaSetting() + 1)
            self.sliderBackgroundGamma.SetValue(self.settings.GetRemixBackgroundGammaSetting())
            self.textCtrlBackgroundGamma.SetValue("%.2f" % self.settings.GetRemixBackgroundGamma())
            self.recomputeRemix = True            
    
    def OnSpinButtonBackgroundGammaSpinDown(self, event):
        if self.backgroundGammaSetting > 0:
            self.settings.SetRemixBackgroundGammaSetting(self.settings.GetRemixBackgroundGammaSetting() - 1)
            self.sliderBackgroundGamma.SetValue(self.settings.GetRemixBackgroundGammaSetting())
            self.textCtrlBackgroundGamma.SetValue("%.2f" % self.settings.GetRemixBackgroundGamma())
            self.recomputeRemix = True  

    ## Nuclei
    ### Colors
    def OnColorButtonNucleiColorClick(self, event):
        self.settings.SetRemixNucleiColor(self.colorButtonNucleiColor.GetBackgroundColour()[0:3])
        self.RefreshNucleiColorButtons()
        self.recomputeRemix = True
        
    def OnColorButtonNucleiSpectrumClick(self, event):
        # Don't do anything, this just resets the color
        self.colorButtonNucleiSpectrum.SetBackgroundColour(self.settings.GetRemixNucleiSpectrum())

    ### Brightness        
    def OnSliderNucleiBrightnessScrollThumbtrack(self, event):
        # Update Text Control
        self.settings.SetRemixNucleiBrightnessSetting(self.sliderNucleiBrightness.GetValue())
        self.textCtrlNucleiBrightness.SetValue("%.2f" % self.settings.GetRemixNucleiBrightness())
        
    def OnSliderNucleiBrightnessScrollThumbrelease(self, event):
        # Update Remix
        self.recomputeRemix = True                    
        
    def OnSpinButtonNucleiBrightnessSpinUp(self, event):
        if self.settings.GetRemixNucleiBrightnessSetting() < 100:
            self.settings.SetRemixNucleiBrightnessSetting(self.settings.GetRemixNucleiBrightnessSetting() + 1)
            self.sliderNucleiBrightness.SetValue(self.settings.GetRemixNucleiBrightnessSetting())
            self.textCtrlNucleiBrightness.SetValue("%.2f" % self.settings.GetRemixNucleiBrightness())
            self.recomputeRemix = True
    
    def OnSpinButtonNucleiBrightnessSpinDown(self, event):
        if self.backgroundBrightnessSetting > 0:
            self.settings.SetRemixNucleiBrightnessSetting(self.settings.GetRemixNucleiBrightnessSetting() - 1)
            self.sliderNucleiBrightness.SetValue(self.settings.GetRemixNucleiBrightnessSetting())
            self.textCtrlNucleiBrightness.SetValue("%.2f" % self.settings.GetRemixNucleiBrightness())
            self.recomputeRemix = True            

    ### Contrast
    def OnSliderNucleiContrastScrollThumbtrack(self, event):
        # Update Text Control
        self.settings.SetRemixNucleiContrastSetting(self.sliderNucleiContrast.GetValue())
        self.textCtrlNucleiContrast.SetValue("%.2f" % self.settings.GetRemixNucleiContrast())
        
    def OnSliderNucleiContrastScrollThumbrelease(self, event):
        # Update Remix
        self.recomputeRemix = True                    
        
    def OnSpinButtonNucleiContrastSpinUp(self, event):
        if self.settings.GetRemixNucleiContrastSetting() < 100:
            self.settings.SetRemixNucleiContrastSetting(self.settings.GetRemixNucleiContrastSetting() + 1)
            self.sliderNucleiContrast.SetValue(self.settings.GetRemixNucleiContrastSetting())
            self.textCtrlNucleiContrast.SetValue("%.2f" % self.settings.GetRemixNucleiContrast())
            self.recomputeRemix = True
    
    def OnSpinButtonNucleiContrastSpinDown(self, event):
        if self.backgroundContrastSetting > 0:
            self.settings.SetRemixNucleiContrastSetting(self.settings.GetRemixNucleiContrastSetting() - 1)
            self.sliderNucleiContrast.SetValue(self.settings.GetRemixNucleiContrastSetting())
            self.textCtrlNucleiContrast.SetValue("%.2f" % self.settings.GetRemixNucleiContrast())
            self.recomputeRemix = True            

    ### Gamma
    def OnSliderNucleiGammaScrollThumbtrack(self, event):
        # Update Text Control
        self.settings.SetRemixNucleiGammaSetting(self.sliderNucleiGamma.GetValue())
        self.textCtrlNucleiGamma.SetValue("%.2f" % self.settings.GetRemixNucleiGamma())
        
    def OnSliderNucleiGammaScrollThumbrelease(self, event):
        # Update Remix
        self.recomputeRemix = True                    
        
    def OnSpinButtonNucleiGammaSpinUp(self, event):
        if self.backgroundGammaSetting < 100:
            self.settings.SetRemixNucleiGammaSetting(self.settings.GetRemixNucleiGammaSetting() + 1)
            self.sliderNucleiGamma.SetValue(self.settings.GetRemixNucleiGammaSetting())
            self.textCtrlNucleiGamma.SetValue("%.2f" % self.settings.GetRemixNucleiGamma())
            self.recomputeRemix = True            
    
    def OnSpinButtonNucleiGammaSpinDown(self, event):
        if self.backgroundGammaSetting > 0:
            self.settings.SetRemixNucleiGammaSetting(self.settings.GetRemixNucleiGammaSetting() - 1)
            self.sliderNucleiGamma.SetValue(self.settings.GetRemixNucleiGammaSetting())
            self.textCtrlNucleiGamma.SetValue("%.2f" % self.settings.GetRemixNucleiGamma())
            self.recomputeRemix = True            
        
    ## Remix Mode        
    def OnChoiceRemixModeChoice(self, event):
        if self.settings.GetRemixRemixMode() != self.choiceRemixMode.GetSelection():
            self.settings.SetRemixRemixMode(self.choiceRemixMode.GetSelection())
            self.recomputeRemix = True
            
    def RefreshBackgroundColorButtons(self):
        self.colorButtonBackgroundColor.SetBackgroundColour(self.settings.GetRemixBackgroundColor())
        self.colorButtonBackgroundColor.Refresh()
        self.colorButtonBackgroundSpectrum.SetBackgroundColour(self.settings.GetRemixBackgroundSpectrum())
        self.colorButtonBackgroundSpectrum.Refresh()
        
    def RefreshNucleiColorButtons(self):
        self.colorButtonNucleiColor.SetBackgroundColour(self.settings.GetRemixNucleiColor())
        self.colorButtonNucleiColor.Refresh()
        self.colorButtonNucleiSpectrum.SetBackgroundColour(self.settings.GetRemixNucleiSpectrum())
        self.colorButtonNucleiSpectrum.Refresh()            

    
if __name__ == "__main__":
    app = wx.App()
    frame = wx.Frame(None,title = "Test Frame")
    frame.SetSize((600, 400))
    unmixPanel = RemixPanel(frame)
    frame.Show()
    app.MainLoop()