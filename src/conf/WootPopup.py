import urllib2
import sys
import subprocess
import urllib
from BeautifulSoup import BeautifulSoup
from ConfigParser import ConfigParser
from ScrapHelper import *
import wx
import ToasterBox as TB
from wxPython.wx import *
import wx.lib.hyperlink as hyperlink
from wx.lib.ticker import Ticker
import threading
import thread
import time

class WootBoy(wxApp):
    
    
        
    def OnInit(self):
        frame = WootFrame(NULL,-1,"Woot Boy")
        frame.Show(true)
        self.SetTopWindow(frame)
        return true

class WootFrame(wxFrame):
    
    def __init__(self,parent,ID,title):
        wxFrame.__init__(self,parent,ID,title,wxDefaultPosition,wxSize(200,150))
        
        bWidth = 200
        bHeight = 100
        tb = TB.ToasterBox(TB.TB_COMPLEX, TB.DEFAULT_TB_STYLE, TB.TB_ONTIME)

        tb.SetPopupSize((bWidth,bHeight))
        tb.SetPopupPosition((1600-bWidth,900-bHeight))
        
        tb.SetPopupPauseTime(4000)
        tb.SetPopupScrollSpeed(8)
        
        self.showPopup(tb,"Hey",1,1,"")           
        
        tb.Play()

    
    def showPopup(self,tb,name,price,progress,link):
        
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
        print name
        #name = fixName(name)
        print name
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
           
    def getThreshold(self,progress):
        if progress > 50:
            return 300
        elif progress > 25:
            return 150
        elif progress > 10:
            return 60
        elif progress > 5:
            return 30
        elif progress > 2:
            return 10
        elif progress > 1:
            return 1
        
    def PopupAction(self,event):
  
        event = threading.Event()

        #############################################
        bWidth = 200
        bHeight = 100
        tb = TB.ToasterBox(self, TB.TB_COMPLEX, TB.DEFAULT_TB_STYLE, TB.TB_ONTIME)

        tb.SetPopupSize((bWidth,bHeight))
        tb.SetPopupPosition((1600-bWidth,900-bHeight))
        
        #tb.SetPopupPauseTime(4000)
        tb.SetPopupScrollSpeed(8)
        ##############################################
        
        url = "http://www.woot.com"

        urlhandle = urllib2.urlopen(url)
        html = urlhandle.read()
        soup = BeautifulSoup(html)
        timeout = 0
        oldName = ""
        
        while True:
            progress = findProgress(soup)
            name = getName(soup)
            
            if name is not oldName:
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
                                timeout = 1;
                                pass
                ##############################################
                self.showPopup(tb,name,amount,progress,link)           
        
                tb.Play()
                oldName = name
                
            timeout = self.getThreshold(int(progress))
            print str(progress) + " " + str(timeout)
            
            time.sleep(timeout)
        
    
    
    
        


app = WootBoy(0)
app.MainLoop()

            