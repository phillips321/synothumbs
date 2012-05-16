#!/bin/bash
# Author:	phillips321 contact through phillips321.co.uk
# License:	CC BY-SA 3.0
# Use:		
# Released:	www.phillips321.co.uk
    version=1.0
# ChangeLog:
#	v1.0 - now supports video conversion (mov and avi)
#		- for more formats please contact me with requests as i dont have any sample mpg etc
#		- ffmpeg output is surpressed (>/dev/null)
#	v0.1 - first release

XLname="SYNOPHOTO:THUMB_XL.jpg" ; XLsize="1280x1280";
Lname="SYNOPHOTO:THUMB_L.jpg" ; Lsize="800x800";
Bname="SYNOPHOTO:THUMB_B.jpg" ; Bsize="640x640";
Mname="SYNOPHOTO:THUMB_M.jpg" ; Msize="320x320";
Sname="SYNOPHOTO:THUMB_S.jpg" ; Ssize="160x160";
ORIGIFS=$IFS ; IFS=$(echo -en "\n\b")

makeline(){ printf '%*s\n' "${1:-${COLUMNS:-$(tput cols)}}" "" | tr " " "${2:-#}"; }
#intro
makeline; echo " Welcome to synoThumb.sh version $version"; echo " This script creates the thumbs for a synology"; makeline;

#help message
if [[ $# == 0 ]] ; then makeline; echo " Error: What directory to process?"; echo " Usage: $0 ."; makeline ; exit 1; fi

#main block for pics######################################################
for i in `find ${1} \( -type f -a \( -name "*.JPG" -o -name "*.jpg" -o -name "*.png" -o -name "*.PNG" -o -name "*.jpeg" -o -name "*.JPEG" \) ! -path "*@eaDir*" \)`
do
  picName=`echo "${i}" |  awk -F\/ '{print $NF}'`
  picDir=`echo "${i}" | sed s/"${picName}"//g | sed s/.$//`
  echo "Searching Thumbs For $i"
  [[ !(-d "$picDir"/"@eaDir"/"$picName") ]] && (mkdir -p "$picDir""/@eaDir/""$picName"; chmod 775 "$picDir"/"@eaDir"/"$picName";)
  [[ !(-f "$picDir"/"@eaDir"/"$picName"/"$XLname") ]] && (convert -size $XLsize "$picDir""/""$picName" -resize $XLsize -auto-orient -flatten "$picDir"/"@eaDir"/"$picName"/"$XLname"; echo "   -- "$XLname" thumbnail created";)
  [[ !(-f "$picDir"/"@eaDir"/"$picName"/"$Lname") ]] && (convert -size $XLsize "$picDir""/@eaDir/""$picName""/""$XLname" -auto-orient -resize $Lsize "$picDir""/@eaDir/""$picName""/""$Lname"; echo "   -- "$Lname" thumbnail created";)
  [[ !(-f "$picDir"/"@eaDir"/"$picName"/"$Bname") ]] && (convert -size $Lsize "$picDir""/@eaDir/""$picName""/""$Lname" -auto-orient -resize $Bsize "$picDir""/@eaDir/""$picName""/""$Bname"; echo "   -- "$Bname" thumbnail created";)
  [[ !(-f "$picDir"/"@eaDir"/"$picName"/"$Mname") ]] && (convert -size $Bsize "$picDir""/@eaDir/""$picName""/""$Bname" -auto-orient -resize $Msize "$picDir""/@eaDir/""$picName""/""$Mname"; echo "   -- "$Mname" thumbnail created";)
  [[ !(-f "$picDir"/"@eaDir"/"$picName"/"$Sname") ]] && (convert -size $Msize "$picDir""/@eaDir/""$picName""/""$Mname" -auto-orient -quality 60 -resize $Ssize "$picDir""/@eaDir/""$picName""/""$Sname"; echo "   -- "$Sname" thumbnail created";)
done


#main block for vids####################################################
# mov files
for i in `find ${1} \( -type f -a \( -name "*.MOV" -o -name "*.mov" \) ! -path "*@eaDir*" \)`
do
  vidName=`echo "${i}" |  awk -F\/ '{print $NF}'`
  vidDir=`echo "${i}" | sed s/"${vidName}"//g | sed s/.$//`
  [[ !(-d "$vidDir"/"@eaDir"/"$vidName") ]] && (mkdir -p "$vidDir""/@eaDir/""$vidName"; chmod 775 "$vidDir"/"@eaDir"/"$vidName";)
  echo "Searching video conversions for $i"
  [[ !(-f "$vidDir"/"@eaDir"/"$vidName"/'SYNOPHOTO:FILM.flv') ]] && ( echo "   -- processing "$vidName ; ffmpeg -i "$vidDir""/""$vidName" -s 426x240 -f flv -deinterlace -ab 64k -acodec libmp3lame -ar 44100 "$vidDir"/"@eaDir"/"$vidName"/'SYNOPHOTO:FILM.flv' 2> /dev/null ; echo "   -- "$vidName "flv created";)
  [[ !(-f "$vidDir"/"@eaDir"/"$vidName"/'SYNOPHOTO:FILM_H264.mp4') ]] && ( echo "   -- processing "$vidName ; ffmpeg -i "$vidDir""/""$vidName" -s 426x240 -f flv -deinterlace -ab 64k -acodec libmp3lame -ar 44100 "$vidDir"/"@eaDir"/"$vidName"/'SYNOPHOTO:FILM_H264.mp4' 2> /dev/null ; echo "   -- "$vidName "h264 created";)

  echo "Searching Thumbs For $i"
  [[ !(-f "$vidDir"/"@eaDir"/"$vidName"/"$XLname") ]] && (ffmpeg -i "$vidDir""/""$vidName" -an -ss 00:00:03 -an -r 1 -vframes 1 "$vidDir"/"@eaDir"/"$vidName"/"$XLname" 2> /dev/null ; echo "   -- "$XLname" thumbnail created";)
  [[ !(-f "$vidDir"/"@eaDir"/"$vidName"/"$Lname") ]] && (convert -size $XLsize "$vidDir""/@eaDir/""$vidName""/""$XLname" -auto-orient -resize $Lsize "$vidDir""/@eaDir/""$vidName""/""$Lname"; echo "   -- "$Lname" thumbnail created";)
  [[ !(-f "$vidDir"/"@eaDir"/"$vidName"/"$Bname") ]] && (convert -size $Lsize "$vidDir""/@eaDir/""$vidName""/""$Lname" -auto-orient -resize $Bsize "$vidDir""/@eaDir/""$vidName""/""$Bname"; echo "   -- "$Bname" thumbnail created";)
  [[ !(-f "$vidDir"/"@eaDir"/"$vidName"/"$Mname") ]] && (convert -size $Bsize "$vidDir""/@eaDir/""$vidName""/""$Bname" -auto-orient -resize $Msize "$vidDir""/@eaDir/""$vidName""/""$Mname"; echo "   -- "$Mname" thumbnail created";)
  [[ !(-f "$vidDir"/"@eaDir"/"$vidName"/"$Sname") ]] && (convert -size $Msize "$vidDir""/@eaDir/""$vidName""/""$Mname" -auto-orient -quality 60 -resize $Ssize "$vidDir""/@eaDir/""$vidName""/""$Sname"; echo "   -- "$Sname" thumbnail created";)
done
# avi files
for i in `find ${1} \( -type f -a \( -name "*.AVI" -o -name "*.avi" \) ! -path "*@eaDir*" \)`
do
  vidName=`echo "${i}" |  awk -F\/ '{print $NF}'`
  vidDir=`echo "${i}" | sed s/"${vidName}"//g | sed s/.$//`
  [[ !(-d "$vidDir"/"@eaDir"/"$vidName") ]] && (mkdir -p "$vidDir""/@eaDir/""$vidName"; chmod 775 "$vidDir"/"@eaDir"/"$vidName";)
  echo "Searching video conversions for $i"
  [[ !(-f "$vidDir"/"@eaDir"/"$vidName"/'SYNOPHOTO:FILM_M.mp4') ]] && ( echo "   -- processing "$vidName ; fmpeg -i "$vidDir""/""$vidName" -vcodec libx264 -vpre medium -ar 44100 "$vidDir"/"@eaDir"/"$vidName"/'SYNOPHOTO:FILM_M.mp4' 2> /dev/null ; echo  "   -- "$vidName "mp4 created";)
  [[ !(-f "$vidDir"/"@eaDir"/"$vidName"/'SYNOPHOTO:FILM_MOBILE.mp4') ]] && ( echo "   -- processing "$vidName ; ffmpeg -i "$vidDir""/""$vidName" -vcodec libx264 -vpre medium -ar 44100 -s 320x240 "$vidDir"/"@eaDir"/"$vidName"/'SYNOPHOTO:FILM_MOBILE.mp4' 2> /dev/null ; echo  "   -- "$vidName "mobile mp4 created";)

  echo "Searching Thumbs For $i"
  [[ !(-f "$vidDir"/"@eaDir"/"$vidName"/"$XLname") ]] && (ffmpeg -i "$vidDir""/""$vidName" -an -ss 00:00:03 -an -r 1 -vframes 1 "$vidDir"/"@eaDir"/"$vidName"/"$XLname" 2> /dev/null ; echo "   -- "$XLname" thumbnail created";)
  [[ !(-f "$vidDir"/"@eaDir"/"$vidName"/"$Lname") ]] && (convert -size $XLsize "$vidDir""/@eaDir/""$vidName""/""$XLname" -auto-orient -resize $Lsize "$vidDir""/@eaDir/""$vidName""/""$Lname"; echo "   -- "$Lname" thumbnail created";)
  [[ !(-f "$vidDir"/"@eaDir"/"$vidName"/"$Bname") ]] && (convert -size $Lsize "$vidDir""/@eaDir/""$vidName""/""$Lname" -auto-orient -resize $Bsize "$vidDir""/@eaDir/""$vidName""/""$Bname"; echo "   -- "$Bname" thumbnail created";)
  [[ !(-f "$vidDir"/"@eaDir"/"$vidName"/"$Mname") ]] && (convert -size $Bsize "$vidDir""/@eaDir/""$vidName""/""$Bname" -auto-orient -resize $Msize "$vidDir""/@eaDir/""$vidName""/""$Mname"; echo "   -- "$Mname" thumbnail created";)
  [[ !(-f "$vidDir"/"@eaDir"/"$vidName"/"$Sname") ]] && (convert -size $Msize "$vidDir""/@eaDir/""$vidName""/""$Mname" -auto-orient -quality 60 -resize $Ssize "$vidDir""/@eaDir/""$vidName""/""$Sname"; echo "   -- "$Sname" thumbnail created";)
done

#exit message###################################################
makeline; echo " Now log into DSM and reindex your photos"; echo " (Control Panel --> Media Indexing Service --> Re-index)"; makeline;

IFS=$ORIGIFS;
exit 0