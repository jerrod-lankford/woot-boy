import urllib
import urllib2
from BeautifulSoup import BeautifulSoup
from ScrapHelper import *
import logging
from wxPython.wx import *
import wx


class WootScrap:

    def __init__(self,url,frame,tid):
        self.url = url
        self.frame = frame
        self.tid=tid
        logging.basicConfig(filename="wootboy.log", format='%(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    def start(self):

        self.timer = wxTimer(self.frame)
        self.frame.Bind(wx.EVT_TIMER,self.run,self.timer)
        
        self.timeout = 1000
        self.timer.Start(self.timeout)
        
        self.oldName = ""
        
    def stop(self):
        self.timer.Stop()
        
    def run(self,event):
        
        urlhandle = urllib2.urlopen(self.url)
        html = urlhandle.read()
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)
        body = soup.find("div",{"id":"content"});
        
        progress = findProgress(body)
        name = self.fixName(getName(body))
        
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
            amount = getAmount(body)
            downloadImage(body,self.tid)
            link = getWantOneLink(body)
            
            ##############################################
            self.frame.showPopup(name,amount,progress,link,self.tid)           
            self.oldName = name
            self.timeout = self.getThreshold(100)

    def getThreshold(self,progress):
        
        if progress > 75:
            return 120
        elif progress > 50:
            return 80
        elif progress > 25:
            return 60
        elif progress > 10:
            return 30
        elif progress > 5:
            return 20
        elif progress > 2:
            return 5
        else:
            return 1
        
    #Crashes if ascii is greater than 127, so strip those out
    def fixName(self,name):
        final = ""
        for a in range(0,len(name)):
            if ord(name[a]) <= 127:
                final+= name[a]
        return final

                       
