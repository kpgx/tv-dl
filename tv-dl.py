import argparse
import scrap
import json
import os

def find_all(sub, a_str):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)

def get_page(url):	
	r = scrap.Render(url)  
	html = r.frame.toHtml()
	
	return str(html)	
	
def scrape(source):
	episodes=[]
	epi_idx=list(find_all('<td class="episode">',source))
	s_name_s=source.find('<a href="index.html">')+21
	s_name_e=source.find('</a>',s_name_s)
	e_name_s=source.find('</a>',s_name_s)+13
	e_name_e=source.find('</td>',s_name_s)
	s_name=source[s_name_s:s_name_e].strip()
	e_name=source[e_name_s:e_name_e].strip()
	fpath=[s_name,e_name]
	for idx in epi_idx:		
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
		e_link_nowvideo_s=source.find('href="http://www.free-tv-video-online.me/player/nowvideo.php?id=',int(idx))+len('href="http://www.free-tv-video-online.me/player/nowvideo.php?id=')	
		e_link_nowvideo_e=e_link_nowvideo_s+13
		if source.find('href="http://www.free-tv-video-online.me/player/nowvideo.php?id=',int(idx))>0:			
			epi_data['hosts'].append('nowvideo')
			epi_data['link']['nowvideo']=source[e_link_nowvideo_s:e_link_nowvideo_e]
		#~ e_link_gorilla_s=source.find('http://www.free-tv-video-online.me/player/gorillavid.php?id=',int(idx))+len('http://www.free-tv-video-online.me/player/gorillavid.php?id=')
		#~ e_link_gorilla_e=e_link_gorilla_s+12
		#~ if source.find('http://www.free-tv-video-online.me/player/gorillavid.php?id=',int(idx))>0:			
			#~ epi_data['hosts'].append('gorilla')
			#~ epi_data['link']['gorilla']=source[e_link_gorilla_s:e_link_gorilla_e]		
		episodes.append(epi_data)
		
	return episodes	
	
def host_link(episodes):
	for episode in episodes:
		if len(episode['link'])>0:
			
			for key in episode['link'].keys():
				if key=='gorilla':
					episode['link']['gorilla']='http://gorillavid.in/'+episode['link']['gorilla']
				if key=='nowvideo':
					episode['link']['nowvideo']='http://www.nowvideo.ch/video/'+episode['link']['nowvideo']
				
	return episodes
	
def file_link():
	pass
	
def write_jason(host_data):
	json.dump(host_data, open("data",'w'))
	
	
def read_jason():
	return json.load(open("data"))
	
def d_axel(f_link,f_path):
	cmd='youtube-dl -g '+f_link+' | xargs axel -a -n 10 -o "'+f_path+'"'	
	return os.system(cmd)
def d_native(f_link,f_path):
	cmd='youtube-dl '+f_link+' -o "'+f_path+'"'
	return os.system(cmd)
	

def download_axel(eps,choices,host):
	ep=eps[0]
	op=os.system('mkdir "'+ep['path'][0]+'" > /dev/null 2> /dev/null')
	op=os.system('mkdir "'+ep['path'][0]+'/'+ep['path'][1]+'" > /dev/null 2> /dev/null')
	count =1
	for ep in eps:
		if host not in ep['hosts']:
			host=ep['hosts'][0]
		f_link=ep['link'][host]
		f_path=ep['path'][0]+'/'+ep['path'][1]+'/'+ep['name']		
		if choices is not None and len(choices)>0:             
			if ep['id'][1:] in choices:
				print('Downloading file (%d/%d)...  '%(count,len(choices)))				
				rv=d_axel(f_link,f_path)
				#~ rv=d_native(f_link,f_path)
				
		else:
			print('Downloading file (%d/%d)...  '%(count,len(eps)))				
			rv=d_axel(f_link,f_path)
			#~ rv=d_native(f_link,f_path)
		if rv!=0:
			return 1		
		count +=1
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
	download_axel(host_data,kwargs['e'],host)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TV series downloader.currently supports only nowvideo host only')
    parser.add_argument('url', type=str, help='Url of the season')    
    parser.add_argument('-e', nargs='+', type=str, help='Episodes')
    parser.add_argument('-H', type=str, help='Hosts')
    args = parser.parse_args()
    main(**vars(args))
