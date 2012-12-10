import wx
from wxPython.wx import *
from wx import EmptyIcon

    
class WootIcon(wx.TaskBarIcon):

    def __init__(self,frame):
        wx.TaskBarIcon.__init__(self)
        self.frame = frame
        
        png = wx.Bitmap("robot.png",wx.BITMAP_TYPE_PNG)

        icon = EmptyIcon()
        icon.CopyFromBitmap(png)

        self.tbIcon = icon
        self.SetIcon(self.tbIcon,"Woot Boy")

    def OnTaskBarActivate(self, evt):
        pass

    def OnTaskBarClose(self,evt):
        self.frame.Close()

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(100,"&Start","Start")
        menu.Append(101,"S&top","Stop")
        menu.Append(102,"&Close","Close")
        EVT_MENU(self,100,self.frame.PopupAction)
        EVT_MENU(self,101,self.frame.Stop)
        EVT_MENU(self,102,self.frame.onClose)
        self.PopupMenu(menu)
        menu.Destroy()
        

