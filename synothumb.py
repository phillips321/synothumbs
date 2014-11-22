#!/usr/bin/env python
# sudo mount_nfs -P 192.168.0.2:/volume1/photo /Users/phillips321/nfsmount
# Author:       phillips321
# License:      CC BY-SA 3.0
# Use:          home use only, commercial use by permission only
# Released:     www.phillips321.co.uk
# Dependencies: PIL, libjpeg, libpng, dcraw, ffmpeg
# Supports:     jpg, bmp, png, tif
# Version:      5.0
# ChangeLog:
#       v5.0 - addition of PREVIEW thumbnail type; check for proper video conversion command
#       v4.0 - addition of autorate (thanks Markus Luisser)
#       v3.1 - filename fix (_ instead of :) and improvement of rendering (antialias and quality=90 - thanks to alkopedia)
#       v3.0 - Video support 
#       v2.1 - CR2 raw support
#       v2.0 - multithreaded
#       v1.0 - First release
# ToDo:
#       add more raw formats
#       add more movie formats
import os,sys,Image,Queue,threading,time,subprocess,shlex,ImageChops

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
videoExtensions=['.mov','.m4v','mp4']
xlName="SYNOPHOTO_THUMB_XL.jpg" ; xlSize=(1280,1280) #XtraLarge
lName="SYNOPHOTO_THUMB_L.jpg" ; lSize=(800,800) #Large
bName="SYNOPHOTO_THUMB_B.jpg" ; bSize=(640,640) #Big
mName="SYNOPHOTO_THUMB_M.jpg" ; mSize=(320,320) #Medium
sName="SYNOPHOTO_THUMB_S.jpg" ; sSize=(160,160) #Small
pName="SYNOPHOTO_THUMB_PREVIEW.jpg" ; pSize=(120,160) #Preview, keep ratio, pad with black

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

                ###### Check image orientation and rotate if necessary
                ## code adapted from: http://www.lifl.fr/~riquetd/auto-rotating-pictures-using-pil.html
                self.exif = self.image._getexif()
    
                if not self.exif:
                    return False
            
                self.orientation_key = 274 # cf ExifTags
                if self.orientation_key in self.exif:
                    self.orientation = self.exif[self.orientation_key]
            
                    rotate_values = {
                        3: 180,
                        6: 270,
                        8: 90
                    }
            
                    if self.orientation in rotate_values:
                        self.image=self.image.rotate(rotate_values[self.orientation])

                #### end of orientation part

                self.image.thumbnail(xlSize, Image.ANTIALIAS)
                self.image.save(os.path.join(self.thumbDir,xlName), quality=90)
                self.image.thumbnail(lSize, Image.ANTIALIAS)
                self.image.save(os.path.join(self.thumbDir,lName), quality=90)
                self.image.thumbnail(bSize, Image.ANTIALIAS)
                self.image.save(os.path.join(self.thumbDir,bName), quality=90)
                self.image.thumbnail(mSize, Image.ANTIALIAS)
                self.image.save(os.path.join(self.thumbDir,mName), quality=90)
                self.image.thumbnail(sSize, Image.ANTIALIAS)
                self.image.save(os.path.join(self.thumbDir,sName), quality=90)
                self.image.thumbnail(pSize, Image.ANTIALIAS)
                # pad out image
                self.image_size = self.image.size
                self.preview_img = self.image.crop((0, 0, pSize[0], pSize[1]))
                self.offset_x = max((pSize[0] - self.image_size[0]) / 2, 0)
                self.offset_y = max((pSize[1] - self.image_size[1]) / 2, 0)
                self.preview_img = ImageChops.offset(self.preview_img, self.offset_x, self.offset_y)
                self.preview_img.save(os.path.join(self.thumbDir,pName), quality=90)
            self.queueIMG.task_done()

#########################################################################
# Video Class
#########################################################################
class convertVideo(threading.Thread):
    def __init__(self,queueVID):
        threading.Thread.__init__(self)
        self.queueVID=queueVID

    def is_tool(self, name):
        try:
            devnull = open(os.devnull)
            subprocess.Popen([name], stdout=devnull, stderr=devnull).communicate()
        except OSError as e:
            if e.errno == os.errno.ENOENT:
                return False
        return True
    
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
		# Check video conversion command and convert video to flv
                if self.is_tool("ffmpeg"):
			self.ffmpegcmd = "ffmpeg -loglevel panic -i '%s' -y -ar 44100 -r 12 -ac 2 -f flv -qscale 5 -s 320x180 -aspect 320:180 '%s/SYNOPHOTO:FILM.flv'" % (self.videoPath,self.thumbDir) # ffmpeg replaced by avconv on ubuntu
                elif self.is_tool("avconv"):
			self.ffmpegcmd = "avconv -loglevel panic -i '%s' -y -ar 44100 -r 12 -ac 2 -f flv -qscale 5 -s 320x180 -aspect 320:180 '%s/SYNOPHOTO:FILM.flv'" % (self.videoPath,self.thumbDir)
                else: return False
                self.ffmpegproc = subprocess.Popen(shlex.split(self.ffmpegcmd), stdout=subprocess.PIPE)
                self.ffmpegproc.communicate()[0]
            
                # Create video thumbs
                self.tempThumb=os.path.join("/tmp",os.path.splitext(self.videoName)[0]+".jpg")
                if self.is_tool("ffmpeg"):
			self.ffmpegcmdThumb = "ffmpeg -loglevel panic -i '%s' -y -an -ss 00:00:03 -an -r 1 -vframes 1 '%s'" % (self.videoPath,self.tempThumb) # ffmpeg replaced by avconv on ubuntu
                elif self.is_tool("avconv"):
			self.ffmpegcmdThumb = "avconv -loglevel panic -i '%s' -y -an -ss 00:00:03 -an -r 1 -vframes 1 '%s'" % (self.videoPath,self.tempThumb)
                else: return False
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

