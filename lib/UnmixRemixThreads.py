import wx
import threading
import time

class UnmixThread(threading.Thread):
    """
    This class is for spectral unmixing.
    """
    def __init__(self, window):
        threading.Thread.__init__(self)
        self.window = window
        self.timeToQuit = threading.Event()
        self.timeToQuit.clear()

    def stop(self):
        self.timeToQuit.set()
        
    def run(self):
        wx.CallAfter(self.window.LogMessage, "Unmix Started.")
        self.window.UnmixImage()
        if not self.timeToQuit.isSet():
            wx.CallAfter(self.window.UnmixThreadFinished)
            
class RemixThread(threading.Thread):
    """
    This class is for remixing.
    """
    def __init__(self, window):
        threading.Thread.__init__(self)
        self.window = window
        self.timeToQuit = threading.Event()
        self.timeToQuit.clear()
        
    def stop(self):
        self.timeToQuit.set()
        
    def run(self):
        wx.CallAfter(self.window.LogMessage, "Remix Started.")
        self.window.RemixImage()
        if not self.timeToQuit.isSet():
            wx.CallAfter(self.window.RemixThreadFinished)
            
class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title = "Multi-threaded GUI")
        self.unmixThread = []
        self.remixThread = []
        
        panel = wx.Panel(self)
        
        btnSize = (100, -1)
        
        restartUnmixBtn = wx.Button(panel, -1, "Restart Unmix", size = btnSize)
        restartRemixBtn = wx.Button(panel, -1, "Restart Remix", size = btnSize)
        stopUnmixBtn = wx.Button(panel, -1, "Stop Unmix", size = btnSize)
        stopRemixBtn = wx.Button(panel, -1, "Stop Remix", size = btnSize)

        self.log = wx.TextCtrl(panel, -1, "",
                    style = wx.TE_RICH | wx.TE_MULTILINE)
                    
        inner = wx.BoxSizer(wx.HORIZONTAL)
        inner.Add(restartUnmixBtn, 0, wx.RIGHT, 15)
        inner.Add(restartRemixBtn, 0, wx.RIGHT, 15)
        inner.Add(stopUnmixBtn, 0, wx.RIGHT, 15)
        inner.Add(stopRemixBtn, 0, wx.RIGHT, 15)
        
        
        main = wx.BoxSizer(wx.VERTICAL)
        main.Add(inner, 0, wx.ALL, 5)
        main.Add(self.log, 1, wx.EXPAND | wx.ALL, 5)
        panel.SetSizer(main)
        panel.Fit()
        
        self.Bind(wx.EVT_BUTTON, self.OnRestartUnmixBtn, restartUnmixBtn)
        self.Bind(wx.EVT_BUTTON, self.OnRestartRemixBtn, restartRemixBtn)
        self.Bind(wx.EVT_BUTTON, self.OnStopUnmixBtn, stopUnmixBtn)
        self.Bind(wx.EVT_BUTTON, self.OnStopRemixBtn, stopRemixBtn)
        
    def UnmixImage(self):
        # Dummy function
        self.WaitingRoom(2)
        
    def RemixImage(self):
        # Dummy function
        self.WaitingRoom(1)
        
    def WaitingRoom(self, waitTime):
        start = time.time()
        while time.time() - start < waitTime:
            pass
        
    def OnRestartUnmixBtn(self, event):
        if self.remixThread:
            self.StopRemixThread()
        if self.unmixThread:
            self.StopUnmixThread()
        self.StartUnmixThread()

    def OnRestartRemixBtn(self, event):
        if self.unmixThread:
            return # Wait for unmix to finish.
        if self.remixThread:
            self.StopRemixThread()
        self.StartRemixThread()
        
    def OnStopUnmixBtn(self, event):
        self.StopUnmixThread()
        self.StopRemixThread()
        
    def OnStopRemixBtn(self, event):
        self.StopRemixThread()
        
    def StartUnmixThread(self):
        thread = UnmixThread(self)
        self.unmixThread.append(thread)
        thread.start()
    
    def StartRemixThread(self):
        thread = RemixThread(self)
        self.remixThread.append(thread)
        thread.start()
        
    def StopUnmixThread(self):
        if self.unmixThread:
            thread = self.unmixThread[0]
            thread.stop()
            self.unmixThread.remove(thread)
            self.LogMessage("Unmix Stopped!")      
        
    def StopRemixThread(self):
        if self.remixThread:
            thread = self.remixThread[0]
            thread.stop()
            self.remixThread.remove(thread)
            self.LogMessage("Remix Stopped!")
            
    def StopThreads(self):
        self.StopRemixThread()
        self.StopUnmixThread()
        
    def OnCloseWindow(self, evt):
        self.StopThreads()
        self.Destroy()
        
    def LogMessage(self, msg):
        self.log.AppendText(msg + "\n")
        
    def UnmixThreadFinished(self):
        if self.unmixThread:
            thread = self.unmixThread[0]
            self.unmixThread.remove(thread)
        self.LogMessage("Unmix Finished!")    
        self.StartRemixThread()
        
    def RemixThreadFinished(self):
        if self.remixThread:
            thread = self.remixThread[0]
            self.remixThread.remove(thread)
        self.LogMessage("Remix Finished!")
        
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frm = MyFrame()
    frm.Show()
    app.MainLoop()