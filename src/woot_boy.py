import sys
import wx
import wx.lib.agw.toasterbox as TB
from wxPython.wx import *
import wx.lib.hyperlink as hyperlink
from wx.lib.ticker import Ticker
import threading
import time
from WootIcon import WootIcon


###################################################
#Get the progress from the div, assuming the format stays at:
# <div class="wootOffProgressBarValue" style="width: 34%;"></div>
# then this script should continue to work.
###################################################
    
class WootBoy(wxApp):
    
        
    def OnInit(self):
        frame = WootFrame(NULL,-1,"Woot Boy")
        frame.Show(False)
        self.SetTopWindow(frame)
        
        return true

class WootFrame(wxFrame):
    def __init__(self,parent,ID,title):
        wxFrame.__init__(self,parent,ID,title,wxDefaultPosition,wxSize(200,150))
        self.tbIcon = WootIcon(self)
        self.Bind(wx.EVT_CLOSE,self.onClose)
        
    def onClose(self,evt):
        self.tbIcon.RemoveIcon()
        self.tbIcon.Destroy()
        self.Destroy()            
    
    def showPopup(self,name,price,progress,link,tid):

        res = wx.GetDisplaySize()
        
        #############################################
        bWidth = 200
        bHeight = 100
        tb = TB.ToasterBox(self, TB.TB_COMPLEX, TB.TB_DEFAULT_STYLE, TB.TB_ONTIME)

        tb.SetPopupSize((bWidth,bHeight))
        tb.SetPopupPosition((res[0]-bWidth,res[1]-bHeight))
        
        tb.SetPopupPauseTime(6000)
        tb.SetPopupScrollSpeed(8)
        ##############################################
        
        # This Is The New Call Style: The Call To GetToasterBoxWindow()
        # Is Mandatory, In Order To Create A Custom Parent On ToasterBox.
        
        tbpanel = tb.GetToasterBoxWindow()
        panel = wxPanel(tbpanel, -1)

        sizer = wxBoxSizer(wxVERTICAL)
        horsizer1 = wxBoxSizer(wxHORIZONTAL)

        try:
            bmp = wx.Bitmap("conf/temp"+str(tid)+".jpg",wx.BITMAP_TYPE_ANY)
            image = wx.ImageFromBitmap(bmp)
            height = int((75 / float(image.GetWidth())) * image.GetHeight())
            image = image.Scale(75,height,wx.IMAGE_QUALITY_HIGH)
            bmp = wx.BitmapFromImage(image)
            stbmp = wxStaticBitmap(panel, -1, bmp)
            horsizer1.Add(stbmp, 0)
        except:
            print "cannot display image"
            
        strs = str(name) + " - " + str(price) + "\n"
        
        sttext = wxStaticText(panel, -1, strs)
        sttext.SetFont(wxFont(7, wxSWISS, wxNORMAL, wxNORMAL, False, "Verdana"))
        horsizer1.Add(sttext, 1, wxEXPAND | wxLEFT | wxRIGHT, 5)

        hl = hyperlink.HyperLinkCtrl(panel, -1, "Buy Now!",
                                     URL=link)

        sizer.Add((0,6))        
        sizer.Add(horsizer1, 2, wxEXPAND)

        horsizer2 = wxBoxSizer(wxHORIZONTAL)
        horsizer2.Add((5, 0))
        horsizer2.Add(hl, 0, wxEXPAND | wxTOP, 10)
        sizer.Add(horsizer2, 1, wxEXPAND)

        sizer.Layout()
        panel.SetSizer(sizer)
        
        tb.AddPanel(panel)
        tb.Play()
        
#Thresholds#
#
#initial: 5 minutes
#50%: 2.5 minutes
#25%: 1.5 minutes
#10%: 1 minute
#5%: 30 seconds
#2%: 10 seconds
#1%: 1 second
#

app = WootBoy(0)
app.MainLoop()


