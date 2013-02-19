import wx
from wxPython.wx import *
from wx import EmptyIcon
from WootScrap import WootScrap

#Menu ids
ID_START = 100
ID_STOP = 101
ID_CLOSE = 102

#Woot menu check items
WOOT_IDS = [201,202,203,204,205]
urls = ["http://www.woot.com","http://home.woot.com","http://sport.woot.com","http://kids.woot.com","http://wine.woot.com"]
timers = []

class WootIcon(wx.TaskBarIcon):

    def __init__(self,frame):
        wx.TaskBarIcon.__init__(self)
        self.frame = frame
        
        png = wx.Bitmap("robot.png",wx.BITMAP_TYPE_PNG)

        icon = EmptyIcon()
        icon.CopyFromBitmap(png)

        self.tbIcon = icon
        self.SetIcon(self.tbIcon,"Woot Boy")

        self.menu = self.CreateMenu()

    def OnTaskBarActivate(self, evt):
        pass

    def OnTaskBarClose(self,evt):
        self.frame.Close()

    def CreateMenu(self):
        checkMenu = wx.Menu()

        checkMenu.AppendCheckItem(WOOT_IDS[0],"Woot!").Check(True)
        checkMenu.AppendCheckItem(WOOT_IDS[1],"Home")
        checkMenu.AppendCheckItem(WOOT_IDS[2],"Sport")
        checkMenu.AppendCheckItem(WOOT_IDS[3],"Kids")
        checkMenu.AppendCheckItem(WOOT_IDS[4],"Wine")
        
        menu = wx.Menu()
        menu.Append(ID_START,"&Start","Start")
        menu.Append(ID_STOP,"S&top","Stop").Enable(False)

        menu.AppendMenu(200,"Woots",checkMenu)
        menu.Append(ID_CLOSE,"&Close","Close")
        EVT_MENU(self,ID_START,self.start)
        EVT_MENU(self,ID_STOP,self.stop)
        EVT_MENU(self,ID_CLOSE,self.frame.onClose)

        return menu
        
    def CreatePopupMenu(self):
        
        self.PopupMenu(self.menu)
        #menu.Destroy()
        #checkMenu.destroy()

    def start(self,event):
        startItem = self.menu.FindItemById(ID_START)
        stopItem = self.menu.FindItemById(ID_STOP)
        startItem.Enable(False);
        stopItem.Enable(True);

        #Disable woot selection
        for a in range(0,5):
            item = self.menu.FindItemById(WOOT_IDS[a])
            item.Enable(False)
            if item.IsChecked():
                #pass in the thread id to get rid of race condition for temp.jpg
                ws = WootScrap(urls[a],self.frame,a)
                ws.start()
                timers.append(ws)

        

    def stop(self,event):
        startItem = self.menu.FindItemById(ID_START)
        stopItem = self.menu.FindItemById(ID_STOP)
        startItem.Enable(True);
        stopItem.Enable(False);

        #Enable woot selection
        for a in range(0,5):
            item = self.menu.FindItemById(WOOT_IDS[a])
            item.Enable(True)

        #Stop all timers and clear list
        for b in timers:
            b.stop()

        del timers[:]
        

