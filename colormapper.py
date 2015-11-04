import wx


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

        
if __name__ == '__main__':
    app = ColormapperApp(False)
    app.MainLoop()
    
    

