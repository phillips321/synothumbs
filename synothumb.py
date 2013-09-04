#!/usr/bin/env python
# sudo mount_nfs -P 192.168.0.2:/volume1/photo /Users/phillips321/nfsmount
# Author:       phillips321
# License:      CC BY-SA 3.0
# Use:          home use only, commercial use by permission only
# Released:     www.phillips321.co.uk
# Dependencies: PIL, libjpeg, libpng, dcraw, ffmpeg
# Supports:     jpg, bmp, png, tif
# Version:      3.0
# ChangeLog:
#       v3.0 - Video support 
#       v2.1 - CR2 raw support
#       v2.0 - multithreaded
#       v1.0 - First release
# ToDo:
#       add more raw formats
#       add more movie formats
import os,sys,Image,Queue,threading,time,subprocess,shlex

try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO


#########################################################################
# Settings
#########################################################################
NumOfThreads=8  # Number of threads
startTime=time.time()
imageExtensions=['.jpg','.png','.jpeg','.tif','.bmp','.cr2'] #possibly add other raw types?
videoExtensions=['.mov','.m4v']
xlName="SYNOPHOTO:THUMB_XL.jpg" ; xlSize=(1280,1280) #XtraLarge
lName="SYNOPHOTO:THUMB_L.jpg" ; lSize=(800,800) #Large
bName="SYNOPHOTO:THUMB_B.jpg" ; bSize=(640,640) #Big
mName="SYNOPHOTO:THUMB_M.jpg" ; mSize=(320,320) #Medium
sName="SYNOPHOTO:THUMB_S.jpg" ; sSize=(160,160) #Small

#########################################################################
# Images Class
#########################################################################
class convertImage(threading.Thread):
    def __init__(self,queueIMG):
        threading.Thread.__init__(self)
        self.queueIMG=queueIMG

    def run(self):
        while True:
            self.imagePath=self.queueIMG.get()
            self.imageDir,self.imageName = os.path.split(self.imagePath)
            self.thumbDir=os.path.join(self.imageDir,"@eaDir",self.imageName)
            print "\t[-]Now working on %s" % (self.imagePath)
            if os.path.isfile(os.path.join(self.thumbDir,xlName)) != 1:
                if os.path.isdir(self.thumbDir) != 1:
                    try:os.makedirs(self.thumbDir)
                    except:continue
                
                #Following if statements converts raw images using dcraw first
                if os.path.splitext(self.imagePath)[1].lower() == ".cr2":
                    self.dcrawcmd = "dcraw -c -b 8 -q 0 -w -H 5 '%s'" % self.imagePath
                    self.dcraw_proc = subprocess.Popen(shlex.split(self.dcrawcmd), stdout=subprocess.PIPE)
                    self.raw = StringIO(self.dcraw_proc.communicate()[0])
                    self.image=Image.open(self.raw)
                else:
                    self.image=Image.open(self.imagePath)
    
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
            self.queueIMG.task_done()

#########################################################################
# Video Class
#########################################################################
class convertVideo(threading.Thread):
    def __init__(self,queueVID):
        threading.Thread.__init__(self)
        self.queueVID=queueVID
    
    def run(self):
        while True:
            self.videoPath=self.queueVID.get()
            self.videoDir,self.videoName = os.path.split(self.videoPath)
            self.thumbDir=os.path.join(self.videoDir,"@eaDir",self.videoName)
            if os.path.isfile(os.path.join(self.thumbDir,xlName)) != 1:
                print "Now working on %s" % (self.videoPath)
                if os.path.isdir(self.thumbDir) != 1:
                    try:os.makedirs(self.thumbDir)
                    except:continue
                
                # Following statements converts video to flv using ffmpeg
                self.ffmpegcmd = "ffmpeg -loglevel panic -i '%s' -y -ar 44100 -r 12 -ac 2 -f flv -qscale 5 -s 320x180 -aspect 320:180 '%s/SYNOPHOTO:FILM.flv'" % (self.videoPath,self.thumbDir)
                self.ffmpegproc = subprocess.Popen(shlex.split(self.ffmpegcmd), stdout=subprocess.PIPE)
                self.ffmpegproc.communicate()[0]
            
                # Create video thumbs
                self.tempThumb=os.path.join("/tmp",os.path.splitext(self.videoName)[0]+".jpg")
                self.ffmpegcmdThumb = "ffmpeg -loglevel panic -i '%s' -y -an -ss 00:00:03 -an -r 1 -vframes 1 '%s'" % (self.videoPath,self.tempThumb)
                self.ffmpegThumbproc = subprocess.Popen(shlex.split(self.ffmpegcmdThumb), stdout=subprocess.PIPE)
                self.ffmpegThumbproc.communicate()[0]
                self.image=Image.open(self.tempThumb)
                self.image.thumbnail(xlSize)
                self.image.save(os.path.join(self.thumbDir,xlName))
                self.image.thumbnail(mSize)
                self.image.save(os.path.join(self.thumbDir,mName))
            
            self.queueVID.task_done()

#########################################################################
# Main
#########################################################################
def main():
    queueIMG = Queue.Queue()
    queueVID = Queue.Queue()
    try:
        rootdir=sys.argv[1]
    except:
        print "Usage: %s directory" % sys.argv[0]
        sys.exit(0)

    # Finds all images of type in extensions array
    imageList=[]
    print "[+] Looking for images and populating queue (This might take a while...)"
    for path, subFolders, files in os.walk(rootdir):
        for file in files:
            ext=os.path.splitext(file)[1].lower()
            if any(x in ext for x in imageExtensions):#check if extensions matches ext
                if "@eaDir" not in path:
                    if file != ".DS_Store" and file != ".apdisk" and file != "Thumbs.db": # maybe remove
                        imageList.append(os.path.join(path,file))

    print "[+] We have found %i images in search directory" % len(imageList)
    raw_input("\tPress Enter to continue or Ctrl-C to quit")

    #spawn a pool of threads
    for i in range(NumOfThreads): #number of threads
        t=convertImage(queueIMG)
        t.setDaemon(True)
        t.start()

    # populate queue with Images
    for imagePath in imageList:
        queueIMG.put(imagePath)

    queueIMG.join()


    # Finds all videos of type in extensions array
    videoList=[]
    print "[+] Looking for videos and populating queue (This might take a while...)"
    for path, subFolders, files in os.walk(rootdir):
        for file in files:
            ext=os.path.splitext(file)[1].lower()
            if any(x in ext for x in videoExtensions):#check if extensions matches ext
                if "@eaDir" not in path:
                    if file != ".DS_Store" and file != ".apdisk" and file != "Thumbs.db": #maybe remove?
                        videoList.append(os.path.join(path,file))

    print "[+] We have found %i videos in search directory" % len(videoList)
    raw_input("\tPress Enter to continue or Ctrl-C to quit")

    #spawn a pool of threads
    for i in range(NumOfThreads): #number of threads
        v=convertVideo(queueVID)
        v.setDaemon(True)
        v.start()

    # populate queueVID with Images
    for videoPath in videoList:
        queueVID.put(videoPath) # could we possibly put this instead of videoList.append(os.path.join(path,file))

    queueVID.join()

    endTime=time.time()
    print "Time to complete %i" % (endTime-startTime)

    sys.exit(0)

if __name__ == "__main__":
    main()







