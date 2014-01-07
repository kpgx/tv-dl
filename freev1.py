#!/usr/bin/env python

import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os



def find_all(sub, a_str):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)


def browse(args):
    """
    not yet completed
    """
    for key, value in args.items():
        print (key, value)
    driver = webdriver.Chrome()
    driver.get('http://www.free-tv-video-online.me/')
    elem = driver.find_element_by_class_name('dhx_combo_input')
    elem.send_keys(args['name'])
    elem.send_keys(Keys.RETURN)

def browse_by_url(args):
    """
    """
    episodes=[]
    driver = webdriver.Chrome()
    #~ driver = webdriver.Remote("http://localhost:4444/wd/hub", webdriver.DesiredCapabilities.HTMLUNITWITHJS)
    print('Loading web page...')
    driver.get(args['url'])
    source = driver.page_source
    driver.close()
    s_name_s=source.find('<a href="index.html">')+21
    s_name_e=source.find('</a>',s_name_s)
    e_name_s=source.find('</a>',s_name_s)+13
    e_name_e=source.find('</td>',s_name_s)
    s_name=source[s_name_s:s_name_e].strip()
    e_name=source[e_name_s:e_name_e].strip()
    fpath=[s_name,e_name]
    epi_idx=list(find_all('<td class="episode">',source))
    for idx in epi_idx:
        e_id_s=source.find('<a name="',int(idx))+9
        e_id_e=source.find('"></a>',int(idx))
        e_name_s=source.find('<b>',int(idx))+3
        e_name_e=source.find('</b>',int(idx))
        e_link_s=source.find('href="http://www.free-tv-video-online.me/player/nowvideo.php?id=',int(idx))+64
        e_link_e=e_link_s+13
        episodes.append({'id':source[e_id_s:e_id_e],'name':source[e_name_s:e_name_e],'path':fpath,'link_id_nowvideo':source[e_link_s:e_link_e]})
    return episodes
    
def dummy_link_maker(episodes):
    """
    """
    for episode in episodes:
        episode['link_nowvideo']='http://www.nowvideo.ch/video/'+episode['link_id_nowvideo']
    return episodes

def download(eps,choices):
    ep=eps[0]
    op=os.system('mkdir "'+ep['path'][0]+'"')
    op=os.system('mkdir "'+ep['path'][0]+'/'+ep['path'][1]+'"')
    count =1
    for ep in eps:
        
        if choices is not None and len(choices)>0:             
            if ep['id'][1:] in choices:
                print('Downloading file (%d/%d)...'%(count,len(choices)))
                cmd='youtube-dl -g '+ep['link_nowvideo']+' | xargs axel -a -n 10 -o "'+ep['path'][0]+'/'+ep['path'][1]+'/'+ep['name']+'"'
                #~ print (cmd)
                #~ cmd='youtube-dl '+ep['link_nowvideo']
                while 1:
                    op=os.system(cmd)
                    print (op)
                    if op==0 or op==31488:
                        break
                    if op==33280:
                        return 1
                count +=1
        else:
            print('Downloading file (%d/%d)...'%(count,len(eps)))
            cmd='youtube-dl -g '+ep['link_nowvideo']+' | xargs axel -a -n 10 -o "'+ep['path'][0]+'/'+ep['path'][1]+'/'+ep['name']+'"'
            #~ print (cmd)
            #~ cmd='youtube-dl '+ep['link_nowvideo']
            while 1:
                op=os.system(cmd)
                print (op)
                if op==0 or op==31488:
                    break
                if op==33280:
                    return 1
            count +=1
            
    
def main(**kwargs):
    
    #~ print (episodes)
    
    episodes=browse_by_url(kwargs)
    if len(episodes)==0:
        print("web page load failed or no downloadable links in web page!")
        return 1
    episodes_nowvideo=dummy_link_maker(episodes)
    download(episodes_nowvideo,kwargs['e'])
    print('download complete')
    return 0
    #~ print (episodes_nowvideo)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TV series downloader')
    parser.add_argument('url', type=str, help='Url of the season')
    #~ parser.add_argument('-s', type=str, help='Season')
    parser.add_argument('-e', nargs='+', type=str, help='Episodes')
    args = parser.parse_args()
    main(**vars(args))


"""
<a href="/internet/
"></a>

"""
