import wx
import numpy as np
from ColorButton import ColorButton

class RemixPanel(wx.Panel):
    # Data Defaults
    backgroundColor = (230, 160, 200)
    backgroundSpectrum = (99, 69, 86)
    backgroundThresh = 0
    backgroundGain = 1.0
    backgroundGainSetting = 10
    backgroundGamma = 1.0
    backgroundGammaSetting = 50
    nucleiColor = ( 70,  30, 150)
    nucleiSpectrum = (71, 31, 153)
    nucleiThresh = 0
    nucleiGain = 1.0
    nucleiGainSetting = 10
    nucleiGamma = 1.0
    nucleiGammaSetting = 50
    remixMode = 0
    
    # Other variables
    recomputeRemix = False
    gainValues = np.linspace(0,10,101)
    gammaValues = np.logspace(-1,1,101)

    def __init__(self, parent, id = -1):
    
        # Construct Controls
        wx.Panel.__init__(self, parent, id)
        wx.StaticText(self, -1, "Remix Controls:")
        
        # Background
        wx.StaticText(self, -1, "Bulk Tissue:", pos = (0, 25))
        self.colorButtonBackgroundColor = ColorButton(self, -1,
            color = self.backgroundColor, pos = (100, 25),
            size = (20, 20))
        wx.Button(self, -1, label = "+", pos = (125, 19), size = (25, 25))
        wx.StaticText(self, -1, "Spectrum:", pos = (170, 25))
        self.colorButtonBackgroundSpectrum = ColorButton(self, -1,
            color = self.backgroundSpectrum, pos = (250, 25),
            size = (20, 20))
        wx.StaticText(self, -1, "Threshold:", pos = (0, 50))
        self.sliderBackgroundThresh = wx.Slider(self, -1, 
            self.backgroundThresh, 0, 100, pos=(70, 50),
            size=(220, -1),
            style=wx.SL_HORIZONTAL)
        self.spinCtrlBackgroundThresh = wx.SpinCtrl(self, -1,
            str(self.backgroundThresh),
            initial = self.backgroundThresh, min = 0, max = 100,
            pos = (290, 50), size = (100, -1),
            style = wx.SP_ARROW_KEYS)
        wx.StaticText(self, -1, "Gain:", pos = (0, 75))
        self.sliderBackgroundGain = wx.Slider(self, -1,
            self.backgroundGainSetting, 0, 100, pos = (70, 75),
            size = (220, -1),
            style = wx.SL_HORIZONTAL)
        self.textCtrlBackgroundGain = wx.TextCtrl(self, -1,
            value = str(self.gainValues[self.backgroundGainSetting]), 
            pos = (290, 75), size = (83, -1))
        self.spinButtonBackgroundGain = wx.SpinButton(self, -1, 
            pos = (374, 75), size = (-1, -1), 
            style = wx.SB_VERTICAL | wx.SP_WRAP)
        wx.StaticText(self, -1, "Gamma:", pos = (0, 100))
        self.sliderBackgroundGamma = wx.Slider(self, -1, 
            self.backgroundGammaSetting, 0, 100, pos = (70, 100),
            size = (220, -1),
            style = wx.SL_HORIZONTAL)
        self.textCtrlBackgroundGamma = wx.TextCtrl(self, -1,
            value = str(self.gammaValues[self.backgroundGammaSetting]),
            pos = (290, 100), size = (83, -1))
        self.spinButtonBackgroundGamma = wx.SpinButton(self, -1,
            pos = (374, 100), size = (-1, -1),
            style = wx.SB_VERTICAL | wx.SP_WRAP)
        
        # Nuclei
        wx.StaticText(self, -1, "Nuclei:", pos = (0, 125))
        self.colorButtonNucleiColor = ColorButton(self, -1,
            color = self.nucleiColor, pos = (100, 125),
            size = (20, 20))
        wx.Button(self, -1, label = "+", pos = (125, 119), size = (25, 25))
        wx.StaticText(self, -1, "Spectrum:", pos = (170, 125))
        self.colorButtonNucleiSpectrum = ColorButton(self, -1,
            color = self.nucleiSpectrum, pos = (250, 125),
            size = (20, 20))
        wx.StaticText(self, -1, "Threshold:", pos = (0, 150))
        self.sliderNucleiThresh = wx.Slider(self, -1,
            self.nucleiThresh, 0, 100, pos=(70, 150),
            size=(220, -1),
            style=wx.SL_HORIZONTAL)
        self.spinCtrlNucleiThresh = wx.SpinCtrl(self, -1,
            str(self.nucleiThresh),
            initial = self.nucleiThresh, min = 0, max = 100,
            pos = (290, 150), size = (100, -1),
            style = wx.SP_ARROW_KEYS)
        wx.StaticText(self, -1, "Gain:", pos = (0, 175))
        self.sliderNucleiGain = wx.Slider(self, -1,
            self.nucleiGainSetting, 0, 100, pos = (70, 175),
            size = (220, -1),
            style = wx.SL_HORIZONTAL)
        self.textCtrlNucleiGain = wx.TextCtrl(self, -1,
            value = str(self.gainValues[self.nucleiGainSetting]), 
            pos = (290, 175), size = (83, -1))
        self.spinButtonNucleiGain = wx.SpinButton(self, -1, 
            pos = (374, 175), size = (-1, -1), 
            style = wx.SB_VERTICAL | wx.SP_WRAP)
        wx.StaticText(self, -1, "Gamma:", pos = (0, 200))
        self.sliderNucleiGamma = wx.Slider(self, -1, 
            self.nucleiGammaSetting, 0, 100, pos = (70, 200),
            size = (220, -1),
            style = wx.SL_HORIZONTAL)
        self.textCtrlNucleiGamma = wx.TextCtrl(self, -1,
            value = str(self.gammaValues[self.nucleiGammaSetting]),
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
            
        self.Bind(wx.EVT_SCROLL_THUMBTRACK,
            self.OnSliderBackgroundThreshScrollThumbtrack,
            self.sliderBackgroundThresh)
        self.Bind(wx.EVT_SCROLL_THUMBRELEASE,
            self.OnSliderBackgroundThreshScrollThumbrelease,
            self.sliderBackgroundThresh)
        self.Bind(wx.EVT_SPINCTRL, 
            self.OnSpinCtrlBackgroundThreshSpinCtrl,
            self.spinCtrlBackgroundThresh)         
            
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
            
        self.Bind(wx.EVT_SCROLL_THUMBTRACK,
            self.OnSliderNucleiThreshScrollThumbtrack,
            self.sliderNucleiThresh)
        self.Bind(wx.EVT_SCROLL_THUMBRELEASE,
            self.OnSliderNucleiThreshScrollThumbrelease,
            self.sliderNucleiThresh)
        self.Bind(wx.EVT_SPINCTRL, 
            self.OnSpinCtrlNucleiThreshSpinCtrl,
            self.spinCtrlNucleiThresh)              

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

        self.Bind(wx.EVT_CHOICE,
            self.OnChoiceRemixModeChoice,
            self.choiceRemixMode)            

    def OnSliderBackgroundGainScrollThumbtrack(self, event):
        # Update Text Control
        self.backgroundGainSetting = \
            self.sliderBackgroundGain.GetValue()
        self.backgroundGain = self.gainValues[self.backgroundGainSetting]
        self.textCtrlBackgroundGain.SetValue(str(self.backgroundGain))
        
    def OnSliderBackgroundGainScrollThumbrelease(self, event):
        # Update Unmix
        self.recomputeRemix = True                    
        
    def OnSpinButtonBackgroundGainSpinUp(self, event):
        if self.backgroundGainSetting < 100:
            self.backgroundGainSetting += 1
            self.backgroundGain = self.gainValues[self.backgroundGainSetting]
            self.sliderBackgroundGain.SetValue(self.backgroundGainSetting)
            self.textCtrlBackgroundGain.SetValue(str(self.backgroundGain))
            self.recomputeRemix = True
    
    def OnSpinButtonBackgroundGainSpinDown(self, event):
        if self.backgroundGainSetting > 0:
            self.backgroundGainSetting -= 1
            self.backgroundGain = self.gainValues[self.backgroundGainSetting]
            self.sliderBackgroundGain.SetValue(self.backgroundGainSetting)
            self.textCtrlBackgroundGain.SetValue(str(self.backgroundGain))
            self.recomputeRemix = True            

    def OnSliderBackgroundGammaScrollThumbtrack(self, event):
        # Update Text Control
        self.backgroundGammaSetting = \
            self.sliderBackgroundGamma.GetValue()
        self.backgroundGamma = self.gammaValues[self.backgroundGammaSetting]
        self.textCtrlBackgroundGamma.SetValue(str(self.backgroundGamma))
        
    def OnSliderBackgroundGammaScrollThumbrelease(self, event):
        # Update Unmix
        self.recomputeRemix = True                    
        
    def OnSpinButtonBackgroundGammaSpinUp(self, event):
        if self.backgroundGammaSetting < 100:
            self.backgroundGammaSetting += 1
            self.backgroundGamma = self.gammaValues[self.backgroundGammaSetting]
            self.sliderBackgroundGamma.SetValue(self.backgroundGammaSetting)
            self.textCtrlBackgroundGamma.SetValue(str(self.backgroundGamma))
            self.recomputeRemix = True            
    
    def OnSpinButtonBackgroundGammaSpinDown(self, event):
        if self.backgroundGammaSetting > 0:
            self.backgroundGammaSetting -= 1
            self.backgroundGamma = self.gammaValues[self.backgroundGammaSetting]
            self.sliderBackgroundGamma.SetValue(self.backgroundGammaSetting)
            self.textCtrlBackgroundGamma.SetValue(str(self.backgroundGamma))
            self.recomputeRemix = True            

    def OnSliderNucleiGainScrollThumbtrack(self, event):
        # Update Text Control
        self.nucleiGainSetting = \
            self.sliderNucleiGain.GetValue()
        self.nucleiGain = self.gainValues[self.nucleiGainSetting]
        self.textCtrlNucleiGain.SetValue(str(self.nucleiGain))
        
    def OnSliderNucleiGainScrollThumbrelease(self, event):
        # Update Unmix
        self.recomputeRemix = True                    
        
    def OnSpinButtonNucleiGainSpinUp(self, event):
        if self.nucleiGainSetting < 100:
            self.nucleiGainSetting += 1
            self.nucleiGain = self.gainValues[self.nucleiGainSetting]
            self.sliderNucleiGain.SetValue(self.nucleiGainSetting)
            self.textCtrlNucleiGain.SetValue(str(self.nucleiGain))
            self.recomputeRemix = True            
    
    def OnSpinButtonNucleiGainSpinDown(self, event):
        if self.nucleiGainSetting > 0:
            self.nucleiGainSetting -= 1
            self.nucleiGain = self.gainValues[self.nucleiGainSetting]
            self.sliderNucleiGain.SetValue(self.nucleiGainSetting)
            self.textCtrlNucleiGain.SetValue(str(self.nucleiGain))
            self.recomputeRemix = True

    def OnSliderNucleiGammaScrollThumbtrack(self, event):
        # Update Text Control
        self.nucleiGammaSetting = \
            self.sliderNucleiGamma.GetValue()
        self.nucleiGamma = self.gammaValues[self.nucleiGammaSetting]
        self.textCtrlNucleiGamma.SetValue(str(self.nucleiGamma))
        
    def OnSliderNucleiGammaScrollThumbrelease(self, event):
        # Update Unmix
        self.recomputeRemix = True                    
        
    def OnSpinButtonNucleiGammaSpinUp(self, event):
        if self.nucleiGammaSetting < 100:
            self.nucleiGammaSetting += 1
            self.nucleiGamma = self.gammaValues[self.nucleiGammaSetting]
            self.sliderNucleiGamma.SetValue(self.nucleiGammaSetting)
            self.textCtrlNucleiGamma.SetValue(str(self.nucleiGamma))
            self.recomputeRemix = True            
    
    def OnSpinButtonNucleiGammaSpinDown(self, event):
        if self.nucleiGammaSetting > 0:
            self.nucleiGammaSetting -= 1
            self.nucleiGamma = self.gammaValues[self.nucleiGammaSetting]
            self.sliderNucleiGamma.SetValue(self.nucleiGammaSetting)
            self.textCtrlNucleiGamma.SetValue(str(self.nucleiGamma))
            self.recomputeRemix = True            

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
        
    def OnSliderBackgroundThreshScrollThumbtrack(self, event):
        # Update Spin Control
        self.backgroundThresh = \
            self.sliderBackgroundThresh.GetValue()
        self.spinCtrlBackgroundThresh.SetValue(self.backgroundThresh)
    
    def OnSliderBackgroundThreshScrollThumbrelease(self, event):
        # Update Unmix
        self.recomputeRemix = True
    
    def OnSpinCtrlBackgroundThreshSpinCtrl(self, event):
        # Update Slider
        self.backgroundThresh = \
            self.spinCtrlBackgroundThresh.GetValue()
        self.sliderBackgroundThresh.SetValue(self.backgroundThresh)
        self.recomputeRemix = True
        
    def OnSliderNucleiThreshScrollThumbtrack(self, event):
        # Update Spin Control
        self.nucleiThresh = \
            self.sliderNucleiThresh.GetValue()
        self.spinCtrlNucleiThresh.SetValue(self.nucleiThresh)
    
    def OnSliderNucleiThreshScrollThumbrelease(self, event):
        # Update Unmix
        self.recomputeRemix = True
    
    def OnSpinCtrlNucleiThreshSpinCtrl(self, event):
        # Update Slider
        self.nucleiThresh = \
            self.spinCtrlNucleiThresh.GetValue()
        self.sliderNucleiThresh.SetValue(self.nucleiThresh)
        self.recomputeRemix = True        
        
    def OnChoiceRemixModeChoice(self, event):
        if self.remixMode != self.choiceRemixMode.GetSelection():
            self.remixMode = self.choiceRemixMode.GetSelection()
            self.recomputeRemix = True

    
if __name__ == "__main__":
    app = wx.App()
    frame = wx.Frame(None,title = "Test Frame")
    frame.SetSize((600,400))
    unmixPanel = RemixPanel(frame)
    frame.Show()
    app.MainLoop()