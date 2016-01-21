import wx
import wx.lib.buttons as buttons


# This is the class for the main Colormapper App
class ColorButtonTestApp(wx.App):
    def OnInit(self):
        frame = ColorButtonTestFrame()
        frame.Show()
        self.SetTopWindow(frame)
        return True


class ColorButtonTestFrame(wx.Frame):
    def __init__(self):
        self.title = "Color Button Test"
        wx.Frame.__init__(self, None, -1, self.title, size = (400, 400))
        
        # Start with a red button
        color = (255, 0, 0)
        button = ColorButton(self, -1, color, pos = (0,0), size = (20,20))


class ColorButton(wx.lib.buttons.GenButton):
    def __init__(self, parent, id = -1, color = (0, 0, 0), pos = wx.DefaultPosition, 
        size = (30, 30)):
        wx.lib.buttons.GenButton.__init__(self, parent, id = -1, pos = pos, 
            size = size)
        self.SetBackgroundColour(color)
        self.Bind(wx.EVT_BUTTON, self.OnButtonPress, self)

    def OnButtonPress(self, event):
        # Set the initial color of the color dialog
        # box to the current button color
        data = wx.ColourData()
        data.SetChooseFull(True)
        currentColor = self.GetBackgroundColour()
        data.SetColour(
            wx.Colour(currentColor[0], currentColor[1], currentColor[2]))
        # Get the new color from the user
        self.dlg = wx.ColourDialog(self, data)
        if self.dlg.ShowModal() == wx.ID_OK:
            self.color = \
                self.dlg.GetColourData().GetColour()[0:3] # Remove Opacity
            self.SetBackgroundColour(self.color)            
        self.dlg.Destroy()
        event.Skip()
        
# Start the main loop of the ColorButtonTest App
if __name__ == '__main__':
    app = ColorButtonTestApp(False)
    app.MainLoop()
    
    

