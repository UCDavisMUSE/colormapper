import wx
from lib.ColormapperFrame import *

# This is the class for the main Colormapper App
class ColormapperApp(wx.App):
    def OnInit(self):
        frame = ColormapperFrame()
        frame.Show()
        self.SetTopWindow(frame)
        return True

# Start the main loop of the Colormapper App        
if __name__ == '__main__':
    app = ColormapperApp(False)
    app.MainLoop()
    
