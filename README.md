% TV-DL

# NAME
tv-dl - Cli script for download multiple videos at once from video hosting sites

# SYNOPSIS
**tv-dl** [OPTIONS] URL [URL...]

# DESCRIPTION
**tv-dl** is a small command-line program to download multiple videos from
http://www.free-tv-video-online.me. Best suitable for downloading the whole season at once. 
It requires the Python interpreter, version 2.7 + python-qt4. 
It currently tested on linux/gnu system.

# REQUIRMENTS

	**axel**		http://axel.alioth.debian.org/
	**python-qt4**	https://wiki.python.org/moin/PyQt4
	**youtube-dl**	http://rg3.github.io/youtube-dl/

To install the requirments in ubuntu $sudo apt-get install "package-name"

# OPTIONS
    -h, --help                 	print this help text and exit
    -H 							specify the prefered host. If the prefered host
								doesn't available it'll automaticaly fall back to available host
								(currently supports novamov,nowvideo)
	-e							specify the episodes you want to download.
								default it'll download all the available downloads
								
Examples

	$tv-dl http://www.free-tv-video-online.me/internet/two_and_a_half_men/season_6.html
		-will download all the available episodes with any available host
	$tv-dl http://www.free-tv-video-online.me/internet/two_and_a_half_men/season_6.html -e 1 2 3
		-will download episode 1,2,3 with any available host
	$tv-dl http://www.free-tv-video-online.me/internet/two_and_a_half_men/season_6.html -e 1 2 3 -H novamov
		-will download episode 1,2,3 from novamov if available, else any available host
		
