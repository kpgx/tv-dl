#!/usr/bin/python2
import argparse
import json
import os
import sys
import urllib2


def find_all(sub, a_str):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)    

def get_page(url):
    response = urllib2.urlopen(url)
    page_source = response.read()
    #~ print page_source
    return page_source

def scrape(source):
    """
    scrape the source page and extract file ids for nowvideo hosted videos
    """
    episodes=[]
    epi_idx=list(find_all('<td class="episode">',source))
    s_name_s=source.find('<a href="index.html">')+21
    s_name_e=source.find('</a>',s_name_s)
    e_name_s=source.find('</a>',s_name_s)+8
    e_name_e=source.find('</td>',s_name_s)
    s_name=source[s_name_s:s_name_e].strip()
    e_name=source[e_name_s:e_name_e].strip()
    fpath=[s_name,e_name]
    c=1
    for idx in epi_idx:        
        st=int(idx)
        if    c<len(epi_idx):
            end=int(epi_idx[c])
        else:
            end=len(source)
        epi_data={}
        epi_data['hosts']=[]
        epi_data['path']=fpath
        epi_data['link']={}
        e_id_s=source.find('<a name="',int(idx))+9
        e_id_e=source.find('"></a>',int(idx))
        epi_data['id']=source[e_id_s:e_id_e]
        e_name_s=source.find('<b>',int(idx))+3
        e_name_e=source.find('</b>',int(idx))
        epi_data['name']=source[e_name_s:e_name_e]
        #nowvideo
        nowvideo='href="http://www.free-tv-video-online.me/player/nowvideo.php?id='
        e_link_nowvideo_s=source.find(nowvideo,st,end)+len(nowvideo)    
        e_link_nowvideo_e=e_link_nowvideo_s+13
        if source.find(nowvideo,st,end)>0:            
            epi_data['hosts'].append('nowvideo')
            epi_data['link']['nowvideo']=source[e_link_nowvideo_s:e_link_nowvideo_e]
        #novamov
        novamov='href="http://www.free-tv-video-online.me/player/novamov.php?id='
        e_link_novamov_s=source.find(novamov,st,end)+len(novamov)    
        e_link_novamov_e=e_link_novamov_s+13
        if source.find(novamov,st,end)>0:            
            epi_data['hosts'].append('novamov')
            epi_data['link']['novamov']=source[e_link_novamov_s:e_link_novamov_e]
        #uncomment below part when gorilla support is restored
        #~ gorilla='http://www.free-tv-video-online.me/player/gorillavid.php?id='
        #~ e_link_gorilla_s=source.find(gorilla,st,end)+len(gorilla)
        #~ e_link_gorilla_e=e_link_gorilla_s+12
        #~ if source.find(gorilla,st,end)>0:            
            #~ epi_data['hosts'].append('gorilla')
            #~ epi_data['link']['gorilla']=source[e_link_gorilla_s:e_link_gorilla_e]
            
        episodes.append(epi_data)
        c+=1
    return episodes    
    
def host_link(episodes):
    """
    create the real links
    """
    for episode in episodes:
        if len(episode['link'])>0:
            
            for key in episode['link'].keys():
                if key=='gorilla':
                    episode['link']['gorilla']='http://gorillavid.in/'+episode['link']['gorilla']
                if key=='nowvideo':
                    episode['link']['nowvideo']='http://www.nowvideo.ch/video/'+episode['link']['nowvideo']
                if key=='novamov':
                    episode['link']['novamov']='http://www.novamov.com/video/'+episode['link']['novamov']
                
    return episodes
    
def file_link():
    pass
    
def write_jason(host_data):
    json.dump(host_data, open("data",'w'))
    
    
def read_jason():
    return json.load(open("data"))
    
def d_axel(f_link,f_path):
    """
    download using axel
    """
    cmd='youtube-dl -g '+f_link+' | xargs axel -a -n 10 -o "'+f_path+'"'
    #~ print cmd
    #~ return 0
    #~ rv=1
    #~ while rv:
    rv=os.system(cmd)
    return rv
    
def d_native(f_link,f_path):
    """
    download using native youtube-dl
    """
    cmd='youtube-dl '+f_link+' -o "'+f_path+'"'
    #~ print cmd
    #~ rv=1
    #~ while rv:
    rv=os.system(cmd)
    return rv
    

def download(eps,choices,host):
    """
    create the command and send it to appropriate downloader
    """
    #~ print eps
    ep=eps[0]
    op=os.system('mkdir "'+ep['path'][0]+'" > /dev/null 2> /dev/null')
    op=os.system('mkdir "'+ep['path'][0]+'/'+ep['path'][1]+'" > /dev/null 2> /dev/null')
    count =1
    #~ print eps
    for ep in eps:
        hst=host
        rv=0
        if host not in ep['hosts'] and len(ep['hosts'])>0:
            hst=ep['hosts'][0]
        f_link=ep['link'][hst]
        f_path=ep['path'][0]+'/'+ep['path'][1]+'/'+ep['name']        
        if choices is not None and len(choices)>0:
            #~ print choices,ep['id'][1:]      
            if ep['id'][1:] in choices:
                print('Downloading file (%d/%d)...  '%(count,len(choices)))                
                rv=d_axel(f_link,f_path)
                #~ rv=d_native(f_link,f_path)
                count +=1
                
        else:
            print('Downloading file (%d/%d)...  '%(count,len(eps)))                
            rv=d_axel(f_link,f_path)
            count +=1            
        if rv!=0:
            return 1        
        #~ count +=1
    print ('download complete')
    
def main(**kwargs):
    host=kwargs['H']
    print 'Getting source...'
    source_page=get_page(kwargs['url'])    
    print 'Scrapping the page...'         
    rough_data=scrape(source_page)
    if len(rough_data)==0:
        print("web page load failed or no downloadable links in web page!")
        return 1        
    host_data=host_link(rough_data)
    #~ for i in host_data:
        #~ print i
    download(host_data,kwargs['e'],host)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TV series downloader.currently supports only nowvideo host only')
    parser.add_argument('url', type=str, help='Url of the season')    
    parser.add_argument('-e', nargs='+', type=str, help='Episodes')
    parser.add_argument('-H', type=str, help='Hosts')
    args = parser.parse_args()
    main(**vars(args))

