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


def createCaption(rawimage, descript, fontsize, left=False, drawBox=True):
	# get a font
	fnt = ImageFont.truetype('arial.ttf', size=fontsize)
	desclength = len(descript)
    # width of the box to measure to decide
    # whether to have black or white text	
	xs, ys = rawimage.size
	# print(xs, ys)
    # create a new Image to contain the text overprinted
	txtbackgcolour = (0,0,0,0)        
	txt = Image.new('RGBA', rawimage.size, txtbackgcolour)
	# get a drawing context
	d = ImageDraw.Draw(txt)
	# find the size the text will be in pixels
	tlength, theight = d.textsize(descript, font=fnt)
	print("text length = {l}px, height= {h}px".format(l=tlength, h=theight))
	if "\n" in descript:
		tmargin = 0.5*theight / len(descript.split("\n"))
	else:
		tmargin = 0.5*theight
	# make the width a bit longer than the box to leave 1/2 textheight at each end
	boxwidth = int(tlength + 2*tmargin)	
	# caption to be at top-right of image unless left=True		        
	if left:
		box = (0,0,boxwidth,theight + 2*tmargin)
	else:
		box = (xs-boxwidth,0,xs,theight + 2*tmargin)
	# extract a region from the image
	region = rawimage.crop(box)
	r,g,b,a = region.split()
	# get band means and percentiles
	meanregion = [numpy.mean(r), numpy.mean(g), numpy.mean(b)]
	print("band means:")
	print(meanregion)
	meanregion = numpy.mean(meanregion)
	print("overall mean pixel value = {m}".format(m=meanregion))
	percentiles = [numpy.percentile(r,[10,90]),
	numpy.percentile(g,[10,90]),
	numpy.percentile(b,[10,90])]
	print("10th and 90th percentiles:")
	print(percentiles)
	p10 = [i[0] for i in percentiles]
	p90 = [i[1] for i in percentiles]
	meanp10 = numpy.mean(p10)
	meanp90 = numpy.mean(p90)	
	# fully opaque text and a partially opaque box
	opac=255
	boxopac = 128
    # if the region is dark, have white text and vice versa
    # if the region is very dark or very light, reduce the opacity of the box
	if meanregion < 100:
		boxopac = int(boxopac * meanp90/255)
		boxcolour = (0,0,0,boxopac)
		txtcolour2 = (255,255,255,opac)
	else:
		boxopac = int(boxopac * (255-meanp10)/255)
		boxcolour = (255,255,255,boxopac)	
		txtcolour2 = (0,0,0,opac)		
	if drawBox:
		# print(box)
		d.rectangle(box,fill=boxcolour,outline=None,width=0)
	# draw text
	if left:
		d.text((tmargin,tmargin), descript, font=fnt, fill=txtcolour2)
	else:	
		d.text((xs-boxwidth + tmargin, tmargin), descript, font=fnt, fill=txtcolour2)
	# overlay on the original image		
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

q = input("Do you have the full-size images (Y/N) in the current directory?")
if q[0].upper() == "Y":
	fullsize = True
else:
	fullsize = False
	
for p in listpics2:
	# get the caption out of the HTML	
	descript = p.a['data-description']
	# the preview filename
	prevfilename = p.a.img['src']
	print(descript)
	desclength = len(descript)
	if fullsize:
	    # expect the full-size images in the same directory as the script
		mainfilename = os.path.split(prevfilename)[1]
		try:
			im = Image.open(mainfilename).convert('RGBA')
		except IOError:
			print("IOError encountered")
		# output at full resolution
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
		#outfile = mainfilename.replace(".png", ".jpg")
		#outfile = os.path.join(outdir, outfile)
		#outfile2 = os.path.join(outdir, subdir, mainfilename.replace(".png", ".jpg"))
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
        # output file name
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
