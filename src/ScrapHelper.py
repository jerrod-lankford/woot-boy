import urllib
from BeautifulSoup import BeautifulSoup
def findProgress(soup):
    test = soup.find("div", {"class" : "wootOffProgressBarValue"})
    if test == None:
        return -1
    if test.has_key('style'):
        return test['style'].partition(":")[2].replace('%','')
    else:
        return -1
def getName(soup):
    tag = soup.find("h2",{"class" : "fn"})
    soup.find()
    if tag == None or tag.string == None:
        return None
    else:
        return str(tag.string)

def getAmount(soup):
    tag = soup.find("span",{"class" : "amount"})
    if tag == None or tag.string == None:
        return None
    else:
        return str(tag.string)

def downloadImage(soup):
    img = soup.find("img",{"class" : "photo"})
    if img.has_key('src'):
        urllib.urlretrieve(img['src'],"conf/temp.jpg")
