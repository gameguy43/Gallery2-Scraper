# gallery2 scraper
# by D. Parker Phinney
# http://madebyparker.com
# i@madebyparker.com
# no rights reserved.  sharing is caring.

import os
import urllib2
import urllib
import BeautifulSoup
import re

BASE_URL='http://madebyparker.com/gallery/'
#where we'll dump our scrape
#should be relative to the working directory
#no trailing slash
SCRAPE_DEST='images'

def mkdir(dirname):
	if not os.path.isdir("./" + dirname + "/"):
		os.mkdir("./" + dirname + "/")


def gallery_importantHTMLsoup(url):
	fd = urllib2.urlopen(url)
	response = fd.read()
	soup = BeautifulSoup.BeautifulSoup(response)
	#grab everything in the sort of main part of the page 
	#gallery_contents = soup('div', "gsContentAlbum")[0]
	gallery_contents = soup('div', id="gsContent")[0]
	return gallery_contents

def image_importantHTMLsoup(url):
	fd = urllib2.urlopen(url)
	response = fd.read()
	soup = BeautifulSoup.BeautifulSoup(response)
	#grab everything in the sort of main part of the page 
	gallery_contents = soup('div', "gsContentPhoto")[0]
	return gallery_contents



def scrape_gallery():
	mkdir(SCRAPE_DEST)
	#splash page with list of galleries
	gallery_contents = gallery_importantHTMLsoup(BASE_URL + 'main.php')
	gallery_thumbs = gallery_contents('img', "ImageFrame_none giThumbnail")
	print gallery_thumbs
	i = 1;
	#descending into each gallery...
	for outerThumbImg in gallery_thumbs:
		innerGalleryURL = outerThumbImg.parent["href"]
		innerGalleryName = outerThumbImg.parent.parent.parent('p', "giTitle")[0].string
		mkdir(SCRAPE_DEST + '/' + innerGalleryName)
		there_is_another_page = 1 
		#iterating through pages...
		while there_is_another_page:
			innerGallerySoup = gallery_importantHTMLsoup(BASE_URL + innerGalleryURL)
			innerGallery_thumbs = innerGallerySoup('img', "ImageFrame_none giThumbnail")
			
			#going into each image's page...
			for innerThumbImg in innerGallery_thumbs:
				ImgPageSoup = image_importantHTMLsoup(BASE_URL + innerThumbImg.parent["href"])
				#grab the url for the full size image
				theImgURL = ImgPageSoup('a', title="Full Size")[0]['href']
				theImgDesc = ImgPageSoup('img', "ImageFrame_none")[0]['alt']

				print theImgDesc
				urllib.urlretrieve(BASE_URL + theImgURL, SCRAPE_DEST + '/' + innerGalleryName + '/' + theImgDesc)
				print "done"
				i+=1
			nextLinks = innerGallerySoup('a', title="Next")
			if (len(nextLinks) >= 1):
				innerGalleryURL = nextLinks[0]['href'] 
			else:
				there_is_another_page = 0
	return 

if __name__ == '__main__':
    scrape_gallery()
