import wx
import numpy as np
from ColorButton import ColorButton
from ColormapperSettings import ColormapperSettings

class RemixPanel(wx.Panel):     
    # Default Settings
    settings = ColormapperSettings()
    # Other variables
    recomputeRemix = False
   
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

        wx.StaticText(self, -1, "Spectrum:", 
            pos = (170, 25))
        self.colorButtonBackgroundSpectrum = ColorButton(self, -1,
            color = self.settings.GetRemixBackgroundSpectrum(), 
            pos = (250, 25), size = (20, 20))

        wx.StaticText(self, -1, "Threshold:", 
            pos = (0, 50))
        self.sliderBackgroundThresh = wx.Slider(self, -1, 
            self.settings.GetRemixBackgroundThreshSetting(), 0, 100, 
            pos = (70, 50), size = (220, -1),
            style=wx.SL_HORIZONTAL)
        self.textCtrlBackgroundThresh = wx.TextCtrl(self, -1,
            value = "%.2f" % settings.GetRemixBackgroundThresh(),
            pos = (290, 50), size = (83, -1))
        self.spinButtonBackgroundThresh = wx.SpinButton(self, -1,
            pos = (374, 50), size = (-1, -1),
            style = wx.SB_VERTICAL | wx.SP_WRAP)

        wx.StaticText(self, -1, "Gain:", 
            pos = (0, 75))
        self.sliderBackgroundGain = wx.Slider(self, -1,
            self.settings.GetRemixBackgroundGainSetting(), 0, 100, 
            pos = (70, 75), size = (220, -1),
            style = wx.SL_HORIZONTAL)
        self.textCtrlBackgroundGain = wx.TextCtrl(self, -1,
            value = "%.2f" % settings.GetRemixBackgroundGain(),
            pos = (290, 75), size = (83, -1))
        self.spinButtonBackgroundGain = wx.SpinButton(self, -1, 
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
            pos = (0, 135))
        self.colorButtonNucleiColor = ColorButton(self, -1,
            color = self.settings.GetRemixNucleiColor(), 
            pos = (100, 135), size = (20, 20))
        self.buttonNucleiCrosshair = wx.Button(self, -1, 
            label = "+", 
            pos = (125, 129), size = (25, 25))
            
        wx.StaticText(self, -1, "Spectrum:", 
            pos = (170, 135))
        self.colorButtonNucleiSpectrum = ColorButton(self, -1,
            color = self.settings.GetRemixNucleiSpectrum(), 
            pos = (250, 135), size = (20, 20))

        wx.StaticText(self, -1, "Threshold:", 
            pos = (0, 160))
        self.sliderNucleiThresh = wx.Slider(self, -1,
            self.settings.GetRemixNucleiThreshSetting(), 0, 100, 
            pos = (70, 160), size = (220, -1),
            style=wx.SL_HORIZONTAL)
        self.textCtrlNucleiThresh = wx.TextCtrl(self, -1,
            value = "%.2f" % settings.GetRemixNucleiThresh(),
            pos = (290, 160), size = (83, -1))
        self.spinButtonNucleiThresh = wx.SpinButton(self, -1,
            pos = (374, 160), size = (-1, -1),
            style = wx.SB_VERTICAL | wx.SP_WRAP)

        wx.StaticText(self, -1, "Gain:",
            pos = (0, 185))
        self.sliderNucleiGain = wx.Slider(self, -1,
            self.settings.GetRemixNucleiGainSetting(), 0, 100, 
            pos = (70, 185), size = (220, -1),
            style = wx.SL_HORIZONTAL)
        self.textCtrlNucleiGain = wx.TextCtrl(self, -1,
            value = "%.2f" % self.settings.GetRemixNucleiGain(),
            pos = (290, 185), size = (83, -1))
        self.spinButtonNucleiGain = wx.SpinButton(self, -1, 
            pos = (374, 185), size = (-1, -1), 
            style = wx.SB_VERTICAL | wx.SP_WRAP)
            
        wx.StaticText(self, -1, "Gamma:",
            pos = (0, 210))
        self.sliderNucleiGamma = wx.Slider(self, -1, 
            self.settings.GetRemixNucleiGammaSetting(), 0, 100, 
            pos = (70, 210), size = (220, -1),
            style = wx.SL_HORIZONTAL)
        self.textCtrlNucleiGamma = wx.TextCtrl(self, -1,
            value = "%.2f" % self.settings.GetRemixNucleiGamma(),
            pos = (290, 210), size = (83, -1))
        self.spinButtonNucleiGamma = wx.SpinButton(self, -1,
            pos = (374, 210), size = (-1, -1),
            style = wx.SB_VERTICAL | wx.SP_WRAP)
        
        wx.StaticText(self, -1, "Remix Mode:", 
            pos = (0, 235))
        self.choiceRemixMode = wx.Choice(self, -1, 
            pos = (85, 233), 
            choices = (
                "Brightfield (Beer-Lambert)",
                "Brightfield (Invert-Multiply)",
                "Fluorescence",
                "Experimental"))
        self.choiceRemixMode.SetSelection(self.settings.GetRemixRemixMode())
        

        # Event Handlers
        ## Background
        ### Colors
        self.Bind(wx.EVT_BUTTON, self.OnColorButtonBackgroundColorClick,
            self.colorButtonBackgroundColor)
        self.Bind(wx.EVT_BUTTON, self.OnColorButtonBackgroundSpectrumClick,
            self.colorButtonBackgroundSpectrum)
        ### Thresh
        self.Bind(wx.EVT_SCROLL_THUMBTRACK,
            self.OnSliderBackgroundThreshScrollThumbtrack,
            self.sliderBackgroundThresh)
        self.Bind(wx.EVT_SCROLL_THUMBRELEASE,
            self.OnSliderBackgroundThreshScrollThumbrelease,
            self.sliderBackgroundThresh)
        self.Bind(wx.EVT_SPIN_UP,
            self.OnSpinButtonBackgroundThreshSpinUp,
            self.spinButtonBackgroundThresh)
        self.Bind(wx.EVT_SPIN_DOWN,
            self.OnSpinButtonBackgroundThreshSpinDown,
            self.spinButtonBackgroundThresh)        
        ### Gain            
        self.Bind(wx.EVT_SCROLL_THUMBTRACK,
            self.OnSliderBackgroundGainScrollThumbtrack,
            self.sliderBackgroundGain)
        self.Bind(wx.EVT_SCROLL_THUMBRELEASE,
            self.OnSliderBackgroundGainScrollThumbrelease,
            self.sliderBackgroundGain)
        self.Bind(wx.EVT_SPIN_UP,
            self.OnSpinButtonBackgroundGainSpinUp,
            self.spinButtonBackgroundGain)
        self.Bind(wx.EVT_SPIN_DOWN,
            self.OnSpinButtonBackgroundGainSpinDown,
            self.spinButtonBackgroundGain)
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
        ### Thresh
        self.Bind(wx.EVT_SCROLL_THUMBTRACK,
            self.OnSliderNucleiThreshScrollThumbtrack,
            self.sliderNucleiThresh)
        self.Bind(wx.EVT_SCROLL_THUMBRELEASE,
            self.OnSliderNucleiThreshScrollThumbrelease,
            self.sliderNucleiThresh)
        self.Bind(wx.EVT_SPIN_UP,
            self.OnSpinButtonNucleiThreshSpinUp,
            self.spinButtonNucleiThresh)
        self.Bind(wx.EVT_SPIN_DOWN,
            self.OnSpinButtonNucleiThreshSpinDown,
            self.spinButtonNucleiThresh)            
        ### Gain
        self.Bind(wx.EVT_SCROLL_THUMBTRACK,
            self.OnSliderNucleiGainScrollThumbtrack,
            self.sliderNucleiGain)
        self.Bind(wx.EVT_SCROLL_THUMBRELEASE,
            self.OnSliderNucleiGainScrollThumbrelease,
            self.sliderNucleiGain)
        self.Bind(wx.EVT_SPIN_UP,
            self.OnSpinButtonNucleiGainSpinUp,
            self.spinButtonNucleiGain)
        self.Bind(wx.EVT_SPIN_DOWN,
            self.OnSpinButtonNucleiGainSpinDown,
            self.spinButtonNucleiGain)
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
        self.settings.SetRemixBackgroundColor(
            self.colorButtonBackgroundColor.GetBackgroundColour()[0:3])
        self.RefreshBackgroundColorButtons()
        self.recomputeRemix = True
        
    def OnColorButtonBackgroundSpectrumClick(self, event):
        # Don't do anything, this just resets the color
        self.colorButtonBackgroundSpectrum.SetBackgroundColour(
            self.settings.GetRemixBackgroundSpectrum())
            
    ### Thresh
    def OnSliderBackgroundThreshScrollThumbtrack(self, event):
        # Update Text Control
        self.settings.SetRemixBackgroundThreshSetting(
            self.sliderBackgroundThresh.GetValue())
        self.textCtrlBackgroundThresh.SetValue(
            "%.2f" % self.settings.GetRemixBackgroundThresh())
        
    def OnSliderBackgroundThreshScrollThumbrelease(self, event):
        # Update Remix
        self.recomputeRemix = True                    
        
    def OnSpinButtonBackgroundThreshSpinUp(self, event):
        if self.settings.GetRemixBackgroundThreshSetting() < 100:
            self.settings.SetRemixBackgroundThreshSetting(
                self.settings.GetRemixBackgroundThreshSetting() + 1)
            self.sliderBackgroundThresh.SetValue(
                self.settings.GetRemixBackgroundThreshSetting())
            self.textCtrlBackgroundThresh.SetValue(
                "%.2f" % self.settings.GetRemixBackgroundThresh())
            self.recomputeRemix = True
    
    def OnSpinButtonBackgroundThreshSpinDown(self, event):
        if self.settings.GetRemixBackgroundThreshSetting() > 0:
            self.settings.SetRemixBackgroundThreshSetting(
                self.settings.GetRemixBackgroundThreshSetting() - 1)
            self.sliderBackgroundThresh.SetValue(
                self.settings.GetRemixBackgroundThreshSetting())
            self.textCtrlBackgroundThresh.SetValue(
                "%.2f" % self.settings.GetRemixBackgroundThresh())
            self.recomputeRemix = True 

    ### Gain
    def OnSliderBackgroundGainScrollThumbtrack(self, event):
        # Update Text Control
        self.settings.SetRemixBackgroundGainSetting(
            self.sliderBackgroundGain.GetValue())
        self.textCtrlBackgroundGain.SetValue(
            "%.2f" % self.settings.GetRemixBackgroundGain())
        
    def OnSliderBackgroundGainScrollThumbrelease(self, event):
        # Update Remix
        self.recomputeRemix = True                    
        
    def OnSpinButtonBackgroundGainSpinUp(self, event):
        if self.settings.GetRemixBackgroundGainSetting() < 100:
            self.settings.SetRemixBackgroundGainSetting(
                self.settings.GetRemixBackgroundGainSetting() + 1)
            self.sliderBackgroundGain.SetValue(
                self.settings.GetRemixBackgroundGainSetting())
            self.textCtrlBackgroundGain.SetValue(
                "%.2f" % self.settings.GetRemixBackgroundGain())
            self.recomputeRemix = True
    
    def OnSpinButtonBackgroundGainSpinDown(self, event):
        if self.settings.GetRemixBackgroundGainSetting() > 0:
            self.settings.SetRemixBackgroundGainSetting(
                self.settings.GetRemixBackgroundGainSetting() - 1)
            self.sliderBackgroundGain.SetValue(
                self.settings.GetRemixBackgroundGainSetting())
            self.textCtrlBackgroundGain.SetValue(
                "%.2f" % self.settings.GetRemixBackgroundGain())
            self.recomputeRemix = True            

    ### Gamma
    def OnSliderBackgroundGammaScrollThumbtrack(self, event):
        # Update Text Control
        self.settings.SetRemixBackgroundGammaSetting(
            self.sliderBackgroundGamma.GetValue())
        self.textCtrlBackgroundGamma.SetValue(
            "%.2f" % self.settings.GetRemixBackgroundGamma())
        
    def OnSliderBackgroundGammaScrollThumbrelease(self, event):
        # Update Remix
        self.recomputeRemix = True                    
        
    def OnSpinButtonBackgroundGammaSpinUp(self, event):
        if self.settings.GetRemixBackgroundGammaSetting() < 100:
            self.settings.SetRemixBackgroundGammaSetting(
                self.settings.GetRemixBackgroundGammaSetting() + 1)
            self.sliderBackgroundGamma.SetValue(
                self.settings.GetRemixBackgroundGammaSetting())
            self.textCtrlBackgroundGamma.SetValue(
                "%.2f" % self.settings.GetRemixBackgroundGamma())
            self.recomputeRemix = True            
    
    def OnSpinButtonBackgroundGammaSpinDown(self, event):
        if self.settings.GetRemixBackgroundGammaSetting() > 0:
            self.settings.SetRemixBackgroundGammaSetting(
                self.settings.GetRemixBackgroundGammaSetting() - 1)
            self.sliderBackgroundGamma.SetValue(
                self.settings.GetRemixBackgroundGammaSetting())
            self.textCtrlBackgroundGamma.SetValue(
                "%.2f" % self.settings.GetRemixBackgroundGamma())
            self.recomputeRemix = True  

    ## Nuclei
    ### Colors
    def OnColorButtonNucleiColorClick(self, event):
        self.settings.SetRemixNucleiColor(
            self.colorButtonNucleiColor.GetBackgroundColour()[0:3])
        self.RefreshNucleiColorButtons()
        self.recomputeRemix = True
        
    def OnColorButtonNucleiSpectrumClick(self, event):
        # Don't do anything, this just resets the color
        self.colorButtonNucleiSpectrum.SetBackgroundColour(
            self.settings.GetRemixNucleiSpectrum())

    ### Thresh        
    def OnSliderNucleiThreshScrollThumbtrack(self, event):
        # Update Text Control
        self.settings.SetRemixNucleiThreshSetting(
            self.sliderNucleiThresh.GetValue())
        self.textCtrlNucleiThresh.SetValue(
            "%.2f" % self.settings.GetRemixNucleiThresh())
        
    def OnSliderNucleiThreshScrollThumbrelease(self, event):
        # Update Remix
        self.recomputeRemix = True                    
        
    def OnSpinButtonNucleiThreshSpinUp(self, event):
        if self.settings.GetRemixNucleiThreshSetting() < 100:
            self.settings.SetRemixNucleiThreshSetting(
                self.settings.GetRemixNucleiThreshSetting() + 1)
            self.sliderNucleiThresh.SetValue(
                self.settings.GetRemixNucleiThreshSetting())
            self.textCtrlNucleiThresh.SetValue(
                "%.2f" % self.settings.GetRemixNucleiThresh())
            self.recomputeRemix = True
    
    def OnSpinButtonNucleiThreshSpinDown(self, event):
        if self.settings.GetRemixBackgroundThreshSetting() > 0:
            self.settings.SetRemixNucleiThreshSetting(
                self.settings.GetRemixNucleiThreshSetting() - 1)
            self.sliderNucleiThresh.SetValue(
                self.settings.GetRemixNucleiThreshSetting())
            self.textCtrlNucleiThresh.SetValue(
                "%.2f" % self.settings.GetRemixNucleiThresh())
            self.recomputeRemix = True            

    ### Gain
    def OnSliderNucleiGainScrollThumbtrack(self, event):
        # Update Text Control
        self.settings.SetRemixNucleiGainSetting(
            self.sliderNucleiGain.GetValue())
        self.textCtrlNucleiGain.SetValue(
            "%.2f" % self.settings.GetRemixNucleiGain())
        
    def OnSliderNucleiGainScrollThumbrelease(self, event):
        # Update Remix
        self.recomputeRemix = True                    
        
    def OnSpinButtonNucleiGainSpinUp(self, event):
        if self.settings.GetRemixNucleiGainSetting() < 100:
            self.settings.SetRemixNucleiGainSetting(
                self.settings.GetRemixNucleiGainSetting() + 1)
            self.sliderNucleiGain.SetValue(
                self.settings.GetRemixNucleiGainSetting())
            self.textCtrlNucleiGain.SetValue(
                "%.2f" % self.settings.GetRemixNucleiGain())
            self.recomputeRemix = True
    
    def OnSpinButtonNucleiGainSpinDown(self, event):
        if self.settings.GetRemixBackgroundGainSetting() > 0:
            self.settings.SetRemixNucleiGainSetting(
                self.settings.GetRemixNucleiGainSetting() - 1)
            self.sliderNucleiGain.SetValue(
                self.settings.GetRemixNucleiGainSetting())
            self.textCtrlNucleiGain.SetValue(
                "%.2f" % self.settings.GetRemixNucleiGain())
            self.recomputeRemix = True            

    ### Gamma
    def OnSliderNucleiGammaScrollThumbtrack(self, event):
        # Update Text Control
        self.settings.SetRemixNucleiGammaSetting(
            self.sliderNucleiGamma.GetValue())
        self.textCtrlNucleiGamma.SetValue(
            "%.2f" % self.settings.GetRemixNucleiGamma())
        
    def OnSliderNucleiGammaScrollThumbrelease(self, event):
        # Update Remix
        self.recomputeRemix = True                    
        
    def OnSpinButtonNucleiGammaSpinUp(self, event):
        if self.settings.GetRemixBackgroundGammaSetting() < 100:
            self.settings.SetRemixNucleiGammaSetting(
                self.settings.GetRemixNucleiGammaSetting() + 1)
            self.sliderNucleiGamma.SetValue(
                self.settings.GetRemixNucleiGammaSetting())
            self.textCtrlNucleiGamma.SetValue(
                "%.2f" % self.settings.GetRemixNucleiGamma())
            self.recomputeRemix = True            
    
    def OnSpinButtonNucleiGammaSpinDown(self, event):
        if self.settings.GetRemixBackgroundGammaSetting() > 0:
            self.settings.SetRemixNucleiGammaSetting(
                self.settings.GetRemixNucleiGammaSetting() - 1)
            self.sliderNucleiGamma.SetValue(
                self.settings.GetRemixNucleiGammaSetting())
            self.textCtrlNucleiGamma.SetValue(
                "%.2f" % self.settings.GetRemixNucleiGamma())
            self.recomputeRemix = True            
        
    ## Remix Mode        
    def OnChoiceRemixModeChoice(self, event):
        if (self.settings.GetRemixRemixMode() 
            != self.choiceRemixMode.GetSelection()):
            self.settings.SetRemixRemixMode(
                self.choiceRemixMode.GetSelection())
            self.recomputeRemix = True
            
    def RefreshBackgroundColorButtons(self):
        self.colorButtonBackgroundColor.SetBackgroundColour(
            self.settings.GetRemixBackgroundColor())
        self.colorButtonBackgroundColor.Refresh()
        self.colorButtonBackgroundSpectrum.SetBackgroundColour(
            self.settings.GetRemixBackgroundSpectrum())
        self.colorButtonBackgroundSpectrum.Refresh()
        
    def RefreshNucleiColorButtons(self):
        self.colorButtonNucleiColor.SetBackgroundColour(
            self.settings.GetRemixNucleiColor())
        self.colorButtonNucleiColor.Refresh()
        self.colorButtonNucleiSpectrum.SetBackgroundColour(
            self.settings.GetRemixNucleiSpectrum())
        self.colorButtonNucleiSpectrum.Refresh()            

    
if __name__ == "__main__":
    app = wx.App()
    frame = wx.Frame(None,title = "Test Frame")
    frame.SetSize((600, 400))
    unmixPanel = RemixPanel(frame)
    frame.Show()
    app.MainLoop()