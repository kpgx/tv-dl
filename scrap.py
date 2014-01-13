import sys  
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import *  
  
class Render(QWebPage):  
  def __init__(self, url):  
    self.app = QApplication(sys.argv)  
    QWebPage.__init__(self)  
    self.loadFinished.connect(self._loadFinished)  
    self.mainFrame().load(QUrl(url))  
    self.app.exec_()  
  
  def _loadFinished(self, result):  
    self.frame = self.mainFrame()  
    self.app.quit()  
"""
url = 'http://www.free-tv-video-online.me/internet/nypd_blue/season_1.html'  
#~ url = 'http://webscraping.com'
r = Render(url)  
html = r.frame.toHtml()
print type(html)
f=open('test.html','w')
f.write(html)
f.close()
"""
