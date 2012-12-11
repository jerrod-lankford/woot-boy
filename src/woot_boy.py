import urllib2
import sys
import subprocess
import urllib
from BeautifulSoup import BeautifulSoup
from WootConfig import WootConfig
from ConfigParser import ConfigParser
from ScrapHelper import *
import wx
import wx.lib.agw.toasterbox as TB
from wxPython.wx import *
import wx.lib.hyperlink as hyperlink
from wx.lib.ticker import Ticker
import threading
import time
from WootIcon import WootIcon
import logging

###################################################
#Get the progress from the div, assuming the format stays at:
# <div class="wootOffProgressBarValue" style="width: 34%;"></div>
# then this script should continue to work.
###################################################
#Crashes if ascii is greater than 127, so strip those out
def fixName(name):
    final = ""
    for a in range(0,len(name)):
        if ord(name[a]) <= 127:
            final+= name[a]
    return final
    
class WootBoy(wxApp):
    
        
    def OnInit(self):
        frame = WootFrame(NULL,-1,"Woot Boy")
        frame.Show(False)
        self.SetTopWindow(frame)
        logging.basicConfig(filename="wootboy.log", format='%(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
        
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
        
    def getThreshold(self,progress):
        
        if progress > 75:
            return 260
        elif progress > 50:
            return 180
        elif progress > 25:
            return 120
        elif progress > 10:
            return 50
        elif progress > 5:
            return 20
        elif progress > 2:
            return 5
        else:
            return 1


    def Stop(self,event): 
        self.timer.Stop()   
            
    def PopupAction(self,event):

        
        self.timer = wxTimer(self)
        self.Bind(wx.EVT_TIMER,self.run,self.timer)
        
        self.timeout = 1000
        self.timer.Start(self.timeout)
        
        self.oldName = ""
        self.url = "http://www.woot.com"
        
    def run(self,event):
        #event = threading.Event()
        
            
        urlhandle = urllib2.urlopen(self.url)
        html = urlhandle.read()
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)
        progress = findProgress(soup)
        name = fixName(getName(soup))
        
        newTimeout = self.getThreshold(int(progress))
        
        if (newTimeout < self.timeout):
            self.timeout = self.getThreshold(int(progress))
        #self.timer.Stop()
        #print "Timeout: " + str(self.timeout)
        self.timer.Start(self.timeout * 1000)
        
        print str(progress) + " " + str(self.timeout)
        print "Comparing: " + self.oldName + " : " + name 
        if name not in self.oldName:
            logging.debug("Discovered \"%s\" at %s%%" % (name,progress))
            amount = getAmount(soup)
            downloadImage(soup)

            soup = BeautifulSoup(html)
            
            link = getWantOneLink(soup)
            
            ##############################################
            self.showPopup(name,amount,progress,link)           
            self.oldName = name
            self.timeout = self.getThreshold(100)
                
    
    def showPopup(self,name,price,progress,link):

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
            bmp = wx.Bitmap("conf/temp.jpg",wx.BITMAP_TYPE_ANY)
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

#print "Item: " + name + " - " + amount + ". Progress:" + str(progress)
#print "Link: " + link
#app = wx.PySimpleApp()
#frame = ToasterBoxDemo(None)
#frame.Show()
#app.MainLoop()

parse = WootConfig()
parse.read("config.ini")
parse.init()

