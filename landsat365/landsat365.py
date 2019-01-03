# module to superimpose captions on the Landsat images from www.landsat365.org
# This website shared a Landsat 8 image of somewhere on Earth every day of 2017
# the website is no longer online as of Jan 2019
# however see Twitter and Instagram @landsat365
# and the index page is accessible via web.archive.org

import os
import numpy
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


def createCaption(rawimage, descript, fontsize, left=False):
	# get a font
	fnt = ImageFont.truetype('arial.ttf', size=fontsize)
	desclength = len(descript)
        # width of the box to measure to decide
        # whether to have black or white text
	boxwidth = int(desclength * fontsize / 1.8 + fontsize*0.75)
	xs, ys = rawimage.size
        # caption to be at top-right of image unless left=True
	if left:
		box = (0,0,boxwidth,ys/12)
	else:
		box = (xs-boxwidth,0,xs,ys/12)
	region = rawimage.crop(box)
	r,g,b,a = region.split()
	meanregion = numpy.mean([numpy.mean(r), numpy.mean(g), numpy.mean(b)])
	print(meanregion)
	
	opac=255
        # if the image is dark, have white text and vice versa
	if meanregion < 100:
		txtcolour = (0,0,0,0)
		txtcolour2 = (255,255,255,opac)
	else:
		txtcolour = (255,255,255,0)	
		txtcolour2 = (0,0,0,opac)	
	txt = Image.new('RGBA', rawimage.size, txtcolour)
	# get a drawing context
	d = ImageDraw.Draw(txt)		
	# draw text
	if left:
		d.text((fontsize*0.7,fontsize*0.7), descript, font=fnt, fill=txtcolour2)
	else:	
		d.text((xs-boxwidth,fontsize*0.7), descript, font=fnt, fill=txtcolour2)
	out = Image.alpha_composite(rawimage, txt)	
	return out

picDir = "."
indexfile = "Landsat365 Retina Wallpapers.html"
# specify output directories
outdir = "output"
outdir = os.path.join(picDir,outdir)
subdir = "1440px"
subdir2 = "preview"
os.chdir(picDir)
os.makedirs(os.path.join(outdir, subdir), exist_ok=True)
os.makedirs(os.path.join(outdir, subdir2), exist_ok=True)


raw = open(indexfile,'r').read()
soup = BeautifulSoup(raw,"lxml")

#print(soup.prettify())

# extract the items from the HTML list
listpics = soup.find_all("ul")
print(len(listpics))
listpics2 = listpics[0].find_all("li")
print(len(listpics2))

# if you have the full-size images, set fullsize=True
# otherwise use the 250px square preview images
# in the _files folder from the index HTML file

# fullsize = True
fullsize = False
for p in listpics2:
	descript = p.a['data-description']
	prevfilename = p.a.img['src']
	print(descript)
	desclength = len(descript)
	if fullsize:
	        #expect the full-size images in the same directory as the script
		mainfilename = os.path.split(prevfilename)[1]
		try:
			im = Image.open(mainfilename).convert('RGBA')
		except IOError:
			print("IOError encountered")
			
		out = createCaption(im, descript, 60)
		print(prevfilename, mainfilename)
		# resize to 1440px
		xs, ys = im.size
		ys2 = 1440
		xs2 = int((ys2/ys) * xs)
		im2 = im.resize((xs2, ys2))
		out2 = createCaption(im2, descript, 48)
		
		# out.show()
		# I encountered jpg problem in Pillow  - don't do conversion for now
		# outfile = mainfilename.replace(".png", ".jpg")
		# outfile = os.path.join(outdir, outfile)
		outfile = os.path.join(outdir, mainfilename)
		outfile2 = os.path.join(outdir, subdir,mainfilename)

		print(outfile)
		if mainfilename != outfile:
			try:
				out.save(outfile)
				out2.save(outfile2)
			except IOError:
				print("cannot convert", mainfilename)
	else:
                # using the preview images
		outfilename = os.path.split(prevfilename)[1]
		try:
			im = Image.open(prevfilename).convert('RGBA')
		except IOError:
			print("IOError encountered")
                # for preview images, start a new line at every comma in caption
                # and write it at the top-left
		descript = descript.replace(",",",\n")
		out = createCaption(im, descript, 16, left=True)		
		print(prevfilename)
		outfile = os.path.join(outdir, subdir2, outfilename)
		if prevfilename != outfile:
			try:
				out.save(outfile)				
			except IOError:
				print("cannot convert", prevfilename)		
	#im.show()
	
	

