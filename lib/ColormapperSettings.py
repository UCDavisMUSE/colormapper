import numpy as np

class ColormapperSettings:
    """
    This class stores settings for the colormapper app, 
    as well as Get and Set methods to adjust the settings.
    """
    # Defaults
    # For Unmixing:
    unmix = {
        "backgroundColor": (244, 205, 100),
        "backgroundSpectrum": (113, 95, 46),
        "nucleiColor": (228, 250, 166),
        "nucleiSpectrum": (90, 99, 66),
        "subtractBackground": False,
        "subtractBackgroundAmount": 0
        }
    # For Remixing:
    remix = {
        "backgroundColor": (230, 160, 200),
        "backgroundSpectrum": (99, 69, 86),
        "backgroundBrightness": 0,
        "backgroundBrightnessSetting": 0,
        "backgroundContrast": 1.0,
        "backgroundContrastSetting": 50,
        "backgroundGamma": 1.0,
        "backgroundGammaSetting": 50,
        "nucleiColor": ( 70,  30, 150),
        "nucleiSpectrum": (71, 31, 153),
        "nucleiBrightness": 0,
        "nucleiBrightnessSetting": 0,
        "nucleiContrast": 1.0,
        "nucleiContrastSetting": 50,
        "nucleiGamma": 1.0,
        "nucleiGammaSetting": 50,
        "remixMode": 0,
        "brightnessValuesStart": 0,
        "brightnessValuesEnd": 2,
        "contrastValuesStart": -0.5,
        "contrastValuesEnd": 0.5,
        "gammaValuesStart": -1,
        "gammaValuesEnd": 1,
        }
    

    # Class defaults able to be overwritten when instantiated
    def __init__(self, unmix = unmix, remix = remix):
        self.unmix = unmix
        self.remix = remix
        self.brightnessValues = np.linspace(
            self.remix["brightnessValuesStart"],
            self.remix["brightnessValuesEnd"], 101)
        self.contrastValues = np.logspace(
            self.remix["contrastValuesStart"],
            self.remix["contrastValuesEnd"], 101)
        self.gammaValues = np.logspace(
            self.remix["gammaValuesStart"],
            self.remix["gammaValuesEnd"], 101)
        
    # Get Methods
    def GetUnmixSettings(self):
        return self.unmix
    def GetRemixSettings(self): 
        return self.remix
    def GetSettings(self): 
        return (self.GetUnmixSettings(), self.GetRemixSettings())

    ## Unmix
    def GetUnmixBackgroundColor(self): 
        return self.unmix["backgroundColor"]
    def GetUnmixBackgroundSpectrum(self): 
        return self.unmix["backgroundSpectrum"]
    def GetUnmixNucleiColor(self): 
        return self.unmix["nucleiColor"]
    def GetUnmixNucleiSpectrum(self): 
        return self.unmix["nucleiSpectrum"]
    def GetUnmixSubtractBackground(self): 
        return self.unmix["subtractBackground"]
    def GetUnmixSubtractBackgroundAmount(self): 
        return self.unmix["subtractBackgroundAmount"]

    ## Remix
    def GetRemixBackgroundColor(self): 
        return self.remix["backgroundColor"]
    def GetRemixBackgroundSpectrum(self): 
        return self.remix["backgroundSpectrum"]
    def GetRemixBackgroundBrightness(self): 
        return self.remix["backgroundBrightness"]
    def GetRemixBackgroundBrightnessSetting(self):
        return self.remix["backgroundBrightnessSetting"]
    def GetRemixBackgroundContrast(self):
        return self.remix["backgroundContrast"]
    def GetRemixBackgroundContrastSetting(self): 
        return self.remix["backgroundContrastSetting"]
    def GetRemixBackgroundGamma(self): 
        return self.remix["backgroundGamma"]
    def GetRemixBackgroundGammaSetting(self): 
        return self.remix["backgroundGammaSetting"]
    def GetRemixNucleiColor(self): 
        return self.remix["nucleiColor"]
    def GetRemixNucleiSpectrum(self): 
        return self.remix["nucleiSpectrum"]
    def GetRemixNucleiBrightness(self): 
        return self.remix["nucleiBrightness"]
    def GetRemixNucleiBrightnessSetting(self):
        return self.remix["nucleiBrightnessSetting"]
    def GetRemixNucleiContrast(self): 
        return self.remix["nucleiContrast"]
    def GetRemixNucleiContrastSetting(self): 
        return self.remix["nucleiContrastSetting"]
    def GetRemixNucleiGamma(self): 
        return self.remix["nucleiGamma"]
    def GetRemixNucleiGammaSetting(self): 
        return self.remix["nucleiGammaSetting"]
    def GetRemixRemixMode(self): 
        return self.remix["remixMode"]
    def GetRemixBrightnessValuesStart(self):
        return self.remix["brightnessValuesStart"]
    def GetRemixBrightnessValuesEnd(self):
        return self.remix["brightnessValuesStart"]
    def GetRemixContrastValuesStart(self): 
        return self.remix["contrastValuesStart"]
    def GetRemixContrastValuesEnd(self): 
        return self.remix["contrastValuesEnd"]
    def GetRemixGammaValuesStart(self): 
        return self.remix["gammaValuesStart"]
    def GetRemixGammaValuesEnd(self): 
        return self.remix["gammaValuesEnd"]
  
    # Set Methods
    # Note: I have only written methods for variables that should be set
    # in the interface. Derived attributes will not have (at least for now)
    # public Set methods.
    def SetUnmixSettings(self, unmix): self.unmix = unmix
    def SetRemixSettings(self, remix): self.remix = remix
    def SetSettings(self, unmix, remix):
        self.SetUnmixSettings(unmix)
        self.SetRemixSettings(remix)
    

    ## Unmix
    def SetUnmixBackgroundColor(self, color):
        self.unmix["backgroundColor"] = color
        self.unmix["backgroundSpectrum"] = self.__NormalizeSpectrum(color)

    def SetUnmixNucleiColor(self, color):
        self.unmix["nucleiColor"] = color
        if self.GetUnmixSubtractBackground():
            color = self.__SubtractBackground(color, 
                self.GetUnmixBackgroundColor(), 
                self.GetUnmixSubtractBackgroundAmount())
        self.unmix["nucleiSpectrum"] = self.__NormalizeSpectrum(color)
    
    def SetUnmixSubtractBackground(self, subtractBackground):
        self.unmix["subtractBackground"] = subtractBackground
        # Update the Nuclei Spectrum
        self.SetUnmixNucleiColor(self.GetUnmixNucleiColor())
        
    def SetUnmixSubtractBackgroundAmount(self, subtractBackgroundAmount):
        self.unmix["subtractBackgroundAmount"] = subtractBackgroundAmount
        # Update the Nuclei Spectrum
        self.SetUnmixNucleiColor(self.GetUnmixNucleiColor())        
        
    ## Remix
    def SetRemixBackgroundColor(self, color):
        self.remix["backgroundColor"] = color
        self.remix["backgroundSpectrum"] = self.__NormalizeSpectrum(color)
        
    def SetRemixBackgroundBrightnessSetting(self, brightnessSetting):
        self.remix["backgroundBrightnessSetting"] = brightnessSetting
        self.remix["backgroundBrightness"] = \
            self.brightnessValues[brightnessSetting]
        
    def SetRemixBackgroundContrastSetting(self, contrastSetting):
        self.remix["backgroundContrastSetting"] = contrastSetting
        self.remix["backgroundContrast"] = \
            self.contrastValues[contrastSetting]
        
    def SetRemixBackgroundGammaSetting(self, gammaSetting):
        self.remix["backgroundGammaSetting"] = gammaSetting
        self.remix["backgroundGamma"] = \
            self.gammaValues[gammaSetting]
        
    def SetRemixNucleiColor(self, color):
        self.remix["nucleiColor"] = color
        self.remix["nucleiSpectrum"] = self.__NormalizeSpectrum(color)
        
    def SetRemixNucleiColor(self, color):
        self.remix["nucleiColor"] = color
        self.remix["nucleiSpectrum"] = self.__NormalizeSpectrum(color)
        
    def SetRemixNucleiBrightnessSetting(self, brightnessSetting):
        self.remix["nucleiBrightnessSetting"] = brightnessSetting
        self.remix["nucleiBrightness"] = \
            self.brightnessValues[brightnessSetting]
        
    def SetRemixNucleiContrastSetting(self, contrastSetting):
        self.remix["nucleiContrastSetting"] = contrastSetting
        self.remix["nucleiContrast"] = \
            self.contrastValues[contrastSetting]
        
    def SetRemixNucleiGammaSetting(self, gammaSetting):
        self.remix["nucleiGammaSetting"] = gammaSetting
        self.remix["nucleiGamma"] = \
            self.gammaValues[gammaSetting]
    
    def SetRemixRemixMode(self, remixMode):
        self.remix["remixMode"] = remixMode
        
    # Private Methods
    def __NormalizeSpectrum(self, color):
        """
        Returns a normalized spectrum of the color in the tuple color.
        
        Note that, due to rounding, the result may not always add to 255,
        so do not explicitly rely on this fact.
        """
        if color == (0, 0, 0):
            return color
        else:
            intensity = (color[0] + color[1] + color[2])
            return (
                int(round(255.0*color[0]/intensity)),
                int(round(255.0*color[1]/intensity)),
                int(round(255.0*color[2]/intensity)))
                
    def __SubtractBackground(self, foregroundColor, backgroundColor, amount):
        """
        Subtracts a certain percentage amount of the background color from
        the foreground color. Returns a tuple of integers.
        
        Note that this is not a spectrum and would need to be normalized.
        """
        maxAmount = 255
        for i in range(3):
            if backgroundColor[i] != 0:
                maxAmount = min(maxAmount,
                    1.0*foregroundColor[i]/backgroundColor[i])
        return (
            int(round(foregroundColor[0] 
                - 1.0*(amount/100.0)*maxAmount*backgroundColor[0])),
            int(round(foregroundColor[1] 
                - 1.0*(amount/100.0)*maxAmount*backgroundColor[1])),
            int(round(foregroundColor[2] 
                - 1.0*(amount/100.0)*maxAmount*backgroundColor[2])))
