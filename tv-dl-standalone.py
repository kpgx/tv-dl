import urllib2
from t0mm0.common.net import Net
#~ import re

def novamov(url):
    net = Net()
    page=get_source(url)
    test_key = '175.157.195.24-1c5ff7beee30aaa3b55f13fa496ab5a6'
    test_id='4rurhn9x446jj'
    #~ print file_key,len(file_key)
    video_id= get_item('file="',page,len(test_id))
    file_key = get_item('flashvars.filekey="',page,len(test_key))
    api = 'http://www.novamov.com/api/player.api.php?key=175.157.195.24-1c5ff7beee30aaa3b55f13fa496ab5a6&file=4rurhn9x446jj'
    api_response=net.http_GET(api).content
    print api_response
    
    #~ print file_key,len(file_key)
    #~ pass
    #~ valid_url=r'http://(?:(?:www\.)?novamov\.com/video/|(?:(?:embed|www)\.)novamov\.com/embed\.php\?v=)(?P<videoid>[a-z\d]{13})'
    #~ mobj = re.match(valid_url, url)
    #~ video_id = mobj.group('videoid')
    
def nowvideo(url):
    pass
def videoweed(url):
    pass
def gorilla(url):
    pass
def main():
    pass    
def get_source(url):  
    #~ url='http://www.novamov.com/video/4rurhn9x446jj'
    #~ url='http://www.free-tv-video-online.me/internet/true_blood/season_1.html'
    response = urllib2.urlopen(url)
    page_source = response.read()
    return page_source

def get_item(key,source,length):
    st=source.find(key)+len(key)
    end=st+length
    return source[st:end]
    

url='http://www.free-tv-video-online.me/internet/true_blood/season_1.html'
url='http://www.novamov.com/video/afdad9e2dcfe7'
#~ url='http://www.nowvideo.ch/video/dl945o23o8bvn'
#~ url='http://gorillavid.in/v8n2x2y0rp07'


novamov(url)
