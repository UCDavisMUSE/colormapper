import wx


# This is the class for the main Colormapper App
class ColormapperApp(wx.App):
    def OnInit(self):
        frame = ColormapperFrame()
        frame.Show()
        self.SetTopWindow(frame)
        return True


# This is the class for the main window of the Colormapper App        
class ColormapperFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Colormapper")
        self.SetMinSize((400,300))
        self.SetSize((800,600))


# Start the main loop of the Colormapper App        
if __name__ == '__main__':
    app = ColormapperApp(False)
    app.MainLoop()
    
    

