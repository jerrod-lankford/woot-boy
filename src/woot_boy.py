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
        frame.Show(true)
        self.SetTopWindow(frame)
        return true

class WootFrame(wxFrame):
    def __init__(self,parent,ID,title):
        wxFrame.__init__(self,parent,ID,title,wxDefaultPosition,wxSize(200,150))
        menu = wxMenu()
        menu.Append(100,"&Popup","Popup")
        menuBar = wxMenuBar()
        menuBar.Append(menu,"&File")
        self.SetMenuBar(menuBar)

        EVT_MENU(self,100,self.PopupAction)

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
        soup = BeautifulSoup(html)
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
            amount = getAmount(soup)
            downloadImage(soup)
            link = ""

            soup = BeautifulSoup(html)
            links = soup.findAll("a")

            #Todo: Play with beautiful soup and find a better way to get the link
            for a in links:
                if a is not None and a.string is not None:
                     if a.string.find("I Want One!") != -1:
                         #TODO: Fix this horrible horrible code
                        try:
                            link = a['href']
                        except:
                            self.timeout = 1;
                            pass
            ##############################################
            self.showPopup(name,amount,progress,link)           
            self.oldName = name
            self.timeout = self.getThreshold(100)
                
    
    def showPopup(self,name,price,progress,link):
        
        #############################################
        bWidth = 200
        bHeight = 100
        tb = TB.ToasterBox(self, TB.TB_COMPLEX, TB.TB_DEFAULT_STYLE, TB.TB_ONTIME)

        tb.SetPopupSize((bWidth,bHeight))
        tb.SetPopupPosition((1680-bWidth,1050-bHeight))
        
        tb.SetPopupPauseTime(6000)
        tb.SetPopupScrollSpeed(8)
        ##############################################
        
        # This Is The New Call Style: The Call To GetToasterBoxWindow()
        # Is Mandatory, In Order To Create A Custom Parent On ToasterBox.
        
        tbpanel = tb.GetToasterBoxWindow()
        panel = wxPanel(tbpanel, -1)

        sizer = wxBoxSizer(wxVERTICAL)
        horsizer1 = wxBoxSizer(wxHORIZONTAL)

        bmp = wx.Bitmap("conf/temp.jpg",wx.BITMAP_TYPE_JPEG)
        image = wx.ImageFromBitmap(bmp)
        image = image.Scale(50,50,wx.IMAGE_QUALITY_HIGH)
        bmp = wx.BitmapFromImage(image)
        stbmp = wxStaticBitmap(panel, -1, bmp)
        horsizer1.Add(stbmp, 0)
        strs = str(name) + " - " +  "$" + str(price) + "\n"
        
        sttext = wxStaticText(panel, -1, strs)
        sttext.SetFont(wxFont(7, wxSWISS, wxNORMAL, wxNORMAL, False, "Verdana"))
        horsizer1.Add(sttext, 1, wxEXPAND | wxLEFT | wxRIGHT, 5)

        hl = hyperlink.HyperLinkCtrl(panel, -1, "Buy Now!",
                                     URL=link)

        sizer.Add((0,5))        
        sizer.Add(horsizer1, 0, wxEXPAND)

        horsizer2 = wxBoxSizer(wxHORIZONTAL)
        horsizer2.Add((5, 0))
        horsizer2.Add(hl, 0, wxEXPAND | wxTOP, 10)
        sizer.Add(horsizer2, 0, wxEXPAND)

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

