#!/usr/bin/env python
# sudo mount_nfs -P 192.168.0.2:/volume1/photo /Users/phillips321/nfsmount
import os,sys,Image
try:
    rootdir=sys.argv[1]
except:
    print "Usage: %s directory" % sys.argv[0]
    sys.exit(0)
imageList=[]

# Finds all images of type jpg,png,jpeg,tif,bmp
for path, subFolders, files in os.walk(rootdir):
    for file in files:
        if os.path.splitext(file)[1].lower() == ".jpg" or ".png" or ".jpeg" or ".tif" or ".bmp":
            if "@eaDir" not in path:
                if file != ".DS_Store": imageList.append(os.path.join(path,file))

xlName="SYNOPHOTO:THUMB_XL.jpg" ; xlSize=(1280,1280) #XtraLarge
lName="SYNOPHOTO:THUMB_L.jpg" ; lSize=(800,800) #Large
bName="SYNOPHOTO:THUMB_B.jpg" ; bSize=(640,640) #Big
mName="SYNOPHOTO:THUMB_M.jpg" ; mSize=(320,320) #Medium
sName="SYNOPHOTO:THUMB_S.jpg" ; sSize=(160,160) #Small

for imagePath in imageList:
    imageDir,imageName = os.path.split(imagePath)
    thumbDir=os.path.join(imageDir,"@eaDir",imageName)
    if os.path.isdir(thumbDir) != 1:
        try:os.makedirs(thumbDir)
        except:continue
    image=Image.open(imagePath)
    if os.path.isfile(os.path.join(thumbDir,xlName)) != 1:
        print "Now working on %s : %s" % (imageName,xlName)
        image.thumbnail(xlSize, Image.ANTIALIAS)
        image.save(os.path.join(thumbDir,xlName))
        print "Now working on %s : %s" % (imageName,lName)
        image.thumbnail(lSize, Image.ANTIALIAS)
        image.save(os.path.join(thumbDir,lName))
        print "Now working on %s : %s" % (imageName,bName)
        image.thumbnail(bSize, Image.ANTIALIAS)
        image.save(os.path.join(thumbDir,bName))
        print "Now working on %s : %s" % (imageName,mName)
        image.thumbnail(mSize, Image.ANTIALIAS)
        image.save(os.path.join(thumbDir,mName))
        print "Now working on %s : %s" % (imageName,sName)
        image.thumbnail(sSize, Image.ANTIALIAS)
        image.save(os.path.join(thumbDir,sName))