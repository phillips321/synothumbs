#!/usr/bin/env python
# sudo mount_nfs -P 192.168.0.2:/volume1/photo /Users/phillips321/nfsmount
# Author:       phillips321
# License:      CC BY-SA 3.0
# Use:          home use only, commercial use by permission only
# Released:     www.phillips321.co.uk
# Dependencies: PIL, libjpeg, libpng
# Supports:     jpg, bmp, png, tif
# Version:      2.0
# ChangeLog:
#       v2.0 - multithreaded
#       v1.0 - First release
# ToDo:
#       add movie support
#       add CR2 support?
import os,sys,Image,Queue,threading,time
startTime=time.time()
NumOfThreads=8  # Number of threads
extensions=['.jpg','.png','.jpeg','.tif','.bmp'] #possibly add cr2 and other raw types?
skipfiles=['.DS_Store','.apdisk','Thumbs.db'] # file to skip  (not yet implemented)
xlName="SYNOPHOTO:THUMB_XL.jpg" ; xlSize=(1280,1280) #XtraLarge
lName="SYNOPHOTO:THUMB_L.jpg" ; lSize=(800,800) #Large
bName="SYNOPHOTO:THUMB_B.jpg" ; bSize=(640,640) #Big
mName="SYNOPHOTO:THUMB_M.jpg" ; mSize=(320,320) #Medium
sName="SYNOPHOTO:THUMB_S.jpg" ; sSize=(160,160) #Small

queue = Queue.Queue()
try:
    rootdir=sys.argv[1]
except:
    print "Usage: %s directory" % sys.argv[0]
    sys.exit(0)
imageList=[]


# class that performs the thumbnail creation for the image
class convertImage(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue=queue

    def run(self):
        while True:
            self.imagePath=self.queue.get()
            self.imageDir,self.imageName = os.path.split(self.imagePath)
            self.thumbDir=os.path.join(self.imageDir,"@eaDir",self.imageName)
            if os.path.isdir(self.thumbDir) != 1:
                try:os.makedirs(self.thumbDir)
                except:continue
            self.image=Image.open(self.imagePath)
            if os.path.isfile(os.path.join(self.thumbDir,xlName)) != 1:
                print "Now working on %s" % (self.imagePath)
                self.image.thumbnail(xlSize)
                self.image.save(os.path.join(self.thumbDir,xlName))
                self.image.thumbnail(lSize)
                self.image.save(os.path.join(self.thumbDir,lName))
                self.image.thumbnail(bSize)
                self.image.save(os.path.join(self.thumbDir,bName))
                self.image.thumbnail(mSize)
                self.image.save(os.path.join(self.thumbDir,mName))
                self.image.thumbnail(sSize)
                self.image.save(os.path.join(self.thumbDir,sName))
            self.queue.task_done()

# Finds all images of type in extensions array
for path, subFolders, files in os.walk(rootdir):
    for file in files:
        ext=os.path.splitext(file)[1].lower()
        if any(x in ext for x in extensions):#check if extensions matches ext
            if "@eaDir" not in path:
                if file != ".DS_Store" and file != ".apdisk" and file != "Thumbs.db":
                    print "Now searching thumbs for %s " % (os.path.join(path,file))
                    imageList.append(os.path.join(path,file))

#spawn a pool of threads
for i in range(NumOfThreads): #number of threads
    t=convertImage(queue)
    t.setDaemon(True)
    t.start()


for imagePath in imageList:
    queue.put(imagePath)

queue.join()

endTime=time.time()
print "Time to complete %i" % (endTime-startTime)











