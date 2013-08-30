#!/usr/bin/env python
# sudo mount_nfs -P 192.168.0.2:/volume1/photo /Users/phillips321/nfsmount
# Author:       phillips321
# License:      CC BY-SA 3.0
# Use:          home use only, commercial use by permission only
# Released:     www.phillips321.co.uk
# Dependencies: PIL, libjpeg, libpng
# Supports:     jpg, bmp, png, tif
# Version:      1.0
# ChangeLog:
#       v1.0 - First release
# ToDo:
#       add movie support
import os,sys,Image
#import Queue,threading
#queue = Queue.Queue
extensions=['.jpg','.png','.jpeg','.tif','.bmp']
skipfiles=['.DS_Store','.apdisk','Thumbs.db']
try:
    rootdir=sys.argv[1]
except:
    print "Usage: %s directory" % sys.argv[0]
    sys.exit(0)
imageList=[]

# Finds all images of type in extensions array
for path, subFolders, files in os.walk(rootdir):
    for file in files:
        ext=os.path.splitext(file)[1].lower()
        if any(x in ext for x in extensions):#check if extensions matches ext
            if "@eaDir" not in path:
                if file != ".DS_Store" and file != ".apdisk" and file != "Thumbs.db":
                    print "Now searching thumbs for %s " % (os.path.join(path,file))
                    imageList.append(os.path.join(path,file))

xlName="SYNOPHOTO:THUMB_XL.jpg" ; xlSize=(1280,1280) #XtraLarge
lName="SYNOPHOTO:THUMB_L.jpg" ; lSize=(800,800) #Large
bName="SYNOPHOTO:THUMB_B.jpg" ; bSize=(640,640) #Big
mName="SYNOPHOTO:THUMB_M.jpg" ; mSize=(320,320) #Medium
sName="SYNOPHOTO:THUMB_S.jpg" ; sSize=(160,160) #Small

def convertImage(imagePath):
    image=Image.open(imagePath)
    if os.path.isfile(os.path.join(thumbDir,xlName)) != 1:
        print "Now working on %s" % (imagePath)
        image.thumbnail(xlSize, Image.ANTIALIAS)
        image.save(os.path.join(thumbDir,xlName))
        image.thumbnail(lSize, Image.ANTIALIAS)
        image.save(os.path.join(thumbDir,lName))
        image.thumbnail(bSize, Image.ANTIALIAS)
        image.save(os.path.join(thumbDir,bName))
        image.thumbnail(mSize, Image.ANTIALIAS)
        image.save(os.path.join(thumbDir,mName))
        image.thumbnail(sSize, Image.ANTIALIAS)
        image.save(os.path.join(thumbDir,sName))

for imagePath in imageList:
    imageDir,imageName = os.path.split(imagePath)
    thumbDir=os.path.join(imageDir,"@eaDir",imageName)
    if os.path.isdir(thumbDir) != 1:
        try:os.makedirs(thumbDir)
        except:continue
    convertImage(imagePath)