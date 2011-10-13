from ConfigParser import ConfigParser

class WootConfig(ConfigParser):
    
    config = None
    def init(self):
        self.config = dict(self._sections)
        for k in  self.config:
            self.config[k] = dict(self._defaults,** self.config[k])
            self.config[k].pop('__name__',None)
            
    def getRefresh(self):
        return self.config['woot']['refresh']

    def getBrowser(self):
        return self.config['woot']['browser']
parse = WootConfig()
parse.read("conf/config.ini")
parse.init()
print parse.config
print parse.getRefresh()
print parse.getBrowser()
