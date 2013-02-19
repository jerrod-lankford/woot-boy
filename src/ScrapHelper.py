import urllib
from BeautifulSoup import BeautifulSoup
def findProgress(soup):
    #print soup.prettify()
    test = soup.find("div", {"class" : "percent-remaining"})
    if test == None or test.string == "Sold Out":
        return -1
    return test.string.replace("% left","")

def getName(soup):
    tag = soup.find("h2",{"class" : "fn"})
    soup.find()
    if tag == None or tag.string == None:
        return None
    else:
        return str(tag.string)

def getAmount(soup):
    tag = soup.find("span",{"class" : "price"})
    if tag == None or tag.string == None:
        return None
    else:
        return str(tag.string)

def downloadImage(soup,tid):
    img = soup.find("img",{"class" : "photo"})
    if img.has_key('src'):
        urllib.urlretrieve(img['src'],"conf/temp" + str(tid) + ".jpg")

#link is relative
def getWantOneLink(soup):
    linkNode = soup.find("a", {"class" : "wantone  "})
    if linkNode == None:
        return ""
    link = linkNode['href']
    return "www.woot.com" + link
